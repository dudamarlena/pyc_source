# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/viewers/console.py
# Compiled at: 2015-04-04 17:41:22
from __future__ import absolute_import, unicode_literals
import logging, os, sys
from .base import BaseViewer
logger = logging.getLogger(__name__)

class Console(BaseViewer):
    defaults = BaseViewer.defaults.copy_and_update(redirect_to=b'stdout')

    def __init__(self, *args, **kwargs):
        super(Console, self).__init__(*args, **kwargs)
        self._output = getattr(sys, self.config.redirect_to)

    def _input_forwarder(self, data):
        sys.stdout.write(data.message)
        if not data.message.endswith(os.linesep):
            sys.stdout.write(os.linesep)

    on_recv = _input_forwarder