# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/tests/functional/test_remote_server.py
# Compiled at: 2008-08-07 05:46:10
from divimon.tests import *

class TestServerController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='remote/server'))