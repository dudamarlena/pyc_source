# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/prism_rest/renderer.py
# Compiled at: 2013-08-18 16:48:56
"""
Implementation of a custom renderer that handles more complex objects when
rendering to JSON. Purhaps in the future this could be extended to support
other serialization formats based on request headers.
"""
import json, logging
from prism_rest import viewmodels
from prism_rest.errors import ViewModelNotFoundError
log = logging.getLogger('prism.rest.renderer')

class APISerializer(object):

    def __init__(self, info):
        """
        Constructor: info will be an object having the
        following attributes: name (the renderer name), package
        (the package that was 'current' at the time the
        renderer was registered), type (the renderer type
        name), registry (the current application registry) and
        settings (the deployment settings dictionary).
        """
        pass

    def __call__(self, value, system):
        """
        Call the renderer implementation with the value and the system value
        passed in as arguments and return the result (a string or unicode
        object). The value is the return value of a view. The system value is
        a dictionary containing available system values (e.g. view, context,
        and request).
        """
        request = system.get('request')
        if request is not None:
            response = request.response
            if response.content_type == response.default_content_type:
                response.content_type = 'application/json'
        model_version = None
        model_metadata = value.get('metadata')
        if model_metadata:
            model_version = model_metadata.get('version')
        return json.dumps(value, cls=JSONEncoder, indent=2, model_version=model_version, request=request)


class JSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for handling more complex objects.
    """
    _encoders = {}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.model_version = kwargs.pop('model_version', None)
        json.JSONEncoder.__init__(self, *args, **kwargs)
        return

    def default(self, o):
        """
        Handle encoding of complex objects.
        """
        encoder = self.get_encoder(o)
        if encoder:
            return encoder.encode(o)
        try:
            modelCls = viewmodels.get_model(self.model_version, o)
            model = modelCls(self.request)
            return model.serialize(o)
        except ViewModelNotFoundError:
            pass

        return json.JSONEncoder.default(self, o)

    @classmethod
    def get_encoder(cls, o):
        for t, encoder in cls._encoders.iteritems():
            if isinstance(o, t):
                return encoder

        return

    @classmethod
    def register_encoder(cls, tcls, encoder):
        cls._encoders[tcls] = encoder


def register_encoder(type_cls):

    def deco(cls):
        JSONEncoder.register_encoder(type_cls, cls())
        return cls

    return deco