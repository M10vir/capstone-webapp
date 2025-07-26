def generate_plan_and_code(requirments_doc: dict) -> tuple[str, str]:
    """Convert requirments inot a design plan and working CLI code."""
    plan = (
        "Design plan:\n"
        "- Use argparse for CLI input parsing\n"
        "- Implement functions for +, -, *, /\n"
        "- handle divide-by-zero gracefully\n"
        "- Package in a single .py file, no external dependencies"
    )

    code = '''\
import argparse

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Error: Divide by zero"

parser = argparse.ArgumentParser(description="Simple CLI Calculator")
parser.add_argument("op", choices=["+", "-", "*", "/"], help="Operation")
parser.add_argument("a", type=float, help="First operand")
parser.add_argument("b", type=float, help="Second operand")
args = parser.parse_args()

operations = {"+": add, "-": subtract, "*": multiply, "/": divide}
result = operations[args.op](args.a, args.b)
print("Result:", result)
'''
    return plan, code
