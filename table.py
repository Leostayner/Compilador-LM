class SymbolsTable:
    def __init__(self):
        self.nEBP = 0
        self.dic  = {}

    def get(self, name):
        if (name in self.dic): return self.dic[name]
        raise Exception("valor nao definido")

    def sett(self, name, value, type):
        dword = {"INTEGER": 4, "BOOLEAN": 4} 
        
        if name not in self.dic:
            self.nEBP += dword[type]
            self.dic[name] = [value, type, self.nEBP]
            return

        self.dic[name] = [value, type, self.dic[name][2]]