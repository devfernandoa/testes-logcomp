from tokenizer import Tokenizer
from nodes import IntVal, StringVal, BoolVal, Identifier, UnOp, BinOp, Assignment, NoOp, Block, While, If, FuncCall
  
class Parser():
    def __init__(self):
        self.tokenizer = None # Tokenizer

    def parseFactor(self):
        if self.tokenizer.next.type == "INT":
            result = IntVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return result
        if self.tokenizer.next.type == "string":
            result = StringVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return result
        if self.tokenizer.next.type == "bool":
            result = BoolVal(self.tokenizer.next.value, [])
            self.tokenizer.selectNext()
            return result
        if self.tokenizer.next.type == "identifier":
            name = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "(":
                # chamada de função em expressão
                self.tokenizer.selectNext()
                args = []
                if self.tokenizer.next.type != ")":
                    args.append(self.BExpression())
                    while self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        args.append(self.BExpression())
                if self.tokenizer.next.type != ")":
                    raise Exception(f"Expected ')', got {self.tokenizer.next.value}")
                self.tokenizer.selectNext()
                return FuncCall(name, args)
            return Identifier(name, [])
        elif self.tokenizer.next.type == "+":
            self.tokenizer.selectNext()
            return UnOp("+", [self.parseFactor()])
        elif self.tokenizer.next.type == "-":
            self.tokenizer.selectNext()
            return UnOp("-", [self.parseFactor()])
        elif self.tokenizer.next.type == "!":
            self.tokenizer.selectNext()
            return UnOp("!", [self.parseFactor()])
        elif self.tokenizer.next.type == "(":
            self.tokenizer.selectNext()
            result = self.BExpression()
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
        while self.tokenizer.next.type in ("+", "-", "."):
            if self.tokenizer.next.type == "+":
                self.tokenizer.selectNext()
                result = BinOp("+", [result, self.parseTerm()])
            elif self.tokenizer.next.type == "-":
                self.tokenizer.selectNext()
                result = BinOp("-", [result, self.parseTerm()])
            elif self.tokenizer.next.type == ".":
                self.tokenizer.selectNext()
                result = BinOp(".", [result, self.parseTerm()])
        return result

    def RelExpression(self):
        result = self.parseExpression()
        while self.tokenizer.next.type in ("<", ">", "=="):
            if self.tokenizer.next.type == "<":
                self.tokenizer.selectNext()
                result = BinOp("<", [result, self.parseExpression()])
            elif self.tokenizer.next.type == ">":
                self.tokenizer.selectNext()
                result = BinOp(">", [result, self.parseExpression()])
            elif self.tokenizer.next.type == "==":
                self.tokenizer.selectNext()
                result = BinOp("==", [result, self.parseExpression()])
        return result

    def BTerm(self):
        result = self.RelExpression()
        while self.tokenizer.next.type == "&&":
            self.tokenizer.selectNext()
            result = BinOp("&&", [result, self.RelExpression()])
        return result

    def BExpression(self):
        result = self.BTerm()
        while self.tokenizer.next.type == "||":
            self.tokenizer.selectNext()
            result = BinOp("||", [result, self.BTerm()])
        return result
    
    def parseStatement(self):
        # atribuição ou chamada de função terminada por ';'
        if self.tokenizer.next.type == "identifier":
            name_tok = self.tokenizer.next
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == "=":
                self.tokenizer.selectNext()
                expr = self.BExpression()
                if self.tokenizer.next.type != "SEMI":
                    raise Exception("Missing ';' after assignment")
                self.tokenizer.selectNext()
                return Assignment(None, [Identifier(name_tok.value, []), expr])
            elif self.tokenizer.next.type == "(":
                # chamada de função como statement
                self.tokenizer.selectNext()
                args = []
                if self.tokenizer.next.type != ")":
                    args.append(self.BExpression())
                    while self.tokenizer.next.type == "COMMA":
                        self.tokenizer.selectNext()
                        args.append(self.BExpression())
                if self.tokenizer.next.type != ")":
                    raise Exception(f"Expected ')', got {self.tokenizer.next.value}")
                self.tokenizer.selectNext()
                if self.tokenizer.next.type != "SEMI":
                    raise Exception("Missing ';' after function call")
                self.tokenizer.selectNext()
                return FuncCall(name_tok.value, args)
            else:
                raise Exception(f"Invalid token after identifier: {self.tokenizer.next.value}")

        if self.tokenizer.next.type == "while":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != "(":
                raise Exception("Expected '(' after while")
            self.tokenizer.selectNext()
            cond = self.BExpression()
            if self.tokenizer.next.type != ")":
                raise Exception("Expected ')' after while condition")
            self.tokenizer.selectNext()
            block = self.parseBlock()
            return While(None, [cond, block])

        if self.tokenizer.next.type == "if":
            self.tokenizer.selectNext()
            if self.tokenizer.next.type != "(":
                raise Exception("Expected '(' after if")
            self.tokenizer.selectNext()
            cond = self.BExpression()
            if self.tokenizer.next.type != ")":
                raise Exception("Expected ')' after if condition")
            self.tokenizer.selectNext()
            then_block = self.parseBlock()
            if self.tokenizer.next.type == "else":
                self.tokenizer.selectNext()
                else_block = self.parseBlock()
                return If(None, [cond, then_block, else_block])
            return If(None, [cond, then_block])

        if self.tokenizer.next.type == "SEMI":
            self.tokenizer.selectNext()
            return NoOp("SEMI", [])

        raise Exception(f"Invalid input {self.tokenizer.next.value}") 
    
    def parseBlock(self):
        if self.tokenizer.next.type != "{":
            raise Exception(f"Invalid input {self.tokenizer.next.value}, need {{")
        self.tokenizer.selectNext()
        result = []
        while self.tokenizer.next.type != "}":
            result.append(self.parseStatement())
        self.tokenizer.selectNext()
        return Block(None, result)
        
    def run(self, code):
        self.tokenizer = Tokenizer(code)
        self.tokenizer.selectNext()
        result = self.parseBlock()
        if self.tokenizer.next.type != "EOF":
            raise Exception("Input sem EOF")
        return result
