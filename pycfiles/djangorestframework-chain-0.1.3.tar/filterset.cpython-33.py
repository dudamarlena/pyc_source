# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philip/vms/vagrant/django-rest-framework-chain/rest_framework_chain/filterset.py
# Compiled at: 2013-12-11 23:52:53
# Size of source mod 2**32: 1752 bytes
from django.db.models.constants import LOOKUP_SEP
from django.utils.datastructures import SortedDict
from django.db.models.related import RelatedObject
from django.utils import six
import django_filters
from django_filters.filters import LOOKUP_TYPES
from django_filters.filterset import get_model_field
from .filters import RelatedFilter, AllLookupsFilter

class ChainedFilterSet(django_filters.FilterSet):

    def __new__(cls, *args, **kwargs):
        new_cls = super(ChainedFilterSet, cls).__new__(cls)
        for name, filter_ in six.iteritems(new_cls.base_filters):
            if isinstance(filter_, RelatedFilter):
                for f in filter_.filterset.base_filters.values():
                    if f in new_cls.base_filters.values():
                        continue
                    f.name = '%s%s%s' % (name, LOOKUP_SEP, f.name)
                    new_cls.base_filters[f.name] = f

            elif isinstance(filter_, AllLookupsFilter):
                model = new_cls._meta.model
                field = get_model_field(model, filter_.name)
                for lookup_type in LOOKUP_TYPES:
                    if isinstance(field, RelatedObject):
                        f = new_cls.filter_for_reverse_field(field, filter_.name)
                    else:
                        f = new_cls.filter_for_field(field, filter_.name)
                    f.lookup_type = lookup_type
                    new_cls.base_filters['%s__%s' % (filter_.name, lookup_type)] = f

                continue

        return new_cls