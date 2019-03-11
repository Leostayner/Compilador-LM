#Compilador - LM
#python3

import sys
import re

class Token:

   def __init__(self, type, value):
       self.type  = type
       self.value = value

class Tokenizer:

    def __init__(self, origin):
        self.origin   = origin                       #código fonte que será tokenizado
        self.position = 0                            #posição atual que o Tokenizador está separando
        self.actual   = self.origin[self.position]   #o último token separando

    def selectNext(self):
        ops = ["+", "-", "*", "/", "(", ")"]
        newToken = ""
        type = ""

        if self.position == len(self.origin):
            type = "EOF"
      
        else: 
            while self.origin[self.position] == " ":
                self.position += 1
                
                if self.position == len(self.origin):
                    type = "EOF"
                    self.actual = Token(type, newToken)
                    return
            
            if self.origin[self.position] in ops:
                type = self.origin[self.position]
                self.position += 1
                    

            elif(self.origin[self.position].isdigit()):
                while self.origin[self.position].isdigit():
                    newToken += self.origin[self.position]
 
                    self.position += 1
                    
                    if self.position == len(self.origin):
                        break

                type = "int"
                
        self.actual = Token(type, newToken)
        
class Parser:

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.parseExpression()
        
        if(Parser.tokens.actual.type == 'EOF'):
            print(result)

        else:
            print("last token is not EOP, operation syntactic error")

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
        while Parser.tokens.actual.type == "+" or Parser.tokens.actual.type == "+":
            
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
                print("Error")

        elif Parser.tokens.actual.type == "+":
            Parser.tokens.selectNext()
            result += int(Parser.factor())

        elif Parser.tokens.actual.type == "-": 
            Parser.tokens.selectNext()
            result -= int(Parser.factor())
            
        else:
            print("Error")
            sys.exit()
        
        return result


class PrePro:    
    @staticmethod
    def filter(code):
        if("'" not in code):
            return code[:-1]
        return re.sub("('.*?)\n", ' ', code)


code = input("Digite uma operação: ") + "\n"
code = PrePro.filter(code)

if len(code) > 0:
    Parser.run(str(code))
