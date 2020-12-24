# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/hookbox/user.py
# Compiled at: 2012-07-04 04:55:04
import logging, eventlet
from errors import ExpectedException
try:
    import json
except ImportError:
    import simplejson as json

import datetime

def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


class User(object):
    logger = logging.getLogger('HookboxUser')
    _options = {'reflective': True, 
       'moderated_message': True, 
       'per_connection_subscriptions': False, 
       'global_unsubscriptions': False, 
       'auto_subscribe': []}

    def __init__(self, server, name, **options):
        self.server = server
        self.name = name
        self.connections = []
        self.channels = {}
        self._temp_cookie = ''
        self.update_options(**self._options)
        self.update_options(**options)
        self._frame_errors = {}

    def serialize(self):
        return {'channels': [ chan_name for chan_name in self.channels ], 'connections': [ conn.id for conn in self.connections ], 'name': self.name, 
           'options': dict([ (key, getattr(self, key)) for key in self._options ])}

    def extract_valid_options(self, options):
        return dict([ (key, options.get(key, self._options[key])) for key in self._options ])

    def update_options(self, **options):
        for key, val in options.items():
            if key not in self._options:
                raise ValueError('Invalid keyword argument %s' % key)
            default = self._options[key]
            cls = default.__class__
            if cls in (unicode, str):
                cls = basestring
            if not isinstance(val, cls):
                raise ValueError('Invalid type for %s (should be %s)' % (key, default.__class__))
            if key == 'state':
                self.state_replace(val)
                continue
            if isinstance(val, dict):
                for _key, _val in val.items():
                    if _key not in self._options[key]:
                        raise ValueError('Invalid keyword argument %s' % _key)
                    default = self._options[key][_key]
                    cls = default.__class__
                    if isinstance(default, float) and isinstance(_val, int):
                        _val = float(_val)
                    if cls in (unicode, str):
                        cls = basestring
                    if not isinstance(_val, cls):
                        raise ValueError('%s is Invalid type for %s (should be %s)' % (_val, _key, default.__class__))

        for key, val in options.items():
            if isinstance(val, dict) and hasattr(self, key):
                getattr(self, key).update(val)
            else:
                setattr(self, key, val.__class__(val))

    def add_connection(self, conn):
        self.connections.append(conn)
        conn.user = self
        eventlet.spawn(self._send_initial_subscriptions, conn)

    def _send_initial_subscriptions(self, conn):
        for channel_name, channel_connections in self.channels.items():
            if self.server.exists_channel(channel_name):
                frame = self.server.get_channel(self, channel_name)._build_subscribe_frame(self)
                conn.send_frame('SUBSCRIBE', frame)

    def remove_connection(self, conn):
        if conn not in self.connections:
            return
        self.connections.remove(conn)
        for channel_name, channel_connections in self.channels.items():
            if conn in self.channels[channel_name]:
                if self.global_unsubscriptions:
                    del self.channels[channel_name][:]
                else:
                    self.channels[channel_name].remove(conn)
            if (self.per_connection_subscriptions or self.global_unsubscriptions) and not self.channels[channel_name]:
                if self.server.exists_channel(channel_name):
                    self.server.get_channel(self, channel_name).unsubscribe(self, needs_auth=True, force_auth=True)

        if not self.connections:
            self._temp_cookie = conn.get_cookie()
            for channel_name, connections in self.channels.items():
                if self.server.exists_channel(channel_name):
                    self.server.get_channel(self, channel_name).unsubscribe(self, needs_auth=True, force_auth=True)

            self.server.remove_user(self.name)

    def channel_subscribed(self, channel, conn=None):
        if channel.name not in self.channels:
            self.channels[channel.name] = [
             conn]
        elif conn not in self.channels[channel.name]:
            self.channels[channel.name].append(conn)

    def channel_unsubscribed(self, channel):
        if channel.name in self.channels:
            del self.channels[channel.name]

    def get_name(self):
        return self.name

    def send_frame(self, name, args={}, omit=None, channel=None):
        if not self.per_connection_subscriptions:
            channel = None
        if channel and channel.name not in self.channels:
            return
        else:
            for conn in (self.channels[channel.name] if channel else self.connections)[:]:
                if conn is not omit:
                    channel_name = channel.name if hasattr(channel, name) else '<no channel>'
                    msg = 'user: %s, conn: %s, channel:%s, frame:%s-%s' % (self.name, conn.id, channel_name, name, args)
                    if conn.send_frame(name, args) is False:
                        self.logger.info('send_frame ( error ): %s' % msg)
                        self.remove_connection(conn)

            return

    def add_frame_error(self, conn, name, args):
        if name in self._frame_errors:
            self._frame_errors[name].append((conn.id, args))
        else:
            self._frame_errors[name] = [
             (
              conn.id, args)]
        if name in self._frame_errors:
            error_conns = []
            for conn, e in self._frame_errors[name]:
                if e == args:
                    error_conns.append(conn)

            if error_conns:
                self.logger.warn('Error sending frame %s, %s to connections %s' % (name, args, error_conns))

    def add_frame_error(self, conn, name, args):
        if name in self._frame_errors:
            self._frame_errors[name].append((conn.id, args))
        else:
            self._frame_errors[name] = [
             (
              conn.id, args)]

    def get_cookie(self, conn=None):
        if conn:
            return conn.get_cookie()
        return self._temp_cookie or ''

    def send_message(self, recipient_name, payload, conn=None, needs_auth=True):
        try:
            encoded_payload = json.loads(payload)
        except:
            raise ExpectedException('Invalid json for payload')

        payload = encoded_payload
        if needs_auth and self.moderated_message:
            form = {'sender': self.get_name(), 'recipient': recipient_name, 'recipient_exists': self.server.exists_user(recipient_name), 'payload': json.dumps(payload)}
            success, options = self.server.http_request('message', self.get_cookie(conn), form, conn=conn)
            self.server.maybe_auto_subscribe(self, options, conn=conn)
            if not success:
                raise ExpectedException(options.get('error', 'Unauthorized'))
            payload = options.get('override_payload', payload)
            recipient_name = options.get('override_recipient_name', recipient_name)
        elif not self.server.exists_user(recipient_name):
            raise ExpectedException('Invalid user name')
        recipient = self.server.get_user(recipient_name) if self.server.exists_user(recipient_name) else None
        frame = {'sender': self.get_name(), 'recipient': recipient.get_name() if recipient else 'null', 'payload': payload, 'datetime': get_now()}
        if recipient:
            recipient.send_frame('MESSAGE', frame)
        if self.reflective and (not recipient or recipient.name != self.name):
            self.send_frame('MESSAGE', frame)
        return