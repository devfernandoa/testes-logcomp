class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        # ignora todos os espaços em branco (inclui \n)
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        ch = self.source[self.position]

        # números
        if ch.isdigit():
            acc = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                acc += self.source[self.position]
                self.position += 1
            self.next = Token("INT", int(acc))
            return

        # strings
        if ch == '"':
            self.position += 1
            acc = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                acc += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise Exception("Invalid token: unterminated string")
            self.position += 1
            self.next = Token("string", acc)
            return

        # dois caracteres
        if ch == '=' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
            self.next = Token('==', '=='); self.position += 2; return
        if ch == '&' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '&':
            self.next = Token('&&', '&&'); self.position += 2; return
        if ch == '|' and self.position + 1 < len(self.source) and self.source[self.position + 1] == '|':
            self.next = Token('||', '||'); self.position += 2; return

        # um caractere
        if ch in '+-*/(){};,.=!<>':
            mapping = {
                ',': 'COMMA',
                ';': 'SEMI',
            }
            ttype = mapping.get(ch, ch)
            self.next = Token(ttype, ch)
            self.position += 1
            return

        # identificadores e keywords
        if ch.isalpha() or ch == '_':
            acc = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                acc += self.source[self.position]
                self.position += 1
            if acc in ("if", "else", "while"):
                self.next = Token(acc, acc); return
            if acc == 'true':
                self.next = Token('bool', True); return
            if acc == 'false':
                self.next = Token('bool', False); return
            self.next = Token('identifier', acc)
            return

        raise Exception(f"Invalid token {self.source[self.position]}")