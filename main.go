// main.go
package main

import (
	"bufio"
	"bytes"
	"fmt"
	"go/constant"
	"go/token"
	"go/types"
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
	if len(os.Args) == 2 {
		return os.Args[1]
	}
	info, err := os.Stdin.Stat()
	if err == nil && (info.Mode()&os.ModeCharDevice) == 0 {
		var buf bytes.Buffer
		r := bufio.NewReader(os.Stdin)
		_, _ = io.Copy(&buf, r)
		return buf.String()
	}
	usage()
	return ""
}

func main() {
	in := readInput()

	// Keep only digits and +-, skip spaces
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

	// Basic validation like the Python version
	if filtered[0] == '+' || filtered[0] == '-' || filtered[len(filtered)-1] == '+' || filtered[len(filtered)-1] == '-' {
		invalid()
	}
	for i := 1; i < len(filtered); i++ {
		if (filtered[i] == '+' || filtered[i] == '-') && (filtered[i-1] == '+' || filtered[i-1] == '-') {
			invalid()
		}
	}

	// Eval using go/types
	expr := string(filtered)
	fset := token.NewFileSet()
	pkg := types.NewPackage("p", "p")
	tv, err := types.Eval(fset, pkg, token.NoPos, expr)
	if err != nil {
		invalid()
	}
	v := constant.ToInt(tv.Value)
	if v == nil {
		invalid()
	}

	// Print exact integer value (arbitrary precision)
	fmt.Println(constant.String(v))
}
