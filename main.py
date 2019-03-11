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
        signal = ["+", "-", "*", "/"]
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
            
            if self.origin[self.position] in signal:

                if (self.origin[self.position] in signal[:2]):
                    type = "signal"
                
                else:
                    type = "signal2"
                  
                newToken = self.origin[self.position]
                self.position += 1
                

            elif(self.origin[self.position].isdigit):
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
        result = Parser.parseExpression()
        
        if(Parser.tokens.actual.type == 'EOF'):
            print(result)

        else:
            print("last token is not EOP, operation syntactic error")
            print(Parser.tokens.actual.type)
            print(Parser.tokens.actual.value)
       
    @staticmethod
    def term():
        result = 0
        Parser.tokens.selectNext()
        
        if Parser.tokens.actual.type == "int":
            result = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            
            while Parser.tokens.actual.type == "signal2":
                        
                if Parser.tokens.actual.value == "*":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "int":
                        result *= int(Parser.tokens.actual.value)

                    else:
                        print("Error: value {0} is not int after signal *".format(Parser.tokens.actual.value))
                        sys.exit()

                elif Parser.tokens.actual.value == "/":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "int":
                        result /= int(Parser.tokens.actual.value)
                    
                    else:
                        print("Error: value {0} is not int after signal /".format(Parser.tokens.actual.value))
                        print(Parser.tokens.position)
                        sys.exit()

                Parser.tokens.selectNext()
        else:
            print("Error: first value {0} is not a int".format(Parser.tokens.actual.value))
            sys.exit()
            
        return result

    
    @staticmethod
    def parseExpression():
        result = Parser.term()
        while Parser.tokens.actual.type == "signal":
            
            if Parser.tokens.actual.value == "+":
                result += Parser.term()

            elif Parser.tokens.actual.value == "-":
                result -= Parser.term()
        
        return result


class PrePro:    
    @staticmethod
    def filter(code):
        if("'" not in code):
            return code[:-1]
        return re.sub("'.*?\n", ' ', code)

code = input("Digite uma operação: ") + "\n"
code = PrePro.filter(code)

if len(code) > 0:
    Parser.run(str(code))
