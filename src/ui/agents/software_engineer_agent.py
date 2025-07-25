def generate_plan_and_code(requirments_doc):
    plan = "Design plan: Use argparse for CLI parsing, basic arithmetic functions for operations."
    code = '''
import argparse

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b

parser = argparse.ArgumentParser(description="Simple Calculator")
parser.add_argument("op", choices=["+", "-", "*", "/"])
parser.add_argument("a", type=float)
parser.add_argument("b", type=float)
args = parser.parse_args()

operations = {"+": add, "-": subtract, "*": multiply, "/": divide}
result = operations[args.op](args.a, args.b)
print("Result:", result)
'''
    return plan, code