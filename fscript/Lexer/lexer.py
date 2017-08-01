import re
import string

from Lexer.tokens import *
from collections import OrderedDict

debug = False


class RuleException(Exception):
    def __init__(self, reason=None, lineNum=-1):
        self.lineNum = lineNum
        self.reason = reason

    def __repr__(self):
        return str(self)

class DuplicateRuleException(RuleException):
    def __str__(self):
        return "Rule with duplicate name " + str(self.reason) + " lineNum: " + str(self.lineNum)

class InvalidRuleException(RuleException):
    def __str__(self):
        return "Rule was wrong! " + str(self.reason) + " lineNum: " + str(self.lineNum)



class Rule:
    def __init__(self, name, content, lineNum):
        self.name = name
        self.content = content
        self.lineNum = lineNum

    def __str__(self):
        return "{name} := {content} -- line: {lineNum}".format(name =self.name, 
                                                               content = self.content, 
                                                               lineNum = self.lineNum)


class StateStoreQueue:
    __slots__ = [
        "tokens",
        "count",
        "old_state"
    ]

    def __init__(self, tokens=(), start_count=0):
        self.tokens = list(tokens)
        self.count = start_count
        self.old_state = None

    def pop(self):
        temp = self.tokens[self.count]
        self.count += 1
        return temp

    def peek(self):
        return self.tokens[self.count]

    def append(self, item):
        self.tokens.append(item)

    def extend(self, items):
        for i in items:
            self.tokens.append(i)

    def store_state(self):
        self.old_state = self.count
        return self.old_state

    def restore_state(self):
        assert self.old_state is not None
        self.count = self.old_state
        return self.count

    def __len__(self):
        return len(self.tokens) - self.count

    def __getitem__(self, item):
        return self.tokens[self.count+item]

    def peek_type(self, type):
        return isinstance(self.peek(), type)

    def __str__(self):
        return str(self.tokens[self.count:])

    def __repr__(self):
        return str(self)




class Lexer:
    statements = OrderedDict([
        ("LeftBracket", LeftBracket),
        ("RightBracket", RightBracket),
        ("CommaSeperator", CommaSeperator),
        ("PrintToken", PrintToken),

        ("NumLiteral", NumLiteral),
        ("StrLiteral", StrLiteral),

        ("LogicalOperator", LogicalOperator),
        ("BitwiseOperator", BitwiseOperator),
        ("MathOperator", MathOperator),

        ("WhatsThisOperator", WhatsThisOperator),


        ("NumType", NumType),
        ("StringType", StringType),
        ("Assignment", Assignment),

        ("ToWord", ToToken),
        ("AddWord", AddToken),
        ("TakeWord", TakeToken),
        ("FromWord", FromToken),



        ("Term", Term),



        ("EndChar", EndChar),
    ]
    )
    # statements will be converted into a dictionary containing, in __init__
    # "logicaloperator" : [class logicalOperator, regex pattern]

    # Ordered, higher means higher priority
    # must be passed in as a list or it losses its order to the kwargs gods


    NO_SPACE = ['+', '-', '*', '/', '--', '++', '==', '=', ';', "(", ")"]

    def __init__(self, rule_file="rules.txt"):
        self.rules = {} # string:Rule
        self.read_rules(rule_file)
        for key, value in self.statements.items():
            self.statements[key] = [value, re.compile("^" + self.rules[key])]

    def read_rules(self, file):
        with open(file) as f:
            for lineNum, line in enumerate(f):
                if line.isspace() or line.startswith("#"):
                    continue
                try:
                    name, content = line.split(":=", maxsplit=1)
                    name = name.strip(" ")
                    content = content.strip(" ")
                except ValueError:
                    raise InvalidRuleException("No := symbol on line", lineNum+1)
                self.add_rule(name.strip(), content, lineNum+1)

    def add_rule(self, rule_name, content, lineNum):
        """Sub's in dependencies and processes the content"""
        word = []
        all_words = []
        in_string = False
        has_quotes = False
        escaped = False

        for letter in content:
            if letter == " " and not in_string:
                if not word:
                    raise InvalidRuleException("Empty word before space symbol " + str(all_words), lineNum)
                if in_string:
                    raise InvalidRuleException("Require a closing quote before + symbol", lineNum)

                if not has_quotes:
                    # this word is an actual rule and needs to be filled in
                    word = "".join(word)
                    all_words.append(self.get_rule(word, lineNum))
                    
                else:
                    # this word is a raw string 
                    word = "".join(word)
                    all_words.append(word)
                word = []
                has_quotes = False
            elif letter == " ":
                word.append(" ")

            elif letter.isspace():
                continue

            elif letter == '"' and not escaped:
                if not in_string and has_quotes:
                    raise InvalidRuleException("> 2 quotes", lineNum)
                in_string = not in_string
                has_quotes = True

            elif letter == "\\" and not escaped:
                escaped = True
                word.append("\\")
            else:
                escaped = False
                if has_quotes and not in_string:
                    # there is a letter after a quoted rule, e.g. ("asdf" fs + )
                    raise InvalidRuleException("Unexpected characters after closing quote", lineNum)
                word.append(letter)

        if in_string:
            raise InvalidRuleException("Unclosed quotation", lineNum)

        if word:
            if not has_quotes:
                # this word is an actual rule and needs to be filled in
                word = "".join(word)
                all_words.append(self.get_rule(word, lineNum))
                    
            else:
                # this word is a raw string 
                word = "".join(word)
                all_words.append(word)

        ret = "".join(all_words)
        self.rules[rule_name] = ret
        return ret

    def get_rule(self, ruleName, lineNum=-1):
        try:
            return self.rules[ruleName]
        except KeyError:
            raise InvalidRuleException("Cannot find rule, " + str(ruleName), lineNum)

    def read_source(self, fname):
        ret = StateStoreQueue()
        with open(fname) as f:
            file = f.read()
            for i, line in enumerate(file.splitlines()):
                ret.extend(self.tokenize(line, i+1))
        return ret
    

    def tokenize(self, file, row=-1):
        ret = []
        col = 1
        while file:
            while file.startswith(tuple(string.whitespace)):
                file = file[1:]
                col += 1

            if not file:
                # the file is empty
                break
            for class_name, pattern in self.statements.values():
                match = pattern.match(file)
                if match:
                    assert match.span()[0] == 0
                    token_len = match.span()[1]
                    ret.append(class_name(match.group(), row, col))
                    col += token_len

                    file = file[token_len:]
                    break
            else:
                raise SyntaxError("Uncrecongnizable token at row: {}, col: {}, remaining content: \"{}\"".format(row, col, file))

        return ret





