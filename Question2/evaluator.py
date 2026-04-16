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

        elif char.isdigit() or char == ".":
            num = ""
            dot_count = 0

            while i < n and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        return None
                num += expression[i]
                i += 1

            # Reject "." by itself
            if num == ".":
                return None

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

            # Implicit multiplication, e.g. 2(3+4) or (2+3)(4+5)
            elif tok_type in ("NUM", "LPAREN"):
                right = parse_factor()
                node = ("bin", "*", node, right)

            else:
                break

        return node

    def parse_factor():
        tok_type, tok_val = peek()

        # Unary negation allowed
        if tok_type == "OP" and tok_val == "-":
            advance()
            operand = parse_factor()
            return ("neg", operand)

        # Unary plus NOT allowed
        if tok_type == "OP" and tok_val == "+":
            raise ValueError("Unary + is not allowed")

        if tok_type == "NUM":
            advance()
            return ("num", tok_val)

        if tok_type == "LPAREN":
            advance()
            node = parse_expression()

            if peek()[0] != "RPAREN":
                raise ValueError("Missing closing parenthesis")

            advance()
            return node

        raise ValueError("Invalid syntax")

    tree = parse_expression()

    if peek()[0] != "END":
        raise ValueError("Extra tokens after expression")

    return tree


# ---------------- EVALUATOR ---------------- #

def evaluate(node):
    if node[0] == "num":
        return float(node[1])

    if node[0] == "neg":
        return -evaluate(node[1])

    if node[0] == "bin":
        op = node[1]
        left = evaluate(node[2])
        right = evaluate(node[3])

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right

    raise ValueError("Invalid evaluation node")


# ---------------- FORMATTING ---------------- #

def format_number_string(num_string):
    value = float(num_string)
    if value.is_integer():
        return str(int(value))
    return str(round(value, 4))


def format_tree(node):
    if node[0] == "num":
        return format_number_string(node[1])

    if node[0] == "neg":
        return "(neg " + format_tree(node[1]) + ")"

    if node[0] == "bin":
        op = node[1]
        left = format_tree(node[2])
        right = format_tree(node[3])
        return "(" + op + " " + left + " " + right + ")"

    return "ERROR"


def format_tokens(token_list):
    parts = []
    for tok_type, tok_val in token_list:
        if tok_type == "END":
            parts.append("[END:]")
        else:
            parts.append(f"[{tok_type}:{tok_val}]")
    return " ".join(parts)


def format_result(value):
    if float(value).is_integer():
        return str(int(value))
    return str(round(value, 4))


# ---------------- MAIN FUNCTION ---------------- #

def evaluate_file(input_path: str) -> list[dict]:
    results = []
    output_path = os.path.join(os.path.dirname(os.path.abspath(input_path)), "output.txt")

    with open(input_path, "r") as infile:
        lines = infile.readlines()

    with open(output_path, "w") as outfile:
        for line in lines:
            expr = line.rstrip("\n")

            if expr.strip() == "":
                continue

            tree_str = "ERROR"
            token_str = "ERROR"
            result_str = "ERROR"
            result_val = "ERROR"

            try:
                token_list = tokenize(expr)
                if token_list is None:
                    raise ValueError("Invalid token")

                tree = parse(token_list)

                tree_str = format_tree(tree)
                token_str = format_tokens(token_list)

                try:
                    value = evaluate(tree)
                    result_str = format_result(value)
                    result_val = float(value)
                except Exception:
                    result_str = "ERROR"
                    result_val = "ERROR"

            except Exception:
                tree_str = "ERROR"
                token_str = "ERROR"
                result_str = "ERROR"
                result_val = "ERROR"

            outfile.write("Input: " + expr + "\n")
            outfile.write("Tree: " + tree_str + "\n")
            outfile.write("Tokens: " + token_str + "\n")
            outfile.write("Result: " + result_str + "\n\n")

            results.append({
                "input": expr,
                "tree": tree_str,
                "tokens": token_str,
                "result": result_val
            })

    return results


# ---------------- RUN DIRECTLY ---------------- #

if __name__ == "__main__":
    import sys

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(script_dir, "sample_input.txt")

    print("=" * 50)
    print("Reading:", input_file)
    print("=" * 50)

    results = evaluate_file(input_file)

    for item in results:
        print("Input  :", item["input"])
        print("Tree   :", item["tree"])
        print("Tokens :", item["tokens"])
        if item["result"] == "ERROR":
            print("Result : ERROR")
        else:
            print("Result :", format_result(item["result"]))
        print()