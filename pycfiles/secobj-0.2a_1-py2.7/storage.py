# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/storage.py
# Compiled at: 2012-08-22 08:52:48
from abc import ABCMeta, abstractmethod
from secobj.config import getconfig
from secobj.localization import _
from secobj.logger import getlogger
from secobj.utils import error

class Storage(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.config = getconfig()
        self.log = getlogger('storage')
        self.providerclass = None
        return

    def createprovider(self):
        if self.providerclass is None:
            from secobj.provider import SecurityProvider
            package, classname = self.config.get('secobj', 'provider').rsplit('.', 1)
            try:
                module = __import__(package, fromlist=[classname])
                self.providerclass = getattr(module, classname)
            except Exception:
                raise error(ValueError, self.log, _('Invalid provider class: {package}.{classname}'), package=package, classname=classname)

            if not issubclass(self.providerclass, SecurityProvider):
                raise error(ValueError, self.log, _("'{package}.{classname}' is not a provider class"), package=package, classname=classname)
        return self.providerclass()

    @abstractmethod
    def getprovider(self):
        raise NotImplementedError


GLOBAL_PROVIDER = None

class GlobalStorage(Storage):

    def getprovider(self):
        global GLOBAL_PROVIDER
        if GLOBAL_PROVIDER is None:
            GLOBAL_PROVIDER = self.createprovider()
        return GLOBAL_PROVIDER


class ThreadStorage(Storage):

    def getprovider(self):
        import threading
        l = threading.local()
        if not hasattr(l, '__secobj_provider__'):
            l.__secobj_provider__ = self.createprovider()
        return l.__secobj_provider__


STORAGE = None

def getstorage():
    global STORAGE
    if STORAGE is None:
        config = getconfig()
        log = getlogger('storage')
        package, classname = config.get('secobj', 'storage').rsplit('.', 1)
        try:
            module = __import__(package, fromlist=[classname])
            storageclass = getattr(module, classname)
        except Exception:
            raise error(ValueError, log, _('Invalid storage class: {package}.{classname}'), package=package, classname=classname)

        if not issubclass(storageclass, Storage):
            raise error(ValueError, log, _("'{package}.{classname}' is not a storage class"), package=package, classname=classname)
        STORAGE = storageclass()
    return STORAGE