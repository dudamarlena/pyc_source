# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joe/workspace/python/klient/src/django-caldav/django_caldav/lock.py
# Compiled at: 2014-08-22 06:39:00
from djangodav import locks

class DummyLock(locks.DummyLock):
    pass