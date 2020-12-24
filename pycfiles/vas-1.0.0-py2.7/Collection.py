# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/Collection.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Deletable import Deletable
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class Collection(Resource):
    """A dynamic collection of items

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """
    __items = None

    def __init__(self, client, location, type, entry_class):
        self.__type = type
        self.__entry_class = entry_class
        super(Collection, self).__init__(client, location)

    def reload(self):
        """Reloads the resource's details from the server"""
        super(Collection, self).reload()
        self.__items = None
        return

    def __iter__(self):
        self.__items = self.__items or self.__create_collection_entries()
        return iter(self.__items)

    def _create_entry(self, location):
        entry = self.__entry_class(self._client, location)
        if isinstance(entry, Deletable):
            entry._collection = self
        return entry

    def __create_collection_entries(self):
        entries_json = self._details[self.__type]
        if entries_json:
            return [ self._create_entry(LinkUtils.get_self_link_href(json)) for json in entries_json ]
        else:
            return []