# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/__init__.py
# Compiled at: 2017-04-04 09:15:23
from __future__ import print_function, division, absolute_import
from __future__ import unicode_literals
from pkg_resources import get_distribution
__version__ = get_distribution(__name__).version
from orlo.config import config
from orlo.app import app
app.logger.info(b'Initialisation completed')