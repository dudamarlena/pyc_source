# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grecco/Documents/code/pizco/pizco/agent.py
# Compiled at: 2012-11-09 15:26:09
"""
    pyzr
    ~~~~

    A small remoting framework with notification and async commands using ZMQ.

    :copyright: 2012 by Lantz Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import os, sys, uuid, pickle, inspect, logging, threading, subprocess
from collections import defaultdict, namedtuple
import zmq
from zmq.eventloop import zmqstream, ioloop
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
import socketserver
DEFAULT_LAUNCHER = os.environ.get('DEFAULT_LAUNCHER', None)
if not DEFAULT_LAUNCHER:
    DEFAULT_LAUNCHER = [
     '/usr/X11/bin/xterm', '-e']

def _uuid():
    """Generate a unique id for messages.
    """
    return uuid.uuid4().urn


class Signal(object):
    """PyQt like signal object
    """

    def __init__(self):
        self.slots = []

    def connect(self, slot):
        if slot not in self.slots:
            self.slots.append(slot)

    def disconnect(self, slot=None):
        if slot is None:
            self.slots = []
        self.slots.remove(slot)
        return

    def emit(self, *args):
        for slot in self.slots:
            slot(*args)


def bind(sock, endpoint='tcp://127.0.0.1:0'):
    """Bind socket to endpoint accepting a variety of endpoint formats.

    If connection is tcp and port is 0 or not given, it will call bind_to_random_port.

    :param sock: Socket to bind
    :type sock: zmq.Socket
    :param endpoint: endpoint to bind as string or (address, port) tuple
    :type endpoint: tuple or str

    :return: bound endpoint
    :rtype: str
    """
    if not endpoint:
        endpoint = 'tcp://127.0.0.1:0'
    else:
        if isinstance(endpoint, (tuple, list)):
            endpoint = 'tcp://{}:{}'.format(*endpoint)
        if endpoint.startswith('tcp://') and endpoint.endswith(':0'):
            endpoint = endpoint[:-2]
            port = sock.bind_to_random_port(endpoint)
            endpoint += ':' + str(port)
        else:
            sock.bind(endpoint)
    return endpoint


class RemoteAttribute(object):
    """Representing a remote attribute that can handle
     callables, container types, descriptors and signals.

    :param request: a callable used to send the request to the server, taking to arguments action and payload.
    :param name: name of the attribute.
    :param signal_manager:
    """

    def __init__(self, name, request, signal_manager):
        self.name = name
        self.request = request
        self.signal_manager = signal_manager

    def __get__(self, key):
        return self.request('exec', {'name': self.name,  'method': '__get__', 
         'args': (
                  key,)})

    def __set__(self, key, value):
        return self.request('exec', {'name': self.name,  'method': '__set__', 
         'args': (
                  key, value)})

    def __getitem__(self, key):
        return self.request('exec', {'name': self.name,  'method': '__getitem__', 
         'args': (
                  key,)})

    def __setitem__(self, key, value):
        return self.request('exec', {'name': self.name,  'method': '__setitem__', 
         'args': (
                  key, value)})

    def __call__(self, *args, **kwargs):
        payload = {'name': self.name,  'method': '__call__'}
        if args:
            payload['args'] = args
        if kwargs:
            payload['kwargs'] = kwargs
        return self.request('exec', payload)

    def connect(self, fun):
        logger.debug('Connecting {} to {}'.format(self.name, fun))
        self.signal_manager('connect', self.name, fun)

    def disconnect(self, fun):
        self.signal_manager('disconnect', self.name, fun)

    def emit(self, value, old_value, other):
        self.signal_manager('emit', self.name, (value, old_value, other))


class Agent(object):
    """An object that can communicate via ZMQ to other Agents.

    Each agent has:
    - a REP socket to receive requests
    - one REQ per each Agent that it has to talk to (stored in self.connections)
    - one PUB to emit notifications
    - one SUB to subscribe to notifications

    :param rep_endpoint: endpoint of the REP socket.
    :param pub_endpoint: endpoint of the PUB socket.
    :param ctx: ZMQ context, if None will use default context.
    :param loop: ZMQ event loop, if None will use default loop.
    """
    loop_thread = None
    loop_agent = defaultdict(list)

    def __init__(self, rep_endpoint='tcp://127.0.0.1:0', pub_endpoint='tcp://127.0.0.1:0', ctx=None, loop=None):
        self.ctx = ctx or zmq.Context.instance()
        self.loop = loop or ioloop.IOLoop.instance()
        logger.debug('New agent at {} with context {} and loop {}'.format(rep_endpoint, self.ctx, self.loop))
        self.connections = {}
        rep = self.ctx.socket(zmq.REP)
        self.rep_endpoint = bind(rep, rep_endpoint)
        logger.debug('Bound rep at {} REP.'.format(self.rep_endpoint, self.rep_endpoint))
        self.subscriptions = defaultdict(int)
        pub = self.ctx.socket(zmq.XPUB)
        self.pub_endpoint = bind(pub, pub_endpoint)
        logger.debug('{} PUB: {}'.format(self.rep_endpoint, self.pub_endpoint))
        sub = self.ctx.socket(zmq.SUB)
        self.sub_endpoint = bind(sub)
        logger.debug('{} SUB: {}'.format(self.rep_endpoint, self.sub_endpoint))
        self.notifications_callbacks = {}
        self.sub_connections = set()
        self._lock = threading.RLock()
        self.rep_to_pub = {}
        self._start(rep, pub, sub)
        logger.info('Started agent {}'.format(self.rep_endpoint))

    def _start(self, rep, pub, sub, in_callback=False):
        if self.loop.running() and not in_callback:
            self.loop.add_callback(lambda : self._start(rep, pub, sub, True))
        else:
            with self._lock:
                self.rep = zmqstream.ZMQStream(rep, self.loop)
                self.pub = zmqstream.ZMQStream(pub, self.loop)
                self.sub = zmqstream.ZMQStream(sub, self.loop)
                self.rep.on_recv_stream(self._on_request)
                self.pub.on_recv_stream(self._on_incoming_xpub)
                self.sub.on_recv_stream(self._on_notification)
                self.loop_agent[self.loop].append(self)
                self._Agent__running = True
        if not self.loop.running() and not in_callback:
            with self._lock:
                self.__class__.loop_thread = t = threading.Thread(target=self.loop.start, name='ioloop-{}'.format(id(self.loop)))
                t.daemon = True
                t.start()

    def stop(self):
        """Stop actor unsubscribing from all notification and closing the streams.
        """
        with self._lock:
            if not self._Agent__running:
                return
            self.publish('__status__', 'stop')
            for stream in (self.rep, self.pub, self.sub):
                self.loop.add_callback(stream.flush)
                self.loop.add_callback(lambda : stream.on_recv_stream(None))
                self.loop.add_callback(stream.close)

            self.loop_agent[self.loop].remove(self)
            if not self.loop_agent[self.loop]:
                del self.loop_agent[self.loop]
                self.loop.add_callback(lambda : self.loop.stop)
                self.loop.add_callback(lambda : self.loop.close)
            self._Agent__running = False
            logger.info('Stopped agent {}'.format(self.rep_endpoint))

    def __del__(self):
        self.stop()

    def request(self, recipient, content):
        """Send a request to another agent and waits for the response.

        Messages have the following structure (sender name, message id, content)
        This methods is executed in the calling thread.

        :param recipient: endpoint of the recipient.
        :param content: content to be sent.
        :return: The response of recipient.
        """
        logger.debug('{} -> {}: {}'.format(self, recipient, content))
        try:
            req = self.connections[recipient]
        except KeyError:
            req = self.ctx.socket(zmq.REQ)
            req.connect(recipient)
            self.connections[recipient] = req

        req.send_pyobj((self.rep_endpoint, _uuid(), content))
        return req.recv_pyobj()

    def _on_request(self, stream, message):
        """Handles incoming requests from other agents, dispatch them to
        on_request and send the response back on the same stream.

        Messages have the following structure (sender name, message id, message)
        This methods is executed in the IOLoop thread.
        """
        sender, msgid, content = pickle.loads(message[0])
        logger.debug('{} <- {}: ({}) {}'.format(self.rep_endpoint, sender, msgid, content))
        ret = self.on_request(sender, msgid, content)
        logger.debug('Return value for {}: {}'.format(msgid, ret))
        stream.send_pyobj((self.rep_endpoint, msgid, ret))

    def on_request(self, sender, msgid, content):
        """Handles incoming request from other agents and return the response
        that should be sent to the source.

        Overload this method on your class to provide an specific behaviour.
        Call super to enable

        This methods is executed in the IOLoop thread.

        :param sender: name of the sender.
        :param msgid: unique id of the message
        :param content: the actual content
        :return: message to be sent to the sender
        """
        if content == 'info':
            return {'rep_endpoint': self.rep_endpoint,  'pub_endpoint': self.pub_endpoint}
        if content == 'stop':
            cb = ioloop.DelayedCallback(self.stop, 0.1, self.loop)
            cb.start()
            return 'stopping'
        return content

    def _publish(self, topic, payload):
        """Publish a message to the PUB socket.

        This methods must be executed in IOLoop thread.

        """
        self.pub.send_string(topic, flags=zmq.SNDMORE)
        self.pub.send_pyobj(payload)

    def publish(self, topic, content):
        """Thread safe publish of a message to the PUB socket.

        Messages have the following structure: topic <STOP> (sender, message id, content)
        This method is executed in the calling thread, the actual publishing is done the IOLoop.

        :param topic: topic of the message.
        :param content: content of the message.
        """
        self.loop.add_callback(lambda : self._publish(topic, (self.rep_endpoint, _uuid, content)))

    def _on_incoming_xpub(self, stream, message):
        """Handles incoming message in the XPUB sockets, increments or decrements the subscribers
        per topic and dispatch to on_subscribe, on_unsubscribe
        Messages contain a byte indicating if a subscription or unsubscription and the topic.

        This methods is executed in the IOLoop thread.
        """
        message = message[0]
        action, topic = message[0] == 1, message[1:].decode('utf-8')
        logger.debug('Incoming XPUB {} {}'.format(action, topic))
        if action:
            self.subscriptions[topic] += 1
            self.on_subscribe(topic, self.subscriptions[topic])
        elif self.subscriptions[topic] > 0:
            self.subscriptions[topic] -= 1
            self.on_unsubscribe(topic, self.subscriptions[topic])

    def on_subscribe(self, topic, count):
        """Callback for incoming subscriptions.

        This methods is executed in the IOLoop thread.

        :param topic: a string with the topic.
        :param count: number of subscribers
        """
        pass

    def on_unsubscribe(self, topic, count):
        """Callback for incoming unsubscriptions.

        This methods is executed in the IOLoop thread.

        :param topic: a string with the topic.
        :param count: number of subscribers
        """
        pass

    def _subscribe(self, endpoint, topic):
        """Subscribe to a topic at endpoint.

        This methods must be executed in IOLoop thread.
        """
        if endpoint not in self.sub_connections:
            self.sub.connect(endpoint)
            self.sub_connections.add(endpoint)
        self.sub.setsockopt_string(zmq.SUBSCRIBE, topic)
        logger.debug('Subscription sent to {} {}'.format(endpoint, topic))

    def _unsubscribe(self, endpoint, topic):
        """Unsubscribe to a topic at endpoint.

        This methods must be executed in IOLoop thread.
        """
        self.sub.setsockopt_string(zmq.UNSUBSCRIBE, topic)
        logger.debug('Unsubscription sent to {} {}'.format(endpoint, topic))

    def subscribe(self, rep_endpoint, topic, callback=None, pub_endpoint=None):
        """Thread safe subscribe to a topic at endpoint from another agent
        and assign a callback for the specific endpoint and topic.

        Notice that Agent.subscribe_to_agent takes the rep_endpoint
        of the other agent.

        This method will be executed in main thread, the actual subscription is done the IOLoop.

        :param rep_endpoint: endpoint of an agent REP socket.
        :param topic: a string with the topic to subscribe.
        :param callback: a callable with the (sender, topic, content)
        :param pub_endpoint: endpoint of an agent PUB socket, if not given it will be queried.
        """
        pub_endpoint = pub_endpoint or self.rep_to_pub.get(rep_endpoint, None)
        if not pub_endpoint:
            ret = self.request(rep_endpoint, 'info')[(-1)]
            pub_endpoint = ret['pub_endpoint']
            self.rep_to_pub[rep_endpoint] = pub_endpoint
        elif rep_endpoint not in [rep_endpoint]:
            self.rep_to_pub[rep_endpoint] = pub_endpoint
        logger.debug('Subscribing to {} {} with {}'.format(rep_endpoint, topic, callback))
        self.loop.add_callback(lambda : self._subscribe(pub_endpoint, topic))
        self.notifications_callbacks[(rep_endpoint, topic)] = callback
        return

    def unsubscribe(self, rep_endpoint, topic, pub_endpoint=None):
        """Thread safe unsubscribe to a topic at endpoint and assign a callback
        for the specific endpoint and topic.

        This method will be executed in main thread, the actual unsubscription is done the IOLoop.

        :param rep_endpoint: endpoint of an agent REP socket.
        :param topic: a string with the topic to subscribe.
        :param pub_endpoint: endpoint of an agent PUB socket, if not given it will be queried.
        """
        pub_endpoint = pub_endpoint or self.rep_to_pub.get(rep_endpoint, None)
        if not pub_endpoint:
            ret = self.request(rep_endpoint, 'info')[(-1)]
            pub_endpoint = ret['pub_endpoint']
            self.rep_to_pub[rep_endpoint] = pub_endpoint
        logger.debug('Unsubscribing to {} {}'.format(rep_endpoint, topic))
        self.loop.add_callback(lambda : self._unsubscribe(pub_endpoint, topic))
        del self.notifications_callbacks[(rep_endpoint, topic)]
        return

    def _on_notification(self, stream, message):
        """Handles incoming messages in the SUB socket dispatching to a callback if provided or
        to on_notification.

        This methods is executed in the IOLoop thread.
        """
        topic, (sender, msgid, content) = message[0], pickle.loads(message[1])
        topic = topic.decode('utf-8')
        callback = self.notifications_callbacks[(sender, topic)]
        if callback:
            callback(sender, topic, msgid, content)
        else:
            self.on_notification(sender, topic, msgid, content)

    def on_notification(self, sender, topic, msgid, content):
        """Default notification callback for (sender, topic) in which a callback is not provided.

        Override this method to provide a custom behaviour.
        This methods is executed in the IOLoop thread.

        :param sender: sender of the notification.
        :param topic: topic of the notification.
        :param msgid: message id.
        :param content: content.
        """
        logger.debug('Received notification: {}, {}, {}, {}'.format(sender, topic, msgid, content))


def PSMessage(action, options):
    """Builds a message
    """
    return (
     'PSMessage', action, options)


class Server(Agent):
    """Serves an object for remote access from a Proxy. A Server can serve a single object.

    :param served_object: object to be served.

    .. seealso:: :class:`.Agent`
    .. seealso:: :class:`.Proxy`
    """

    def __init__(self, served_object, rep_endpoint='tcp://127.0.0.1:0', pub_endpoint='tcp://127.0.0.1:0', ctx=None, loop=None):
        self.served_object = served_object
        self.signal_calls = {}
        super().__init__(rep_endpoint, pub_endpoint, ctx, loop)

    def on_request(self, sender, msgid, content):
        """Handles Proxy Server communication, handling attribute access in served_object.

        Messages between proxy and server are handled using a tuple
        containing three elements: a string 'PSMessage', `action` and `options`.

        From Proxy to Server, valid actions are:

        - `exec`: execute a method from an attribute served object.
        - `getattr`: get an attribute from the served object.
        - `setattr`: set an attribute to the served object.
        - `get`: get an attribute from the served object, returning a remote object
                 when necessary.

        From Server to Proxy, valid action are:

        - `return`: return a value.
        - `remote`: return a RemoteAttribute object.
        - `raise`: raise an exception.

        """
        try:
            content_type, action, options = content
            if content_type != 'PSMessage':
                raise ValueError()
        except:
            return super().on_request(sender, msgid, content)

        try:
            if action == 'exec':
                attr = getattr(self.served_object, options['name'])
                meth = getattr(attr, options['method'])
                ret = meth(*options.get('args', ()), **options.get('kwargs', {}))
                return PSMessage('return', ret)
            if action == 'getattr':
                ret = getattr(self.served_object, options['name'])
                return PSMessage('return', ret)
            if action == 'setattr':
                setattr(self.served_object, options['name'], options['value'])
                return PSMessage('return', None)
            if action == 'get':
                attr = getattr(self.served_object, options['name'])
                if hasattr(attr, '__get__'):
                    return PSMessage('remote', None)
                if hasattr(attr, '__getitem__') or hasattr(attr, '__setitem__'):
                    return PSMessage('remote', None)
                else:
                    if callable(attr):
                        return PSMessage('remote', None)
                    if hasattr(attr, 'connect') and hasattr(attr, 'disconnect') and hasattr(attr, 'emit'):
                        return PSMessage('remote', None)
                    return PSMessage('return', attr)
            elif action == 'instantiate':
                if self.served_object is not None:
                    return PSMessage('raise', Exception('Cannot instantiate another object.'))
                else:
                    mod_name, class_name = options['class'].rsplit('.', 1)
                    mod = __import__(mod_name, fromlist=[class_name])
                    klass = getattr(mod, class_name)
                    self.served_object = klass(*options['args'], **options['kwargs'])
                    return PSMessage('return', None)
                ret = Exception('invalid message action {}'.format(action))
                return PSMessage('raise', ret)
        except Exception as ex:
            return PSMessage('raise', ex)

        return

    def emit(self, topic, value, old_value, other):
        logger.debug('Emitting {}, {}, {}, {}'.format(topic, value, old_value, other))
        self.publish(topic, (value, old_value, other))

    def on_subscribe(self, topic, count):
        if count == 1:
            logger.debug('Connecting {} signal on server'.format(topic))

            def fun(value, old_value=None, other=None):
                logger.debug('ready to emit')
                self.emit(topic, value, old_value, other)

            self.signal_calls[topic] = fun
            getattr(self.served_object, topic).connect(self.signal_calls[topic])
        return

    def on_unsubscribe(self, topic, count):
        if count == 0:
            logger.debug('Disconnecting {} signal on server'.format(topic))
            getattr(self.served_object, topic).disconnect(self.signal_calls[topic])
            del self.signal_calls[topic]

    @classmethod
    def serve_in_thread(cls, served_cls, args, kwargs, rep_endpoint, pub_endpoint='tcp://127.0.0.1:0'):
        t = threading.Thread(target=cls, args=(None, rep_endpoint, pub_endpoint), kwargs={'ctx': zmq.Context.instance(),  'loop': ioloop.IOLoop.instance()})
        t.start()
        proxy = Proxy(rep_endpoint)
        proxy._proxy_agent.instantiate(served_cls, args, kwargs)
        return proxy

    @classmethod
    def serve_in_process(cls, served_cls, args, kwargs, rep_endpoint, pub_endpoint='tcp://127.0.0.1:0', verbose=False):
        cwd = os.path.dirname(inspect.getfile(served_cls))
        cmd = [sys.executable, __file__, rep_endpoint, pub_endpoint, '-p', cwd]
        if verbose:
            cmd += ['-v']
        subprocess.Popen(DEFAULT_LAUNCHER + cmd, cwd=cwd)
        import time
        time.sleep(1)
        proxy = Proxy(rep_endpoint)
        proxy._proxy_agent.instantiate(served_cls, args, kwargs)
        return proxy

    def serve_forever(self):
        self.__class__.loop_thread.join()
        print('joined')


class ProxyAgent(Agent):
    """Helper class that handles Proxy to Server communication.

    :param remote_rep_endpoint: REP endpoint of the Server.
    """

    def __init__(self, remote_rep_endpoint):
        super().__init__()
        self.remote_rep_endpoint = remote_rep_endpoint
        ret = self.request(self.remote_rep_endpoint, 'info')[(-1)]
        self.remote_pub_endpoint = ret['pub_endpoint']
        logger.debug('Started Proxy pointing to REP: {} and PUB: {}'.format(self.remote_rep_endpoint, self.remote_pub_endpoint))
        self._signals = defaultdict(Signal)

    def request_server(self, action, options):
        """Sends a request to the associated server using PSMessage

        :param action: action to be sent.
        :param options: options of the action.
        :return:
        """
        sender, msgid, content = self.request(self.remote_rep_endpoint, PSMessage(action, options))
        try:
            ret_type, ret_action, ret_options = content
            if ret_type != 'PSMessage':
                raise ValueError
        except:
            raise ValueError('Invalid response from Server {}'.format(content))

        if ret_action == 'raise':
            raise ret_options
        else:
            if ret_action == 'remote':
                return RemoteAttribute(options['name'], self.request_server, self.signal_manager)
            if ret_action == 'return':
                return ret_options
            raise ValueError('Unknown {}'.format(ret_action))

    def signal_manager(self, action, signal_name, fun):
        if action == 'connect':
            if not self._signals[(self.remote_rep_endpoint, signal_name)].slots:
                self.subscribe(self.remote_rep_endpoint, signal_name, None, self.remote_pub_endpoint)
            self._signals[(self.remote_rep_endpoint, signal_name)].connect(fun)
        else:
            if action == 'disconnect':
                self._signals[(self.remote_rep_endpoint, signal_name)].disconnect(fun)
                if not self._signals[(self.remote_rep_endpoint, signal_name)].slots:
                    self.unsubscribe(self.remote_rep_endpoint, signal_name, self.remote_pub_endpoint)
            else:
                raise ValueError(action)
        return

    def on_notification(self, sender, topic, msgid, content):
        try:
            self._signals[(sender, topic)].emit(*content)
        except KeyError:
            super().on_notification(sender, topic, msgid, content)

    def instantiate(self, served_cls, args, kwargs):
        if not isinstance(served_cls, str):
            served_cls = served_cls.__module__ + '.' + served_cls.__name__
        self.request_server('instantiate', {'class': served_cls,  'args': args,  'kwargs': kwargs})


class Proxy(object):
    """Proxy object to access a server.

    :param remote_endpoint: endpoint of the server.
    """

    def __init__(self, remote_endpoint):
        self._proxy_agent = ProxyAgent(remote_endpoint)

    def __getattr__(self, item):
        if item.startswith('_proxy_'):
            return super().__getattr__(item)
        return self._proxy_agent.request_server('get', {'name': item})

    def __setattr__(self, item, value):
        if item.startswith('_proxy_'):
            super().__setattr__(item, value)
            return
        return self._proxy_agent.request_server('setattr', {'name': item,  'value': value})

    def _proxy_stop_server(self):
        self._proxy_agent.request(self._proxy_agent.remote_rep_endpoint, 'stop')

    def _proxy_stop_me(self):
        self._proxy_agent.stop()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('Starts an server')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-p', '--path', type=str)
    parser.add_argument('rep_endpoint')
    parser.add_argument('pub_endpoint')
    args = parser.parse_args()
    if args.path:
        sys.path.append(args.path)
    if args.verbose:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
    s = Server(None, args.rep_endpoint, args.pub_endpoint)
    print('Server started at {}'.format(s.rep_endpoint))
    s.serve_forever()
    print('Server stopped')