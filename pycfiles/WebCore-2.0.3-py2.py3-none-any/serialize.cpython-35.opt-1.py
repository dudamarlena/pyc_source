# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/serialize.py
# Compiled at: 2016-09-25 02:19:33
# Size of source mod 2**32: 2712 bytes
"""An example, though quite usable extension to handle list and dictionary return values."""
from __future__ import unicode_literals
import pkg_resources
from collections import Mapping
from marrow.package.host import PluginManager
from web.core.compat import str
try:
    from bson import json_util as json
except ImportError:
    import json

log = __import__('logging').getLogger(__name__)
json

class SerializationPlugins(PluginManager):

    def __init__(self, namespace, folders=None):
        self.__dict__['names'] = set()
        self.__dict__['types'] = set()
        super(SerializationPlugins, self).__init__(namespace, folders)

    def register(self, name, plugin):
        super(SerializationPlugins, self).register(name, plugin)
        self.names.add(name)
        if '/' in name:
            self.types.add(name)

    def _register(self, dist):
        try:
            super(SerializationPlugins, self)._register(dist)
        except pkg_resources.DistributionNotFound:
            pass


class SerializationExtension(object):
    __doc__ = 'Sample extension demonstrating integration of automatic serialization, such as JSON.\n\t\n\tThis extension registers handlers for lists and dictionaries (technically list and mappings).\n\t\n\tAdditional serializers can be registered during runtime by other extensions by adding a new mimetype mapping\n\tto the `context.serialize` dictionary-like object.  For convienence the default serializers are also provided\n\tusing their simple names, so you can access the JSON encoder directly, for example:\n\t\n\t\tcontext.serialize.json.dumps(...)\n\t'
    provides = {
     'serialization'}
    extensions = {'web.serializer'}
    context = {'serialize'}

    def __init__(self, default='application/json', types=(list, Mapping)):
        self.default = default
        self.types = types

    def start(self, context):
        manager = SerializationPlugins('web.serialize')
        manager.__dict__['__isabstractmethod__'] = False
        context.serialize = manager
        for kind in self.types:
            context.view.register(kind, self.render_serialization)

    def render_serialization(self, context, result):
        """Render serialized responses."""
        resp = context.response
        serial = context.serialize
        match = context.request.accept.best_match(serial.types, default_match=self.default)
        result = serial[match](result)
        if isinstance(result, str):
            result = result.decode('utf-8')
        resp.charset = 'utf-8'
        resp.content_type = match
        resp.text = result
        return True