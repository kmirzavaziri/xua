import ply.lex as lex
rules = {
    # Keywords
    "SUPER": r"t",
    "EXTENDS": r"t",
    "CONST": r"t",
    "VALIDATION": r"t",
    "PREDICATE": r"t",
    "MARSHAL": r"t",
    "UNMARSHAL": r"t",
    "DATABASETYPE": r"t",

    "ENTITY": r"t",

    "METHOD": r"t",

    "INTERFACE": r"t",

    # Specific Values
    "TRUE": r"t",
    "FALSE": r"t",
    "NULL": r"t",

    # Operators

    # Symbols
    'LEFT_PARENTHESIS': r"t",
    'RIGHT_PARENTHESIS': r"t",

    'LEFT_BRACES': r"t",
    'RIGHT_BRACES': r"t",

    'LEFT_BRACKETS': r"t",
    'RIGHT_BRACKETS': r"t",

    'LEFT_ANGLE': r"t",
    'RIGHT_ANGLE': r"t",

    'LEFT_PHP': r"t",
    'RIGHT_PHP': r"t",

    'COMMA': r"t",
    'COLON': r"t",
    'SEMICOLON': r"t",

    'MAPS_TO': r"t",

    'EQUALS': r"t",

    'PLUS': r"t",
    'MINUS': r"t",
    'TIMES': r"t",
    'POWER': r"t",
    'DIVIDES': r"t",
    'DOUBLE_DIVIDES': r"t",
    'MOD': r"t",
    'DOT': r"t",

    # Value-Carring Tokens
    "NUMBER": r"t",
    "STRING": r"t",
    "FOREIGN_CODE": r"t",

    "ADDRESS": r"t",
    "ID": r"t",
}

tokens = list(rules.keys())

for token in tokens:
    globals()[f"t_{token}"] = rules[token]


def t_error(t):
    print(f"Unknown character {t.value[0]}")
    t.lexer.skip(1)


lexer = lex.lex()
lexer.input('test')
while True:
    token = lexer.token()
    if token:
        print(token)
    else:
        break
