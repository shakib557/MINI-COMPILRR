# symbol_table.py

from ast_nodes import *

def build_symbol_table(ast_root):
    """
    Builds a symbol table from AST.
    Supports variable names with special characters: @ # $ & *
    """

    table = {}

    def visit(node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                visit(stmt)

        elif isinstance(node, VarDeclNode):
            # Initial value None
            table[node.var_name] = {'type': node.var_type, 'value': None}

        elif isinstance(node, AssignNode):
            val = evaluate(node.expression)
            if node.var_name in table:
                table[node.var_name]['value'] = val
            else:
                table[node.var_name] = {'type':'int','value':val}

    def evaluate(node):
        if isinstance(node, ConstNode):
            return node.value
        elif isinstance(node, VarNode):
            return table[node.var_name]['value']
        elif isinstance(node, BinOpNode):
            left_val = evaluate(node.left)
            right_val = evaluate(node.right)
            if node.op == '+': return left_val + right_val
            if node.op == '-': return left_val - right_val
            if node.op == '*': return left_val * right_val
            if node.op == '/': return left_val // right_val
        return None

    visit(ast_root)
    return table