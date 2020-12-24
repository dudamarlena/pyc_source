# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/templatetags/in_list.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 656 bytes
"""
django-helpdesk - A Django powered ticket tracker for small enterprise.

(c) Copyright 2008 Jutda. All Rights Reserved. See LICENSE for details.

templatetags/in_list.py - Very simple template tag to allow us to use the
                          equivilent of 'if x in y' in templates. eg:

Assuming 'food' = 'pizza' and 'best_foods' = ['pizza', 'pie', 'cake]:

{% if food|in_list:best_foods %}
 You've selected one of our favourite foods!
{% else %}
 Your food isn't one of our favourites.
{% endif %}
"""
from django import template

def in_list(value, arg):
    return value in (arg or [])


register = template.Library()
register.filter(in_list)