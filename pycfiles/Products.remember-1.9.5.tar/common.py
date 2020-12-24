# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/common.py
# Compiled at: 2008-09-11 19:48:09
from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName
from Products.Relations.config import *
import os, sys
sys.path.append('%s/Products' % os.environ['INSTANCE_HOME'])
product_dependencies = [
 PROJECTNAME]

def installProducts():
    for product in product_dependencies:
        PloneTestCase.installProduct(product)


def installWithinPortal():
    from Products.Archetypes.tests import attestcase
    installProducts()
    PloneTestCase.setupPloneSite(products=product_dependencies)


def createObjects(testcase, names):
    """Given a testname and a list of portal types "names", I will create
    in testcase.folder objects that correspond to the given names, with their
    ids set to their type names.

    Returns the list of objects created."""
    value = []
    for t in names:
        testcase.folder.invokeFactory(t, t)
        obj = getattr(testcase.folder, t)
        value.append(obj)

    return value


def createRuleset(testcase, id):
    """Creates a ruleset and registers it. Returns the new ruleset."""
    ttool = getToolByName(testcase.portal, 'portal_types')
    construct = ttool.constructContent
    construct('Ruleset', testcase.folder, id)
    ruleset = getattr(testcase.folder, id)
    library = getToolByName(testcase.portal, RELATIONS_LIBRARY)
    library.registerRuleset(ruleset)
    return ruleset