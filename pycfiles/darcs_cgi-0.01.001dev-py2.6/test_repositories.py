# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/darcscgi/tests/functional/test_repositories.py
# Compiled at: 2009-09-11 13:58:44
from darcscgi.tests import *

class TestRepositoriesController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='repositories', action='index'))