# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/tests/handlers/test_main.py
# Compiled at: 2012-09-09 20:09:24
import env_setup
env_setup.setup_tests()
env_setup.setup_django()
from agar.test import BaseTest, WebTest
import main

class MainTest(BaseTest, WebTest):
    APPLICATION = main.application

    def test_hello_world(self):
        response = self.get('/')
        self.assertOK(response)