# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/parsers/regex.py
# Compiled at: 2015-04-04 17:40:27
from __future__ import absolute_import, unicode_literals
import re
from .base import BaseParser

class Regex(BaseParser):
    defaults = BaseParser.defaults.copy_and_update(regex=b'')

    def __init__(self, *args, **kwargs):
        super(Regex, self).__init__(*args, **kwargs)
        self.re = re.compile(self.config.regex)

    def __str__(self):
        return b'REGEX-EXTRACTOR'

    def on_recv(self, data):
        match = self.re.search(data.message)
        if match:
            data.update_meta(match.groupdict())
        return self.output.send(data)