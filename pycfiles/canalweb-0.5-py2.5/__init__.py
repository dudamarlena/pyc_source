# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/canalweb/__init__.py
# Compiled at: 2009-01-10 09:42:48
"""Manage videos from the Canal+ website."""

class Show(object):
    """Describe a single Canal+ show."""

    def __init__(self, pid, nickname, fullname):
        self.pid = pid
        self.nickname = nickname
        self.fullname = fullname


SHOW_BY_NICK = {}
SHOW_BY_PID = {}
for show in [Show(1830, 'zapping', 'Le Zapping'),
 Show(1784, 'guignoles', 'Les Gignoles'),
 Show(1787, 'magzin', 'Groland Magzin')]:
    SHOW_BY_NICK[show.nickname] = show
    SHOW_BY_PID[show.pid] = show