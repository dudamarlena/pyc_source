# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/c2/sample/csvworkflow/tests/base.py
# Compiled at: 2010-06-16 04:21:46
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
ztc.installProduct('SimpleAttachment')
ztc.installProduct('RichDocument')

@onsetup
def setup_optilux_policy():
    fiveconfigure.debug_mode = True
    import c2.sample.csvworkflow
    zcml.load_config('configure.zcml', c2.sample.csvworkflow)
    fiveconfigure.debug_mode = False
    ztc.installPackage('c2.sample.csvworkflow')


setup_optilux_policy()
ptc.setupPloneSite(products=['c2.sample.csvworkflow'])

class C2CsvworkflowTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """
    pass