# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/qiita/__init__.py
# Compiled at: 2012-10-22 07:01:15
"""
    qiita
    ~~~~~

    Qiita api wrapper for Python.

    :copyright: (c) 2012 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
try:
    import simplejson as json
except:
    import json

from .client import Client
from .items import Items
from .users import Users
from .tags import Tags
__version__ = '0.1.1'
__all__ = ['json', 'Client', 'Items', 'Users', 'Tags']