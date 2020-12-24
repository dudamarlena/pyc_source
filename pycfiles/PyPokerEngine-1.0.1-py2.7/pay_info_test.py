# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/pypokerengine/engine/pay_info_test.py
# Compiled at: 2016-11-22 02:08:34
from tests.base_unittest import BaseUnitTest
from pypokerengine.engine.pay_info import PayInfo

class PayInfoTest(BaseUnitTest):

    def setUp(self):
        self.info = PayInfo()

    def test_update_by_pay(self):
        self.info.update_by_pay(10)
        self.eq(10, self.info.amount)
        self.eq(PayInfo.PAY_TILL_END, self.info.status)

    def test_update_by_allin(self):
        self.info.update_to_allin()
        self.eq(0, self.info.amount)
        self.eq(PayInfo.ALLIN, self.info.status)

    def test_update_to_fold(self):
        self.info.update_to_fold()
        self.eq(0, self.info.amount)
        self.eq(PayInfo.FOLDED, self.info.status)

    def test_serialization(self):
        self.info.update_by_pay(100)
        self.info.update_to_allin()
        serial = self.info.serialize()
        restored = PayInfo.deserialize(serial)
        self.eq(100, restored.amount)
        self.eq(PayInfo.ALLIN, restored.status)