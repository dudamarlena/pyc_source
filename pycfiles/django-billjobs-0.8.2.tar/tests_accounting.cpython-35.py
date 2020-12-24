# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_accounting.py
# Compiled at: 2017-01-13 19:06:36
# Size of source mod 2**32: 5749 bytes
from django.test import TestCase, Client
from billjobs.models import UserProfile
from django.contrib.auth.models import User

class AccountingTestCase(TestCase):
    __doc__ = ' Test accounting module \n    last name less 6 len\n    test with de féligonde\n    last name more 6 len\n    last name with space\n    last name similar and produce same existing 6\n    '

    def setUp(self):
        for user in User.objects.all():
            base_id = user.id
            for i in range(0, 6):
                user.id = '%s%s' % (base_id, i)
                user.username = '%s%s' % (user.username, i)
                user.save()

    fixtures = [
     'accounting_tests.yaml']

    def get_create_number(self, user_id):
        """ Return number for a specific user """
        user = User.objects.get(pk=user_id)
        profile = UserProfile(user=user)
        profile.save()
        return profile.accounting_number

    def test_create_number_when_name_less_6(self):
        """ Test number is created with 6 char when name is less than 6 char """
        self.assertEqual(self.get_create_number(1), '01JOBS')

    def test_create_number_when_name_is_6(self):
        """ Test number is created with 8 chars when name is 6 chars """
        self.assertEqual(self.get_create_number(2), '01MARTIN')

    def test_create_number_when_name_more_6(self):
        """ Test number is created with 8 chars when name is more than 6 chars """
        self.assertEqual(self.get_create_number(3), '01LEFEBV')

    def test_create_number_when_name_is_composed(self):
        """ Test number is created with a composed name """
        self.assertEqual(self.get_create_number(4), '01DEFELI')

    def test_number_is_unique_less_6(self):
        """ Test number is unique whit 6 chars name """
        self.assertEqual(self.get_create_number(1), '01JOBS')
        self.assertEqual(self.get_create_number(10), '01JOBSB')
        self.assertEqual(self.get_create_number(11), '01JOBSBI')
        self.assertEqual(self.get_create_number(12), '01JOBBIL')
        self.assertEqual(self.get_create_number(13), '01JOBILL')
        self.assertEqual(self.get_create_number(14), '01JBILL')
        self.assertEqual(self.get_create_number(15), '01BILL')

    def test_number_is_unique_is_6(self):
        """ Test number is unique when name is 6 chars long """
        self.assertEqual(self.get_create_number(2), '01MARTIN')
        self.assertEqual(self.get_create_number(20), '01MARTIJ')
        self.assertEqual(self.get_create_number(21), '01MARTJU')
        self.assertEqual(self.get_create_number(22), '01MARJUL')
        self.assertEqual(self.get_create_number(23), '01MAJULI')
        self.assertEqual(self.get_create_number(24), '01MJULIE')
        self.assertEqual(self.get_create_number(25), '01JULIEN')

    def test_number_is_unique_more_6(self):
        """ Test number is unique when name is more 6 chars long """
        self.assertEqual(self.get_create_number(3), '01LEFEBV')
        self.assertEqual(self.get_create_number(30), '01LEFEBJ')
        self.assertEqual(self.get_create_number(31), '01LEFEJE')
        self.assertEqual(self.get_create_number(32), '01LEFJEA')
        self.assertEqual(self.get_create_number(33), '01LEJEAN')
        self.assertEqual(self.get_create_number(34), '01LJEAN')
        self.assertEqual(self.get_create_number(35), '01JEAN')

    def test_number_is_unique_when_name_is_composed(self):
        self.assertEqual(self.get_create_number(4), '01DEFELI')
        self.assertEqual(self.get_create_number(40), '01DEFELC')
        self.assertEqual(self.get_create_number(41), '01DEFECH')
        self.assertEqual(self.get_create_number(42), '01DEFCHA')
        self.assertEqual(self.get_create_number(43), '01DECHAR')
        self.assertEqual(self.get_create_number(44), '01DCHARL')
        self.assertEqual(self.get_create_number(45), '01CHARLE')

    def test_number_is_unique_when_first_name_is_composed(self):
        self.assertEqual(self.get_create_number(5), '01JOBS')
        self.assertEqual(self.get_create_number(50), '01JOBSY')
        self.assertEqual(self.get_create_number(51), '01JOBSYA')
        self.assertEqual(self.get_create_number(52), '01JOBYAN')
        self.assertEqual(self.get_create_number(53), '01JOYANP')
        self.assertEqual(self.get_create_number(54), '01JYANPA')
        self.assertEqual(self.get_create_number(55), '01YANPAU')

    def test_create_number_raise_execption(self):
        """ Test create number raise NotImplementedError """
        user = User.objects.get(pk=1)
        self.get_create_number(1)
        self.get_create_number(10)
        self.get_create_number(11)
        self.get_create_number(12)
        self.get_create_number(13)
        self.get_create_number(14)
        self.get_create_number(15)
        user = User(first_name='Bill', last_name='Jobs')
        user.save()
        profile = UserProfile(user=user)
        with self.assertRaises(NotImplementedError):
            profile.save()

    def test_multiple_profile_save_do_not_change_accounting_number(self):
        """ Test that a save of profile instance do not change existing value"""
        user = User.objects.get(pk=1)
        self.get_create_number(user.id)
        profile = UserProfile.objects.get(user=user)
        profile.save()
        self.assertEqual(profile.accounting_number, '01JOBS')

    def test_manual_input_change_record_new_value(self):
        user = User.objects.get(pk=1)
        self.get_create_number(user.id)
        self.assertEqual(user.userprofile.accounting_number, '01JOBS')
        user.userprofile.accounting_number = '01JOBSBI'
        user.userprofile.save()
        self.assertEqual(user.userprofile.accounting_number, '01JOBSBI')