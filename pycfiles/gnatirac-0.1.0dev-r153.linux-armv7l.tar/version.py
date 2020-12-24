# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/gnatirac/common/version.py
# Compiled at: 2011-12-29 07:58:32
"""
Created on Dec 29, 2011

@author: maemo
"""
CURRENT_VERSION = '0.1.0-SNAPSHOT'

def getInstance():
    return SINGLETON


class Version(object):
    """
    Hold the revision of the application.
    """

    def __init__(self):
        """
        Constructor
        """
        self.revision = ''

    def submitRevision(self, rev):
        """
        submit a new revision. If the revision is upper than
        the current revision, it become the new current revision
        """
        if self.revision < rev:
            self.revision = rev

    def getRevision(self):
        """
        Return the scm revision for this application
        """
        return self.revision

    def getVersion(self):
        """
        Return the marketing version for this application.
        """
        return CURRENT_VERSION


SINGLETON = Version()
getInstance().submitRevision('$Revision: 4 $')