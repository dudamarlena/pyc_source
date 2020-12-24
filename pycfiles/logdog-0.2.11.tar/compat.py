# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/compat.py
# Compiled at: 2015-04-04 18:06:53
from logdog.core.utils.six import *
__all__ = [
 'import_object', 'text_type']
from tornado.util import import_object as _import_object
if PY2:
    import_object = lambda name: _import_object(str(name))
if PY3:
    import_object = _import_object