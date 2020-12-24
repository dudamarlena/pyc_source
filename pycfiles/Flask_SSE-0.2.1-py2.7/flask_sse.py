# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/flask_sse.py
# Compiled at: 2016-04-15 16:55:22
from __future__ import unicode_literals
from collections import OrderedDict
from flask import Blueprint, request, current_app, json, stream_with_context
from redis import StrictRedis
import six
__version__ = b'0.2.1'

@six.python_2_unicode_compatible
class Message(object):
    """
    Data that is published as a server-sent event.
    """

    def __init__(self, data, type=None, id=None, retry=None):
        """
        Create a server-sent event.

        :param data: The event data. If it is not a string, it will be
            serialized to JSON using the Flask application's
            :class:`~flask.json.JSONEncoder`.
        :param type: An optional event type.
        :param id: An optional event ID.
        :param retry: An optional integer, to specify the reconnect time for
            disconnected clients of this stream.
        """
        self.data = data
        self.type = type
        self.id = id
        self.retry = retry

    def to_dict(self):
        """
        Serialize this object to a minimal dictionary, for storing in Redis.
        """
        d = {b'data': self.data}
        if self.type:
            d[b'type'] = self.type
        if self.id:
            d[b'id'] = self.id
        if self.retry:
            d[b'retry'] = self.retry
        return d

    def __str__(self):
        """
        Serialize this object to a string, according to the `server-sent events
        specification <https://www.w3.org/TR/eventsource/>`_.
        """
        if isinstance(self.data, six.string_types):
            data = self.data
        else:
            data = json.dumps(self.data)
        lines = [ (b'data:{value}').format(value=line) for line in data.splitlines() ]
        if self.type:
            lines.insert(0, (b'event:{value}').format(value=self.type))
        if self.id:
            lines.append((b'id:{value}').format(value=self.id))
        if self.retry:
            lines.append((b'retry:{value}').format(value=self.retry))
        return (b'\n').join(lines) + b'\n\n'

    def __repr__(self):
        kwargs = OrderedDict()
        if self.type:
            kwargs[b'type'] = self.type
        if self.id:
            kwargs[b'id'] = self.id
        if self.retry:
            kwargs[b'retry'] = self.retry
        kwargs_repr = (b'').join((b', {key}={value!r}').format(key=key, value=value) for key, value in kwargs.items())
        return (b'{classname}({data!r}{kwargs})').format(classname=self.__class__.__name__, data=self.data, kwargs=kwargs_repr)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.data == other.data and self.type == other.type and self.id == other.id and self.retry == other.retry


class ServerSentEventsBlueprint(Blueprint):
    """
    A :class:`flask.Blueprint` subclass that knows how to publish, subscribe to,
    and stream server-sent events.
    """

    @property
    def redis(self):
        """
        A :class:`redis.StrictRedis` instance, configured to connect to the
        current application's Redis server.
        """
        redis_url = current_app.config.get(b'SSE_REDIS_URL')
        if not redis_url:
            redis_url = current_app.config.get(b'REDIS_URL')
        if not redis_url:
            raise KeyError(b'Must set a redis connection URL in app config.')
        return StrictRedis.from_url(redis_url)

    def publish(self, data, type=None, id=None, retry=None, channel=b'sse'):
        """
        Publish data as a server-sent event.

        :param data: The event data. If it is not a string, it will be
            serialized to JSON using the Flask application's
            :class:`~flask.json.JSONEncoder`.
        :param type: An optional event type.
        :param id: An optional event ID.
        :param retry: An optional integer, to specify the reconnect time for
            disconnected clients of this stream.
        :param channel: If you want to direct different events to different
            clients, you may specify a channel for this event to go to.
            Only clients listening to the same channel will receive this event.
            Defaults to "sse".
        """
        message = Message(data, type=type, id=id, retry=retry)
        msg_json = json.dumps(message.to_dict())
        return self.redis.publish(channel=channel, message=msg_json)

    def messages(self, channel=b'sse'):
        """
        A generator of :class:`~flask_sse.Message` objects from the given channel.
        """
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        for pubsub_message in pubsub.listen():
            if pubsub_message[b'type'] == b'message':
                msg_dict = json.loads(pubsub_message[b'data'])
                yield Message(**msg_dict)

    def stream(self):
        """
        A view function that streams server-sent events. Ignores any
        :mailheader:`Last-Event-ID` headers in the HTTP request.
        Use a "channel" query parameter to stream events from a different
        channel than the default channel (which is "sse").
        """
        channel = request.args.get(b'channel') or b'sse'

        @stream_with_context
        def generator():
            for message in self.messages(channel=channel):
                yield str(message)

        return current_app.response_class(generator(), mimetype=b'text/event-stream')


sse = ServerSentEventsBlueprint(b'sse', __name__)
sse.add_url_rule(rule=b'', endpoint=b'stream', view_func=sse.stream)