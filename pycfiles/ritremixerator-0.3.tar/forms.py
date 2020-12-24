# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eitan/Documents/code/RITRemixerator/dorrie/../dorrie/comps/forms.py
# Compiled at: 2012-02-01 14:42:02
from django import forms
from parse import ls_ks, languages, timezones

class NameForm(forms.Form):
    """
    Name and template
    """
    select_language = forms.ChoiceField(choices=languages(), initial='en_US')
    select_timezone = forms.ChoiceField(choices=timezones())
    name_of_the_spin = forms.CharField()
    kschoices = ((None, 'Use your own!'), ) + ls_ks()
    based_on = forms.ChoiceField(choices=kschoices)
    uploaded_kickstart = forms.FileField()
    select_language.widget.attrs['class'] = 'forminputdropdown'
    select_timezone.widget.attrs['class'] = 'forminputdropdown'
    name_of_the_spin.widget.attrs['class'] = 'forminputtext'
    based_on.widget.attrs['class'] = 'forminputdropdown'


class BasicForm(forms.Form):
    """
    Name and template
    """
    select_language = forms.ChoiceField(choices=languages(), initial='en_US')
    select_timezone = forms.ChoiceField(choices=timezones())