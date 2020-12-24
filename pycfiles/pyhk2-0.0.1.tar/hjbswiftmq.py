# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/hjb/scripts/hjbswiftmq.py
# Compiled at: 2006-06-04 06:15:41
__doc__ = '\nDemo showing pyhjb accessing a SwiftMQ JMS provider via a HJB\nserver.\n\n'
from copy import deepcopy
from hjb.hjbclient import HJBClient, SimpleMessagingScenario
from hjb.democli import DemoCommand
__docformat__ = 'restructuredtext en'
queue_aliases = {'Map': 'hjb_sample_MAP@hjbrouter', 'Text': 'hjb_sample_TEXT@hjbrouter', 'Object': 'hjb_sample_OBJECT@hjbrouter', 'Stream': 'hjb_sample_STREAM@hjbrouter', 'Bytes': 'hjb_sample_BYTES@hjbrouter'}
topic_aliases = {'qotd': 'hjb_sample_QOTD', 'logmessage': 'hjb_sample_LOGMESSAGE', 'heartbeat': 'hjb_sample_HEARTBEAT'}
destination_aliases = deepcopy(queue_aliases)
destination_aliases.update(deepcopy(topic_aliases))

def create_scenario():
    provider_config = {'provider': {'java.naming.factory.initial': 'com.swiftmq.jndi.InitialContextFactoryImpl', 'java.naming.provider.url': 'smqp://localhost:4091/timeout=10000'}}
    provider = 'swiftmq'
    root = '/hjb-swiftmq/hjb'
    factory = '/ConnectionFactory'
    host = 'localhost:8015'
    return SimpleMessagingScenario(HJBClient(host, root), provider, factory, destination_aliases.values(), provider_config)


def main():
    command = DemoCommand(create_scenario(), destination_aliases)
    command.execute()


if __name__ == '__main__':
    main()