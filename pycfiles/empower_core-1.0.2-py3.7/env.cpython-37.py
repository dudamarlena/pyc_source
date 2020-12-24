# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/envmanager/env.py
# Compiled at: 2020-05-10 06:49:23
# Size of source mod 2**32: 8841 bytes
"""Runtime configuration."""
import uuid, platform
from importlib import import_module
from pymodm import MongoModel, fields
import empower_core.serialize as serialize
from empower_core.launcher import srv_or_die
from empower_core.serialize import serializable_dict
from empower_core.worker import EWorker

@serializable_dict
class Env(MongoModel):
    __doc__ = "Env class\n\n    Attributes:\n        project_id: The project identifier. Notice how there is only one Env\n            instance active at any given time and that the project_id of the\n            workers loaded by Env is always set to the Env's project_id\n        bootstrap: the list of services to be loaded at bootstrap\n        services: the services\n    "
    project_id = fields.UUIDField(primary_key=True)
    bootstrap = fields.DictField(required=False, blank=True)

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.services = {}
        self.manager = srv_or_die('envmanager')

    def write_points(self, points):
        """Write points to time-series manager."""
        ts_manager = srv_or_die('tsmanager')
        ts_manager.write_points(points)

    def save_service_state(self, service_id):
        """Save service state."""
        service = self.services[service_id]
        self.bootstrap[str(service.service_id)] = {'name':service.name, 
         'params':serialize.serialize(service.params), 
         'callbacks':serialize.serialize(service.callbacks), 
         'configuration':serialize.serialize(service.configuration)}
        self.save()

    def remove_service_state(self, service_id):
        """Remove service state."""
        del self.bootstrap[str(service_id)]
        self.save()

    def load_service(self, service_id, name, params):
        """Load a service instance."""
        init_method = getattr(import_module(name), 'launch')
        service = init_method(context=self, service_id=service_id, **params)
        if not isinstance(service, EWorker):
            raise ValueError('Service %s not EWorker type' % name)
        return service

    def register_service(self, name, params, service_id=None):
        """Register service."""
        if not service_id:
            requested = self.load_service(uuid.uuid4(), name, params)
            services = self.services.values()
            found = next((s for s in services if s == requested), None)
            if found:
                return found
        else:
            service_id = service_id or uuid.uuid4()
        service = self.start_service(service_id, name, params)
        self.save_service_state(service.service_id)
        return service

    def unregister_service(self, service_id):
        """Unregister service."""
        if service_id not in self.services:
            raise KeyError('Service %s not running' % service_id)
        self.stop_service(service_id)
        self.remove_service_state(service_id)

    def reconfigure_service(self, service_id, params):
        """Reconfigure service."""
        if service_id not in self.services:
            raise KeyError('Service %s not registered' % service_id)
        service = self.services[service_id]
        for param in params:
            if param not in self.bootstrap[str(service_id)]['params']:
                raise KeyError('Param %s undefined' % param)
            setattr(service, param, params[param])

        self.save_service_state(service_id)
        return self.services[service_id]

    def start_services(self):
        """Start registered services."""
        for service_id in list(self.bootstrap):
            try:
                name = self.bootstrap[service_id]['name']
                params = self.bootstrap[service_id]['params']
                callbacks = self.bootstrap[service_id]['callbacks']
                configuration = self.bootstrap[service_id]['configuration']
                service_id = uuid.UUID(service_id)
                self.start_service(service_id, name, params, configuration, callbacks)
            except ModuleNotFoundError as ex:
                try:
                    self.manager.log.error('Unable to start service %s: %s', name, ex)
                    self.remove_service_state(service_id)
                finally:
                    ex = None
                    del ex

            except TypeError as ex:
                try:
                    self.manager.log.error('Unable to start service %s: %s', name, ex)
                    self.remove_service_state(service_id)
                finally:
                    ex = None
                    del ex

            except ValueError as ex:
                try:
                    self.manager.log.error('Unable to start service %s: %s', name, ex)
                    self.remove_service_state(service_id)
                finally:
                    ex = None
                    del ex

    def stop_services(self):
        """Stop registered services."""
        for service_id in self.bootstrap:
            self.stop_service(uuid.UUID(service_id))

    def start_service(self, service_id, name, params, configuration=None, callbacks=None):
        """Start a service."""
        if service_id in self.services:
            raise ValueError('Service %s is already running' % service_id)
        else:
            self.manager.log.info('Loading service: %s (%s)', name, service_id)
            self.manager.log.info(' - params: %s', params)
            service = self.load_service(service_id, name, params)
            service or self.manager.log.error('Unable to start service id %s name %s', service_id, name)
            return
        self.services[service.service_id] = service
        if configuration:
            for entry in configuration:
                setattr(service, entry, configuration[entry])

        if callbacks:
            service.callbacks = callbacks
        for handler in service.HANDLERS:
            api_manager = srv_or_die('apimanager')
            api_manager.register_handler(handler)
            handler.service = service

        self.manager.log.info('Starting service: %s (%s)', name, service_id)
        service.start()
        return service

    def stop_service(self, service_id):
        """Stop a service."""
        if service_id not in self.services:
            raise KeyError('Service %s not running' % service_id)
        self.services[service_id].stop()
        del self.services[service_id]

    def to_dict(self):
        """Return JSON-serializable representation of the object."""
        output = {}
        output['project_id'] = self.project_id
        output['bootstrap'] = self.bootstrap
        output['platform'] = {'machine':platform.machine(), 
         'node':platform.node(), 
         'platform':platform.platform(), 
         'processor':platform.processor(), 
         'python_version':platform.python_version(), 
         'release':platform.release(), 
         'system':platform.system(), 
         'version':platform.version()}
        return output

    def to_str(self):
        """Return an ASCII representation of the object."""
        return str(self.project_id)

    def __str__(self):
        return self.to_str()

    def __hash__(self):
        return hash(self.project_id)

    def __eq__(self, other):
        if isinstance(other, Env):
            return self.project_id == other.project_id
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"