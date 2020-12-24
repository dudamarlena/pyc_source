# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/seafileapi/group.py
# Compiled at: 2014-11-09 11:12:37


class Group(object):

    def __init__(self, client, group_id, group_name):
        self.client = client
        self.group_id = group_id
        self.group_name = group_name

    def list_memebers(self):
        pass

    def delete(self):
        pass

    def add_member(self, username):
        pass

    def remove_member(self, username):
        pass

    def list_group_repos(self):
        pass