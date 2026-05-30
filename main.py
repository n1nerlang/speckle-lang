import sys
from lex import Lexer
from parse import Parser
from env import bootstrap_environment

def run_repl(interpreter):
    print("Speckle Language Terminal Environment [v1.5.0b]")
    print("Copyright (c) 2026 Speckle LLC / n1nerlang. Type 'exit' to leave.\n")
    
    while True:
        try:
            line = input("spk > ").strip()
            if line.lower() == "exit": break
            if not line: continue
                
            ast = Parser(Lexer(line).tokenize()).parse()
            res = interpreter.execute(ast)
            if res is not None:
                print(f"-> {res}")
        except KeyboardInterrupt:
            print("\nExiting system safely.")
            break
        except Exception as e:
            print(f"🚨 Line execution faulted: {e}", file=sys.stderr)

if __name__ == "__main__":
    interpreter = bootstrap_environment()
    
    if len(sys.argv) < 2:
        run_repl(interpreter)
    else:
        target = sys.argv[1]
        try:
            with open(target, 'r', encoding='utf-8') as f:
                code = f.read()
            ast = Parser(Lexer(code).tokenize()).parse()
            interpreter.execute(ast)
        except FileNotFoundError:
            print(f"❌ IO Error: File path not found: '{target}'")
            sys.exit(1)
        except Exception as err:
            print(f"🚨 Execution Fault Error:\n{err}", file=sys.stderr)
