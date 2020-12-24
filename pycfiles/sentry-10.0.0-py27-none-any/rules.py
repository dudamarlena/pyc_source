# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/receivers/rules.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.db.models.signals import post_save
from sentry.models import Project, Rule
DEFAULT_RULE_LABEL = 'Send a notification for new issues'
DEFAULT_RULE_DATA = {'match': 'all', 
   'conditions': [{'id': 'sentry.rules.conditions.first_seen_event.FirstSeenEventCondition'}], 'actions': [{'id': 'sentry.rules.actions.notify_event.NotifyEventAction'}]}

def create_default_rules(instance, created=True, RuleModel=Rule, **kwargs):
    if not created:
        return
    RuleModel.objects.create(project=instance, label=DEFAULT_RULE_LABEL, data=DEFAULT_RULE_DATA)


post_save.connect(create_default_rules, sender=Project, dispatch_uid='create_default_rules', weak=False)