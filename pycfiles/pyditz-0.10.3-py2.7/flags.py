# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/flags.py
# Compiled at: 2016-03-07 14:40:46
"""
Issue, release and status flags.
"""
BUGFIX = ':bugfix'
FEATURE = ':feature'
TASK = ':task'
TYPE = {BUGFIX: 'bugfix', FEATURE: 'feature', TASK: 'task'}
TYPE_PLURAL = {BUGFIX: 'bugfixes', FEATURE: 'features', TASK: 'tasks'}
UNSTARTED = ':unstarted'
PAUSED = ':paused'
IN_PROGRESS = ':in_progress'
CLOSED = ':closed'
STATUS = {UNSTARTED: 'unstarted', PAUSED: 'paused', IN_PROGRESS: 'in progress', 
   CLOSED: 'closed'}
FLAGS = {UNSTARTED: '_', PAUSED: '=', IN_PROGRESS: '>', CLOSED: 'x'}
SORT = {UNSTARTED: 1, PAUSED: 2, IN_PROGRESS: 3, CLOSED: 0}
FIXED = ':fixed'
WONTFIX = ':wontfix'
REORG = ':reorg'
DISPOSITION = {FIXED: 'fixed', WONTFIX: "won't fix", REORG: 'reorganized'}
RELEASED = ':released'
UNRELEASED = ':unreleased'
RELSTATUS = {RELEASED: 'released', UNRELEASED: 'unreleased'}