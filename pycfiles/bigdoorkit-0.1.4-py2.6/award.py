# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/bigdoorkit/resources/award.py
# Compiled at: 2010-07-29 15:08:39
from bigdoorkit.resources.base import BDResource
from bigdoorkit.resources.user import EndUser

class NamedAwardCollection(BDResource):
    endpoint = 'named_award_collection'


class NamedAward(BDResource):
    endpoint = 'named_award'
    parent_class = NamedAwardCollection
    parent_id_attr = 'named_award_collection_id'

    def __init__(self, **kw):
        self.named_award_collection_id = kw.get('named_award_collection_id', None)
        self.relative_weight = kw.get('relative_weight', None)
        self.collection_resource_uri = kw.get('collection_resource_uri', None)
        super(NamedAward, self).__init__(**kw)
        return


class Award(BDResource):
    endpoint = 'award'
    parent_class = EndUser
    parent_id_attr = 'end_user_login'

    def __init__(self, **kw):
        self.end_user_login = kw.get('end_user_login', None)
        self.named_award_id = kw.get('named_award_id', None)
        super(Award, self).__init__(**kw)
        return