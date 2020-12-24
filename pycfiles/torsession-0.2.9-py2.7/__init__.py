# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/torsession/__init__.py
# Compiled at: 2016-08-27 22:50:28
"""An async && sync session backend with mongodb for tornado"""
import uuid
from datetime import datetime, timedelta
VERSION = (0, 2, 9)

def get_version():
    return ('.').join(map(str, VERSION))


__version__ = get_version()

def gen_session_id():
    return str(uuid.uuid1())


class SessionBase(object):

    def __init__(self, collection, id_, expired_time, **data):
        self.collection = collection
        self.id = id_
        self.expired_time = expired_time
        self.data = data

    def expired(self):
        return self.expired_time < datetime.now()


class SessionManagerBase(object):
    EXPIRED_AFTER = timedelta(days=3)

    def __init__(self, collection, expired_after=None):
        self.collection = collection
        self.expired_after = expired_after or self.EXPIRED_AFTER