# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/settings.py
# Compiled at: 2016-11-27 06:27:17
__doc__ = '\nDefault global settings.\n'

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