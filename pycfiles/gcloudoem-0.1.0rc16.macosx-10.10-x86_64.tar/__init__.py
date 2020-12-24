# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/__init__.py
# Compiled at: 2015-04-20 22:18:08
from __future__ import absolute_import
from io import open
import os
from .datastore import credentials, connection, environment, utils, connect, query
from .entity import *
from .properties import *
version_file = open(os.path.join(os.path.dirname(__file__), 'VERSION'), encoding='utf-8')
VERSION = version_file.read().strip()
version_file.close()