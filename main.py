import sys

class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

class BinOp(Node):
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        elif self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()

class UnOp(Node):
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        elif self.value == "-":
            return -self.children[0].evaluate()

class IntVal(Node):
    def evaluate(self):
        return self.value

class NoOp(Node):
    def evaluate(self):
        pass

class PrePro(): # Tira comentários com // até o \n ou EOF
    def filter(self, code):
        lines = code.split("\n")
        new_code = ""
        for line in lines:
            new_code += line.split("//")[0] + "\n"
        return new_code

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
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        if self.source[self.position].isdigit():
            next = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                next += self.source[self.position]
                self.position += 1
            self.next = Token("INT", int(next))
            return

        if self.source[self.position] == "+":
            self.next = Token("+", self.source[self.position])
            self.position += 1
            return

        if self.source[self.position] == "-":
            self.next = Token("-", self.source[self.position])
            self.position += 1
            return
        
        if self.source[self.position] == "*":
            self.next = Token("*", self.source[self.position])
            self.position += 1
            return
        
        if self.source[self.position] == "/":
            self.next = Token("/", self.source[self.position])
            self.position += 1
            return
        
        if self.source[self.position] == "(":
            self.next = Token("(", self.source[self.position])
            self.position += 1
            return
        
        if self.source[self.position] == ")":
            self.next = Token(")", self.source[self.position])
            self.position += 1
            return

        raise Exception(f"Invalid input {self.source[self.position]}")

class Parser():
    def __init__(self):
        self.tokenizer = None # Tokenizer

    def parseFactor(self):
        if self.tokenizer.next.type == "INT":
            result = IntVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return result
        elif self.tokenizer.next.type == "+":
            self.tokenizer.selectNext()
            return UnOp("+", [self.parseFactor()])
        elif self.tokenizer.next.type == "-":
            self.tokenizer.selectNext()
            return UnOp("-", [self.parseFactor()])
        elif self.tokenizer.next.type == "(":
            self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.tokenizer.next.type == ")":
                self.tokenizer.selectNext()
                return result
            else:
                raise Exception(f"Parenthesis not closed {self.tokenizer.next.value}")
        else:
            raise Exception(f"Invalid input {self.tokenizer.next.value}")

    def parseTerm(self):
        result = self.parseFactor()
        while self.tokenizer.next.type == "*" or self.tokenizer.next.type == "/":
            if self.tokenizer.next.type == "*":
                self.tokenizer.selectNext()
                result = BinOp("*", [result, self.parseFactor()])
            elif self.tokenizer.next.type == "/":
                self.tokenizer.selectNext()
                result = BinOp("/", [result, self.parseFactor()])
        return result
        
    def parseExpression(self):
        result = self.parseTerm()
        while self.tokenizer.next.type == "+" or self.tokenizer.next.type == "-":
            if self.tokenizer.next.type == "+":
                self.tokenizer.selectNext()
                result = BinOp("+", [result, self.parseTerm()])
            elif self.tokenizer.next.type == "-":
                self.tokenizer.selectNext()
                result = BinOp("-", [result, self.parseTerm()])
        return result

    def run(self, code):
        self.tokenizer = Tokenizer(code)
        self.tokenizer.selectNext()
        result = self.parseExpression()
        if self.tokenizer.next.type != "EOF":
            raise Exception("Input sem EOF")
        return result

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py nome_do_arquivo.go", file=sys.stderr)
        sys.exit(1)
    
    with open(sys.argv[1], "r") as file:
        code = file.read()

    prepro = PrePro()
    code = prepro.filter(code)

    parser = Parser()
    result = parser.run(code)
    print(result.evaluate())
    

if __name__ == "__main__":
    main()