# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylispng/util/sprint.py
# Compiled at: 2008-11-09 14:06:31
from pylispng import lisp

def getTree(sexp, padding='', initial=False):
    """
    An s-expression printer.
    """
    out = ''
    indent = ' ' * 4
    for node in sexp:
        if isinstance(node, lisp.ListObject):
            out += getTree(node, padding + indent)
        else:
            type = lisp.get_type(node)
            if type == lisp.SymbolObject:
                out += padding + indent + '|--[' + str(node) + ']\n'
            else:
                prefix = '+--'
                if initial:
                    prefix = '   '
                out += padding + prefix + '[' + str(node) + ']\n'

    return out


def sprint(sexp):
    print '\n', getTree(sexp, initial=True)