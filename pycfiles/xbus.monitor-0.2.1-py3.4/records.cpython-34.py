# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/resources/records.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 1575 bytes
from pyramid.httpexceptions import HTTPBadRequest
from pyramid import security
from xbus.monitor.auth import MANAGER_GROUP
from xbus.monitor.resources.root import RootFactory

class GenericRecordFactory(RootFactory):
    __doc__ = 'Base factory for individual records; provides:\n    - id_attribute: name of the "ID" attribute.\n    - record_id.\n    - record: sqlalchemy representation of the record.\n    - sqla_model: sqlalchemy class.\n    - sqla_session: sqlalchemy session object.\n    '
    id_attribute = 'id'
    sqla_model = None
    __acl__ = [
     (
      security.Allow, MANAGER_GROUP, 'read'),
     (
      security.Allow, MANAGER_GROUP, 'update'),
     (
      security.Allow, MANAGER_GROUP, 'delete')]

    def __init__(self, request):
        self.record_id = self._get_record_id(request)
        query = self.sqla_session(request).query(self.sqla_model)
        query = query.filter(getattr(self.sqla_model, self.id_attribute) == self.record_id)
        self.record = query.first()

    def sqla_session(self, request):
        """To be implemented by derived classes.
        :rtype: SQLAlchemy session object.
        """
        raise NotImplementedError

    @staticmethod
    def _get_record_id(request):
        try:
            return request.matchdict.get('id')
        except:
            raise HTTPBadRequest(json_body={'error': 'Invalid ID'})