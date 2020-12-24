# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/templatetags/saved_queries.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 841 bytes
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

templatetags/saved_queries.py - This template tag returns previously saved
                                queries. Therefore you don't need to modify
                                any views.
"""
from django.template import Library
from django.db.models import Q
from tendenci.apps.helpdesk.models import SavedSearch

def saved_queries(user):
    try:
        user_saved_queries = SavedSearch.objects.filter(Q(user=user) | Q(shared__exact=True))
        return user_saved_queries
    except Exception as e:
        try:
            import sys
            print("'saved_queries' template tag (django-helpdesk) crashed with following error:", file=(sys.stderr))
            print(e, file=(sys.stderr))
            return ''
        finally:
            e = None
            del e


register = Library()
register.filter('saved_queries', saved_queries)