class Token():
    def __init__(self, type, value):
        self.type = type # String
        self.value = value # Int
    
class Tokenizer():
    def __init__(self, source):
        self.source = source # String
        self.position = 0 # Int
        self.next = None # Token
    
    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position].isspace() and self.source[self.position] != "\n":
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        elif self.source[self.position].isdigit():
            next = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                next += self.source[self.position]
                self.position += 1
            self.next = Token("INT", int(next))
            return

        elif self.source[self.position] == "+":
            self.next = Token("+", self.source[self.position])
            self.position += 1
            return

        elif self.source[self.position] == "-":
            self.next = Token("-", self.source[self.position])
            self.position += 1
            return
        
        elif self.source[self.position] == "*":
            self.next = Token("*", self.source[self.position])
            self.position += 1
            return
        
        elif self.source[self.position] == "/":
            self.next = Token("/", self.source[self.position])
            self.position += 1
            return
        
        elif self.source[self.position] == "(":
            self.next = Token("(", self.source[self.position])
            self.position += 1
            return
        
        elif self.source[self.position] == ")":
            self.next = Token(")", self.source[self.position])
            self.position += 1
            return
    
        elif self.source[self.position] == "{": 
            self.next = Token("{", self.source[self.position])
            self.position += 1
            return
        
        elif self.source[self.position] == "}":
            self.next = Token("}", self.source[self.position])
            self.position += 1
            return
        
        elif self.source[self.position] == "=":
            self.next = Token("=", self.source[self.position])
            self.position += 1
            return
        
        elif self.source[self.position] == "\n":
            self.next = Token("barra_n", self.source[self.position])
            self.position += 1
            return

        elif self.source[self.position].isalpha():
            next = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                next += self.source[self.position]
                self.position += 1

            if next == "log":
                self.next = Token("log", next)
            else:
                self.next = Token("identifier", next)
            return

        raise Exception(f"Invalid token {self.source[self.position]}")