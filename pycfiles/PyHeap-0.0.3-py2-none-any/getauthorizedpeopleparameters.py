# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/getauthorizedpeopleparameters.py
# Compiled at: 2015-12-19 03:58:41
from lxml import etree

class GetAuthorizedPeopleParameters:

    def __init__(self):
        self.person_id_cursor = None
        self.authorizations_created_since = None
        self.num_results = None
        return

    def get_info(self):
        parameters = etree.Element('parameters')
        if self.person_id_cursor is not None:
            cursor = etree.Element('person-id-cursor')
            cursor.text = self.person_id_cursor
            parameters.append(cursor)
        if self.authorizations_created_since is not None:
            since = etree.Element('authorizations-created-since')
            since.text = self.authorizations_created_since.isoformat()
            parameters.append(since)
        if self.num_results is not None:
            num_results = etree.Element('num-results')
            num_results.text = str(self.num_results)
            parameters.append(num_results)
        return parameters