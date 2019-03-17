#Compilador - LM
#python3

from token import *
from prepro import *
from parser import *

def main():
    try:
        code = input("Digite uma operação: ")
        code = PrePro.filter(code)
        
        if len(code) > 0:
                Parser.run(str(code))
        
    except Exception as err:
        print(err)

main()