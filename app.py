"""
Flask Web Application for Python Interpreter
Provides a web interface for the interpreter with API endpoints.
"""

from flask import Flask, render_template, request, jsonify
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from ast_nodes import *

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    """
    Execute code and return output, symbol table, and execution timeline.
    """
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code.strip():
            return jsonify({
                'success': False,
                'error': 'No code provided'
            })
        
        # Capture output
        output_lines = []
        timeline = []
        
        # Create custom interpreter with output capture
        class WebInterpreter(Interpreter):
            def __init__(self):
                super().__init__()
                self.output_lines = []
                self.timeline = []
            
            def visit_PrintNode(self, node):
                """Override print to capture output."""
                value = self.visit(node.expr)
                output_str = str(value)
                self.output_lines.append(output_str)
                
                # Add to timeline
                self.timeline.append({
                    'type': 'print',
                    'value': output_str,
                    'symbol_table': dict(self.symbol_table)
                })
                
                return value
            
            def visit_AssignNode(self, node):
                """Override assignment to track in timeline."""
                result = super().visit_AssignNode(node)
                
                # Add to timeline
                self.timeline.append({
                    'type': 'assignment',
                    'variable': node.var,
                    'value': self.symbol_table[node.var],
                    'symbol_table': dict(self.symbol_table)
                })
                
                return result
        
        # Lexical analysis
        lexer = Lexer(code)
        
        # Parsing
        parser = Parser(lexer)
        ast = parser.parse()
        
        # Interpretation
        interpreter = WebInterpreter()
        interpreter.interpret(ast)
        
        return jsonify({
            'success': True,
            'output': interpreter.output_lines,
            'symbol_table': interpreter.symbol_table,
            'timeline': interpreter.timeline
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/tokenize', methods=['POST'])
def tokenize():
    """
    Tokenize code and return the token stream.
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
        tokens = []
        
        while True:
            token = lexer.get_next_token()
            tokens.append({
                'type': token.type.name,
                'value': str(token.value) if token.value is not None else '',
                'line': token.line,
                'column': token.column
            })
            
            if token.type.name == 'EOF':
                break
        
        return jsonify({
            'success': True,
            'tokens': tokens
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/parse', methods=['POST'])
def parse():
    """
    Parse code and return the AST structure.
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
        
        # Convert AST to JSON-serializable format
        def ast_to_dict(node):
            """Convert AST node to dictionary."""
            if isinstance(node, NumberNode):
                return {
                    'type': 'Number',
                    'value': node.value
                }
            elif isinstance(node, VarNode):
                return {
                    'type': 'Variable',
                    'name': node.name
                }
            elif isinstance(node, BinOpNode):
                return {
                    'type': 'BinaryOperation',
                    'operator': node.op,
                    'left': ast_to_dict(node.left),
                    'right': ast_to_dict(node.right)
                }
            elif isinstance(node, AssignNode):
                return {
                    'type': 'Assignment',
                    'variable': node.var,
                    'expression': ast_to_dict(node.expr)
                }
            elif isinstance(node, PrintNode):
                return {
                    'type': 'Print',
                    'expression': ast_to_dict(node.expr)
                }
            elif isinstance(node, ProgramNode):
                return {
                    'type': 'Program',
                    'statements': [ast_to_dict(stmt) for stmt in node.statements]
                }
            else:
                return {
                    'type': 'Unknown',
                    'value': str(node)
                }
        
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

@app.route('/examples', methods=['GET'])
def get_examples():
    """
    Get list of example programs.
    """
    try:
        examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
        examples = []
        
        if os.path.exists(examples_dir):
            for filename in sorted(os.listdir(examples_dir)):
                if filename.endswith('.txt'):
                    filepath = os.path.join(examples_dir, filename)
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    examples.append({
                        'name': filename.replace('.txt', '').replace('_', ' ').title(),
                        'filename': filename,
                        'code': content
                    })
        
        return jsonify({
            'success': True,
            'examples': examples
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
