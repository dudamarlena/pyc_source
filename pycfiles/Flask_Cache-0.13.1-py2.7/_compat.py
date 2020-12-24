# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_cache/_compat.py
# Compiled at: 2014-04-21 06:45:19
"""
    flask_cache._compat
    ~~~~~~~~~~~~~~~~~~~

    Some py2/py3 compatibility support based on a stripped down
    version of six so we don't have to depend on a specific version
    of it.

    :copyright: (c) 2013 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys
PY2 = sys.version_info[0] == 2
PYPY = hasattr(sys, 'pypy_translation_info')
if not PY2:
    range_type = range
else:
    range_type = xrange