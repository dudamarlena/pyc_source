# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/apps.py
# Compiled at: 2017-06-07 04:25:24
from django.apps import AppConfig
from django.db.models.signals import post_migrate
import secretballot

def do_enable_voting_on(sender, **kwargs):
    from jmbo import models
    secretballot.enable_voting_on(models.ModelBase, manager_name='secretballot_objects', total_name='secretballot_added_vote_total')


class JmboAppConfig(AppConfig):
    name = 'jmbo'

    def ready(self):
        post_migrate.connect(do_enable_voting_on)