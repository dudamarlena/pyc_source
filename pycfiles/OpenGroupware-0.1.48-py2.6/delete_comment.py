# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/schedular/delete_comment.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.foundation import *
from coils.core import *

class DeleteComment(Command):
    __domain__ = 'appointment'
    __operation__ = 'delete-comment'

    def __init__(self):
        Command.__init__(self)
        self._result = False

    def parse_parameters(self, **params):
        self.obj = params.get('appointment', None)
        return

    def delete(self):
        db = self._ctx.db_session()
        comment = db.query(DateInfo).filter(DateInfo.parent_id == self.obj.object_id).first()
        if comment is not None:
            self._ctx.db_session().delete(comment)
        return

    def run(self):
        if self.obj is None:
            raise CoilsException('Delete comment invoked with no appointment')
        self.delete()
        self._result = True
        return