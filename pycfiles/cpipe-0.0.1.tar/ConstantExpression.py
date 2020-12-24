# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/ConstantExpression.py
# Compiled at: 2017-10-03 13:07:15
__doc__ = 'Handles the Python interpretation of a constant-expression. See\n:title-reference:`ISO/IEC 14882:1998(E)`\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import logging, re
from cpip import ExceptionCpip

class ExceptionConstantExpression(ExceptionCpip):
    """Simple specialisation of an exception class for the ConstantExpression classes."""


class ExceptionConditionalExpressionInit(ExceptionConstantExpression):
    """Exception when initialising a ConstantExpression class."""


class ExceptionConditionalExpression(ExceptionConstantExpression):
    """Exception when conditional expression e.g. ... ? ... : ... fails to evaluate."""


class ExceptionEvaluateExpression(ExceptionConstantExpression):
    """Exception when conditional expression e.g. 1 < 2 fails to evaluate."""


class ConstantExpression(object):
    """Class that interpret a stream of pre-processing tokens
    (:py:class:`cpip.core.PpToken.PpToken` objects) and evaluate it as a constant expression.
    """
    RE_CONDITIONAL_EXPRESSION = re.compile('^(.+)\\?(.+):(.+)$')
    REPLACE_CONDITIONAL_EXPRESSION = 'if %s:\n  result = %s\nelse:\n  result = %s'

    def __init__(self, theTokTypeS):
        """Constructor takes a list pf PpToken."""
        self._tokTypeS = theTokTypeS[:]

    def __str__(self):
        return ('').join([ t.t for t in self._tokTypeS ])

    def translateTokensToString(self):
        """Returns a string to be evaluated as a constant-expression.
        
        :title-reference:`ISO/IEC ISO/IEC 14882:1998(E) 16.1 Conditional inclusion sub-section 4`
        i.e. 16.1-4
        
        All remaining identifiers and keywords 137) , except for true and
        false, are replaced with the pp-number 0"""
        return ('').join([ aTok.evalConstExpr() for aTok in self._tokTypeS ])

    def evaluate(self):
        """Evaluates the constant expression and returns 0 or 1."""
        s = self.translateTokensToString()
        m = self.RE_CONDITIONAL_EXPRESSION.match(s)
        if m is not None:
            return self._evaluateConditionalExpression(m)
        else:
            return self._evaluateExpression(s)

    def _evaluateConditionalExpression(self, theMatch):
        """Evaluates a conditional expression e.g. expr ? t : f
        Which we convert with a regular expression to: ::
            if exp:
                t
            else:
                f
        """
        assert theMatch is not None
        compileString = self.REPLACE_CONDITIONAL_EXPRESSION % (
         theMatch.group(1), theMatch.group(2), theMatch.group(3))
        try:
            _locals = {'result': None}
            c = compile(compileString, '<string>', 'exec')
            exec (
             c, {}, _locals)
            return _locals['result']
        except Exception as err:
            logging.error('ConstantExpression._evaluateConditionalExpression() can not evaluate: "%s"' % compileString)
            raise ExceptionConditionalExpression(str(err))

        return

    def _evaluateExpression(self, theStr):
        """Evaluates a conditional expression e.g. 1 < 2 """
        assert self.RE_CONDITIONAL_EXPRESSION.match(self.translateTokensToString()) is None
        try:
            return eval(theStr)
        except Exception as err:
            raise ExceptionEvaluateExpression('Evaluation of "%s" gives error: %s' % (theStr, str(err)))

        return