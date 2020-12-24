# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/doctor/getdoctorid.py
# Compiled at: 2014-12-12 07:13:54
from bika.lims.browser import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError
from bika.health.permissions import *
import json, plone

class ajaxGetDoctorID(BrowserView):
    """ Grab ID for newly created doctor (#420)
    """

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request)
        Fullname = self.request.get('Fullname', '')
        if not Fullname:
            return json.dumps({'DoctorID': ''})
        else:
            proxies = None
            try:
                proxies = self.portal_catalog(portal_type='Doctor', Title=Fullname, sort_on='created', sort_order='reverse')
            except ParseError:
                pass

            if not proxies:
                return json.dumps({'DoctorID': ''})
            return json.dumps({'DoctorID': proxies[0].getObject().getDoctorID(), 'DoctorSysID': proxies[0].getObject().id})