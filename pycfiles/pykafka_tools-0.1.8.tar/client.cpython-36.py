# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/client.py
# Compiled at: 2018-08-15 18:16:00
# Size of source mod 2**32: 7718 bytes
__doc__ = '\nAuthor: Keith Bourgoin, Emmett Butler\n'
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = [
 'KafkaClient']
import logging
from .cluster import Cluster
from .handlers import ThreadingHandler
try:
    from .handlers import GEventHandler
except ImportError:
    GEventHandler = None

log = logging.getLogger(__name__)

class KafkaClient(object):
    """KafkaClient"""

    def __init__(self, hosts='127.0.0.1:9092', zookeeper_hosts=None, socket_timeout_ms=30000, offsets_channel_socket_timeout_ms=10000, use_greenlets=False, exclude_internal_topics=True, source_address='', ssl_config=None, broker_version='0.9.0'):
        """Create a connection to a Kafka cluster.

        Documentation for source_address can be found at
        https://docs.python.org/2/library/socket.html#socket.create_connection

        :param hosts: Comma-separated list of kafka hosts to which to connect.
            If `ssl_config` is specified, the ports specified here are assumed
            to be SSL ports
        :type hosts: str
        :param zookeeper_hosts: KazooClient-formatted string of ZooKeeper hosts to which
            to connect. If not `None`, this argument takes precedence over `hosts`
        :type zookeeper_hosts: str
        :param socket_timeout_ms: The socket timeout (in milliseconds) for
            network requests
        :type socket_timeout_ms: int
        :param offsets_channel_socket_timeout_ms: The socket timeout (in
            milliseconds) when reading responses for offset commit and
            offset fetch requests.
        :type offsets_channel_socket_timeout_ms: int
        :param use_greenlets: Whether to perform parallel operations on greenlets
            instead of OS threads
        :type use_greenlets: bool
        :param exclude_internal_topics: Whether messages from internal topics
            (specifically, the offsets topic) should be exposed to the consumer.
        :type exclude_internal_topics: bool
        :param source_address: The source address for socket connections
        :type source_address: str `'host:port'`
        :param ssl_config: Config object for SSL connection
        :type ssl_config: :class:`pykafka.connection.SslConfig`
        :param broker_version: The protocol version of the cluster being connected to.
            If this parameter doesn't match the actual broker version, some pykafka
            features may not work properly.
        :type broker_version: str
        """
        self._seed_hosts = zookeeper_hosts if zookeeper_hosts is not None else hosts
        self._source_address = source_address
        self._socket_timeout_ms = socket_timeout_ms
        self._offsets_channel_socket_timeout_ms = offsets_channel_socket_timeout_ms
        if use_greenlets:
            if not GEventHandler:
                raise ImportError('use_greenlets can only be used when gevent is installed.')
        self._handler = GEventHandler() if use_greenlets else ThreadingHandler()
        self.cluster = Cluster(hosts,
          (self._handler),
          socket_timeout_ms=(self._socket_timeout_ms),
          offsets_channel_socket_timeout_ms=(self._offsets_channel_socket_timeout_ms),
          exclude_internal_topics=exclude_internal_topics,
          source_address=(self._source_address),
          zookeeper_hosts=zookeeper_hosts,
          ssl_config=ssl_config,
          broker_version=broker_version)
        self.brokers = self.cluster.brokers
        self.topics = self.cluster.topics

    def __repr__(self):
        return '<{module}.{name} at {id_} (hosts={hosts})>'.format(module=(self.__class__.__module__),
          name=(self.__class__.__name__),
          id_=(hex(id(self))),
          hosts=(self._seed_hosts))

    def update_cluster(self):
        """Update known brokers and topics.

        Updates each Topic and Broker, adding new ones as found,
        with current metadata from the cluster.
        """
        self.cluster.update()