// main.swift
import Foundation

@inline(__always)
func stderr(_ message: String) {
    FileHandle.standardError.write(Data((message + "\n").utf8))
}

@inline(__always)
func usageAndExit() -> Never {
    stderr("Uso: swift main.swift 'conta'")
    exit(1)
}

@inline(__always)
func invalidAndExit() -> Never {
    stderr("Erro: input inválido")
    exit(1)
}

let args = CommandLine.arguments
if args.count != 2 {
    usageAndExit()
}

// Pré-processamento
let cadeia = args[1]
var filtered = String()
filtered.reserveCapacity(cadeia.count)

for ch in cadeia {
    if ch == " " { continue }
    if ch.isNumber || ch == "+" || ch == "-" {
        filtered.append(ch)
    }
}

// Se input não for válido dar um stderr
if filtered.isEmpty {
    invalidAndExit()
}

// Análise léxica
var listaOperacoes: [Character] = []
var listaNumeros: [Int64] = []
var num = ""

let chars = Array(filtered)
for i in 0..<chars.count {
    let ch = chars[i]
    if ch == "+" || ch == "-" {
        if num.isEmpty || i == 0 || i == chars.count - 1 {
            invalidAndExit()
        }
        if let val = Int64(num) {
            listaNumeros.append(val)
        } else {
            // overflow ou não-numérico
            invalidAndExit()
        }
        listaOperacoes.append(ch)
        num.removeAll(keepingCapacity: true)
    } else {
        // dígito
        num.append(ch)
    }
}

if !num.isEmpty {
    if let val = Int64(num) {
        listaNumeros.append(val)
    } else {
        invalidAndExit()
    }
}

if listaNumeros.isEmpty || listaOperacoes.isEmpty {
    invalidAndExit()
}

// Gera resultado
var resultado: Int64 = 0
for i in 0..<listaNumeros.count {
    if i == 0 {
        resultado = listaNumeros[i]
    } else {
        if listaOperacoes[i - 1] == "+" {
            resultado += listaNumeros[i]
        } else {
            resultado -= listaNumeros[i]
        }
    }
}

print(resultado)
