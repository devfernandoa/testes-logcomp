// main.zig
const std = @import("std");

fn usageAndExit() noreturn {
    const err = std.io.getStdErr().writer();
    _ = err.print("Uso: zig run main.zig 'conta'\n", .{}) catch {};
    std.process.exit(1);
}

fn invalidAndExit() noreturn {
    const err = std.io.getStdErr().writer();
    _ = err.print("Erro: input inválido\n", .{}) catch {};
    std.process.exit(1);
}

pub fn main() !void {
    const gpa = std.heap.page_allocator;

    const args = try std.process.argsAlloc(gpa);
    defer std.process.argsFree(gpa, args);

    if (args.len != 2) {
        usageAndExit();
    }

    const input = args[1];

    // Pré-processamento: remove espaços e mantém apenas dígitos e +-
    var filtered = std.ArrayList(u8).init(gpa);
    defer filtered.deinit();
    try filtered.ensureTotalCapacity(input.len);

    for (input) |c| {
        switch (c) {
            ' ' => {}, // skip
            '0'...'9', '+', '-' => filtered.appendAssumeCapacity(c),
            else => {}, // ignore any other char (como no Python)
        }
    }

    if (filtered.items.len == 0) {
        invalidAndExit();
    }

    // Análise léxica e avaliação
    const fb = filtered.items;
    var num_buf = std.ArrayList(u8).init(gpa);
    defer num_buf.deinit();

    var result: i128 = 0;
    var last_op: u8 = '+';
    var have_num = false;
    var num_count: usize = 0;
    var op_count: usize = 0;

    var i: usize = 0;
    while (i < fb.len) : (i += 1) {
        const ch = fb[i];
        if (ch == '+' or ch == '-') {
            // inválido se operador for primeiro, último ou sem número antes
            if (i == 0 or i == fb.len - 1 or !have_num) {
                invalidAndExit();
            }
            // fecha número atual
            const n = std.fmt.parseInt(i128, num_buf.items, 10) catch invalidAndExit();
            if (num_count == 0) {
                result = n;
            } else {
                if (last_op == '+') {
                    result += n;
                } else {
                    result -= n;
                }
            }
            num_count += 1;
            num_buf.clearRetainingCapacity();
            have_num = false;

            last_op = ch;
            op_count += 1;
        } else {
            // dígito
            try num_buf.append(ch);
            have_num = true;
        }
    }

    // Finaliza com o último número
    if (have_num) {
        const n = std.fmt.parseInt(i128, num_buf.items, 10) catch invalidAndExit();
        if (num_count == 0) {
            result = n;
        } else {
            if (last_op == '+') {
                result += n;
            } else {
                result -= n;
            }
        }
        num_count += 1;
    }

    // Valida listas não vazias (espelha o Python)
    if (num_count == 0 or op_count == 0) {
        invalidAndExit();
    }

    // Saída
    const out = std.io.getStdOut().writer();
    try out.print("{d}\n", .{result});
}
