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
        while Parser.tokens.actual.type == "*" or Parser.tokens.actual.type == "/":
            token = Parser.tokens.actual.type
            Parser.tokens.selectNext()                    
            c0 = BinOp(token, [c0, Parser.factor()])
        
        return c0
    
    @staticmethod
    def parseExpression():
        c0 = Parser.term()
        while Parser.tokens.actual.type == "+" or Parser.tokens.actual.type == "-":
            token = Parser.tokens.actual.type
            Parser.tokens.selectNext()
            c0 = BinOp(token, [c0, Parser.term()])
                
        return c0

    @staticmethod
    def factor():
        if(Parser.tokens.actual.type == "int"):
            result = IntVal(int(Parser.tokens.actual.value)) 
            Parser.tokens.selectNext() 
            return result


        elif(Parser.tokens.actual.type == "("):
            Parser.tokens.selectNext()
            result = Parser.parseExpression() 

            if(Parser.tokens.actual.type != ")"):
                raise Exception("There is no ')' after the expression.")

            Parser.tokens.selectNext()
            return result            
            
            

        elif Parser.tokens.actual.type == "+":
            Parser.tokens.selectNext()
            return UnOp("+", [Parser.factor()])


        elif Parser.tokens.actual.type == "-": 
            Parser.tokens.selectNext()
            return UnOp("-", [Parser.factor()])


        elif Parser.tokens.actual.type == "char":
            var = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return CharVal(var)

        else:
            raise Exception("Syntactic Error")

    @staticmethod
    def statement():
        if(Parser.tokens.actual.type == "char"):
            var = Var(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            
            if(Parser.tokens.actual.type != "assig"):
                raise Exception("Error: '{0}' is not = after identifier".format(Parser.tokens.actual.value))
            
            Parser.tokens.selectNext()
            return AssOP("=", [var, Parser.parseExpression()])
        
        elif(Parser.tokens.actual.value == "PRINT"):
            Parser.tokens.selectNext()
            return UnOp("PRINT", [Parser.parseExpression()])

        elif(Parser.tokens.actual.value == "BEGIN"):
            return Parser.statements()

        return

    @staticmethod
    def statements():
        list_c =  []
        
        if(Parser.tokens.actual.value != "BEGIN"):
            raise Exception("Error: token '{0}' is not BEGIN".format(Parser.tokens.actual.value))

        Parser.tokens.selectNext()
        if(Parser.tokens.actual.type != "endLine"):
            raise Exception("Error: '{0}' is not endline after begin".format(Parser.tokens.actual.value))

        Parser.tokens.selectNext()
        while(Parser.tokens.actual.value != "END"):
            list_c.append(Parser.statement())
            
            if(Parser.tokens.actual.type != "endLine"):
                raise Exception("Error: '{0}' is not endline after statement".format(Parser.tokens.actual.value))
            
            Parser.tokens.selectNext()
        
        Parser.tokens.selectNext()
        return Stat("Statements", list_c)