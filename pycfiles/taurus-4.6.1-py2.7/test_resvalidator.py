# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/resource/test/test_resvalidator.py
# Compiled at: 2019-08-19 15:09:29
"""Test for taurus.core.resource.test.test_resvalidator..."""
import os.path as osp, taurus
from taurus.core.taurusexception import TaurusException
import unittest
from taurus.core.test import valid, invalid, names, AbstractNameValidatorTestCase
from taurus.core.resource.resvalidator import ResourceAuthorityNameValidator, ResourceDeviceNameValidator, ResourceAttributeNameValidator

class _AbstractResNameValidatorTestCase(AbstractNameValidatorTestCase):
    """Abstract class for creating res validator test cases. Derived classes
    need to provide the `res_map` dictionary class member"""
    res_map = {}

    def setUp(self):
        unittest.TestCase.setUp(self)
        f = taurus.Factory('res')
        f.clear()
        f.loadResource(self.res_map)

    def tearDown(self):
        f = taurus.Factory('res')
        f.clear()


@valid(name='res:foo02')
@valid(name='res:localhost')
@invalid(name='res:foo:10000')
@invalid(name='res:10000')
@invalid(name='res:127.0.0.1')
@invalid(name='res:badtango_1', exceptionType=TaurusException)
class ResourceAuthorityValidatorTestCase(_AbstractResNameValidatorTestCase, unittest.TestCase):
    """
    Test for ResourceAuthorityNameValidator loading the resources
    from a dictionary.
    """
    validator = ResourceAuthorityNameValidator
    res_map = {'badtango_1': 'foo:10000', 'foo02': 'tango://foo:10000', 
       'localhost': 'eval://localhost'}


@valid(name='res:MyDev')
@valid(name='res:tangoDev1')
@valid(name='res:tangoDev_bck')
@invalid(name='res:123')
@invalid(name='res:wrong_dev')
class ResourceDeviceValidatorTestCase(_AbstractResNameValidatorTestCase, unittest.TestCase):
    """
    Test for ResourceDeviceNameValidator loading the resources
    from a dictionary.
    """
    validator = ResourceDeviceNameValidator
    res_map = {'MyDev': 'eval:@foo', 'tangoDev1': 'tango://foo:10000/a/b/c', 
       'tangoDev_bck': 'tango:a/b/c', 
       'wrong_dev': 'eval://mydev'}


@names(name='MyAttr', out=('eval://localhost/@DefaultEvaluator/1', '1', '1'))
@names(name='foo', out=('eval://localhost/@Foo/True', '@Foo/True', 'True'))
@valid(name='res:MyAttr')
@valid(name='res:My_Attr')
@valid(name='res:attr_1')
@valid(name='res:attr_2')
@invalid(name='res:attr_tango_bck_1')
@valid(name='res:attr_tango_bck_1', strict=False)
@valid(name='res:attr_tango_bck_2')
@valid(name='res:attr_state')
@valid(name='res:attr1')
@valid(name='res:foo')
@valid(name='res:Foo')
@valid(name='res:res_attr')
@invalid(name='res:1')
@invalid(name='res:1foo')
@invalid(name='res: foo')
@invalid(name='res:dev1')
@invalid(name='res:dev2')
@invalid(name='res:NotExist')
class ResourceAttributeValidatorTestCase(_AbstractResNameValidatorTestCase, unittest.TestCase):
    """
    Test for ResourceAttributeNameValidator loading the resources
    from a dictionary.
    """
    validator = ResourceAttributeNameValidator
    res_map = {'MyAttr': 'eval:1', 'My_Attr': 'eval:foo=1;bar=2;foo+bar', 
       'attr_1': 'tango:a/b/c/d', 
       'attr_2': 'a/b/c/d', 
       'attr_tango_bck_1': 'tango://a/b/c/d', 
       'attr_tango_bck_2': 'tango://foo:10000/a/b/c/d', 
       'attr_state': 'a/b/c/state', 
       'attr1': 'eval:"Hello_World!!"', 
       'foo': 'eval:/@Foo/True', 
       '1foo': 'eval:2', 
       'Foo': 'eval:False', 
       'res_attr': 'res:attr1', 
       'dev1': 'tango:a/b/c', 
       'dev2': 'eval:@foo'}