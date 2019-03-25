from token import *
from node import *

class Parser:

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.parseExpression()

        
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

            if(Parser.tokens.actual.type == ")"):
                Parser.tokens.selectNext()
                return result            
            else:
                raise Exception("There is no ')' after the expression.")


        elif Parser.tokens.actual.type == "+":
            Parser.tokens.selectNext()
            return UnOp("+", [Parser.factor()])


        elif Parser.tokens.actual.type == "-": 
            Parser.tokens.selectNext()
            return UnOp("-", [Parser.factor()])


        else:
            raise Exception("Syntactic Error")