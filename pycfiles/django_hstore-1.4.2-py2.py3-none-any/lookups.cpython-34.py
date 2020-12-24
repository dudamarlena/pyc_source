# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/lookups.py
# Compiled at: 2015-06-28 18:07:27
# Size of source mod 2**32: 4823 bytes
from __future__ import unicode_literals, absolute_import
from django.utils import six
from django.db.models.lookups import GreaterThan, GreaterThanOrEqual, LessThan, LessThanOrEqual, Contains, IContains, IsNull
from django_hstore.utils import get_cast_for_param, get_value_annotations
__all__ = [
 'HStoreComparisonLookupMixin',
 'HStoreGreaterThan',
 'HStoreGreaterThanOrEqual',
 'HStoreLessThan',
 'HStoreLessThanOrEqual',
 'HStoreContains',
 'HStoreIContains',
 'HStoreIsNull']

class HStoreLookupMixin(object):

    def __init__(self, lhs, rhs, *args, **kwargs):
        if isinstance(rhs, dict):
            self.value_annot = get_value_annotations(rhs)
        super(HStoreLookupMixin, self).__init__(lhs, rhs)


class HStoreComparisonLookupMixin(HStoreLookupMixin):
    __doc__ = '\n    Mixin for hstore comparison custom lookups.\n    '

    def as_postgresql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        if len(rhs_params) == 1 and isinstance(rhs_params[0], dict):
            param = rhs_params[0]
            sign = (self.lookup_name[0] == 'g' and '>%s' or '<%s') % (self.lookup_name[(-1)] == 'e' and '=' or '')
            param_keys = list(param.keys())
            conditions = []
            for key in param_keys:
                cast = get_cast_for_param(self.value_annot, key)
                conditions.append("(%s->'%s')%s %s %%s" % (lhs, key, cast, sign))

            return (
             ' AND '.join(conditions), param.values())
        raise ValueError('invalid value')


class HStoreGreaterThan(HStoreComparisonLookupMixin, GreaterThan):
    pass


class HStoreGreaterThanOrEqual(HStoreComparisonLookupMixin, GreaterThanOrEqual):
    pass


class HStoreLessThan(HStoreComparisonLookupMixin, LessThan):
    pass


class HStoreLessThanOrEqual(HStoreComparisonLookupMixin, LessThanOrEqual):
    pass


class HStoreContains(HStoreLookupMixin, Contains):

    def as_postgresql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        if lhs.endswith('::text'):
            lhs = '{0}{1}'.format(lhs[:-4], 'hstore')
        param = self.rhs
        if isinstance(param, dict):
            values = list(param.values())
            keys = list(param.keys())
            if len(values) == 1 and isinstance(values[0], (list, tuple)):
                return (
                 "%s->'%s' = ANY(%%s)" % (lhs, keys[0]), [[str(x) for x in values[0]]])
            if len(keys) == 1 and len(values) == 1:
                cast = get_cast_for_param(self.value_annot, keys[0])
                return (
                 "(%s->'%s')%s = %%s" % (lhs, keys[0], cast), [values[0]])
            return ('%s @> %%s' % lhs, [param])
        if isinstance(param, (list, tuple)):
            if len(param) == 0:
                raise ValueError('invalid value')
            if len(param) < 2:
                return ('%s ? %%s' % lhs, [param[0]])
            if param:
                return ('%s ?& %%s' % lhs, [param])
        else:
            if isinstance(param, six.string_types):
                pass
            elif hasattr(self.lhs.target, 'serializer'):
                try:
                    self.lhs.target._serialize_value(param)
                except Exception:
                    raise ValueError('invalid value')

            else:
                raise ValueError('invalid value')
        return super(HStoreContains, self).as_sql(compiler, connection)


class HStoreIContains(IContains, HStoreContains):
    pass


class HStoreIsNull(IsNull):

    def as_postgresql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        if isinstance(self.rhs, dict):
            param = self.rhs
            param_keys = list(param.keys())
            conditions = []
            for key in param_keys:
                op = 'IS NULL' if param[key] else 'IS NOT NULL'
                conditions.append("(%s->'%s') %s" % (lhs, key, op))

            return (
             ' AND '.join(conditions), lhs_params)
        return super(HStoreIsNull, self).as_sql(compiler, connection)