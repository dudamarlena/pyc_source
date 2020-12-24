# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/apps.py
# Compiled at: 2019-04-03 22:56:33
# Size of source mod 2**32: 1403 bytes
from django.apps import AppConfig

class VoucherAppConfig(AppConfig):
    name = 'danceschool.vouchers'
    verbose_name = 'Voucher Functions'

    def ready(self):
        from danceschool.core.models import Customer
        from danceschool.core.constants import getConstant
        from .models import CustomerVoucher

        def creditsAvailable(customer):
            cvs = CustomerVoucher.objects.filter(customer=customer)
            amount = 0
            for cv in cvs:
                amount += cv.voucher.amountLeft

            return amount

        def getCustomerVouchers(customer):
            cvs = CustomerVoucher.objects.filter(customer=customer)
            return [cv.voucher for cv in cvs]

        def getCustomerReferralVouchers(customer):
            cvs = (CustomerVoucher.objects.filter)(customer=customer, 
             voucher__category=getConstant('referrals__referrerCategory'))
            return [cv.voucher for cv in cvs]

        Customer.add_to_class('getAvailableCredits', creditsAvailable)
        Customer.add_to_class('getVouchers', getCustomerVouchers)
        Customer.add_to_class('getReferralVouchers', getCustomerReferralVouchers)
        from . import handlers