# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/tests/config.py
# Compiled at: 2017-03-15 09:46:43
from egnyte import configuration, client, exc
import unittest
CONFIG_NAME = 'test_config.json'
ROOT_FOLDER_PATH = '/Shared/test_python_sdk/'

class EgnyteTestCase(unittest.TestCase):

    def setUp(self):
        self.config = configuration.load(CONFIG_NAME)
        self.egnyte = client.EgnyteClient(self.config)
        self.root_folder = self.egnyte.folder(ROOT_FOLDER_PATH)

    def tearDown(self):
        self.egnyte.folder(ROOT_FOLDER_PATH).delete()
        self.egnyte.close()
        del self.egnyte