# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nmcbride/virtualenvs/nmcbride.marketservice/lib/python2.7/site-packages/pyramid-1.0-py2.7.egg/pyramid/paster_templates/zodb/+package+/models.py
# Compiled at: 2011-03-15 14:22:35
from persistent.mapping import PersistentMapping

class MyModel(PersistentMapping):
    __parent__ = __name__ = None


def appmaker(zodb_root):
    if 'app_root' not in zodb_root:
        app_root = MyModel()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']