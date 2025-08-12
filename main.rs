// src/main.rs
use std::env;
use std::process;

fn usage_and_exit(prog: &str) -> ! {
    eprintln!("Uso: {} 'conta'", prog);
    process::exit(1);
}

fn invalid_and_exit() -> ! {
    eprintln!("Erro: input inválido");
    process::exit(1);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        usage_and_exit(&args.get(0).map(String::as_str).unwrap_or("programa"));
    }

    // Pré-processamento
    let cadeia = &args[1];
    let mut filtered = String::with_capacity(cadeia.len());
    for b in cadeia.bytes() {
        match b {
            b' ' => {}
            b'0'..=b'9' | b'+' | b'-' => filtered.push(b as char),
            _ => {} // ignora quaisquer outros caracteres (espelha o Python)
        }
    }

    if filtered.is_empty() {
        invalid_and_exit();
    }

    // Análise léxica
    let bytes = filtered.as_bytes();
    let mut lista_operacoes: Vec<u8> = Vec::new();
    let mut lista_numeros: Vec<i128> = Vec::new();
    let mut num = String::new();

    for i in 0..bytes.len() {
        let c = bytes[i];
        if c == b'+' || c == b'-' {
            if num.is_empty() || i == 0 || i == bytes.len() - 1 {
                invalid_and_exit();
            }
            match num.parse::<i128>() {
                Ok(v) => lista_numeros.push(v),
                Err(_) => invalid_and_exit(), // overflow ou inválido
            }
            num.clear();
            lista_operacoes.push(c);
        } else {
            // dígito
            num.push(c as char);
        }
    }
    if !num.is_empty() {
        match num.parse::<i128>() {
            Ok(v) => lista_numeros.push(v),
            Err(_) => invalid_and_exit(),
        }
    }

    if lista_numeros.is_empty() || lista_operacoes.is_empty() {
        invalid_and_exit();
    }

    // Gera resultado
    let mut resultado: i128 = 0;
    for i in 0..lista_numeros.len() {
        if i == 0 {
            resultado = lista_numeros[i];
        } else {
            if lista_operacoes[i - 1] == b'+' {
                resultado += lista_numeros[i];
            } else {
                resultado -= lista_numeros[i];
            }
        }
    }

    println!("{}", resultado);
}
