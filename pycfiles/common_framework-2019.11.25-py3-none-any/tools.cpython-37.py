# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/templatetags/tools.py
# Compiled at: 2018-07-09 09:23:18
# Size of source mod 2**32: 6174 bytes
from django.http import QueryDict
from django.template import Library
from django.utils.formats import localize
register = Library()

@register.filter(name='meta')
def filter_meta(instance, key):
    """
    Récupération d'une métadonnée sur une instance
    :param key: Clé
    :return: Valeur
    """
    if hasattr(instance, 'get_metadata'):
        return instance.get_metadata(key)


@register.filter(name='parsedate')
def filter_parsedate(value, options=''):
    """
    Parse une date ou un datetime dans n'importe quel format
    :param value: Date ou datetime au format texte
    :param options: Options de parsing (au format query string)
    :return: Date ou datetime
    """
    from common.utils import parsedate
    options = QueryDict(options)
    return parsedate(value, **options)


@register.filter(name='get')
def filter_get(value, key):
    """
    Permet de récupérer une valeur depuis un objet quelconque
    :param value: Objet
    :param key: Clé ou index
    :return: Valeur
    """
    try:
        if isinstance(value, dict):
            return value.get(key) or value.get(int(key))
        if isinstance(value, (list, tuple)):
            return value[int(key)]
        return getattr(value, key, None)
    except ValueError:
        return


@register.filter(name='localize')
def filter_localize(value, use_l10n=None):
    """
    Localise une valeur brute
    :param value: Valeur
    :param use_l10n: Force ou non la localisation
    :return: Valeur localisée (si possible)
    """
    return localize(value, use_l10n=use_l10n) or value


@register.simple_tag(name='query', takes_context=True)
def tag_query(context, queryset, save='', **kwargs):
    """
    Permet de faire des opérations complémentaires sur un QuerySet
    :param context: Contexte local
    :param queryset: QuerySet
    :param save: Nom du contexte qui contiendra le nouveau QuerySet
    :param kwargs: Options de filtre/tri/etc...
    :return: Rien
    """
    from common.api.utils import url_value, AGGREGATES
    from django.db.models import F, QuerySet
    if not isinstance(queryset, QuerySet):
        return queryset

    def get(name):
        return kwargs.get(name, '').replace('.', '__').replace(' ', '')

    reserved_keywords = ('filters', 'fields', 'order_by', 'group_by', 'distinct', 'select_related',
                         'prefetch_related', 'limit') + tuple(AGGREGATES.keys())

    def do_filter(queryset):
        filters = {}
        excludes = {}
        for key, value in kwargs.items():
            if key in reserved_keywords:
                continue
            key = key.replace('.', '__')
            if isinstance(value, str):
                if value.startswith('('):
                    if value.endswith(')'):
                        value = F(value[1:-1])
            if key.startswith('_'):
                key = key[1:]
                excludes[key] = url_value(key, value)
            else:
                key = key.strip()
                filters[key] = url_value(key, value)

        if filters:
            queryset = (queryset.filter)(**filters)
        if excludes:
            queryset = (queryset.exclude)(**excludes)
        others = kwargs.get('filters', None)
        if others:
            from common.api.utils import parse_filters
            queryset = queryset.filter(parse_filters(others))
        return queryset

    select_related = get('select_related')
    if select_related:
        queryset = (queryset.select_related)(*select_related.split(','))
    prefetch_related = get('prefetch_related')
    if prefetch_related:
        queryset = (queryset.prefetch_related)(*prefetch_related.split(','))
    aggregations = {}
    for aggregate, function in AGGREGATES.items():
        for field in kwargs.get(aggregate, '').split(','):
            if not field:
                continue
            distinct = field.startswith(' ')
            field = field.strip().replace('.', '__')
            aggregations[field + '_' + aggregate] = function(field, distinct=distinct)

    group_by = get('group_by')
    if group_by:
        _queryset = (queryset.values)(*group_by.split(','))
        if aggregations:
            _queryset = (_queryset.annotate)(**aggregations)
        else:
            _queryset = _queryset.distinct()
        queryset = _queryset
    else:
        if aggregations:
            queryset = do_filter(queryset)
            return (queryset.aggregate)(**aggregations)
        queryset = do_filter(queryset)
        fields = get('fields')
        if fields:
            queryset = queryset.select_related(None).prefetch_related(None)
            relateds = set()
            field_names = set()
            for field in fields.split(','):
                if not field:
                    continue
                field_names.add(field)
                *related, field_name = field.split('__')
                if related:
                    relateds.add('__'.join(related))

            if relateds:
                queryset = (queryset.select_related)(*relateds)
            if field_names:
                queryset = (queryset.values_list)(*field_names, **{'named': True})
        order_by = get('order_by')
        if order_by:
            _queryset = (queryset.order_by)(*order_by.split(','))
            str(_queryset.query)
            queryset = _queryset
        distinct = get('distinct')
        if distinct:
            if distinct is True:
                distincts = ()
            else:
                distincts = distinct.split(',')
            queryset = (queryset.distinct)(*distincts)
        limit = get('limit')
        if limit:
            limit = [int(l) for l in limit.split(',')]
            limit_inf, limit_sup = (0, limit[0]) if len(limit) == 1 else limit[:2]
            queryset = queryset[limit_inf:limit_sup]
        context[save] = queryset
        return ''