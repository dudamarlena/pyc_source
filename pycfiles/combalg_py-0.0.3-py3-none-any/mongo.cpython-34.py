# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/breezekay/Dropbox/Codes/nextoa/comb/comb/mq/mongo.py
# Compiled at: 2014-10-21 10:41:15
# Size of source mod 2**32: 480 bytes


def token(collection, token='token'):
    return collection.find_and_modify({token: {'$exists': False}}, {'$set': {'token': True}})


def release(collection, token='token'):
    return collection.update({token: True}, {'$set': {token: False}}, multi=True)


def garbage(collection, token='token'):
    """
    garbage for mongo message queue
    :param collection:
    :param token:
    :return:
    """
    collection.remove({token: False}, multi=True)