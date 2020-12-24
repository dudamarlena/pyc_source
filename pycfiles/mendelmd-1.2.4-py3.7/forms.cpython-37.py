# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/settings/forms.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 355 bytes
from django.db import models
from django.forms import ModelForm
from .models import S3Credential

class S3CredentialForm(ModelForm):

    class Meta:
        model = S3Credential
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        (super(S3CredentialForm, self).__init__)(*args, **kwargs)