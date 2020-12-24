# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/loadschedule.py
# Compiled at: 2012-10-12 07:02:39
from StringIO import StringIO
from datetime import datetime
from coils.core import *
from coils.net import *
from messageobject import MessageObject
from workflow import WorkflowPresentation

class LoadScheduleObject(DAVObject):
    """ Represent a BPML markup object in WebDAV """

    def __init__(self, parent, name, **params):
        self.version = None
        DAVObject.__init__(self, parent, name, **params)
        self.text = None
        return

    def get_property_webdav_getetag(self):
        return 'loadSchedule'

    def get_property_webdav_displayname(self):
        return 'Workflow load schedule'

    def get_property_webdav_getcontentlength(self):
        self.generate_schedule()
        return str(len(self.text))

    def get_property_webdav_getcontenttype(self):
        return 'text/plain'

    def get_property_webdav_creationdate(self):
        return datetime.now()

    def get_property_webdav_getlastmodified(self):
        return datetime.now()

    def generate_schedule(self):
        if self.text is None:
            stream = StringIO('')
            for column in ['Hour', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
                stream.write((' {0} ').format(column))

            stream.write('\r\n')
            for hour in range(24):
                stream.write((' {0:#2} ').format(hour))
                for day in range(7):
                    stream.write((' {0:#4} ').format(10))

                stream.write('\r\n')

            self.text = stream.getvalue()
            stream.close()
            stream = None
        return

    def do_GET(self):
        """ Handle a GET request. """
        self.generate_schedule()
        self.request.simple_response(200, data=self.text, mimetype='application/text', headers={'ETag': self.get_property_webdav_getetag()})