"""
===============================================================================
                       The Speckle Programming Language
===============================================================================
Core Engine Production Platform (.spk / .speckle / .sp / .pk)
Advanced Features: Mutable Scopes, Chat Networking Simulation, Console IO

Architecture Blueprint:
  1. Lexer (Tokenizer)     - Full expression parsing, logic operators, strings.
  2. AST Nodes             - Variables, assignment, literals, functions.
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
        
        # Comprehensive lexical match rules array
        rules = [
            ('COMMENT',    r'\(\([\s\S]*?\)\)'), 
            ('STRING',     r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''),
            ('NUMBER',     r'-?\d+(?:\.\d+)?'), # Support floats and integers            
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
                    value = value[1:-1] # Slice off literal boundary quotation characters
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
        # Check ahead to identify if we are dealing with a variable modification statement
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
            # Is it a variable access placeholder or a stacked function reference parameter?
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
        try:
            for statement in statements:
                self.visit(statement)
        except Exception as e:
            print(f"⚠️ Runtime Engine Execution Interrupted:\n-> {e}", file=sys.stderr)

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
# Speckle Massive Standard Lua-Style API Core Library Hooks
# =============================================================================

def speckle_print(*args):
    """Lua style print statement formatting output fields directly."""
    output_string = " ".join(str(arg) for arg in args)
    print(output_string)

def speckle_warn(*args):
    """Outputs text styled inside warning diagnostic prefixes."""
    output_string = " ".join(str(arg) for arg in args)
    print(f"⚠️ [Speckle Warning] {output_string}", file=sys.stderr)

def speckle_clear():
    """Wipes terminal clean."""
    print("\033[H\033[2J", end="")

def speckle_send_chat(user: str, message: str):
    """Simulates multi-user dynamic network server chat channels."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"💬 [{timestamp}] [{user}]: {message}")

def speckle_broadcast_event(event_name: str, numeric_payload: float):
    """Simulates inter-process networking signals across server loops."""
    print(f"📡 [Broadcast] Event '{event_name}' fired with code value: {numeric_payload}")

def speckle_loop_step(variable_name: str, start: int, end: int, function_name: str, interpreter_instance: Interpreter):
    """A high-level stepping loop that runs a mapped function on each iteration."""
    print(f"🔁 [Loop Engine] Executing loop sequence control for mapping method: '{function_name}'")
    for i in range(start, end + 1):
        interpreter_instance.env.variables[variable_name] = i
        if function_name in interpreter_instance.env.functions:
            interpreter_instance.env.functions[function_name](i)
        else:
            raise NameError(f"Loop Routine Aborted: Function target execution handle '{function_name}' is missing.")

# Vector Graphics Rendering Array Modules
def init_canvas():
    turtle.setup(width=700, height=500)
    turtle.title("Speckle Engine Matrix Workspace")
    turtle.bgcolor("#0f0f17") 
    turtle.color("#cdd6f4")
    turtle.pencolor("#89b4fa") 
    turtle.speed(0) # Maximum rendering acceleration speed
    turtle.shape("classic")

def set_line_color(color: str):        turtle.pencolor(color)
def set_background_color(color: str):  turtle.bgcolor(color)
def move_forward(distance: float):     turtle.forward(distance)
def turn_left(degrees: float):         turtle.left(degrees)
def turn_right(degrees: float):        turtle.right(degrees)

# Extended Mathematics Modules
def speckle_add(x: float, y: float) -> float: return x + y
def speckle_sub(x: float, y: float) -> float: return x - y
def speckle_mul(x: float, y: float) -> float: return x * y
def speckle_div(x: float, y: float) -> float: return x / y if y != 0 else 0.0
def speckle_rand(low: int, high: int) -> int: return random.randint(low, high)
def speckle_sin(degrees: float) -> float:     return math.sin(math.radians(degrees))


# =============================================================================
# CLI Orchestration Execution Pipeline Entry
# =============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Runtime Startup Error: Missing file argument.")
        print("Usage Checklist: python main.py <filename>.spk")
        sys.exit(1)
        
    target_filepath = sys.argv[1]
    
    try:
        with open(target_filepath, 'r', encoding='utf-8') as file:
            speckle_payload = file.read()
    except FileNotFoundError:
        print(f"❌ IO Error: Target data track file not found: '{target_filepath}'")
        sys.exit(1)

    # Initialize Environment Spaces
    runtime_env = Environment()
    interpreter = Interpreter(runtime_env)

    # Register Global IO & Networking Methods
    runtime_env.register_function("print", speckle_print)
    runtime_env.register_function("warn", speckle_warn)
    runtime_env.register_function("clear_console", speckle_clear)
    runtime_env.register_function("send_chat", speckle_send_chat)
    runtime_env.register_function("broadcast_event", speckle_broadcast_event)
    
    # Register Core Math & Utility Operations
    runtime_env.register_function("add", speckle_add)
    runtime_env.register_function("sub", speckle_sub)
    runtime_env.register_function("mul", speckle_mul)
    runtime_env.register_function("div", speckle_div)
    runtime_env.register_function("random_range", speckle_rand)
    runtime_env.register_function("get_sin", speckle_sin)
    
    # Register Graphics Controls
    runtime_env.register_function("init_canvas", init_canvas)
    runtime_env.register_function("set_line_color", set_line_color)
    runtime_env.register_function("set_background_color", set_background_color)
    runtime_env.register_function("move_forward", move_forward)
    runtime_env.register_function("turn_left", turn_left)
    runtime_env.register_function("turn_right", turn_right)
    
    # Complex Iterative Functional Mapping Control Wrapper
    runtime_env.register_function(
        "run_loop_sequence", 
        lambda var_name, start, end, func_name: speckle_loop_step(var_name, start, end, func_name, interpreter)
    )

    # Execute Compilation Stack Pipeline
    try:
        lexer = Lexer(speckle_payload)
        token_stream = lexer.tokenize()
        
        parser = Parser(token_stream)
        ast_tree = parser.parse()
        
        print("=======[ Speckle Engine Live Execution Stream ]=======")
        interpreter.execute(ast_tree)
        print("=====================================================")
        
        if turtle.getscreen()._canvas is not None:
            turtle.done()
            
    except Exception as compilation_error:
        print(f"🚨 Compiler Compilation Pipeline Fault:\n{compilation_error}", file=sys.stderr)
