# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/play_groups.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import re

def play_groups(play_hosts, groups, hostvars):
    _list = []
    for host in play_hosts:
        for group in groups:
            if host in groups[group]:
                _list.append(group)

    return list(set(_list))


class FilterModule(object):
    """ Returns a list of play groups that are active within a play """

    def filters(self):
        return {'play_groups': play_groups}