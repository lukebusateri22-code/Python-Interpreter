"""
Web Frontend for Python Interpreter
Flask-based web application with interactive code editor
"""

from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import io
import sys

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/execute', methods=['POST'])
def execute_code():
    """
    Execute code and return results.
    
    Expects JSON with 'code' field.
    Returns JSON with 'output', 'error', 'symbol_table' fields.
    """
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({
                'success': False,
                'error': 'No code provided'
            })
        
        # Capture print output
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        try:
            # Lexical analysis
            lexer = Lexer(code)
            
            # Parsing
            parser = Parser(lexer)
            ast = parser.parse()
            
            # Interpretation with timeline tracking
            interpreter = Interpreter()
            timeline = []
            
            # Track execution steps
            if hasattr(ast, 'statements'):
                for i, stmt in enumerate(ast.statements):
                    step_vars_before = interpreter.get_symbol_table().copy()
                    
                    # Execute statement
                    interpreter.visit(stmt)
                    
                    step_vars_after = interpreter.get_symbol_table().copy()
                    
                    # Create timeline entry
                    timeline_entry = {
                        'action': f'Execute {stmt.__class__.__name__}',
                        'description': get_statement_description(stmt),
                        'variables': step_vars_after,
                        'changes': get_variable_changes(step_vars_before, step_vars_after)
                    }
                    timeline.append(timeline_entry)
            else:
                interpreter.interpret(ast)
            
            # Get output and symbol table
            output = output_buffer.getvalue()
            symbol_table = interpreter.get_symbol_table()
            
            # Restore stdout
            sys.stdout = sys.__stdout__
            
            return jsonify({
                'success': True,
                'output': output,
                'symbol_table': symbol_table,
                'timeline': timeline,
                'error': None
            })
            
        except Exception as e:
            # Restore stdout
            sys.stdout = sys.__stdout__
            
            return jsonify({
                'success': False,
                'output': output_buffer.getvalue(),
                'error': str(e),
                'symbol_table': {}
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })


@app.route('/tokenize', methods=['POST'])
def tokenize_code():
    """
    Tokenize code and return tokens.
    
    Expects JSON with 'code' field.
    Returns JSON with 'tokens' field.
    """
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({
                'success': False,
                'error': 'No code provided'
            })
        
        # Tokenize
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Convert tokens to serializable format
        token_list = []
        for token in tokens:
            token_list.append({
                'type': token.type.name,
                'value': token.value,
                'line': token.line,
                'column': token.column
            })
        
        return jsonify({
            'success': True,
            'tokens': token_list
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/parse', methods=['POST'])
def parse_code():
    """
    Parse code and return AST.
    
    Expects JSON with 'code' field.
    Returns JSON with 'ast' field.
    """
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({
                'success': False,
                'error': 'No code provided'
            })
        
        # Lexical analysis
        lexer = Lexer(code)
        
        # Parsing
        parser = Parser(lexer)
        ast = parser.parse()
        
        # Convert AST to serializable format
        ast_dict = ast_to_dict(ast)
        
        return jsonify({
            'success': True,
            'ast': ast_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


def ast_to_dict(node):
    """Convert AST node to dictionary for JSON serialization."""
    if node is None:
        return None
    
    result = {
        'type': node.__class__.__name__
    }
    
    # Add node-specific attributes
    if hasattr(node, '__dict__'):
        for key, value in node.__dict__.items():
            if key.startswith('_'):
                continue
            
            if isinstance(value, list):
                result[key] = [ast_to_dict(item) if hasattr(item, '__class__') else item for item in value]
            elif hasattr(value, '__class__') and hasattr(value, '__dict__'):
                result[key] = ast_to_dict(value)
            else:
                result[key] = value
    
    return result


def get_statement_description(stmt):
    """Generate a human-readable description of a statement."""
    stmt_type = stmt.__class__.__name__
    
    if stmt_type == 'VariableDeclaration':
        return f"Declare variable '{stmt.name}' = {get_expression_string(stmt.value)}"
    elif stmt_type == 'PrintStatement':
        return f"Print {get_expression_string(stmt.expression)}"
    elif stmt_type == 'Assignment':
        return f"Assign '{stmt.name}' = {get_expression_string(stmt.value)}"
    else:
        return f"Execute {stmt_type}"


def get_expression_string(expr):
    """Convert an expression to a string representation."""
    if expr is None:
        return 'None'
    
    expr_type = expr.__class__.__name__
    
    if expr_type == 'Number':
        return str(expr.value)
    elif expr_type == 'Identifier':
        return expr.name
    elif expr_type == 'BinaryOp':
        left = get_expression_string(expr.left)
        right = get_expression_string(expr.right)
        return f"({left} {expr.op} {right})"
    else:
        return str(expr)


def get_variable_changes(before, after):
    """Identify which variables changed between two states."""
    changes = []
    
    # Check for new or modified variables
    for name, value in after.items():
        if name not in before:
            changes.append(f"{name} = {value} (new)")
        elif before[name] != value:
            changes.append(f"{name}: {before[name]} → {value}")
    
    return changes


@app.route('/examples', methods=['GET'])
def get_examples():
    """Return example programs."""
    examples = [
        {
            'name': 'Basic Arithmetic',
            'code': '''// Basic arithmetic operations
let x = 10 + 5;
let y = x * 2;
print(x);
print(y);'''
        },
        {
            'name': 'Complex Expressions',
            'code': '''// Complex expressions with parentheses
let a = 5;
let b = 10;
let c = (a + b) * 2;
let d = c / 3;
print(a);
print(b);
print(c);
print(d);'''
        },
        {
            'name': 'Operator Precedence',
            'code': '''// Demonstrating operator precedence
let result1 = 2 + 3 * 4;
print(result1);  // 14, not 20

let result2 = (2 + 3) * 4;
print(result2);  // 20'''
        },
        {
            'name': 'Variable References',
            'code': '''// Using variables in expressions
let num1 = 100;
let num2 = 50;
let sum = num1 + num2;
let diff = num1 - num2;
let product = num1 * num2;
let quotient = num1 / num2;

print(sum);
print(diff);
print(product);
print(quotient);'''
        },
        {
            'name': 'Nested Expressions',
            'code': '''// Nested expressions
let x = 10;
let y = 20;
let z = 30;
let result = (x + y) * z - (x * y) / z;
print(result);'''
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Python Interpreter Web Interface")
    print("=" * 60)
    print("\nStarting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, port=5000)
