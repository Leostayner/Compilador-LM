from table import * 

tb = SymbolsTable()

class Node:
    def __init__(self):
        self.value      #variant
        self.children   #list of nodes

    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value     = value 
        self.children  = children
 
    def Evaluate(self):
        if self.value == "/":
            return self.children[0].Evaluate() / self.children[1].Evaluate()

        elif self.value == "*":
            return self.children[0].Evaluate() * self.children[1].Evaluate()

        elif self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()

        elif self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        
        elif self.value == "=":
            return self.children[0].Evaluate() == self.children[1].Evaluate()

        elif self.value == ">":
            return self.children[0].Evaluate() > self.children[1].Evaluate()
        
        elif self.value == "<":
            return self.children[0].Evaluate() < self.children[1].Evaluate()



        
class AssOP(Node):
    def __init__(self, value, children):
        self.value     = value 
        self.children  = children
 
    def Evaluate(self):
        tb.sett(self.children[0].Evaluate(), self.children[1].Evaluate())


class UnOp(Node):
    def __init__(self, value, children):
        self.value     = value 
        self.children  = children
 
    def Evaluate(self):
        if self.value   == "+"     : return + int(self.children[0].Evaluate())
        elif self.value == "-"     : return - int(self.children[0].Evaluate())
        elif self.value == "PRINT" : print(self.children[0].Evaluate())

class IntVal(Node):
    def __init__(self, value):
        self.value     = value
 
    def Evaluate(self):
        return self.value


class CharVal(Node):
    def __init__(self, value):
        self.value     = value
 
    def Evaluate(self):
        return tb.get(self.value)

class Var(Node):
    def __init__(self, value):
        self.value     = value
 
    def Evaluate(self):
        return self.value


class Stat(Node):
    def __init__(self, value, children):
        self.value     = value 
        self.children  = children
         
    def Evaluate(self):
        for element in self.children:
            element.Evaluate()


class NoOp(Node):
    
    def Evaluate(self):
        pass


class WhileOp(Node):
    def __init__(self, value, children):
        self.value     = value 
        self.children  = children
         
    def Evaluate(self):
        while(self.children[0].Evaluate()):
            self.children[1].Evaluate()


class ifOp(Node):
    def __init__(self, value, children):
        self.value     = value 
        self.children  = children
         
    def Evaluate(self):
        if(self.children[0].Evaluate()):
            self.children[1].Evaluate()
            
        elif len(self.children) == 3:
            self.children[2].Evaluate()

