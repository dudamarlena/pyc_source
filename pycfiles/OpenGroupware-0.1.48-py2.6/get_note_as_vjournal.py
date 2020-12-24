# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_note_as_vjournal.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.core.icalendar import Render

class GetNoteAsVJournal(GetCommand):
    __domain__ = 'note'
    __operation__ = 'get-as-vjournal'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        if params.has_key('object'):
            self.data = [
             params['object']]
        elif params.has_key('objects'):
            self.data = params['objects']
        else:
            raise 'No notes provided to command.'

    def run(self):
        if self.data is None:
            self._result = None
        self._result = Render.render(self.data, self._ctx)
        return