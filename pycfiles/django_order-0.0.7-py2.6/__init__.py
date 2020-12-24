# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/order/__init__.py
# Compiled at: 2011-09-15 05:06:32
from django.db.models.signals import post_save, post_syncdb
from order import models, signal_handlers
post_save.connect(signal_handlers.post_save)
post_syncdb.connect(signal_handlers.post_syncdb, sender=models)