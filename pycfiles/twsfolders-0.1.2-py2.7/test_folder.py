# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twsfolders/tests/test_folder.py
# Compiled at: 2014-07-10 09:02:09
import unittest
from twsfolders import Folder
from twsfolders.item import Item
from application import Application
from application import ApplicationService

class FolderTestCase(unittest.TestCase):

    def get_folders_three(self):
        application = Application(name='application')
        service1 = ApplicationService(application, name='service1')
        folder11 = Folder(service1, name='folder11')
        folder12 = Folder(folder11, name='folder11')
        Item(folder12, name='item13')
        service2 = ApplicationService(application, name='service2')
        folder21 = Folder(service2, name='folder21')
        folder22 = Folder(folder21, name='folder21')
        Item(folder22, name='item23')
        return application

    def test_url(self):
        application = self.get_folders_three()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()