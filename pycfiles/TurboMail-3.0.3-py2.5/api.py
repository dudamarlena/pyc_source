# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/api.py
# Compiled at: 2009-11-05 11:34:55
"""TurboMail extension API."""
import logging, warnings
from turbomail.control import interface
from turbomail.exceptions import ManagerException
__all__ = [
 'Extension', 'TransportFactory', 'Transport', 'Manager']

class Extension(object):
    """Basic extension API that allows for startup and shutdown hooks."""

    def __init__(self):
        super(Extension, self).__init__()
        self.ready = False

    def start(self):
        self.ready = True
        return True

    def stop(self):
        if not self.ready:
            return False
        self.ready = False
        return True


class TransportFactory(Extension):
    """An extension that creates new Transport instances.
    
    This is useful to perform configuration or startup tasks outside the Transport's initializer.
    """
    transport = None

    def __init__(self):
        super(TransportFactory, self).__init__()

    def new(self):
        if not self.ready:
            return
        return self.transport()


class Transport(object):
    """Message delivery subsystem API.
    
    A Transport can deliver messages towards their recipients with a specific
    method, e.g. SMTP. They don't care about delivery strategies like queing or
    batch submission."""

    def __init__(self):
        super(Transport, self).__init__()

    def deliver(self, message):
        raise NotImplementedError, 'Transport plugin must override this method without inheritance.'

    def config_get(self, key, default=None, tm2_key=None):
        """Returns the value for the given key from the configuration. If the 
        value was not found, this method looks if old configuration option 
        (specified in tm2_key) is used. If tm2_key was ommitted, it tries to
        calculate the old key from the new one by cutting out the 'smtp.' in the
        middle. If an old configuration key is used, a DeprecationWarning is
        issued. 
        As a final fallback, the default value (default None) is 
        returned."""
        value = interface.config.get(key, None)
        if value == None:
            if tm2_key != None and not tm2_key.startswith('mail.'):
                tm2_key = 'mail.' + tm2_key
            elif tm2_key == None:
                tm2_key = key.replace('.smtp.', '.')
            value = interface.config.get(tm2_key, None)
            if value is not None:
                basemsg = 'Configuration key "%s" is deprecated, please use "%s" instead'
                warn_text = basemsg % (tm2_key, key)
                warnings.warn(warn_text, category=DeprecationWarning)
        if value == None:
            value = default
        return value

    def stop(self):
        """Called by the manager before the transport instance is destroyed. The
        transport can do some final cleanups (like releasing external resources)
        here."""
        pass


class Manager(Extension):
    """Manager instances orchestrate the delivery of messages."""

    def __init__(self):
        super(Manager, self).__init__()
        self.transport_factory = None
        return

    def get_new_transport(self):
        if self.transport_factory == None:
            self.transport_factory = interface.transport
        transport = self.transport_factory.new()
        if transport is None:
            raise ManagerException('Unable to allocate new transport.')
        return transport

    def deliver(self, message):
        return self.ready