# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/signals.py
# Compiled at: 2016-10-05 04:00:23
from django import dispatch
entry_changed = dispatch.Signal(providing_args=[
 'user', 'old_msgstr', 'old_fuzzy', 'pofile', 'language_code'])
post_save = dispatch.Signal(providing_args=[
 'language_code', 'request'])