# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/javed/Work/Dinette/dinette/forms.py
# Compiled at: 2013-07-02 04:51:32
from django.forms import ModelForm
from django import forms
from dinette.models import Ftopics, Reply

class FtopicForm(ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'size': 90}))
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows': 10}))

    class Meta:
        model = Ftopics
        fields = ('subject', 'message', 'message_markup_type', 'file')


class ReplyForm(ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 90, 'rows': 10}))

    class Meta:
        model = Reply
        fields = ('message', 'message_markup_type', 'file')