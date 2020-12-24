# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/google_credentials/models.py
# Compiled at: 2013-01-22 03:47:41
from django.db import models
from oauth2client.django_orm import CredentialsField

class Credentials(models.Model):
    client_id = models.CharField(max_length=128)
    credentials = CredentialsField(editable=False, blank=True, null=True)