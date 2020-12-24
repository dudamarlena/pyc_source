# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/standalone/runtests.py
# Compiled at: 2010-02-28 14:01:23
"""
Test-Runner für die Tests gegen standalone
"""

def runtests():
    """
    The test runner for setup.py test usage. This sets up
    a memory database with sqlite3 and runs the tests via
    the django test command.
    """
    from conf import settings
    settings = settings(DATABASE_ENGINE='sqlite3', DATABASE_NAME=':memory:')
    from django.test.utils import get_runner
    test_runner = get_runner(settings)
    failures = test_runner([], verbosity=1, interactive=True)
    raise SystemExit(failures)