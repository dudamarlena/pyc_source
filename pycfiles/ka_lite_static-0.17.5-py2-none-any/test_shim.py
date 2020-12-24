# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/test_shim.py
# Compiled at: 2018-07-11 18:15:31
"""
This file is needed as 1.6 only finds tests in files labelled test_*,
and ignores tests/__init__.py.
"""
from south.tests import *