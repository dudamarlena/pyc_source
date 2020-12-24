# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/tests/layer.py
# Compiled at: 2007-09-08 18:44:19
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase
from Products.Five import fiveconfigure
from Products.Five import zcml
from OFS.Application import install_package
import simplon.plone.currency

class SimplonPloneCurrency(PloneSite):
    __module__ = __name__

    @classmethod
    def setUp(cls):
        app = ZopeTestCase.app()
        install_package(app, simplon.plone.currency, None)
        ZopeTestCase.close(app)
        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml', simplon.plone.currency)
        fiveconfigure.debug_mode = False
        return

    @classmethod
    def tearDown(cls):
        pass