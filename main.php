<?php
// main.php

if ($argc !== 2) {
    fwrite(STDERR, "Uso: php main.php 'conta'\n");
    exit(1);
}

// Pré-processamento
$cadeia = $argv[1];
$cadeiaSemEspacos = str_replace(' ', '', $cadeia);

// Mantém apenas dígitos e +-
$filtered = '';
$len = strlen($cadeiaSemEspacos);
for ($i = 0; $i < $len; $i++) {
    $c = $cadeiaSemEspacos[$i];
    if (($c >= '0' && $c <= '9') || $c === '+' || $c === '-') {
        $filtered .= $c;
    }
}

// Se input não for válido dar um stderr
if ($filtered === '') {
    fwrite(STDERR, "Erro: input inválido\n");
    exit(1);
}

$listaOperacoes = [];
$listaNumeros = [];
$num = "";

// Análise léxica
$L = strlen($filtered);
for ($i = 0; $i < $L; $i++) {
    $ch = $filtered[$i];
    if ($ch === '+' || $ch === '-') {
        if ($num === "" || $i === 0 || $i === $L - 1) {
            fwrite(STDERR, "Erro: input inválido\n");
            exit(1);
        }
        $listaOperacoes[] = $ch;
        if ($num !== "") {
            $listaNumeros[] = intval($num, 10);
            $num = "";
        }
    } else {
        $num .= $ch;
    }
}
if ($num !== "") {
    $listaNumeros[] = intval($num, 10);
}

if (count($listaNumeros) === 0 || count($listaOperacoes) === 0) {
    fwrite(STDERR, "Erro: input inválido\n");
    exit(1);
}

// Gera resultado
$resultado = 0;
for ($i = 0; $i < count($listaNumeros); $i++) {
    if ($i === 0) {
        $resultado = $listaNumeros[$i];
    } else {
        if ($listaOperacoes[$i - 1] === '+') {
            $resultado += $listaNumeros[$i];
        } else {
            $resultado -= $listaNumeros[$i];
        }
    }
}

echo $resultado . PHP_EOL;
