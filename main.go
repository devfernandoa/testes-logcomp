// main.go
package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
	"unicode"
)

// parseAndEval recebe uma expressão contendo inteiros positivos e operadores + ou - (sem outros símbolos)
// Faz limpeza, validação léxica e devolve o resultado ou erro.
func parseAndEval(expr string) (int, error) {
	// Remover espaços e filtrar apenas dígitos e + -
	var b strings.Builder
	for _, r := range expr {
		if r == ' ' { // ignora espaços
			continue
		}
		if unicode.IsDigit(r) || r == '+' || r == '-' { // mantém tokens válidos
			b.WriteRune(r)
		}
	}
	cleaned := b.String()
	if cleaned == "" {
		return 0, errors.New("input inválido")
	}

	// Análise léxica + avaliação em uma passada
	resultado := 0
	current := strings.Builder{}
	expectNumber := true // Inicia esperando número
	var lastOp rune = '+'

	commitNumber := func() error {
		if current.Len() == 0 {
			return errors.New("input inválido")
		}
		n, err := strconv.Atoi(current.String())
		if err != nil {
			return errors.New("input inválido")
		}
		if lastOp == '+' {
			resultado += n
		} else {
			resultado -= n
		}
		current.Reset()
		return nil
	}

	for i, r := range cleaned {
		if unicode.IsDigit(r) {
			current.WriteRune(r)
			expectNumber = false
			// Último char: commit
			if i == len([]rune(cleaned))-1 { // avoid reallocation by converting once; fine for small input
				if err := commitNumber(); err != nil {
					return 0, err
				}
			}
			continue
		}
		// r é operador
		if expectNumber { // dois operadores seguidos ou operador inicial
			return 0, errors.New("input inválido")
		}
		if err := commitNumber(); err != nil {
			return 0, err
		}
		lastOp = r
		expectNumber = true
	}

	if expectNumber { // expressão termina em operador
		return 0, errors.New("input inválido")
	}
	return resultado, nil
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "Uso: go run main.go 'conta'")
		os.Exit(1)
	}
	res, err := parseAndEval(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, "Erro: input inválido")
		os.Exit(1)
	}
	fmt.Println(res)
}
