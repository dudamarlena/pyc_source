# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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