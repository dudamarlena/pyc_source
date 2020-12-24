# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/details/dublincore/dublincore.py
# Compiled at: 2010-08-27 06:32:04
from datetime import datetime
from zope.event import notify
from zope.dublincore.interfaces import IZopeDublinCore
from zope.lifecycleevent import ObjectModifiedEvent, Attributes

class EditDublinCore:

    def edit(self):
        try:
            dc = IZopeDublinCore(self.context)
        except TypeError:
            return
        else:
            request = self.request
            formatter = self.request.locale.dates.getFormatter('dateTime', 'medium')
            message = ''
            if 'dctitle' in request:
                dc.title = unicode(request['dctitle'])
                dc.description = unicode(request['dcdescription'])
                description = Attributes(IZopeDublinCore, 'title', 'description')
                notify(ObjectModifiedEvent(self.context, description))
                message = 'Changed data %s' % formatter.format(datetime.utcnow())

        return {'message': message, 'dctitle': dc.title, 'dcdescription': dc.description, 
           'modified': (dc.modified or dc.created) and formatter.format(dc.modified or dc.created) or '', 
           'created': dc.created and formatter.format(dc.created) or '', 
           'creators': dc.creators}