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


# ---------------- PARSER ---------------- #

def parse(tokens):
    pos = 0

    def peek():
        return tokens[pos]

    def advance():
        nonlocal pos
        pos += 1

    def parse_expression():
        node = parse_term()
        while peek()[0] == "OP" and peek()[1] in "+-":
            op = peek()[1]
            advance()
            right = parse_term()
            node = ("bin", op, node, right)
        return node

    def parse_term():
        node = parse_factor()
        while True:
            tok_type, tok_val = peek()

            if tok_type == "OP" and tok_val in "*/":
                op = tok_val
                advance()
                right = parse_factor()
                node = ("bin", op, node, right)

            # Implicit multiplication: e.g. 2(3+4)
            elif tok_type in ("NUM", "LPAREN"):
                right = parse_factor()
                node = ("bin", "*", node, right)

            else:
                break

        return node

    def parse_factor():
        tok_type, tok_val = peek()

        # Unary negation: handles -5, --5, -(3+4)
        if tok_type == "OP" and tok_val == "-":
            advance()
            operand = parse_factor()
            return ("neg", operand)

        if tok_type == "OP" and tok_val == "+":
            raise ValueError("Unary + is not allowed")

        elif tok_type == "NUM":
            advance()
            return ("num", tok_val)

        elif tok_type == "LPAREN":
            advance()
            node = parse_expression()
            if peek()[0] != "RPAREN":
                raise ValueError("Missing )")
            advance()
            return node

        else:
            raise ValueError("Invalid syntax")

    tree = parse_expression()

    if peek()[0] != "END":
        raise ValueError("Extra tokens after expression")

    return tree
