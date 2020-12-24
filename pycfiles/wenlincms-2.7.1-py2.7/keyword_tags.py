# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/generic/templatetags/keyword_tags.py
# Compiled at: 2016-05-20 23:42:06
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model, Count
from future.builtins import int, round
from wenlincms import template
from wenlincms.conf import settings
from wenlincms.generic.models import AssignedKeyword, Keyword
register = template.Library()

@register.as_tag
def keywords_for(*args):
    """
    Return a list of ``Keyword`` objects for the given model instance
    or a model class. In the case of a model class, retrieve all
    keywords for all instances of the model and apply a ``weight``
    attribute that can be used to create a tag cloud.
    """
    if isinstance(args[0], Model):
        obj = args[0]
        if hasattr(obj, b'get_content_model'):
            obj = obj.get_content_model() or obj
        keywords_name = obj.get_keywordsfield_name()
        keywords_queryset = getattr(obj, keywords_name).all()
        prefetched = getattr(obj, b'_prefetched_objects_cache', {})
        if keywords_name not in prefetched:
            keywords_queryset = keywords_queryset.select_related(b'keyword')
        if len(args) == 2:
            try:
                maxnum = int(args[1])
                if maxnum:
                    keywords_queryset = keywords_queryset[:maxnum]
            except ValueError:
                pass

        return [ assigned.keyword for assigned in keywords_queryset ]
    try:
        app_label, model = args[0].split(b'.', 1)
    except ValueError:
        return []

    content_type = ContentType.objects.get(app_label=app_label, model=model)
    assigned = AssignedKeyword.objects.filter(content_type=content_type)
    keywords = Keyword.objects.filter(assignments__in=assigned)
    keywords = keywords.annotate(item_count=Count(b'assignments'))
    if not keywords:
        return []
    settings.use_editable()
    counts = [ keyword.item_count for keyword in keywords ]
    min_count, max_count = min(counts), max(counts)
    factor = settings.TAG_CLOUD_SIZES - 1.0
    if min_count != max_count:
        factor /= max_count - min_count
    for kywd in keywords:
        kywd.weight = int(round((kywd.item_count - min_count) * factor)) + 1

    return keywords