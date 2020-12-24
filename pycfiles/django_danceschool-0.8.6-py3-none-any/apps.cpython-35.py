# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/apps.py
# Compiled at: 2018-03-26 19:55:32
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
            cvs = CustomerVoucher.objects.filter(**{'customer': customer, 
             'voucher__category': getConstant('referrals__referrerCategory')})
            return [cv.voucher for cv in cvs]

        Customer.add_to_class('getAvailableCredits', creditsAvailable)
        Customer.add_to_class('getVouchers', getCustomerVouchers)
        Customer.add_to_class('getReferralVouchers', getCustomerReferralVouchers)
        from . import handlers