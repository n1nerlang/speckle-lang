from typing import List, Any
from lex.py import Token  # Direct link to simplified lexer module

class ASTNode: pass

class NumberNode(ASTNode):
    def __init__(self, value: str):
        self.value = float(value) if '.' in value else int(value)

class StringNode(ASTNode):
    def __init__(self, value: str):
        self.value = value

class VariableAccessNode(ASTNode):
    def __init__(self, name: str):
        self.name = name

class VariableAssignmentNode(ASTNode):
    def __init__(self, name: str, value_node: ASTNode):
        self.name = name
        self.value_node = value_node

class CallNode(ASTNode):
    def __init__(self, callee: str, arguments: List[ASTNode]):
        self.callee = callee          
        self.arguments = arguments    

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
