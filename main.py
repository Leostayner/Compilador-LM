#Compilador - LM
#python3

from token import *
from prepro import *
from parser import *

def readFile(file_name):
    with open(file_name, 'r') as f:
        code = ''.join(f.readlines())
        return code
       
def main():
    try:
        code = readFile("input.txt")
        code = PrePro.filter(code)
        print("Operação: {0}".format(code))
        
        if len(code) > 0:
                result = Parser.run(str(code))
                print(result.Evaluate())

    except Exception as err:
        print(err)

main()
