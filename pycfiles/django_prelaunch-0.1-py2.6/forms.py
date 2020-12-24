# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/prelaunch/forms.py
# Compiled at: 2011-05-18 01:14:38
import hashlib
from django import forms
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.conf import settings
from settings import *
from models import PrelaunchSubscriber
from shorten import ShortCode

class PrelaunchForm(forms.Form):
    email_address = forms.EmailField()
    prelaunch_referrer = forms.CharField(widget=forms.HiddenInput(), required=False)