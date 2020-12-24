# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/publisher/__init__.py
# Compiled at: 2011-10-05 09:27:43
from django.db.models import signals
from publisher.models import Publisher

def publish(sender, instance, action, reverse, model, pk_set, **kwargs):
    if model == Publisher:
        if pk_set and action == 'post_add':
            publishers = Publisher.objects.filter(pk__in=pk_set)
            for publisher in publishers:
                publisher.publish(instance)


signals.m2m_changed.connect(publish)