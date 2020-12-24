# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_globals.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 1555 bytes
import pytest
from mediagoblin import mg_globals

class TestGlobals(object):

    def setup(self):
        self.old_database = mg_globals.database

    def teardown(self):
        mg_globals.database = self.old_database

    def test_setup_globals(self):
        mg_globals.setup_globals(database='my favorite database!', public_store='my favorite public_store!', queue_store='my favorite queue_store!')
        assert mg_globals.database == 'my favorite database!'
        assert mg_globals.public_store == 'my favorite public_store!'
        assert mg_globals.queue_store == 'my favorite queue_store!'
        pytest.raises(AssertionError, mg_globals.setup_globals, no_such_global_foo='Dummy')