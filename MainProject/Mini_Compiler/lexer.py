# lexer.py

import ply.lex as lex

# =====================================
# TOKENS
# =====================================

tokens = (

    'INT',
    'ID',
    'NUMBER',

    'PLUS',
    'MINUS',
    'MULT',
    'DIV',

    'ASSIGN',
    'SEMICOLON',

    'LPAREN',
    'RPAREN'
)

# =====================================
# RESERVED WORDS
# =====================================

reserved = {
    'int': 'INT'
}

# =====================================
# SIMPLE TOKENS
# =====================================

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

t_ASSIGN = r'='
t_SEMICOLON = r';'

t_LPAREN = r'\('
t_RPAREN = r'\)'

# =====================================
# IGNORE SPACES
# =====================================

t_ignore = ' \t'

# =====================================
# NEW LINE TRACKING
# =====================================

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# =====================================
# IDENTIFIERS
#
# Supports:
# a
# abc
# test$
# user#
# data@
# value&
# ptr*
# =====================================

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_@$#&*]*'

    t.type = reserved.get(
        t.value,
        'ID'
    )

    return t

# =====================================
# NUMBER
# =====================================

def t_NUMBER(t):
    r'\d+'

    t.value = int(t.value)

    return t

# =====================================
# ERROR HANDLING
# =====================================

def t_error(t):

    raise Exception(
        f"Illegal Character '{t.value[0]}' at Line {t.lineno}"
    )

# =====================================
# BUILD LEXER
# =====================================

lexer = lex.lex()

# =====================================
# TOKENIZE FUNCTION
# =====================================

def tokenize(source_code):

    lexer.lineno = 1

    lexer.input(source_code)

    token_list = []

    while True:

        tok = lexer.token()

        if not tok:
            break

        token_list.append(tok)

    return token_list