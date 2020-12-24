# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/notifications/evolutions/webhooktarget_extra_state.py
# Compiled at: 2020-02-11 04:03:56
from django_evolution.mutations import AddField, RenameField
from django.db import models
from djblets.db.fields import JSONField
MUTATIONS = [
 AddField('WebHookTarget', 'encoding', models.CharField, initial='application/json', max_length=40),
 AddField('WebHookTarget', 'repositories', models.ManyToManyField, null=True, related_model='scmtools.Repository'),
 AddField('WebHookTarget', 'custom_content', models.TextField, null=True),
 AddField('WebHookTarget', 'use_custom_content', models.BooleanField, initial=False),
 AddField('WebHookTarget', 'apply_to', models.CharField, initial='A', max_length=1),
 AddField('WebHookTarget', 'extra_data', JSONField, initial=None),
 RenameField('WebHookTarget', 'handlers', 'events')]