# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylogo/common.py
# Compiled at: 2007-10-14 14:35:26


class LogoError(Exception):
    """
    A generic Logo error.  It tracks file position and some
    of the (Logo) traceback.
    """
    __module__ = __name__

    def __init__(self, *args, **kw):
        Exception.__init__(self, *args)
        if 'tokenizer' in kw:
            tokenizer = kw.pop('tokenizer')
        else:
            tokenizer = None
        self.kw = kw
        if tokenizer is not None:
            self.set_tokenizer(tokenizer)
        self.msg = (' ').join(args)
        self.frame = None
        if 'description' in kw:
            self.description = kw['description']
        return

    def set_frame(self, frame):
        if self.frame:
            return
        self.frame = frame
        self.stack = [FrozenFrame(frame, frame.tokenizer, row=self.kw.get('row'), col=self.kw.get('col'))]
        self._traceback_initialized = False
        self.initialize_traceback()

    def initialize_traceback(self):
        frame = self.frame
        tokenizers = frame.tokenizers[:-1]
        while 1:
            if not tokenizers:
                if frame.root is frame:
                    break
                frame = frame.parent
                tokenizers = frame.tokenizers
                continue
            self.stack.append(FrozenFrame(frame, tokenizers[(-1)]))
            tokenizers = tokenizers[:-1]

        self._traceback_initialized = True
        self.stack.reverse()

    def traceback(self):
        return ('').join([ str(f) for f in self.stack ])

    def __str__(self):
        s = '\n'
        s += self.traceback()
        s += self.description + ': ' + Exception.__str__(self)
        return s


class FrozenFrame:
    __module__ = __name__

    def __init__(self, frame, tokenizer, row=None, col=None, pos=None):
        self.frame = frame
        self.tokenizer = tokenizer
        if hasattr(tokenizer, 'list'):
            self.file = None
            self.list = tokenizer.list
            self.pos = pos
            if self.pos is None:
                try:
                    self.pos = self.tokenizer.pos - len(self.tokenizer.peeked)
                except AttributeError:
                    pass

        elif hasattr(tokenizer, 'file'):
            self.list = None
            self.file = tokenizer.file
            self.row = row
            self.col = col
            if self.row is None:
                try:
                    self.row = self.file.row
                except AttributeError:
                    pass

            if self.col is None:
                try:
                    self.col = self.file.col
                except AttributeError:
                    pass

        else:
            assert 0, 'Unknown tokenizer: %r' % tokenizer
        return

    def __repr__(self):
        if self.file:
            return '<FrozenFrame %x in %s:%s:%s>' % (id(self), self.file.name, self.row, self.col)
        elif self.list is not None:
            return '<FrozenFrame %x for %r>' % (id(self), self.list)
        else:
            assert 0, 'Unknown frame/tokenizer type'
        return

    def __str__(self):
        if self.file:
            return error_for_file(self.file, self.row, self.col)
        elif self.list is not None:
            return error_for_list(self.list, self.pos)
        else:
            assert 0, 'Unknown frame/tokenizer type'
        return


def error_for_file(errorFile, row=None, col=None):
    try:
        name = errorFile.name
    except AttributeError:
        name = '<string>'

    if row is not None:
        try:
            row = errorFile.row
        except AttributeError:
            pass

    if not col:
        try:
            col = errorFile.col
        except AttributeError:
            pass

    if row is not None:
        s = 'File %s, line %i\n' % (name, row)
        l = errorFile.row_line(row)
        if l is not None:
            s += l
            s += '%s^\n' % (' ' * col)
    else:
        s = 'File %s\n' % name
    return s


def error_for_list(lst, pos=None):
    try:
        f = lst.sourceList
        s = error_for_file(f) + '\n'
    except AttributeError:
        s = ''

    if pos is not None:
        segment = '[' + (' ').join(map(str, lst[:pos]))
        segment = segment.split('\n')[(-1)]
        rest = (' ').join(map(str, lst[pos:])) + ']'
        rest = rest.split('\n')[0]
        s += segment + ' ' + rest + '\n'
        s += ' ' * len(segment) + '^\n'
    else:
        s += repr(lst) + '\n'
    return s


class LogoSyntaxError(LogoError):
    __module__ = __name__
    description = 'Syntax error'


class LogoNameError(LogoError):
    __module__ = __name__
    description = 'Name not found error'


class LogoUndefinedError(LogoNameError):
    __module__ = __name__
    description = 'Function undefined error'


class LogoEndOfLine(LogoError):
    __module__ = __name__
    description = 'Unexpected end of line error'


class LogoEndOfCode(LogoError):
    __module__ = __name__
    description = 'Unexpected end of code block error'


class LogoList(list):
    __module__ = __name__

    def __init__(self, body=None, source_file=None):
        if body is None:
            body = []
        list.__init__(self, body)
        self.file = source_file
        return


class LogoControl(Exception):
    __module__ = __name__


class LogoOutput(LogoControl):
    __module__ = __name__

    def __init__(self, value):
        self.value = value
        Exception.__init__(self)


class LogoContinue(LogoControl):
    __module__ = __name__


class LogoBreak(LogoControl):
    __module__ = __name__


class _EOF:
    __module__ = __name__

    def __repr__(self):
        return '[EOF]'


EOF = _EOF()

def logofunc(name=None, aliases=None, aware=False, arity=None, hide=False):

    def decorator(func):
        func.logo_expose = True
        if name is not None:
            func.logo_name = name
        if arity is not None:
            func.arity = arity
        if aliases is not None:
            func.aliases = aliases
        if aware:
            func.logo_aware = aware
        if hide:
            func.logo_hide = hide
        return func

    return decorator