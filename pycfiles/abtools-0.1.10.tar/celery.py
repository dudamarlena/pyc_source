# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bryanbriney/git/ab-tools/identity_divergence/queue/celery.py
# Compiled at: 2015-01-06 03:27:13
from __future__ import absolute_import
from celery import Celery
celery = Celery(include=['utils.identity'])
celery.config_from_object('celeryconfig')
if __name__ == '__main__':
    celery.start()