# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_signup.py
# Compiled at: 2017-11-15 05:29:34
# Size of source mod 2**32: 859 bytes
from django.test import TestCase
from django.shortcuts import reverse

class SignupAndSlack(TestCase):
    __doc__ = " Test signup when project owner doesn't define slack settings "

    def test_slack_invitation(self):
        """ Test signup and slack invitation """
        data = {'username':'noslack', 
         'password':'motdepasse', 
         'first_name':'Bill', 
         'last_name':'Jobs', 
         'email':'billjobs_noslack@yopmail.com', 
         'billing_address':'une adresse'}
        response = self.client.post((reverse('billjobs_signup')),
          data, follow=True)
        self.assertRedirects(response,
          (reverse('billjobs_signup_success')),
          status_code=302,
          target_status_code=200)