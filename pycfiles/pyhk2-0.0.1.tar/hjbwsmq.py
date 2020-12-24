# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/hjb/scripts/hjbwsmq.py
# Compiled at: 2006-06-04 03:45:03
__doc__ = '\nDemo showing pyhjb accessing a WebSphere MQ messaging provider via a HJB\nserver.\n\n'
from copy import deepcopy
from hjb.hjbclient import HJBClient, SimpleMessagingScenario
from hjb.democli import DemoCommand
__docformat__ = 'restructuredtext en'
queue_aliases = {'Map': 'HJB\\SAMPLE\\MAP', 'Text': 'HJB\\SAMPLE\\TEXT', 'Object': 'HJB\\SAMPLE\\OBJECT', 'Stream': 'HJB\\SAMPLE\\STREAM', 'Bytes': 'HJB\\SAMPLE\\BYTES'}
topic_aliases = {'qotd': 'HJB\\SAMPLE\\QOTD', 'logmessage': 'HJB\\SAMPLE\\LOGMESSAGE', 'heartbeat': 'HJB\\SAMPLE\\HEARTBEAT'}
destination_aliases = deepcopy(queue_aliases)
destination_aliases.update(deepcopy(topic_aliases))

def create_scenario():
    provider_config = {'provider': {'java.naming.factory.initial': 'com.sun.jndi.fscontext.RefFSContextFactory', 'java.naming.provider.url': 'file:/C:/tim_root/var/wsmq/jndi'}}
    provider = 'wsmq'
    root = '/hjb-wsmq/hjb'
    factory = 'HJB\\SAMPLE\\ConnectionFactory'
    host = 'localhost:8015'
    return SimpleMessagingScenario(HJBClient(host, root), provider, factory, destination_aliases.values(), provider_config)


def main():
    command = DemoCommand(create_scenario(), destination_aliases)
    command.execute()


if __name__ == '__main__':
    main()