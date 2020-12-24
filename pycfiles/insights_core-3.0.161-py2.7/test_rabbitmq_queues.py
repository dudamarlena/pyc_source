# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rabbitmq_queues.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers import ParseException
from insights.parsers.rabbitmq import RabbitMQQueues
from insights.tests import context_wrap
QUEUES = '\ncinder-scheduler        0       3       false\ncinder-scheduler.ha-controller  0       3       false\ncinder-scheduler_fanout_ea9c69fb630f41b2ae6120eba3cd43e0        8141    1   true\ncinder-scheduler_fanout_9aed9fbc3d4249289f2cb5ea04c062ab        8145    0   true\ncinder-scheduler_fanout_b7a2e488f3ed4e1587b959f9ac255b93        8141    0   true\n'
MORE_QUEUES = '\nListing queues ...\nq-agent-notifier-tunnel-delete_fanout_a8dc17bbb6ee469c8aaab31079c01c1c\t0\t1\tfalse\ndhcp_agent.undercloud-per720xd.default.redhat.local\t0\t1\tfalse\nmistral_executor.0.0.0.0\t0\t1\tfalse\nreply_aeff2b095dac4b09b8a4ea27986b402c\t0\t1\tfalse\nreply_6cf2931b774f4a58a14c819570059114\t0\t1\tfalse\nq-agent-notifier-tunnel-update\t0\t1\tfalse\ncert\t0\t1\tfalse\nq-plugin.undercloud-per720xd.default.redhat.local\t0\t2\tfalse\nreply_5d74d09f9758439fbd247097c096c1a2\t0\t1\tfalse\nmetering.sample\t1\t1\tfalse\nheat-engine-listener.65218f91-59b6-45bc-99df-63f5af707351\t0\t1\tfalse\nreply_e7fb8381d78b4dcf9501ba8a72ad335f\t0\t1\tfalse\nreply_e366ce8a5b3846608e1e181e9e413231\t0\t1\tfalse\nreply_19ec1f054dc74298b896cbbb06c7b7e7\t0\t1\tfalse\nscheduler.undercloud-per720xd.default.redhat.local\t0\t1\tfalse\nq-server-resource-versions_fanout_56cc075fd8cc486bacd0648225b61970\t0\t1\tfalse\nq-server-resource-versions.undercloud-per720xd.default.redhat.local\t0\t2\tfalse\nmistral_engine.0.0.0.0\t0\t1\tfalse\nreply_c97293591c5c46be9331f0a5662f8961\t0\t1\tfalse\nmistral_engine_fanout_a660b93980ca41ac84b6f1b56cf8a25c\t0\t1\tfalse\nevent.sample\t0\t1\tfalse\n...done.\n'
QUEUES_BAD_1 = '\nError: unable to connect to node\n'
QUEUES_BAD_2 = '\nqueue1 1 x false\n'
QUEUES_BAD_3 = '\nqueue1 1 1 maybe\n'

def test_rabbitmq_queues():
    queues = RabbitMQQueues(context_wrap(QUEUES))
    assert queues is not None
    assert len(queues.data) == 5
    assert queues.data[0] == RabbitMQQueues.QueueInfo(name='cinder-scheduler', messages=0, consumers=3, auto_delete=False)
    assert queues.data[3] == RabbitMQQueues.QueueInfo(name='cinder-scheduler_fanout_9aed9fbc3d4249289f2cb5ea04c062ab', messages=8145, consumers=0, auto_delete=True)
    assert queues.data[3].name == 'cinder-scheduler_fanout_9aed9fbc3d4249289f2cb5ea04c062ab'
    many_queues = RabbitMQQueues(context_wrap(MORE_QUEUES))
    assert many_queues.data[1].name == 'dhcp_agent.undercloud-per720xd.default.redhat.local'
    assert many_queues.data[1].auto_delete is False
    with pytest.raises(ParseException):
        queues = RabbitMQQueues(context_wrap(QUEUES_BAD_1))
    with pytest.raises(ValueError):
        queues = RabbitMQQueues(context_wrap(QUEUES_BAD_2))
    with pytest.raises(ParseException):
        queues = RabbitMQQueues(context_wrap(QUEUES_BAD_3))
    return