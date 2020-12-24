# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/get_versions.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetDocumentVersions(GetCommand):
    __domain__ = 'document'
    __operation__ = 'get-versions'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if 'document' in params:
            self.object_ids.append(params['document'].object_id)

    def run(self, **params):
        self.set_multiple_result_mode()
        db = self._ctx.db_session()
        query = db.query(DocumentVersion).filter(DocumentVersion.document_id.in_(self.object_ids))
        self.set_return_value(query.all())


class GetDocumentVersion(GetCommand):
    __domain__ = 'document'
    __operation__ = 'get-version'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        if len(self.object_ids) == 0:
            if 'document' in params:
                self.object_ids.append(params['document'].object_id)
            else:
                raise CoilsException('Not document id specified for document::get-version')
        self._version = int(params.get('version', 1))

    def run(self, **params):
        self.set_single_result_mode()
        object_id = self.object_ids[0]
        db = self._ctx.db_session()
        query = db.query(DocumentVersion).filter(and_(DocumentVersion.document_id == object_id, DocumentVersion.version == self._version))
        self.set_return_value(query.all())