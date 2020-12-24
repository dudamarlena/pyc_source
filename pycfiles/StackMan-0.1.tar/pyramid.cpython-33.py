# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/pyramid.py
# Compiled at: 2013-12-13 03:37:21
# Size of source mod 2**32: 556 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class Pyramid(StackItem):
    __doc__ = '\n    pserve kept deadlocking this, so we use gunicorn here insetad.\n\n    Arguments:\n    * config str Paste Configuration File\n                 Default: development.ini\n    * port int Port to bind to\n               Default: 6543\n    '
    ready_text = 'Listening'

    @property
    def command(self):
        command = 'gunicorn --paster ' + self.config
        command += ' -b 0.0.0.0:' + self.port
        return command