# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/test_cli.py
# Compiled at: 2015-11-08 18:30:19
import mock
from tvrenamer import cli
from tvrenamer.tests import base

class CliTest(base.BaseTest):

    def test_cli(self):
        with mock.patch.object(cli.service, 'prepare_service'):
            with mock.patch.object(cli.manager, 'run', return_value={}):
                rv = cli.main()
                self.assertEqual(rv, 0)