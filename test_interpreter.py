"""
Test Suite for the Interpreter

This module contains unit tests for the lexer, parser, and interpreter.
Run with: python test_interpreter.py
"""

import unittest
from lexer import Lexer, TokenType
from parser import Parser
from interpreter import Interpreter
from ast_nodes import NumberNode, VarNode, BinOpNode


class TestLexer(unittest.TestCase):
    """Test cases for the Lexer."""
    
    def test_tokenize_assignment(self):
        """Test tokenizing a simple assignment."""
        lexer = Lexer("let x = 5;")
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.LET,
            TokenType.ID,
            TokenType.ASSIGN,
            TokenType.NUMBER,
            TokenType.SEMI,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_tokenize_arithmetic(self):
        """Test tokenizing arithmetic operations."""
        lexer = Lexer("10 + 5 * 2")
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.NUMBER,
            TokenType.PLUS,
            TokenType.NUMBER,
            TokenType.MUL,
            TokenType.NUMBER,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_tokenize_print(self):
        """Test tokenizing a print statement."""
        lexer = Lexer("print(x);")
        tokens = lexer.tokenize()
        
        expected_types = [
            TokenType.PRINT,
            TokenType.LPAREN,
            TokenType.ID,
            TokenType.RPAREN,
            TokenType.SEMI,
            TokenType.EOF
        ]
        
        actual_types = [token.type for token in tokens]
        self.assertEqual(actual_types, expected_types)
    
    def test_skip_comments(self):
        """Test that comments are skipped."""
        lexer = Lexer("let x = 5; // This is a comment")
        tokens = lexer.tokenize()
        
        # Should not include comment tokens
        for token in tokens:
            self.assertNotIn('//', str(token.value) if token.value else '')


class TestParser(unittest.TestCase):
    """Test cases for the Parser."""
    
    def test_parse_number(self):
        """Test parsing a number."""
        lexer = Lexer("let x = 42;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].var, 'x')
        self.assertIsInstance(ast.statements[0].expr, NumberNode)
        self.assertEqual(ast.statements[0].expr.value, 42)
    
    def test_parse_binary_operation(self):
        """Test parsing a binary operation."""
        lexer = Lexer("let x = 10 + 5;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        self.assertIsInstance(ast.statements[0].expr, BinOpNode)
        self.assertEqual(ast.statements[0].expr.op, '+')
    
    def test_parse_operator_precedence(self):
        """Test that operator precedence is correct."""
        lexer = Lexer("let x = 2 + 3 * 4;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        # Should parse as 2 + (3 * 4), not (2 + 3) * 4
        expr = ast.statements[0].expr
        self.assertIsInstance(expr, BinOpNode)
        self.assertEqual(expr.op, '+')
        self.assertIsInstance(expr.left, NumberNode)
        self.assertIsInstance(expr.right, BinOpNode)
        self.assertEqual(expr.right.op, '*')
    
    def test_parse_parentheses(self):
        """Test parsing parentheses."""
        lexer = Lexer("let x = (2 + 3) * 4;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        # Should parse as (2 + 3) * 4
        expr = ast.statements[0].expr
        self.assertIsInstance(expr, BinOpNode)
        self.assertEqual(expr.op, '*')
        self.assertIsInstance(expr.left, BinOpNode)
        self.assertEqual(expr.left.op, '+')


class TestInterpreter(unittest.TestCase):
    """Test cases for the Interpreter."""
    
    def test_interpret_number(self):
        """Test interpreting a number."""
        lexer = Lexer("let x = 42;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 42)
    
    def test_interpret_addition(self):
        """Test interpreting addition."""
        lexer = Lexer("let x = 10 + 5;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 15)
    
    def test_interpret_subtraction(self):
        """Test interpreting subtraction."""
        lexer = Lexer("let x = 10 - 5;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 5)
    
    def test_interpret_multiplication(self):
        """Test interpreting multiplication."""
        lexer = Lexer("let x = 10 * 5;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 50)
    
    def test_interpret_division(self):
        """Test interpreting division."""
        lexer = Lexer("let x = 10 / 5;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 2)
    
    def test_interpret_operator_precedence(self):
        """Test that operator precedence is correct in interpretation."""
        lexer = Lexer("let x = 2 + 3 * 4;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        # Should be 2 + (3 * 4) = 14, not (2 + 3) * 4 = 20
        self.assertEqual(interpreter.symbol_table['x'], 14)
    
    def test_interpret_variable_reference(self):
        """Test interpreting variable references."""
        lexer = Lexer("let x = 10; let y = x + 5;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 10)
        self.assertEqual(interpreter.symbol_table['y'], 15)
    
    def test_interpret_complex_expression(self):
        """Test interpreting a complex expression."""
        lexer = Lexer("let x = (10 + 5) * 2 / 3;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 10.0)
    
    def test_undefined_variable_error(self):
        """Test that using an undefined variable raises an error."""
        lexer = Lexer("let x = y + 5;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        
        with self.assertRaises(Exception) as context:
            interpreter.interpret(ast)
        
        self.assertIn("not defined", str(context.exception))
    
    def test_division_by_zero_error(self):
        """Test that division by zero raises an error."""
        lexer = Lexer("let x = 10 / 0;")
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        
        with self.assertRaises(Exception) as context:
            interpreter.interpret(ast)
        
        self.assertIn("Division by zero", str(context.exception))


class TestEndToEnd(unittest.TestCase):
    """End-to-end test cases."""
    
    def test_example_program(self):
        """Test the example program from the assignment."""
        source = """
        let x = 10 + 5;
        let y = x * 2;
        print(x);
        print(y);
        """
        
        lexer = Lexer(source)
        parser = Parser(lexer)
        ast = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
        self.assertEqual(interpreter.symbol_table['x'], 15)
        self.assertEqual(interpreter.symbol_table['y'], 30)


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
