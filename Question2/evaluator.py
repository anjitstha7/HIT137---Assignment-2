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

# ---------------- EVALUATOR ---------------- #

def evaluate(node):
    if node[0] == "num":
        return float(node[1])

    elif node[0] == "neg":
        return -evaluate(node[1])

    elif node[0] == "bin":
        op    = node[1]
        left  = node[2]
        right = node[3]
        l = evaluate(left)
        r = evaluate(right)

        if op == "+":
            return l + r
        elif op == "-":
            return l - r
        elif op == "*":
            return l * r
        elif op == "/":
            if r == 0:
                raise ZeroDivisionError("Division by zero")
            return l / r


# ---------------- TREE FORMAT ---------------- #

def format_tree(node):
    if node[0] == "num":
        val = float(node[1])
        return str(int(val)) if val.is_integer() else str(round(val, 4))

    elif node[0] == "neg":
        return "(neg " + format_tree(node[1]) + ")"

    elif node[0] == "bin":
        op    = node[1]
        left  = node[2]
        right = node[3]
        return "(" + op + " " + format_tree(left) + " " + format_tree(right) + ")"
    
# ---------------- TOKEN FORMAT ---------------- #

def format_tokens(token_list):
    parts = []
    for tok_type, tok_val in token_list:
        if tok_type == "END":
            continue
        parts.append(tok_val)
    return " ".join(parts)

# ---------------- RESULT FORMAT ---------------- #

def format_result(value):
    if float(value).is_integer():
        return str(int(value))
    else:
        return str(round(value, 4))
    
# ---------------- MAIN FUNCTION ---------------- #

def evaluate_file(input_path: str) -> list[dict]:
    results = []
    output_path = os.path.join(os.path.dirname(os.path.abspath(input_path)), "output.txt")

    with open(input_path, "r") as f:
        lines = f.readlines()

    with open(output_path, "w") as out:
        for line in lines:
            expr = line.rstrip("\n")

            if expr.strip() == "":
                continue

            tree_str   = "ERROR"
            token_str  = "ERROR"
            result_str = "ERROR"
            result_val = "ERROR"

            # Step 1: tokenise and parse
            try:
                token_list = tokenize(expr)

                if token_list is None:
                    raise ValueError("Unknown character in expression")

                tree      = parse(token_list)
                tree_str  = format_tree(tree)
                token_str = format_tokens(token_list)

            except Exception:
                out.write("Input: "  + expr       + "\n")
                out.write("Tree: "   + tree_str   + "\n")
                out.write("Tokens: " + token_str  + "\n")
                out.write("Result: " + result_str + "\n\n")
                results.append({"input": expr, "tree": tree_str, "tokens": token_str, "result": result_val})
                continue

            # Step 2: evaluate (tree already saved, only result becomes ERROR on failure)
            try:
                value      = evaluate(tree)
                result_str = format_result(value)
                result_val = float(value)

            except Exception:
                result_str = "ERROR"
                result_val = "ERROR"

            out.write("Input: "  + expr       + "\n")
            out.write("Tree: "   + tree_str   + "\n")
            out.write("Tokens: " + token_str  + "\n")
            out.write("Result: " + result_str + "\n\n")

            results.append({"input": expr, "tree": tree_str, "tokens": token_str, "result": result_val})

    return results


# ---------------- RUN DIRECTLY FOR TESTING ---------------- #

if __name__ == "__main__":
    import sys
    import os

    _script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_script_dir, "sample_input.txt")

    print("=" * 50)
    print("=" * 50)
    print("  Reading: " + input_file)
    print()

    results = evaluate_file(input_file)

    for r in results:
        val_str = "ERROR" if r["result"] == "ERROR" else format_result(r["result"])
        print("Input  : " + r["input"])
        print("Tree   : " + r["tree"])
        print("Tokens : " + r["tokens"])
        print("Result : " + val_str)
        print()