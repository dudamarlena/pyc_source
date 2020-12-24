# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact-setup/easy_contact_setup/forms.py
# Compiled at: 2014-10-23 11:39:00
from django.forms import ModelForm, PasswordInput

class SetupForm(ModelForm):

    class Meta:
        widgets = {'mail_host_pass': PasswordInput(render_value=True)}