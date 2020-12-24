# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/__init__.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 357 bytes
import pytest, os
from firestore.db.connector import is_online
FIREBASE_PATH = os.path.abspath(os.path.join(os.path.expanduser('~'), '.ssh/mcr.json'))
IS_LOCAL_ENV = os.environ.get('FIRESTORE_CONFIG', False)
online = pytest.mark.skipif((not (is_online() and IS_LOCAL_ENV)),
  reason='Only run this test if internet connectivity is available')