class SymbolsTable:
    def __init__(self, ancestor):
        self.dic      =     {}
        self.ancestor = ancestor

    def get(self, name):
        if (name in self.dic) : 
            return self.dic[name]
        
        elif(self.ancestor != None): return self.ancestor.get(name)

        raise Exception("Semaintic Error: Variavel {0} Indefinida".format(name))

    def sett(self, name, value, type):
        self.dic[name] = [value, type]