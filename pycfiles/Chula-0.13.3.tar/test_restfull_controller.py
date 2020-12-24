# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmcfarlane/dev/Chula/tests/bat/test_restfull_controller.py
# Compiled at: 2011-07-29 02:37:04
import os
from chula.test import bat

class Test_restfull_controller(bat.Bat):

    def test_uri_parsing(self):
        retval = self.request('/blog/jmcfarlane/2010-05-12/comments')
        if 'CHULA_REGEX_MAPPER' in os.environ:
            html = "blog: {'username': 'jmcfarlane', 'date': '2010-05-12', 'commens': 'comments'}"
            self.assertEquals(retval.data, html)
            self.assertEquals(retval.status, 200)
        else:
            self.assertTrue('404' in retval.data)
            self.assertEquals(retval.status, 404)