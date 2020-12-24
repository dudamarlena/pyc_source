# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_note.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetNote(GetCommand):
    __domain__ = 'note'
    __operation__ = 'get'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if 'uid' in params:
            self._caldav_uid = unicode(params.get('uid'))
        else:
            self._caldav_uid = None
        return

    def add_comments(self, notes):
        self.log.info('getting comments')
        for note in notes:
            handle = self._ctx.run_command('note::get-handle', id=note.object_id)
            note.content = handle.read()

        return notes

    def run(self):
        db = self._ctx.db_session()
        if self._caldav_uid is None:
            query = db.query(Note).filter(and_(Note.object_id.in_(self.object_ids), Note.status != 'archived'))
        else:
            self.set_single_result_mode()
            query = db.query(Note).filter(Note.caldav_uid == self._caldav_uid)
        self.set_return_value(self.add_comments(query.all()))
        return