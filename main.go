// main.go
package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "Uso: go run main.go 'conta'")
		os.Exit(1)
	}

	expr := os.Args[1]
	expr = removeSpaces(expr)
	if expr == "" {
		fmt.Fprintln(os.Stderr, "Erro: input inválido")
		os.Exit(1)
	}

	res, err := evalSimple(expr)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Erro: input inválido")
		os.Exit(1)
	}
	fmt.Println(res)
}

func removeSpaces(s string) string {
	out := ""
	for _, c := range s {
		if c != ' ' {
			out += string(c)
		}
	}
	return out
}

func evalSimple(expr string) (int, error) {
	n := len(expr)
	if n == 0 {
		return 0, fmt.Errorf("vazio")
	}
	res := 0
	num := ""
	op := byte('+')
	for i := 0; i < n; i++ {
		c := expr[i]
		if c >= '0' && c <= '9' {
			num += string(c)
		}
		if c == '+' || c == '-' || i == n-1 {
			if num == "" {
				return 0, fmt.Errorf("input inválido")
			}
			val, err := strconv.Atoi(num)
			if err != nil {
				return 0, err
			}
			if op == '+' {
				res += val
			} else {
				res -= val
			}
			op = c
			num = ""
		}
	}
	// Se terminou com operador, erro
	if num == "" && (expr[n-1] == '+' || expr[n-1] == '-') {
		return 0, fmt.Errorf("input inválido")
	}
	return res, nil
}
