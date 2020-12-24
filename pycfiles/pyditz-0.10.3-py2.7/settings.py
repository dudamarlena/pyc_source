# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/settings.py
# Compiled at: 2016-11-27 06:27:17
"""
Default global settings.
"""

class Settings(object):

    def __init__(self, **kw):
        self.autosave = False
        self.usecache = False
        self.cachefile = '.ditz-cache'
        self.externalplugins = True
        self.highlight = False
        self.nocomment = False
        self.comment = None
        self.searchparents = False
        self.versioncontrol = False
        self.setup = True
        self.termlines = 0
        self.termcols = 0
        self.linetrunc = '...'
        for attr, val in kw.items():
            if hasattr(self, attr):
                setattr(self, attr, val)
            else:
                raise ValueError("no setting called '%s'" % attr)

        return