# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mukulhase/Dev/github/webwhatsapp-scripts/webwhatsapi/objects/contact.py
# Compiled at: 2018-05-27 06:05:33
# Size of source mod 2**32: 1418 bytes
from six import string_types
from .whatsapp_object import WhatsappObjectWithId, driver_needed
from ..helper import safe_str

class Contact(WhatsappObjectWithId):
    __doc__ = "\n    Class which represents a Contact on user's phone\n    "

    def __init__(self, js_obj, driver=None):
        """

        :param js_obj:
        :param driver:
        :type driver: WhatsAPIDriver
        """
        super(Contact, self).__init__(js_obj, driver)
        if 'shortName' in js_obj:
            self.short_name = js_obj['shortName']
        if 'pushname' in js_obj:
            self.push_name = js_obj['pushname']
        if 'formattedName' in js_obj:
            self.formatted_name = js_obj['formattedName']

    @driver_needed
    def get_common_groups(self):
        return list(self.driver.contact_get_common_groups(self.id))

    @driver_needed
    def get_chat(self):
        return self.driver.get_chat_from_id(self.id)

    def get_safe_name(self):
        """

        :return: String used for representation of the Contact

        :rtype: String

        """
        name = self.name or self.push_name or self.formatted_name
        if isinstance(name, string_types):
            safe_name = safe_str(name)
        else:
            safe_name = 'Unknown'
        return safe_name

    def __repr__(self):
        safe_name = self.get_safe_name()
        return '<Contact {0} ({1})>'.format(safe_name, self.id)