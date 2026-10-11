# ast_nodes.py

class ASTNode:
    """Base class for all AST nodes."""
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # List of statements

class VarDeclNode(ASTNode):
    def __init__(self, var_type, var_name):
        self.var_type = var_type
        self.var_name = var_name

class AssignNode(ASTNode):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression

class ConstNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VarNode(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right