# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/tales/pythonexpr.py
# Compiled at: 2007-12-02 16:26:58
"""Generic Python Expression Handler

$Id: pythonexpr.py 30451 2005-05-20 04:54:15Z fdrake $
"""

class PythonExpr(object):
    __module__ = __name__

    def __init__(self, name, expr, engine):
        text = ('\n').join(expr.splitlines())
        text = '(' + text + ')'
        self.text = text
        try:
            code = self._compile(text, '<string>')
        except SyntaxError, e:
            raise engine.getCompilerError()(str(e))

        self._code = code
        self._varnames = code.co_names

    def _compile(self, text, filename):
        return compile(text, filename, 'eval')

    def _bind_used_names(self, econtext, builtins):
        names = {}
        vars = econtext.vars
        marker = self
        if not isinstance(builtins, dict):
            builtins = builtins.__dict__
        for vname in self._varnames:
            val = vars.get(vname, marker)
            if val is not marker:
                names[vname] = val
            elif vname not in builtins:
                val = econtext._engine.getTypes().get(vname, marker)
                if val is not marker:
                    val = ExprTypeProxy(vname, val, econtext)
                    names[vname] = val

        names['__builtins__'] = builtins
        return names

    def __call__(self, econtext):
        __traceback_info__ = self.text
        vars = self._bind_used_names(econtext, __builtins__)
        return eval(self._code, vars)

    def __str__(self):
        return 'Python expression "%s"' % self.text

    def __repr__(self):
        return '<PythonExpr %s>' % self.text


class ExprTypeProxy(object):
    """Class that proxies access to an expression type handler"""
    __module__ = __name__

    def __init__(self, name, handler, econtext):
        self._name = name
        self._handler = handler
        self._econtext = econtext

    def __call__(self, text):
        return self._handler(self._name, text, self._econtext._engine)(self._econtext)


from salamoia.tests import *
runDocTests()