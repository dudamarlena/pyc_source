# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_model.py
# Compiled at: 2019-02-28 16:17:24
# Size of source mod 2**32: 4834 bytes
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from billjobs.models import Bill, Service
from billjobs.settings import BILLJOBS_BILL_ISSUER
from .factories import ServiceFactory, BillFactory, UserFactory
import datetime

class BillingTestCase(TestCase):
    __doc__ = ' Test billing creation and modification '
    fixtures = ['dev_model_010_user.yaml', 'dev_model_020_userprofile.yaml']

    def setUp(self):
        self.user = User.objects.get(username='bill')

    def test_create_bill(self):
        bill = Bill(user=(self.user))
        bill.save()
        self.assertEqual(bill.user.username, self.user.username)
        self.assertEqual(bill.issuer_address, BILLJOBS_BILL_ISSUER)
        self.assertEqual(bill.billing_address, self.user.userprofile.billing_address)

    def test_user_change_billing_address(self):
        """ Test when user is changing is billing address
            Previous bill is with old address
            New bill is with new address
        """
        bill = Bill(user=(self.user))
        previous_billing_address = self.user.userprofile.billing_address
        bill.save()
        self.user.userprofile.billing_address = '1 new street\n34000 Town'
        self.user.save()
        new_billing_address = self.user.userprofile.billing_address
        new_bill = Bill(user=(self.user))
        new_bill.save()
        self.assertEqual(bill.billing_address, previous_billing_address)
        self.assertEqual(new_bill.billing_address, new_billing_address)

    def test_save_bill_do_not_change_billing_address(self):
        """ Test when user change his billing address and modify an old bill
            it doesn't change the billing address
        """
        bill = Bill(user=(self.user))
        previous_billing_address = self.user.userprofile.billing_address
        bill.save()
        self.user.userprofile.billing_address = '1 new street\n34000 Town'
        self.user.save()
        bill.amount = 100
        bill.save()
        self.assertEqual(bill.billing_address, previous_billing_address)

    def test_bill_number_is_more_than_999(self):
        """ Test the bill number property could be more than 999 """
        for i in range(1100):
            bill = Bill(user=(self.user))
            bill.save()
            del bill

        last_bill = Bill.objects.order_by('id').last()
        today = datetime.date.today()
        last_number = 'F%s%s' % (today.strftime('%Y%m'), '1100')
        self.assertEqual(last_bill.number, last_number)

    def test_service_price_change_do_not_change_bill_line(self):
        """Test when admin change a service price

        Previous stored bills do not have to be impacted by price change
        """
        user = UserFactory()
        for i in range(0, 4):
            service = ServiceFactory()
            bill = BillFactory(user=user)
            bill.billline_set.create(service=service)
            self.assertEqual(bill.billline_set.first().total, service.price)
            service.price += 10
            service.save()
            self.assertNotEqual(bill.billline_set.first().total, service.price)

    def test_bill_number_as_no_limit(self):
        """ Test the bill number has no limit """
        user = UserFactory()
        numbers = (999, 2122, 13456, 123456, 999999)
        prefix = 'F{}'.format(datetime.date.today().strftime('%Y%m'))
        for number in numbers:
            BillFactory(user=user, number=('{}{}'.format(prefix, number)))
            BillFactory(user=user)
            last_bill = Bill.objects.order_by('id').last()
            self.assertEqual(last_bill.number, '{}{}'.format(prefix, number + 1))


class ServiceTestCase(TestCase):
    __doc__ = ' Test CRUD for Service model '

    def test_create_service_without_price_raise_constraint(self):
        service = Service()
        service.reference = 'TEST'
        service.name = 'Service test'
        with self.assertRaises(IntegrityError):
            service.save()