# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/openidutil.py
# Compiled at: 2007-09-26 14:43:59
from pylons import request, c, session, config
from openid.store.filestore import FileOpenIDStore
from openid.consumer import consumer
from openid.consumer.discover import DiscoveryFailure
import os

def openid_store():
    cache = config['app_conf']['cache_dir']
    storepath = os.path.join(cache, 'openid_store.db')
    return FileOpenIDStore(storepath)


def openid_consumer():
    return consumer.Consumer(session, openid_store())


try:
    from openid import urinorm

    def normalizeURI(uri):
        return urinorm.urinorm(uri)


except ImportError:
    from openid import oidutil

    def normalizeURI(uri):
        return oidutil.normalizeUrl(uri)