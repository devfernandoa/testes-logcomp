if (args.size != 1) {
    System.err.println("Uso: kotlin Main.kt 'conta'")
    exitProcess(1)
}

val cadeia = args[0]
// Remove espaços e mantém apenas dígitos e +-
val cadeiaSemEspacos = cadeia.replace(" ", "")
    .filter { it.isDigit() || it == '+' || it == '-' }

if (cadeiaSemEspacos.isEmpty()) {
    System.err.println("Erro: input inválido")
    exitProcess(1)
}

val listaOperacoes = mutableListOf<Char>()
val listaNumeros = mutableListOf<Int>()
val numBuilder = StringBuilder()

for (i in cadeiaSemEspacos.indices) {
    val ch = cadeiaSemEspacos[i]
    if (ch == '+' || ch == '-') {
        if (numBuilder.isEmpty() || i == 0 || i == cadeiaSemEspacos.lastIndex) {
            System.err.println("Erro: input inválido")
            exitProcess(1)
        }
        listaOperacoes.add(ch)
        if (numBuilder.isNotEmpty()) {
            listaNumeros.add(numBuilder.toString().toInt())
            numBuilder.clear()
        }
    } else {
        numBuilder.append(ch)
    }
}
if (numBuilder.isNotEmpty()) {
    listaNumeros.add(numBuilder.toString().toInt())
}

if (listaNumeros.isEmpty() || listaOperacoes.isEmpty()) {
    System.err.println("Erro: input inválido")
    exitProcess(1)
}

var resultado = 0
for (i in listaNumeros.indices) {
    if (i == 0) {
        resultado = listaNumeros[i]
    } else {
        if (listaOperacoes[i - 1] == '+') {
            resultado += listaNumeros[i]
        } else {
            resultado -= listaNumeros[i]
        }
    }
}

println(resultado)
