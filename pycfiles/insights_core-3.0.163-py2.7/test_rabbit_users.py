# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rabbit_users.py
# Compiled at: 2019-05-16 13:41:33
from insights.core.context import OSP
from insights.parsers.rabbitmq import RabbitMQUsers
from insights.tests import context_wrap
osp_controller = OSP()
osp_controller.role = 'Controller'
RABBITMQ_LIST_USERS = '\nListing users ...\nguest   [administrator]\ntest    [administrator]\n...done.\n'
RABBITMQ_LIST_EDGES = '\nListing users ...\nprobe   []\nbrain   []\nnone\nuser1   [monitoring,user]\nguest   [made up data]\n...done.\n'

def test_rabbitmq_list_users():
    context = context_wrap(RABBITMQ_LIST_USERS, hostname='controller_1', osp=osp_controller)
    result = RabbitMQUsers(context)
    expect = {'guest': 'administrator', 'test': 'administrator'}
    assert result.data == expect


def test_rabbitmq_list_users_stub():
    context = context_wrap(RABBITMQ_LIST_EDGES, hostname='controller_1', osp=osp_controller)
    result = RabbitMQUsers(context)
    assert result.data['probe'] == ''
    assert 'none' not in result.data
    assert result.data['user1'] == 'monitoring,user'
    assert result.data['guest'] == 'made up data'