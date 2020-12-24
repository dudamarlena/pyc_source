# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/bigdoorkit/resources/good.py
# Compiled at: 2010-07-29 15:08:39
from bigdoorkit.resources.base import BDResource
from bigdoorkit.resources.user import EndUser

class NamedGoodCollection(BDResource):
    endpoint = 'named_good_collection'


class NamedGood(BDResource):
    endpoint = 'named_good'
    parent_class = NamedGoodCollection
    parent_id_attr = 'named_good_collection_id'

    def __init__(self, **kw):
        self.named_good_collection_id = kw.get('named_good_collection_id', None)
        self.relative_weight = kw.get('relative_weight', None)
        self.collection_resource_uri = kw.get('collection_resource_uri', None)
        super(NamedGood, self).__init__(**kw)
        return


class Good(BDResource):
    endpoint = 'good'
    parent_class = EndUser
    parent_id_attr = 'reciever_end_user_login'

    def __init__(self, **kw):
        self.sender_end_user_login = kw.get('sender_end_user_login', None)
        self.reciever_end_user_login = kw.get('reciever_end_user_login', None)
        self.named_good_id = kw.get('named_good_id', None)
        self.end_user_message_subject = kw.get('end_user_message_subject', None)
        self.end_user_message_body = kw.get('end_user_message_body', None)
        super(Good, self).__init__(**kw)
        return