# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/doctor/getdoctorinfo.py
# Compiled at: 2014-12-12 07:13:54
from Products.ZCTextIndex.ParseTree import ParseError
from bika.lims.browser import BrowserView
from Products.CMFCore.utils import getToolByName
import plone, json

class ajaxGetDoctorInfo(BrowserView):
    """ Grab details of newly created doctor
    """

    def __call__(self):
        plone.protect.CheckAuthenticator(self.request)
        Fullname = self.request.get('Fullname', '')
        uid = self.request.get('UID', '')
        ret = {'id': '', 'DoctorID': '', 
           'UID': '', 
           'Fullname': ''}
        bpc = getToolByName(self.context, 'portal_catalog')
        proxies = None
        if uid:
            try:
                proxies = bpc(UID=uid)
            except ParseError:
                pass

        elif Fullname:
            try:
                proxies = bpc(Title=Fullname, sort_on='created', sort_order='reverse')
            except ParseError:
                pass

        if not proxies:
            return json.dumps(ret)
        else:
            doctor = proxies[0].getObject()
            ret = {'DoctorID': doctor.getDoctorID(), 'id': doctor.id, 
               'UID': doctor.UID(), 
               'Fullname': doctor.Title()}
            return json.dumps(ret)