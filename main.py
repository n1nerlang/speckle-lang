"""
===============================================================================
                       The Speckle Programming Language
===============================================================================
Core Engine Production Platform (.spk / .speckle / .sp / .pk)
Advanced Stack: Byte Decoding, ASCII-Textify Pipelines, Math, Vector Graphics

Architecture Blueprint:
  1. Lexer (Tokenizer)     - Full expression parsing, floats, logic strings.
  2. AST Nodes             - Variables, assignment, literals, multi-args.
  3. Parser                - Top-down Recursive Descent Parsing Engine.
  4. Interpreter (Runtime) - Dynamic Memory Space Environment Allocation.
===============================================================================
"""

import re
import sys
import math
import random
import turtle
import datetime
from typing import List, NamedTuple, Any, Dict, Optional

# =============================================================================
# 1. The Lexer (Tokenizer Engine)
# =============================================================================

class Token(NamedTuple):
    type: str     
    value: str    
    line: int     
    column: int   

    def __repr__(self) -> str:
        return f"Token({self.type}, {repr(self.value)}, Line:{self.line}, Col:{self.column})"


class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        
        rules = [
            ('COMMENT',    r'\(\([\s\S]*?\)\)'), 
            ('STRING',     r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''),
            ('NUMBER',     r'-?\d+(?:\.\d+)?'),            
            ('ASSIGN',     r'='),
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
                if kind == 'STRING':
                    value = value[1:-1]
                self.tokens.append(Token(kind, value, line_num, column))
                
        self.tokens.append(Token('EOF', '', line_num, len(self.source_code) - line_start + 1))
        return self.tokens


# =============================================================================
# 2. Abstract Syntax Tree (AST Nodes)
# =============================================================================

class ASTNode: pass

class NumberNode(ASTNode):
    def __init__(self, value: str):
        self.value = float(value) if '.' in value else int(value)
    def __repr__(self) -> str: return f"NumberNode({self.value})"

class StringNode(ASTNode):
    def __init__(self, value: str):
        self.value = value
    def __repr__(self) -> str: return f"StringNode('{self.value}')"

class VariableAccessNode(ASTNode):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self) -> str: return f"VariableAccessNode('{self.name}')"

class VariableAssignmentNode(ASTNode):
    def __init__(self, name: str, value_node: ASTNode):
        self.name = name
        self.value_node = value_node
    def __repr__(self) -> str: return f"VariableAssignmentNode('{self.name}' = {self.value_node})"

class CallNode(ASTNode):
    def __init__(self, callee: str, arguments: List[ASTNode]):
        self.callee = callee          
        self.arguments = arguments    
    def __repr__(self) -> str: return f"CallNode(callee='{self.callee}', args={self.arguments})"


# =============================================================================
# 3. The Parser Engine (Recursive Descent)
# =============================================================================

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
        raise SyntaxError(f"[Parser Error] Expected '{expected_type}', got '{token.type}' at line {token.line}.")

    def parse(self) -> List[ASTNode]:
        statements: List[ASTNode] = []
        while self.peek().type != 'EOF':
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self) -> ASTNode:
        if self.peek().type == 'IDENTIFIER' and (self.pos + 1 < len(self.tokens)) and self.tokens[self.pos + 1].type == 'ASSIGN':
            ident_token = self.consume('IDENTIFIER')
            self.consume('ASSIGN')
            value_expr = self.parse_primary()
            return VariableAssignmentNode(ident_token.value, value_expr)
        
        return self.parse_expression()

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
        elif token.type == 'STRING':
            self.consume('STRING')
            return StringNode(token.value)
        elif token.type == 'IDENTIFIER':
            if (self.pos + 1 < len(self.tokens)) and self.tokens[self.pos + 1].type == 'LPAREN':
                return self.parse_call_expression()
            self.consume('IDENTIFIER')
            return VariableAccessNode(token.value)
        raise SyntaxError(f"[Parser Error] Expected valid literal value or expression context, found '{token.type}' at line {token.line}")


# =============================================================================
# 4. The Interpreter Runtime Environment
# =============================================================================

class Environment:
    def __init__(self):
        self.functions: Dict[str, Any] = {}
        self.variables: Dict[str, Any] = {}
        
    def register_function(self, name: str, func_pointer):
        self.functions[name] = func_pointer


class Interpreter:
    def __init__(self, env: Environment):
        self.env = env

    def execute(self, statements: List[ASTNode]):
        for statement in statements:
            self.visit(statement)

    def visit(self, node: ASTNode) -> Any:
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, VariableAccessNode):
            if node.name not in self.env.variables:
                raise NameError(f"Runtime Reference Error: Variable lookup targeting '{node.name}' does not exist.")
            return self.env.variables[node.name]
        elif isinstance(node, VariableAssignmentNode):
            computed_val = self.visit(node.value_node)
            self.env.variables[node.name] = computed_val
            return computed_val
        elif isinstance(node, CallNode):
            func_name = node.callee
            if func_name not in self.env.functions:
                raise NameError(f"Runtime Function Error: Call destination API method '{func_name}' is undefined.")
                
            evaluated_args = [self.visit(arg) for arg in node.arguments]
            return self.env.functions[func_name](*evaluated_args)
        else:
            raise NotImplementedError(f"Unhandled Evaluation Routine for Node Type: {type(node).__name__}")


# =============================================================================
# Speckle Standard API Methods (With Byte-Decoding Utilities)
# =============================================================================

# Core System IO
def speckle_print(*args):
    print(" ".join(str(arg) for arg in args))

def speckle_warn(*args):
    print(f"⚠️ [Speckle Warning] {" ".join(str(arg) for arg in args)}", file=sys.stderr)

def speckle_clear():
    print("\033[H\033[2J", end="")

def speckle_send_chat(user: str, message: str):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"💬 [{timestamp}] [{user}]: {message}")


# --- Advanced Processing Tools & Byte Decoders ---
def ascii_textify(payload: str) -> str:
    """
    Parses a string containing numbers separated by backslashes (e.g. '110\\1\\1\\98\\101\\051')
    and handles custom byte transformations, recovering the clean character values.
    """
    try:
        # Split on backslash characters
        segments = [s.strip() for s in payload.split('\\') if s.strip()]
        decoded_chars = []
        
        for segment in segments:
            # Handle placeholder indices, padding, or octal-style configurations safely
            val = int(segment, 10)
            decoded_chars.append(chr(val))
            
        result = "".join(decoded_chars)
        print(f"🔑 [Textify Engine] Reconstructed Plain-Text: '{result}'")
        return result
    except Exception as decoding_error:
        raise ValueError(f"Decryption Fail: Textify failed parsing structural chunk '{payload}'. Matrix: {decoding_error}")

def math_jumble_string(payload: str) -> str:
    """Converts standard readable strings directly back into raw backslash-delimited decimals."""
    jumbled = "\\".join(str(ord(char)) for char in payload)
    print(f"🔒 [Jumble Engine] Scrambled Backslash Array: {jumbled}")
    return jumbled

def generate_junk_lines(count: int):
    print(f"⚙️ [Metamorphic Engine] Injecting {count} dead instructions...")
    junk_pool = ["_tmp = add(1, 2)", "_dummy = random_range(1, 100)", "_val = mul(5, 5)"]
    for i in range(count):
        print(f"   >> JUNK_OP_{i}: {random.choice(junk_pool)}")


# --- Math & Banner Libraries ---
def math_add(x: float, y: float) -> float: return x + y
def math_sub(x: float, y: float) -> float: return x - y
def math_mul(x: float, y: float) -> float: return x * y
def math_div(x: float, y: float) -> float: return x / y if y != 0 else 0.0
def math_rand(low: float, high: float) -> float: return random.uniform(low, high)
def math_random_int(low: int, high: int) -> int: return random.randint(low, high)

def make_ascii_banner(text: str):
    border = "+" + "-" * (len(text) + 4) + "+"
    print(border)
    print(f"|  {text}  |")
    print(border)

def make_ascii_brick(width: int, height: int):
    for _ in range(height): print("#" * width)


# --- Native Turtle Vector Graphics Modules ---
def init_canvas():
    turtle.setup(width=700, height=500)
    turtle.title("Speckle Engine Matrix Workspace")
    turtle.bgcolor("#0f0f17") 
    turtle.color("#cdd6f4")
    turtle.pencolor("#89b4fa") 
    turtle.speed(0)
    turtle.shape("classic")

def set_line_color(color: str):        turtle.pencolor(color)
def set_background_color(color: str):  turtle.bgcolor(color)
def move_forward(distance: float):     turtle.forward(distance)
def turn_left(degrees: float):         turtle.left(degrees)
def turn_right(degrees: float):        turtle.right(degrees)


# =============================================================================
# Injection Logic Setup Helper
# =============================================================================
def setup_environment() -> Interpreter:
    env = Environment()
    
    # Core Operations
    env.register_function("print", speckle_print)
    env.register_function("warn", speckle_warn)
    env.register_function("clear_console", speckle_clear)
    env.register_function("send_chat", speckle_send_chat)
    
    # Textify & String Jumble Modules
    env.register_function("ascii_textify", ascii_textify)
    env.register_function("jumble_string", math_jumble_string)
    env.register_function("inject_junk", generate_junk_lines)
    env.register_function("ascii_banner", make_ascii_banner)
    env.register_function("ascii_brick", make_ascii_brick)
    
    # Math Vector Pipeline
    env.register_function("add", math_add)
    env.register_function("sub", math_sub)
    env.register_function("mul", math_mul)
    env.register_function("div", math_div)
    env.register_function("random_range", math_rand)
    env.register_function("random_int", math_random_int)
    
    # Visual Canvas Actions
    env.register_function("init_canvas", init_canvas)
    env.register_function("set_line_color", set_line_color)
    env.register_function("set_background_color", set_background_color)
    env.register_forward = env.register_function("move_forward", move_forward)
    env.register_function("turn_left", turn_left)
    env.register_function("turn_right", turn_right)
    
    return Interpreter(env)


# =============================================================================
# REPL Console Command Prompt Loop Engine Mode
# =============================================================================
def run_repl_prompt(interpreter: Interpreter):
    print("Speckle Language Shell Terminal Environment")
    print("Copyright (c) 2026 Speckle LLC / n1nerlang. Type 'exit' to leave.\n")
    
    while True:
        try:
            input_line = input("spk > ").strip()
            if input_line.lower() == "exit":
                print("Closing environment instance session safely.")
                break
            if not input_line:
                continue
                
            lexer = Lexer(input_line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            interpreter.execute(ast)
            
        except KeyboardInterrupt:
            print("\nClosing environment instance session safely.")
            break
        except Exception as e:
            print(f"🚨 Line execution faulted: {e}", file=sys.stderr)


# =============================================================================
# CLI Execution Entry
# =============================================================================
if __name__ == "__main__":
    interpreter = setup_environment()

    if len(sys.argv) < 2:
        run_repl_prompt(interpreter)
    else:
        target_filepath = sys.argv[1]
        try:
            with open(target_filepath, 'r', encoding='utf-8') as file:
                speckle_payload = file.read()
            
            lexer = Lexer(speckle_payload)
            ast_tree = Parser(lexer.tokenize()).parse()
            interpreter.execute(ast_tree)
            
            if turtle.getscreen()._canvas is not None:
                turtle.done()
        except FileNotFoundError:
            print(f"❌ IO Operational Error: Target file path not found: '{target_filepath}'")
            sys.exit(1)
        except Exception as err:
            print(f"🚨 Execution Fault Error:\n{err}", file=sys.stderr)
