# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.6.0-i686/egg/tvdbapi_client/tests/test_options.py
# Compiled at: 2015-06-27 23:24:07
from tvdbapi_client import options
from tvdbapi_client.tests import base

class OptionsTest(base.BaseTest):

    def test_list_opts(self):
        self.assertIsNotNone(options.list_opts())