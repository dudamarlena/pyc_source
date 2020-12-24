# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/test_cli.py
# Compiled at: 2015-06-14 13:30:57
import mock
from seedbox import cli
from seedbox import db
from seedbox.tests import test

class CliTestCase(test.ConfiguredBaseTestCase):

    def setUp(self):
        super(CliTestCase, self).setUp()
        self.patch(db, '_DBAPI', {})

    @mock.patch('seedbox.service.prepare_service')
    def test_cli(self, mock_service):
        self.assertIsNone(cli.main())