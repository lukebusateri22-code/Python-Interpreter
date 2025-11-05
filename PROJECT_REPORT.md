# CS 390 Final Project Report
## Building a Python Interpreter

**Course:** CS 390  
**Project:** Python Interpreter  
**Date:** November 2025

---

## 1. Executive Summary

This project implements a fully functional interpreter for a simple programming language using Python. The interpreter successfully handles variable assignments, arithmetic operations, and print statements through a three-stage architecture: lexical analysis, parsing, and interpretation. The implementation demonstrates core compiler design principles including tokenization, Abstract Syntax Tree (AST) construction, and tree-based program execution.

---

## 2. Project Structure and Architecture

### 2.1 Overview

The interpreter follows a classic three-stage pipeline architecture:

```
Source Code → Lexer → Tokens → Parser → AST → Interpreter → Execution
```

### 2.2 Core Components

#### **Lexer (lexer.py)**
The lexical analyzer converts raw source code into a stream of tokens. It implements:
- **Token Recognition**: Identifies numbers, identifiers, keywords (`let`, `print`), and operators
- **Position Tracking**: Maintains line and column numbers for error reporting
- **Comment Handling**: Skips single-line comments (`//`)
- **Whitespace Management**: Properly handles all whitespace characters

**Key Classes:**
- `TokenType`: Enumeration of all token types (NUMBER, ID, LET, PRINT, PLUS, MINUS, etc.)
- `Token`: Represents individual tokens with type, value, and position information
- `Lexer`: Main tokenization engine

**Example:**
```
Input:  "let x = 10 + 5;"
Output: [LET, ID(x), ASSIGN, NUMBER(10), PLUS, NUMBER(5), SEMI, EOF]
```

#### **Parser (parser.py)**
The parser constructs an Abstract Syntax Tree from the token stream using recursive descent parsing. It implements:
- **Grammar Rules**: Defines the language syntax structure
- **Operator Precedence**: Correctly handles mathematical precedence (multiplication/division before addition/subtraction)
- **Error Detection**: Provides detailed syntax error messages
- **AST Construction**: Builds a hierarchical tree representation of the program

**Grammar Definition:**
```
program     : statement*
statement   : assignment | print_stmt
assignment  : LET ID ASSIGN expr SEMI
print_stmt  : PRINT LPAREN expr RPAREN SEMI
expr        : term ((PLUS | MINUS) term)*
term        : factor ((MUL | DIV) factor)*
factor      : NUMBER | ID | LPAREN expr RPAREN
```

**Example AST for "let x = 10 + 5;":**
```
ProgramNode
└── AssignNode(var='x')
    └── BinOpNode(op='+')
        ├── NumberNode(10)
        └── NumberNode(5)
```

#### **AST Nodes (ast_nodes.py)**
Defines the node classes that represent program constructs:
- `NumberNode`: Numeric literals (integers and floats)
- `VarNode`: Variable references
- `BinOpNode`: Binary operations (+, -, *, /)
- `AssignNode`: Variable assignment statements
- `PrintNode`: Print statements
- `ProgramNode`: Root node containing all statements

#### **Interpreter (interpreter.py)**
Executes the program by traversing the AST using the Visitor pattern:
- **Symbol Table**: Dictionary storing variable names and values
- **Expression Evaluation**: Recursively evaluates arithmetic expressions
- **Error Handling**: Detects undefined variables and division by zero
- **Visitor Pattern**: Clean separation of AST traversal and execution logic

**Execution Flow:**
1. Visit each statement in the program sequentially
2. For assignments: evaluate the expression and store in symbol table
3. For print statements: evaluate the expression and output the result
4. For expressions: recursively evaluate operands and apply operators

#### **Main Entry Point (main.py)**
Provides two execution modes:
- **File Mode**: Execute programs from source files
- **REPL Mode**: Interactive Read-Eval-Print Loop for testing

---

## 3. Key Design Decisions

### 3.1 Recursive Descent Parsing
We chose recursive descent parsing for its simplicity and direct correspondence to the grammar rules. Each grammar rule has a corresponding method in the parser, making the code intuitive and maintainable.

### 3.2 Visitor Pattern for Interpretation
The interpreter uses the Visitor pattern to separate AST traversal logic from execution logic. This design allows for:
- Easy addition of new node types
- Clean, modular code structure
- Potential for multiple "visitors" (e.g., type checker, optimizer)

### 3.3 Token Position Tracking
Every token stores its line and column position, enabling precise error messages that help users quickly locate and fix issues.

### 3.4 Modular Architecture
Each component (lexer, parser, interpreter) is independent and can be tested separately. This modularity simplifies debugging and future enhancements.

---

## 4. Features Implemented

### 4.1 Required Features
✅ **Variable Assignments**: `let variable = expression;`  
✅ **Arithmetic Operations**: Addition (+), Subtraction (-), Multiplication (*), Division (/)  
✅ **Print Statements**: `print(expression);`  
✅ **Multiple Statements**: Sequential execution of statements  
✅ **Operator Precedence**: Correct mathematical precedence  
✅ **Parentheses**: Expression grouping with parentheses  

### 4.2 Additional Features
✅ **Comments**: Single-line comments using `//`  
✅ **REPL Mode**: Interactive testing environment  
✅ **Error Handling**: Detailed error messages with position information  
✅ **Float Support**: Both integer and floating-point numbers  
✅ **Comprehensive Testing**: Unit tests for all components  

---

## 5. Testing

### 5.1 Test Suite (test_interpreter.py)
The project includes comprehensive unit tests covering:

**Lexer Tests:**
- Token generation for all language constructs
- Comment handling
- Number and identifier recognition

**Parser Tests:**
- AST construction correctness
- Operator precedence verification
- Parentheses handling

**Interpreter Tests:**
- All arithmetic operations
- Variable storage and retrieval
- Error conditions (undefined variables, division by zero)

**End-to-End Tests:**
- Complete program execution

### 5.2 Example Programs

**Example 1: Basic Arithmetic**
```
let x = 10 + 5;
let y = x * 2;
print(x);  // Output: 15
print(y);  // Output: 30
```

**Example 2: Complex Expressions**
```
let a = 5;
let b = 10;
let c = (a + b) * 2;
let d = c / 3;
print(c);  // Output: 30
print(d);  // Output: 10.0
```

**Example 3: Operator Precedence**
```
let result = 2 + 3 * 4;
print(result);  // Output: 14 (not 20)
```

---

## 6. How to Use

### 6.1 Running a Program File
```bash
python main.py examples/example1.txt
```

### 6.2 Interactive REPL Mode
```bash
python main.py
>>> let x = 10;
>>> let y = x + 5;
>>> print(y);
15
>>> vars
Symbol Table:
  x = 10
  y = 15
>>> exit
```

### 6.3 Running Tests
```bash
python test_interpreter.py
```

---

## 7. Challenges and Solutions

### 7.1 Operator Precedence
**Challenge:** Ensuring multiplication and division are evaluated before addition and subtraction.  
**Solution:** Implemented separate parsing methods (`expr` for +/-, `term` for */`) that naturally enforce precedence through the grammar structure.

### 7.2 Error Reporting
**Challenge:** Providing helpful error messages to users.  
**Solution:** Tracked line and column positions throughout tokenization and parsing, allowing precise error location reporting.

### 7.3 Symbol Table Management
**Challenge:** Handling variable scope and undefined variable errors.  
**Solution:** Implemented a simple dictionary-based symbol table with runtime checks for undefined variables.

---

## 8. Future Enhancements

Possible extensions to the interpreter:
- Boolean operations and comparisons (`==`, `!=`, `<`, `>`, `and`, `or`)
- Conditional statements (`if`, `else`)
- Loop constructs (`while`, `for`)
- Functions and function calls
- String data type and operations
- Lists/arrays
- Input statements

---

## 9. Conclusion

This project successfully implements a fully functional interpreter that meets all assignment requirements. The implementation demonstrates solid understanding of:
- Lexical analysis and tokenization
- Parsing and AST construction
- Tree-based program execution
- Compiler design principles

The modular architecture and comprehensive testing ensure the interpreter is reliable, maintainable, and extensible. The project provides a strong foundation for understanding how programming languages are implemented and can be easily extended with additional features.

---

## 10. Group Contributions

**[Add your group member names and contributions here]**

Example format:
- **Student 1 Name**: Implemented lexer and tokenization logic, wrote lexer tests
- **Student 2 Name**: Implemented parser and AST construction, wrote parser tests
- **Student 3 Name**: Implemented interpreter and visitor pattern, wrote interpreter tests
- **All Members**: Collaborated on design decisions, documentation, and final report

---

## Appendix: Code Statistics

- **Total Lines of Code**: ~800 lines
- **Core Modules**: 5 (lexer, parser, ast_nodes, interpreter, main)
- **Test Cases**: 20+ unit tests
- **Example Programs**: 3 demonstration programs
- **Documentation**: Comprehensive inline comments and docstrings

---

**End of Report**
