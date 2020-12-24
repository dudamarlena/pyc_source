# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/pypokerengine/engine/pay_info.py
# Compiled at: 2016-06-11 01:57:21


class PayInfo:
    PAY_TILL_END = 0
    ALLIN = 1
    FOLDED = 2

    def __init__(self, amount=0, status=0):
        self.amount = amount
        self.status = status

    def update_by_pay(self, amount):
        self.amount += amount

    def update_to_fold(self):
        self.status = self.FOLDED

    def update_to_allin(self):
        self.status = self.ALLIN

    def serialize(self):
        return [
         self.amount, self.status]

    @classmethod
    def deserialize(self, serial):
        return self(amount=serial[0], status=serial[1])