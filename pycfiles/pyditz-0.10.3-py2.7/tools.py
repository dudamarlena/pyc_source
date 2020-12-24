# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/command/tools.py
# Compiled at: 2016-03-07 14:40:46
"""
Utility commands.
"""
import os

class CmdTools(object):

    def do_ipython(self, arg):
        """ipython -- enter embedded IPython interpreter"""
        try:
            from IPython import embed
        except ImportError:
            self.error('IPython is not available')

        embed()

    def do_shell(self, arg):
        """shell -- run a system command"""
        os.system(arg)