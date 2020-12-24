# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/titi/aha/pythonpath/eagexp/airwires.py
# Compiled at: 2012-12-03 07:11:00
from eagexp.cmd import command_eagle
from path import path
import tempfile
ulp_templ = '\nint count=0;\n\nif (board) {\n    board(B) {\n        B.signals(S) {\n            S.wires(W) {\n                if (W.layer == 19) {\n                    count++;\n                }\n            }\n        }\n    }\n  output("FILE_NAME", "wt")\n  {\n    printf("%d\\n", count);\n  };\n}\n'

def airwires(board, showgui=0):
    """search for airwires in eagle board"""
    board = path(board).expand().abspath()
    file_out = tempfile.NamedTemporaryFile(suffix='.txt', delete=0)
    file_out.close()
    ulp = ulp_templ.replace('FILE_NAME', file_out.name)
    file_ulp = tempfile.NamedTemporaryFile(suffix='.ulp', delete=0)
    file_ulp.write(ulp)
    file_ulp.close()
    commands = [
     'run ' + file_ulp.name,
     'quit']
    command_eagle(board, commands=commands, showgui=showgui)
    n = int(path(file_out.name).text())
    path(file_out.name).remove()
    path(file_ulp.name).remove()
    return n