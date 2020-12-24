# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/checks/abstract_check.py
# Compiled at: 2018-09-04 03:34:18
# Size of source mod 2**32: 2294 bytes
import json
from six import iteritems

class AbstractCheck(object):
    name = None
    check_type = None

    def __init__(self, message, description, reference_url, tags):
        self.message = message
        self.description = description
        self.reference_url = reference_url
        self.tags = tags

    def check(self, target):
        pass

    def __str__(self):
        return '{}\n   -> {}\n   -> {}\n   -> {}\n   -> {}\n'.format(self.name, self.message, self.description, self.reference_url, ', '.join(self.tags))

    @property
    def json(self):
        """
        Get json representation of the check

        :return: dict (str -> obj)
        """
        return {'name':self.name, 
         'message':self.message, 
         'description':self.description, 
         'reference_url':self.reference_url, 
         'tags':self.tags}

    @staticmethod
    def json_from_all_checks(checks):
        result_json = {}
        for group, group_checks in iteritems(checks):
            result_list = []
            for check in group_checks:
                result_list.append(check.json)

            result_json[group] = result_list

        return result_json

    @staticmethod
    def save_checks_to_json(file, checks):
        json.dump(obj=AbstractCheck.json_from_all_checks(checks=checks), fp=file,
          indent=4)