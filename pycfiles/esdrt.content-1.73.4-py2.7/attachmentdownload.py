# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/browser/attachmentdownload.py
# Compiled at: 2019-05-21 05:08:42
from plone.namedfile.browser import Download as Base
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.publisher.interfaces import NotFound

class Download(Base):

    def _getFile(self):
        if not self.fieldname:
            info = IPrimaryFieldInfo(self.context, None)
            if info is None:
                raise NotFound(self, '', self.request)
            self.fieldname = info.fieldname
            file = info.value
        else:
            context = getattr(self.context, 'aq_explicit', self.context)
            file = getattr(context, self.fieldname, None)
        if file is None:
            raise NotFound(self, self.fieldname, self.request)
        return file