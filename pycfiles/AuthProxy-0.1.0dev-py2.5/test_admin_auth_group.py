# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/tests/functional/test_admin_auth_group.py
# Compiled at: 2005-08-12 03:08:20
from authproxy.tests import *

class TestAuthGroupController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='admin/auth_group'))