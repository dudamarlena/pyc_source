# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/constants.py
# Compiled at: 2015-06-14 13:30:57
"""
Constants needed throughout application.
"""
INIT = 'init'
READY = 'ready'
ACTIVE = 'active'
DONE = 'done'
CANCELLED = 'cancelled'
STATES = [
 INIT, READY, ACTIVE, DONE, CANCELLED]
ACTIVE_STATES = [INIT, READY, ACTIVE]
INACTIVE_STATES = [DONE, CANCELLED]