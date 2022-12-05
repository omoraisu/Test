"""
Daenielle Rai Peladas 
CMSC 124 B MP 3 Part 1
"""

#######################
#       DIGITS        #
#######################

DIGITS = '0123'

#######################
#        ERROR        #
#######################

class Error:
    def __init__ (self, error_name):
        self.error_name = error_name
    
    def as_string(self):
        return f'{self.error_name}\n'

class IllegalCharError(Error):
    def __init__(self):
        super().__init__('Illegal Character')

class InvalidSyntaxError(Error):
    def __init__(self):
        super().__init__('Invalid Syntax')


#######################
#       TOKENS        #
#######################

DIGIT        = 'DIGIT'
ADD_OP       = 'ADD_OP'
SUB_OP       = 'SUB-OP'
MULT_OP      = 'MULT_OP'
DIV_OP       = 'DIV_OP'
LEFT_PAREN   = 'LEFT_PAREN'
RIGHT_PAREN  = 'RIGHT_PAREN'
END_STMNT    = 'END_STMNT'
MY_EOF       = 'MY_EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'

#######################
#        LEXER        #
#######################

class Lexer: 
    def __init__(self, input):
        self.input = input 
        self.pos = -1 
        self.curr_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.curr_char = self.input[self.pos] if self.pos < len(self.input) else None
    
    def lookup(self):
        tokens = []

        while self.curr_char != None:
            if self.curr_char == ' ':
                self.advance()
            elif self.curr_char in DIGITS:
                tokens.append(Token(DIGIT, int(self.curr_char)))
                self.advance()
            elif self.curr_char == '+':
                tokens.append(Token(ADD_OP, self.curr_char))
                self.advance()
            elif self.curr_char == '-':
                tokens.append(Token(SUB_OP, self.curr_char))
                self.advance()
            elif self.curr_char == '*':
                tokens.append(Token(MULT_OP, self.curr_char))
                self.advance()
            elif self.curr_char == '/':
                tokens.append(Token(DIV_OP, self.curr_char))
                self.advance()
            elif self.curr_char == '(':
                tokens.append(Token(LEFT_PAREN, self.curr_char))
                self.advance()
            elif self.curr_char == ')':
                tokens.append(Token(RIGHT_PAREN, self.curr_char))
                self.advance()
            elif self.curr_char == '$':
                tokens.append(Token(END_STMNT, self.curr_char))
                self.advance()
            else:
                char = self.curr_char
                self.advance()
                return [], IllegalCharError() # Return error statement here 
        
        tokens.append(Token(MY_EOF, self.curr_char))

        return tokens, None 

#######################
#        NODES        #
#######################
class DigitNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

class OpCode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class EndNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

#######################
#    PARSE RESULT     #
#######################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
    
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#######################
#       PARSER        #
#######################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    
    # Moves to the next token
    def advance(self):

        self.tok_idx += 1

        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        
        return self.current_tok
    
    """
    S ::= <expr>
    """

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != MY_EOF:
            return res.failure(InvalidSyntaxError())
        return res

    """
    <factor> ::= (<expr>) |<digit>
    """
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type == DIGIT:
            self.advance()
            return res.success(DigitNode(tok))

        if tok.type == END_STMNT and self.tok_idx == len(self.tokens):
            return res.success(EndNode(tok))
        
        return res.failure(InvalidSyntaxError())
    
    """
    <term> ::= <factor> | <term>*<factor> | <term>/<factor> 
    """
    def term(self):
        return self.general_op(self.factor, (MULT_OP, DIV_OP))

    """
    <expr> ::= <term> | <expr>+<term> | <expr>-<term>
    """
    def expr(self):
        return self.general_op(self.term, (ADD_OP, SUB_OP))
    
    """
    This is a generic form of both the grammar from expr and term since 
    these two have more or less the same methods. 
    """ 
    
    def general_op(self, func, ops):
        res  = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops: # loops so long an operation is detected
            op_tok = self.current_tok 
            self.advance()
            right = res.register(func())
            print(left, op_tok, right)
            if res.error: return res
            left = OpCode(left, op_tok, right)

        return res.success(left)
        
#######################
#        TESTS        #
#######################

lexer = Lexer("1-2*3$") 
tokens, error = lexer.lookup()

parser = Parser(tokens)
ast = parser.parse()
if ast.error: print(ast.error.as_string())
else: print(ast.node)

"""
Notes: Do something about catching the $ 
"""

