from token import *
from node import *

class Parser:

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.program()
        
        if(Parser.tokens.actual.type == "endLine"):
            Parser.tokens.selectNext()

        if(Parser.tokens.actual.type == 'EOF'):
            return result

        else:
            raise Exception("Syntactic Error: Last token is not EOP")

    
    def checkType(type, textError):
        if(Parser.tokens.actual.type != type):
            raise Exception(textError)

        Parser.tokens.selectNext()
    

    def checkValue(value, textError):
        if(Parser.tokens.actual.value != value):
            raise Exception(textError)
        
        Parser.tokens.selectNext()
        
    
    @staticmethod
    def term():
        c0 = Parser.factor()
        while Parser.tokens.actual.value in ["*", "/", "AND"]:
            value = Parser.tokens.actual.value
            Parser.tokens.selectNext()                    
            c0 = BinOp(value, [c0, Parser.factor()])
        
        return c0
    
    @staticmethod
    def parseExpression():
        c0 = Parser.term()
        while Parser.tokens.actual.value in ["+", "-", "OR"]:
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

        elif (Parser.tokens.actual.value in ["TRUE" , "FALSE"]):
            temp = Parser.tokens.actual.value
            Parser.tokens.selectNext()

            if(temp == "TRUE"):
                return BolOP(True)
            
            return BolOP(False)

        elif(Parser.tokens.actual.value == "("):
            Parser.tokens.selectNext()
            result = Parser.relExpression() 

            Parser.checkValue(")" , "There is no ')' after the expression." )
            return result            
            
        elif (Parser.tokens.actual.value in ["+", "-", "NOT"] ):
            temp = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return UnOp(temp, [Parser.factor()])

        elif Parser.tokens.actual.type == "char":
            idt = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return CharVal(idt)


        elif(Parser.tokens.actual.value == "INPUT"):
            inp = InputOp("input")
            Parser.tokens.selectNext() 
            return inp 

        else:
            raise Exception("Factor : Syntactic Error")

    @staticmethod
    def statement():
        ## Start IF token
        if(Parser.tokens.actual.value == "IF"):
            Parser.tokens.selectNext()
            l_if = [Parser.relExpression()]

            Parser.checkValue("THEN", "Error: '{0}' is not THEN".format(Parser.tokens.actual.value) )
            Parser.checkType("endLine", "Error: '{0}' is not endLine".format(Parser.tokens.actual.type))

            l1 = []
            while(Parser.tokens.actual.value not in ["END", "ELSE"] ):
                l1.append(Parser.statement())
                Parser.checkType("endLine", "Syntatic Erro: Not endLine")
            
            l_if.append(Stmts("STATEMENTS", l1))

            
            if Parser.tokens.actual.value == "ELSE":    
                l2 = []
                Parser.tokens.selectNext()
                Parser.checkType("endLine", "Error not is endLine") 

                while(Parser.tokens.actual.value != "END" ):
                    l2.append(Parser.statement())
                    Parser.checkType("endLine", "Syntatic Erro: Not endLine")    
                
                l_if.append(Stmts("STATEMENTS", l2))

            Parser.tokens.selectNext()
            Parser.checkValue("IF", "Syntatic Error: not if")

            return ifOp("if", l_if)


        ## Start IDENT token
        elif(Parser.tokens.actual.type == "char"):
            idt = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
        
            Parser.checkValue("=", "Error: '{0}' is not = after identifier".format(Parser.tokens.actual.value))
            
            return AssOP("=", [idt, Parser.relExpression()])
        

        ## Start PRINT Token
        elif(Parser.tokens.actual.value == "PRINT"):
            Parser.tokens.selectNext()
            return UnOp("PRINT", [Parser.parseExpression()])

        
        #Start WHILE Token
        elif(Parser.tokens.actual.value == "WHILE"):
            Parser.tokens.selectNext()
            c0 = Parser.relExpression()
            
            Parser.checkType("endLine", "Error: '{0}' is not endLien".format(Parser.tokens.actual.type))

            l = []
            while(Parser.tokens.actual.value != "WEND"):
                l.append(Parser.statement())
                Parser.checkType("endLine", "Syntatic Error : not is endLine")

     
            Parser.tokens.selectNext()
            
            return WhileOp("WHILE", [c0, Stmts("STATEMENTS", l)])
            
        #Start Dim
        elif(Parser.tokens.actual.value == "DIM"):
            Parser.tokens.selectNext()
            idt = Parser.tokens.actual.value
            
            Parser.checkType("char", "Syntatic Error: not is char")
            Parser.checkValue("AS", "Syntatic Error : not is AS")
            
            return VarDec(children = [Identifier(idt), Parser.Type()])


        return



    @staticmethod
    def program():
        Parser.checkValue("SUB" , "Error not SUB")
        Parser.checkValue("MAIN", "Error not MAIN")
        Parser.checkValue("("   , "Error not (")
        Parser.checkValue(")"   , "Error not )")
        Parser.checkType("endLine", "Error not endLine1")
        
        list_c = []
        while (Parser.tokens.actual.value != "END"):
            list_c.append(Parser.statement())
            Parser.checkType("endLine", "Error not endLine2")

        Parser.tokens.selectNext()

        Parser.checkValue("SUB", "Error not SUB")
        return Stmts("Statement", list_c)
        


    @staticmethod
    def relExpression():
        c0 = Parser.parseExpression()
        value = Parser.tokens.actual.value
        
        if(value in ["=", ">", "<" ]):
            Parser.tokens.selectNext()
            c1 = Parser.parseExpression()
            return BinOp(value, [c0, c1])
        
        return c0

    @staticmethod
    def Type():
        value = Parser.tokens.actual.value 
        if value in ["INTEGER" , "BOOLEAN"]:
            Parser.tokens.selectNext()
            return Tp(value)
        
        raise  Exception("Syntatic Error : Invalide Type") 