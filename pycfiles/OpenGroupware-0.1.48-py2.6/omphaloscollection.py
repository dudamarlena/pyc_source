# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/omphaloscollection.py
# Compiled at: 2012-10-12 07:02:39
import json, yaml
from datetime import datetime
from coils.core import *
import coils.core.omphalos as omphalos, coils.core.xml as omphalos_xml
from davobject import DAVObject

class OmphalosCollection(DAVObject):
    """ Represents an OpenGroupware entity in a DAV collection,  a GET will return the
        representation of the object - vCard, vEvent, vToDo, etc... """

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)
        self.render_mode = params.get('rendered', False)
        self.detail = int(params.get('detailLevel', 0))

    def _encode(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        raise TypeError()

    def do_GET(self):
        if self.render_mode:
            result = omphalos.Render.Results(self.data, self.detail, self.context)
        else:
            result = []
            for entry in self.data:
                if isinstance(entry, list):
                    entity = entry[0]
                else:
                    entity = entry
                if entity.version is None:
                    version = 0
                else:
                    version = entity.version
                displayName = ''
                if hasattr(entity, 'get_display_name'):
                    displayName = entity.get_display_name()
                result.append({'objectId': entity.object_id, 'entityName': entity.__entityName__, 
                   'displayName': displayName, 
                   'version': version})

            json_data = json.dumps(result, default=self._encode)
            result = None
            self.request.simple_response(200, data=json_data, mimetype='application/json')
            json_data = None
            return