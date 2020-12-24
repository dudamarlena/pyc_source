# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifierlib/channels/stdout.py
# Compiled at: 2017-09-18 14:04:38
from notifierlib.notifierlib import Channel
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'plaintext'
__date__ = '18-09-2017'

class Stdout(Channel):
    """A simple library to print to stdout"""

    def __init__(self, name):
        self.name = name

    def notify(self, **kwargs):
        print ('Subject :{}').format(kwargs.get('subject'))
        print ('Message :{}').format(kwargs.get('message'))
        print ()
        return True