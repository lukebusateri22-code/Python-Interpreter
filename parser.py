"""
Parser

This module implements the parser, which takes the tokens from the lexer
and constructs an Abstract Syntax Tree (AST). The parser uses recursive
descent parsing to handle operator precedence and grammar rules.

Grammar:
    program     : statement*
    statement   : assignment | print_stmt
    assignment  : LET ID ASSIGN expr SEMI
    print_stmt  : PRINT LPAREN expr RPAREN SEMI
    expr        : term ((PLUS | MINUS) term)*
    term        : factor ((MUL | DIV) factor)*
    factor      : NUMBER | ID | LPAREN expr RPAREN
"""

from lexer import TokenType, Lexer
from ast_nodes import (
    NumberNode, VarNode, BinOpNode, AssignNode, 
    PrintNode, ProgramNode
)


class Parser:
    """
    Parser that constructs an AST from tokens.
    
    Attributes:
        lexer (Lexer): The lexer providing tokens
        current_token (Token): The current token being examined
    """
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, msg="Invalid syntax"):
        """Raise a parser error with token information."""
        raise Exception(
            f"Parser error at line {self.current_token.line}, "
            f"column {self.current_token.column}: {msg}"
        )
    
    def eat(self, token_type):
        """
        Consume the current token if it matches the expected type.
        
        Args:
            token_type (TokenType): Expected token type
        
        Raises:
            Exception: If the current token doesn't match
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(
                f"Expected {token_type}, got {self.current_token.type}"
            )
    
    def factor(self):
        """
        Parse a factor (number, variable, or parenthesized expression).
        
        factor : NUMBER | ID | LPAREN expr RPAREN
        
        Returns:
            ASTNode: NumberNode, VarNode, or expression node
        """
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(token.value)
        
        elif token.type == TokenType.ID:
            self.eat(TokenType.ID)
            return VarNode(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        
        else:
            self.error(f"Unexpected token {token.type}")
    
    def term(self):
        """
        Parse a term (handles multiplication and division).
        
        term : factor ((MUL | DIV) factor)*
        
        Returns:
            ASTNode: BinOpNode or factor node
        """
        node = self.factor()
        
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            
            node = BinOpNode(left=node, op=token.value, right=self.factor())
        
        return node
    
    def expr(self):
        """
        Parse an expression (handles addition and subtraction).
        
        expr : term ((PLUS | MINUS) term)*
        
        Returns:
            ASTNode: BinOpNode or term node
        """
        node = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            
            node = BinOpNode(left=node, op=token.value, right=self.term())
        
        return node
    
    def assignment(self):
        """
        Parse an assignment statement.
        
        assignment : LET ID ASSIGN expr SEMI
        
        Returns:
            AssignNode: Assignment node
        """
        self.eat(TokenType.LET)
        
        var_token = self.current_token
        self.eat(TokenType.ID)
        
        self.eat(TokenType.ASSIGN)
        
        expr_node = self.expr()
        
        self.eat(TokenType.SEMI)
        
        return AssignNode(var=var_token.value, expr=expr_node)
    
    def print_stmt(self):
        """
        Parse a print statement.
        
        print_stmt : PRINT LPAREN expr RPAREN SEMI
        
        Returns:
            PrintNode: Print statement node
        """
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        
        expr_node = self.expr()
        
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMI)
        
        return PrintNode(expr=expr_node)
    
    def statement(self):
        """
        Parse a statement (assignment or print).
        
        statement : assignment | print_stmt
        
        Returns:
            ASTNode: Statement node
        """
        if self.current_token.type == TokenType.LET:
            return self.assignment()
        elif self.current_token.type == TokenType.PRINT:
            return self.print_stmt()
        else:
            self.error(f"Unexpected token {self.current_token.type}")
    
    def program(self):
        """
        Parse the entire program.
        
        program : statement*
        
        Returns:
            ProgramNode: Root node containing all statements
        """
        statements = []
        
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        
        return ProgramNode(statements)
    
    def parse(self):
        """
        Parse the input and return the AST.
        
        Returns:
            ProgramNode: The root of the AST
        """
        return self.program()


def main():
    """Test the parser with sample input."""
    test_input = """
    let x = 10 + 5;
    let y = x * 2;
    print(x);
    print(y);
    """
    
    print("Input:")
    print(test_input)
    print("\nAST:")
    
    lexer = Lexer(test_input)
    parser = Parser(lexer)
    ast = parser.parse()
    
    print(ast)
    print("\nStatements:")
    for stmt in ast.statements:
        print(f"  {stmt}")


if __name__ == "__main__":
    main()
