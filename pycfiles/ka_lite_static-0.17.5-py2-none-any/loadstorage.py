# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/formtools/tests/wizard/loadstorage.py
# Compiled at: 2018-07-11 18:15:30
from django.test import TestCase
from django.contrib.formtools.wizard.storage import get_storage, MissingStorageModule, MissingStorageClass
from django.contrib.formtools.wizard.storage.base import BaseStorage

class TestLoadStorage(TestCase):

    def test_load_storage(self):
        self.assertEqual(type(get_storage('django.contrib.formtools.wizard.storage.base.BaseStorage', 'wizard1')), BaseStorage)

    def test_missing_module(self):
        self.assertRaises(MissingStorageModule, get_storage, 'django.contrib.formtools.wizard.storage.idontexist.IDontExistStorage', 'wizard1')

    def test_missing_class(self):
        self.assertRaises(MissingStorageClass, get_storage, 'django.contrib.formtools.wizard.storage.base.IDontExistStorage', 'wizard1')