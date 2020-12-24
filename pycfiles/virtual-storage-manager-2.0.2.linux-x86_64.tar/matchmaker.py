# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/rpc/matchmaker.py
# Compiled at: 2016-06-13 14:11:03
"""
The MatchMaker classes should except a Topic or Fanout exchange key and
return keys for direct exchanges, per (approximate) AMQP parlance.
"""
import contextlib, itertools, json, eventlet
from oslo.config import cfg
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import log as logging
matchmaker_opts = [
 cfg.StrOpt('matchmaker_ringfile', default='/etc/nova/matchmaker_ring.json', help='Matchmaker ring file (JSON)'),
 cfg.IntOpt('matchmaker_heartbeat_freq', default='300', help='Heartbeat frequency'),
 cfg.IntOpt('matchmaker_heartbeat_ttl', default='600', help='Heartbeat time-to-live.')]
CONF = cfg.CONF
CONF.register_opts(matchmaker_opts)
LOG = logging.getLogger(__name__)
contextmanager = contextlib.contextmanager

class MatchMakerException(Exception):
    """Signified a match could not be found."""
    message = _('Match not found by MatchMaker.')


class Exchange(object):
    """
    Implements lookups.
    Subclass this to support hashtables, dns, etc.
    """

    def __init__(self):
        pass

    def run(self, key):
        raise NotImplementedError()


class Binding(object):
    """
    A binding on which to perform a lookup.
    """

    def __init__(self):
        pass

    def test(self, key):
        raise NotImplementedError()


class MatchMakerBase(object):
    """
    Match Maker Base Class.
    Build off HeartbeatMatchMakerBase if building a
    heartbeat-capable MatchMaker.
    """

    def __init__(self):
        self.bindings = []
        self.no_heartbeat_msg = _('Matchmaker does not implement registration or heartbeat.')

    def register(self, key, host):
        """
        Register a host on a backend.
        Heartbeats, if applicable, may keepalive registration.
        """
        pass

    def ack_alive(self, key, host):
        """
        Acknowledge that a key.host is alive.
        Used internally for updating heartbeats,
        but may also be used publically to acknowledge
        a system is alive (i.e. rpc message successfully
        sent to host)
        """
        pass

    def is_alive(self, topic, host):
        """
        Checks if a host is alive.
        """
        pass

    def expire(self, topic, host):
        """
        Explicitly expire a host's registration.
        """
        pass

    def send_heartbeats(self):
        """
        Send all heartbeats.
        Use start_heartbeat to spawn a heartbeat greenthread,
        which loops this method.
        """
        pass

    def unregister(self, key, host):
        """
        Unregister a topic.
        """
        pass

    def start_heartbeat(self):
        """
        Spawn heartbeat greenthread.
        """
        pass

    def stop_heartbeat(self):
        """
        Destroys the heartbeat greenthread.
        """
        pass

    def add_binding(self, binding, rule, last=True):
        self.bindings.append((binding, rule, False, last))

    def queues(self, key):
        workers = []
        for binding, exchange, bit, last in self.bindings:
            if binding.test(key):
                workers.extend(exchange.run(key))
                if last:
                    return workers

        return workers


class HeartbeatMatchMakerBase(MatchMakerBase):
    """
    Base for a heart-beat capable MatchMaker.
    Provides common methods for registering,
    unregistering, and maintaining heartbeats.
    """

    def __init__(self):
        self.hosts = set()
        self._heart = None
        self.host_topic = {}
        super(HeartbeatMatchMakerBase, self).__init__()
        return

    def send_heartbeats(self):
        """
        Send all heartbeats.
        Use start_heartbeat to spawn a heartbeat greenthread,
        which loops this method.
        """
        for key, host in self.host_topic:
            self.ack_alive(key, host)

    def ack_alive(self, key, host):
        """
        Acknowledge that a host.topic is alive.
        Used internally for updating heartbeats,
        but may also be used publically to acknowledge
        a system is alive (i.e. rpc message successfully
        sent to host)
        """
        raise NotImplementedError('Must implement ack_alive')

    def backend_register(self, key, host):
        """
        Implements registration logic.
        Called by register(self,key,host)
        """
        raise NotImplementedError('Must implement backend_register')

    def backend_unregister(self, key, key_host):
        """
        Implements de-registration logic.
        Called by unregister(self,key,host)
        """
        raise NotImplementedError('Must implement backend_unregister')

    def register(self, key, host):
        """
        Register a host on a backend.
        Heartbeats, if applicable, may keepalive registration.
        """
        self.hosts.add(host)
        self.host_topic[(key, host)] = host
        key_host = ('.').join((key, host))
        self.backend_register(key, key_host)
        self.ack_alive(key, host)

    def unregister(self, key, host):
        """
        Unregister a topic.
        """
        if (
         key, host) in self.host_topic:
            del self.host_topic[(key, host)]
        self.hosts.discard(host)
        self.backend_unregister(key, ('.').join((key, host)))
        LOG.info(_('Matchmaker unregistered: %s, %s' % (key, host)))

    def start_heartbeat(self):
        """
        Implementation of MatchMakerBase.start_heartbeat
        Launches greenthread looping send_heartbeats(),
        yielding for CONF.matchmaker_heartbeat_freq seconds
        between iterations.
        """
        if len(self.hosts) == 0:
            raise MatchMakerException(_('Register before starting heartbeat.'))

        def do_heartbeat():
            while True:
                self.send_heartbeats()
                eventlet.sleep(CONF.matchmaker_heartbeat_freq)

        self._heart = eventlet.spawn(do_heartbeat)

    def stop_heartbeat(self):
        """
        Destroys the heartbeat greenthread.
        """
        if self._heart:
            self._heart.kill()


class DirectBinding(Binding):
    """
    Specifies a host in the key via a '.' character
    Although dots are used in the key, the behavior here is
    that it maps directly to a host, thus direct.
    """

    def test(self, key):
        if '.' in key:
            return True
        return False


class TopicBinding(Binding):
    """
    Where a 'bare' key without dots.
    AMQP generally considers topic exchanges to be those *with* dots,
    but we deviate here in terminology as the behavior here matches
    that of a topic exchange (whereas where there are dots, behavior
    matches that of a direct exchange.
    """

    def test(self, key):
        if '.' not in key:
            return True
        return False


class FanoutBinding(Binding):
    """Match on fanout keys, where key starts with 'fanout.' string."""

    def test(self, key):
        if key.startswith('fanout~'):
            return True
        return False


class StubExchange(Exchange):
    """Exchange that does nothing."""

    def run(self, key):
        return [
         (
          key, None)]


class RingExchange(Exchange):
    """
    Match Maker where hosts are loaded from a static file containing
    a hashmap (JSON formatted).

    __init__ takes optional ring dictionary argument, otherwise
    loads the ringfile from CONF.mathcmaker_ringfile.
    """

    def __init__(self, ring=None):
        super(RingExchange, self).__init__()
        if ring:
            self.ring = ring
        else:
            fh = open(CONF.matchmaker_ringfile, 'r')
            self.ring = json.load(fh)
            fh.close()
        self.ring0 = {}
        for k in self.ring.keys():
            self.ring0[k] = itertools.cycle(self.ring[k])

    def _ring_has(self, key):
        if key in self.ring0:
            return True
        return False


class RoundRobinRingExchange(RingExchange):
    """A Topic Exchange based on a hashmap."""

    def __init__(self, ring=None):
        super(RoundRobinRingExchange, self).__init__(ring)

    def run(self, key):
        if not self._ring_has(key):
            LOG.warn(_("No key defining hosts for topic '%s', see ringfile") % (
             key,))
            return []
        host = next(self.ring0[key])
        return [(key + '.' + host, host)]


class FanoutRingExchange(RingExchange):
    """Fanout Exchange based on a hashmap."""

    def __init__(self, ring=None):
        super(FanoutRingExchange, self).__init__(ring)

    def run(self, key):
        nkey = key.split('fanout~')[1:][0]
        if not self._ring_has(nkey):
            LOG.warn(_("No key defining hosts for topic '%s', see ringfile") % (
             nkey,))
            return []
        return map(lambda x: (key + '.' + x, x), self.ring[nkey])


class LocalhostExchange(Exchange):
    """Exchange where all direct topics are local."""

    def __init__(self, host='localhost'):
        self.host = host
        super(Exchange, self).__init__()

    def run(self, key):
        return [
         (
          ('.').join((key.split('.')[0], self.host)), self.host)]


class DirectExchange(Exchange):
    """
    Exchange where all topic keys are split, sending to second half.
    i.e. "compute.host" sends a message to "compute.host" running on "host"
    """

    def __init__(self):
        super(Exchange, self).__init__()

    def run(self, key):
        e = key.split('.', 1)[1]
        return [(key, e)]


class MatchMakerRing(MatchMakerBase):
    """
    Match Maker where hosts are loaded from a static hashmap.
    """

    def __init__(self, ring=None):
        super(MatchMakerRing, self).__init__()
        self.add_binding(FanoutBinding(), FanoutRingExchange(ring))
        self.add_binding(DirectBinding(), DirectExchange())
        self.add_binding(TopicBinding(), RoundRobinRingExchange(ring))


class MatchMakerLocalhost(MatchMakerBase):
    """
    Match Maker where all bare topics resolve to localhost.
    Useful for testing.
    """

    def __init__(self, host='localhost'):
        super(MatchMakerLocalhost, self).__init__()
        self.add_binding(FanoutBinding(), LocalhostExchange(host))
        self.add_binding(DirectBinding(), DirectExchange())
        self.add_binding(TopicBinding(), LocalhostExchange(host))


class MatchMakerStub(MatchMakerBase):
    """
    Match Maker where topics are untouched.
    Useful for testing, or for AMQP/brokered queues.
    Will not work where knowledge of hosts is known (i.e. zeromq)
    """

    def __init__(self):
        super(MatchMakerLocalhost, self).__init__()
        self.add_binding(FanoutBinding(), StubExchange())
        self.add_binding(DirectBinding(), StubExchange())
        self.add_binding(TopicBinding(), StubExchange())