# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.5 (112)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/components/check.py
# Compiled at: 2017-12-02 07:21:41
# Size of source mod 2**32: 534 bytes
from cliez.component import Component
try:
    from shlex import quote as shell_quote
except ImportError:
    from pipes import quote as shell_quote

class CheckComponent(Component):

    def run(self, options):
        """
        plan feature

        we should check

        * only support centos or macosx
        * check pssh is installed

        :param options:
        :return:
        """
        pass