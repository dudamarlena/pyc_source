# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfriszky/testest/env/lib/python3.6/site-packages/kontol/clis/base.py
# Compiled at: 2019-10-18 04:53:04
# Size of source mod 2**32: 430 bytes
from docopt import docopt

class Base(object):
    __doc__ = 'Base class for the commands'

    def __init__(self, options, command_args):
        """
        Initialize the commands.

        :param command_args: arguments of the command
        """
        self.options = options
        self.args = docopt((self.__doc__), argv=command_args)

    def execute(self):
        """Execute the commands"""
        raise NotImplementedError