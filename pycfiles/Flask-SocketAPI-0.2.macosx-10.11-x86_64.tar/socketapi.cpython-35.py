# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/tmp/Flask-SocketAPI/venv/lib/python3.5/site-packages/flask_socketapi/socketapi.py
# Compiled at: 2016-07-11 08:08:31
# Size of source mod 2**32: 7830 bytes
from functools import wraps
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from flask import current_app, request
from flask_socketio import join_room, leave_room
from .exc import InvalidRequestError, InvalidURIError, SocketAPIError

class SocketAPI(object):

    def __init__(self, socketio=None, namespace=None):
        self.namespace = namespace
        self.routes = Map()
        self.urls = self.routes.bind('/', '/')
        self.patch_handlers = {}
        if socketio is not None:
            self.init_socketio(socketio)

    def init_socketio(self, socketio):
        self.socketio = socketio

        @socketio.on('create', namespace=self.namespace)
        def handle_create(payload):
            if 'uri' not in payload:
                raise InvalidRequestError('missing URI')
            uri = payload['uri']
            attributes = payload.get('attributes', {})
            try:
                creator, kwargs = self.urls.match(uri, method='POST')
            except HTTPException:
                raise InvalidRequestError("no registered resource creator for %s'" % uri)

            kwargs.update(attributes)
            resource = creator(**kwargs)
            self.socketio.emit('create', {'uri': uri, 
             'resource': resource}, room=uri)

        @socketio.on('patch')
        def handle_patch(payload, namespace=self.namespace):
            if 'uri' not in payload:
                raise InvalidRequestError('missing URI')
            uri = payload['uri']
            patch = payload.get('patch', {})
            try:
                rule, kwargs = self.urls.match(uri, return_rule=True, method='PATCH')
                kwargs['patch'] = patch
            except HTTPException:
                raise InvalidRequestError("no registered resource patcher for %s'" % uri)

            for patch_handler in self.patch_handlers[rule.rule]:
                patch_handler(**kwargs)

            for room_name in (uri, uri[0:len(uri) - len(uri.split('/')[(-1)])]):
                self.socketio.emit('patch', {'uri': uri, 
                 'patch': patch}, room=room_name)

        @socketio.on('delete', namespace=self.namespace)
        def handle_delete(payload):
            if 'uri' not in payload:
                raise InvalidRequestError('missing URI')
            uri = payload['uri']
            try:
                deleter, kwargs = self.urls.match(uri, method='DELETE')
            except HTTPException:
                raise InvalidRequestError("no registered resource deleter for %s'" % uri)

            resource = deleter(**kwargs)
            for room_name in (uri, uri[0:len(uri) - len(uri.split('/')[(-1)])]):
                self.socketio.emit('delete', {'uri': uri}, room=room_name)

        @socketio.on('subscribe', namespace=self.namespace)
        def handle_subscribe(uri):
            try:
                getter, kwargs = self.urls.match(uri, method='GET')
                resource = getter(**kwargs)
            except HTTPException:
                resource = None

            if resource is not None:
                self.socketio.emit('state', {'uri': uri, 
                 'resource': resource}, room=request.sid)
            join_room(uri)

        @socketio.on('unsubscribe', namespace=self.namespace)
        def handle_unsubscribe(uri):
            leave_room(uri)

        @socketio.on_error(self.namespace)
        def handle_error(e):
            if isinstance(e, SocketAPIError):
                self.socketio.emit('api_error', {'error': e.__class__.__name__, 
                 'message': str(e)}, room=request.sid)
            else:
                self.socketio.emit('server_error', {'error': e.__class__.__name__, 
                 'message': str(e) if current_app.debug else None}, room=request.sid)
            current_app.logger.exception(e)

    def resource_creator(self, rule):
        if not rule.endswith('/'):
            raise InvalidURIError('resource creators should be registered on list uri')

        def decorate(fn):

            @wraps(fn)
            def decorated(*args, **kwargs):
                return fn(*args, **kwargs)

            self.routes.add(Rule(rule, endpoint=decorated, methods=['POST']))
            return decorated

        return decorate

    def resource_getter(self, rule):

        def decorate(fn):

            @wraps(fn)
            def decorated(*args, **kwargs):
                return fn(*args, **kwargs)

            self.routes.add(Rule(rule, endpoint=decorated, methods=['GET']))
            return decorated

        return decorate

    def resource_patcher(self, rule):
        if rule.endswith('/'):
            raise InvalidURIError('cannot register resource patchers on a list uri')

        def decorate(fn):

            @wraps(fn)
            def decorated(*args, **kwargs):
                return fn(*args, **kwargs)

            for route in self.routes.iter_rules():
                if route.rule == rule and 'PATCH' in route.methods:
                    break
            else:
                self.routes.add(Rule(rule, methods=['PATCH']))

            if rule not in self.patch_handlers:
                self.patch_handlers[rule] = []
            self.patch_handlers[rule].append(decorated)
            return decorated

        return decorate

    def resource_deleter(self, rule):
        if rule.endswith('/'):
            raise InvalidURIError('cannot register resource deleters on a list uri')

        def decorate(fn):

            @wraps(fn)
            def decorated(*args, **kwargs):
                return fn(*args, **kwargs)

            self.routes.add(Rule(rule, endpoint=decorated, methods=['DELETE']))
            return decorated

        return decorate