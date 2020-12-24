# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philip/vms/vagrant/django-rest-framework-chain/rest_framework_chain/filters.py
# Compiled at: 2013-12-11 18:25:13
# Size of source mod 2**32: 387 bytes
import django_filters

class RelatedFilter(django_filters.ModelChoiceFilter):

    def __init__(self, filterset, *args, **kwargs):
        self.filterset = filterset
        kwargs['queryset'] = self.filterset._meta.model.objects.all()
        super(RelatedFilter, self).__init__(*args, **kwargs)


class AllLookupsFilter(django_filters.Filter):
    pass