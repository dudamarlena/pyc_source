# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/ploneformgen/readonlystringfield/tests/base.py
# Compiled at: 2009-03-24 10:51:59
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
ztc.installProduct('PloneFormGen')

@onsetup
def setup_package():
    import Products.PloneFormGen
    zcml.load_config('configure.zcml', Products.PloneFormGen)
    fiveconfigure.debug_mode = True
    import quintagroup.ploneformgen.readonlystringfield
    zcml.load_config('configure.zcml', quintagroup.ploneformgen.readonlystringfield)
    fiveconfigure.debug_mode = False
    ztc.installPackage('quintagroup.ploneformgen.readonlystringfield')


setup_package()
ptc.setupPloneSite(products=['quintagroup.ploneformgen.readonlystringfield'])

class ReadOnlyStringFieldTestCase(ptc.PloneTestCase):
    """Common test base class"""
    __module__ = __name__


class ReadOnlyStringFieldFunctionalTestCase(ptc.FunctionalTestCase):
    """Common functional test base class"""
    __module__ = __name__