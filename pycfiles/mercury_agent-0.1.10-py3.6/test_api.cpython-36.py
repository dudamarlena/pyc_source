# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/raid_abstraction/test_api.py
# Compiled at: 2018-03-02 13:43:50
# Size of source mod 2**32: 6079 bytes
import json, os
from mercury_agent.hardware.raid.abstraction.api import RAIDAbstractionException, RAIDActions
from ..base import MercuryAgentUnitTest

class DummyImplementation(RAIDActions):

    def __init__(self):
        super(DummyImplementation, self).__init__()
        with open(os.path.join(os.path.dirname(__file__), '../resources/dummy.json')) as (fp):
            self.dummy_data = json.load(fp)

    def transform_adapter_info(self, adapter_index):
        try:
            return self.dummy_data[adapter_index]
        except IndexError:
            raise RAIDAbstractionException('...')

    def create(self, adapter, level, drives=None, size=None, array=None):
        return True

    def delete_logical_drive(self, adapter, array, ld):
        return True

    def clear_configuration(self, adapter):
        return True

    def add_spares(self, adapter, drives, arrays=None):
        return True

    @staticmethod
    def sort_drives(drives):
        drives.sort(key=(lambda x: '{}-{:05}-{:05}'.format(x['extra']['port'], int(x['extra']['box']), int(x['extra']['bay']))))


class MercuryRAIDAbstractionAPITest(MercuryAgentUnitTest):

    def setUp(self):
        super(MercuryRAIDAbstractionAPITest, self).setUp()
        self.dummy = DummyImplementation()
        self.abstract = RAIDActions()

    def test_raid_calc(self):
        _calc = self.dummy.raid_calculator
        tests = [
         dict(level='0', number=1, size=300, result=300),
         dict(level='1', number=2, size=300, result=300),
         dict(level='5', number=3, size=300, result=600),
         dict(level='6', number=6, size=300, result=1200),
         dict(level='10', number=4, size=300, result=600),
         dict(level='1+0', number=4, size=300, result=600),
         dict(level='50', number=6, size=300, result=1200),
         dict(level='60', number=8, size=300, result=1200)]
        for test in tests:
            assert _calc(test['level'], test['number'], test['size']) == test['result']

        (self.assertRaises)(RAIDAbstractionException, _calc, *('20', 0, 0, 0))

    def test_raid_minimums(self):
        _min = self.dummy.raid_minimums
        tests = [
         dict(level='1', _pass=2, fail=1),
         dict(level='5', _pass=3, fail=2),
         dict(level='6', _pass=4, fail=3),
         dict(level='10', _pass=4, fail=7),
         dict(level='1+0', _pass=4, fail=3),
         dict(level='50', _pass=6, fail=5),
         dict(level='60', _pass=8, fail=7)]
        for test in tests:
            self.assertEqual(_min(test['level'], test['_pass']), None)

        for test in tests:
            (self.assertRaises)(RAIDAbstractionException, _min, *(test['level'], test['fail']))

        (self.assertRaises)(RAIDAbstractionException, _min, *('60', 11))

    def test_create(self):
        if not self.dummy.create_logical_drive(adapter=0, level='0', drives='9, 10', size='10GiB'):
            raise AssertionError
        else:
            if not self.dummy.create_logical_drive(adapter=0, level='0', drives='9-11', size='10%FREE'):
                raise AssertionError
            else:
                assert self.dummy.create_logical_drive(adapter=0, level='0', drives=9)
                assert self.dummy.create_logical_drive(adapter=0, level='0', drives=[9, 10, 11])
            assert self.dummy.create_logical_drive(adapter=0, level='0', array=0, size='10%FREE')
        test_exception_args = [
         (0, '0', '9, 10', '100TiB'),
         (0, '0'),
         (0, '0', None, '10GiB', 100),
         (1, '0', None, '1MiB', 0),
         (0, '0', None, '100TiB', 0),
         (0, '0', None, '100%', 0),
         (0, '0', '11-9', None, None),
         (0, '0', '9-XXX', None, None),
         (0, '0', '9_10', None, None),
         (0, '0', '9-10-11', None, None),
         (0, '0', 'all', None, None),
         (0, '0', 'unassigned', None, None)]
        for args in test_exception_args:
            (self.assertRaises)(RAIDAbstractionException, self.dummy.create_logical_drive, *args)

    def test_abstract(self):
        (self.assertRaises)(NotImplementedError, self.abstract.transform_adapter_info, *(0, ))
        (self.assertRaises)(NotImplementedError, self.abstract.create, *(0, 0))
        (self.assertRaises)(NotImplementedError, self.abstract.delete_logical_drive, *(0,
                                                                                       0,
                                                                                       0))
        (self.assertRaises)(NotImplementedError, self.abstract.clear_configuration, *(0, ))
        (self.assertRaises)(NotImplementedError, self.abstract.add_spares, *(0, 0,
                                                                             None))
        self.abstract.sort_drives([0, 1, 2, 3])

    def test_get_drives(self):
        assert self.dummy.get_unassigned(0)
        (self.assertRaises)(RAIDAbstractionException, self.dummy.get_unassigned, *(100, ))

    def test_add_index(self):
        drives = self.dummy.get_all_drives(0)
        for idx in range(len(drives)):
            assert idx == drives[idx]['index']