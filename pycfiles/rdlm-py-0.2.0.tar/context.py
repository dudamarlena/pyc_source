# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fab/Documents/rdlm-py/rdlmpy/context.py
# Compiled at: 2013-03-04 16:22:39
from rdlmpy.client import RDLMClient

class RDLMContextManager(object):
    """
    Class which defines a ContextManager to get a convenient way to use RDLMClient with
    the "with" statement
    """
    __client = None
    __resource_name = None
    __lock = None

    def __init__(self, resource_name, server='localhost', port=8888, lifetime=300, wait=10, title=None):
        self.__client = RDLMClient(server=server, port=port, default_lifetime=lifetime, default_wait=wait, default_title=title)
        self.__resource_name = resource_name

    def __enter__(self):
        self.__lock = self.__client.lock_acquire(self.__resource_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__lock:
            self.__client.lock_release(self.__lock)
        return False


class RDLMContextManagerFactory(object):
    """
    Class which defines a factory of ContextManager preconfigured object
    """
    __default_server = None
    __default_port = None
    __default_lifetime = None
    __default_wait = None
    __default_title = None

    def __init__(self, default_server='localhost', default_port=8888, default_lifetime=300, default_wait=10, default_title=None):
        self.__default_server = default_server
        self.__default_port = default_port
        self.__default_lifetime = default_lifetime
        self.__default_wait = default_wait
        self.__default_title = default_title

    def factory(self, resource_name, override_server=None, override_port=None, override_lifetime=None, override_wait=10, override_title=None):
        server = override_server if override_server is not None else self.__default_server
        port = override_port if override_port is not None else self.__default_port
        lifetime = override_lifetime if override_lifetime is not None else self.__default_lifetime
        wait = override_wait if override_wait is not None else self.__default_wait
        title = override_title if override_title is not None else self.__default_title
        return RDLMContextManager(resource_name, server=server, port=port, lifetime=lifetime, wait=wait, title=title)