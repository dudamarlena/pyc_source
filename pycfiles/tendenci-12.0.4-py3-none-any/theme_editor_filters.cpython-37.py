# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme_editor/templatetags/theme_editor_filters.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 476 bytes
from django.template import Library
register = Library()

@register.filter()
def sortcontents(value):
    """
    Takes a list of folders and files, sorts the folder, and moves the files to the bottom.
    """
    ordered = sorted(value)
    contents_index = [i for i, x in enumerate(ordered) if x[0] == 'contents'][0]
    if len(ordered) > 1:
        contents = ordered[contents_index]
        ordered.pop(contents_index)
        ordered.append(contents)
    return ordered