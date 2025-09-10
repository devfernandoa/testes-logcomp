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

class UnOp(Node):
    def evaluate(self, st):
        if self.value == "+":
            return self.children[0].evaluate(st)
        elif self.value == "-":
            return -self.children[0].evaluate(st)

class IntVal(Node):
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
        print(self.children[0].evaluate(st))
    
class Assignment(Node):
    def evaluate(self, st):
        st.setter(self.children[0].value, self.children[1].evaluate(st))

class Block(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)