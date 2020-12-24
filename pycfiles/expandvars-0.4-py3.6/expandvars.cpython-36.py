# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/expandvars.py
# Compiled at: 2019-06-21 23:49:45
# Size of source mod 2**32: 7460 bytes
from os import environ
__author__ = 'Arijit Basu'
__email__ = 'sayanarijit@gmail.com'
__homepage__ = 'https://github.com/sayanarijit/expandvars'
__description__ = 'Expand system variables Unix style'
__version__ = 'v0.4'
__license__ = 'MIT'
__all__ = ['Expander', 'expandvars']
ESCAPE_CHAR = '\\'

def _valid_char(char):
    return char.isalnum() or char == '_'


def _isint(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


class Expander(object):
    __doc__ = 'A class that helps expanding variables.\n\n    Params:\n        vars_ (str): System variables to expand\n\n    Example usage: ::\n\n        from expandvars import expandvars\n\n        print(Expander("$PATH:$HOME/bin:${SOME_UNDEFINED_PATH:-/default/path}").result)\n        # /bin:/sbin:/usr/bin:/usr/sbin:/home/you/bin:/default/path\n    '

    def __init__(self, vars_):
        self._result = []
        self._buffr = []
        self.escaping = False
        if len(vars_) == 0:
            return
        variter = iter(vars_)
        c = next(variter)
        if c == ESCAPE_CHAR:
            self.escape(variter)
            return
        if c == '$':
            self.expand_var(variter)
            return
        self.expand_val(variter, c)

    def _next_or_done(self, variter):
        """Returns the next character or None if iteration is done.
        
        Arguments:
            variter (list_iterator): Iterator of the variable being parsed.
        """
        try:
            return next(variter)
        except StopIteration:
            self.process_buffr()
            return

    def escape(self, variter):
        """Logic to escape characters.
        
        Arguments:
            variter (list_iterator): Iterator of the variable being parsed.
        """
        if self._buffr:
            self.process_buffr()
        else:
            try:
                c = next(variter)
            except StopIteration:
                raise ValueError('escape character is not escaping anything')

            if c == '$':
                self._result.append(c)
                c = self._next_or_done(variter)
            else:
                self._result.append(ESCAPE_CHAR)
        self.expand_val(variter, c)

    def process_buffr(self):
        """Process the expression or variable in the buffer."""
        if not self._buffr:
            return
        else:
            if ':' not in self._buffr:
                self._result.append(environ.get(''.join(self._buffr), ''))
                del self._buffr[:]
                return
            else:
                x, y = ''.join(self._buffr).split(':', 1)
                x, y = x.strip(), y.strip()
                if y.startswith('+'):
                    y = y[1:]
                    if x in environ:
                        self._result.append(y)
                    del self._buffr[:]
                    return
                if y.startswith('?'):
                    if x in environ:
                        self._result.append(environ[x])
                        del self._buffr[:]
                        return
                    err = y[1:]
                    if not err:
                        err = 'parameter null or not set'
                    raise ValueError('{}: {}'.format(x, err))
                if y.startswith('-') or y.startswith('='):
                    _y = y[0]
                    y = y[1:]
                    self._result.append(environ.get(x, y))
                    if _y == '=':
                        if x not in environ:
                            environ.update({x: y})
                    del self._buffr[:]
                    return
                if ':' not in y:
                    if not y:
                        raise ValueError('bad substitution')
                    if not y.isalnum():
                        raise ValueError('{}: syntax error: operand expected (error token is {})'.format(y, repr(y)))
                    if not _isint(y):
                        self._result.append(environ.get(x, ''))
                        del self._buffr[:]
                        return
                    else:
                        self._result.append(environ.get(x, '')[int(y):])
                        del self._buffr[:]
                        return
                y, z = y.split(':', 1)
                y, z = y.strip(), z.strip()
                if not z or z.isalpha():
                    del self._buffr[:]
                    return
                if not z.isalnum():
                    if not _isint(z):
                        raise ValueError('{}: syntax error: operand expected (error token is {})'.format(z, repr(z)))
                z = int(z)
                if z < 0:
                    raise ValueError('{}: substring expression < 0'.format(z))
            if not y or not y.isdigit():
                self._result.append(environ.get(x, '')[:z])
                del self._buffr[:]
                return
        y = int(y)
        self._result.append(environ.get(x, '')[y:y + z])
        del self._buffr[:]

    def expand_var(self, variter):
        """Continues the expansion of a variable.
        
        Arguments:
            variter (list_iterator): Iterator of the variable being parsed.
        """
        if self._buffr:
            self.process_buffr()
        else:
            c = self._next_or_done(variter)
            if not c:
                self._result.append('$')
                return
            if c == ESCAPE_CHAR:
                self.expand_val(variter, '$\\')
                return
            if c == '{':
                self.expand_modifier_var(variter)
                return
            while _valid_char(c):
                self._buffr.append(c)
                c = self._next_or_done(variter)
                if c == ESCAPE_CHAR:
                    self.escape(variter)
                    return
                if not c:
                    self.process_buffr()
                    return

            if c == '$':
                self.expand_var(variter)
                return
        self.expand_val(variter, c)

    def expand_modifier_var(self, variter):
        """Continues the expansion of a modifier variable.

        Arguments:
            variter (list_iterator): Iterator of the variable being parsed.
        """
        try:
            c = next(variter)
            while c != '}':
                self._buffr.append(c)
                c = next(variter)

        except StopIteration:
            raise ValueError('${{{}: {} was never closed.'.format(''.join(self._buffr), repr('{')))

        c = self._next_or_done(variter)
        if not c:
            self.process_buffr()
            return
        if c == '$':
            self.expand_var(variter)
            return
        self.expand_val(variter, c)

    def expand_val(self, variter, c):
        """Continues the expansion of a string.
        
        Arguments:
            variter (list_iterator): Iterator of the variable being parsed.
            c (str): the character to prepend if it's not "$".
        """
        if self._buffr:
            self.process_buffr()
        while c and c != '$':
            self._result.append(c)
            c = self._next_or_done(variter)
            if c == ESCAPE_CHAR:
                self.escape(variter)
                return

        if c:
            self.expand_var(variter)

    @property
    def result(self):
        return ''.join(self._result)


def expandvars(vars_):
    """Expand system variables Unix style.

    Params:
        vars_ (str): System variables to expand.

    Returns:
        str: Expanded values.

    Example usage: ::

        from expandvars import expandvars

        print(expandvars("$PATH:$HOME/bin:${SOME_UNDEFINED_PATH:-/default/path}"))
        # /bin:/sbin:/usr/bin:/usr/sbin:/home/you/bin:/default/path
    """
    return Expander(vars_).result