
from flask import Flask, request, jsonify, render_template
from z3 import *
import re

app = Flask(__name__)


def tokenize_expression(expr):
    """Convert a string math expression to Z3 expressions"""
    # Replace spaces
    expr = expr.replace(' ', '')

    # Extract variables and coefficients
    tokens = re.findall(r'([+-]?)([0-9]*\.?[0-9]*)([a-zA-Z]*)', expr)

    result = 0
    for sign, coef, var in tokens:
        if not (coef or var):  # Skip empty tokens
            continue

        # Handle the sign
        sign_val = -1 if sign == '-' else 1

        # Handle coefficient
        if coef:
            coef_val = float(coef) if coef else 1
        else:
            coef_val = 1

        # Apply sign
        coef_val *= sign_val

        # Handle the variable or constant
        if var:
            if var in var_dict:
                term = coef_val * var_dict[var]
            else:
                var_dict[var] = Real(var)
                term = coef_val * var_dict[var]
        else:
            term = coef_val

        result += term

    return result


def parse_equation(equation_str):
    """Parse and solve equations using Z3"""
    global var_dict
    var_dict = {}  # Reset var_dict for each equation

    try:
        # Clean up the input
        equation_str = equation_str.strip()

        # Handle equations with = sign
        if '=' in equation_str:
            parts = equation_str.split('=')
            if len(parts) != 2:
                return "Error: Equation should have exactly one '=' sign."

            left_expr = parts[0].strip()
            right_expr = parts[1].strip()

            # If right side is empty, treat as "= 0"
            if not right_expr:
                right_expr = "0"

            # Parse both sides
            left_side = tokenize_expression(left_expr)
            right_side = tokenize_expression(right_expr)

            # Set up solver
            s = Solver()
            s.add(left_side == right_side)

            # Solve
            if s.check() == sat:
                model = s.model()
                return {str(var): str(model[var_dict[var]]) for var in var_dict}
            else:
                return "No solution found."

        # Handle arithmetic expressions without = sign
        elif re.search(r'[+\-*/]', equation_str) and '=' not in equation_str:
            # Evaluate as a simple arithmetic expression
            result = eval(equation_str)
            return f"Result: {result}"

        else:
            return "Error: No equation or arithmetic operation found."

    except Exception as e:
        return f"Error solving equation: {str(e)}"


def solve_system_of_equations(equations):
    """Solve a system of multiple equations using Z3"""
    global var_dict
    var_dict = {}  # Reset var_dict for the system

    try:
        # Set up solver
        s = Solver()

        # Process each equation
        for equation_str in equations:
            equation_str = equation_str.strip()

            if '=' in equation_str:
                parts = equation_str.split('=')
                if len(parts) != 2:
                    return f"Error in equation '{equation_str}': Should have exactly one '=' sign."

                left_expr = parts[0].strip()
                right_expr = parts[1].strip()

                # If right side is empty, treat as "= 0"
                if not right_expr:
                    right_expr = "0"

                # Parse both sides
                left_side = tokenize_expression(left_expr)
                right_side = tokenize_expression(right_expr)

                # Add constraint to solver
                s.add(left_side == right_side)
            else:
                return f"Error: Equation '{equation_str}' is missing an '=' sign."

        # Solve the system
        if s.check() == sat:
            model = s.model()
            return {str(var): str(model[var_dict[var]]) for var in var_dict}
        else:
            return "No solution found for the system of equations."

    except Exception as e:
        return f"Error solving system: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    query = data.get('query', '').strip()

    # Check if we're dealing with arithmetic
    if not re.search(r'[a-zA-Z]', query) and '=' not in query:
        try:
            result = eval(query)
            return jsonify({"response": f"Result: {result}"})
        except:
            pass  # If eval fails, continue with normal equation solving

    # Check if this is a system of equations
    if ';' in query or '\n' in query:
        equations = [eq.strip() for eq in re.split(r'[;\n]', query) if eq.strip()]
        result = solve_system_of_equations(equations)
    else:
        result = parse_equation(query)

    if isinstance(result, dict):
        response = "Solution:\n"
        for var, val in result.items():
            response += f"{var} = {val}\n"
    elif isinstance(result, list):
        response = "Solutions:\n" + "\n".join(result)
    else:
        response = result

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)