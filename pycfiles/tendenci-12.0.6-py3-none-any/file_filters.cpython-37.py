# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/files/templatetags/file_filters.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 671 bytes
from builtins import str
from django.template import Library
register = Library()

@register.filter
def file_exists(obj):
    """
    Returns boolean
    Checks if file exists at a disk level
    Accepts File, FileField and String [path] type object
    """
    from django.forms import FileField
    from django.core.files.storage import default_storage
    from tendenci.apps.files.models import File
    if isinstance(obj, File):
        return default_storage.exists(obj.file.path)
    if isinstance(obj, FileField):
        return default_storage.exists(obj.path)
    if isinstance(obj, str):
        if obj:
            return default_storage.exists(obj)
    return False