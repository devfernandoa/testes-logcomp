// main.js

if (process.argv.length !== 3) {
    console.error("Uso: node main.ts 'conta'");
    process.exit(1);
}

// Pré-processamento
const cadeia: string = process.argv[2];
let cadeiaSemEspacos: string = cadeia.replace(/ /g, "");
cadeiaSemEspacos = [...cadeiaSemEspacos].filter((c: string) => /\d/.test(c) || c === "+" || c === "-").join("");

// Se input não for válido dar um stderr
if (cadeiaSemEspacos.length === 0) {
    console.error("Erro: input inválido");
    process.exit(1);
}

const listaOperacoes: string[] = [];
const listaNumeros: number[] = [];
let num: string = "";

// Análise léxica
for (let i = 0; i < cadeiaSemEspacos.length; i++) {
    const char: string = cadeiaSemEspacos[i];
    if (char === "+" || char === "-") {
        if (num === "" || i === 0 || i === cadeiaSemEspacos.length - 1) {
            console.error("Erro: input inválido");
            process.exit(1);
        }
        listaOperacoes.push(char);
        if (num) {
            listaNumeros.push(Number(num));
            num = "";
        }
    } else {
        num += char;
    }
}
if (num) {
    listaNumeros.push(Number(num));
}

if (listaNumeros.length === 0 || listaOperacoes.length === 0) {
    console.error("Erro: input inválido");
    process.exit(1);
}

let resultado: number = 0;

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