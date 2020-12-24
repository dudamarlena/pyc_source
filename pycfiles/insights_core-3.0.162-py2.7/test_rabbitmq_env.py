# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rabbitmq_env.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from .test_rabbitmq_queues import QUEUES
from insights.parsers import rabbitmq
from insights.tests import context_wrap
RABBITMQ_ENV = ('\nRABBITMQ_SERVER_ERL_ARGS="+K true +P 1048576 -kernel inet_default_connect_options [{nodelay,true},{raw,6,18,<<5000:64/native>>}] -kernel inet_default_listen_options [{raw,6,18,<<5000:64/native>>}]"\n').strip()
RABBITMQ_ENV_DIFFERENT_TIMEOUT = ('\nRABBITMQ_SERVER_ERL_ARGS="+K true +P 1048576 -kernel inet_default_connect_options [{nodelay,true},{raw,6,18,<<5000:64/native>>}] -kernel inet_default_listen_options [{raw,6,18,<<3000:64/native>>}]"\n').strip()
RABBITMQ_ENV_OPTIONS = ('\nOPTIONS="+K true +P 1048576 -kernel inet_default_connect_options [{nodelay,true},{raw,6,18,<<5000:64/native>>}] -kernel inet_default_listen_options [{raw,6,18,<<5000:64/native>>}]"\n').strip()
RABBITMQ_ENV_BAD_PATTERN = ('\nRABBITMQ_SERVER_ERL_ARGS="+K true +P 1048576 -kernel inet_default_connect_options [{nodelay,true},{raw,6,18,<<5000:64/native>>}] -kernel inet_default_options [{raw,6,18,<<5000:64/native>>}]"\n').strip()

def test_rabbitmq_env():
    rabbitmq_env = rabbitmq.RabbitMQEnv(context_wrap(RABBITMQ_ENV))
    assert rabbitmq_env.rabbitmq_server_erl_args == '+K true +P 1048576 -kernel inet_default_connect_options [{nodelay,true},{raw,6,18,<<5000:64/native>>}] -kernel inet_default_listen_options [{raw,6,18,<<5000:64/native>>}]'
    assert rabbitmq_env.data['RABBITMQ_SERVER_ERL_ARGS'] == '+K true +P 1048576 -kernel inet_default_connect_options [{nodelay,true},{raw,6,18,<<5000:64/native>>}] -kernel inet_default_listen_options [{raw,6,18,<<5000:64/native>>}]'
    assert rabbitmq_env.rmq_erl_tcp_timeout == '5000'
    rabbitmq_env = rabbitmq.RabbitMQEnv(context_wrap(RABBITMQ_ENV_DIFFERENT_TIMEOUT))
    assert rabbitmq_env.rmq_erl_tcp_timeout is None
    rabbitmq_env = rabbitmq.RabbitMQEnv(context_wrap(RABBITMQ_ENV_OPTIONS))
    assert rabbitmq_env.rabbitmq_server_erl_args is None
    assert rabbitmq_env.rmq_erl_tcp_timeout is None
    rabbitmq_env = rabbitmq.RabbitMQEnv(context_wrap(RABBITMQ_ENV_BAD_PATTERN))
    assert rabbitmq_env.rmq_erl_tcp_timeout is None
    return


def test_doc_examples():
    failed, total = doctest.testmod(rabbitmq, globs={'rabbitmq_env': rabbitmq.RabbitMQEnv(context_wrap(RABBITMQ_ENV)), 'queues': rabbitmq.RabbitMQQueues(context_wrap(QUEUES))})
    assert failed == 0