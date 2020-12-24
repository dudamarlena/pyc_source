# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/update_contact.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.logic.address import UpdateCompany
from coils.foundation import *
from keymap import COILS_CONTACT_KEYMAP
from command import ContactCommand

class UpdateContact(UpdateCompany, ContactCommand):
    __domain__ = 'contact'
    __operation__ = 'set'

    def prepare(self, ctx, **params):
        self.keymap = COILS_CONTACT_KEYMAP
        UpdateCompany.prepare(self, ctx, **params)
        self.set_enterprises()
        self.set_projects()