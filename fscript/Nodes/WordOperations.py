from Nodes.NodeBase import *
from Lexer.tokens import *


class AddWordOperation(ParseTree):
    def __init__(self, tokens, parser):
        self.parser = parser
        super().__init__(tokens)
        assert isinstance(tokens.pop(), AddToken)
        self.amount = tokens.pop()

        assert isinstance(tokens.pop(), ToToken)
        self.operand = tokens.pop()
        assert isinstance(self.operand, Term)

        if isinstance(parser.get_type(self.operand.token_content), NumType):
            # make sure the amount added is also a number
            if isinstance(self.amount, Term):
                if isinstance(parser.get_type(self.amount.token_content), NumType):
                    pass
                else:
                    raise SyntaxError("Amount added on line {}, row {}, must be a number".format(self.amount.line_num, self.amount.line_col))
            elif isinstance(self.amount, NumLiteral):
                pass
            else:
                raise SyntaxError("Amount added must be a number literal, or another number")
        else:
            raise NotImplementedError()
        assert isinstance(tokens.pop(), EndChar)




    def __str__(self):
        return "{} += {}".format(self.operand, self.amount)


