## Tarefas:
  1. Colocar o Diagrama Sintático no README do GitHub.
  1. Criar uma Classe **Token** com 2 atributos:
    - `type`: string. É o tipo do token
    - `value`: integer | string. É o valor do token
  1. Criar uma Classe **Lexer** com 3 atributos e 1 método:
    - `source`: string. É o código-fonte que será tokenizado
    - `position`: integer. É a posição atual que o Lexer está separando
    - `next`: Token. É o último token separado
    - `selectNext()`: lê o próximo token e atualiza o atributo `next`
  1. Criar uma Classe **Parser** com 1 atributo e 2 métodos (**estáticos**):
    - `lexer`: Lexer. Objeto da classe que irá ler o código fonte e alimentar o Parser.
    - `parseExpression(): int`: consome os tokens do Lexer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado numérico da expressão analisada.
    - `run(code: string): int`: recebe o código fonte como argumento, inicializa um objeto Lexer em `lex`, posiciona no primeiro token e retorna o resultado do `parseExpression()`. Ao final verificar se terminou de consumir toda a cadeia (o token deve ser `EOF`).
  1. O main() do compilador deve chamar o método Parser.run() e imprimir o retorno do método.