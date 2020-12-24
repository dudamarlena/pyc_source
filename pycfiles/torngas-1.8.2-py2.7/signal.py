# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/signal.py
# Compiled at: 2016-02-16 00:41:00
from dispatch import Signal
call_started = Signal(providing_args=['request'])
handler_started = Signal(providing_args=['handler'])
handler_response = Signal(providing_args=['handler', 'chunk'])
call_finished = Signal(providing_args=['handler'])
handler_render = Signal(providing_args=['handler', 'template_name', 'kwargs'])