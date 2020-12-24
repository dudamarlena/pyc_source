# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/hjb/scripts/hjbjboss.py
# Compiled at: 2006-06-04 10:28:13
__doc__ = "\n\nDemo showing pyhjb accessing a 'JBoss Messaging' JMS provider via a\nHJB server.\n\nN.B. JBoss Messaging is not the same as JBoss MQ.  The demo should\nwork just the same, but as of 2006/06/01, it has been tested on JBoss\nMessaging, but not on JBoss MQ.\n\n"
from copy import deepcopy
from hjb.hjbclient import HJBClient, SimpleMessagingScenario
from hjb.democli import DemoCommand
__docformat__ = 'restructuredtext en'
queue_aliases = {'Map': '/queue/hjb.sample.MAP', 'Text': '/queue/hjb.sample.TEXT', 'Object': '/queue/hjb.sample.OBJECT', 'Stream': '/queue/hjb.sample.STREAM', 'Bytes': '/queue/hjb.sample.BYTES'}
topic_aliases = {'qotd': '/topic/hjb.sample.QOTD', 'logmessage': '/topic/hjb.sample.LOGMESSAGE', 'heartbeat': '/topic/hjb.sample.HEARTBEAT'}
destination_aliases = deepcopy(queue_aliases)
destination_aliases.update(deepcopy(topic_aliases))

def create_scenario():
    provider_config = {'provider': {'java.naming.factory.initial': 'org.jnp.interfaces.NamingContextFactory', 'java.naming.provider.url': 'jnp://localhost:1099', 'java.naming.factory.url.pkgs': 'org.jboss.naming:org.jnp.interfaces'}}
    provider = 'jboss'
    root = '/hjb-jboss/hjb'
    factory = '/ConnectionFactory'
    host = 'localhost:8015'
    return SimpleMessagingScenario(HJBClient(host, root), provider, factory, destination_aliases.values(), provider_config)


def main():
    command = DemoCommand(create_scenario(), destination_aliases)
    command.execute()


if __name__ == '__main__':
    main()