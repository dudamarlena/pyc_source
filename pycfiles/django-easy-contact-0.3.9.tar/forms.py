# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact/easy_contact/forms.py
# Compiled at: 2014-10-17 10:59:57
__author__ = 'A. Fritz - c.a.t.forge.eu'
__date__ = '$09.09.2009 20:35:14$'
__doc__ = 'Zur Zeit noch keine Dokumentation.'
from django import forms
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
    """
    Einfaches Mailformular ohne Betreff.
    """
    email = forms.EmailField(required=True)
    subject = forms.Field(required=True)
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        u"""Prüft auf mindest Wort anzahl"""
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError(_('Not enough words!'))
        return message