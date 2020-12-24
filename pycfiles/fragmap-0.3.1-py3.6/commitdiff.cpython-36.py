# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\fragmap\commitdiff.py
# Compiled at: 2019-08-04 05:05:22
# Size of source mod 2**32: 290 bytes


class CommitDiff(object):

    def __init__(self, pygit_commit, pygit_diff):
        self.header = pygit_commit
        self.filepatches = [patch for patch in pygit_diff]

    def __repr__(self):
        return '<CommitDiff: %s %s>' % (self.header, self.filepatches)