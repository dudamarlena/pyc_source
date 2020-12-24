# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/grubber/util.py
# Compiled at: 2017-04-03 18:58:57
"""
This module contains utility functions and classes used by the main system and
by the modules for various tasks.
"""
try:
    import hashlib
except ImportError:
    import md5 as hashlib

import os
from msg import _, msg

def md5_file(fname):
    """
    Compute the MD5 sum of a given file.
    """
    m = hashlib.md5()
    file = open(fname)
    for line in file.readlines():
        m.update(line)

    file.close()
    return m.digest()


class Watcher:
    """
    Watch for any changes of the files to survey, by checking the file MD5 sums.
    """

    def __init__(self):
        self.files = {}

    def watch(self, file):
        if os.path.exists(file):
            self.files[file] = md5_file(file)
        else:
            self.files[file] = None
        return

    def update(self):
        """
        Update the MD5 sums of all files watched, and return the name of one
        of the files that changed, or None of they didn't change.
        """
        changed = []
        for file in self.files.keys():
            if os.path.exists(file):
                new = md5_file(file)
                if self.files[file] != new:
                    msg.debug(_('%s MD5 checksum changed') % os.path.basename(file))
                    changed.append(file)
                self.files[file] = new

        return changed