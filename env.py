import sys
import os
import math
import random
import turtle
import urllib.request
from typing import Dict, Any, List
from parse import ASTNode, NumberNode, StringNode, VariableAccessNode, VariableAssignmentNode, CallNode

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
        last_val = None
        for statement in statements:
            last_val = self.visit(statement)
        return last_val

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

# Speckle API Endpoints
def spk_print(*args): print(" ".join(str(arg) for arg in args))
def spk_warn(*args):  print(f"⚠️ [Speckle Warning] {' '.join(str(arg) for arg in args)}", file=sys.stderr)
def spk_clear():     print("\033[H\033[2J", end="")

def spk_http_get(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"🚨 Network Fault: {e}"

def spk_write_file(path: str, data: str) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f: f.write(data)
        return True
    except: return False

def spk_read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: return f"🚨 File IO Error: {e}"

def spk_os_execute(cmd: str) -> str:
    import subprocess
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.stdout else result.stderr.strip()
    except Exception as e: return f"🚨 Shell Error: {e}"

def spk_get_platform() -> str:
    if os.path.exists('/data/data/com.termux'): return "android_termux"
    return sys.platform

def spk_if_equal(val1, val2, matching_result, fallback_result):
    return matching_result if val1 == val2 else fallback_result

def ascii_textify(payload: str) -> str:
    try:
        segments = [s.strip() for s in payload.split('\\') if s.strip()]
        return "".join(chr(int(seg, 10)) for seg in segments)
    except: return "🚨 Decoding Fault"

def jumble_string(payload: str) -> str:
    return "\\".join(str(ord(c)) for c in payload)

def inject_junk(count: int):
    pool = ["_tmp = add(1, 2)", "_dummy = random_range(1, 10)", "_val = mul(5, 5)"]
    for i in range(count): print(f"   >> JUNK_OP_{i}: {random.choice(pool)}")

def math_add(x, y): return x + y
def math_sub(x, y): return x - y
def math_mul(x, y): return x * y
def math_div(x, y): return x / y if y != 0 else 0.0
def math_rand_int(l, h): return random.randint(int(l), int(h))

def bootstrap_environment() -> Interpreter:
    env = Environment()
    env.register_function("print", spk_print)
    env.register_function("warn", spk_warn)
    env.register_function("clear_console", spk_clear)
    env.register_function("http_get", spk_http_get)
    env.register_function("write_file", spk_write_file)
    env.register_function("read_file", spk_read_file)
    env.register_function("os_execute", spk_os_execute)
    env.register_function("get_platform", spk_get_platform)
    env.register_function("if_equal", spk_if_equal)
    env.register_function("ascii_textify", ascii_textify)
    env.register_function("jumble_string", jumble_string)
    env.register_function("inject_junk", inject_junk)
    env.register_function("add", math_add)
    env.register_function("sub", math_sub)
    env.register_function("mul", math_mul)
    env.register_function("div", math_div)
    env.register_function("random_int", math_rand_int)
    return Interpreter(env)
