# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mukulhase/Dev/github/webwhatsapp-scripts/webwhatsapi/objects/whatsapp_object.py
# Compiled at: 2018-05-27 06:05:33
# Size of source mod 2**32: 2140 bytes
from weakref import ref

def driver_needed(func):
    """
    Decorator for WhatsappObjectWithId methods that need to communicate with the browser

    It ensures that the object receives a driver instance at construction

    :param func: WhatsappObjectWithId method
    :return: Wrapped method
    """

    def wrapped(self, *args):
        if not self.driver:
            raise AttributeError('No driver passed to object')
        return func(self, *args)

    return wrapped


class WhatsappObject(object):
    __doc__ = '\n    Base class for Whatsapp objects\n\n    Intended to wrap JS objects fetched from the browser\n\n    Can also be used as an interface to operations (such as sending messages to chats)\n    To enable this functionality the constructor must receive a WhatsAPIDriver instance\n    '

    def __init__(self, js_obj, driver=None):
        """
        Constructor

        :param js_obj: Whatsapp JS object to wrap
        :type js_obj: dict
        :param driver: Optional driver instance
        :type driver: WhatsAPIDriver
        """
        self._js_obj = js_obj
        self._driver = ref(driver)

    @property
    def driver(self):
        return self._driver()

    def get_js_obj(self):
        return self._js_obj


class WhatsappObjectWithId(WhatsappObject):
    __doc__ = '\n    Base class for Whatsapp objects\n\n    Intended to wrap JS objects fetched from the browser\n\n    Can also be used as an interface to operations (such as sending messages to chats)\n    To enable this functionality the constructor must receive a WhatsAPIDriver instance\n    '

    def __init__(self, js_obj, driver=None):
        """
        Constructor

        :param js_obj: Whatsapp JS object to wrap
        :type js_obj: dict
        :param driver: Optional driver instance
        :type driver: WhatsAPIDriver
        """
        super(WhatsappObjectWithId, self).__init__(js_obj, driver)
        if 'id' in js_obj:
            self.id = js_obj['id']
        if 'name' in js_obj:
            self.name = js_obj['name']

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id