# main.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from lexer import tokenize
from parser import parse_code
from symbol_table import build_symbol_table
from intermediate_code import generate_icode
from optimizer import optimize_icode
from ast_nodes import ASTNode

FONT = ("Consolas", 12)

class MiniCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Mini Compiler v1.0")
        self.root.geometry("1400x850")
        self.root.configure(bg="#f0f0f0")

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(
            root, textvariable=self.status_var, relief="sunken",
            anchor="w", font=("Segoe UI", 10)
        )
        self.status_bar.pack(side="bottom", fill="x")

        # Tabs
        self.tab_control = ttk.Notebook(root)
        self.source_tab = scrolledtext.ScrolledText(self.tab_control, font=FONT)
        self.tokens_tab = scrolledtext.ScrolledText(self.tab_control, font=FONT)
        self.parse_tab = scrolledtext.ScrolledText(self.tab_control, font=FONT)
        self.symbol_tab = scrolledtext.ScrolledText(self.tab_control, font=FONT)
        self.icode_tab = scrolledtext.ScrolledText(self.tab_control, font=FONT)
        self.opt_tab = scrolledtext.ScrolledText(self.tab_control, font=FONT)
        self.ast_tab = scrolledtext.ScrolledText(self.tab_control, font=FONT)

        self.tab_control.add(self.source_tab, text="Source Code")
        self.tab_control.add(self.tokens_tab, text="Tokens")
        self.tab_control.add(self.parse_tab, text="Parse Trace")
        self.tab_control.add(self.symbol_tab, text="Symbol Table")
        self.tab_control.add(self.icode_tab, text="Intermediate Code")
        self.tab_control.add(self.opt_tab, text="Optimized Code")
        self.tab_control.add(self.ast_tab, text="AST Tree")
        self.tab_control.pack(expand=1, fill='both')

        # Compile Button
        self.compile_btn = tk.Button(
            root, text="Compile", font=("Segoe UI", 12, "bold"),
            bg="#4CAF50", fg="white", command=self.compile_code
        )
        self.compile_btn.pack(pady=5)

    def compile_code(self):
        source = self.source_tab.get("1.0", tk.END)
        self.clear_all_tabs()
        try:
            # Tokens
            tokens_list = tokenize(source)
            self.tokens_tab.insert(
                tk.END,
                "\n".join([f"{t.type}\t{t.value}\tLine {t.lineno}" for t in tokens_list])
            )

            # AST & Parse Trace
            ast, trace = parse_code(source)
            self.parse_tab.insert(tk.END, "\n".join(trace))

            # Symbol Table
            symbol_table = build_symbol_table(ast)
            self.symbol_tab.insert(
                tk.END,
                "\n".join([f"{k} -> {v}" for k,v in symbol_table.items()])
            )

            # Intermediate Code
            icode = generate_icode(ast)
            self.icode_tab.insert(tk.END, "\n".join(icode))

            # Optimized Code
            optimized = optimize_icode(icode)
            self.opt_tab.insert(tk.END, "\n".join(optimized))

            # AST Tree
            self.ast_tab.insert(tk.END, self.print_ast(ast))

            self.status_var.set(f"Compilation Successful ✓ | Tokens: {len(tokens_list)}")
            messagebox.showinfo("Success", "Compilation Successful!")

        except Exception as e:
            self.status_var.set("Compilation Failed ✗")
            messagebox.showerror("Error", str(e))

    def print_ast(self, node, level=0):
        indent = "  " * level
        text = f"{indent}{node.__class__.__name__}"

        if hasattr(node, "var_name"):
            text += f" ({node.var_name})"
        if hasattr(node, "op"):
            text += f" [{node.op}]"
        if hasattr(node, "value"):
            text += f" = {node.value}"

        text += "\n"

        if hasattr(node, "statements"):
            for stmt in node.statements:
                text += self.print_ast(stmt, level + 1)

        if hasattr(node, "expression"):
            text += self.print_ast(node.expression, level + 1)

        if hasattr(node, "left"):
            text += self.print_ast(node.left, level + 1)
        if hasattr(node, "right"):
            text += self.print_ast(node.right, level + 1)

        return text

    def clear_all_tabs(self):
        for tab in [self.tokens_tab, self.parse_tab, self.symbol_tab,
                    self.icode_tab, self.opt_tab, self.ast_tab]:
            tab.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = MiniCompilerGUI(root)
    root.mainloop()