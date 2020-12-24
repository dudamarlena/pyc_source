# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/ExcelFormula.py
# Compiled at: 2008-03-17 12:58:02
__rev_id__ = '$Id: ExcelFormula.py,v 1.3 2005/08/11 08:53:48 rvk Exp $'
import ExcelFormulaParser, ExcelFormulaLexer, struct
from antlr import ANTLRException

class Formula(object):
    __slots__ = [
     '__init__', 'text', 'rpn', '__s', '__parser']

    def __init__(self, s):
        try:
            self.__s = s
            lexer = ExcelFormulaLexer.Lexer(s)
            self.__parser = ExcelFormulaParser.Parser(lexer)
            self.__parser.formula()
        except ANTLRException:
            raise Exception, "can't parse formula " + s

    def text(self):
        return self.__s

    def rpn(self):
        """
        Offset    Size    Contents
        0         2       Size of the following formula data (sz)
        2         sz      Formula data (RPN token array)
        [2+sz]    var.    (optional) Additional data for specific tokens

        """
        return struct.pack('<H', len(self.__parser.rpn)) + self.__parser.rpn