# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\teval.py
# Compiled at: 2011-11-06 21:21:06
from dao.solve import make_solver
from dao.t.grammar import grammar
from dao.builtins.parser import parse_text
from dao.t.builtins import global_env

def teval(text):
    solver = make_solver(global_env, global_env.extend(), None, None)
    exp = parse_text(grammar, text)
    return solver.eval(exp)


teval('1')