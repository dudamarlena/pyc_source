# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/interop/oldimporter/db.py
# Compiled at: 2014-05-07 09:54:09
"""
Django database routers are described here:
https://docs.djangoproject.com/en/dev/topics/db/multi-db/#using-routers
"""

class DefaultRouter(object):

    def db_for_read(self, model, **hints):
        """
        Reads from nodeshot2 db
        """
        if model._meta.app_label != 'oldimporter':
            return 'default'
        else:
            return

    def db_for_write(self, model, **hints):
        """
        Writes to nodeshot2 db
        """
        if model._meta.app_label != 'oldimporter':
            return 'default'
        else:
            return

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed between nodeshot2 objects only
        """
        if obj1._meta.app_label != 'oldimporter' and obj2._meta.app_label != 'oldimporter':
            return True
        else:
            return

    def allow_syncdb(self, db, model):
        """
        Make sure the old_nodeshot app only appears in the 'old_nodeshot' database
        """
        if db != 'old_nodeshot' and model._meta.app_label != 'oldimporter':
            return True
        else:
            return

    allow_migrate = allow_syncdb


class OldNodeshotRouter(object):

    def db_for_read(self, model, **hints):
        """
        Reads old nodeshot models from old_nodeshot db.
        """
        if model._meta.app_label == 'oldimporter':
            return 'old_nodeshot'
        else:
            return

    def db_for_write(self, model, **hints):
        """
        Writes not allowed
        """
        if model._meta.app_label == 'oldimporter':
            return 'old_nodeshot'
        else:
            return

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed between old_nodeshot objects only
        """
        if obj1._meta.app_label == 'oldimporter' and obj2._meta.app_label == 'oldimporter':
            return True
        else:
            return

    def allow_syncdb(self, db, model):
        """
        Make sure the old_nodeshot app only appears in the 'old_nodeshot' database
        """
        if db != 'old_nodeshot' or model._meta.app_label != 'oldimporter':
            return False
        return True

    allow_migrate = allow_syncdb