# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/lib/glam/glrule.py
# Compiled at: 2011-07-08 01:47:53
""" Representing a rule of ACL
"""
import re, urllib
REGEXP_SET = {'valid_permission': '-|R|RW\\+?C?D?'}

class GLRule:
    """ Representing a rule of ACL """

    def __init__(self, perm, refex_list, member_list):
        self.perm = perm
        self.refex_list = refex_list
        self.member_list = member_list
        self.deleted = False

    def check_parameters(self):
        """ Checks if parameters are valid """
        if not isinstance(self.perm, (str, unicode)):
            raise TypeError('Parameters type invalid.')
        for member in self.member_list:
            if not isinstance(member, (str, unicode)):
                raise TypeError('Parameters type invalid.')

        for refex in self.refex_list:
            if not isinstance(refex, (str, unicode)):
                raise TypeError('Parameters type invalid.')
            try:
                re.compile(refex)
            except:
                raise ValueError('Refex %s can not pass compilation.')

    def get_id(self):
        return (',').join(sorted(map(urllib.quote, self.refex_list))) + ';' + (',').join(sorted(self.member_list))

    @staticmethod
    def parse_id(rule_id):
        """  """
        refex_list = map(urllib.unquote, rule_id[0:rule_id.rfind(';')].split(','))
        member_list = rule_id[rule_id.rfind(';') + 1:].split(',')
        return (refex_list, member_list)

    def delete(self):
        """ Delete an existing rule """
        self.deleted = True
        return True

    def dumps(self):
        """ Dumps to string for writing file """
        if self.deleted:
            return ''
        else:
            return '    %s %s = %s\n' % (self.perm,
             (' ').join(self.refex_list),
             (' ').join(self.member_list))

    def to_dict(self):
        """ Using a dict to present it """
        return dict(permission=self.perm, refex_list=self.refex_list, member_list=self.member_list)

    @staticmethod
    def check_permission(perm):
        """ match the regular expression given """
        if not isinstance(perm, (str, unicode)):
            raise TypeError('Parameters type invalid.')
        if re.match(REGEXP_SET['valid_permission'], perm) != None:
            raise ValueError('Permission is not valid.')
        return