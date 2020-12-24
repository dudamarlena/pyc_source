# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/tests/unit/v1/contrib/test_list_extensions.py
# Compiled at: 2016-06-13 14:11:03
from vsmclient import extension
from vsmclient.v1.contrib import list_extensions
from vsmclient.tests.unit import utils
from vsmclient.tests.unit.v1 import fakes
extensions = [
 extension.Extension(list_extensions.__name__.split('.')[(-1)], list_extensions)]
cs = fakes.FakeClient(extensions=extensions)

class ListExtensionsTests(utils.TestCase):

    def test_list_extensions(self):
        all_exts = cs.list_extensions.show_all()
        cs.assert_called('GET', '/extensions')
        self.assertTrue(len(all_exts) > 0)
        for r in all_exts:
            self.assertTrue(len(r.summary) > 0)