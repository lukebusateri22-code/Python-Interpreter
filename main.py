"""
Main Entry Point for the Python Interpreter

This module provides the main interface for running the interpreter.
It can execute code from a file or run in interactive (REPL) mode.
"""

import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def run_file(filename):
    """
    Execute a source file.
    
    Args:
        filename (str): Path to the source file
    """
    try:
        with open(filename, 'r') as f:
            source_code = f.read()
        
        print(f"Executing {filename}...")
        print("-" * 50)
        
        run_code(source_code)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def run_code(source_code):
    """
    Execute source code.
    
    Args:
        source_code (str): The source code to execute
    """
    try:
        # Lexical analysis
        lexer = Lexer(source_code)
        
        # Parsing
        parser = Parser(lexer)
        ast = parser.parse()
        
        # Interpretation
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except Exception as e:
        print(f"Error: {e}")
        raise


def repl():
    """
    Run the interpreter in REPL (Read-Eval-Print Loop) mode.
    
    In REPL mode, users can enter statements interactively.
    """
    print("Python Interpreter REPL")
    print("Type 'exit' or 'quit' to exit")
    print("-" * 50)
    
    interpreter = Interpreter()
    
    while True:
        try:
            # Read
            line = input(">>> ")
            
            # Check for exit commands
            if line.strip().lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
            
            # Skip empty lines
            if not line.strip():
                continue
            
            # Special command to show variables
            if line.strip() == 'vars':
                print("Symbol Table:")
                for var, value in interpreter.get_symbol_table().items():
                    print(f"  {var} = {value}")
                continue
            
            # Eval and Print
            lexer = Lexer(line)
            parser = Parser(lexer)
            ast = parser.parse()
            interpreter.interpret(ast)
            
        except EOFError:
            print("\nGoodbye!")
            break
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function."""
    if len(sys.argv) > 1:
        # File mode
        filename = sys.argv[1]
        run_file(filename)
    else:
        # REPL mode
        repl()


if __name__ == "__main__":
    main()
