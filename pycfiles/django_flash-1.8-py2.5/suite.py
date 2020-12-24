# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/djangoflash/tests/suite.py
# Compiled at: 2011-01-28 16:01:34
"""Project's test suite.
"""
import sys
from django.core.management import setup_environ
import djangoflash.tests.testproj.settings as project_settings
sys.path.insert(0, setup_environ(project_settings))
from context_processors import *
from decorators import *
from models import *
from storage import *
from codec import *
has_sqlite = True
try:
    import sqlite3
except ImportError:
    try:
        import pysqlite2
        has_sqlite = True
    except ImportError:
        pass

if has_sqlite:
    import django.test.utils as test_utils
    from django.db import connection
    test_utils.setup_test_environment()
    connection.creation.create_test_db()
    from testproj.app.tests import *
else:
    print >> sys.stderr, 'Integration: module "sqlite3" (or "pysqlite2") is required... SKIPPED'