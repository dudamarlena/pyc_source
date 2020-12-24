# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-statistic/vkontakte_groups_statistic/forms.py
# Compiled at: 2013-08-08 03:51:26
from django import forms
from django.utils.translation import ugettext_lazy as _
from vkontakte_groups.forms import GroupImportForm
from models import Group
from datetime import datetime, timedelta

class GroupImportStatisticForm(GroupImportForm):

    def save(self, *args, **kwargs):
        group = super(GroupImportStatisticForm, self).save(*args, **kwargs)
        group.fetch_statistic()
        return group