# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/get_notes.py
# Compiled at: 2012-10-12 07:02:39
import traceback
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetProjectNotes(GetCommand):
    __domain__ = 'project'
    __operation__ = 'get-notes'

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        if 'id' in params:
            self.project_id = int(params['id'])
        elif 'project' in params:
            self.project_id = params['project'].object_id
        else:
            raise CoilsException('No project or project id provided to project::get-notes')

    def add_comments(self, notes):
        for note in notes:
            handle = self._ctx.run_command('note::get-handle', id=note.object_id)
            try:
                note.content = handle.read()
            except UnicodeDecodeError, e:
                message = traceback.format_exc()
                if self._ctx.amq_available:
                    self._ctx.send_administrative_notice(category='data', urgency=6, subject=('UTF-8 Decoding Error with Note objectId#{0}').format(note.object_id), message=message)
                raise e

        return notes

    def run(self, **params):
        self.access_check = False
        self.mode = RETRIEVAL_MODE_MULTIPLE
        db = self._ctx.db_session()
        query = db.query(Note).filter(and_(Note.project_id == self.project_id, Note.status != 'archived'))
        return self.set_return_value(self.add_comments(query.all()))