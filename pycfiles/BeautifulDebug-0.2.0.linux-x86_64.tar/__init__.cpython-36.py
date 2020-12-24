# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cufrancis/Develop/BeautifulDebug/.env/lib/python3.6/site-packages/BeautifulDebug/__init__.py
# Compiled at: 2017-10-23 08:12:21
# Size of source mod 2**32: 137 bytes
version = '0.2.0'
from .utils import Dump
from .settings import Setting
setting = Setting()
dump = Dump(setting=setting).run