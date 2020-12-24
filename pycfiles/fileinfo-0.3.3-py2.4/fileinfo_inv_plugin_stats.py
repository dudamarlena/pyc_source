# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/plugins/fileinfo_inv_plugin_stats.py
# Compiled at: 2008-06-17 03:23:49
"""A fileinfo plug-in for general file attributes.
"""
from fileinfo.investigator import BaseInvestigator

class StatInvestigator(BaseInvestigator):
    """A class for determining general attributes of files."""
    __module__ = __name__
    attrMap = {'counter': 'counter', 'lc': 'getLineCount', 'wc': 'getWordCount', 'md5': 'getMd5Hash'}
    totals = ('lc', 'wc')

    def __init__(self, path):
        self.path = path
        self.cnt = -1

    def activate(self):
        """Try activating self, setting 'active' variable."""
        self.active = True
        self.content = None
        return self.active

    def counter(self):
        """A counter generator."""
        self.cnt += 1
        return self.cnt

    def getLineCount(self):
        """Return the number of lines in a file."""
        if self.content is None:
            self.content = open(self.path).read()
        content = getattr(self, 'content', self.content)
        return content.count('\n') + int(len(content) > 0)

    def getWordCount(self):
        """Return the number of words in a file."""
        if self.content is None:
            self.content = open(self.path).read()
        content = getattr(self, 'content', self.content)
        return len(content.split())

    def getMd5Hash(self):
        """Return the MD5 hash value of an entire file."""
        import md5
        if self.content is None:
            self.content = open(self.path).read()
        content = getattr(self, 'content', self.content)
        m = md5.new()
        m.update(content)
        hash = m.hexdigest()
        return hash