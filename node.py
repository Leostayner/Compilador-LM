from table import * 
from assembler import *

tb  = SymbolsTable()
asb = Assembler()

class Node:

    i = 0
    def __init__(self, value = False, children = []):
        self.value      = value         #value
        self.children   = children      #list of nodes
        self._id        = self.newId() 

    def Evaluate(self):
        pass
    
    #@staticmethod
    def newId(self):
        Node.i += 1
        return Node.i
        

class BinOp(Node):
    
    def Evaluate(self):
        c1 = self.children[0].Evaluate()
        asb.write( ("PUSH EBX\n") )
              
        c2 = self.children[1].Evaluate()
        asb.write( ("POP EAX\n") ) 
        
    
        if self.value == "/":
            asb.i_arithmeticASB("IDIV")
            return c1 // c2

        elif self.value == "*":
            asb.i_arithmeticASB("IMUL")
            return c1 * c2

        elif self.value == "+":
            asb.arithmeticASB("ADD")
            return c1 + c2

        elif self.value == "-":
            asb.arithmeticASB("SUB")
            return c1 - c2        

        ## Ajustar assembler
        elif self.value == "=":
            asb.conditionalASB("binop_je")
            return c1 == c2
        
        elif self.value == ">":
            asb.conditionalASB("binop_jg")
            return c1 > c2
        
        elif self.value == "<":
            asb.conditionalASB("binop_jl")
            return c1 < c2
        
        elif self.value == "OR":
            asb.arithmeticASB("OR")
            return c1 or c2
        
        elif self.value == "AND":
            asb.arithmeticASB("AND")
            return c1 and c2

        
class AssOP(Node):

    def Evaluate(self):
        tp_tranformer = {"INTEGER": "<class 'int'>", "BOOLEAN": "<class 'bool'>"}
        
        name = self.children[0].Evaluate()
        val  = self.children[1].Evaluate()        
        tp   = tb.get(name)[1]
        
        if(tp_tranformer[tp] != str(type(val))): 
            raise Exception("Semantic Error: {0} Invalid assigment type".format(name))
        
        tb.sett(name, val, tp)
        asb.write("MOV [EBP-{0}], EBX\n".format(tb.get(name)[2]))
        
class UnOp(Node):
    
    def Evaluate(self):
        c = self.children[0].Evaluate()

        if   self.value == "+"     : return + int(c)
        elif self.value == "-"     : return - int(c)
        
        elif self.value == "NOT"   : 
            if (c): asb.write("MOV EBX, 0\n") 
            else  : asb.write("MOV EBX, 1\n")
            return not int(c)
        
        elif self.value == "PRINT" : asb.printASB()

class IntVal(Node):
    
    def Evaluate(self):
        asb.write( "MOV EBX, {0}\n".format(self.value) ) 
        return self.value

class CharVal(Node):
    
    def Evaluate(self):
        obj = tb.get(self.value)
        asb.write( ("MOV EBX, ") ) 
        asb.write( "[EBP-{0}]\n".format(obj[2]))
        return obj[0]

class Identifier(Node):
    
    def Evaluate(self):
        return self.value

class Stmts(Node):
         
    def Evaluate(self):
        for element in self.children:
            element.Evaluate()

class NoOp(Node):
    
    def Evaluate(self):
        pass

class WhileOp(Node):
         
    def Evaluate(self):
        asb.loopASB(self._id, "init")

        #while(self.children[0].Evaluate()):
        condition = self.children[0].Evaluate()
        asb.loopASB(self._id, "endCondition")
        
        if(condition):
            self.children[1].Evaluate()

        asb.loopASB(self._id, "end")
        
class ifOp(Node):
         
    def Evaluate(self):
        condition = self.children[0].Evaluate()
        
        asb.write("CMP EBX, False\n")
        asb.write("JE EXIT_" + str(self._id) + "\n")
        self.children[1].Evaluate()
        
        asb.write("EXIT_" + str(self._id) + ":\n")   
        if (len(self.children) == 3): 
            self.children[2].Evaluate()


class InputOp(Node):
         
    def Evaluate(self):
        tmp = int(input("Input: "))
        asb.write( "MOV EBX, {0}\n".format(tmp) ) 
        return tmp

class Tp(Node):
         
    def Evaluate(self):
        return self.value

class VarDec(Node):
       
    def Evaluate(self):
        name = self.children[0].Evaluate()
        tp   = self.children[1].Evaluate()
        
        tb.sett(name, "" , tp)
        asb.variableASB(name, tp.lower() , tb.get(name)[2])
        
class BolOP(Node):

    def Evaluate(self):
        asb.write( "MOV EBX, {0}\n".format(self.value) ) 
        return self.value