# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\landon\envs\mezzanine\lib\site-packages\mezzanine_wiki-0.1-py3.6.egg\mezzanine_wiki\templatetags\mezawiki_tags.py
# Compiled at: 2018-01-31 08:31:33
# Size of source mod 2**32: 2248 bytes
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Count
from mezzanine_wiki.models import WikiPage, WikiCategory
from mezzanine import template
from mezzanine.conf import settings
from mezzanine.utils.importing import import_dotted_path
from django.utils.safestring import mark_safe
from diff_match_patch import diff_match_patch
register = template.Library()

@register.filter
def html_diff(diff):
    html = []
    for op, data in diff:
        text = (data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br />'),)
        if op == diff_match_patch.DIFF_INSERT:
            html.append('<span class="added">%s</span>' % text)
        else:
            if op == diff_match_patch.DIFF_DELETE:
                html.append('<span class="removed">%s</del>' % text)
            else:
                if op == diff_match_patch.DIFF_EQUAL:
                    html.append('<span>%s</span>' % text)

    return mark_safe(''.join(html))


@register.as_tag
def wiki_categories(*args):
    """
    Put a list of categories for wiki pages into the template context.
    """
    pages = WikiPage.objects.published()
    categories = WikiCategory.objects.filter(wikipages__in=pages)
    return list(categories.annotate(page_count=(Count('wikipages'))))


@register.as_tag
def wiki_authors(*args):
    """
    Put a list of authors (users) for wiki pages into the template context.
    """
    wiki_pages = WikiPage.objects.published()
    authors = User.objects.filter(wikipages__in=wiki_pages)
    return list(authors.annotate(post_count=(Count('wikipages'))))


@register.as_tag
def wiki_recent_pages(limit=5):
    """
    Put a list of recently published wiki pages into the template context.
    """
    return list(WikiPage.objects.published().order_by('-publish_date')[:limit])


@register.filter
def wikitext_filter(content):
    """
    This template filter takes a string value and passes it through the
    function specified by the WIKI_TEXT_FILTER setting.
    """
    if settings.WIKI_TEXT_FILTER:
        func = import_dotted_path(settings.WIKI_TEXT_FILTER)
    else:
        func = lambda s: s
    return func(content)