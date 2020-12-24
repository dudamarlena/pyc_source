# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/templatetags/bootstrap_pagination_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 279 bytes
from django import template
from dj_pagination.templatetags.pagination_tags import paginate, do_autopaginate
register = template.Library()
register.inclusion_tag('base/bootstrap_pagination.html', takes_context=True)(paginate)
register.tag('autopaginate', do_autopaginate)