# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/formatters/fmtr.py
# Compiled at: 2015-04-04 17:44:17
from __future__ import absolute_import, unicode_literals
from .base import BaseFormatter

class Formatter(BaseFormatter):
    defaults = BaseFormatter.defaults.copy_and_update(format=b'{msg.source!s}: {msg.message!s}', format_meta_name=None)

    def __init__(self, *args, **kwargs):
        super(Formatter, self).__init__(*args, **kwargs)
        self.format = self.config.format
        self.format_meta_name = self.config.format_meta_name

    def __str__(self):
        return b'FORMATTER'

    def on_recv(self, data):
        msg = self.format.format(msg=data)
        if self.format_meta_name is not None:
            data.update_meta({self.format_meta_name: msg})
        else:
            data.update_message(msg)
        return self.output.send(data)