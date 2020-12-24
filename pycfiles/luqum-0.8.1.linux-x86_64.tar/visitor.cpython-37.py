# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/luqum/elasticsearch/visitor.py
# Compiled at: 2019-08-01 20:03:10
# Size of source mod 2**32: 16036 bytes
import warnings
from luqum.elasticsearch.tree import ElasticSearchItemFactory
from luqum.exceptions import OrAndAndOnSameLevel
from luqum.tree import OrOperation, AndOperation, UnknownOperation
from luqum.tree import Word
from .tree import EMust, EMustNot, EShould, EWord, EPhrase, ERange, ENested
from ..utils import LuceneTreeVisitorV2, normalize_nested_fields_specs, normalize_object_fields_specs, flatten_nested_fields_specs
from ..check import CheckNestedFields
from ..naming import get_name

class ElasticsearchQueryBuilder(LuceneTreeVisitorV2):
    __doc__ = '\n    Query builder to convert a Tree in an Elasticsearch query dsl (json)\n\n    .. warning:: there are some limitations\n\n        - mix of AND and OR on same level in expressions is not supported\n          has this leads to unpredictable results (see `this article`_)\n\n        - for full text fields,\n          `zero_terms_query` parameter of `match queries`_\n          is managed at best according to where the terms appears.\n          Lucene would just remove fields with only stop words\n          while this query builder have to retain all expressions,\n          even if is only made of stop words.\n          So in the case of an expression appearing in `AND` expression,\n          it will be set to "all"\n          while it will be set to "none" if it\'s part of a `OR` on `AND NOT`\n          to avoid influencing the rest of the query.\n          Some edge case like having all terms resolving to stop words\n          may however lead to different results than string_query..\n\n    .. _`this article`: https://lucidworks.com/blog/2011/12/28/why-not-and-or-and-not/\n    .. _`match queries`:\n        https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html\n    '
    SHOULD = 'should'
    MUST = 'must'
    CONTEXT_ANALYZE_MARKER = 'analyzed'
    CONTEXT_FIELD_PREFIX = 'field_prefix'

    def __init__(self, default_operator=SHOULD, default_field='text', not_analyzed_fields=None, nested_fields=None, object_fields=None, sub_fields=None, field_options=None, match_word_as_phrase=False):
        """
        :param default_operator: to replace blank operator (MUST or SHOULD)
        :param default_field: to search
        :param not_analyzed_fields: field that are not analyzed in ES
          (do not forget to include eventual sub fields)
        :param nested_fields: dict contains fields that are nested in ES
            each nested fields contains
            either a dict of nested fields
            (if some of them are also nested)
            or a list of nesdted fields (this is for commodity)

            exemple, a where record contains multiple authors,
            each with one name and multiple books.
            Each book has on title but multiple formats with on type each::

                'author': {
                    'name': None,
                    'book': {
                        'format': ['type'],
                        'title': None
                    }
                },
        :param object_fields: list containing full qualified names of object fields.
          You may also use a spec similar to the one used for nested_fields.
          None, will accept all non nested fields as object fields.
        :param sub_fields: list containing full qualified names of sub fields.
          None, will accept all non nested fields or object fields as sub fields.
        :param dict field_options: allows you to give defaults options for each fields.
          They will be applied unless, overwritten by generated parameters.
          For match query, the `match_type` parameter modifies the type of match query.
        :param bool match_word_as_phrase: if True,
          word expressions are matched using `match_phrase` instead of `match`.
          This options mainly keeps stability with 0.6 version.
          It may be removed in the future.

        .. note::
            some of the parameters above
            can be deduced from elasticsearch index configuration.
            see :py:meth:`luqum.elasticsearch.schema.SchemaAnalyzer.query_builder_options`

        """
        if not_analyzed_fields:
            self._not_analyzed_fields = not_analyzed_fields
        else:
            self._not_analyzed_fields = []
        self.nested_fields = self._normalize_nested_fields(nested_fields)
        self._nested_prefixes = set((k.rsplit('.', 1)[0] for k in flatten_nested_fields_specs(self.nested_fields)))
        self.object_fields = self._normalize_object_fields(object_fields)
        self.sub_fields = sub_fields
        self.field_options = field_options or {}
        self.default_operator = default_operator
        self.default_field = default_field
        self.es_item_factory = ElasticSearchItemFactory(no_analyze=(self._not_analyzed_fields),
          nested_fields=(self.nested_fields),
          field_options=(self.field_options))
        self.nesting_checker = CheckNestedFields(nested_fields=(self.nested_fields),
          object_fields=(self.object_fields),
          sub_fields=(self.sub_fields))
        if match_word_as_phrase:
            warnings.warn('match_word_as_phrase is a transient option to keep compatibility with previous versions.\nConsider wrapping your expressions in quotes (maybe using a transformer) or forcing type in field_options.', PendingDeprecationWarning)
        self.match_word_as_phrase = match_word_as_phrase

    def _field_prefix(self, context):
        if context is not None:
            return context.get(self.CONTEXT_FIELD_PREFIX, [])
        return []

    def _fields(self, context):
        default = [
         self.default_field]
        if context is not None:
            return context.get(self.CONTEXT_FIELD_PREFIX, default)
        return default

    def _split_nested(self, node, context):
        """split the node name to its nesting
        """
        names = node.name.split('.')
        prefix = self._field_prefix(context)
        for i in range(len(names)):
            nested_prefix = '.'.join(prefix + names[:-i or None])
            if nested_prefix in self._nested_prefixes:
                break
        else:
            nested_prefix = None

        return nested_prefix

    def _is_analyzed(self, context):
        """return if current search field is analyzed
        """
        marker = context.get(self.CONTEXT_ANALYZE_MARKER) if context is not None else None
        if marker is None:
            return self.default_field not in self._not_analyzed_fields
        return marker

    def _normalize_nested_fields(self, nested_fields):
        return normalize_nested_fields_specs(nested_fields)

    def _normalize_object_fields(self, object_fields):
        return normalize_object_fields_specs(object_fields)

    def simplify_if_same(self, children, current_node):
        """
        If two same operation are nested, then simplify
        Should be use only with should and must operations because Not(Not(x))
        can't be simplified as Not(x)
        :param children:
        :param current_node:
        :return:
        """
        for child in children:
            if type(child) is type(current_node):
                yield from self.simplify_if_same(child.children, current_node)
            else:
                yield child

    def _get_operator_extract(self, binary_operation, delta=8):
        """
        Return an extract around the operator
        :param binary_operation: operator to extract
        :param delta: nb of characters to extract before and after the operator
        :return: str

        ::
            >>> operation = OrOperation(Word('Python'), Word('Monty'))
            >>> builder = ElasticsearchQueryBuilder()
            >>> builder._get_operator_extract(operation, 3)
            'hon OR Mon'
        """
        node_str = str(binary_operation)
        child_str_1 = str(binary_operation.children[0])
        child_str_2 = str(binary_operation.children[1])
        middle_length = len(node_str) - len(child_str_1) - len(child_str_2)
        position = node_str.find(child_str_2)
        if position - middle_length - delta >= 0:
            start = position - middle_length - delta
        else:
            start = 0
        end = position + delta
        return node_str[start:end]

    def _is_must(self, operation):
        """
        Returns True if the node is a AndOperation or an UnknownOperation when
        the default operator is MUST
        :param node: to check
        :return: Boolean

        ::
            >>> ElasticsearchQueryBuilder(
            ...     default_operator=ElasticsearchQueryBuilder.MUST
            ... )._is_must(AndOperation(Word('Monty'), Word('Python')))
            True
        """
        return isinstance(operation, AndOperation) or isinstance(operation, UnknownOperation) and self.default_operator == ElasticsearchQueryBuilder.MUST

    def _is_should(self, operation):
        """
        Returns True if the node is a OrOperation or an UnknownOperation when
        the default operator is SHOULD

        ::
            >>> ElasticsearchQueryBuilder(
            ...     default_operator=ElasticsearchQueryBuilder.MUST
            ... )._is_should(OrOperation(Word('Monty'), Word('Python')))
            True
        """
        return isinstance(operation, OrOperation) or isinstance(operation, UnknownOperation) and self.default_operator == ElasticsearchQueryBuilder.SHOULD

    def _yield_nested_children(self, parent, children):
        """
        Raise if a OR (should) is in a AND (must) without being in parenthesis::

            >>> builder = ElasticsearchQueryBuilder()
            >>> op = OrOperation(Word('yo'), OrOperation(Word('lo'), Word('py')))
            >>> list(builder._yield_nested_children(op, op.children))
            [Word('yo'), OrOperation(Word('lo'), Word('py'))]

            >>> op = OrOperation(Word('yo'), AndOperation(Word('lo'), Word('py')))
            >>> list(builder._yield_nested_children(op, op.children))
            Traceback (most recent call last):
                ...
            luqum.exceptions.OrAndAndOnSameLevel: lo AND py
        """
        for child in children:
            if not (self._is_should(parent) and self._is_must(child)):
                if self._is_must(parent):
                    if self._is_should(child):
                        raise OrAndAndOnSameLevel(self._get_operator_extract(child))
                yield child

    def _binary_operation(self, cls, node, parents, context):
        children = self.simplify_if_same(node.children, node)
        children = self._yield_nested_children(node, children)
        items = [self.visit(child, parents + [node], context) for child in children]
        return self.es_item_factory.build(cls, items)

    def _must_operation(self, *args, **kwargs):
        return (self._binary_operation)(EMust, *args, **kwargs)

    def _should_operation(self, *args, **kwargs):
        return (self._binary_operation)(EShould, *args, **kwargs)

    def visit_and_operation(self, *args, **kwargs):
        return (self._must_operation)(*args, **kwargs)

    def visit_or_operation(self, *args, **kwargs):
        return (self._should_operation)(*args, **kwargs)

    def visit_search_field(self, node, parents, context):
        child_context = dict(context) if context is not None else {}
        prefix = self._field_prefix(context) + node.name.split('.')
        name = '.'.join(prefix)
        child_context[self.CONTEXT_ANALYZE_MARKER] = name not in self._not_analyzed_fields
        child_context[self.CONTEXT_FIELD_PREFIX] = prefix
        enode = self.visit(node.children[0], parents + [node], child_context)
        nested_path = self._split_nested(node, context)
        skip_nesting = isinstance(enode, ENested)
        if nested_path is not None:
            if not skip_nesting:
                enode = self.es_item_factory.build(ENested, nested_path=nested_path, items=enode)
        return enode

    def visit_not(self, node, parents, context):
        items = [self.visit(n, parents + [node], context) for n in self.simplify_if_same(node.children, node)]
        return self.es_item_factory.build(EMustNot, items)

    def visit_prohibit(self, *args, **kwargs):
        return (self.visit_not)(*args, **kwargs)

    def visit_plus(self, *args, **kwargs):
        return (self._must_operation)(*args, **kwargs)

    def visit_unknown_operation(self, *args, **kwargs):
        if self.default_operator == self.SHOULD:
            return (self._should_operation)(*args, **kwargs)
        return (self._must_operation)(*args, **kwargs)

    def visit_boost(self, node, parents, context):
        eword = self.visit(node.children[0], parents + [node], context)
        eword.boost = float(node.force)
        return eword

    def visit_fuzzy(self, node, parents, context):
        eword = self.visit(node.term, parents + [node], context)
        eword.fuzziness = float(node.degree)
        return eword

    def visit_proximity(self, node, parents, context):
        ephrase = self.visit(node.term, parents + [node], context)
        if self._is_analyzed(context):
            ephrase.slop = float(node.degree)
        else:
            ephrase.fuzziness = float(node.degree)
        return ephrase

    def visit_word(self, node, parents, context):
        if self._is_analyzed(context):
            if self.match_word_as_phrase:
                method = 'match_phrase'
            else:
                method = 'match'
        else:
            method = 'term'
        return self.es_item_factory.build(EWord,
          q=(node.value),
          method=method,
          fields=(self._fields(context)),
          _name=(get_name(node)))

    def visit_phrase(self, node, parents, context):
        if self._is_analyzed(context):
            return self.es_item_factory.build(EPhrase,
              phrase=(node.value),
              fields=(self._fields(context)),
              _name=(get_name(node)))
        return self.es_item_factory.build(EWord,
          q=(node.value[1:-1]),
          fields=(self._fields(context)),
          _name=(get_name(node)))

    def visit_range(self, node, parents, context):
        kwargs = {'gte' if node.include_low else 'gt': node.low.value, 
         'lte' if node.include_high else 'lt': node.high.value}
        return (self.es_item_factory.build)(
 ERange, _name=get_name(node), 
         fields=self._fields(context), **kwargs)

    def visit_group(self, node, parents, context):
        return self.visit(node.expr, parents + [node], context)

    def visit_field_group(self, node, parents, context):
        fields = self.visit(node.expr, parents + [node], context)
        return fields

    def __call__(self, tree):
        """Calling the query builder returns
        you the json compatible structure corresponding to the request tree passed in parameter

        :param luqum.tree.Item tree: a luqum parse tree
        :return dict:
        """
        self.nesting_checker(tree)
        return self.visit(tree).json