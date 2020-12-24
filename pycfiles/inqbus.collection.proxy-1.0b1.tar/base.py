# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/development/checkouts/inqbus.collection.proxy/inqbus/collection/proxy/tests/base.py
# Compiled at: 2011-05-30 09:47:18
"""Lets write some unit-tests...
"""
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and it depencies.

    First of all, to set up our package we musst be sure to install
    all depencies
    """
    fiveconfigure.debug_mode = True
    import inqbus.collection.proxy
    zcml.load_config('configure.zcml', inqbus.collection.proxy)
    fiveconfigure.debug_mode = False
    ztc.installPackage('inqbus.collection.proxy')


setup_product()
ptc.setupPloneSite(products=['inqbus.collection.proxy'])

class InqbusCollectionProxyTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """
    pass