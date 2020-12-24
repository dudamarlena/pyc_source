# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/shaders/expression.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 2910 bytes
from ext.six import string_types
from .shader_object import ShaderObject

class Expression(ShaderObject):
    __doc__ = ' Base class for expressions (ShaderObjects that do not have a\n    definition nor dependencies)\n    '

    def definition(self, names):
        pass


class TextExpression(Expression):
    __doc__ = ' Plain GLSL text to insert inline\n    '

    def __init__(self, text):
        super(TextExpression, self).__init__()
        if not isinstance(text, string_types):
            raise TypeError('Argument must be string.')
        self._text = text

    def __repr__(self):
        return '<TextExpression %r for at 0x%x>' % (self.text, id(self))

    def expression(self, names=None):
        return self._text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t
        self.changed()

    def __eq__(self, a):
        if isinstance(a, TextExpression):
            return a._text == self._text
        if isinstance(a, string_types):
            return a == self._text
        return False

    def __hash__(self):
        return self._text.__hash__()


class FunctionCall(Expression):
    __doc__ = ' Representation of a call to a function\n    \n    Essentially this is container for a Function along with its signature. \n    '

    def __init__(self, function, args):
        from .function import Function
        super(FunctionCall, self).__init__()
        if not isinstance(function, Function):
            raise TypeError('FunctionCall needs a Function')
        sig_len = len(function.args)
        if len(args) != sig_len:
            raise TypeError('Function %s requires %d arguments (got %d)' % (
             function.name, sig_len, len(args)))
        sig = function.args
        self._function = function
        self._args = [ShaderObject.create(arg, ref=(sig[i][1])) for i, arg in enumerate(args)]
        self._add_dep(function)
        for arg in self._args:
            self._add_dep(arg)

    def __repr__(self):
        return '<FunctionCall of %r at 0x%x>' % (self.function.name, id(self))

    @property
    def function(self):
        return self._function

    @property
    def dtype(self):
        return self._function.rtype

    def expression(self, names):
        str_args = [arg.expression(names) for arg in self._args]
        args = ', '.join(str_args)
        fname = self.function.expression(names)
        return '%s(%s)' % (fname, args)