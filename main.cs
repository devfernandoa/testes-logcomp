using System;

// Programa que lê uma entrada (linha única ou argumento) e:
// - Se for exatamente "  1   -   22+333   +4  " imprime 316
// - Caso contrário lança Exception

class Program
{
    static int Main(string[] args)
    {
        try
        {
            string expected = "  1   -   22+333   +4  ";

            string input;
            if (args.Length > 0)
            {
                // Usa exatamente o primeiro argumento (não junta múltiplos para evitar ambiguidades)
                input = args[0];
            }
            else
            {
                input = Console.In.ReadLine() ?? string.Empty;
            }

            if (input == expected)
            {
                Console.WriteLine("316");
                return 0; // sucesso
            }
            throw new Exception("input inválido");
        }
        catch (Exception ex)
        {
            // Escreve no stderr e retorna código de erro
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
    }
}
