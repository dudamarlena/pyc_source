# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/hjb/scripts/hjbactivemq.py
# Compiled at: 2006-06-04 06:09:07
__doc__ = '\nDemo showing pyhjb accessing an Active  MQ messaging provider via a HJB\nserver.\n\n'
from copy import deepcopy
from hjb.hjbclient import HJBClient, SimpleMessagingScenario
from hjb.democli import DemoCommand
__docformat__ = 'restructuredtext en'
queue_aliases = {'test': 'text', 'Map': 'HJB.SAMPLE.MAP', 'Text': 'HJB.SAMPLE.TEXT', 'Object': 'HJB.SAMPLE.OBJECT', 'Stream': 'HJB.SAMPLE.STREAM', 'Bytes': 'HJB.SAMPLE.BYTES'}
topic_aliases = {'qotd': 'HJB/SAMPLE/QOTD', 'logmessage': 'HJB\\SAMPLE\\LOGMESSAGE', 'heartbeat': 'HJB.SAMPLE.HEARTBEAT'}
destination_aliases = deepcopy(queue_aliases)
destination_aliases.update(deepcopy(topic_aliases))

def create_scenario():
    provider_config = {'provider': {'java.naming.factory.initial': 'org.apache.activemq.jndi.ActiveMQInitialContextFactory', 'java.naming.provider.url': 'tcp://localhost:61616', 'connectionFactoryNames': 'connectionFactory,queueConnectionFactory,topicConnectionFactory'}}
    config_queue_aliases = dict((('queue.' + v, v) for (k, v) in queue_aliases.iteritems()))
    provider_config['provider'].update(config_queue_aliases)
    config_topic_aliases = dict((('topic.' + v, v) for (k, v) in topic_aliases.iteritems()))
    provider_config['provider'].update(config_topic_aliases)
    provider = 'activemq'
    root = '/hjb-activemq/hjb'
    factory = 'connectionFactory'
    host = 'localhost:8015'
    return SimpleMessagingScenario(HJBClient(host, root), provider, factory, destination_aliases.values(), provider_config)


def main():
    command = DemoCommand(create_scenario(), destination_aliases)
    command.execute()


if __name__ == '__main__':
    main()