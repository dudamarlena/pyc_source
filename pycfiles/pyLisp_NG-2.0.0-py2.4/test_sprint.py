# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylispng/util/test/test_sprint.py
# Compiled at: 2008-11-11 00:23:26
import unittest
from pylispng import lisp
from pylispng.util import sprint
ans1 = '\n   [*]\n    |--[2]\n    +--[*]\n        +--[*]\n            |--[3]\n            |--[4]\n        +--[*]\n            |--[2]\n            |--[3]\n'
ans2 = '\n   [*]\n    |--[5]\n    +--[+]\n        |--[3]\n        |--[4]\n        |--[6]\n    |--[22]\n    +--[*]\n        |--[2.3999999999999999]\n        |--[5]\n        |--[0.001]\n    +--[-]\n        |--[5]\n        +--[+]\n            |--[2]\n            +--[-]\n                |--[2]\n                |--[4]\n'

class SExpressionPrintTestCase(unittest.TestCase):
    """

    """
    __module__ = __name__

    def test_tree(self):
        """

        """
        exprs = [
         '(* 2 (* (* 3 4) (* 2 3)))', '(* 5 (+ 3 4 6) 22 (* 2.4 5 0.001) (- 5 (+ 2 (- 2 4))))']
        answers = [ x.lstrip('\n') for x in [ans1, ans2] ]
        r = lisp.Reader()
        for (expr, expected) in zip(exprs, answers):
            sexpr = r.get_sexpr(expr)
            self.assertEquals(sprint.getTree(sexpr, initial=True), expected)