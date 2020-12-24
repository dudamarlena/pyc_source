# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rabbitmq_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.rabbitmq_log import RabbitMQStartupLog
from insights.parsers.rabbitmq_log import RabbitMQStartupErrLog
from insights.parsers.rabbitmq_log import RabbitMQLogs
from insights.tests import context_wrap
from datetime import datetime
STARTUP_LOG = '\nstarting file handle cache server                                     ...done\nstarting worker pool                                                  ...done\nstarting database                                                     ...done\nstarting empty DB check                                               ...done\nstarting exchange recovery                                            ...done\nstarting queue supervisor and queue recovery                          ...BOOT ERROR: FAILED\n'
STARTUP_ERR_LOG = '\nError: {node_start_failed,normal}\n\nCrash dump was written to: erl_crash.dump\nKernel pid terminated (application_controller) ({application_start_failure,kernel,{shutdown,{kernel,start,[normal,[]]}}})\n'

def test_rabbitmq_startup_log():
    log = RabbitMQStartupLog(context_wrap(STARTUP_LOG))
    assert len(log.get('done')) == 5


def test_rabbitmq_start_err_log():
    log = RabbitMQStartupErrLog(context_wrap(STARTUP_ERR_LOG))
    assert len(log.get('Error')) == 1


RABBIT_MQ_LOG = ('\n=INFO REPORT==== 7-Jun-2015::03:42:13 ===\naccepting AMQP connection <0.13548.17> (192.168.100.40:59815 -> 192.168.100.41:5672)\n\n=ERROR REPORT==== 7-Jun-2015::03:42:28 ===\nAMQP connection <0.13548.17> (running), channel 19793 - error:\n{amqp_error,frame_error,\n            "type 65, all octets = <<>>: {frame_too_large,1342177289,131064}",\n            none}\n\n=ERROR REPORT==== 7-Jun-2015::03:42:31 ===\nclosing AMQP connection <0.13548.17> (192.168.100.40:59815 -> 192.168.100.41:5672):\nfatal_frame_error\n').strip()

def test_rabbitmq_log():
    log = RabbitMQLogs(context_wrap(RABBIT_MQ_LOG, path='/var/log/rabbitmq/rabbit@queue.example.com.log'))
    assert len(log.get('AMQP')) == 3
    assert len(list(log.get_after(datetime(2015, 6, 7, 3, 42, 20)))) == 9