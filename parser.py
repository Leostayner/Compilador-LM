from token import *
from node import *

class Parser:

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.program()
        return result
    
    def checkType(type, textError):
        if(Parser.tokens.actual.type != type): raise Exception(textError)
        Parser.tokens.selectNext()
    
    def checkValue(value, textError):
        if(Parser.tokens.actual.value != value): raise Exception(textError)
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
            l_c = []
            idt = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            if(Parser.tokens.actual.value == "("):
                Parser.tokens.selectNext()

                if(Parser.tokens.actual.value != ")"):
                    while True:
                        l_c.append(Parser.relExpression())
                        if(Parser.tokens.actual.value == ","): 
                            Parser.tokens.selectNext()
                            continue
                        break
                
                Parser.checkValue(")", "Error factor 6")
                return FuncCall(idt, l_c)

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

        #Call --- contertar tokens
        elif(Parser.tokens.actual.value == "CALL"):
            lc = []
            Parser.tokens.selectNext()
            
            callName = Parser.tokens.actual.value
            Parser.checkType("char", "Error call1")
            Parser.checkValue("(","Error call 2")
            
            if(Parser.tokens.actual.value != "("):
                while (True):
                    l_c.append(Parser.relExpression())
                    if(Parser.tokens.actual.value == ","): continue
                    break

            Parser.checkValue("(", "Error call 3")
            return FuncCall(callName, l_c)

        return



    @staticmethod
    def program():
        list_c = []
        while(Parser.tokens.actual.type != 'EOF'):
            if(Parser.tokens.actual.value == "SUB"):
                list_c.append(Parser.funcSub())

                if(Parser.tokens.actual.type == "endLine"):
                    Parser.tokens.selectNext()
         
            elif(Parser.tokens.actual.value == "FUNCTION"):
                list_c.append(Parser.funcDec())

                if(Parser.tokens.actual.type == "endLine"):
                    Parser.tokens.selectNext()

            else:
                print(Parser.tokens.actual.type) 
            
                raise Exception("Syntactic Error: Last token is not EOP")
        
        list_c.append(FuncCall("MAIN"))
        return Stmts("STATEMENTS", list_c)
        
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



    @staticmethod
    def funcDec():
        l_c  = [VarDec()]
        l_cn = []

        Parser.checkValue("FUNCTION", "Error funcDec")
        funcName = Parser.tokens.actual.value

        Parser.checkType("char", "Error funcDec")
        Parser.checkValue("(", "Error funcDec2")


        if(Parser.tokens.actual.value != ")"):                
            while(True):
                idt = Parser.tokens.actual.value
                Parser.checkType("char", "Error a1")
                Parser.checkValue("AS", "Error funcDec3")
                l_c.append(VarDec(children = [Identifier(idt), Parser.Type()]))
                
                if(Parser.tokens.actual.value == ","):
                    Parser.tokens.selectNext()
                    continue
                break
        
        Parser.checkValue(")", "Error funcDec4")
        Parser.checkValue("AS","Error funcDec5")
        l_c[0] = (VarDec(children = [Identifier(funcName), Parser.Type()]))

        Parser.checkType("endLine", "Error funcDec6")

        while(Parser.tokens.actual.value != "END"):
            l_cn.append(Parser.statement())
            Parser.checkType("endLine", "erro")
        
        Parser.checkValue("END", "funcDec7")
        Parser.checkValue("FUNCTION", "funcDec8")
        
        l_c.append(Stmts("STATEMENTS", l_cn))
        return FuncDec(funcName, l_c)


    @staticmethod
    def funcSub():
        l_c  = []
        l_cn = []

        Parser.checkValue("SUB", "Mensagem de Erro")
        subName = Parser.tokens.actual.value
        
        Parser.checkType("char", "Error funcDec")
        Parser.checkValue("(", "Error funcSub")
        
        if(Parser.tokens.actual.value != ")"):                
            while(True):
                idt = Parser.tokens.actual.value
                Parser.checktype("char", "Error funcDec3")
                Parser.checkValue("AS", "Error funcDec3")
                l_c.append(VarDec(children = [Identifier(idt), Parser.Type()]))

                if(Parser.tokens.actual.value == ","):
                    Parser.tokens.selectNext()
                    continue
                break

        Parser.checkValue(")", "Error funcDec4")
        Parser.checkType("endLine", "Error funcSub4")

        while(Parser.tokens.actual.value != "END"):
            l_cn.append(Parser.statement())
            Parser.checkType("endLine", "asda")
       
        Parser.checkValue("END", "funcSub5")
        Parser.checkValue("SUB", "funcSub6")

        l_c.append(Stmts("STATEMENTS", l_cn))
        return FuncSub(subName, l_c)