# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/linkedin/browser/profile_info.py
# Compiled at: 2009-11-27 05:18:01
from zope.component import getSiteManager
from collective.linkedin.browser.interfaces import ICollectiveLinkedInManagement

class ProfileInfo(object):
    __module__ = __name__

    def get_settings(self):
        sm = getSiteManager()
        return sm.queryUtility(ICollectiveLinkedInManagement, name='linkedin_config')