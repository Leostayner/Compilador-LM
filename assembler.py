from text import *
class Assembler:

    def __init__(self):
        self.textASB = initial_st

    def write(self, text):
        self.textASB += text 

    def variableASB(self, variable, type, index):
        st = "PUSH DWORD 0; Dim {0} as {1} [EBP-{2}]\n".format(variable.lower(), type.lower(), index)
        self.textASB += st
    
    def arithmeticASB(self, op):
        st = ("{0} EAX, EBX\n"
              "MOV EBX, EAX\n").format(op)
        self.textASB += st

    def i_arithmeticASB(self, op):
        st = ("{0} EBX\n"
              "MOV EBX, EAX\n").format(op)
        self.textASB += st
        
    def conditionalASB(self, def_name):
        st = ("CMP EAX, EBX\n"
              "CALL {0}\n"
              ).format(def_name)
    
        self.textASB += st

    def loopASB(self, numberLoop, state):
        if(state == "init"):
            st  = ("LOOP_{0}:\n").format(numberLoop)     
        
        elif(state == "endCondition"):
            st = ("JE EXIT_{0}\n").format(numberLoop)
            
        elif(state == "end"):
            st = ("JMP LOOP_{0}\n"
                  "EXIT_{0}:\n").format(numberLoop)
        self.textASB += st

        
    def printASB(self):
        st = ("PUSH EBX\n"
              "CALL print\n"
              "POP EBX\n")
        
        self.textASB += st

    def endCode(self):
        st = ("\n; interrupcao de saida\n"
              "POP EBP\n"
              "MOV EAX, 1\n"
              "INT 0x80")
        
        self.textASB += st
            