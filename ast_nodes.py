"""
Abstract Syntax Tree (AST) Node Definitions

This module defines the node classes used to represent the structure
of the parsed program. Each node type represents a different construct
in the language (expressions, statements, etc.).
"""

class ASTNode:
    """Base class for all AST nodes."""
    pass


class NumberNode(ASTNode):
    """
    Represents a numeric literal.
    
    Attributes:
        value (int/float): The numeric value
    """
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"NumberNode({self.value})"


class VarNode(ASTNode):
    """
    Represents a variable reference.
    
    Attributes:
        name (str): The variable name
    """
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"VarNode({self.name})"


class BinOpNode(ASTNode):
    """
    Represents a binary operation (e.g., addition, multiplication).
    
    Attributes:
        left (ASTNode): The left operand
        op (str): The operator (+, -, *, /)
        right (ASTNode): The right operand
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"


class AssignNode(ASTNode):
    """
    Represents a variable assignment statement.
    
    Attributes:
        var (str): The variable name being assigned to
        expr (ASTNode): The expression being assigned
    """
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    
    def __repr__(self):
        return f"AssignNode(var={self.var}, expr={self.expr})"


class PrintNode(ASTNode):
    """
    Represents a print statement.
    
    Attributes:
        expr (ASTNode): The expression to print
    """
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return f"PrintNode(expr={self.expr})"


class ProgramNode(ASTNode):
    """
    Represents the entire program (a list of statements).
    
    Attributes:
        statements (list): List of statement nodes
    """
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"ProgramNode({self.statements})"
