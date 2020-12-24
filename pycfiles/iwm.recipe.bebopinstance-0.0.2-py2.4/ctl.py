# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iwm/recipe/bebopinstance/ctl.py
# Compiled at: 2007-07-16 10:35:40
"""Top-level controller for 'zopectl'.
"""
import os, zdaemon.zdctl

class ZopectlCmd(zdaemon.zdctl.ZDCmd):
    __module__ = __name__

    def do_debug(self, rest):
        os.system(self._debugzope)

    def help_debug(self):
        print 'debug -- Initialize the Zope application, providing a'
        print '         debugger object at an interactive Python prompt.'

    def do_run(self, arg):
        os.system(self._scriptzope + ' ' + arg)

    def help_run(self):
        print 'run <script> [args] -- run a Python script with the Zope '
        print '                       environment set up.  The script has '
        print "                       'root' exposed as the root container."


def main(debugzope, scriptzope, args):

    class Cmd(ZopectlCmd):
        __module__ = __name__
        _debugzope = debugzope
        _scriptzope = scriptzope

    zdaemon.zdctl.main(args, None, Cmd)
    return