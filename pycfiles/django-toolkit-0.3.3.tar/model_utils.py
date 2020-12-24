# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/db/model_utils.py
# Compiled at: 2014-06-24 21:10:34
from __future__ import absolute_import
from django_toolkit.db.models import QuerySetManager
from model_utils.managers import InheritanceManager

class InheritanceQuerySetManager(QuerySetManager, InheritanceManager):
    pass