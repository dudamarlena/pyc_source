# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/client.py
# Compiled at: 2018-08-15 18:16:00
# Size of source mod 2**32: 7718 bytes
"""
Author: Keith Bourgoin, Emmett Butler
"""
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
    __doc__ = "\n    A high-level pythonic client for Kafka\n\n    NOTE: `KafkaClient` holds weak references to `Topic` instances via\n    :class:`pykafka.cluster.TopicDict`. To perform operations directly on these topics,\n    such as examining their partition lists, client code must hold a strong reference to\n    the topics it cares about. If client code doesn't need to examine `Topic` instances\n    directly, no strong references are necessary.\n\n    Notes on Zookeeper: Zookeeper is used by kafka and its clients to store several\n    types of information, including broker host strings, partition ownerships, and\n    depending on your kafka version, consumer offsets. The kafka-console-* tools rely\n    on zookeeper to discover brokers - this is why you can't directly specify a broker\n    to these tools and are required to give a zookeeper host string. In theory, this\n    insulates you as a user of the console tools from having to care about which\n    specific brokers in your kafka cluster might be accessible at any given time.\n\n    In pykafka, the paradigm is slightly different, though the above method is also\n    supported. When you instantiate a `KafkaClient`, you can specify either `hosts` or\n    `zookeeper_hosts`. `hosts` is a comma-separated list of brokers to which to\n    connect, and `zookeeper_hosts` is a zookeeper connection string. If you specify\n    `zookeeper_hosts`, it overrides `hosts`. Thus you can create a `KafkaClient`\n    that is connected to your kafka cluster by providing either a zookeeper or a\n    broker connection string.\n\n    As for why the specific components do and don't require knowledge of the zookeeper\n    cluster, there are some different reasons. `SimpleConsumer`, since it does not\n    perform consumption balancing, does not actually require access to zookeeper at\n    all. Since kafka 0.8.2, consumer offset information is stored by the kafka broker\n    itself instead of the zookeeper cluster. The `BalancedConsumer`, by contrast,\n    requires explicit knowledge of the zookeeper cluster because it performs\n    consumption balancing. Zookeeper stores the information about which consumers own\n    which partitions and provides a central repository of that information for all\n    consumers to read. The `BalancedConsumer` cannot do what it does without direct\n    access to zookeeper for this reason. Note that the `ManagedBalancedConsumer`,\n    which works with kafka 0.9 and above, removes this dependency on zookeeper from\n    the balanced consumption process by storing partition ownership information in\n    the kafka broker.\n\n    The `Producer` is allowed to send messages to whatever partitions it wants. In\n    pykafka, by default the partition for each message is chosen randomly to provide\n    an even distribution of messages across partitions. The producer actually doesn't\n    do anything that requires information stored in zookeeper, and since the\n    connection to the kafka cluster is handled by the above-mentioned logic in\n    `KafkaClient`, it doesn't need the zookeeper host string at all.\n    "

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