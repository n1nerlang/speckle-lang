import re
from typing import List, NamedTuple

class Token(NamedTuple):
    type: str     
    value: str    
    line: int     
    column: int   

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
