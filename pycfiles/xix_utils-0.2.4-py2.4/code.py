# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/code.py
# Compiled at: 2006-03-02 13:59:00
"""code ...
"""
from xix.utils.comp.interface import implements
from xux.utils.interfaces import ICodeRunner
import warnings, commands
__author__ = 'Drew Smathers'
__revision__ = '$Revision$'
__contact__ = 'drew.smathers@gmail.com'
__license__ = 'MIT'
warnings.warn('xix.utils.code module is pre-alpha/unstable')

class CodeRunner(ICodeRunner):
    __module__ = __name__
    implements(ICodeRunner)

    def run(self, code):
        pass


class CommandRunner(CodeRunner):
    __module__ = __name__

    def run(self, command):
        return commands.getstatusoutput(command)