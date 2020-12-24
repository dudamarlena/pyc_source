# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/tests/test_config_handler.py
# Compiled at: 2014-01-14 07:49:27
# Size of source mod 2**32: 984 bytes
from unittest import TestCase
import os
from ploader.tests.environment_handler import *
import ploader.utils as utils

class TestExistingConfig(TestCase):

    def setUp(self):
        handle_cwd()
        self.config = './ploader.yaml'
        create_test_config(self.config)

    def tearDown(self):
        os.remove(self.config)

    def test_normal_loading(self):
        utils.set_config_path(self.config)
        settings = utils.load_config()
        self.assertEqual(settings['port'], 42424)
        self.assertEqual(settings['download-dir'], 'somewhere')
        self.assertEqual(settings['captcha-api-key'], 'foo')


class TestNonexistentConfig(TestCase):

    def setUp(self):
        handle_cwd()
        self.config = 'candybar.ploader'

    def tearDown(self):
        os.remove(self.config)

    def test_default_loading(self):
        utils.set_config_path(self.config)
        settings = utils.load_config()
        self.assertEqual(settings['port'], 50505)
        self.assertEqual(settings['download-dir'], 'downloads')
        self.assertEqual(settings['captcha-api-key'], 'xyz')