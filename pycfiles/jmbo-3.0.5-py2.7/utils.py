# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/utils.py
# Compiled at: 2017-05-03 05:57:29
import inspect, re, types
from django.db.models import Q
from django.db.utils import IntegrityError
from django.template.defaultfilters import slugify
RE_NUMERICAL_SUFFIX = re.compile('^[\\w-]*-(\\d+)+$')

def generate_slug(obj, text, tail_number=0):
    from jmbo.models import ModelBase
    slug = slugify(text)
    if not slug:
        slug = 'no-title'
    values_list = ModelBase.objects.filter(slug__startswith=slug).values_list('id', 'slug')
    max = -1
    for tu in values_list:
        if tu[1] == slug:
            if tu[0] == obj.id:
                return slug
            if max == -1:
                max = 0
        match = RE_NUMERICAL_SUFFIX.match(tu[1])
        if match is not None:
            if tu[0] == obj.id:
                return tu[1]
            i = int(match.group(1))
            if i > max:
                max = i

    if max >= 0:
        return '%s-%s' % (slug, max + 1)
    else:
        return slug
        return


def modify_class(original_class, modifier_class, override=True):
    """
    Adds class methods from modifier_class to original_class.
    If override is True existing methods in original_class are overriden by
    those provided by modifier_class.
    """
    modifier_methods = inspect.getmembers(modifier_class, inspect.ismethod)
    for method_tuple in modifier_methods:
        name = method_tuple[0]
        method = method_tuple[1]
        if isinstance(method, types.UnboundMethodType):
            if hasattr(original_class, name) and not override:
                return
            setattr(original_class, name, method.im_func)

    return


def normalize_query(query_string, findterms=re.compile('"([^"]+)"|(\\S+)').findall, normspace=re.compile('\\s{2,}').sub):
    """
    Splits the query string in invidual keywords, getting rid of unecessary
    spaces and grouping quoted words together.
    Example:

    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    return [ normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)
           ]


def get_query(query_string, search_fields):
    """
    Returns a query, that is a combination of Q objects. That combination
    aims to search keywords within a model by testing the given search fields.
    search_fields should be something like: [('title', 'iexact'),
    ('content', 'icontains'), ]
    """
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field in search_fields:
            q = Q(**{'%s__%s' % (field[0], field[1]): term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q

        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query