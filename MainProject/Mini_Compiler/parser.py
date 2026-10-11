# parser.py

from ast_nodes import *
from lexer import tokens

import ply.yacc as yacc

# =====================================
# PARSE TRACE
# =====================================

parse_trace = []

def add_trace(msg):
    parse_trace.append(msg)

# =====================================
# PRECEDENCE
# =====================================

precedence = (

    ('left', 'PLUS', 'MINUS'),

    ('left', 'MULT', 'DIV')

)

# =====================================
# PROGRAM
# =====================================

def p_program(p):
    '''
    program : statement_list
    '''

    p[0] = ProgramNode(
        p[1]
    )

# =====================================
# STATEMENT LIST
# =====================================

def p_statement_list_multiple(p):
    '''
    statement_list : statement_list statement
    '''

    p[0] = p[1] + [p[2]]

def p_statement_list_single(p):
    '''
    statement_list : statement
    '''

    p[0] = [p[1]]

# =====================================
# VARIABLE DECLARATION
# =====================================

def p_var_declaration(p):
    '''
    statement : INT ID SEMICOLON
    '''

    add_trace(
        f"[DECLARATION] int {p[2]}"
    )

    p[0] = VarDeclNode(
        "int",
        p[2]
    )

# =====================================
# ASSIGNMENT
# =====================================

def p_assignment(p):
    '''
    statement : ID ASSIGN expression SEMICOLON
    '''

    add_trace(
        f"[ASSIGNMENT] {p[1]}"
    )

    p[0] = AssignNode(
        p[1],
        p[3]
    )

# =====================================
# BINARY EXPRESSIONS
# =====================================

def p_expression_binop(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression MULT expression
               | expression DIV expression
    '''

    add_trace(
        f"[EXPR] {p[2]}"
    )

    p[0] = BinOpNode(
        p[1],
        p[2],
        p[3]
    )

# =====================================
# PARENTHESIS
# =====================================

def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''

    p[0] = p[2]

# =====================================
# NUMBER
# =====================================

def p_expression_number(p):
    '''
    expression : NUMBER
    '''

    p[0] = ConstNode(
        p[1]
    )

# =====================================
# VARIABLE
# =====================================

def p_expression_variable(p):
    '''
    expression : ID
    '''

    p[0] = VarNode(
        p[1]
    )

# =====================================
# ERROR
# =====================================

def p_error(p):

    if p:

        raise Exception(
            f"Syntax Error at '{p.value}'"
        )

    else:

        raise Exception(
            "Syntax Error at EOF"
        )

# =====================================
# BUILD PARSER
# =====================================

parser = yacc.yacc()

# =====================================
# MAIN PARSE FUNCTION
# =====================================

def parse_code(source_code):

    global parse_trace

    parse_trace = []

    add_trace(
        "[INFO] Parsing Started"
    )

    ast = parser.parse(
        source_code
    )

    add_trace(
        "[SUCCESS] Parsing Completed"
    )

    return ast, parse_trace