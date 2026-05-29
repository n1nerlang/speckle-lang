"""
===============================================================================
                       The Speckle Programming Language
===============================================================================
Core Engine Prototype (.spk / .speckle)
Features: Loops, Math Constants, and Turtle Graphics Integration
Written in Python 3

Syntax Architecture:
  - Multi-line Comments: Wrapped inside double-parentheses `(( like this ))`.
  - Functional Invocation: Standard Lua-style identifier expressions.
===============================================================================
"""

import re
import sys
import math
import turtle
from typing import List, NamedTuple, Any, Dict

# =============================================================================
# 1. The Lexer (Tokenizer)
# =============================================================================
# The lexer scans through the source code character by character, turning the
# raw text into "Tokens" while skipping comments and trailing whitespace.

class Token(NamedTuple):
    """An atomic unit of Speckle syntax."""
    type: str     # Category (e.g., 'IDENTIFIER', 'NUMBER', 'LPAREN')
    value: str    # The actual string matched in the text
    line: int     # Line number for tracking down errors
    column: int   # Column number for precise tracking

    def __repr__(self) -> str:
        return f"Token({self.type}, '{self.value}', Line:{self.line}, Col:{self.column})"


class Lexer:
    """Scans raw source text using regular expressions to output clean Speckle tokens."""
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        
        # Priority rules. Multi-line comments are evaluated first.
        rules = [
            ('COMMENT',    r'\(\([\s\S]*?\)\)'), 
            ('NUMBER',     r'-?\d+'),            # Updated regex to handle negative numbers too!
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('LPAREN',     r'\('),
            ('RPAREN',     r'\)'),
            ('COMMA',      r','),
            ('NEWLINE',    r'\n'),
            ('SKIP',       r'[ \t\r]+'),         
            ('MISMATCH',   r'.'),                
        ]
        self.master_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in rules))

    def tokenize(self) -> List[Token]:
        line_num = 1
        line_start = 0
        
        for match in self.master_regex.finditer(self.source_code):
            kind = match.lastgroup
            value = match.group(kind)
            column = match.start() - line_start + 1
            
            if kind == 'NEWLINE':
                line_start = match.end()
                line_num += 1
            elif kind == 'COMMENT':
                line_num += value.count('\n')
                if '\n' in value:
                    line_start = match.start() + value.rfind('\n') + 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"[Lexer Error] Unexpected character '{value}' found at line {line_num}, column {column}")
            else:
                self.tokens.append(Token(kind, value, line_num, column))
                
        self.tokens.append(Token('EOF', '', line_num, len(self.source_code) - line_start + 1))
        return self.tokens


# =============================================================================
# 2. Abstract Syntax Tree (AST) Nodes
# =============================================================================
# Structural blueprints representing the parsed configurations of your syntax.

class ASTNode:
    pass


class NumberNode(ASTNode):
    """Represents an integer literal value."""
    def __init__(self, value: str):
        self.value = int(value)

    def __repr__(self) -> str:
        return f"NumberNode({self.value})"


class CallNode(ASTNode):
    """Represents a function call execution sequence."""
    def __init__(self, callee: str, arguments: List[ASTNode]):
        self.callee = callee          
        self.arguments = arguments    

    def __repr__(self) -> str:
        return f"CallNode(callee='{self.callee}', args={self.arguments})"


# =============================================================================
# 3. The Parser
# =============================================================================
# Validates grammatical correctness and builds our structural AST tree branches.

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0  

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, expected_type: str) -> Token:
        token = self.peek()
        if token.type == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(
            f"[Parser Error] Expected token type '{expected_type}', "
            f"but found '{token.type}' ('{token.value}') at line {token.line}, col {token.column}."
        )

    def parse(self) -> List[ASTNode]:
        statements: List[ASTNode] = []
        while self.peek().type != 'EOF':
            statements.append(self.parse_expression())
        return statements

    def parse_expression(self) -> ASTNode:
        token = self.peek()
        if token.type == 'IDENTIFIER':
            return self.parse_call_expression()
        raise SyntaxError(f"[Parser Error] Expression cannot begin with token '{token.type}' at line {token.line}")

    def parse_call_expression(self) -> CallNode:
        identifier_token = self.consume('IDENTIFIER')
        callee_name = identifier_token.value
        
        self.consume('LPAREN')
        arguments: List[ASTNode] = []
        if self.peek().type != 'RPAREN':
            arguments.append(self.parse_primary())
            while self.peek().type == 'COMMA':
                self.consume('COMMA') 
                arguments.append(self.parse_primary())
                
        self.consume('RPAREN')
        return CallNode(callee=callee_name, arguments=arguments)

    def parse_primary(self) -> ASTNode:
        token = self.peek()
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            return NumberNode(token.value)
        raise SyntaxError(f"[Parser Error] Expected a valid numerical parameter, found '{token.type}' at line {token.line}")


# =============================================================================
# 4. The Interpreter (Runtime Engine)
# =============================================================================
# Maps your parsed AST nodes to actual native functional features and variables.

class Environment:
    """Manages the registered functions available globally in Speckle scripts."""
    def __init__(self):
        self.globals: Dict[str, Any] = {}

    def register_function(self, name: str, func_pointer):
        self.globals[name] = func_pointer


class Interpreter:
    def __init__(self, env: Environment):
        self.env = env

    def execute(self, statements: List[ASTNode]):
        try:
            for statement in statements:
                self.visit(statement)
        except Exception as e:
            print(f"Execution Aborted: {e}", file=sys.stderr)

    def visit(self, node: ASTNode) -> Any:
        if isinstance(node, NumberNode):
            return self.visit_NumberNode(node)
        elif isinstance(node, CallNode):
            return self.visit_CallNode(node)
        else:
            raise NotImplementedError(f"No interpreter routine found for node type: {type(node).__name__}")

    def visit_NumberNode(self, node: NumberNode) -> int:
        return node.value

    def visit_CallNode(self, node: CallNode) -> Any:
        func_name = node.callee
        if func_name not in self.env.globals:
            raise NameError(f"Runtime Exception: The function '{func_name}' is not defined in Speckle environment.")
            
        evaluated_args = [self.visit(arg) for arg in node.arguments]
        return self.env.globals[func_name](*evaluated_args)


# =============================================================================
# Speckle Standard API (Native Library Functions)
# =============================================================================

# --- 1. The Fibonacci Tracker Loop ---
def speckle_fibonacci_loop(start_val: int, limit: int):
    """Computes and visually outputs the Fibonacci progression starting from values."""
    print(f"\n[Speckle Loop] Calculating sequence up to limit: {limit}")
    a, b = start_val, start_val + 1 if start_val == 0 else start_val
    sequence = []
    
    while a <= limit:
        sequence.append(a)
        a, b = b, a + b
        
    print(f"-> Generated Sequence: {sequence}")

# --- 2. Math Library ---
def speckle_add(x: int, y: int) -> int: return x + y
def speckle_sub(x: int, y: int) -> int: return x - y
def speckle_mul(x: int, y: int) -> int: return x * y
def speckle_div(x: int, y: int) -> int: 
    if y == 0: raise ZeroDivisionError("Cannot divide by zero in Speckle math.")
    return x // y

# --- 3. Linear / Object Movement (Turtle API) ---
def init_canvas():
    """Sets up our visual canvas window."""
    turtle.setup(width=600, height=600)
    turtle.title("Speckle Engine Visual Render Instance")
    turtle.bgcolor("#1e1e2e") # Deep dark aesthetic
    turtle.color("#a6adc8")
    turtle.pencolor("#89b4fa") # Pastel blue tracer line
    turtle.speed(3)
    turtle.shape("turtle")

def move_forward(distance: int):  turtle.forward(distance)
def move_backward(distance: int): turtle.backward(distance)
def turn_left(degrees: int):      turtle.left(degrees)
def turn_right(degrees: int):     turtle.right(degrees)
def pen_up():                     turtle.penup()
def pen_down():                   turtle.pendown()


# =============================================================================
# Core Pipeline Execution
# =============================================================================
if __name__ == "__main__":
    # Writing a robust script directly in our new language syntax!
    speckle_script = """
    (( First let's calculate our finished Fibonacci numbers ))
    fib(1, 100)
    
    (( Let's trigger our graphics setup routine ))
    init_canvas()
    
    (( Draw a structural geometric vector shape on the screen using movement commands ))
    move_forward(100)
    turn_left(90)
    move_forward(100)
    turn_left(90)
    move_forward(100)
    turn_left(90)
    move_forward(100)
    turn_left(45)
    
    (( Shift coordinates without rendering tracks ))
    pen_up()
    move_forward(150)
    pen_down()
    
    (( Draw another line scaled dynamically with our math rules ))
    move_forward(100)
    """

    print("-" * 70)
    print(" Speckle Engine Development Pipeline")
    print("-" * 70)
    
    # Run Compiler Stages
    lexer = Lexer(speckle_script)
    token_stream = lexer.tokenize()
    
    parser = Parser(token_stream)
    ast_tree = parser.parse()

    # Hooking up Environment Context mapping keys to Python implementations
    runtime_env = Environment()
    
    # Bind Sequence & Math Commands
    runtime_env.register_function("fib", speckle_fibonacci_loop)
    runtime_env.register_function("add", speckle_add)
    runtime_env.register_function("sub", speckle_sub)
    runtime_env.register_function("mul", speckle_mul)
    runtime_env.register_function("div", speckle_div)
    
    # Bind Object Linear Actions
    runtime_env.register_function("init_canvas", init_canvas)
    runtime_env.register_function("move_forward", move_forward)
    runtime_env.register_function("move_backward", move_backward)
    runtime_env.register_function("turn_left", turn_left)
    runtime_env.register_function("turn_right", turn_right)
    runtime_env.register_function("pen_up", pen_up)
    runtime_env.register_function("pen_down", pen_down)
    
    print("\n--- Script Output Start ---")
    interpreter = Interpreter(runtime_env)
    interpreter.execute(ast_tree)
    print("--- Script Output End ---\n")
    
    print("-" * 70)
    print(" Pipeline execution finished cleanly. Close the canvas to finish.")
    print("-" * 70)
    
    # Keep turtle graphic pipeline active until manually closed by clicking
    turtle.done()
