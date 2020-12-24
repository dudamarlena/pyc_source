# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/localization.py
# Compiled at: 2019-02-13 03:47:25
# Size of source mod 2**32: 1399 bytes
from __future__ import unicode_literals
import contextlib, locale, six, rows.fields

@contextlib.contextmanager
def locale_context(name, category=locale.LC_ALL):
    old_name = locale.getlocale()
    if None not in old_name:
        old_name = '.'.join(old_name)
    if isinstance(name, six.text_type):
        name = str(name)
    if old_name != name:
        locale.setlocale(category, name)
    rows.fields.SHOULD_NOT_USE_LOCALE = False
    try:
        yield
    finally:
        if old_name != name:
            locale.setlocale(category, old_name)

    rows.fields.SHOULD_NOT_USE_LOCALE = True