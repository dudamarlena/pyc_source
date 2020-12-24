# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /www/elorus/local/lib/python2.7/site-packages/yawdadmin/models.py
# Compiled at: 2013-08-25 05:42:06
from django.db import models
from fields import OptionNameField

class AppOption(models.Model):
    optionset_label = models.CharField(max_length=50)
    name = OptionNameField(max_length=50)
    value = models.TextField(null=True)
    lang_dependant = models.BooleanField(default=False)

    class Meta:
        unique_together = ('optionset_label', 'name')
        ordering = ['optionset_label', 'lang_dependant']

    def __unicode__(self):
        return '%s.%s' % (self.optionset_label, self.name)