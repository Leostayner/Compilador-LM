from token import *

class Parser:

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.parseExpression()
        
        if(Parser.tokens.actual.type == 'EOF'):
            print(result)

        else:
            raise Exception("Syntactic Error: Last token is not EOP")

    @staticmethod
    def term():
        result = Parser.factor()
        
        while Parser.tokens.actual.type == "*" or Parser.tokens.actual.type == "/":
                    
            if Parser.tokens.actual.type == "*":
                Parser.tokens.selectNext()                    
                result *= int(Parser.factor())

            elif Parser.tokens.actual.type == "/":
                Parser.tokens.selectNext()
                result /= int(Parser.factor())
            
        return result
    
    @staticmethod
    def parseExpression():
        result = int(Parser.term())
        while Parser.tokens.actual.type == "+" or Parser.tokens.actual.type == "-":
            
            if Parser.tokens.actual.type == "+":
                Parser.tokens.selectNext()
                result += int(Parser.term())

            elif Parser.tokens.actual.type == "-":
                Parser.tokens.selectNext()
                result -= int(Parser.term())
                    
        return result


    @staticmethod
    def factor():
        result = 0
        
        if(Parser.tokens.actual.type == "int"):
            result = int(Parser.tokens.actual.value) 
            Parser.tokens.selectNext()
        
        elif(Parser.tokens.actual.type == "("):
            Parser.tokens.selectNext()
            result = int(Parser.parseExpression())

            if(Parser.tokens.actual.type == ")"):
                Parser.tokens.selectNext()
            
            else:
                raise Exception("There is no ')' after the expression.")

        elif Parser.tokens.actual.type == "+":
            Parser.tokens.selectNext()
            result += int(Parser.factor())

        elif Parser.tokens.actual.type == "-": 
            Parser.tokens.selectNext()
            result -= int(Parser.factor())
            
        else:
            raise Exception("Syntactic Error")
            sys.exit()
        
        return result
