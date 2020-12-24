# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/viewers/null.py
# Compiled at: 2015-04-04 17:41:25
from __future__ import absolute_import, unicode_literals
from .base import BaseViewer

class Null(BaseViewer):

    def _input_forwarder(self, data):
        pass

    on_recv = _input_forwarder