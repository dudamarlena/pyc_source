# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/nodes/signals.py
# Compiled at: 2015-01-21 11:13:52
import django.dispatch
node_status_changed = django.dispatch.Signal(providing_args=['instance', 'old_status', 'new_status'])