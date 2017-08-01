import re
import string
import csv

debug = False

class RuleException(Exception):
	def __init__(self, reason=None, lineNum=-1):
		self.lineNum = lineNum
		self.reason = reason
	def __repr__(self):
		return ___str__(self)


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


	

class Lexer:
	def __init__(self):
		self.rules = {} # string:Rule

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
				print("adding rule:", name, "content: \"" +self.add_rule(name.strip(), content, lineNum+1)+"\"")

	def add_rule(self, rule_name, content, lineNum):
		"""Sub's in dependencies and processes the content"""
		word = []
		all_words = []
		in_string = False
		has_quotes = False
		escaped = False

		for letter in content:
			if debug:
				print("let:", ord(letter), letter)

			if letter.isspace() and not in_string:
				continue
			elif letter == '+' and not in_string:
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




try:
	lex = Lexer()
	lex.read_rules("rules.txt")
except Exception as e:
	print(e)
	print('done')
	raise