# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/__ui__.py
# Compiled at: 2016-04-13 20:07:13
__all__ = [
 'ui']

class ui(object):

    def __init__(self, route, guid):
        self.route = route
        self.guid = guid
        self.set_guid(route, guid)

    @staticmethod
    def set_guid(obj, guid):
        setattr(obj, 'ui.guid', guid)

    @staticmethod
    def get_guid(obj):
        if not hasattr(obj, 'ui.guid'):
            return None
        else:
            return getattr(obj, 'ui.guid')