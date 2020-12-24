# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/frontends/embeddedclient.py
# Compiled at: 2007-12-02 16:26:54
from salamoia.h2o.logioni import *
from salamoia.h2o.container import *
from salamoia.frontends.config import Config
import traceback
try:
    from salamoia.nacl.backend import Backend
except:
    print 'GOT EXCEPTION IMPORTING BACKEND'
    raise

class FakeNaclOptions(object):
    __module__ = __name__

    def __init__(self):
        pass


class EmbeddedClient(object):
    __module__ = __name__

    def __init__(self, profile=None):
        self.profile = profile
        Ione.setLogMode('syslog')
        cfg = Config()
        Backend.options = FakeNaclOptions()
        Backend.options.profile = cfg.get(profile, 'naclprofile', profile)
        self._backendInfo = {'naclUptime': 'fake', 'suffix': cfg.get(profile, 'suffix', ''), 'loggedUsers': [''], 'hostname': 'embedded'}
        try:
            self.control = Backend.defaultBackendClass()().controlClass()()
        except:
            traceback.print_exc()
            raise

    def connect(self):
        pass

    def backendInfo(self, action):
        return self._backendInfo[action]

    def __getattr__(self, name):
        return EmbeddedClientWrapper(getattr(self.control, name))


class EmbeddedClientWrapper(object):
    __module__ = __name__

    def __init__(self, method):
        self.method = method

    def __call__(self, *args, **kwargs):
        res = self.method(*args, **kwargs)
        if isinstance(res, Object):
            res = res.resurrect()
        return res