import sys
from expr_tree import *

class WordTokenizer():
    def __init__(self, s):
        self.s = s
        self.cur = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.cur < len(self.s):
            if self.s[self.cur] == ' ':
                self.cur = self.cur + 1
            elif self.s[self.cur] == ',':
                self.cur = self.cur + 1
                return ","
            elif self.s[self.cur].isalpha():
                token = ""
                while self.cur < len(self.s) and self.s[self.cur].isalpha():
                    token = token + self.s[self.cur]
                    self.cur = self.cur + 1
                return token
            else:
                raise Exception("Unexpected symbol")
        raise StopIteration


class TextParser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.cur = 0
        self.letter = 'P'

    def calc_expr_tree(self, quantor=False):
        if self.cur == len(self.tokens):
            raise Exception("Unexpected end of statement")
        if self.tokens[self.cur] == "неправда":
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == ",")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "что")
            self.cur = self.cur + 1
            et = self.calc_expr_tree()
            return NegExprTree(et)
        elif self.tokens[self.cur] == "если":
            self.cur = self.cur + 1
            arg1 = self.calc_expr_tree()
            assert(self.tokens[self.cur] == ",")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "то")
            self.cur = self.cur + 1
            arg2 = self.calc_expr_tree()
            return BinaryExprTree(BinaryOperation.IMPL, arg1, arg2)
        elif self.tokens[self.cur] == "из":
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "того")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "факта")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == ",")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "что")
            self.cur = self.cur + 1
            arg1 = self.calc_expr_tree()
            assert(self.tokens[self.cur] == ",")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "следует")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == ",")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "что")
            self.cur = self.cur + 1
            arg2 = self.calc_expr_tree()
            return BinaryExprTree(BinaryOperation.IMPL, arg1, arg2)
        elif self.tokens[self.cur] == "верно":
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "как")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "то")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == ",")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "что")
            self.cur = self.cur + 1
            arg1 = self.calc_expr_tree()
            assert(self.tokens[self.cur] == ",")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "так")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "и")
            self.cur = self.cur + 1
            assert(self.tokens[self.cur] == "что")
            self.cur = self.cur + 1
            arg2 = self.calc_expr_tree()
            return BinaryExprTree(BinaryOperation.CONJ, arg1, arg2)
       # elif self.tokens[self.cur] == "некоторые":
       #     self.cur = self.cur + 1
       #     et = self.calc_expr_tree(True)
       #     assert(et.get_type() == ExprTreeType.VAR)
       #     et.var_name = "Exists x " + et.var_name
       #     return et
       # elif self.tokens[self.cur] == "все":
       #     self.cur = self.cur + 1
       #     et = self.calc_expr_tree(True)
       #     assert(et.get_type() == ExprTreeType.VAR)
       #     et.var_name = "All x " + et.var_name
       #     return et
        else:
            if self.tokens[self.cur] == "некоторые":
                self.cur = self.cur + 1
                et = self.calc_expr_tree(True)
                assert(et.get_type() == ExprTreeType.VAR)
                et.var_name = "Exists x " + et.var_name
            elif self.tokens[self.cur] == "все":
                self.cur = self.cur + 1
                et = self.calc_expr_tree(True)
                assert(et.get_type() == ExprTreeType.VAR)
                et.var_name = "All x " + et.var_name
            else:
                noun = self.tokens[self.cur]
                self.cur = self.cur + 1
                neg = False
                if self.tokens[self.cur] == "не":
                    neg = True
                    self.cur = self.cur + 1
                verb = self.tokens[self.cur]
                self.cur = self.cur + 1
                if self.cur < len(self.tokens) and self.tokens[self.cur] not in ["и", "или", ","]:
                    verb = verb + " " + self.tokens[self.cur]
                    self.cur = self.cur + 1
                et = VarExpr(self.letter + "(x)")
                self.letter = chr(ord(self.letter) + 1)
                print(et.var_name, " = '", "x ", verb, "'", sep='')
                if neg:
                    # et = NegExprTree(et)
                    et.var_name = "~" + et.var_name
            if self.cur < len(self.tokens) and not quantor:
                if self.tokens[self.cur] == "и":
                    self.cur = self.cur + 1
                    et1 = self.calc_expr_tree()
                    et = BinaryExprTree(BinaryOperation.CONJ, et, et1)
                elif self.tokens[self.cur] == "или":
                    self.cur = self.cur + 1
                    et1 = self.calc_expr_tree()
                    et = BinaryExprTree(BinaryOperation.DISJ, et, et1)
            return et


f = open('input.txt', 'r')
s = f.readline()
print(s)
tokens = list(WordTokenizer(s))
#print(tokens)
tp = TextParser(tokens)
et = tp.calc_expr_tree()
et.print(sys.stdout)
