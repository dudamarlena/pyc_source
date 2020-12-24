# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/inviteme/tests/forms.py
# Compiled at: 2012-04-10 19:15:22
import time
from django.test import TestCase
from inviteme.forms import ContactMailSecurityForm, ContactMailForm

class ContactMailSecurityFormTestCase(TestCase):

    def test_constructor(self):
        form = ContactMailSecurityForm()
        self.assert_(form.initial.get('timestamp', None) != None)
        self.assert_(form.initial.get('security_hash', None) != None)
        self.assert_(form.initial.get('honeypot', None) == None)
        initial = {'timestamp': '1122334455', 'security_hash': 'blahblahashed'}
        form = ContactMailSecurityForm(initial=initial.copy())
        self.assert_(form.initial['timestamp'] != initial['timestamp'])
        self.assert_(form.initial['security_hash'] != initial['security_hash'])
        return

    def test_clean_timestamp(self):
        form = ContactMailSecurityForm()
        timestamp = int(form.initial['timestamp']) - 7320
        security_hash = form.generate_security_hash(timestamp)
        data = {'timestamp': str(timestamp), 'security_hash': security_hash}
        form = ContactMailSecurityForm(data=data)
        self.assert_(form.errors.get('timestamp', None) != None)
        return

    def test_clean_security_hash(self):
        form = ContactMailSecurityForm()
        data = {'timestamp': str(time.time()), 'security_hash': form.initial['security_hash']}
        form = ContactMailSecurityForm(data=data)
        self.assert_(form.errors.get('security_hash', None) != None)
        return

    def test_clean_honeypot(self):
        form = ContactMailSecurityForm()
        data = {'honeypot': 'Oh! big mistake!'}
        data.update(form.initial)
        form = ContactMailSecurityForm(data=data)
        self.assert_(form.errors.get('honeypot', None) != None)
        return


EMAIL_ADDR = 'alice.liddell@wonderland.com'

class ContactMailFormTestCase(TestCase):

    def test_get_instance_data(self):
        form = ContactMailForm()
        email = 'jane.bloggs@example.com'
        data = {'email': email}
        data.update(form.initial)
        form = ContactMailForm(data=data)
        form.is_valid()
        data = form.get_instance_data()
        self.assert_(len(data) == 2)
        self.assert_(email == data['email'])