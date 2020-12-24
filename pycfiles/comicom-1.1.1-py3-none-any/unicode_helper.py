# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/comicnamer/unicode_helper.py
# Compiled at: 2010-09-01 08:39:06
__doc__ = 'Helpers to deal with strings, unicode objects and terminal output\nModified from http://github.com/dbr/tvnamer\n'
import sys

def unicodify(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


def p(*args, **kw):
    """Rough implementation of the Python 3 print function,
    http://www.python.org/dev/peps/pep-3105/

    def print(*args, sep=' ', end='
', file=None)

    """
    kw.setdefault('encoding', 'utf-8')
    kw.setdefault('sep', ' ')
    kw.setdefault('end', '\n')
    kw.setdefault('file', sys.stdout)
    new_args = []
    for x in args:
        if not isinstance(x, basestring):
            new_args.append(repr(x))
        elif kw['encoding'] is not None:
            new_args.append(x.encode(kw['encoding']))
        else:
            new_args.append(x)

    out = kw['sep'].join(new_args)
    kw['file'].write(out + kw['end'])
    return