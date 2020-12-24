# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\parse.py
# Compiled at: 2011-10-28 02:31:36
from dao.term import conslist
from dao.builtins.parser import settext
from dao.builtins.terminal import eoi
from dao.builtins.control import and_
from dao.solve import Solver

class Grammar:

    def __init__(self, start, rules, result):
        self.rules, self.start, self.result = rules, start, result


def parse(grammar, text):
    global envvarCache
    envvarCache = {}
    solver = Solver()
    exp = conslist('letr', grammar.rules, (settext, text), (
     and_, grammar.start, [eoi]), grammar.result)
    return solver.eval(exp)


def eval(grammar, text):
    solver = Solver()
    exp = conslist('letr', grammar.rules, (settext, text), (
     and_, grammar.start, [eoi]), grammar.result)
    parsedExp = solver.eval(exp)
    return solver.eval(parsedExp)