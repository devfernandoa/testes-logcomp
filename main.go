// main.go
package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "Uso: go run main.go 'conta'")
		os.Exit(1)
	}

	original := os.Args[1]

	// Pré-processamento: remove espaços e mantém apenas dígitos e +-
	filteredBytes := make([]byte, 0, len(original))
	for i := 0; i < len(original); i++ {
		c := original[i]
		if c == ' ' { // ignora espaços
			continue
		}
		if (c >= '0' && c <= '9') || c == '+' || c == '-' {
			filteredBytes = append(filteredBytes, c)
		}
	}
	if len(filteredBytes) == 0 {
		fmt.Fprintln(os.Stderr, "Erro: input inválido")
		os.Exit(1)
	}

	expr := string(filteredBytes)

	// Análise léxica semelhante ao Python
	nums := make([]int, 0, 8)
	ops := make([]byte, 0, 8)
	num := 0
	building := false

	for i := 0; i < len(expr); i++ {
		c := expr[i]
		if c >= '0' && c <= '9' {
			num = num*10 + int(c-'0')
			building = true
			// Se for último caractere, fecha número.
			if i == len(expr)-1 {
				nums = append(nums, num)
			}
			continue
		}
		// c é + ou -
		if !building || i == 0 || i == len(expr)-1 { // número ausente ou operador em extremidade
			fmt.Fprintln(os.Stderr, "Erro: input inválido")
			os.Exit(1)
		}
		nums = append(nums, num)
		num = 0
		building = false
		ops = append(ops, c)
	}

	if len(nums) == 0 || len(ops) == 0 { // precisa ter ao menos um operador e números
		fmt.Fprintln(os.Stderr, "Erro: input inválido")
		os.Exit(1)
	}

	// Geração de resultado
	resultado := nums[0]
	for i := 1; i < len(nums); i++ {
		if ops[i-1] == '+' {
			resultado += nums[i]
		} else {
			resultado -= nums[i]
		}
	}
	fmt.Println(resultado)
}
