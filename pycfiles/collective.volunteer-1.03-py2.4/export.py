# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/Plone/zinstance/src/collective.volunteer/collective/volunteer/browser/export.py
# Compiled at: 2008-11-10 22:24:07
from Products.Five import BrowserView
import csv, time
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName

class CSV(BrowserView):
    __module__ = __name__

    def __call__(self):
        pm = getToolByName(self.context, 'portal_membership')
        utils = getToolByName(self.context, 'plone_utils')
        buffer = StringIO()
        writer = csv.writer(buffer, quoting=csv.QUOTE_ALL)
        writer.writerow(('Time', 'Job', 'Assignment'))
        for slot in self.context.getTimesAvailable():
            slot = slot.split('|')
            if len(slot) == 3:
                slot[2] = pm.getMemberById(slot[2]).getProperty('fullname')
            writer.writerow(slot)

        value = buffer.getvalue()
        value = unicode(value, 'utf-8').encode('iso-8859-1', 'replace')
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment;filename=%s-%s.csv' % (utils.normalizeString(self.context.Title()), time.strftime('%Y%m%d-%H%M')))
        return value