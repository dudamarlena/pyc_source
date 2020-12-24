# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/fields/related_lookups.py
# Compiled at: 2019-02-14 00:35:17
from django.db.models.lookups import Exact, GreaterThan, GreaterThanOrEqual, In, IsNull, LessThan, LessThanOrEqual

class MultiColSource(object):
    contains_aggregate = False

    def __init__(self, alias, targets, sources, field):
        self.targets, self.sources, self.field, self.alias = (
         targets, sources, field, alias)
        self.output_field = self.field

    def __repr__(self):
        return ('{}({}, {})').format(self.__class__.__name__, self.alias, self.field)

    def relabeled_clone(self, relabels):
        return self.__class__(relabels.get(self.alias, self.alias), self.targets, self.sources, self.field)


def get_normalized_value(value, lhs):
    from django.db.models import Model
    if isinstance(value, Model):
        value_list = []
        sources = lhs.output_field.get_path_info()[(-1)].target_fields
        for source in sources:
            while not isinstance(value, source.model) and source.remote_field:
                source = source.remote_field.model._meta.get_field(source.remote_field.field_name)

            try:
                value_list.append(getattr(value, source.attname))
            except AttributeError:
                return (value.pk,)

        return tuple(value_list)
    if not isinstance(value, tuple):
        return (value,)
    return value


class RelatedIn(In):

    def get_prep_lookup(self):
        if not isinstance(self.lhs, MultiColSource) and self.rhs_is_direct_value():
            self.rhs = [ get_normalized_value(val, self.lhs)[0] for val in self.rhs ]
            if hasattr(self.lhs.output_field, 'get_path_info'):
                target_field = self.lhs.output_field.get_path_info()[(-1)].target_fields[(-1)]
                self.rhs = [ target_field.get_prep_value(v) for v in self.rhs ]
        return super(RelatedIn, self).get_prep_lookup()

    def as_sql(self, compiler, connection):
        if isinstance(self.lhs, MultiColSource):
            from django.db.models.sql.where import WhereNode, SubqueryConstraint, AND, OR
            root_constraint = WhereNode(connector=OR)
            if self.rhs_is_direct_value():
                values = [ get_normalized_value(value, self.lhs) for value in self.rhs ]
                for value in values:
                    value_constraint = WhereNode()
                    for source, target, val in zip(self.lhs.sources, self.lhs.targets, value):
                        lookup_class = target.get_lookup('exact')
                        lookup = lookup_class(target.get_col(self.lhs.alias, source), val)
                        value_constraint.add(lookup, AND)

                    root_constraint.add(value_constraint, OR)

            else:
                root_constraint.add(SubqueryConstraint(self.lhs.alias, [ target.column for target in self.lhs.targets ], [ source.name for source in self.lhs.sources ], self.rhs), AND)
            return root_constraint.as_sql(compiler, connection)
        else:
            if getattr(self.rhs, '_forced_pk', False) and not getattr(self.lhs.field.target_field, 'primary_key', False):
                self.rhs.clear_select_clause()
                if getattr(self.lhs.output_field, 'primary_key', False) and self.lhs.output_field.model == self.rhs.model:
                    target_field = self.lhs.field.name
                else:
                    target_field = self.lhs.field.target_field.name
                self.rhs.add_fields([target_field], True)
            return super(RelatedIn, self).as_sql(compiler, connection)


class RelatedLookupMixin(object):

    def get_prep_lookup(self):
        if not isinstance(self.lhs, MultiColSource) and self.rhs_is_direct_value():
            self.rhs = get_normalized_value(self.rhs, self.lhs)[0]
            if self.prepare_rhs and hasattr(self.lhs.output_field, 'get_path_info'):
                target_field = self.lhs.output_field.get_path_info()[(-1)].target_fields[(-1)]
                self.rhs = target_field.get_prep_value(self.rhs)
        return super(RelatedLookupMixin, self).get_prep_lookup()

    def as_sql(self, compiler, connection):
        if isinstance(self.lhs, MultiColSource):
            assert self.rhs_is_direct_value()
            self.rhs = get_normalized_value(self.rhs, self.lhs)
            from django.db.models.sql.where import WhereNode, AND
            root_constraint = WhereNode()
            for target, source, val in zip(self.lhs.targets, self.lhs.sources, self.rhs):
                lookup_class = target.get_lookup(self.lookup_name)
                root_constraint.add(lookup_class(target.get_col(self.lhs.alias, source), val), AND)

            return root_constraint.as_sql(compiler, connection)
        return super(RelatedLookupMixin, self).as_sql(compiler, connection)


class RelatedExact(RelatedLookupMixin, Exact):
    pass


class RelatedLessThan(RelatedLookupMixin, LessThan):
    pass


class RelatedGreaterThan(RelatedLookupMixin, GreaterThan):
    pass


class RelatedGreaterThanOrEqual(RelatedLookupMixin, GreaterThanOrEqual):
    pass


class RelatedLessThanOrEqual(RelatedLookupMixin, LessThanOrEqual):
    pass


class RelatedIsNull(RelatedLookupMixin, IsNull):
    pass