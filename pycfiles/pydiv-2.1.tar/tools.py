# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/command/tools.py
# Compiled at: 2016-03-07 14:40:46
__doc__ = '\nUtility commands.\n'
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