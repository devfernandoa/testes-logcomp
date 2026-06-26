## Lista de tarefas simples

- [ ] Criar a classe Token para representar tipo e valor.
- [ ] Criar a classe Lexer com os atributos source, position e next.
- [ ] Implementar Lexer.select_next para ignorar espaços em branco.
- [ ] Reconhecer tokens INT, PLUS, MINUS e EOF no Lexer.
- [ ] Adicionar erro léxico para símbolo inválido com prefixo [Lexer].
- [ ] Criar a classe Parser com método estático parse_expression.
- [ ] Implementar regra: expressão começa com INT, senão erro [Parser].
- [ ] Implementar loop para processar PLUS e MINUS com próximo INT.
- [ ] Calcular o resultado da expressão durante o parse.
- [ ] Criar método estático Parser.run como ponto de entrada.
- [ ] No run, validar que ao final o próximo token é EOF.
- [ ] Exibir mensagens de erro claras e com origem ([Lexer] ou [Parser]).
- [ ] Testar casos válidos: 1+2, 3-2, 11+22-33, 789 +345 -123.
- [ ] Testar casos inválidos: 1 1, +1, 1+.

## Extra (opcional)

- [ ] Implementar operador XOR com símbolo ^ e mesma precedência de + e -.
- [ ] Adicionar testes para XOR (exemplo: 2 ^ 3 = 1).
