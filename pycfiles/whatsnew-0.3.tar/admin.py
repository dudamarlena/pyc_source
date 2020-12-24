# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-whatsnew/whatsnew/admin.py
# Compiled at: 2014-04-04 10:09:51
from django import forms
from django.contrib.admin import ModelAdmin, site
from whatsnew.models import WhatsNew
try:
    from suit_redactor.widgets import RedactorWidget
except ImportError:

    class RedactorWidget(forms.Textarea):

        def __init__(self, attrs=None, editor_options=None):
            super(RedactorWidget, self).__init__(attrs)


class WhatsNewForm(forms.ModelForm):

    class Meta:
        widgets = {'content': RedactorWidget(editor_options={'lang': 'en'})}


class WhatsNewAdmin(ModelAdmin):
    change_form_template = 'admin/whatsnew/change_form_whatsnew.html'
    list_display = ('version', 'expire', 'enabled')
    form = WhatsNewForm


site.register(WhatsNew, WhatsNewAdmin)