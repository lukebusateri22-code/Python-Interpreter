"""
Lexical Analyzer (Lexer)

This module implements the lexer, which converts the input source code
into a sequence of tokens. Tokens are the basic building blocks that
the parser will use to construct the AST.
"""

import re
from enum import Enum, auto


class TokenType(Enum):
    """Enumeration of all token types in the language."""
    # Literals and identifiers
    NUMBER = auto()
    ID = auto()
    
    # Keywords
    LET = auto()
    PRINT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    ASSIGN = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    SEMI = auto()
    
    # Special
    EOF = auto()


class Token:
    """
    Represents a single token.
    
    Attributes:
        type (TokenType): The type of the token
        value: The value of the token (for numbers and identifiers)
        line (int): Line number where the token appears
        column (int): Column number where the token appears
    """
    def __init__(self, type_, value=None, line=1, column=1):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


class Lexer:
    """
    Lexical analyzer that converts source code into tokens.
    
    Attributes:
        text (str): The source code to tokenize
        pos (int): Current position in the text
        current_char (str): Current character being examined
        line (int): Current line number
        column (int): Current column number
    """
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
        self.line = 1
        self.column = 1
    
    def error(self, msg="Invalid character"):
        """Raise a lexer error with position information."""
        raise Exception(f"Lexer error at line {self.line}, column {self.column}: {msg}")
    
    def advance(self):
        """Move to the next character in the input."""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset=1):
        """Look ahead at the next character without consuming it."""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments (starting with //)."""
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            if self.current_char == '\n':
                self.advance()
    
    def number(self):
        """Parse a number (integer or float)."""
        result = ''
        start_column = self.column
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        # Convert to int or float
        if '.' in result:
            return Token(TokenType.NUMBER, float(result), self.line, start_column)
        else:
            return Token(TokenType.NUMBER, int(result), self.line, start_column)
    
    def identifier(self):
        """Parse an identifier or keyword."""
        result = ''
        start_column = self.column
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if it's a keyword
        keywords = {
            'let': TokenType.LET,
            'print': TokenType.PRINT,
        }
        
        token_type = keywords.get(result, TokenType.ID)
        return Token(token_type, result, self.line, start_column)
    
    def get_next_token(self):
        """
        Lexical analyzer (tokenizer).
        
        Returns the next token from the input.
        """
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            # Numbers
            if self.current_char.isdigit():
                return self.number()
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # Operators and delimiters
            if self.current_char == '+':
                token = Token(TokenType.PLUS, '+', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '-':
                token = Token(TokenType.MINUS, '-', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '*':
                token = Token(TokenType.MUL, '*', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '/':
                token = Token(TokenType.DIV, '/', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '=':
                token = Token(TokenType.ASSIGN, '=', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == '(':
                token = Token(TokenType.LPAREN, '(', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ')':
                token = Token(TokenType.RPAREN, ')', self.line, self.column)
                self.advance()
                return token
            
            if self.current_char == ';':
                token = Token(TokenType.SEMI, ';', self.line, self.column)
                self.advance()
                return token
            
            # Unknown character
            self.error(f"Invalid character '{self.current_char}'")
        
        # End of file
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self):
        """
        Tokenize the entire input and return a list of tokens.
        
        Returns:
            list: List of Token objects
        """
        tokens = []
        token = self.get_next_token()
        
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        
        tokens.append(token)  # Add EOF token
        return tokens


def main():
    """Test the lexer with sample input."""
    test_input = """
    let x = 10 + 5;
    let y = x * 2;
    print(x);
    print(y);
    """
    
    print("Input:")
    print(test_input)
    print("\nTokens:")
    
    lexer = Lexer(test_input)
    tokens = lexer.tokenize()
    
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
