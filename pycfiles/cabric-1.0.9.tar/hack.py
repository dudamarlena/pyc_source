# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/hack.py
# Compiled at: 2017-11-03 00:25:19
import os
from fabric.context_managers import env
from fabric.decorators import task
from cabric.utils import parse_hosts

@task
def ez(curr, current_path='./config/fabric'):
    """

    :param curr: which env to use
    :param current_path: set load path

      ..note::
        if you use `ol` as value, cabric will translate `online`

    :return:
    """
    curr = 'online' if curr == 'ol' else curr
    env_file = os.path.join(current_path, curr + '.conf')
    env.use_ssh_config = True
    env.hosts, env_host_names = parse_hosts(env_file)