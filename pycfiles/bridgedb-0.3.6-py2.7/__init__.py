# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/__init__.py
# Compiled at: 2015-11-05 10:40:17
from ._version import get_versions
from ._langs import get_langs
__version__ = get_versions()['version']
__langs__ = get_langs()
del get_versions
del get_langs