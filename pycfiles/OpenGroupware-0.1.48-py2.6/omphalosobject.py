# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/omphalosobject.py
# Compiled at: 2012-10-12 07:02:39
import json
from StringIO import StringIO
import yaml
from datetime import datetime
from coils.core import *
import coils.core.omphalos as omphalos, coils.core.xml as omphalos_xml
from davobject import DAVObject

class OmphalosObject(DAVObject):
    """ Represents an OpenGroupware entity in a DAV collection,  a GET will return the
        representation of the object - vCard, vEvent, vToDo, etc... """

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def _encode(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        raise TypeError()

    def do_GET(self):
        if self.name[-5:] == '.json':
            result = omphalos.Render.Result(self.entity, 65503, self.context)
            payload = json.dumps(result, default=self._encode)
            mimetype = 'text/plain'
        elif self.name[-5:] == '.yaml':
            result = omphalos.Render.Result(self.entity, 65503, self.context)
            payload = yaml.dump(result)
            mimetype = 'text/plain'
        elif self.name[-4:] == '.xml':
            payload = omphalos_xml.Render.render(self.entity, self.context, detailLevel=65503)
            mimetype = 'application/xml'
        result = None
        self.request.simple_response(200, data=payload, mimetype=mimetype, headers={'X-COILS-OBJECT-ID': self.entity.object_id})
        payload = None
        return