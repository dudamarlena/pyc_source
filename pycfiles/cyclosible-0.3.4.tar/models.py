# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seraf/Cycloid/Cyclosible/cyclosible/appversion/models.py
# Compiled at: 2015-12-22 05:07:25
from django.db import models
from cyclosible.playbook.models import Playbook

class AppVersion(models.Model):

    class Meta:
        app_label = 'appversion'

    ENV = (
     ('prod', 'prod'),
     ('preprod', 'preprod'),
     ('dev', 'dev'),
     ('infra', 'infra'))
    application = models.CharField(max_length=100, null=False)
    version = models.CharField(max_length=128, null=False)
    env = models.CharField(max_length=10, choices=ENV, default='PROD')
    deployed = models.BooleanField(default=False)
    playbook = models.ForeignKey(Playbook)

    def __unicode__(self):
        return ('-').join((self.playbook.name, self.application, self.env, self.version))