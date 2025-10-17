def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def run_calculator():
    """
    Orchestrates the calculator's operations by prompting the user for input,
    validating it, performing the calculation, and displaying the result.
    """
    while True:
        try:
            num1_str = input("Enter the first number: ")
            num1 = float(num1_str)

            operator = input("Enter an operator (+, -, *, /): ")
            if operator not in ['+', '-', '*', '/']:
                print("Error: Invalid operator. Please use +, -, *, or /.")
                continue

            num2_str = input("Enter the second number: ")
            num2 = float(num2_str)

            result = None
            if operator == '+':
                result = add(num1, num2)
            elif operator == '-':
                result = subtract(num1, num2)
            elif operator == '*':
                result = multiply(num1, num2)
            elif operator == '/':
                result = divide(num1, num2)
            
            print(f"Result: {result}")
            break

        except ValueError as e:
            print(f"Error: Invalid input. {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    run_calculator()
