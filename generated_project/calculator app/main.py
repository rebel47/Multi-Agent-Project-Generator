def add(num1, num2):
    """
    Adds two numbers and returns the sum.
    """
    return num1 + num2

def subtract(num1, num2):
    """
    Subtracts the second number from the first and returns the difference.
    """
    return num1 - num2

def multiply(num1, num2):
    """
    Multiplies two numbers and returns the product.
    """
    return num1 * num2

def divide(num1, num2):
    """
    Divides the first number by the second and returns the quotient.
    Handles division by zero by returning an error message.
    """
    if num2 == 0:
        return "Error: Cannot divide by zero."
    return num1 / num2

def main():
    """
    Orchestrates the calculator's user interaction.
    Prompts for two numbers and an operation, then displays the result.
    Handles invalid inputs.
    """
    while True:
        try:
            num1 = float(input("Enter the first number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the first number.")

    while True:
        try:
            num2 = float(input("Enter the second number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the second number.")

    while True:
        operation = input("Enter the operation (+, -, *, /): ")
        if operation in ['+', '-', '*', '/']:
            break
        else:
            print("Invalid operation. Please choose from +, -, *, /.")

    result = None
    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        result = divide(num1, num2)

    print(f"The result is: {result}")

if __name__ == "__main__":
    main()
