# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/common/test_tools.py
# Compiled at: 2015-11-08 18:30:19
from tvrenamer.common import tools
from tvrenamer.tests import base

class ToolsTest(base.BaseTest):

    def test_make_opt_list(self):
        group_name = 'test'
        options = ['x', 'y', 'z', 'v']
        results = tools.make_opt_list(options, group_name)
        self.assertEqual(results, [('test', ['x', 'y', 'z', 'v'])])