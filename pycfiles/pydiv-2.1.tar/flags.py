# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/flags.py
# Compiled at: 2016-03-07 14:40:46
__doc__ = '\nIssue, release and status flags.\n'
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