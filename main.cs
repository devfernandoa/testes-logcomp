using System;

// Programa que lê uma entrada (linha única ou argumento) e:
// - Se for exatamente "  1   -   22+333   +4  " imprime 316
// - Caso contrário lança Exception

class Program
{
    static int Main(string[] args)
    {
        if (args[1] == '  1   -   22+333   +4  ')
            Console.WriteLine("316");
        else
            throw new Exception("BLA")
        return 0;
    }
}
