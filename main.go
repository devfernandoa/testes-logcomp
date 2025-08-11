// main.go
package main

import (
	"fmt"
	"os"
)

func invalid() {
	fmt.Fprintln(os.Stderr, "Erro: input inválido")
	os.Exit(1)
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "Uso: go run main.go 'conta'")
		os.Exit(1)
	}

	in := os.Args[1]
	// Pré-processamento: remove espaços e mantém apenas dígitos e +-
	// (espelha a lógica do Python)
	filtered := make([]byte, 0, len(in))
	for i := 0; i < len(in); i++ {
		c := in[i]
		if c == ' ' {
			continue
		}
		if (c >= '0' && c <= '9') || c == '+' || c == '-' {
			filtered = append(filtered, c)
		}
	}

	if len(filtered) == 0 {
		invalid()
	}

	var result int64
	var cur int64
	haveNum := false
	var lastOp byte = '+'
	numCount := 0
	opCount := 0

	for i := 0; i < len(filtered); i++ {
		c := filtered[i]
		if c == '+' || c == '-' {
			// inválido se operador for primeiro, último ou se não houve número antes (operadores consecutivos)
			if i == 0 || i == len(filtered)-1 || !haveNum {
				invalid()
			}
			if numCount == 0 {
				result = cur
			} else {
				if lastOp == '+' {
					result += cur
				} else {
					result -= cur
				}
			}
			numCount++
			cur = 0
			haveNum = false
			lastOp = c
			opCount++
		} else {
			// dígito
			cur = cur*10 + int64(c-'0')
			haveNum = true
		}
	}

	// Finaliza com o último número
	if haveNum {
		if numCount == 0 {
			result = cur
		} else {
			if lastOp == '+' {
				result += cur
			} else {
				result -= cur
			}
		}
		numCount++
	}

	// Valida listas não vazias (espelha o Python)
	if numCount == 0 || opCount == 0 {
		invalid()
	}

	fmt.Println(result)
}
