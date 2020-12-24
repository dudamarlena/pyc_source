# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skywisemodel/_subscription.py
# Compiled at: 2017-05-19 14:29:52
from voluptuous import Any, Schema
from . import ModelApiResource
_subscription_deserialize = Schema({'id': Any(None, str, unicode), 
   'model_id': Any(str, unicode), 
   'event': Any(str, unicode), 
   'subscriber_email': Any(str, unicode), 
   'options': dict})
_subscription_serialize = Schema({'id': Any(None, str, unicode), 
   'model_id': Any(str, unicode), 
   'event': Any(str, unicode), 
   'subscriber_email': Any(str, unicode), 
   'options': dict})

class Subscription(ModelApiResource):
    _path = '/models/{model_id}/subscriptions'
    _deserialize = _subscription_deserialize
    _serialize = _subscription_serialize
    _args = Schema({'event': Any(str, unicode), 
       'subscriber_email': Any(str, unicode)})

    @classmethod
    def find(cls, id_=None, **kwargs):
        if id_ is not None:
            return _SubscriptionById.find(id_)
        else:
            return super(Subscription, cls).find(**kwargs)


class _SubscriptionById(ModelApiResource):
    _path = '/subscriptions'
    _deserialize = _subscription_deserialize
    _serialize = _subscription_serialize