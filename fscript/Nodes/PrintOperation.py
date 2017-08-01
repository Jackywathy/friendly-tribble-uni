from Nodes.NodeBase import *
from Lexer.tokens import *

class PrintOperation(ParseTree):
    print_val = []



    def __init__(self, tokens, parser):
        super().__init__(tokens)
        tokens.pop()
        assert(isinstance(tokens.pop(), LeftBracket))
        self.toprint = tokens.pop()
        assert isinstance(self.toprint, (NumLiteral, StrLiteral)) or isinstance(parser.get_type(self.toprint.token_content), (NumType, StringType))
        if isinstance(self.toprint, StrLiteral):
            self.print_val.append(self.toprint.token_content)
        assert(isinstance(tokens.pop(), RightBracket))
        assert(isinstance(tokens.pop(), EndChar))
