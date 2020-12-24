# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/lib/glam/glgroup.py
# Compiled at: 2011-07-08 01:47:53
""" Representing a group
"""
import re

class GLGroup:
    """ Representing a group """

    def __init__(self, name, member_list):
        """
        name: the group name('@' prefix)
        member_list: a list of the member_list
        """
        self.name = name
        self.member_list = member_list
        self.expanded_member_list = []
        self.deleted = False
        self.check_parameters()

    def check_parameters(self):
        """ Checks if parameters are valid """
        if not (isinstance(self.name, (str, unicode)) and isinstance(self.member_list, list)):
            raise TypeError('Parameters type invalid.')
        if not self.name.startswith('@'):
            raise ValueError('Group name should starts with "@".')

    def get_id(self):
        """ ID """
        return '@' + self.name[self.name.find('_') + 1:]

    @staticmethod
    def parse_id(group_id):
        """ Returns repo name and group name"""
        return (
         group_id[1:group_id.find('_')], '@' + group_id[group_id.find('_') + 1:])

    @staticmethod
    def expand(member_list, group_list):
        """ Expands a list of members """
        result = []
        for member in member_list:
            if not member.startswith('@') and member not in result:
                result.append(member)
            else:
                for group in group_list:
                    if group.name == member:
                        group_list.remove(group)
                        tmp = GLGroup.expand(group.member_list, group_list)
                        for item in tmp:
                            if item not in result:
                                result.append(item)

                        break

        return result

    def dumps(self):
        """ Returns a string representing the group """
        if not self.deleted:
            return '%s = %s\n' % (self.name, (' ').join(self.member_list))
        else:
            return ''

    def delete(self):
        """ Delete this group """
        self.deleted = True
        return True

    def join(self, element):
        """ element is a group or user """
        assert isinstance(element, (str, unicode))
        assert re.match('@?\\w+', element) != None
        if element not in self.member_list:
            self.member_list.append(element)
        return

    def leave(self, element):
        """ element is a group or user """
        assert isinstance(element, (str, unicode))
        assert re.match('@?\\w+', element) != None
        if element in self.member_list:
            self.member_list.remove(element)
        return

    def to_dict(self):
        """ Convert to dict """
        return dict(name=self.name, member_list=self.member_list)