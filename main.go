// main.go
package main

import(
    "fmt"
    "os"
    "strconv"
    "unicode"
)

func main() {
    if len(os.Args) != 2 {
        fmt.Fprintln(os.Stderr, "Uso: go run main.go 'conta'")
        os.Exit(1)
    }

    cadeia:= os.Args[1]
    cadeiaSemEspacos:= ""
    for _, c := range cadeia {
        if c != ' ' {
            cadeiaSemEspacos += string(c)
        }
    }

    // Mantém apenas dígitos e +-
    aux:= ""
    for _, c := range cadeiaSemEspacos {
        if unicode.IsDigit(c) || c == '+' || c == '-' {
            aux += string(c)
        }
    }
    cadeiaSemEspacos = aux

    if len(cadeiaSemEspacos) == 0 {
        fmt.Fprintln(os.Stderr, "Erro: input inválido")
        os.Exit(1)
    }

    var listaOperacoes []rune
    var listaNumeros []int
    num:= ""

    for i, c := range cadeiaSemEspacos {
        if c == '+' || c == '-' {
            if num == "" || i == 0 || i == len(cadeiaSemEspacos) - 1 {
                fmt.Fprintln(os.Stderr, "Erro: input inválido")
                os.Exit(1)
            }
            listaOperacoes = append(listaOperacoes, c)
            if num != "" {
                n, err := strconv.Atoi(num)
                if err != nil {
                    fmt.Fprintln(os.Stderr, "Erro: input inválido")
                    os.Exit(1)
                }
                listaNumeros = append(listaNumeros, n)
                num = ""
            }
        } else {
            num += string(c)
        }
    }
    if num != "" {
        n, err := strconv.Atoi(num)
        if err != nil {
            fmt.Fprintln(os.Stderr, "Erro: input inválido")
            os.Exit(1)
        }
        listaNumeros = append(listaNumeros, n)
    }

    if len(listaNumeros) == 0 || len(listaOperacoes) == 0 {
        fmt.Fprintln(os.Stderr, "Erro: input inválido")
        os.Exit(1)
    }

    resultado:= 0
    for i, n := range listaNumeros {
        if i == 0 {
            resultado = n
        } else {
            if listaOperacoes[i - 1] == '+' {
                resultado += n
            } else {
                resultado -= n
            }
        }
    }

    fmt.Println(resultado)
}