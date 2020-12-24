# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/linkedin/browser/company_info.py
# Compiled at: 2009-11-27 05:18:01
from zope.component import getSiteManager
from collective.linkedin.browser.interfaces import ICollectiveLinkedInManagement

class CompanyInfo(object):
    __module__ = __name__

    def get_settings(self):
        sm = getSiteManager()
        return sm.queryUtility(ICollectiveLinkedInManagement, name='linkedin_config')

    def company_name(self):
        settings = self.get_settings()
        return settings and settings.company_insider_widget or None