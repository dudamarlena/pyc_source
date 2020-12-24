# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_i18n.py
# Compiled at: 2013-04-11 17:47:52
from camelot.test import ModelThreadTestCase
from PyQt4 import QtCore

class I18NTest(ModelThreadTestCase):

    def test_ugettext(self):
        from snippet.i18n.specify_translation_string import message
        self.assertTrue(message)

    def test_ugettext_lazy(self):
        from snippet.i18n.specify_lazy_translation_string import message
        self.assertTrue(message)

    def test_load_translators(self):
        from camelot.admin.application_admin import ApplicationAdmin
        app_admin = ApplicationAdmin()
        QtCore.QLocale.setDefault(QtCore.QLocale('pt_BR'))
        self.assertEqual(len(app_admin.get_translator()), 2)
        QtCore.QLocale.setDefault(QtCore.QLocale('nl_BE'))
        self.assertEqual(len(app_admin.get_translator()), 1)
        QtCore.QLocale.setDefault(QtCore.QLocale('pt'))
        self.assertEqual(len(app_admin.get_translator()), 1)