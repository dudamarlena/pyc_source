# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/sipphone/AbstractBaseClass.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
SIPPHONE_SECTION = 'SIP-Phone'

class SipphoneAbstractBaseClass(object):

    def thread_register(self, name):
        pass

    @property
    def name(self):
        return 'SipphoneAbstractBaseClass'

    @property
    def sound_codecs(self):
        return []

    @property
    def sound_devices(self):
        return []

    @property
    def current_call(self):
        return

    @property
    def video_codecs(self):
        return []

    @property
    def video_devices(self):
        return []

    @property
    def current_call_dump(self):
        return {}

    def __init__(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def config(self, **kwargs):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def start(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def stop(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def destroy(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def call(self, number):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def hangup(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def is_admin_number(self, number):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def __del__(self):
        self.destroy()


class RecorderAbstractBaseClass(object):

    def __init__(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def config(self, **kwargs):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def start(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def stop(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def destroy(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def __del__(self):
        self.destroy()


class PlayerAbstractBaseClass(object):

    def __init__(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def config(self, **kwargs):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def start(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def stop(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def destroy(self):
        raise NotImplementedError('Subclass %s should implement this!' % self.__class__.__name__)

    def __del__(self):
        self.destroy()