# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-twitter-relations-history/twitter_relations_history/signals.py
# Compiled at: 2013-05-10 07:56:16
from django.dispatch import Signal
from django.conf import settings
from annoying.decorators import signals
from vkontakte_groups.models import Group