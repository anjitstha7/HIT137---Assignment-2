import os


# ---------------- TOKENIZER ---------------- #

def tokenize(expression):
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        elif char.isdigit() or char == '.':
            num = char
            i += 1
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(("NUM", num))

        elif char in "+-*/":
            tokens.append(("OP", char))
            i += 1

        elif char == "(":
            tokens.append(("LPAREN", "("))
            i += 1

        elif char == ")":
            tokens.append(("RPAREN", ")"))
            i += 1

        else:
            return None

    tokens.append(("END", None))
    return tokens