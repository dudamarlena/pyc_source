# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/behavior.localregistry/src/collective/behavior/localregistry/tests/test_setup.py
# Compiled at: 2014-03-12 09:52:17
from ..testing import COLLECTIVE_BEHAVIOR_LOCALREGISTRY_INTEGRATION_TESTING
from interlude import interact
from plone.testing import layered
from plone.testing import z2
from zope.interface import Interface
import doctest, pprint, unittest2 as unittest
TESTFILES = [
 (
  '../proxy.rst', COLLECTIVE_BEHAVIOR_LOCALREGISTRY_INTEGRATION_TESTING)]
optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
optionflags |= doctest.REPORT_ONLY_FIRST_FAILURE

class IMyDexterityContainer(Interface):
    """ Dexterity container
    """


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([ layered(doctest.DocFileSuite(docfile, globs={'interact': interact, 'pprint': pprint.pprint, 'z2': z2}, optionflags=optionflags), layer=layer) for docfile, layer in TESTFILES
                   ])
    return suite