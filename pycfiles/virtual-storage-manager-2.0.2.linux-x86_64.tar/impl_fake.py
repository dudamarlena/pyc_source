# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/rpc/impl_fake.py
# Compiled at: 2016-06-13 14:11:03
"""Fake RPC implementation which calls proxy methods directly with no
queues.  Casts will block, but this is very useful for tests.
"""
import inspect, json, time, eventlet
from vsm.openstack.common.rpc import common as rpc_common
CONSUMERS = {}

class RpcContext(rpc_common.CommonRpcContext):

    def __init__(self, **kwargs):
        super(RpcContext, self).__init__(**kwargs)
        self._response = []
        self._done = False

    def deepcopy(self):
        values = self.to_dict()
        new_inst = self.__class__(**values)
        new_inst._response = self._response
        new_inst._done = self._done
        return new_inst

    def reply(self, reply=None, failure=None, ending=False):
        if ending:
            self._done = True
        if not self._done:
            self._response.append((reply, failure))


class Consumer(object):

    def __init__(self, topic, proxy):
        self.topic = topic
        self.proxy = proxy

    def call(self, context, version, method, args, timeout):
        done = eventlet.event.Event()

        def _inner():
            ctxt = RpcContext.from_dict(context.to_dict())
            try:
                rval = self.proxy.dispatch(context, version, method, **args)
                res = []
                for reply, failure in ctxt._response:
                    if failure:
                        raise failure[0], failure[1], failure[2]
                    res.append(reply)

                if not ctxt._done:
                    if inspect.isgenerator(rval):
                        for val in rval:
                            res.append(val)

                    else:
                        res.append(rval)
                done.send(res)
            except rpc_common.ClientException as e:
                done.send_exception(e._exc_info[1])
            except Exception as e:
                done.send_exception(e)

        thread = eventlet.greenthread.spawn(_inner)
        if timeout:
            start_time = time.time()
            while not done.ready():
                eventlet.greenthread.sleep(1)
                cur_time = time.time()
                if cur_time - start_time > timeout:
                    thread.kill()
                    raise rpc_common.Timeout()

        return done.wait()


class Connection(object):
    """Connection object."""

    def __init__(self):
        self.consumers = []

    def create_consumer(self, topic, proxy, fanout=False):
        consumer = Consumer(topic, proxy)
        self.consumers.append(consumer)
        if topic not in CONSUMERS:
            CONSUMERS[topic] = []
        CONSUMERS[topic].append(consumer)

    def close(self):
        for consumer in self.consumers:
            CONSUMERS[consumer.topic].remove(consumer)

        self.consumers = []

    def consume_in_thread(self):
        pass


def create_connection(conf, new=True):
    """Create a connection"""
    return Connection()


def check_serialize(msg):
    """Make sure a message intended for rpc can be serialized."""
    json.dumps(msg)


def multicall(conf, context, topic, msg, timeout=None):
    """Make a call that returns multiple times."""
    check_serialize(msg)
    method = msg.get('method')
    if not method:
        return
    else:
        args = msg.get('args', {})
        version = msg.get('version', None)
        try:
            consumer = CONSUMERS[topic][0]
        except (KeyError, IndexError):
            return iter([None])

        return consumer.call(context, version, method, args, timeout)
        return


def call(conf, context, topic, msg, timeout=None):
    """Sends a message on a topic and wait for a response."""
    rv = multicall(conf, context, topic, msg, timeout)
    rv = list(rv)
    if not rv:
        return
    return rv[(-1)]


def cast(conf, context, topic, msg):
    check_serialize(msg)
    try:
        call(conf, context, topic, msg)
    except Exception:
        pass


def notify(conf, context, topic, msg, envelope):
    check_serialize(msg)


def cleanup():
    pass


def fanout_cast(conf, context, topic, msg):
    """Cast to all consumers of a topic"""
    check_serialize(msg)
    method = msg.get('method')
    if not method:
        return
    else:
        args = msg.get('args', {})
        version = msg.get('version', None)
        for consumer in CONSUMERS.get(topic, []):
            try:
                consumer.call(context, version, method, args, None)
            except Exception:
                pass

        return