#Compilador - LM
#python3

import sys
from token import *
from prepro import *
from parser import *

def readFile(file_name):
    with open(file_name, 'r') as f:
        return ''.join(f.readlines())
      
def main():
    try:
        code = readFile(sys.argv[1])    
        code = PrePro.filter(code)
        if len(code) > 0:
                print("Operação: {0}".format(code))
                result = Parser.run(str(code))
                print(result.Evaluate(), "\n")

    except Exception as err:
        print(err, "\n")

main() 