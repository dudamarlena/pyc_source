# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/form/nested_form.py
# Compiled at: 2013-04-11 17:47:52
from camelot.admin.entity_admin import EntityAdmin
from camelot.view import forms
from camelot.core.utils import ugettext_lazy as _

class Admin(EntityAdmin):
    verbose_name = _('person')
    verbose_name_plural = _('persons')
    list_display = ['first_name', 'last_name']
    form_display = forms.TabForm([('Basic', forms.Form(['first_name', 'last_name', 'contact_mechanisms'])),
     (
      'Official',
      forms.Form(['birthdate', 'social_security_number', 'passport_number',
       'passport_expiry_date', 'addresses']))])