from Lexer.lexer import *
from Lexer.tokens import *

from collections import deque

__all__ = [
    "InvalidSyntaxException",
    "ParseTree",
    "Expression",
    "DeclaredTerms"
]

DeclaredTerms = {}


class InvalidSyntaxException(Exception):
    """The Tokens where in a wrong order or something"""
    def __init__(self, token, message=None):
        self.token = token
        self.message = message

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{} on line {}, column {}".format(self.message, self.token.row, self.token.col)


class ParseTree:
    def __init__(self, tokens):
        """BaseClass for ParseTree Elements"""
        self.tokens = tokens # type: StateStoreQueue

    def pop(self):
        return self.tokens.pop()

    def append(self, item):
        self.tokens.append(item)

    def startswithType(self, items):
        return self.tokens and isinstance(self.tokens[0], items)

    def consume_end_char(self):
        if not self.startswithType(EndChar):
            raise SyntaxError("Expected {} at end of declaration".format(";"))
        # pop of the ; character
        self.pop()

    def SyntaxError(self, msg="The Syntax was wrong"):pass


EXPRESSION_CLOSE = CommaSeperator, EndChar
SHUNT_NUMBER = NumLiteral, StrLiteral, Term
OPERATORS = MathOperator, BitwiseOperator, LogicalOperator
L = "LEFT"
R = "RIGHT"
PRECEDENCE = {
    "==": (1, L),
    "^" : (1, L),
    "||": (1, L),

    "+": (3, L),
    "-": (3, L),
    "*": (4, L),
    "/": (4, L),

    "**": (5, R),

    "(": (0, L),
    ")": (100, L),
}


class Expression(ParseTree):
    def __init__(self, tokens, opt=None):
        if tokens is None:
            self.value=opt
            assert opt is not None
            return

        super().__init__(tokens)
        self.value = None
        if tokens.peek_type(NumLiteral):
            self.polish = self.shunting()
            self.value = self.evaluate()
        elif tokens.peek_type(StrLiteral):
            self.value = self.pop()
        else:
            raise InvalidSyntaxException("Must be StrLiteral or NumLiteral?")

    def evaluate(self):
        stack = []
        for letter in self.polish:
            if letter in PRECEDENCE: # it is an operator

                op1,op2 = stack[-2:]
                del stack[-2:]
                if isinstance(op1, NumLiteral) and isinstance(op2, NumLiteral):
                    if letter == "+":
                        stack.append(NumLiteral(int(op1.token_content) + int (op2.token_content)))
                    elif letter == "-":
                        stack.append(NumLiteral(int(op1.token_content) - int (op2.token_content)))
                    elif letter == "*":
                        stack.append(NumLiteral(int(op1.token_content) * int (op2.token_content)))
                    elif letter == "/":
                        stack.append(NumLiteral(int(op1.token_content) // int (op2.token_content)))
                    elif letter == "**":
                        stack.append(NumLiteral(int(op1.token_content) ** int (op2.token_content)))

                    else:
                        raise Exception("cant find operator?")
                else:
                    raise NotImplementedError("Variables in initalization is not supported")
            else:
                stack.append(letter)
        return stack[0]

    def shunting(self):
        """Convert into polish notation"""
        output = deque()
        stack = []

        while self.tokens and not isinstance(self.tokens[0], EXPRESSION_CLOSE):
            token = self.pop()
            if isinstance(token, SHUNT_NUMBER):
                output.append(token)
            elif isinstance(token, OPERATORS):
                while stack:
                    o1 = token.token_content
                    o2 = stack[-1]
                    o1precedence, o1assoc = PRECEDENCE[o1]
                    o2precedence, o2assoc = PRECEDENCE[o2]
                    if o1assoc == L and o1precedence <= o2precedence:
                        output.append(stack[-1])
                        stack.pop()
                    elif o1assoc == R and o1precedence < o2precedence:
                        output.append(stack[-1])
                        stack.pop()
                    else:
                        break
                stack.append(token.token_content)

            elif isinstance(token, LeftBracket):
                stack.append(token.token_content)

            elif isinstance(token, RightBracket):
                before = stack[:]
                try:
                    while stack[-1] != "(":
                        if not stack:
                            raise SyntaxError("Mismatched Brackets")
                        output.append(stack.pop())
                        # raises IndexError on mismatched parenthesis!!!!!! CHANGEEE!
                    # pop the leftbracket off
                    assert stack.pop() == "("
                except:
                    print(before)
                    raise

            else:
                raise Exception("Unexpected token," + str(token))

        while stack:
            if isinstance(stack[-1], (LeftBracket, RightBracket)):
                raise SyntaxError("Mismatched Brackets")
            output.append(stack.pop())
        return output

