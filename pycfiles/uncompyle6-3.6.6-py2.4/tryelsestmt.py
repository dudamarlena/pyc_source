# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/reducecheck/tryelsestmt.py
# Compiled at: 2020-02-16 17:43:52
from uncompyle6.parsers.treenode import SyntaxTree

def tryelsestmt(self, lhs, n, rule, ast, tokens, first, last):
    except_handler = ast[3]
    if except_handler == 'except_handler_else':
        except_handler = except_handler[0]
    if except_handler == 'except_handler':
        come_from = except_handler[(-1)]
        if come_from == 'COME_FROM':
            first_come_from = except_handler[(-1)]
        elif come_from == 'END_FINALLY':
            return False
        else:
            assert come_from == 'come_froms'
            first_come_from = come_from[0]
        leading_jump = except_handler[0]
        if isinstance(leading_jump, SyntaxTree):
            except_handler_first_offset = leading_jump.first_child().off2int()
        else:
            except_handler_first_offset = leading_jump.off2int()
        return first_come_from.attr > except_handler_first_offset
    return False