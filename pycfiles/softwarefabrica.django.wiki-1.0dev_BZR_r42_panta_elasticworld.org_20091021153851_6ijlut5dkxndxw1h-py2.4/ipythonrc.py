# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/demoproj/ipythonrc.py
# Compiled at: 2009-01-08 09:11:51
from django.db.models.loading import get_models
for m in get_models():
    exec 'from %s import %s' % (m.__module__, m.__name__)