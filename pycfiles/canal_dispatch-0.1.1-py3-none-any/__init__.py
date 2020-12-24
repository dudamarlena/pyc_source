# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/canalweb/__init__.py
# Compiled at: 2009-01-10 09:42:48
__doc__ = 'Manage videos from the Canal+ website.'

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