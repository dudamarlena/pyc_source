# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/z3cform/kss/tests/test_all.py
# Compiled at: 2008-06-20 10:10:10
__doc__ = '\ncollective.z3cform.kss\n\nLicensed under the GPL license, see LICENCE.txt for more details.\nCopyright by Affinitic sprl\n\n$Id: test_all.py 66966 2008-06-19 16:22:57Z jfroche $\n'
import unittest
from zope.testing import doctest, cleanup
from Products.Five import zcml
import Products.Five, kss.core, kss.core.tests, plone.app.kss, plone.app.form, collective.z3cform.kss, z3c.form
optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

def setUp(test):
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('meta.zcml', kss.core)
    zcml.load_config('configure.zcml', kss.core)
    zcml.load_config('configure-unittest.zcml', kss.core.tests)
    zcml.load_config('configure.zcml', plone.app.form)
    zcml.load_config('configure.zcml', plone.app.kss)
    zcml.load_config('meta.zcml', z3c.form)
    zcml.load_config('configure.zcml', z3c.form)
    zcml.load_config('configure.zcml', collective.z3cform.kss)


def tearDown(test):
    cleanup.cleanUp()


def test_suite():
    return unittest.TestSuite([doctest.DocFileSuite('README.txt', package='collective.z3cform.kss', setUp=setUp, tearDown=tearDown, optionflags=optionflags)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')