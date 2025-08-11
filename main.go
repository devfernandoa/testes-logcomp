// main.go
package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"os"
)

func usage() {
	fmt.Fprintln(os.Stderr, "Uso: go run main.go 'conta'")
	os.Exit(1)
}

func invalid() {
	fmt.Fprintln(os.Stderr, "Erro: input inválido")
	os.Exit(1)
}

func readInput() string {
	// Prefer argv[1] if present
	if len(os.Args) == 2 {
		return os.Args[1]
	}

	// If stdin is not a TTY (i.e., piped), read it; otherwise show usage
	info, err := os.Stdin.Stat()
	if err == nil && (info.Mode()&os.ModeCharDevice) == 0 {
		// Read up to a reasonable size; no need to hang
		var buf bytes.Buffer
		r := bufio.NewReader(os.Stdin)
		_, _ = io.Copy(&buf, r)
		return buf.String()
	}

	usage()
	return "" // unreachable
}

func main() {
	in := readInput()

	// Pré-processamento: remove espaços e mantém apenas dígitos e +-
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
			// inválido se operador for primeiro, último ou se não houve número antes
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
