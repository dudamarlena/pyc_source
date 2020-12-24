# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/epics/test/test_epicsattribute.py
# Compiled at: 2019-08-19 15:09:29
"""Test for epicsattributes..."""
import os, sys, numpy, subprocess, unittest
from taurus.core.units import Quantity
import taurus
from taurus.test import insertTest, getResourcePath
from taurus.core.taurusbasetypes import DataType, AttrQuality, DataFormat
from taurus.core.taurusbasetypes import TaurusAttrValue

@insertTest(helper_name='write_read_attr', attrname='ca:test:a', setvalue=Quantity('1000mm'), expected=dict(rvalue=Quantity('1m'), type=DataType.Float, writable=True, data_format=DataFormat._0D, range=[
 Quantity('-10m'), Quantity('10m')], alarms=[
 None, None], warnings=[
 None, None]), expected_attrv=dict(rvalue=Quantity('1m'), wvalue=Quantity('1m'), quality=AttrQuality.ATTR_VALID, error=None))
@unittest.skipIf(('epics' in sys.modules) is False, 'epics module is not available')
class AttributeTestCase(unittest.TestCase):
    """TestCase for the taurus.Attribute helper"""
    _process = None

    @classmethod
    def setUpClass(cls):
        """Run the epics_test softIoc"""
        db_name = getResourcePath('taurus.core.epics.test.res', 'epics_test.db')
        args = ['softIoc', '-m', 'INST=test', '-d', db_name]
        dev_null = open(os.devnull, 'wb')
        cls._process = subprocess.Popen(args, stdout=dev_null, stderr=dev_null)

    @classmethod
    def tearDownClass(cls):
        """Terminate the epics_test softIoc process"""
        if cls._process:
            cls._process.terminate()
        else:
            taurus.warning('Process not started, cannot terminate it.')

    def write_read_attr(self, attrname=None, setvalue=None, expected=None, expected_attrv=None, expectedshape=None):
        """check creation and correct write-and-read of an attribute"""
        if expected is None:
            expected = {}
        if expected_attrv is None:
            expected_attrv = {}
        a = taurus.Attribute(attrname)
        if setvalue is None:
            read_value = a.read(cache=False)
        else:
            read_value = a.write(setvalue, with_read=True)
        msg = 'read() for "%s" did not return a TaurusAttrValue (got a %s)' % (
         attrname, read_value.__class__.__name__)
        self.assertTrue(isinstance(read_value, TaurusAttrValue), msg)
        for k, exp in expected.items():
            try:
                got = getattr(a, k)
            except AttributeError:
                msg = 'The attribute, "%s" does not provide info on %s' % (
                 attrname, k)
                self.fail(msg)

            msg = '%s for "%s" should be %r (got %r)' % (
             k, attrname, exp, got)
            self.__assertValidValue(exp, got, msg)

        for k, exp in expected_attrv.items():
            try:
                got = getattr(read_value, k)
            except AttributeError:
                msg = 'The read value for "%s" does not provide info on %s' % (
                 attrname, k)
                self.fail(msg)

            msg = '%s for the value of %s should be %r (got %r)' % (
             k, attrname, exp, got)
            self.__assertValidValue(exp, got, msg)

        if expectedshape is not None:
            msg = 'rvalue.shape for %s should be %r (got %r)' % (
             attrname, expectedshape, read_value.rvalue.shape)
            self.assertEqual(read_value.rvalue.shape, expectedshape, msg)
        return

    def __assertValidValue(self, exp, got, msg):
        if isinstance(got, Quantity):
            got = got.to(Quantity(exp).units).magnitude
        if isinstance(exp, Quantity):
            exp = exp.magnitude
        try:
            chk = numpy.allclose(got, exp)
        except:
            if isinstance(got, numpy.ndarray):
                chk = got.tolist() == exp.tolist()
            else:
                chk = bool(got == exp)

        self.assertTrue(chk, msg)