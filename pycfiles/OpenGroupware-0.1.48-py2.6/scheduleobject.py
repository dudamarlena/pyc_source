# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/scheduleobject.py
# Compiled at: 2012-10-12 07:02:39
import io, yaml, json
from datetime import datetime
from coils.core import *
from coils.net import *
from workflow import WorkflowPresentation

class ScheduleObject(DAVObject, WorkflowPresentation):
    """ Represents a workflow message in a process with a DAV hierarchy. """

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)
        self.entry = params['entry']
        self.payload = json.dumps(self.entry)

    def get_property_webdav_getetag(self):
        return self.entry['UUID']

    def get_property_webdav_displayname(self):
        return self.entry['UUID']

    def get_property_webdav_getcontentlength(self):
        return len(self.payload)

    def get_property_webdav_getcontenttype(self):
        return 'application/json'

    def get_property_webdav_creationdate(self):
        return datetime.now()

    def do_HEAD(self):
        self.request.simple_response(201, mimetype='application/json', headers={'Content-Length': self.get_property_webdav_getcontentlength(), 'ETag': self.get_property_webdav_getetag()})

    def do_GET(self):
        self.request.simple_response(200, data=self.payload, mimetype='application/json', headers={'ETag': self.get_property_webdav_getetag()})