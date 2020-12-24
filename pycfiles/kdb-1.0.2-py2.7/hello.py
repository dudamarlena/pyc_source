# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/hello.py
# Compiled at: 2014-04-26 09:00:59
"""hello Plugin"""
__version__ = '0.0.1'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from circuits import Component
from ..plugin import BasePlugin

class Commands(Component):
    channel = 'commands'

    def hello(self, source, target, args):
        """Say Hello.

        Syntax: HELLO [<message>]
        """
        if not args:
            message = 'World!'
        else:
            message = args
        return ('Hello {0:s}').format(message or 'World!')

    def say(self, source, target, args):
        """Say.

        Syntax: SAY <message>
        """
        if not args:
            return 'No message specified.'
        return args


class Hello(BasePlugin):
    """Hello Plugin"""

    def init(self, *args, **kwargs):
        super(Hello, self).init(*args, **kwargs)
        Commands().register(self)