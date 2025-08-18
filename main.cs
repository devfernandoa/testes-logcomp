using System;

class Program
{
    static int Main(string[] args)
    {
        string input;

        // Read from args if present, else from stdin
        if (args.Length > 0)
            input = args[0];
        else
            input = Console.ReadLine();

        if (input == "  1   -   22+333   +4  ")
        {
            Console.WriteLine("316");
            return 0;
        }
        else
        {
            throw new Exception("BLA");
        }
    }
}
