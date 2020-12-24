# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/zourite/common/version.py
# Compiled at: 2010-04-27 15:21:49
"""
Created on 28 mars 2010

@author: thierry
"""
CURRENT_VERSION = '0.4.0-SNAPSHOT'

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
getInstance().submitRevision('$Revision: 219 $')