''' Task 05 | Expression Validator and Evaluator
Concepts: Stacks, parsing, exception handling
Problem: Create a calculator for integer expressions containing +, -, *, /, parentheses, and whitespace. Apply standard operator precedence and parentheses.
Requirements: Do not use eval(), exec(), or third-party parsers. Handle unary minus, malformed expressions, and division by zero.
Sample / expected behavior: Input: "-(3 + 2) * 4 + 18 / 3" -> -14.0.'''


import re


class ExpressionParser:

    def __init__(self, expression):
        self.tokens = re.findall(r'\d+|[()+\-*/]', expression)

        
        if ''.join(self.tokens) != ''.join(expression.split()):
            raise ValueError("Invalid character in expression")

        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def parse(self):
        if not self.tokens:
            raise ValueError("Expression cannot be empty")

        result = self.expression()

        if self.current() is not None:
            raise ValueError("Unexpected token: " + self.current())

        return result

    
    def expression(self):
        result = self.term()

        while self.current() in ("+", "-"):
            operator = self.current()
            self.position += 1

            right = self.term()

            if operator == "+":
                result += right
            else:
                result -= right

        return result

    
    def term(self):
        result = self.factor()

        while self.current() in ("*", "/"):
            operator = self.current()
            self.position += 1

            right = self.factor()

            if operator == "*":
                result *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= right

        return result

    
    def factor(self):
        token = self.current()

        
        if token == "-":
            self.position += 1
            return -self.factor()

        if token == "+":
            self.position += 1
            return self.factor()

        
        if token == "(":
            self.position += 1

            result = self.expression()

            if self.current() != ")":
                raise ValueError("Missing closing parenthesis")

            self.position += 1
            return result

        
        if token is not None and token.isdigit():
            self.position += 1
            return int(token)

        raise ValueError("Expected a number or parenthesis")


def evaluate_expression(expression):
    parser = ExpressionParser(expression)
    return parser.parse()



expression = "-(3 + 2) * 4 + 18 / 3"

try:
    result = evaluate_expression(expression)
    print("Expression:", expression)
    print("Result:", result)

except (ValueError, ZeroDivisionError) as error:
    print("Error:", error)



print("\nADDITIONAL TESTS")

test_expressions = [
    "10 + 5 * 2",
    "(10 + 5) * 2",
    "-5 + 10",
    "20 / 4",
    "2 * (3 + 4)"
]

for test in test_expressions:
    print(test, "=", evaluate_expression(test))



print("\nERROR TESTS")

invalid_expressions = [
    "2 +",
    "(3 + 2",
    "4 / 0",
    "3 ** 2",
    "2 + abc"
]

for test in invalid_expressions:
    try:
        print(test, "=", evaluate_expression(test))

    except (ValueError, ZeroDivisionError) as error:
        print(test, "->", error)
