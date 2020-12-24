# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_handle.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import BLOBManager, Note
from coils.core import GetCommand

class GetNoteHandle(GetCommand):
    __domain__ = 'note'
    __operation__ = 'get-handle'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._mode = params.get('mode', 'rb')
        self._encoding = params.get('encoding', 'binary')

    def run(self, **params):
        filename = None
        db = self._ctx.db_session()
        query = db.query(Note).filter(Note.object_id.in_(self.object_ids))
        note = query.first()
        handle = BLOBManager.Open(note.get_path(), self._mode)
        if handle is not None:
            self._result = handle
            return
        else:
            message = ('Note path "{0}" is invalid (Note objectId#{1}).').format(note.get_path(), note.object_id)
            if self._ctx.amq_available:
                self._ctx.send_administrative_notice(category='data', urgency=6, subject=('Path to Note with objectId#{0} is invalid').format(note.object_id), message=message)
            raise CoilsException(message)
            return