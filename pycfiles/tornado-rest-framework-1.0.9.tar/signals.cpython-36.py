# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/lib/orm/signals.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 235 bytes
from rest_framework.core.singnals import signal
pre_save = signal('pre_save')
post_save = signal('post_save')
pre_delete = signal('pre_delete')
post_delete = signal('post_delete')
pre_init = signal('pre_init')