# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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