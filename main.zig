// main.zig
const std = @import("std");

fn usageAndExit() noreturn {
    const err = std.io.getStdErr().writer();
    _ = err.print("Uso: zig run main.zig -- arquivo.txt\n", .{}) catch {};
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

    const file_path = args[1];

    // Read entire file contents (read-only)
    // Set a sane upper bound if you prefer (e.g., 16 * 1024).
    const input = try std.fs.cwd().readFileAlloc(gpa, file_path, std.math.maxInt(usize));
    defer gpa.free(input);

    // Pré-processamento: remove espaços e mantém apenas dígitos e +-
    var filtered = std.ArrayList(u8).init(gpa);
    defer filtered.deinit();
    try filtered.ensureTotalCapacity(input.len);

    for (input) |c| {
        switch (c) {
            ' ' => {}, // skip space
            '0'...'9', '+', '-' => filtered.appendAssumeCapacity(c),
            else => {}, // ignore all other chars (e.g., newlines)
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
            if (i == 0 or i == fb.len - 1 or !have_num) {
                invalidAndExit();
            }
            const n = std.fmt.parseInt(i128, num_buf.items, 10) catch invalidAndExit();
            if (num_count == 0) {
                result = n;
            } else if (last_op == '+') {
                result += n;
            } else {
                result -= n;
            }
            num_count += 1;
            num_buf.clearRetainingCapacity();
            have_num = false;

            last_op = ch;
            op_count += 1;
        } else {
            try num_buf.append(ch);
            have_num = true;
        }
    }

    if (have_num) {
        const n = std.fmt.parseInt(i128, num_buf.items, 10) catch invalidAndExit();
        if (num_count == 0) {
            result = n;
        } else if (last_op == '+') {
            result += n;
        } else {
            result -= n;
        }
        num_count += 1;
    }

    if (num_count == 0 or op_count == 0) {
        invalidAndExit();
    }

    const out = std.io.getStdOut().writer();
    try out.print("{d}\n", .{result});
}
