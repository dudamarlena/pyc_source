# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/processors/stripper.py
# Compiled at: 2015-04-04 17:41:04
from __future__ import absolute_import, unicode_literals
from .base import BaseProcessor

class Stripper(BaseProcessor):

    def __str__(self):
        return b'STRIPPER'

    def on_recv(self, data):
        data.update_message(data.message.strip())
        return self.output.send(data)