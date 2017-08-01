class Token:
    type = NotImplemented

    def __init__(self, token_content, line_num=-1, line_col=-1):
        self.token_content = token_content
        self.line_num = line_num
        self.line_col = line_col

    def __str__(self):
        return "\"[{}, {}]\"".format(str(self.type), str(self.token_content))

    def __repr__(self):
        return self.__str__()


class LogicalOperator(Token):
    type = "Logical Operation (==, ||) etc"

class PrintToken(Token):
    type = "Print Token"

class MathOperator(Token):
    type = "Maths Operation"


class NumLiteral(Token):
    type = "Num Literal"


class StrLiteral(Token):
    type = "String Literal"


class Term(Token):
    type = "Term"


class EndChar(Token):
    type = "EndChar (;)"


class Assignment(Token):
    type = "Assignment (=)"


class CommaSeperator(Token):
    type = "Comma Seperator (,)"


class NumType(Token):
    type = "Num datatype"


class LeftBracket(Token):
    type = "LeftBracket"


class RightBracket(Token):
    type = "RightBracket"


class BitwiseOperator(Token):
    type = "Bitwise"

class StringType(Token):
    type = "String datatype"

class AddToken(Token):
    type = "AddWord"

class WhatsThisOperator(Token):
    type = "Whats this?"

class ToToken(Token):
    type = "ToToken"

class TakeToken(Token):
    type = "TakeWord"

class FromToken(Token):
    type = "FromWord"