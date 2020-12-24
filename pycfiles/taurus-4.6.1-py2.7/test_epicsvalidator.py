# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/epics/test/test_epicsvalidator.py
# Compiled at: 2019-08-19 15:09:29
"""Test for taurus.core.epics.test.test_epicsvalidator..."""
__docformat__ = 'restructuredtext'
import sys, unittest
from taurus.core.test import valid, invalid, names, AbstractNameValidatorTestCase
from taurus.core.epics.epicsvalidator import EpicsAuthorityNameValidator, EpicsDeviceNameValidator, EpicsAttributeNameValidator

@valid(name='ca://', groups=dict(authority='//'))
@names(name='ca://', out=('ca://', '//', ''))
@names(name='epics://', out=('ca://', '//', ''))
@invalid(name='ca:')
@invalid(name='ca:/')
@invalid(name='ca:///')
@invalid(name='ca://a')
@unittest.skipIf(('epics' in sys.modules) is False, 'epics module is not available')
class EpicsAuthValidatorTestCase(AbstractNameValidatorTestCase, unittest.TestCase):
    validator = EpicsAuthorityNameValidator


@valid(name='ca:/', groups=dict(authority=None, devname='', path='/'))
@valid(name='epics:/', groups=dict(authority=None, devname='', path='/'))
@valid(name='ca:///', groups=dict(authority='//', devname='', path='/'))
@invalid(name='ca:')
@invalid(name='epics:')
@invalid(name='ca://')
@invalid(name='ca:foo')
@invalid(name='ca:/foo')
@invalid(name='ca:@foo')
@unittest.skipIf(('epics' in sys.modules) is False, 'epics module is not available')
class EpicsDevValidatorTestCase(AbstractNameValidatorTestCase, unittest.TestCase):
    validator = EpicsDeviceNameValidator


@valid(name='epics:XXX:sum', groups={'scheme': 'epics', 'authority': None, 
   'attrname': 'XXX:sum', 
   '__STRICT__': True, 
   'fragment': None})
@valid(name='ca:XXX:sum', groups={'scheme': 'ca', 'authority': None, 
   'attrname': 'XXX:sum', 
   '_field': None, 
   '__STRICT__': True, 
   'fragment': None})
@valid(name='ca:XXX:sum.RBV', groups={'scheme': 'ca', 'authority': None, 
   'attrname': 'XXX:sum.RBV', 
   '_field': 'RBV', 
   '__STRICT__': True, 
   'fragment': None})
@valid(name='ca:XXX:sum.rbv', groups={'scheme': 'ca', 'authority': None, 
   'attrname': 'XXX:sum.rbv', 
   '_field': None, 
   '__STRICT__': True, 
   'fragment': None})
@invalid(name='ca://XXX:sum')
@invalid(name='ca:///XXX:sum')
@valid(name='ca:a.B_c1;d:f-e[g]<h>#i', groups={'attrname': 'a.B_c1;d:f-e[g]<h>', '_field': None, 
   '__STRICT__': True, 
   'fragment': 'i'})
@invalid(name='ca:a$b')
@invalid(name='ca:a/b')
@invalid(name='ca:a\\b')
@invalid(name='ca:a%b')
@invalid(name='ca:a?b')
@invalid(name='ca://XXX:sum')
@invalid(name='ca://')
@valid(name='ca:1#')
@valid(name='ca:1#units', groups={'fragment': 'units'})
@valid(name='ca:a')
@names(name='ca:XXX:sum', out=('ca:XXX:sum', 'XXX:sum', 'XXX:sum'))
@unittest.skipIf(('epics' in sys.modules) is False, 'epics module is not available')
class EpicsAttrValidatorTestCase(AbstractNameValidatorTestCase, unittest.TestCase):
    validator = EpicsAttributeNameValidator