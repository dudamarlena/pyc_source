# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/apps/authors/templatetags/author_tags.py
# Compiled at: 2015-02-18 13:07:39
# Size of source mod 2**32: 623 bytes
from authors.models import Author, Department
from content.models import Article
from django.template import Library
register = Library()

@register.assignment_tag
def get_all_departments():
    depts = Department.objects.all()
    return depts


@register.assignment_tag
def related_articles(author, max_numb=2, exclude=None):
    qs = Article.objects.filter(author=author)
    if exclude:
        qs = qs.exclude(id=exclude.id)
    return qs[:max_numb]


@register.inclusion_tag('partials/team-list.html')
def get_author_list():
    return {'authors': Author.objects.all()}