# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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