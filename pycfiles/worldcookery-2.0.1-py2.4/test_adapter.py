# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/ftests/test_adapter.py
# Compiled at: 2006-09-21 05:27:38
import unittest
from zope.i18n import translate
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.simpletranslationdomain import SimpleTranslationDomain
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('worldcookery_test')
from zope.publisher.browser import BrowserPage
from zope.app.testing.functional import BrowserTestCase
messages = {('es', 'msg'): 'Eso es un mensaje', ('de', 'msg'): 'Dies ist eine Nachricht'}
wc_test = SimpleTranslationDomain('worldcookery_test', messages)

class TestPage(BrowserPage):
    __module__ = __name__

    def __call__(self):
        msg = _('msg', 'This is a message')
        return translate(msg, context=self.request)


class LanguageAdapterTestCase(BrowserTestCase):
    __module__ = __name__

    def test_default(self):
        response = self.publish('/@@testpage')
        self.assertEqual(response.getBody(), 'This is a message')

    def test_http_header(self):
        response = self.publish('/@@testpage', env={'HTTP_ACCEPT_LANGUAGE': 'de'})
        self.assertEqual(response.getBody(), 'Dies ist eine Nachricht')

    def test_browser_form(self):
        response = self.publish('/@@testpage', form={'ZopeLanguage': 'es'})
        self.assertEqual(response.getBody(), 'Eso es un mensaje')

    def test_form_overrides_header(self):
        response = self.publish('/@@testpage', form={'ZopeLanguage': 'es'}, env={'HTTP_ACCEPT_LANGUAGE': 'de'})
        self.assertEqual(response.getBody(), 'Eso es un mensaje')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LanguageAdapterTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()