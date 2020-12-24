# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/support.py
# Compiled at: 2018-06-14 23:17:51
from django.db.models.options import Options
_options = Options({})
supports_index_together = hasattr(_options, 'index_together')