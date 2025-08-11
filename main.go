// main.go
package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"unicode"
)

// parseAndEval recebe uma expressão contendo inteiros positivos e operadores + ou - (sem outros símbolos)
// Faz limpeza, validação léxica e devolve o resultado ou erro.
func parseAndEval(expr string) (int, error) {
	if expr == "" {
		return 0, errors.New("input inválido")
	}

	resultado := 0
	currentNum := ""
	firstNumberSet := false
	var lastOp rune = '+'
	operatorCount := 0
	stateExpectNumber := true // inicia esperando número
	inNumber := false

	commitNumber := func() error {
		if currentNum == "" {
			return errors.New("input inválido")
		}
		n, err := strconv.Atoi(currentNum)
		if err != nil {
			return errors.New("input inválido")
		}
		if !firstNumberSet {
			resultado = n
			firstNumberSet = true
		} else {
			if lastOp == '+' {
				resultado += n
			} else {
				resultado -= n
			}
		}
		currentNum = ""
		return nil
	}

	for _, r := range expr {
		if r == ' ' || r == '\t' || r == '\n' || r == '\r' {
			// espaço delimita término de número se estávamos em um
			if inNumber {
				if err := commitNumber(); err != nil {
					return 0, err
				}
				inNumber = false
				stateExpectNumber = false // agora esperamos operador
			}
			continue
		}
		if unicode.IsDigit(r) {
			if stateExpectNumber { // iniciando um novo número
				currentNum += string(r)
				inNumber = true
				stateExpectNumber = false
			} else {
				if !inNumber { // já deveríamos ter operador antes de novo número
					return 0, errors.New("input inválido")
				}
				currentNum += string(r) // continuação do mesmo número
			}
			continue
		}
		if r == '+' || r == '-' {
			// operador não pode aparecer se esperamos número
			if stateExpectNumber { // operador inicial ou duplo
				return 0, errors.New("input inválido")
			}
			// finalizar número atual (se não já finalizado por espaço)
			if inNumber {
				if err := commitNumber(); err != nil {
					return 0, err
				}
				inNumber = false
			}
			lastOp = r
			operatorCount++
			stateExpectNumber = true
			continue
		}
		// caractere inválido
		return 0, errors.New("input inválido")
	}

	// fim da expressão
	if inNumber {
		if err := commitNumber(); err != nil {
			return 0, err
		}
		inNumber = false
	} else if stateExpectNumber { // terminou em operador
		return 0, errors.New("input inválido")
	}

	if operatorCount == 0 { // precisa ter pelo menos um operador como no código Python original
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
