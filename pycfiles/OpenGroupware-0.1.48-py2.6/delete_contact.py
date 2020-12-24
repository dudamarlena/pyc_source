# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/delete_contact.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.logic.address import DeleteCompany
from keymap import COILS_CONTACT_KEYMAP
from command import ContactCommand

class DeleteContact(DeleteCompany, ContactCommand):
    __domain__ = 'contact'
    __operation__ = 'delete'

    def __init__(self):
        DeleteCompany.__init__(self)

    def run(self):
        DeleteCompany.run(self)