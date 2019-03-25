#Compilador - LM
#python3

from token import *
from prepro import *
from parser import *

def readFile(file_name):
    with open(file_name, 'r') as f:
        return f.readlines()
       
def main():
    code = readFile("input.vbs")    
    for line in code:
        try:
                code = PrePro.filter(line)
                if len(code) > 0:
                        print("Operação: {0}".format(code))
                        result = Parser.run(str(code))
                        print(result.Evaluate(), "\n")

        except Exception as err:
                print(err, "\n")
        
main()
