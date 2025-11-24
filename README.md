# Python Interpreter - CS 390 Final Project

A fully functioning interpreter built in Python with a modern web interface. This interpreter supports variable assignments, arithmetic operations, and print statements through a three-stage architecture: lexical analysis, parsing, and interpretation.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](LICENSE)
[![Web Interface](https://img.shields.io/badge/web-interface-FF6B6B.svg)](http://localhost:5000)

## ✨ Features

- **Modern Web Interface**: Beautiful, tech-themed frontend with gradients and animations
- **Interactive Code Editor**: Syntax highlighting, line numbers, and real-time execution
- **Variable Inspector**: Live symbol table visualization
- **Token Viewer**: See the lexical analysis process
- **Variable Assignments**: Define and use variables with the `let` keyword
- **Arithmetic Operations**: Support for `+`, `-`, `*`, `/` operators
- **Operator Precedence**: Correct handling of mathematical precedence
- **Parentheses**: Support for grouping expressions
- **Print Statements**: Display variable values and expression results
- **Error Handling**: Clear error messages with line and column information
- **Comments**: Single-line comments using `//`
- **REPL Mode**: Interactive mode for testing statements
- **File Execution**: Run programs from source files

## 🚀 Quick Start

### Web Interface (Recommended)

```bash
# Clone the repository
git clone https://github.com/lukebusateri22-code/Python-Interpreter.git
cd Python-Interpreter

# Install Flask
pip3 install flask

# Start the web server
python3 web_app.py

# Open your browser and go to: http://localhost:5000
```

### Command Line Interface

```bash
# Run an example program
python3 main.py examples/example1.txt

# Or start the interactive REPL
python3 main.py

# Run tests
python3 test_interpreter.py
```

**Requirements:** Python 3.6 or higher (Flask required for web interface)

## 📁 Project Structure

```
Python-Interpreter/
├── ast_nodes.py          # AST node class definitions
├── lexer.py              # Lexical analyzer (tokenizer)
├── parser.py             # Parser (builds AST from tokens)
├── interpreter.py        # Interpreter (executes AST)
├── main.py               # Main entry point
├── test_interpreter.py   # Unit tests
├── examples/             # Example programs
│   ├── example1.txt
│   ├── example2.txt
│   └── example3.txt
├── PROJECT_REPORT.md     # Detailed project report
└── README.md             # This file
```

## 💻 Usage

### Running a Program File

```bash
python main.py examples/example1.txt
```

### Interactive REPL Mode

```bash
python main.py
```

In REPL mode, you can:
- Enter statements interactively
- Type `vars` to see all defined variables
- Type `exit` or `quit` to exit

### Running Tests

```bash
python test_interpreter.py
```

### Testing Individual Components

Each module can be run independently for testing:

```bash
# Test the lexer
python lexer.py

# Test the parser
python parser.py

# Test the interpreter
python interpreter.py
```

## 📝 Language Syntax

### Variable Assignment

```
let variable_name = expression;
```

Example:
```
let x = 10;
let y = x + 5;
```

### Arithmetic Operations

Supported operators:
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division

Example:
```
let result = (10 + 5) * 2 - 8 / 4;
```

### Print Statement

```
print(expression);
```

Example:
```
print(x);
print(10 + 20);
```

### Comments

```
// This is a single-line comment
let x = 5; // Comments can also be at the end of lines
```

### Complete Example

```
// Calculate area and perimeter of a rectangle
let width = 10;
let height = 5;

let area = width * height;
let perimeter = (width + height) * 2;

print(area);       // Output: 50
print(perimeter);  // Output: 30
```

## 🏗️ Architecture

The interpreter follows a classic three-stage architecture:

### 1. Lexical Analysis (Lexer)

**File:** `lexer.py`

The lexer converts the source code into a stream of tokens. Each token represents a meaningful unit like a number, identifier, operator, or keyword.

**Key Components:**
- `TokenType`: Enumeration of all token types
- `Token`: Represents a single token with type, value, and position
- `Lexer`: Tokenizes the input string

**Example:**
```
Input:  "let x = 10 + 5;"
Tokens: [LET, ID(x), ASSIGN, NUMBER(10), PLUS, NUMBER(5), SEMI, EOF]
```

### 2. Parsing (Parser)

**File:** `parser.py`

The parser takes the token stream and constructs an Abstract Syntax Tree (AST) that represents the hierarchical structure of the program.

**Grammar:**
```
program     : statement*
statement   : assignment | print_stmt
assignment  : LET ID ASSIGN expr SEMI
print_stmt  : PRINT LPAREN expr RPAREN SEMI
expr        : term ((PLUS | MINUS) term)*
term        : factor ((MUL | DIV) factor)*
factor      : NUMBER | ID | LPAREN expr RPAREN
```

**Key Components:**
- Recursive descent parser
- Handles operator precedence
- Builds AST nodes defined in `ast_nodes.py`

**Example AST for "let x = 10 + 5;":**
```
ProgramNode
└── AssignNode(var='x')
    └── BinOpNode(op='+')
        ├── NumberNode(10)
        └── NumberNode(5)
```

### 3. Interpretation (Interpreter)

**File:** `interpreter.py`

The interpreter traverses the AST and executes the program using the Visitor pattern. It maintains a symbol table to store variable values.

**Key Components:**
- `Interpreter`: Executes the AST
- `symbol_table`: Dictionary storing variable names and values
- Visitor methods for each AST node type

**Execution Flow:**
1. Visit each statement in the program
2. For assignments: evaluate expression and store in symbol table
3. For print statements: evaluate expression and output result
4. For expressions: recursively evaluate operands and apply operators

## 📚 Examples

### Example 1: Basic Arithmetic

**File:** `examples/example1.txt`

```
let x = 10 + 5;
let y = x * 2;
print(x);
print(y);
```

**Output:**
```
15
30
```

### Example 2: Complex Expressions

**File:** `examples/example2.txt`

```
let a = 5;
let b = 10;
let c = (a + b) * 2;
let d = c / 3;
print(a);
print(b);
print(c);
print(d);
```

**Output:**
```
5
10
30
10.0
```

### Example 3: Chained Operations

**File:** `examples/example3.txt`

```
let num1 = 100;
let num2 = 50;
let sum = num1 + num2;
let diff = num1 - num2;
let product = num1 * num2;
let quotient = num1 / num2;

print(sum);
print(diff);
print(product);
print(quotient);

let result = sum + diff - product / quotient;
print(result);
```

**Output:**
```
150
50
5000
2.0
-4800.0
```

## 🧪 Testing

The project includes comprehensive unit tests in `test_interpreter.py`.

**Test Categories:**

1. **Lexer Tests**
   - Token generation
   - Comment handling
   - Number and identifier recognition

2. **Parser Tests**
   - AST construction
   - Operator precedence
   - Parentheses handling

3. **Interpreter Tests**
   - Arithmetic operations
   - Variable storage and retrieval
   - Error handling (undefined variables, division by zero)

4. **End-to-End Tests**
   - Complete program execution

**Run all tests:**
```bash
python test_interpreter.py
```

**Expected Output:**
```
test_division_by_zero_error (__main__.TestInterpreter) ... ok
test_interpret_addition (__main__.TestInterpreter) ... ok
test_interpret_complex_expression (__main__.TestInterpreter) ... ok
...
----------------------------------------------------------------------
Ran XX tests in X.XXXs

OK
```

## 🔍 Implementation Details

### Abstract Syntax Tree (AST)

The AST is a tree representation of the source code structure. Each node represents a construct in the language:

**Node Types:**

1. **NumberNode**: Represents numeric literals
   ```python
   NumberNode(value=42)
   ```

2. **VarNode**: Represents variable references
   ```python
   VarNode(name='x')
   ```

3. **BinOpNode**: Represents binary operations
   ```python
   BinOpNode(left=NumberNode(10), op='+', right=NumberNode(5))
   ```

4. **AssignNode**: Represents variable assignments
   ```python
   AssignNode(var='x', expr=NumberNode(42))
   ```

5. **PrintNode**: Represents print statements
   ```python
   PrintNode(expr=VarNode('x'))
   ```

6. **ProgramNode**: Represents the entire program
   ```python
   ProgramNode(statements=[...])
   ```

### Operator Precedence

The parser implements correct operator precedence through its grammar structure:

1. **Highest Precedence**: Parentheses `()`
2. **High Precedence**: Multiplication `*`, Division `/`
3. **Low Precedence**: Addition `+`, Subtraction `-`

This is achieved by having separate parsing methods:
- `factor()`: Handles numbers, variables, and parentheses
- `term()`: Handles multiplication and division
- `expr()`: Handles addition and subtraction

### Error Handling

The interpreter provides detailed error messages:

**Lexer Errors:**
```
Lexer error at line 1, column 5: Invalid character '@'
```

**Parser Errors:**
```
Parser error at line 2, column 10: Expected SEMI, got PLUS
```

**Runtime Errors:**
```
Runtime error: Variable 'y' is not defined
Runtime error: Division by zero
```

### Symbol Table

The interpreter uses a dictionary to store variables:

```python
symbol_table = {
    'x': 15,
    'y': 30,
    'result': 45
}
```

Variables must be defined before use, otherwise a runtime error is raised.

## 🎯 Key Design Decisions

1. **Visitor Pattern**: Used in the interpreter for clean separation of AST traversal and execution logic

2. **Recursive Descent Parsing**: Simple and intuitive parsing technique that directly mirrors the grammar

3. **Token Position Tracking**: Line and column numbers for better error messages

4. **Modular Design**: Each component (lexer, parser, interpreter) is independent and testable

5. **Extensibility**: Easy to add new operators, statements, or data types by:
   - Adding new token types in `lexer.py`
   - Adding new AST nodes in `ast_nodes.py`
   - Adding new parsing rules in `parser.py`
   - Adding new visitor methods in `interpreter.py`

## 📚 Documentation

For a detailed explanation of the project, including:
- Architecture and design decisions
- Implementation details
- Challenges and solutions
- Group contributions

Please see [PROJECT_REPORT.md](PROJECT_REPORT.md)

## 🚀 Future Enhancements

Possible extensions to the interpreter:

- [ ] Boolean operations and comparisons (`==`, `!=`, `<`, `>`, `and`, `or`)
- [ ] Conditional statements (`if`, `else`)
- [ ] Loop constructs (`while`, `for`)
- [ ] Functions and function calls
- [ ] String data type and operations
- [ ] Lists/arrays

## 📄 License

This project is created for educational purposes as part of CS 390 coursework.

## 👥 Contributors

[Add your group members and their contributions here]

Example:
- **Student 1**: Lexer implementation
- **Student 2**: Parser implementation
- **Student 3**: Interpreter implementation

---

**CS 390 Final Project - Fall 2025**
