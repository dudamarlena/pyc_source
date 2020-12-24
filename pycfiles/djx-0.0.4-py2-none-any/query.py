# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/models/sql/query.py
# Compiled at: 2019-02-14 00:35:17
"""
Create SQL statements for QuerySets.

The code in here encapsulates all of the SQL construction so that QuerySets
themselves do not have to (and could be backed by things other than SQL
databases). The abstraction barrier only works one way: this module has to know
all about the internals of models in order to get the information it needs.
"""
import copy, warnings
from collections import Counter, Iterator, Mapping, OrderedDict
from itertools import chain, count, product
from string import ascii_uppercase
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models.aggregates import Count
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import Col, Ref
from django.db.models.fields.related_lookups import MultiColSource
from django.db.models.lookups import Lookup
from django.db.models.query_utils import Q, check_rel_lookup_compatibility, refs_expression
from django.db.models.sql.constants import INNER, LOUTER, ORDER_DIR, ORDER_PATTERN, QUERY_TERMS, SINGLE
from django.db.models.sql.datastructures import BaseTable, Empty, EmptyResultSet, Join, MultiJoin
from django.db.models.sql.where import AND, OR, ExtraWhere, NothingNode, WhereNode
from django.utils import six
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.utils.tree import Node
__all__ = [
 'Query', 'RawQuery']

def get_field_names_from_opts(opts):
    return set(chain.from_iterable(((f.name, f.attname) if f.concrete else (f.name,)) for f in opts.get_fields()))


class RawQuery(object):
    """
    A single raw SQL query
    """

    def __init__(self, sql, using, params=None, context=None):
        self.params = params or ()
        self.sql = sql
        self.using = using
        self.cursor = None
        self.low_mark, self.high_mark = (0, None)
        self.extra_select = {}
        self.annotation_select = {}
        self.context = context or {}
        return

    def clone(self, using):
        return RawQuery(self.sql, using, params=self.params, context=self.context.copy())

    def get_columns(self):
        if self.cursor is None:
            self._execute_query()
        converter = connections[self.using].introspection.column_name_converter
        return [ converter(column_meta[0]) for column_meta in self.cursor.description
               ]

    def __iter__(self):
        self._execute_query()
        if not connections[self.using].features.can_use_chunked_reads:
            result = list(self.cursor)
        else:
            result = self.cursor
        return iter(result)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    @property
    def params_type(self):
        if isinstance(self.params, Mapping):
            return dict
        return tuple

    def __str__(self):
        return self.sql % self.params_type(self.params)

    def _execute_query(self):
        connection = connections[self.using]
        params_type = self.params_type
        adapter = connection.ops.adapt_unknown_value
        if params_type is tuple:
            params = tuple(adapter(val) for val in self.params)
        elif params_type is dict:
            params = dict((key, adapter(val)) for key, val in six.iteritems(self.params))
        else:
            raise RuntimeError('Unexpected params type: %s' % params_type)
        self.cursor = connection.cursor()
        self.cursor.execute(self.sql, params)


class Query(object):
    """
    A single SQL query.
    """
    alias_prefix = 'T'
    subq_aliases = frozenset([alias_prefix])
    query_terms = QUERY_TERMS
    compiler = 'SQLCompiler'

    def __init__(self, model, where=WhereNode):
        self.model = model
        self.alias_refcount = {}
        self.alias_map = OrderedDict()
        self.external_aliases = set()
        self.table_map = {}
        self.default_cols = True
        self.default_ordering = True
        self.standard_ordering = True
        self.used_aliases = set()
        self.filter_is_sticky = False
        self.subquery = False
        self.select = []
        self.tables = []
        self.where = where()
        self.where_class = where
        self.group_by = None
        self.order_by = []
        self.low_mark, self.high_mark = (0, None)
        self.distinct = False
        self.distinct_fields = []
        self.select_for_update = False
        self.select_for_update_nowait = False
        self.select_for_update_skip_locked = False
        self.select_related = False
        self.max_depth = 5
        self.values_select = []
        self._annotations = None
        self.annotation_select_mask = None
        self._annotation_select_cache = None
        self.combinator = None
        self.combinator_all = False
        self.combined_queries = ()
        self._extra = None
        self.extra_select_mask = None
        self._extra_select_cache = None
        self.extra_tables = ()
        self.extra_order_by = ()
        self.deferred_loading = (
         set(), True)
        self.context = {}
        return

    @property
    def extra(self):
        if self._extra is None:
            self._extra = OrderedDict()
        return self._extra

    @property
    def annotations(self):
        if self._annotations is None:
            self._annotations = OrderedDict()
        return self._annotations

    def __str__(self):
        """
        Returns the query as a string of SQL with the parameter values
        substituted in (use sql_with_params() to see the unsubstituted string).

        Parameter values won't necessarily be quoted correctly, since that is
        done by the database interface at execution time.
        """
        sql, params = self.sql_with_params()
        return sql % params

    def sql_with_params(self):
        """
        Returns the query as an SQL string and the parameters that will be
        substituted into the query.
        """
        return self.get_compiler(DEFAULT_DB_ALIAS).as_sql()

    def __deepcopy__(self, memo):
        result = self.clone(memo=memo)
        memo[id(self)] = result
        return result

    def _prepare(self, field):
        return self

    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError('Need either using or connection')
        if using:
            connection = connections[using]
        return connection.ops.compiler(self.compiler)(self, connection, using)

    def get_meta(self):
        """
        Returns the Options instance (the model._meta) from which to start
        processing. Normally, this is self.model._meta, but it can be changed
        by subclasses.
        """
        return self.model._meta

    def clone(self, klass=None, memo=None, **kwargs):
        """
        Creates a copy of the current instance. The 'kwargs' parameter can be
        used by clients to update attributes after copying has taken place.
        """
        obj = Empty()
        obj.__class__ = klass or self.__class__
        obj.model = self.model
        obj.alias_refcount = self.alias_refcount.copy()
        obj.alias_map = self.alias_map.copy()
        obj.external_aliases = self.external_aliases.copy()
        obj.table_map = self.table_map.copy()
        obj.default_cols = self.default_cols
        obj.default_ordering = self.default_ordering
        obj.standard_ordering = self.standard_ordering
        obj.select = self.select[:]
        obj.tables = self.tables[:]
        obj.where = self.where.clone()
        obj.where_class = self.where_class
        if self.group_by is None:
            obj.group_by = None
        elif self.group_by is True:
            obj.group_by = True
        else:
            obj.group_by = self.group_by[:]
        obj.order_by = self.order_by[:]
        obj.low_mark, obj.high_mark = self.low_mark, self.high_mark
        obj.distinct = self.distinct
        obj.distinct_fields = self.distinct_fields[:]
        obj.select_for_update = self.select_for_update
        obj.select_for_update_nowait = self.select_for_update_nowait
        obj.select_for_update_skip_locked = self.select_for_update_skip_locked
        obj.select_related = self.select_related
        obj.values_select = self.values_select[:]
        obj._annotations = self._annotations.copy() if self._annotations is not None else None
        if self.annotation_select_mask is None:
            obj.annotation_select_mask = None
        else:
            obj.annotation_select_mask = self.annotation_select_mask.copy()
        obj._annotation_select_cache = None
        obj.max_depth = self.max_depth
        obj.combinator = self.combinator
        obj.combinator_all = self.combinator_all
        obj.combined_queries = self.combined_queries
        obj._extra = self._extra.copy() if self._extra is not None else None
        if self.extra_select_mask is None:
            obj.extra_select_mask = None
        else:
            obj.extra_select_mask = self.extra_select_mask.copy()
        if self._extra_select_cache is None:
            obj._extra_select_cache = None
        else:
            obj._extra_select_cache = self._extra_select_cache.copy()
        obj.extra_tables = self.extra_tables
        obj.extra_order_by = self.extra_order_by
        obj.deferred_loading = (copy.copy(self.deferred_loading[0]), self.deferred_loading[1])
        if self.filter_is_sticky and self.used_aliases:
            obj.used_aliases = self.used_aliases.copy()
        else:
            obj.used_aliases = set()
        obj.filter_is_sticky = False
        obj.subquery = self.subquery
        if 'alias_prefix' in self.__dict__:
            obj.alias_prefix = self.alias_prefix
        if 'subq_aliases' in self.__dict__:
            obj.subq_aliases = self.subq_aliases.copy()
        obj.__dict__.update(kwargs)
        if hasattr(obj, '_setup_query'):
            obj._setup_query()
        obj.context = self.context.copy()
        obj._forced_pk = getattr(self, '_forced_pk', False)
        return obj

    def add_context(self, key, value):
        self.context[key] = value

    def get_context(self, key, default=None):
        return self.context.get(key, default)

    def relabeled_clone(self, change_map):
        clone = self.clone()
        clone.change_aliases(change_map)
        return clone

    def rewrite_cols(self, annotation, col_cnt):
        orig_exprs = annotation.get_source_expressions()
        new_exprs = []
        for expr in orig_exprs:
            if isinstance(expr, Ref):
                new_exprs.append(expr)
            elif isinstance(expr, (WhereNode, Lookup)):
                new_expr, col_cnt = self.rewrite_cols(expr, col_cnt)
                new_exprs.append(new_expr)
            elif isinstance(expr, Col) or expr.contains_aggregate and not expr.is_summary:
                col_cnt += 1
                col_alias = '__col%d' % col_cnt
                self.annotations[col_alias] = expr
                self.append_annotation_mask([col_alias])
                new_exprs.append(Ref(col_alias, expr))
            else:
                new_expr, col_cnt = self.rewrite_cols(expr, col_cnt)
                new_exprs.append(new_expr)

        annotation.set_source_expressions(new_exprs)
        return (annotation, col_cnt)

    def get_aggregation(self, using, added_aggregate_names):
        """
        Returns the dictionary with the values of the existing aggregations.
        """
        if not self.annotation_select:
            return {}
        else:
            has_limit = self.low_mark != 0 or self.high_mark is not None
            has_existing_annotations = any(annotation for alias, annotation in self.annotations.items() if alias not in added_aggregate_names)
            if isinstance(self.group_by, list) or has_limit or has_existing_annotations or self.distinct or self.combinator:
                from django.db.models.sql.subqueries import AggregateQuery
                outer_query = AggregateQuery(self.model)
                inner_query = self.clone()
                inner_query.select_for_update = False
                inner_query.select_related = False
                if not has_limit and not self.distinct_fields:
                    inner_query.clear_ordering(True)
                if not inner_query.distinct:
                    if inner_query.default_cols and has_existing_annotations:
                        inner_query.group_by = [
                         self.model._meta.pk.get_col(inner_query.get_initial_alias())]
                    inner_query.default_cols = False
                relabels = {t:'subquery' for t in inner_query.tables}
                relabels[None] = 'subquery'
                col_cnt = 0
                for alias, expression in list(inner_query.annotation_select.items()):
                    if expression.is_summary:
                        expression, col_cnt = inner_query.rewrite_cols(expression, col_cnt)
                        outer_query.annotations[alias] = expression.relabeled_clone(relabels)
                        del inner_query.annotations[alias]
                    inner_query.set_annotation_mask(inner_query.annotation_select_mask)

                if inner_query.select == [] and not inner_query.default_cols and not inner_query.annotation_select_mask:
                    inner_query.select = [
                     self.model._meta.pk.get_col(inner_query.get_initial_alias())]
                try:
                    outer_query.add_subquery(inner_query, using)
                except EmptyResultSet:
                    return {alias:None for alias in outer_query.annotation_select}

            else:
                outer_query = self
                self.select = []
                self.default_cols = False
                self._extra = {}
            outer_query.clear_ordering(True)
            outer_query.clear_limits()
            outer_query.select_for_update = False
            outer_query.select_related = False
            compiler = outer_query.get_compiler(using)
            result = compiler.execute_sql(SINGLE)
            if result is None:
                result = [ None for q in outer_query.annotation_select.items() ]
            converters = compiler.get_converters(outer_query.annotation_select.values())
            result = compiler.apply_converters(result, converters)
            return {alias:val for (alias, annotation), val in zip(outer_query.annotation_select.items(), result)}

    def get_count(self, using):
        """
        Performs a COUNT() query using the current filter constraints.
        """
        obj = self.clone()
        obj.add_annotation(Count('*'), alias='__count', is_summary=True)
        number = obj.get_aggregation(using, ['__count'])['__count']
        if number is None:
            number = 0
        return number

    def has_filters(self):
        return self.where

    def has_results(self, using):
        q = self.clone()
        if not q.distinct:
            if q.group_by is True:
                q.add_fields((f.attname for f in self.model._meta.concrete_fields), False)
                q.set_group_by()
            q.clear_select_clause()
        q.clear_ordering(True)
        q.set_limits(high=1)
        compiler = q.get_compiler(using=using)
        return compiler.has_results()

    def combine(self, rhs, connector):
        """
        Merge the 'rhs' query into the current one (with any 'rhs' effects
        being applied *after* (that is, "to the right of") anything in the
        current query. 'rhs' is not modified during a call to this function.

        The 'connector' parameter describes how to connect filters from the
        'rhs' query.
        """
        if not self.model == rhs.model:
            raise AssertionError('Cannot combine queries on two different base models.')
            assert self.can_filter(), 'Cannot combine queries once a slice has been taken.'
            assert self.distinct == rhs.distinct, 'Cannot combine a unique query with a non-unique query.'
            assert self.distinct_fields == rhs.distinct_fields, 'Cannot combine queries with different distinct fields.'
            change_map = {}
            conjunction = connector == AND
            reuse = set() if conjunction else set(self.tables)
            self.get_initial_alias()
            joinpromoter = JoinPromoter(connector, 2, False)
            joinpromoter.add_votes(j for j in self.alias_map if self.alias_map[j].join_type == INNER)
            rhs_votes = set()
            for alias in rhs.tables[1:]:
                join = rhs.alias_map[alias]
                join = join.relabeled_clone(change_map)
                new_alias = self.join(join, reuse=reuse)
                if join.join_type == INNER:
                    rhs_votes.add(new_alias)
                reuse.discard(new_alias)
                if alias != new_alias:
                    change_map[alias] = new_alias
                if not rhs.alias_refcount[alias]:
                    self.unref_alias(new_alias)

            joinpromoter.add_votes(rhs_votes)
            joinpromoter.update_join_types(self)
            w = rhs.where.clone()
            w.relabel_aliases(change_map)
            self.where.add(w, connector)
            self.select = []
            for col in rhs.select:
                self.add_select(col.relabeled_clone(change_map))

            if connector == OR and self._extra and rhs._extra:
                raise ValueError("When merging querysets using 'or', you cannot have extra(select=...) on both sides.")
        self.extra.update(rhs.extra)
        extra_select_mask = set()
        if self.extra_select_mask is not None:
            extra_select_mask.update(self.extra_select_mask)
        if rhs.extra_select_mask is not None:
            extra_select_mask.update(rhs.extra_select_mask)
        if extra_select_mask:
            self.set_extra_mask(extra_select_mask)
        self.extra_tables += rhs.extra_tables
        self.order_by = rhs.order_by[:] if rhs.order_by else self.order_by
        self.extra_order_by = rhs.extra_order_by or self.extra_order_by
        return

    def deferred_to_data(self, target, callback):
        """
        Converts the self.deferred_loading data structure to an alternate data
        structure, describing the field that *will* be loaded. This is used to
        compute the columns to select from the database and also by the
        QuerySet class to work out which fields are being initialized on each
        model. Models that have all their fields included aren't mentioned in
        the result, only those that have field restrictions in place.

        The "target" parameter is the instance that is populated (in place).
        The "callback" is a function that is called whenever a (model, field)
        pair need to be added to "target". It accepts three parameters:
        "target", and the model and list of fields being added for that model.
        """
        field_names, defer = self.deferred_loading
        if not field_names:
            return
        orig_opts = self.get_meta()
        seen = {}
        must_include = {orig_opts.concrete_model: {orig_opts.pk}}
        for field_name in field_names:
            parts = field_name.split(LOOKUP_SEP)
            cur_model = self.model._meta.concrete_model
            opts = orig_opts
            for name in parts[:-1]:
                old_model = cur_model
                source = opts.get_field(name)
                if is_reverse_o2o(source):
                    cur_model = source.related_model
                else:
                    cur_model = source.remote_field.model
                opts = cur_model._meta
                if not is_reverse_o2o(source):
                    must_include[old_model].add(source)
                add_to_dict(must_include, cur_model, opts.pk)

            field = opts.get_field(parts[(-1)])
            is_reverse_object = field.auto_created and not field.concrete
            model = field.related_model if is_reverse_object else field.model
            model = model._meta.concrete_model
            if model == opts.model:
                model = cur_model
            if not is_reverse_o2o(field):
                add_to_dict(seen, model, field)

        if defer:
            workset = {}
            for model, values in six.iteritems(seen):
                for field in model._meta.fields:
                    if field in values:
                        continue
                    m = field.model._meta.concrete_model
                    add_to_dict(workset, m, field)

            for model, values in six.iteritems(must_include):
                if model in workset:
                    workset[model].update(values)

            for model, values in six.iteritems(workset):
                callback(target, model, values)

        else:
            for model, values in six.iteritems(must_include):
                if model in seen:
                    seen[model].update(values)
                else:
                    seen[model] = values

            for model in orig_opts.get_parent_list():
                if model not in seen:
                    seen[model] = set()

            for model, values in six.iteritems(seen):
                callback(target, model, values)

    def table_alias(self, table_name, create=False):
        """
        Returns a table alias for the given table_name and whether this is a
        new alias or not.

        If 'create' is true, a new alias is always created. Otherwise, the
        most recently created alias for the table (if one exists) is reused.
        """
        alias_list = self.table_map.get(table_name)
        if not create and alias_list:
            alias = alias_list[0]
            self.alias_refcount[alias] += 1
            return (
             alias, False)
        if alias_list:
            alias = '%s%d' % (self.alias_prefix, len(self.alias_map) + 1)
            alias_list.append(alias)
        else:
            alias = table_name
            self.table_map[alias] = [alias]
        self.alias_refcount[alias] = 1
        self.tables.append(alias)
        return (alias, True)

    def ref_alias(self, alias):
        """ Increases the reference count for this alias. """
        self.alias_refcount[alias] += 1

    def unref_alias(self, alias, amount=1):
        """ Decreases the reference count for this alias. """
        self.alias_refcount[alias] -= amount

    def promote_joins(self, aliases):
        """
        Promotes recursively the join type of given aliases and its children to
        an outer join. If 'unconditional' is False, the join is only promoted if
        it is nullable or the parent join is an outer join.

        The children promotion is done to avoid join chains that contain a LOUTER
        b INNER c. So, if we have currently a INNER b INNER c and a->b is promoted,
        then we must also promote b->c automatically, or otherwise the promotion
        of a->b doesn't actually change anything in the query results.
        """
        aliases = list(aliases)
        while aliases:
            alias = aliases.pop(0)
            if self.alias_map[alias].join_type is None:
                continue
            assert self.alias_map[alias].join_type is not None
            parent_alias = self.alias_map[alias].parent_alias
            parent_louter = parent_alias and self.alias_map[parent_alias].join_type == LOUTER
            already_louter = self.alias_map[alias].join_type == LOUTER
            if (self.alias_map[alias].nullable or parent_louter) and not already_louter:
                self.alias_map[alias] = self.alias_map[alias].promote()
                aliases.extend(join for join in self.alias_map.keys() if self.alias_map[join].parent_alias == alias and join not in aliases)

        return

    def demote_joins(self, aliases):
        """
        Change join type from LOUTER to INNER for all joins in aliases.

        Similarly to promote_joins(), this method must ensure no join chains
        containing first an outer, then an inner join are generated. If we
        are demoting b->c join in chain a LOUTER b LOUTER c then we must
        demote a->b automatically, or otherwise the demotion of b->c doesn't
        actually change anything in the query results. .
        """
        aliases = list(aliases)
        while aliases:
            alias = aliases.pop(0)
            if self.alias_map[alias].join_type == LOUTER:
                self.alias_map[alias] = self.alias_map[alias].demote()
                parent_alias = self.alias_map[alias].parent_alias
                if self.alias_map[parent_alias].join_type == INNER:
                    aliases.append(parent_alias)

    def reset_refcounts(self, to_counts):
        """
        This method will reset reference counts for aliases so that they match
        the value passed in :param to_counts:.
        """
        for alias, cur_refcount in self.alias_refcount.copy().items():
            unref_amount = cur_refcount - to_counts.get(alias, 0)
            self.unref_alias(alias, unref_amount)

    def change_aliases(self, change_map):
        """
        Changes the aliases in change_map (which maps old-alias -> new-alias),
        relabelling any references to them in select columns and the where
        clause.
        """
        assert set(change_map.keys()).intersection(set(change_map.values())) == set()
        self.where.relabel_aliases(change_map)
        if isinstance(self.group_by, list):
            self.group_by = [ col.relabeled_clone(change_map) for col in self.group_by ]
        self.select = [ col.relabeled_clone(change_map) for col in self.select ]
        if self._annotations:
            self._annotations = OrderedDict((key, col.relabeled_clone(change_map)) for key, col in self._annotations.items())
        for old_alias, new_alias in six.iteritems(change_map):
            if old_alias not in self.alias_map:
                continue
            alias_data = self.alias_map[old_alias].relabeled_clone(change_map)
            self.alias_map[new_alias] = alias_data
            self.alias_refcount[new_alias] = self.alias_refcount[old_alias]
            del self.alias_refcount[old_alias]
            del self.alias_map[old_alias]
            table_aliases = self.table_map[alias_data.table_name]
            for pos, alias in enumerate(table_aliases):
                if alias == old_alias:
                    table_aliases[pos] = new_alias
                    break

        self.external_aliases = {change_map.get(alias, alias) for alias in self.external_aliases}

    def bump_prefix(self, outer_query):
        """
        Changes the alias prefix to the next letter in the alphabet in a way
        that the outer query's aliases and this query's aliases will not
        conflict. Even tables that previously had no alias will get an alias
        after this call.
        """

        def prefix_gen():
            """
            Generates a sequence of characters in alphabetical order:
                -> 'A', 'B', 'C', ...

            When the alphabet is finished, the sequence will continue with the
            Cartesian product:
                -> 'AA', 'AB', 'AC', ...
            """
            alphabet = ascii_uppercase
            prefix = chr(ord(self.alias_prefix) + 1)
            yield prefix
            for n in count(1):
                seq = alphabet[alphabet.index(prefix):] if prefix else alphabet
                for s in product(seq, repeat=n):
                    yield ('').join(s)

                prefix = None

            return

        if self.alias_prefix != outer_query.alias_prefix:
            return
        local_recursion_limit = 127
        for pos, prefix in enumerate(prefix_gen()):
            if prefix not in self.subq_aliases:
                self.alias_prefix = prefix
                break
            if pos > local_recursion_limit:
                raise RuntimeError('Maximum recursion depth exceeded: too many subqueries.')

        self.subq_aliases = self.subq_aliases.union([self.alias_prefix])
        outer_query.subq_aliases = outer_query.subq_aliases.union(self.subq_aliases)
        change_map = OrderedDict()
        for pos, alias in enumerate(self.tables):
            new_alias = '%s%d' % (self.alias_prefix, pos)
            change_map[alias] = new_alias
            self.tables[pos] = new_alias

        self.change_aliases(change_map)

    def get_initial_alias(self):
        """
        Returns the first alias for this query, after increasing its reference
        count.
        """
        if self.tables:
            alias = self.tables[0]
            self.ref_alias(alias)
        else:
            alias = self.join(BaseTable(self.get_meta().db_table, None))
        return alias

    def count_active_tables(self):
        """
        Returns the number of tables in this query with a non-zero reference
        count. Note that after execution, the reference counts are zeroed, so
        tables added in compiler will not be seen by this method.
        """
        return len([ 1 for count in self.alias_refcount.values() if count ])

    def join(self, join, reuse=None):
        """
        Return an alias for the 'join', either reusing an existing alias for
        that join or creating a new one. 'join' is either a
        sql.datastructures.BaseTable or Join.

        The 'reuse' parameter can be either None which means all joins are
        reusable, or it can be a set containing the aliases that can be reused.

        A join is always created as LOUTER if the lhs alias is LOUTER to make
        sure chains like t1 LOUTER t2 INNER t3 aren't generated. All new
        joins are created as LOUTER if the join is nullable.
        """
        reuse = [ a for a, j in self.alias_map.items() if (reuse is None or a in reuse) and j == join
                ]
        if reuse:
            self.ref_alias(reuse[0])
            return reuse[0]
        else:
            alias, _ = self.table_alias(join.table_name, create=True)
            if join.join_type:
                if self.alias_map[join.parent_alias].join_type == LOUTER or join.nullable:
                    join_type = LOUTER
                else:
                    join_type = INNER
                join.join_type = join_type
            join.table_alias = alias
            self.alias_map[alias] = join
            return alias

    def join_parent_model(self, opts, model, alias, seen):
        """
        Makes sure the given 'model' is joined in the query. If 'model' isn't
        a parent of 'opts' or if it is None this method is a no-op.

        The 'alias' is the root alias for starting the join, 'seen' is a dict
        of model -> alias of existing joins. It must also contain a mapping
        of None -> some alias. This will be returned in the no-op case.
        """
        if model in seen:
            return seen[model]
        else:
            chain = opts.get_base_chain(model)
            if not chain:
                return alias
            curr_opts = opts
            for int_model in chain:
                if int_model in seen:
                    curr_opts = int_model._meta
                    alias = seen[int_model]
                    continue
                if not curr_opts.parents[int_model]:
                    curr_opts = int_model._meta
                    continue
                link_field = curr_opts.get_ancestor_link(int_model)
                _, _, _, joins, _ = self.setup_joins([
                 link_field.name], curr_opts, alias)
                curr_opts = int_model._meta
                alias = seen[int_model] = joins[(-1)]

            return alias or seen[None]

    def add_annotation(self, annotation, alias, is_summary=False):
        """
        Adds a single annotation expression to the Query
        """
        annotation = annotation.resolve_expression(self, allow_joins=True, reuse=None, summarize=is_summary)
        self.append_annotation_mask([alias])
        self.annotations[alias] = annotation
        return

    def _prepare_as_filter_value(self):
        return self.clone()

    def prepare_lookup_value(self, value, lookups, can_reuse, allow_joins=True):
        used_joins = []
        if len(lookups) == 0:
            lookups = [
             'exact']
        if value is None:
            if lookups[(-1)] not in ('exact', 'iexact'):
                raise ValueError('Cannot use None as a query value')
            return (True, ['isnull'], used_joins)
        else:
            if hasattr(value, 'resolve_expression'):
                pre_joins = self.alias_refcount.copy()
                value = value.resolve_expression(self, reuse=can_reuse, allow_joins=allow_joins)
                used_joins = [ k for k, v in self.alias_refcount.items() if v > pre_joins.get(k, 0) ]
            elif isinstance(value, (list, tuple)):
                processed_values = []
                used_joins = set()
                for sub_value in value:
                    if hasattr(sub_value, 'resolve_expression'):
                        pre_joins = self.alias_refcount.copy()
                        processed_values.append(sub_value.resolve_expression(self, reuse=can_reuse, allow_joins=allow_joins))
                        used_joins |= set(k for k, v in self.alias_refcount.items() if v > pre_joins.get(k, 0))

            if hasattr(value, '_prepare_as_filter_value'):
                value = value._prepare_as_filter_value()
                value.bump_prefix(self)
            if connections[DEFAULT_DB_ALIAS].features.interprets_empty_strings_as_nulls and lookups[(-1)] == 'exact' and value == '':
                value = True
                lookups[-1] = 'isnull'
            return (
             value, lookups, used_joins)

    def solve_lookup_type(self, lookup):
        """
        Solve the lookup type from the lookup (eg: 'foobar__id__icontains')
        """
        lookup_splitted = lookup.split(LOOKUP_SEP)
        if self._annotations:
            expression, expression_lookups = refs_expression(lookup_splitted, self.annotations)
            if expression:
                return (expression_lookups, (), expression)
        _, field, _, lookup_parts = self.names_to_path(lookup_splitted, self.get_meta())
        field_parts = lookup_splitted[0:len(lookup_splitted) - len(lookup_parts)]
        if len(lookup_parts) == 0:
            lookup_parts = [
             'exact']
        elif len(lookup_parts) > 1:
            if not field_parts:
                raise FieldError('Invalid lookup "%s" for model %s".' % (
                 lookup, self.get_meta().model.__name__))
        return (
         lookup_parts, field_parts, False)

    def check_query_object_type(self, value, opts, field):
        """
        Checks whether the object passed while querying is of the correct type.
        If not, it raises a ValueError specifying the wrong object.
        """
        if hasattr(value, '_meta'):
            if not check_rel_lookup_compatibility(value._meta.model, opts, field):
                raise ValueError('Cannot query "%s": Must be "%s" instance.' % (
                 value, opts.object_name))

    def check_related_objects(self, field, value, opts):
        """
        Checks the type of object passed to query relations.
        """
        if field.is_relation:
            if getattr(value, '_forced_pk', False) and not check_rel_lookup_compatibility(value.model, opts, field):
                raise ValueError('Cannot use QuerySet for "%s": Use a QuerySet for "%s".' % (
                 value.model._meta.object_name, opts.object_name))
            elif hasattr(value, '_meta'):
                self.check_query_object_type(value, opts, field)
            elif hasattr(value, '__iter__'):
                for v in value:
                    self.check_query_object_type(v, opts, field)

    def build_lookup(self, lookups, lhs, rhs):
        """
        Tries to extract transforms and lookup from given lhs.

        The lhs value is something that works like SQLExpression.
        The rhs value is what the lookup is going to compare against.
        The lookups is a list of names to extract using get_lookup()
        and get_transform().
        """
        lookups = lookups[:]
        while lookups:
            name = lookups[0]
            if len(lookups) == 1:
                final_lookup = lhs.get_lookup(name)
                if not final_lookup:
                    lhs = self.try_transform(lhs, name, lookups)
                    final_lookup = lhs.get_lookup('exact')
                return final_lookup(lhs, rhs)
            lhs = self.try_transform(lhs, name, lookups)
            lookups = lookups[1:]

    def try_transform(self, lhs, name, rest_of_lookups):
        """
        Helper method for build_lookup. Tries to fetch and initialize
        a transform for name parameter from lhs.
        """
        transform_class = lhs.get_transform(name)
        if transform_class:
            return transform_class(lhs)
        raise FieldError("Unsupported lookup '%s' for %s or join on the field not permitted." % (
         name, lhs.output_field.__class__.__name__))

    def build_filter(self, filter_expr, branch_negated=False, current_negated=False, can_reuse=None, connector=AND, allow_joins=True, split_subq=True):
        """
        Builds a WhereNode for a single filter clause, but doesn't add it
        to this Query. Query.add_q() will then add this filter to the where
        Node.

        The 'branch_negated' tells us if the current branch contains any
        negations. This will be used to determine if subqueries are needed.

        The 'current_negated' is used to determine if the current filter is
        negated or not and this will be used to determine if IS NULL filtering
        is needed.

        The difference between current_netageted and branch_negated is that
        branch_negated is set on first negation, but current_negated is
        flipped for each negation.

        Note that add_filter will not do any negating itself, that is done
        upper in the code by add_q().

        The 'can_reuse' is a set of reusable joins for multijoins.

        The method will create a filter clause that can be added to the current
        query. However, if the filter isn't added to the query then the caller
        is responsible for unreffing the joins used.
        """
        if isinstance(filter_expr, dict):
            raise FieldError('Cannot parse keyword query as dict')
        arg, value = filter_expr
        if not arg:
            raise FieldError('Cannot parse keyword query %r' % arg)
        lookups, parts, reffed_expression = self.solve_lookup_type(arg)
        if not allow_joins and len(parts) > 1:
            raise FieldError('Joined field references are not permitted in this query')
        value, lookups, used_joins = self.prepare_lookup_value(value, lookups, can_reuse, allow_joins)
        clause = self.where_class()
        if reffed_expression:
            condition = self.build_lookup(lookups, reffed_expression, value)
            clause.add(condition, AND)
            return (
             clause, [])
        else:
            opts = self.get_meta()
            alias = self.get_initial_alias()
            allow_many = not branch_negated or not split_subq
            try:
                field, sources, opts, join_list, path = self.setup_joins(parts, opts, alias, can_reuse=can_reuse, allow_many=allow_many)
                if isinstance(value, Iterator):
                    value = list(value)
                self.check_related_objects(field, value, opts)
                self._lookup_joins = join_list
            except MultiJoin as e:
                return self.split_exclude(filter_expr, LOOKUP_SEP.join(parts[:e.level]), can_reuse, e.names_with_path)

            if can_reuse is not None:
                can_reuse.update(join_list)
            used_joins = set(used_joins).union(set(join_list))
            targets, alias, join_list = self.trim_joins(sources, join_list, path)
            if field.is_relation:
                num_lookups = len(lookups)
                if num_lookups > 1:
                    raise FieldError(('Related Field got invalid lookup: {}').format(lookups[0]))
                assert num_lookups > 0
                lookup_class = field.get_lookup(lookups[0])
                if lookup_class is None:
                    raise FieldError(('Related Field got invalid lookup: {}').format(lookups[0]))
                if len(targets) == 1:
                    lhs = targets[0].get_col(alias, field)
                else:
                    lhs = MultiColSource(alias, targets, sources, field)
                condition = lookup_class(lhs, value)
                lookup_type = lookup_class.lookup_name
            else:
                col = targets[0].get_col(alias, field)
                condition = self.build_lookup(lookups, col, value)
                lookup_type = condition.lookup_name
            clause.add(condition, AND)
            require_outer = lookup_type == 'isnull' and value is True and not current_negated
            if current_negated and (lookup_type != 'isnull' or value is False):
                require_outer = True
                if lookup_type != 'isnull' and (self.is_nullable(targets[0]) or self.alias_map[join_list[(-1)]].join_type == LOUTER):
                    lookup_class = targets[0].get_lookup('isnull')
                    clause.add(lookup_class(targets[0].get_col(alias, sources[0]), False), AND)
            return (
             clause, used_joins if not require_outer else ())

    def add_filter(self, filter_clause):
        self.add_q(Q(**{filter_clause[0]: filter_clause[1]}))

    def add_q(self, q_object):
        """
        A preprocessor for the internal _add_q(). Responsible for doing final
        join promotion.
        """
        existing_inner = set(a for a in self.alias_map if self.alias_map[a].join_type == INNER)
        clause, _ = self._add_q(q_object, self.used_aliases)
        if clause:
            self.where.add(clause, AND)
        self.demote_joins(existing_inner)

    def _add_q(self, q_object, used_aliases, branch_negated=False, current_negated=False, allow_joins=True, split_subq=True):
        """
        Adds a Q-object to the current filter.
        """
        connector = q_object.connector
        current_negated = current_negated ^ q_object.negated
        branch_negated = branch_negated or q_object.negated
        target_clause = self.where_class(connector=connector, negated=q_object.negated)
        joinpromoter = JoinPromoter(q_object.connector, len(q_object.children), current_negated)
        for child in q_object.children:
            if isinstance(child, Node):
                child_clause, needed_inner = self._add_q(child, used_aliases, branch_negated, current_negated, allow_joins, split_subq)
                joinpromoter.add_votes(needed_inner)
            else:
                child_clause, needed_inner = self.build_filter(child, can_reuse=used_aliases, branch_negated=branch_negated, current_negated=current_negated, connector=connector, allow_joins=allow_joins, split_subq=split_subq)
                joinpromoter.add_votes(needed_inner)
            if child_clause:
                target_clause.add(child_clause, connector)

        needed_inner = joinpromoter.update_join_types(self)
        return (target_clause, needed_inner)

    def names_to_path(self, names, opts, allow_many=True, fail_on_missing=False):
        """
        Walks the list of names and turns them into PathInfo tuples. Note that
        a single name in 'names' can generate multiple PathInfos (m2m for
        example).

        'names' is the path of names to travel, 'opts' is the model Options we
        start the name resolving from, 'allow_many' is as for setup_joins().
        If fail_on_missing is set to True, then a name that can't be resolved
        will generate a FieldError.

        Returns a list of PathInfo tuples. In addition returns the final field
        (the last used join field), and target (which is a field guaranteed to
        contain the same value as the final field). Finally, the method returns
        those names that weren't found (which are likely transforms and the
        final lookup).
        """
        path, names_with_path = [], []
        for pos, name in enumerate(names):
            cur_names_with_path = (
             name, [])
            if name == 'pk':
                name = opts.pk.name
            field = None
            try:
                field = opts.get_field(name)
            except FieldDoesNotExist:
                if name in self.annotation_select:
                    field = self.annotation_select[name].output_field
                elif pos == 0:
                    for rel in opts.related_objects:
                        if name == rel.related_model._meta.model_name and rel.related_name == rel.related_model._meta.default_related_name:
                            related_name = rel.related_name
                            field = opts.get_field(related_name)
                            warnings.warn("Query lookup '%s' is deprecated in favor of Meta.default_related_name '%s'." % (
                             name, related_name), RemovedInDjango20Warning, 2)
                            break

            if field is not None:
                if field.is_relation and not field.related_model:
                    raise FieldError('Field %r does not generate an automatic reverse relation and therefore cannot be used for reverse querying. If it is a GenericForeignKey, consider adding a GenericRelation.' % name)
                try:
                    model = field.model._meta.concrete_model
                except AttributeError:
                    model = None

            else:
                pos -= 1
                if pos == -1 or fail_on_missing:
                    field_names = list(get_field_names_from_opts(opts))
                    available = sorted(field_names + list(self.annotation_select))
                    raise FieldError("Cannot resolve keyword '%s' into field. Choices are: %s" % (
                     name, (', ').join(available)))
                break
            if model is not opts.model:
                path_to_parent = opts.get_path_to_parent(model)
                if path_to_parent:
                    path.extend(path_to_parent)
                    cur_names_with_path[1].extend(path_to_parent)
                    opts = path_to_parent[(-1)].to_opts
            if hasattr(field, 'get_path_info'):
                pathinfos = field.get_path_info()
                if not allow_many:
                    for inner_pos, p in enumerate(pathinfos):
                        if p.m2m:
                            cur_names_with_path[1].extend(pathinfos[0:inner_pos + 1])
                            names_with_path.append(cur_names_with_path)
                            raise MultiJoin(pos + 1, names_with_path)

                last = pathinfos[(-1)]
                path.extend(pathinfos)
                final_field = last.join_field
                opts = last.to_opts
                targets = last.target_fields
                cur_names_with_path[1].extend(pathinfos)
                names_with_path.append(cur_names_with_path)
            else:
                final_field = field
                targets = (field,)
                if fail_on_missing and pos + 1 != len(names):
                    raise FieldError("Cannot resolve keyword %r into field. Join on '%s' not permitted." % (
                     names[(pos + 1)], name))
                break

        return (
         path, final_field, targets, names[pos + 1:])

    def setup_joins(self, names, opts, alias, can_reuse=None, allow_many=True):
        """
        Compute the necessary table joins for the passage through the fields
        given in 'names'. 'opts' is the Options class for the current model
        (which gives the table we are starting from), 'alias' is the alias for
        the table to start the joining from.

        The 'can_reuse' defines the reverse foreign key joins we can reuse. It
        can be None in which case all joins are reusable or a set of aliases
        that can be reused. Note that non-reverse foreign keys are always
        reusable when using setup_joins().

        If 'allow_many' is False, then any reverse foreign key seen will
        generate a MultiJoin exception.

        Returns the final field involved in the joins, the target field (used
        for any 'where' constraint), the final 'opts' value, the joins and the
        field path travelled to generate the joins.

        The target field is the field containing the concrete value. Final
        field can be something different, for example foreign key pointing to
        that value. Final field is needed for example in some value
        conversions (convert 'obj' in fk__id=obj to pk val using the foreign
        key field for example).
        """
        joins = [
         alias]
        path, final_field, targets, rest = self.names_to_path(names, opts, allow_many, fail_on_missing=True)
        for join in path:
            opts = join.to_opts
            if join.direct:
                nullable = self.is_nullable(join.join_field)
            else:
                nullable = True
            connection = Join(opts.db_table, alias, None, INNER, join.join_field, nullable)
            reuse = can_reuse if join.m2m else None
            alias = self.join(connection, reuse=reuse)
            joins.append(alias)

        return (
         final_field, targets, opts, joins, path)

    def trim_joins(self, targets, joins, path):
        """
        The 'target' parameter is the final field being joined to, 'joins'
        is the full list of join aliases. The 'path' contain the PathInfos
        used to create the joins.

        Returns the final target field and table alias and the new active
        joins.

        We will always trim any direct join if we have the target column
        available already in the previous table. Reverse joins can't be
        trimmed as we don't know if there is anything on the other side of
        the join.
        """
        joins = joins[:]
        for pos, info in enumerate(reversed(path)):
            if len(joins) == 1 or not info.direct:
                break
            join_targets = set(t.column for t in info.join_field.foreign_related_fields)
            cur_targets = set(t.column for t in targets)
            if not cur_targets.issubset(join_targets):
                break
            targets_dict = {r[1].column:r[0] for r in info.join_field.related_fields if r[1].column in cur_targets}
            targets = tuple(targets_dict[t.column] for t in targets)
            self.unref_alias(joins.pop())

        return (
         targets, joins[(-1)], joins)

    def resolve_ref(self, name, allow_joins=True, reuse=None, summarize=False):
        if not allow_joins and LOOKUP_SEP in name:
            raise FieldError('Joined field references are not permitted in this query')
        if name in self.annotations:
            if summarize:
                return Ref(name, self.annotation_select[name])
            else:
                return self.annotation_select[name]

        else:
            field_list = name.split(LOOKUP_SEP)
            field, sources, opts, join_list, path = self.setup_joins(field_list, self.get_meta(), self.get_initial_alias(), reuse)
            targets, _, join_list = self.trim_joins(sources, join_list, path)
            if len(targets) > 1:
                raise FieldError("Referencing multicolumn fields with F() objects isn't supported")
            if reuse is not None:
                reuse.update(join_list)
            col = targets[0].get_col(join_list[(-1)], sources[0])
            return col
        return

    def split_exclude(self, filter_expr, prefix, can_reuse, names_with_path):
        """
        When doing an exclude against any kind of N-to-many relation, we need
        to use a subquery. This method constructs the nested query, given the
        original exclude filter (filter_expr) and the portion up to the first
        N-to-many relation field.

        As an example we could have original filter ~Q(child__name='foo').
        We would get here with filter_expr = child__name, prefix = child and
        can_reuse is a set of joins usable for filters in the original query.

        We will turn this into equivalent of:
            WHERE NOT (pk IN (SELECT parent_id FROM thetable
                              WHERE name = 'foo' AND parent_id IS NOT NULL))

        It might be worth it to consider using WHERE NOT EXISTS as that has
        saner null handling, and is easier for the backend's optimizer to
        handle.
        """
        query = Query(self.model)
        query.add_filter(filter_expr)
        query.clear_ordering(True)
        trimmed_prefix, contains_louter = query.trim_start(names_with_path)
        col = query.select[0]
        select_field = col.target
        alias = col.alias
        if self.is_nullable(select_field):
            lookup_class = select_field.get_lookup('isnull')
            lookup = lookup_class(select_field.get_col(alias), False)
            query.where.add(lookup, AND)
        if alias in can_reuse:
            pk = select_field.model._meta.pk
            query.bump_prefix(self)
            lookup_class = select_field.get_lookup('exact')
            lookup = lookup_class(pk.get_col(query.select[0].alias), pk.get_col(alias))
            query.where.add(lookup, AND)
            query.external_aliases.add(alias)
        condition, needed_inner = self.build_filter((
         '%s__in' % trimmed_prefix, query), current_negated=True, branch_negated=True, can_reuse=can_reuse)
        if contains_louter:
            or_null_condition, _ = self.build_filter((
             '%s__isnull' % trimmed_prefix, True), current_negated=True, branch_negated=True, can_reuse=can_reuse)
            condition.add(or_null_condition, OR)
        return (
         condition, needed_inner)

    def set_empty(self):
        self.where.add(NothingNode(), AND)

    def is_empty(self):
        return any(isinstance(c, NothingNode) for c in self.where.children)

    def set_limits(self, low=None, high=None):
        """
        Adjusts the limits on the rows retrieved. We use low/high to set these,
        as it makes it more Pythonic to read and write. When the SQL query is
        created, they are converted to the appropriate offset and limit values.

        Any limits passed in here are applied relative to the existing
        constraints. So low is added to the current low value and both will be
        clamped to any existing high value.
        """
        if high is not None:
            if self.high_mark is not None:
                self.high_mark = min(self.high_mark, self.low_mark + high)
            else:
                self.high_mark = self.low_mark + high
        if low is not None:
            if self.high_mark is not None:
                self.low_mark = min(self.high_mark, self.low_mark + low)
            else:
                self.low_mark = self.low_mark + low
        if self.low_mark == self.high_mark:
            self.set_empty()
        return

    def clear_limits(self):
        """
        Clears any existing limits.
        """
        self.low_mark, self.high_mark = (0, None)
        return

    def can_filter(self):
        """
        Returns True if adding filters to this instance is still possible.

        Typically, this means no limits or offsets have been put on the results.
        """
        return not self.low_mark and self.high_mark is None

    def clear_select_clause(self):
        """
        Removes all fields from SELECT clause.
        """
        self.select = []
        self.default_cols = False
        self.select_related = False
        self.set_extra_mask(())
        self.set_annotation_mask(())

    def clear_select_fields(self):
        """
        Clears the list of fields to select (but not extra_select columns).
        Some queryset types completely replace any existing list of select
        columns.
        """
        self.select = []
        self.values_select = []

    def add_select(self, col):
        self.default_cols = False
        self.select.append(col)

    def set_select(self, cols):
        self.default_cols = False
        self.select = cols

    def add_distinct_fields(self, *field_names):
        """
        Adds and resolves the given fields to the query's "distinct on" clause.
        """
        self.distinct_fields = field_names
        self.distinct = True

    def add_fields(self, field_names, allow_m2m=True):
        """
        Adds the given (model) fields to the select set. The field names are
        added in the order specified.
        """
        alias = self.get_initial_alias()
        opts = self.get_meta()
        try:
            for name in field_names:
                _, targets, _, joins, path = self.setup_joins(name.split(LOOKUP_SEP), opts, alias, allow_many=allow_m2m)
                targets, final_alias, joins = self.trim_joins(targets, joins, path)
                for target in targets:
                    self.add_select(target.get_col(final_alias))

        except MultiJoin:
            raise FieldError("Invalid field name: '%s'" % name)
        except FieldError:
            if LOOKUP_SEP in name:
                raise
            else:
                names = sorted(list(get_field_names_from_opts(opts)) + list(self.extra) + list(self.annotation_select))
                raise FieldError('Cannot resolve keyword %r into field. Choices are: %s' % (
                 name, (', ').join(names)))

    def add_ordering(self, *ordering):
        """
        Adds items from the 'ordering' sequence to the query's "order by"
        clause. These items are either field names (not column names) --
        possibly with a direction prefix ('-' or '?') -- or OrderBy
        expressions.

        If 'ordering' is empty, all ordering is cleared from the query.
        """
        errors = []
        for item in ordering:
            if not hasattr(item, 'resolve_expression') and not ORDER_PATTERN.match(item):
                errors.append(item)
            if getattr(item, 'contains_aggregate', False):
                raise FieldError('Using an aggregate in order_by() without also including it in annotate() is not allowed: %s' % item)

        if errors:
            raise FieldError('Invalid order_by arguments: %s' % errors)
        if ordering:
            self.order_by.extend(ordering)
        else:
            self.default_ordering = False

    def clear_ordering(self, force_empty):
        """
        Removes any ordering settings. If 'force_empty' is True, there will be
        no ordering in the resulting query (not even the model's default).
        """
        self.order_by = []
        self.extra_order_by = ()
        if force_empty:
            self.default_ordering = False

    def set_group_by(self):
        """
        Expands the GROUP BY clause required by the query.

        This will usually be the set of all non-aggregate fields in the
        return data. If the database backend supports grouping by the
        primary key, and the query would be equivalent, the optimization
        will be made automatically.
        """
        self.group_by = []
        for col in self.select:
            self.group_by.append(col)

        if self.annotation_select:
            for alias, annotation in six.iteritems(self.annotation_select):
                for col in annotation.get_group_by_cols():
                    self.group_by.append(col)

    def add_select_related(self, fields):
        """
        Sets up the select_related data structure so that we only select
        certain related models (as opposed to all models, when
        self.select_related=True).
        """
        if isinstance(self.select_related, bool):
            field_dict = {}
        else:
            field_dict = self.select_related
        for field in fields:
            d = field_dict
            for part in field.split(LOOKUP_SEP):
                d = d.setdefault(part, {})

        self.select_related = field_dict

    def add_extra(self, select, select_params, where, params, tables, order_by):
        """
        Adds data to the various extra_* attributes for user-created additions
        to the query.
        """
        if select:
            select_pairs = OrderedDict()
            if select_params:
                param_iter = iter(select_params)
            else:
                param_iter = iter([])
            for name, entry in select.items():
                entry = force_text(entry)
                entry_params = []
                pos = entry.find('%s')
                while pos != -1:
                    if pos == 0 or entry[(pos - 1)] != '%':
                        entry_params.append(next(param_iter))
                    pos = entry.find('%s', pos + 2)

                select_pairs[name] = (
                 entry, entry_params)

            self.extra.update(select_pairs)
        if where or params:
            self.where.add(ExtraWhere(where, params), AND)
        if tables:
            self.extra_tables += tuple(tables)
        if order_by:
            self.extra_order_by = order_by

    def clear_deferred_loading(self):
        """
        Remove any fields from the deferred loading set.
        """
        self.deferred_loading = (
         set(), True)

    def add_deferred_loading(self, field_names):
        """
        Add the given list of model field names to the set of fields to
        exclude from loading from the database when automatic column selection
        is done. The new field names are added to any existing field names that
        are deferred (or removed from any existing field names that are marked
        as the only ones for immediate loading).
        """
        existing, defer = self.deferred_loading
        if defer:
            self.deferred_loading = (existing.union(field_names), True)
        else:
            self.deferred_loading = (
             existing.difference(field_names), False)

    def add_immediate_loading(self, field_names):
        """
        Add the given list of model field names to the set of fields to
        retrieve when the SQL is executed ("immediate loading" fields). The
        field names replace any existing immediate loading field names. If
        there are field names already specified for deferred loading, those
        names are removed from the new field_names before storing the new names
        for immediate loading. (That is, immediate loading overrides any
        existing immediate values, but respects existing deferrals.)
        """
        existing, defer = self.deferred_loading
        field_names = set(field_names)
        if 'pk' in field_names:
            field_names.remove('pk')
            field_names.add(self.get_meta().pk.name)
        if defer:
            self.deferred_loading = (
             field_names.difference(existing), False)
        else:
            self.deferred_loading = (
             field_names, False)

    def get_loaded_field_names(self):
        """
        If any fields are marked to be deferred, returns a dictionary mapping
        models to a set of names in those fields that will be loaded. If a
        model is not in the returned dictionary, none of its fields are
        deferred.

        If no fields are marked for deferral, returns an empty dictionary.
        """
        try:
            return self._loaded_field_names_cache
        except AttributeError:
            collection = {}
            self.deferred_to_data(collection, self.get_loaded_field_names_cb)
            self._loaded_field_names_cache = collection
            return collection

    def get_loaded_field_names_cb(self, target, model, fields):
        """
        Callback used by get_deferred_field_names().
        """
        target[model] = {f.attname for f in fields}

    def set_annotation_mask(self, names):
        """Set the mask of annotations that will actually be returned by the SELECT"""
        if names is None:
            self.annotation_select_mask = None
        else:
            self.annotation_select_mask = set(names)
        self._annotation_select_cache = None
        return

    def append_annotation_mask(self, names):
        if self.annotation_select_mask is not None:
            self.set_annotation_mask(set(names).union(self.annotation_select_mask))
        return

    def set_extra_mask(self, names):
        """
        Set the mask of extra select items that will be returned by SELECT,
        we don't actually remove them from the Query since they might be used
        later
        """
        if names is None:
            self.extra_select_mask = None
        else:
            self.extra_select_mask = set(names)
        self._extra_select_cache = None
        return

    def set_values(self, fields):
        self.select_related = False
        self.clear_deferred_loading()
        self.clear_select_fields()
        if self.group_by is True:
            self.add_fields((f.attname for f in self.model._meta.concrete_fields), False)
            self.set_group_by()
            self.clear_select_fields()
        if fields:
            field_names = []
            extra_names = []
            annotation_names = []
            if not self._extra and not self._annotations:
                field_names = list(fields)
            else:
                self.default_cols = False
                for f in fields:
                    if f in self.extra_select:
                        extra_names.append(f)
                    elif f in self.annotation_select:
                        annotation_names.append(f)
                    else:
                        field_names.append(f)

            self.set_extra_mask(extra_names)
            self.set_annotation_mask(annotation_names)
        else:
            field_names = [ f.attname for f in self.model._meta.concrete_fields ]
        self.values_select = field_names
        self.add_fields(field_names, True)

    @property
    def annotation_select(self):
        """The OrderedDict of aggregate columns that are not masked, and should
        be used in the SELECT clause.

        This result is cached for optimization purposes.
        """
        if self._annotation_select_cache is not None:
            return self._annotation_select_cache
        else:
            if not self._annotations:
                return {}
            else:
                if self.annotation_select_mask is not None:
                    self._annotation_select_cache = OrderedDict((k, v) for k, v in self.annotations.items() if k in self.annotation_select_mask)
                    return self._annotation_select_cache
                return self.annotations

            return

    @property
    def extra_select(self):
        if self._extra_select_cache is not None:
            return self._extra_select_cache
        else:
            if not self._extra:
                return {}
            else:
                if self.extra_select_mask is not None:
                    self._extra_select_cache = OrderedDict((k, v) for k, v in self.extra.items() if k in self.extra_select_mask)
                    return self._extra_select_cache
                return self.extra

            return

    def trim_start(self, names_with_path):
        """
        Trims joins from the start of the join path. The candidates for trim
        are the PathInfos in names_with_path structure that are m2m joins.

        Also sets the select column so the start matches the join.

        This method is meant to be used for generating the subquery joins &
        cols in split_exclude().

        Returns a lookup usable for doing outerq.filter(lookup=self). Returns
        also if the joins in the prefix contain a LEFT OUTER join.
        _"""
        all_paths = []
        for _, paths in names_with_path:
            all_paths.extend(paths)

        contains_louter = False
        lookup_tables = [ t for t in self.tables if t in self._lookup_joins or t == self.tables[0] ]
        for trimmed_paths, path in enumerate(all_paths):
            if path.m2m:
                break
            if self.alias_map[lookup_tables[(trimmed_paths + 1)]].join_type == LOUTER:
                contains_louter = True
            alias = lookup_tables[trimmed_paths]
            self.unref_alias(alias)

        join_field = path.join_field.field
        paths_in_prefix = trimmed_paths
        trimmed_prefix = []
        for name, path in names_with_path:
            if paths_in_prefix - len(path) < 0:
                break
            trimmed_prefix.append(name)
            paths_in_prefix -= len(path)

        trimmed_prefix.append(join_field.foreign_related_fields[0].name)
        trimmed_prefix = LOOKUP_SEP.join(trimmed_prefix)
        if self.alias_map[lookup_tables[(trimmed_paths + 1)]].join_type != LOUTER:
            select_fields = [ r[0] for r in join_field.related_fields ]
            select_alias = lookup_tables[(trimmed_paths + 1)]
            self.unref_alias(lookup_tables[trimmed_paths])
            extra_restriction = join_field.get_extra_restriction(self.where_class, None, lookup_tables[(trimmed_paths + 1)])
            if extra_restriction:
                self.where.add(extra_restriction, AND)
        else:
            select_fields = [ r[1] for r in join_field.related_fields ]
            select_alias = lookup_tables[trimmed_paths]
        for table in self.tables:
            if self.alias_refcount[table] > 0:
                self.alias_map[table] = BaseTable(self.alias_map[table].table_name, table)
                break

        self.set_select([ f.get_col(select_alias) for f in select_fields ])
        return (trimmed_prefix, contains_louter)

    def is_nullable(self, field):
        """
        A helper to check if the given field should be treated as nullable.

        Some backends treat '' as null and Django treats such fields as
        nullable for those backends. In such situations field.null can be
        False even if we should treat the field as nullable.
        """
        if connections[DEFAULT_DB_ALIAS].features.interprets_empty_strings_as_nulls and field.empty_strings_allowed:
            return True
        else:
            return field.null

    def as_subquery_filter(self, db):
        self._db = db
        self.subquery = True
        if self.low_mark == 0 and self.high_mark is None and not self.distinct_fields and not self.select_for_update:
            self.clear_ordering(True)
        return self


def get_order_dir(field, default='ASC'):
    """
    Returns the field name and direction for an order specification. For
    example, '-foo' is returned as ('foo', 'DESC').

    The 'default' param is used to indicate which way no prefix (or a '+'
    prefix) should sort. The '-' prefix always sorts the opposite way.
    """
    dirn = ORDER_DIR[default]
    if field[0] == '-':
        return (field[1:], dirn[1])
    return (
     field, dirn[0])


def add_to_dict(data, key, value):
    """
    A helper function to add "value" to the set of values for "key", whether or
    not "key" already exists.
    """
    if key in data:
        data[key].add(value)
    else:
        data[key] = {
         value}


def is_reverse_o2o(field):
    """
    A little helper to check if the given field is reverse-o2o. The field is
    expected to be some sort of relation field or related object.
    """
    return field.is_relation and field.one_to_one and not field.concrete


class JoinPromoter(object):
    """
    A class to abstract away join promotion problems for complex filter
    conditions.
    """

    def __init__(self, connector, num_children, negated):
        self.connector = connector
        self.negated = negated
        if self.negated:
            if connector == AND:
                self.effective_connector = OR
            else:
                self.effective_connector = AND
        else:
            self.effective_connector = self.connector
        self.num_children = num_children
        self.votes = Counter()

    def add_votes(self, votes):
        """
        Add single vote per item to self.votes. Parameter can be any
        iterable.
        """
        self.votes.update(votes)

    def update_join_types(self, query):
        """
        Change join types so that the generated query is as efficient as
        possible, but still correct. So, change as many joins as possible
        to INNER, but don't make OUTER joins INNER if that could remove
        results from the query.
        """
        to_promote = set()
        to_demote = set()
        for table, votes in self.votes.items():
            if self.effective_connector == 'OR' and votes < self.num_children:
                to_promote.add(table)
            if self.effective_connector == 'AND' or self.effective_connector == 'OR' and votes == self.num_children:
                to_demote.add(table)

        query.promote_joins(to_promote)
        query.demote_joins(to_demote)
        return to_demote