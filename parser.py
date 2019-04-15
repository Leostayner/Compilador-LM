from token import *
from node import *

class Parser:

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.statements()
        if(Parser.tokens.actual.type == "endLine"):
            Parser.tokens.selectNext()

        if(Parser.tokens.actual.type == 'EOF'):
            return result

        else:
            raise Exception("Syntactic Error: Last token is not EOP")

    @staticmethod
    def term():
        c0 = Parser.factor()
        while Parser.tokens.actual.value in ["*", "/"]:
            value = Parser.tokens.actual.value
            Parser.tokens.selectNext()                    
            c0 = BinOp(value, [c0, Parser.factor()])
        
        return c0
    
    @staticmethod
    def parseExpression():
        c0 = Parser.term()
        while Parser.tokens.actual.value in ["+", "-"]:
            value = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            c0 = BinOp(value, [c0, Parser.term()])
                
        return c0

    @staticmethod
    def factor():
        if(Parser.tokens.actual.type == "int"):
            result = IntVal(int(Parser.tokens.actual.value)) 
            Parser.tokens.selectNext() 
            return result


        elif(Parser.tokens.actual.value == "("):
            Parser.tokens.selectNext()
            result = Parser.parseExpression() 

            if(Parser.tokens.actual.value != ")"):
                raise Exception("There is no ')' after the expression.")

            Parser.tokens.selectNext()
            return result            
            
        elif Parser.tokens.actual.value == "+":
            Parser.tokens.selectNext()
            return UnOp("+", [Parser.factor()])


        elif Parser.tokens.actual.value == "-": 
            Parser.tokens.selectNext()
            return UnOp("-", [Parser.factor()])


        elif Parser.tokens.actual.type == "char":
            var = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return CharVal(var)


        elif(Parser.tokens.actual.value == "INPUT"):

            ##Node input a definir --------- 

        else:
            raise Exception("Syntactic Error")

    @staticmethod
    def statement():
        if(Parser.tokens.actual.type == "char"):
            var = Var(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            
            if(Parser.tokens.actual.value != "="):
                raise Exception("Error: '{0}' is not = after identifier".format(Parser.tokens.actual.value))
            
            Parser.tokens.selectNext()
            return AssOP("=", [var, Parser.parseExpression()])
        
        
        elif(Parser.tokens.actual.value == "PRINT"):
            Parser.tokens.selectNext()
            return UnOp("PRINT", [Parser.parseExpression()])

        
        elif(Parser.tokens.actual.value == "WHILE"):
            Parser.tokens.selectNext()
            c0 = Parser.relExpression()
            c1 = Parser.statements()

            if(Parser.tokens.actual.value != "WEND"):
                raise Exception("Error: '{0}' is not WEND".format(Parser.tokens.actual.value))
                            
            Parser.tokens.selectNext()
            
            return WhileOp("WHILE", [c0, c1])

        
        elif(Parser.tokens.actual.value == "IF"):
            Parser.tokens.selectNext()
            l = [Parser.relExpression()]

            if(Parser.tokens.actual.value != "THEN"):
                raise Exception("Error: '{0}' is not THEN".format(Parser.tokens.actual.value))
            
            Parser.tokens.selectNext()
            l.append(Parser.statements())

            
            if(Parser.tokens.actual.value == "ELSE"):
                Parser.tokens.selectNext()
                l.append(Parser.statements())


            if(Parser.tokens.actual.value == "END"):
                Parser.tokens.selectNext()

                if(Parser.tokens.actual.value != "IF"):
                    raise Exception("Error: '{0}' is not IF".format(Parser.tokens.actual.value))
                
                Parser.tokens.selectNext()

            else:
                raise Exception("Error: '{0}' is not End".format(Parser.tokens.actual.value))
            ##Node input a definir ---------


            return ifOp("if", l)

        return

    @staticmethod
    def statements():
        list_c =  []
        list_c.append(Parser.statement())

        while Parser.tokens.actual.type == "endLine":
            Parser.tokens.selectNext()
            list_c.append(Parser.statement())
        
        return Stat("Statements", list_c)


    @staticmethod
    def relExpression():
        c0 = Parser.parseExpression()
        
        value = Parser.tokens.actual.value
        if(value in ["=", ">", "<" ]):
            Parser.tokens.selectNext()
        
        else:
            raise Exception("Syntatic Error: {0} invalid BinOp".format(Parser.tokens.actual.type))

        c1 = Parser.parseExpression()
       
        return BinOp(value, [c0, c1])