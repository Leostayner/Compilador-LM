from SymbolsTable import * 


class Node:
    def __init__(self, value = False, children = []):
        self.value      = value     #variant
        self.children   = children  #list of nodes

    def Evaluate(self, table):
        pass

class BinOp(Node):
 
    def Evaluate(self, table):
        c1 = self.children[0].Evaluate(table)
        c2 = self.children[1].Evaluate(table)
        if   self.value == "/"  : return c1 //  c2
        elif self.value == "*"  : return c1 *   c2
        elif self.value == "+"  : return c1 +   c2
        elif self.value == "-"  : return c1 -   c2
        elif self.value == "="  : return c1 ==  c2
        elif self.value == ">"  : return c1 >   c2 
        elif self.value == "<"  : return c1 <   c2 
        elif self.value == "OR" : return c1 or  c2 
        elif self.value == "AND": return c1 and c2
            
    
class AssOP(Node):
 
    def Evaluate(self, table):
        tp_tranformer = {"INTEGER": "<class 'int'>", "BOOLEAN": "<class 'bool'>"}
    
        name = self.children[0].Evaluate(table)
        tp   = table.get(name)[1]
        val  = self.children[1].Evaluate(table)
           
        if(tp_tranformer[tp] != str(type(val))): 
           
            
            raise Exception("Semantic Error: {0} Invalid assigment type : {1}".format(name, str(type(val)) ))
        
        table.sett(name, val, tp)


class UnOp(Node):
 
    def Evaluate(self, table):
        if self.value   == "+"     : return +   int(self.children[0].Evaluate(table))
        elif self.value == "-"     : return -   int(self.children[0].Evaluate(table))
        elif self.value == "NOT"   : return not int(self.children[0].Evaluate(table))    
        elif self.value == "PRINT" : print(self.children[0].Evaluate(table))


class IntVal(Node):

    def Evaluate(self, table):
        return self.value

class CharVal(Node):
 
    def Evaluate(self, table):
        return table.get(self.value)[0]

class Identifier(Node):
 
    def Evaluate(self, table):
        return self.value

class Stmts(Node):
         
    def Evaluate(self, table):
        for element in self.children:
            element.Evaluate(table)

class NoOp(Node):
    
    def Evaluate(self, table):
        pass

class WhileOp(Node):
         
    def Evaluate(self, table):
        while(self.children[0].Evaluate(table)):
            self.children[1].Evaluate(table)

class ifOp(Node):
         
    def Evaluate(self, table):
        if(self.children[0].Evaluate(table)):
            self.children[1].Evaluate(table)
            
        elif len(self.children) == 3:
            self.children[2].Evaluate(table)

class InputOp(Node):
         
    def Evaluate(self, table):
        return int(input("Input: "))

class Tp(Node):
         
    def Evaluate(self, table):
        return self.value

class VarDec(Node):
       
    def Evaluate(self, table):
        table.sett(self.children[0].Evaluate(table), "" ,self.children[1].Evaluate(table) )
        
class BolOP(Node):
 
    def Evaluate(self, table):
        return self.value

"""
FuncDec: possui n filhos: n-1 VarDec e Statements. Os argumentos da declaração devem ser incorporados
ao VarDec, incluindo o próprio nome da função e seu tipo correspondente. O Evaluate() apenas cria
uma variável na SymbolTable atual, sendo o nome da variável o nome da função, o valor apontando
para o próprio nó FuncDec e o tipo será FUNCTION
"""
class FuncDec(Node):

    def Evaluate(self, table):
        table.sett(self.value, self, "FUNCTION")

class FuncSub(Node):

    def Evaluate(self, table):
        table.sett(self.value, self, "SUB")

"""
FuncCall: possui n filhos do tipo identificador ou expressão - são os argumentos da chamada. O
Evaluate() vai realizar o verdadeiro Evaluate() da FuncDec, recuperando o nó de declaração na
SymbolTable, atribuindo os valores dos argumentos de entrada e executando o bloco (segundo filho).
"""
class FuncCall(Node):
    
    def Evaluate(self, table):        
        table     = SymbolsTable(table)
        funcNode = table.get(self.value)[0]  
        
        if(len(funcNode.children[1:-1]) != len(self.children)):
            raise Exception("Semantic Error: Invalid arguments numbers")
        
        l = []
        for c in funcNode.children[:-1]:
            c.Evaluate(table)
            l.append(c.children[0].Evaluate(table))
        
        for i, c in enumerate(self.children):
            value = c.Evaluate(table)
            table.sett(l[i + 1], value, type(value))

        funcNode.children[-1].Evaluate(table)
        return table.get("SOMA")[0]