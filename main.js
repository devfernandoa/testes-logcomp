// main.js

if (process.argv.length !== 3) {
    console.error("Uso: node main.js 'conta'");
    process.exit(1);
}

// Pré-processamento
let cadeia = process.argv[2];
let cadeiaSemEspacos = cadeia.replace(/ /g, "");
cadeiaSemEspacos = [...cadeiaSemEspacos].filter(c => /\d/.test(c) || c === "+" || c === "-").join("");

// Se input não for válido dar um stderr
if (cadeiaSemEspacos.length === 0) {
    console.error("Erro: input inválido");
    process.exit(1);
}

let listaOperacoes = [];
let listaNumeros = [];
let num = "";

// Análise léxica
for (let i = 0; i < cadeiaSemEspacos.length; i++) {
    if (cadeiaSemEspacos[i] === "+" || cadeiaSemEspacos[i] === "-") {
        if (num === "" || i === 0 || i === cadeiaSemEspacos.length - 1) {
            console.error("Erro: input inválido");
            process.exit(1);
        }
        listaOperacoes.push(cadeiaSemEspacos[i]);
        if (num) {
            listaNumeros.push(parseInt(num));
            num = "";
        }
    } else {
        num += cadeiaSemEspacos[i];
    }
}
if (num) {
    listaNumeros.push(parseInt(num));
}

if (listaNumeros.length === 0 || listaOperacoes.length === 0) {
    console.error("Erro: input inválido");
    process.exit(1);
}

let resultado = 0;

// Gera resultado
for (let i = 0; i < listaNumeros.length; i++) {
    if (i === 0) {
        resultado = listaNumeros[i];
    } else {
        if (listaOperacoes[i - 1] === "+") {
            resultado += listaNumeros[i];
        } else {
            resultado -= listaNumeros[i];
        }
    }
}

console.log(resultado);