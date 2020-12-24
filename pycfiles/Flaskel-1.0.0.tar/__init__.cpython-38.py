# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Project\CLOUD\flaskel\skeleton\blueprints\__init__.py
# Compiled at: 2020-04-24 15:49:59
# Size of source mod 2**32: 224 bytes
from .api import api
from .web import web
from .spa import spa
BLUEPRINTS = (
 (
  api,),
 (
  spa,),
 (
  web,
  {'url_prefix': '/'}))