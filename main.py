import sys
import re

from parser import *

class SymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self, key):
        return self.table[key]

    def setter(self, key, value):
        self.table[key] = value

class PrePro(): # Tira comentários com // até o \n ou EOF
        def filter(self, code):
            return re.sub(r"//.*", "", code)

def main():
    if len(sys.argv) < 2:
        raise Exception("Invalid number of arguments")
    
    filename = sys.argv[1]

    with open(filename, "r") as file:
        code = file.read()

    prepro = PrePro()
    code = prepro.filter(code)

    parser = Parser()
    result = parser.run(code)

    symbol_table = SymbolTable()
    
    result.evaluate(symbol_table)

if __name__ == "__main__":
    main()