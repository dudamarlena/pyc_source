# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/forms.py
# Compiled at: 2015-03-27 08:23:12
""" Form definition for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django import forms
from django.forms.models import inlineformset_factory
from django.utils.html import escape, strip_tags
from ninecms.models import Node, Image

class ContentNodeEditForm(forms.ModelForm):
    """ Node edit or create form """

    class Meta:
        model = Node
        fields = ['page_type', 'language', 'title', 'user', 'status', 'promote', 'sticky', 'created',
         'original_translation', 'summary', 'body', 'highlight', 'link', 'weight']


ImageInlineFormset = inlineformset_factory(Node, Image, fields=['title', 'group', 'image'])

class ContactForm(forms.Form):
    """ Contact form """
    attr = {'class': 'form-control'}
    sender_name = forms.CharField(max_length=100, label='Your name', widget=forms.TextInput(attrs=attr))
    sender_email = forms.EmailField(max_length=100, label='Your email', widget=forms.TextInput(attrs=attr))
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs=attr))
    message = forms.CharField(widget=forms.Textarea(attrs=attr))
    redirect = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        """ Additionally to Django clean() (https://docs.djangoproject.com/en/1.7/ref/forms/validation/)
        Sanitize HTML from form data (http://stackoverflow.com/questions/5641901/sanitizing-html-in-submitted-form-data)
        Otherwise the template will escape without stripping if not so specified
        :return: cleaned data
        """
        cleaned_data = super(ContactForm, self).clean()
        if 'sender_name' in cleaned_data:
            cleaned_data['sender_name'] = escape(strip_tags(cleaned_data['sender_name']))
        if 'sender_email' in cleaned_data:
            cleaned_data['sender_email'] = escape(strip_tags(cleaned_data['sender_email']))
        if 'subject' in cleaned_data:
            cleaned_data['subject'] = '[Website Feedback] ' + escape(strip_tags(cleaned_data['subject']))
        if 'message' in cleaned_data:
            cleaned_data['message'] = escape(strip_tags(cleaned_data['message']))
        if 'redirect' in cleaned_data:
            cleaned_data['redirect'] = escape(strip_tags(cleaned_data['redirect']))
        return cleaned_data