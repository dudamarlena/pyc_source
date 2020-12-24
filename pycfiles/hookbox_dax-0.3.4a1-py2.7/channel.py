# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/hookbox/channel.py
# Compiled at: 2012-07-04 04:55:04
import urllib, eventlet
from errors import ExpectedException
try:
    import json
except ImportError:
    import simplejson as json

import datetime

def get_now():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')


class Channel(object):
    _options = {'reflective': True, 
       'history': [], 'history_size': 0, 
       'history_duration': 0, 
       'history_publish_only': False, 
       'moderated': True, 
       'moderated_publish': False, 
       'moderated_subscribe': False, 
       'moderated_unsubscribe': False, 
       'presenceful': False, 
       'server_presenceful': False, 
       'server_user_presence': [], 'anonymous': False, 
       'polling': {'mode': '', 
                   'interval': 5.0, 
                   'url': '', 
                   'form': {}, 'originator': ''}, 
       'state': {}}

    def __init__(self, server, name, **options):
        self.server = server
        self.name = name
        self.subscribers = []
        self.history = []
        self._polling_task = None
        self._polling_lock = eventlet.semaphore.Semaphore()
        self.state = {}
        self.update_options(**self._options)
        self.update_options(**options)
        return

    def set_history(self, history):
        self.history = history
        self.prune_history()

    def prune_history(self):
        while len(self.history) > self.history_size:
            self.history.pop(0)

        if self.history_duration > 0:
            limit = datetime.datetime.now() - datetime.timedelta(seconds=self.history_duration)
            limit_str = limit.strftime('%Y-%m-%dT%H:%M:%S')
            while len(self.history) > 0 and self.history[0][1]['datetime'] < limit_str:
                self.history.pop(0)

    def update_options(self, notify_polling=True, **options):
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

        if 'polling' in options and notify_polling:
            self.polling_modified()

    def polling_modified(self):
        self._polling_lock.acquire()
        if self._polling_task:
            self._polling_task.kill()
        if self.polling['mode'] in ('once', 'simple', 'persistent'):
            self._polling_task = eventlet.spawn(self._poll)
        self._polling_lock.release()

    def _poll(self):
        while True:
            mode = self.polling['mode']
            interval = self.polling['interval']
            if mode == None:
                return
            eventlet.sleep(interval)
            max_backoff = max(300, interval)
            backoff_interval = 1
            while True:
                self._polling_lock.acquire()
                try:
                    if mode == 'simple':
                        payload = urllib.urlopen(self.polling['url']).read()
                        try:
                            payload = json.loads(payload)
                        except:
                            pass

                        success = True
                        options = {}
                    else:
                        success, options = self.server.http_request(form=self.polling['form'], full_path=self.polling['url'])
                        payload = options.pop('payload', None)
                except Exception as e:
                    self._polling_lock.release()
                    backoff_interval = min(backoff_interval * 2, max_backoff)
                    eventlet.sleep(backoff_interval)
                    continue

                break

            try:
                self.update_options(notify_polling=False, **options)
            except Exception as e:
                pass

            payload = json.dumps(payload)
            self.publish(None, payload, needs_auth=False, originator=self.polling['originator'])
            self._polling_lock.release()
            if 'polling' in options or self.polling['mode'] in ('simple', 'persistent'):
                continue
            return

        return

    def publish(self, user, payload, needs_auth=True, conn=None, **kwargs):
        try:
            encoded_payload = json.loads(payload)
        except:
            raise ExpectedException('Invalid json for payload')

        payload, options = encoded_payload, {}
        if needs_auth and (self.moderated or self.moderated_publish):
            form = {'channel_name': self.name, 'payload': json.dumps(encoded_payload)}
            if not self.anonymous:
                if 'originator' in kwargs:
                    form['originator'] = kwargs['originator']
                else:
                    form['originator'] = user.get_name()
            success, options = self.server.http_request('publish', user.get_cookie(conn), form, conn=conn)
            self.server.maybe_auto_subscribe(user, options, conn=conn)
            if not success:
                raise ExpectedException(options.get('error', 'Unauthorized'))
            payload = options.get('override_payload', payload)
        frame = {'channel_name': self.name, 'payload': payload, 'datetime': get_now()}
        if not self.anonymous:
            if 'originator' in kwargs:
                frame['user'] = kwargs['originator']
            else:
                frame['user'] = user.get_name()
        omit = None
        if not self.reflective:
            omit = conn
        if options.get('only_to_sender', False):
            user.send_frame('PUBLISH', frame, omit=omit, channel=self)
        else:
            for subscriber in self.subscribers:
                subscriber.send_frame('PUBLISH', frame, omit=omit, channel=self)

        self.server.admin.channel_event('publish', self.name, frame)
        if self.history_size:
            del frame['channel_name']
            self.history.append(('PUBLISH', frame))
            self.prune_history()
        return

    def subscribe(self, user, conn=None, needs_auth=True):
        if user in self.subscribers:
            user.channel_subscribed(self, conn=conn)
            return
        else:
            has_initial_data = False
            initial_data = None
            if needs_auth and (self.moderated or self.moderated_subscribe):
                form = {'channel_name': self.name, 'user': user.get_name()}
                success, options = self.server.http_request('subscribe', user.get_cookie(conn), form, conn=conn)
                if not success:
                    raise ExpectedException(options.get('error', 'Unauthorized'))
                if 'initial_data' in options:
                    has_initial_data = True
                    initial_data = options['initial_data']
                self.server.maybe_auto_subscribe(user, options, conn=conn)
            self.subscribers.append(user)
            user.channel_subscribed(self, conn=conn)
            _now = get_now()
            frame = {'channel_name': self.name, 'user': user.get_name(), 'datetime': _now}
            self.server.admin.channel_event('subscribe', self.name, frame)
            if self.presenceful:
                for subscriber in self.subscribers:
                    if subscriber == user:
                        continue
                    subscriber.send_frame('SUBSCRIBE', frame, channel=self)

            frame = self._build_subscribe_frame(user, initial_data)
            user.send_frame('SUBSCRIBE', frame, channel=self)
            if self.history_size and not self.history_publish_only:
                self.history.append(('SUBSCRIBE', {'user': user.get_name(), 'datetime': _now}))
                self.prune_history()
            return

    def state_del(self, key):
        if key not in self.state:
            return
        del self.state[key]
        self.state_broadcast(deletes=[key])

    def state_set(self, key, val):
        if key in self.state and self.state[key] == val:
            return
        self.state[key] = val
        self.state_broadcast(updates={key: val})

    def state_multi_set(self, state):
        updates = {}
        for k, v in state.iteritems():
            if k in self.state and self.state[k] == v:
                pass
            else:
                self.state[k] = v
                updates[k] = v

        self.state_broadcast(updates=updates)

    def state_broadcast(self, updates={}, deletes=[]):
        frame = {'channel_name': self.name, 
           'updates': updates, 
           'deletes': deletes}
        for subscriber in self.subscribers:
            subscriber.send_frame('STATE_UPDATE', frame, channel=self)

    def state_replace(self, state):
        checked_keys = []
        updates = []
        deletes = []
        adds = []
        for key in self.state:
            checked_keys.append(key)
            if key not in state:
                deletes.append(key)
            elif state[key] != self.state[key]:
                updates.append(key)

        for key in state:
            if key in checked_keys:
                continue
            adds.append(key)

        changes = {'updates': dict([ (k, state[k]) for k in updates + adds ]), 'deletes': deletes}
        if state:
            self.state = state
        else:
            self.state = {}
        self.state_broadcast(**changes)

    def _build_subscribe_frame(self, user, initial_data=None):
        frame = {'channel_name': self.name, 'user': user.get_name()}
        frame['history'] = self.history
        frame['history_size'] = self.history_size
        frame['history_duration'] = self.history_duration
        frame['state'] = self.state
        if initial_data:
            frame['initial_data'] = initial_data
        if self.presenceful:
            frame['presence'] = [ subscriber.get_name() for subscriber in self.subscribers ]
        else:
            frame['presence'] = []
        return frame

    def unsubscribe(self, user, conn=None, needs_auth=True, force_auth=False, destroy_empty=True):
        if user not in self.subscribers:
            return
        if needs_auth and (self.moderated or self.moderated_unsubscribe):
            form = {'channel_name': self.name, 'user': user.get_name()}
            try:
                success, options = self.server.http_request('unsubscribe', user.get_cookie(conn), form, conn=conn)
            except ExpectedException:
                if not force_auth:
                    raise
                success, options = False, {}

            if not (success or force_auth):
                raise ExpectedException(options.get('error', 'Unauthorized'))
            self.server.maybe_auto_subscribe(user, options, conn=conn)
        frame = {'channel_name': self.name, 'user': user.get_name(), 'datetime': get_now()}
        self.server.admin.channel_event('unsubscribe', self.name, frame)
        if self.presenceful:
            for subscriber in self.subscribers:
                if subscriber == user:
                    continue
                subscriber.send_frame('UNSUBSCRIBE', frame, channel=self)

        user.send_frame('UNSUBSCRIBE', frame, channel=self)
        try:
            self.subscribers.remove(user)
        except ValueError:
            pass

        user.channel_unsubscribed(self)
        if self.history_size and not self.history_publish_only:
            del frame['channel_name']
            self.history.append(('UNSUBSCRIBE', frame))
            self.prune_history()
        if not self.subscribers and destroy_empty:
            self.server.destroy_channel(self.name)

    def destroy(self, needs_auth=True):
        success = True
        if needs_auth:
            form = {'channel_name': self.name}
            try:
                success, options = self.server.http_request('destroy_channel', form=form)
            except ExpectedException:
                return False

        if success:
            self.presenceful = False
            for user in self.subscribers:
                self.unsubscribe(user, needs_auth=needs_auth, force_auth=True, destroy_empty=False)

        return success

    def serialize(self):
        return {'name': self.name, 
           'options': dict([ (key, getattr(self, key)) for key in self._options ]), 
           'subscribers': [ user.name for user in self.subscribers ]}