# uncompyle6 version 3.6.7
# PyPy Python bytecode 3.5 (112)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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