# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/tests/functional/test_entries.py
# Compiled at: 2011-07-12 22:16:02
from weborg.tests import *

class TestEntriesController(TestController):

    def test_index(self):
        response = self.app.get(url('entries'))

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_entries', format='xml'))

    def test_create(self):
        response = self.app.post(url('entries'))

    def test_new(self):
        response = self.app.get(url('new_entry'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_new_entry', format='xml'))

    def test_update(self):
        response = self.app.put(url('entry', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('entry', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('entry', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('entry', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('entry', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_entry', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('edit_entry', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_edit_entry', id=1, format='xml'))