# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/suds/sax/document.py
# Compiled at: 2010-08-31 11:18:01
"""
Provides XML I{document} classes.
"""
from logging import getLogger
from suds import *
from suds.sax import *
from suds.sax.element import Element
log = getLogger(__name__)

class Document(Element):
    """ simple document """
    DECL = '<?xml version="1.0" encoding="UTF-8"?>'

    def __init__(self, root=None):
        Element.__init__(self, 'document')
        if root is not None:
            self.append(root)
        return

    def root(self):
        if len(self.children):
            return self.children[0]
        else:
            return
            return

    def str(self):
        s = []
        s.append(self.DECL)
        s.append('\n')
        s.append(self.root().str())
        return ('').join(s)

    def plain(self):
        s = []
        s.append(self.DECL)
        s.append(self.root().plain())
        return ('').join(s)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.str()