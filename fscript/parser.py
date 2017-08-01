from Lexer.lexer import *
class Node:
    pass

class ParserException(Exception):
    pass

class InvalidTokenException(ParserException):
    pass

class UndeclaredDataTypeException(ParserException):
    pass



class Parser:
    BUILTIN_DATATYPES = ["int", "bool", "long"]
    SIZES = [4,1,8]
    def __init__(self, filename="fscript.fer", ruleName="rules.txt"):
        self.bss = []
        self.data = []
        self.text = []

        self.program = []
        self.constants = []

        self.tokens = []

        self.userDataType = []
        self.dataTypeSize = {}

        self.init()

        lex = Lexer()
        lex.read_rules(ruleName)
        lex.init()
        

    def generate(self, filename):
        with open(filename, 'w') as f:
            for const in self.constants:
                print(const, file=f)
            print("section .data", file=f)
            for data in self.data:
                print(data, file=f)
            


    def init(self):
        self.text.append("global _start")
        self.constants.append("SYS_EXIT equ 1")
        self.constants.append("SYS_WRITE equ 4")
        self.constants.append("SYS_READ equ 3")

        self.constants.append("STDIN equ 0")
        self.constants.append("STDOUT equ 1")
        self.constants.append("STDERR equ 2")
        for data, size in zip(self.BUILTIN_DATATYPES, self.SIZES):
            self.dataTypeSize[data] = size

    def DECLARE_TOKEN(self, token):
        dataType, vars = token.token_content.split()
        if not (dataType in self.BUILTIN_DATATYPES or dataType in self.userDataType):
            raise UndeclaredDataTypeException()

        itemSize = self.dataTypeSize[dataType]


        for var_data in vars.rstrip(";").split(","):
            li = var_data.split(",")
            if len(li) == 2:
                var, initValue = li
            else:
                assert len(li) == 1
                var = li[0]
                initValue = 0

            self.add_bss(var, itemSize, initValue)

            
    def ASSIGN_TOKEN(self, token):
        pass

    def EXPRESS_TOKEN(self, tokens):
        pass

    def add_bss(self, name, item_size, init_value):
        directive = 'DB'
        if item_size == 4:
            directive = 'DD'
        self.bss.append("{} {} {}".format(name, directive, init_value))
try:
    parse = Parser()
    parse.generate("program.asm")

except Exception as e:
    print(e)
    raise