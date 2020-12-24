# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thoas/Sites/Python/ulule/python-mangopay/mangopay/signals.py
# Compiled at: 2015-06-08 06:37:42
from blinker import Namespace
signals = Namespace()
request_finished = signals.signal('request_finished')
request_started = signals.signal('request_started')
request_error = signals.signal('request_error')
pre_save = signals.signal('pre_save')
post_save = signals.signal('pre_save')