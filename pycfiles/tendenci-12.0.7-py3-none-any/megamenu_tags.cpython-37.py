# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/base/templatetags/megamenu_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 929 bytes
from django.template import Library
register = Library()
PROFILE_DROPDOWN_MIN_COL_COUNT = 1
COMMUNITY_DROPDOWN_MIN_COL_COUNT = 1
BOOTSTRAP_GRID_COL_COUNT = 12

@register.simple_tag(takes_context=True)
def get_profile_dropdown_column_size(context):
    col_count = PROFILE_DROPDOWN_MIN_COL_COUNT
    is_superuser = context['USER_IS_SUPERUSER']
    is_superuser_or_member = is_superuser or context['USER_IS_MEMBER']
    col_count += int(is_superuser_or_member) + int(is_superuser)
    return BOOTSTRAP_GRID_COL_COUNT / col_count


@register.simple_tag(takes_context=True)
def get_community_dropdown_column_size(context):
    col_count = COMMUNITY_DROPDOWN_MIN_COL_COUNT
    is_superuser = context['USER_IS_SUPERUSER']
    col_count += int(is_superuser)
    return BOOTSTRAP_GRID_COL_COUNT / col_count