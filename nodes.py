class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        pass

class BinOp(Node):
    def evaluate(self, st):
        if self.value == "+":
            return self.children[0].evaluate(st) + self.children[1].evaluate(st)
        elif self.value == "-":
            return self.children[0].evaluate(st) - self.children[1].evaluate(st)
        elif self.value == "*":
            return self.children[0].evaluate(st) * self.children[1].evaluate(st)
        elif self.value == "/":
            return self.children[0].evaluate(st) // self.children[1].evaluate(st)
        elif self.value == ".":
            return str(self.children[0].evaluate(st)) + str(self.children[1].evaluate(st))
        elif self.value == "&&":
            return bool(self.children[0].evaluate(st)) and bool(self.children[1].evaluate(st))
        elif self.value == "||":
            return bool(self.children[0].evaluate(st)) or bool(self.children[1].evaluate(st))
        elif self.value == "<":
            return self.children[0].evaluate(st) < self.children[1].evaluate(st)
        elif self.value == ">":
            return self.children[0].evaluate(st) > self.children[1].evaluate(st)
        elif self.value == "==":
            return self.children[0].evaluate(st) == self.children[1].evaluate(st)

class UnOp(Node):
    def evaluate(self, st):
        if self.value == "+":
            return self.children[0].evaluate(st)
        elif self.value == "-":
            return -self.children[0].evaluate(st)
        elif self.value == "!":
            return not bool(self.children[0].evaluate(st))

class IntVal(Node):
    def evaluate(self, st):
        return self.value

class StringVal(Node):
    def evaluate(self, st):
        return self.value

class BoolVal(Node):
    def evaluate(self, st):
        return self.value

class NoOp(Node):
    def evaluate(self, st):
        pass

class Identifier(Node):
    def evaluate(self, st):
        return st.getter(self.value)

class Print(Node):
    def evaluate(self, st):
        val = self.children[0].evaluate(st)
        if isinstance(val, bool):
            print(str(val).lower())
        else:
            print(val)
    
class Assignment(Node):
    def evaluate(self, st):
        st.setter(self.children[0].value, self.children[1].evaluate(st))

class Block(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class While(Node):
    def evaluate(self, st):
        while bool(self.children[0].evaluate(st)):
            self.children[1].evaluate(st)

class If(Node):
    def evaluate(self, st):
        if bool(self.children[0].evaluate(st)):
            self.children[1].evaluate(st)
        elif len(self.children) > 2:
            self.children[2].evaluate(st)

class FuncCall(Node):
    def evaluate(self, st):
        name = self.value
        if name == 'scanf':
            return int(input())
        if name == 'printf':
            if not self.children:
                print()
                return None
            v = self.children[0].evaluate(st)
            if isinstance(v, bool):
                print(str(v).lower())
            else:
                print(v)
            return None
        raise Exception(f"Função não definida: {name}")