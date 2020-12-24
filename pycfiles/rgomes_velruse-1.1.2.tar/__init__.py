# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/nfs/terra.localdomain/home/rgomes/sources/frgomes/velruse/feature.kotti_auth/velruse/examples/kotti_velruse/kotti_velruse/__init__.py
# Compiled at: 2013-10-27 18:57:38
from pyramid.config import Configurator
import velruse.app, views
log = __import__('logging').getLogger(__name__)

def includeme(config):
    velruse.app.includeme(config)
    views.includeme(config)