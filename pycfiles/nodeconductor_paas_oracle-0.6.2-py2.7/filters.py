# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/filters.py
# Compiled at: 2016-12-16 07:39:01
import django_filters
from nodeconductor.structure.filters import BaseResourceStateFilter
from .models import Deployment

class DeploymentFilter(BaseResourceStateFilter):
    db_name = django_filters.CharFilter()

    class Meta(BaseResourceStateFilter.Meta):
        model = Deployment
        fields = [
         'db_name',
         'state']
        order_by = [
         'state',
         '-state']