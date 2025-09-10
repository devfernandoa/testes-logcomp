from tokenizer import Tokenizer
from nodes import IntVal, Identifier, UnOp, BinOp, Assignment, Print, NoOp, Block
  
class Parser():
    def __init__(self):
        self.tokenizer = None # Tokenizer

    def parseFactor(self):
        if self.tokenizer.next.type == "INT":
            result = IntVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return result
        if self.tokenizer.next.type == "identifier":
            result = Identifier(self.tokenizer.next.value, [])
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
            raise Exception(f"Invalid input on parseFactor {self.tokenizer.next.value}")

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
    
    def parseStatement(self):
        if self.tokenizer.next.type == "identifier":
            identifier = self.tokenizer.next
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "=":
                self.tokenizer.selectNext()
                result = self.parseExpression()
                return Assignment(None, [identifier, result])
            else:
                raise Exception(f"Invalid input {self.tokenizer.next.value}")
        elif self.tokenizer.next.type == "print":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "(":
                self.tokenizer.selectNext()
                result = self.parseExpression()
                if self.tokenizer.next.type == ")":
                    self.tokenizer.selectNext()
                    return Print(None, [result])
                else:
                    raise Exception(f"Parenthesis not closed {self.tokenizer.next.value}")
            else:
                raise Exception(f"Invalid input {self.tokenizer.next.value}")
        elif self.tokenizer.next.type == "barra_n":
            self.tokenizer.selectNext()
            return NoOp("barra_n", [])
        else:
            raise Exception(f"Invalid input {self.tokenizer.next.value}") 
    
    def parseBlock(self):
        if True:
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "barra_n":
                self.tokenizer.selectNext()
                result = []
                while self.tokenizer.next.type != "EOF":
                    result.append(self.parseStatement())
                self.tokenizer.selectNext()
                return Block(None, result)
            else:
                raise Exception(f"Invalid input {self.tokenizer.next.value}, need \n")
        else:
            raise Exception(f"Invalid input {self.tokenizer.next.value}, need {{")
        
    def run(self, code):
        self.tokenizer = Tokenizer(code)
        self.tokenizer.selectNext()
        result = self.parseBlock()
        if self.tokenizer.next.type != "EOF":
            raise Exception("Input sem EOF")
        return result
