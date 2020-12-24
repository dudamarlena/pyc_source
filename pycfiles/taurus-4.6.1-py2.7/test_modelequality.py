# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/test/test_modelequality.py
# Compiled at: 2019-08-19 15:09:29
import unittest
from taurus.core.test.modelequality import TaurusModelEqualityTestCase, testDeviceModelEquality, testAttributeModelEquality
dev_models1 = [
 'tango:sys/tg_test/1',
 'tango:SYS/TG_TEST/1']
dev_models2 = [
 'tango:sys/tg_test/1',
 'tango:sys/database/2']
attr_models1 = [
 'tango:sys/tg_test/1/float_scalar',
 'tango:SYS/TG_TEST/1/FLOAT_SCALAR']
attr_models2 = [
 'tango:sys/tg_test/1/state',
 'tango:sys/database/2/state']
attr_models3 = [
 'tango:sys/tg_test/1/float_scalar#label',
 'tango:SYS/TG_TEST/1/FLOAT_SCALAR#LABEL']
attr_models4 = [
 'tango:sys/tg_test/1/state#label',
 'tango:sys/database/2/state#label']
attr_models5 = [
 'tango:sys/tg_test/1/float_scalar#label',
 'tango:SYS/TG_TEST/1/FLOAT_SCALAR#range']

@testAttributeModelEquality(models=attr_models1, equal=True)
@testDeviceModelEquality(models=dev_models1, equal=True)
@testAttributeModelEquality(models=attr_models3, equal=True)
@testAttributeModelEquality(models=attr_models2, equal=False)
@testDeviceModelEquality(models=dev_models2, equal=False)
@testAttributeModelEquality(models=attr_models4, equal=False)
@testAttributeModelEquality(models=attr_models5, equal=True)
class TangoModelEqualityTestCase(TaurusModelEqualityTestCase, unittest.TestCase):
    """TestCase class for tango model equality testing."""
    pass