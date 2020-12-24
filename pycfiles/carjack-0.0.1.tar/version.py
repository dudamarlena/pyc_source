# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/caritang/common/version.py
# Compiled at: 2010-04-24 16:44:56
__doc__ = '\nCreated on Apr 18, 2010\n\n@author: maemo\n'
CURRENT_VERSION = '0.4.0'

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
getInstance().submitRevision('$Revision: 179 $')