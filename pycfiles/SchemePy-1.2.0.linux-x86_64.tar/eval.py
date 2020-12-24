# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/eval.py
# Compiled at: 2015-09-06 09:35:26
from Queue import Empty
import cStringIO, parser, processer, utils
p = processer.processer

def Eval(obj, quotesExpanded=False, ccc=False):
    if isinstance(obj, (str, unicode)):
        obj = cStringIO.StringIO(obj)
    ast = parser.Parser(obj).ast
    try:
        ret = p.doProcess(ast, quotesExpanded=quotesExpanded, ccc=ccc)
    except Empty as e:
        ret = e.ret

    return ret


def Exec(ast):
    try:
        ret = p.doProcess(utils.deepcopy(ast))
    except Empty as e:
        ret = e.ret

    return ret