# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/linkedin/browser/profile_info.py
# Compiled at: 2009-11-27 05:18:01
from zope.component import getSiteManager
from collective.linkedin.browser.interfaces import ICollectiveLinkedInManagement

class ProfileInfo(object):
    __module__ = __name__

    def get_settings(self):
        sm = getSiteManager()
        return sm.queryUtility(ICollectiveLinkedInManagement, name='linkedin_config')