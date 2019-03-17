class Token:

   def __init__(self, type, value):
       self.type  = type
       self.value = value

class Tokenizer:

    def __init__(self, origin):
        self.origin   = origin                       #código fonte que será tokenizado
        self.position = 0                            #posição atual que o Tokenizador está separando
        self.actual   = self.origin[self.position]   #o último token separando

    def selectNext(self):
        ops = ["+", "-", "*", "/", "(", ")"]
        newToken = ""
        type = ""

        if self.position == len(self.origin):
            type = "EOF"
      
        else: 
            while self.origin[self.position] == " ":
                self.position += 1
                
                if self.position == len(self.origin):
                    type = "EOF"
                    self.actual = Token(type, newToken)
                    return
            
            if self.origin[self.position] in ops:
                type = self.origin[self.position]
                self.position += 1
                    

            elif(self.origin[self.position].isdigit()):
                while self.origin[self.position].isdigit():
                    newToken += self.origin[self.position]
 
                    self.position += 1
                    
                    if self.position == len(self.origin):
                        break

                type = "int"
                
        self.actual = Token(type, newToken)
