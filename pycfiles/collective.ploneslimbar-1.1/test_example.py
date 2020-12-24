# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/ploneseltest/tests/test_example.py
# Compiled at: 2009-10-02 06:03:57
from Products.PloneTestCase import PloneTestCase as ptc
from collective.ploneseltest import SeleniumTestCase
ptc.setupPloneSite()

class ExampleTestCase(SeleniumTestCase):

    def afterSetUp(self):
        """Setup for each test
        """
        self.setRoles(['Manager'])
        self.login_user()

    def test_create_foo1(self):
        self.failIf(self.selenium.is_text_present('Foo'))
        self.selenium.click("//dl[@id='plone-contentmenu-factories']/dt/a/span[1]")
        self.selenium.click('document')
        self.wait()
        self.selenium.type('title', 'Foo')
        self.selenium.click('name=form_submit')
        self.wait()
        self.failUnless(self.selenium.is_text_present('Foo'))

    def test_create_foo2(self):
        self.failIf(self.selenium.is_text_present('Foo'))
        self.selenium.click("//dl[@id='plone-contentmenu-factories']/dt/a/span[1]")
        self.selenium.click('document')
        self.wait()
        self.selenium.type('title', 'Foo')
        self.selenium.click('name=form_submit')
        self.wait()
        self.failUnless(self.selenium.is_text_present('Foo'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ExampleTestCase))
    return suite