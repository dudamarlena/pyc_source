# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/forms.py
# Compiled at: 2019-07-30 06:53:25
# Size of source mod 2**32: 676 bytes
from django import forms
from contact.tasks import send_contact_email_task

class ContactForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    message = forms.CharField(label='Message',
      widget=forms.Textarea(attrs={'rows': 5}))
    honeypot = forms.CharField(widget=(forms.HiddenInput()), required=False)

    def send_email(self):
        if self.cleaned_data['honeypot']:
            return False
        send_contact_email_task.delay(self.cleaned_data['email'], self.cleaned_data['message'])