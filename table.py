class SymbolsTable:
    def __init__(self):
        self.dic = {}

    def get(self, name):
        if (name in self.dic): return self.dic[name]
        raise Exception("valor nao definido")

    def sett(self, name, value):
        self.dic[name] = value