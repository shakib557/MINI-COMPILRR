# intermediate_code.py

from ast_nodes import *

temp_count = 0


def new_temp():
    global temp_count

    temp_count += 1

    return f"t{temp_count}"


def generate_icode(ast_root):

    global temp_count

    temp_count = 0

    code = []

    def visit(node):

        # ----------------------
        # Program
        # ----------------------

        if isinstance(node, ProgramNode):

            for stmt in node.statements:
                visit(stmt)

        # ----------------------
        # Variable Declaration
        # ----------------------

        elif isinstance(node, VarDeclNode):

            code.append(
                f"{node.var_name} = 0"
            )

        # ----------------------
        # Assignment
        # ----------------------

        elif isinstance(node, AssignNode):

            result = visit(
                node.expression
            )

            code.append(
                f"{node.var_name} = {result}"
            )

        # ----------------------
        # Binary Operation
        # ----------------------

        elif isinstance(node, BinOpNode):

            left = visit(
                node.left
            )

            right = visit(
                node.right
            )

            temp = new_temp()

            code.append(
                f"{temp} = {left} {node.op} {right}"
            )

            return temp

        # ----------------------
        # Constant
        # ----------------------

        elif isinstance(node, ConstNode):

            return str(
                node.value
            )

        # ----------------------
        # Variable
        # ----------------------

        elif isinstance(node, VarNode):

            return node.var_name

    visit(ast_root)

    return code