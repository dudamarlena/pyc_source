# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/routers.py
# Compiled at: 2015-10-19 03:33:47
from __future__ import unicode_literals
__author__ = b'Matthieu Gallet'

class PowerdnsManagerDbRouter(object):

    def db_for_read(self, model, **hints):
        """Point all operations on powerdns models to 'powerdns'"""
        if model._meta.app_label == b'powerdns':
            return b'powerdns'
        else:
            return

    def db_for_write(self, model, **hints):
        """Point all operations on powerdns models to 'powerdns'"""
        if model._meta.app_label == b'auth':
            return b'default'
        else:
            if model._meta.app_label == b'powerdns':
                return b'powerdns'
            return

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if a model in powerdns is involved"""
        if obj1._meta.app_label == b'powerdns' or obj2._meta.app_label == b'powerdns':
            return True
        return

    def allow_migrate(self, db, model):
        """Make sure the powerdns app only appears on the 'powerdns' db"""
        if db == b'powerdns':
            return model._meta.app_label == b'powerdns'
        else:
            if model._meta.app_label == b'powerdns':
                return False
            return