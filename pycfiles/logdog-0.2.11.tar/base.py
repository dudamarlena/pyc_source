# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/viewers/base.py
# Compiled at: 2015-04-04 17:41:32
from __future__ import absolute_import, unicode_literals
import logging
from logdog.core.base_role import BaseRole
logger = logging.getLogger(__name__)

class BaseViewer(BaseRole):

    def on_recv(self, data):
        logger.debug(data)