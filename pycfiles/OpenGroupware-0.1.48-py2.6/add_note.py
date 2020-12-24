# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/add_note.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from command import ContactCommand

class AddContactNote(Command, ContactCommand):
    __domain__ = 'contact'
    __operation__ = 'new-note'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'contact' in params:
            self._contact = params.get('contact')
        elif 'contact_id' in params:
            contact_id = int(params.get('contact_id'))
            self._contact = self.get_by_id(contact_id, self.access_check)
            if self._contact is None:
                raise CoilsException(('Specified ContactId#{0} not available for contact::new-note').format(contact_id))
        else:
            raise CoilsException('No contact specified for contact::new-note')
        self._text = params.get('text', '')
        self._kind = params.get('kind', None)
        self._title = params.get('title', '')
        return

    def run(self):
        self.set_return_value(self._ctx.run_command('note::new', values={'title': self._title}, text=self._text, kind=self._kind, context=self._contact))