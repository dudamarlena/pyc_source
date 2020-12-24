# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevozodb/test/test_zodb_backend.py
# Compiled at: 2008-01-19 12:50:27
"""Run tests against durus backend.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo.test.library import storage_classes
locals().update(storage_classes(class_label='zodb-1', backend_name='zodb', format=1))
locals().update(storage_classes(class_label='zodb-2', backend_name='zodb', format=2))
optimize.bind_all(sys.modules[__name__])