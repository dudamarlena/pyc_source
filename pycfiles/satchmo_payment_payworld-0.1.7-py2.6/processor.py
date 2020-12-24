# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/satchmo_payment_payworld/processor.py
# Compiled at: 2011-10-29 06:15:45
from payment.modules.base import HeadlessPaymentProcessor

class PaymentProcessor(HeadlessPaymentProcessor):

    def __init__(self, settings):
        super(PaymentProcessor, self).__init__('satchmo_payment_payworld', settings)