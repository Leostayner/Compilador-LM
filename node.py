from table import * 

tb = SymbolsTable()

class Node:
    def __init__(self, value = False, children = []):
        self.value      = value     #variant
        self.children   = children  #list of nodes

    def Evaluate(self):
        pass

class BinOp(Node):
 
    def Evaluate(self):
        c1 = self.children[0].Evaluate()
        c2 = self.children[1].Evaluate()

        if self.value == "/":
            return c1 // c2

        elif self.value == "*":
            return c1 * c2

        elif self.value == "+":
            return c1 + c2

        elif self.value == "-":
            return c1 - c2
        
        elif self.value == "=":
            return c1 == c2

        elif self.value == ">":
            return c1 > c2
        
        elif self.value == "<":
            return c1 < c2
        
        elif self.value == "OR":
            return c1 or c2
        
        elif self.value == "AND":
            return c1 and c2
            
            
class AssOP(Node):
 
    def Evaluate(self):
        tp_tranformer = {"INTEGER": "<class 'int'>", "BOOLEAN": "<class 'bool'>"}
    
 
        name = self.children[0].Evaluate()
        tp   = tb.get(name)[1]
        val  = self.children[1].Evaluate()
        
        if(tp_tranformer[tp] != str(type(val))): 
            raise Exception("Semantic Error: {0} Invalid assigment type : {1}".format(name, str(type(val)) ))
        
        tb.sett(name, val, tp)


class UnOp(Node):
 
    def Evaluate(self):
        if self.value   == "+"     : return + int(self.children[0].Evaluate())
        elif self.value == "-"     : return - int(self.children[0].Evaluate())
        elif self.value == "NOT"   : return not int(self.children[0].Evaluate())    
        elif self.value == "PRINT" : print(self.children[0].Evaluate())


class IntVal(Node):
 
    def Evaluate(self):
        return self.value

class CharVal(Node):
 
    def Evaluate(self):
        return tb.get(self.value)[0]

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
        while(self.children[0].Evaluate()):
            self.children[1].Evaluate()


class ifOp(Node):
         
    def Evaluate(self):
        if(self.children[0].Evaluate()):
            self.children[1].Evaluate()
            
        elif len(self.children) == 3:
            self.children[2].Evaluate()

class InputOp(Node):
         
    def Evaluate(self):
        return int(input("Input: "))


class Tp(Node):
         
    def Evaluate(self):
        return self.value

class VarDec(Node):
       
    def Evaluate(self):
        tb.sett(self.children[0].Evaluate(), "" ,self.children[1].Evaluate() )
        
class BolOP(Node):
 
    def Evaluate(self):
        return self.value



class FuncDec(Node):
    def Evaluate():