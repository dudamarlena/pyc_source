# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/arrange/__init__.py
# Compiled at: 2011-02-05 04:22:02
from django.db.models.signals import class_prepared, post_save
from arrange import signal_handlers
class_prepared.connect(signal_handlers.class_prepared)
post_save.connect(signal_handlers.post_save)