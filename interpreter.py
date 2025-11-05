"""
Interpreter

This module implements the interpreter, which traverses the AST and
executes the program. It maintains a symbol table for variable storage
and performs arithmetic operations and print statements.
"""

from ast_nodes import (
    NumberNode, VarNode, BinOpNode, AssignNode,
    PrintNode, ProgramNode
)


class Interpreter:
    """
    Interpreter that executes the AST.
    
    The interpreter uses the Visitor pattern to traverse the AST.
    Each node type has a corresponding visit method.
    
    Attributes:
        symbol_table (dict): Stores variable names and their values
    """
    
    def __init__(self):
        self.symbol_table = {}
    
    def error(self, msg):
        """Raise an interpreter error."""
        raise Exception(f"Runtime error: {msg}")
    
    def visit(self, node):
        """
        Dispatch method that calls the appropriate visit method
        based on the node type.
        
        Args:
            node (ASTNode): The node to visit
        
        Returns:
            The result of visiting the node
        """
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Called if no explicit visitor method exists for a node."""
        self.error(f"No visit method for {type(node).__name__}")
    
    def visit_NumberNode(self, node):
        """
        Visit a NumberNode and return its value.
        
        Args:
            node (NumberNode): The number node
        
        Returns:
            int/float: The numeric value
        """
        return node.value
    
    def visit_VarNode(self, node):
        """
        Visit a VarNode and return the variable's value from the symbol table.
        
        Args:
            node (VarNode): The variable node
        
        Returns:
            The value of the variable
        
        Raises:
            Exception: If the variable is not defined
        """
        var_name = node.name
        
        if var_name not in self.symbol_table:
            self.error(f"Variable '{var_name}' is not defined")
        
        return self.symbol_table[var_name]
    
    def visit_BinOpNode(self, node):
        """
        Visit a BinOpNode and perform the binary operation.
        
        Args:
            node (BinOpNode): The binary operation node
        
        Returns:
            int/float: The result of the operation
        """
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        
        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            if right_val == 0:
                self.error("Division by zero")
            return left_val / right_val
        else:
            self.error(f"Unknown operator: {node.op}")
    
    def visit_AssignNode(self, node):
        """
        Visit an AssignNode and store the variable in the symbol table.
        
        Args:
            node (AssignNode): The assignment node
        """
        var_name = node.var
        value = self.visit(node.expr)
        
        self.symbol_table[var_name] = value
    
    def visit_PrintNode(self, node):
        """
        Visit a PrintNode and print the expression's value.
        
        Args:
            node (PrintNode): The print node
        """
        value = self.visit(node.expr)
        print(value)
    
    def visit_ProgramNode(self, node):
        """
        Visit a ProgramNode and execute all statements.
        
        Args:
            node (ProgramNode): The program node
        """
        for statement in node.statements:
            self.visit(statement)
    
    def interpret(self, ast):
        """
        Interpret the AST.
        
        Args:
            ast (ProgramNode): The root of the AST
        """
        self.visit(ast)
    
    def get_symbol_table(self):
        """
        Get the current symbol table.
        
        Returns:
            dict: The symbol table
        """
        return self.symbol_table.copy()


def main():
    """Test the interpreter with sample input."""
    from lexer import Lexer
    from parser import Parser
    
    test_input = """
    let x = 10 + 5;
    let y = x * 2;
    print(x);
    print(y);
    let z = (x + y) / 5;
    print(z);
    """
    
    print("Input:")
    print(test_input)
    print("\nOutput:")
    
    # Tokenize
    lexer = Lexer(test_input)
    
    # Parse
    parser = Parser(lexer)
    ast = parser.parse()
    
    # Interpret
    interpreter = Interpreter()
    interpreter.interpret(ast)
    
    print("\nSymbol Table:")
    for var, value in interpreter.get_symbol_table().items():
        print(f"  {var} = {value}")


if __name__ == "__main__":
    main()
