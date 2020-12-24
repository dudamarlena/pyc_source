# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/service.py
# Compiled at: 2020-05-10 06:48:33
# Size of source mod 2**32: 7422 bytes
"""Service."""
import uuid, logging, types
from urllib.parse import urlparse
import requests, tornado.ioloop
from empower_core.serialize import serializable_dict
import empower_core.serialize as serialize
CALLBACK_NATIVE = 'native'
CALLBACK_REST = 'rest'
CALLBACK_TYPES = [
 CALLBACK_NATIVE, CALLBACK_REST]

@serializable_dict
class EService:
    __doc__ = 'Base service class.'
    HANDLERS = []

    def __init__(self, context, service_id, **kwargs):
        self._service_id = None
        self.context = context
        self.service_id = service_id
        if 'every' not in kwargs:
            kwargs['every'] = -1
        self.callbacks = dict()
        self.log = logging.getLogger(self.name)
        self.worker = None
        self.configuration = {}
        self.params = {}
        for param in kwargs:
            setattr(self, param, kwargs[param])

    def save_service_state(self):
        """Save service state."""
        if not self.context:
            return
        self.context.save_service_state(self.service_id)

    def register_service(self, name, **kwargs):
        """Register a service.

        If a service with the same name and parameters is already running, then
        that service instance will be returned. Otherwise a new service will be
        spawned."""
        if not self.context:
            return
        return self.context.register_service(name, params=kwargs)

    def handle_callbacks(self, params=None, name='default'):
        """Invoke registered callbacks."""
        if name not in self.callbacks:
            return
        callback_type = self.callbacks[name]['callback_type']
        argument = params if params else self
        callback = self.callbacks[name]['callback']
        self.log.info('Handling callback %s (%s)', name, callback_type)
        if self.callbacks[name]['callback_type'] == CALLBACK_NATIVE:
            callback(params)
            return
        if self.callbacks[name]['callback_type'] == CALLBACK_REST:
            response = requests.post(url=callback, json=(serialize(argument)))
            self.log.info('POST %s - %u', callback, response.status_code)

    def add_callback(self, callback, name='default', callback_type=CALLBACK_NATIVE):
        """Add a new callback."""
        if 'callbacks' not in self.manifest:
            raise KeyError('Callback %s not defined' % name)
        if name not in self.manifest['callbacks']:
            raise KeyError('Callback %s not defined' % name)
        if callback_type not in CALLBACK_TYPES:
            raise ValueError('Invalid callback type: %s' % callback_type)
        if callback_type == CALLBACK_NATIVE:
            if not isinstance(callback, (
             types.FunctionType, types.MethodType)):
                raise ValueError('Callback not callable')
            self.callbacks[name] = {'name':name, 
             'callback':callback, 
             'callback_type':CALLBACK_NATIVE}
            return
        if callback_type == CALLBACK_REST:
            self.callbacks[name] = {'name':name, 
             'callback':urlparse(callback).geturl(), 
             'callback_type':CALLBACK_REST}
            self.save_service_state()
            return
        raise ValueError('Invalid input to add callback')

    def rem_callback(self, name='default'):
        """Remove a callback."""
        del self.callbacks[name]
        self.save_service_state()

    def to_dict(self):
        """Return JSON-serializable representation of the object."""
        output = {}
        output['service_id'] = self.service_id
        output['manifest'] = self.manifest
        output['name'] = self.name
        output['callbacks'] = self.callbacks
        output['params'] = self.params
        if self.context:
            output['project_id'] = self.context.project_id
        return output

    @property
    def name(self):
        """Get name."""
        return '%s' % self.__class__.__module__

    @property
    def manifest(self):
        """Get manifest."""
        return self.context.manager.catalog[self.name]

    @property
    def service_id(self):
        """Get service_id."""
        return self._service_id

    @service_id.setter
    def service_id(self, value):
        """Set service_id."""
        if isinstance(value, uuid.UUID):
            self._service_id = value
        else:
            self._service_id = uuid.UUID(value)

    @property
    def every(self):
        """Return loop period."""
        return self.params['every']

    @every.setter
    def every(self, value):
        """Set loop period."""
        self.params['every'] = int(value)
        if self.worker:
            self.stop()
            self.start()

    def write_points(self, points):
        """Write points to context."""
        self.context.write_points(points)

    def start(self):
        """Start control loop."""
        if self.every == -1:
            return
        self.worker = tornado.ioloop.PeriodicCallback(self.loop, self.every)
        self.worker.start()

    def stop(self):
        """Stop control loop."""
        self.save_service_state()
        if self.every == -1:
            return
        self.worker.stop()
        self.worker = None

    def loop(self):
        """Control loop."""
        self.log.info('Empty loop')

    def to_str(self):
        """Return an ASCII representation of the object."""
        return '%s' % self.name

    def __str__(self):
        return self.to_str()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, EService):
            return self.name == other.name and self.every == other.every
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"