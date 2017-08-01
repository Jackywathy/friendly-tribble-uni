from Lexer.tokens import Term, EndChar, Assignment, CommaSeperator, NumType, StringType, NumLiteral, StrLiteral
from Nodes.NodeBase import *

__all__ = [
    "VariableDeclarationComplete",
    "SingleVariableDeclaration",
    "DataType",
    "VariableAssignment"
]


class VariableDeclarationComplete(ParseTree):
    def __init__(self, tokens):
        super().__init__(tokens)

        # name = type of declaration
        self.type = self.pop()
        assert isinstance(self.type, (NumType, StringType))

        self.vars = []
        self.vars.append(SingleVariableDeclaration(tokens, self.type))

        while self.startswithType(CommaSeperator):
            self.pop()
            self.vars.append(SingleVariableDeclaration(tokens, self.type))

        if not self.startswithType(EndChar):
            raise SyntaxError("Expected {} at end of declaration".format(";"))
        # pop of the ; character
        self.pop()

    def  __str__(self):
        return str(self.type.token_content)


class SingleVariableDeclaration(ParseTree):
    def __init__(self, tokens, token_type):
        super().__init__(tokens)
        self.name = DataType(tokens)

        self.init = None
        if self.startswithType(Assignment):
            # remove Assignment
            self.pop()
            self.init = Expression(tokens)
        else:
            if isinstance(token_type, NumType):
                self.init = Expression(None, NumLiteral(0))
            elif isinstance(token_type, StringType):
                self.init = Expression(None, StrLiteral(0))
            else:
                raise SyntaxError("Must be stringType or NumType")

    def __str__(self):
        return str(self.init.value)

    def __repr__(self):
        return str(self)


class DataType(ParseTree):
    def __init__(self, tokens):
        super().__init__(tokens)
        if not self.startswithType(Term):
            raise SyntaxError("Expected term at start of variable declaration")
        self.name = self.pop()

    def __str__(self):
        return self.name.token_content


class VariableAssignment(SingleVariableDeclaration):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.consume_end_char()
