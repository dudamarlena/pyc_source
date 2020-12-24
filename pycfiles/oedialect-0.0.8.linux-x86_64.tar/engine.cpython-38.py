# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/oedialect/engine.py
# Compiled at: 2020-04-01 06:35:53
# Size of source mod 2**32: 12005 bytes
import json, os, requests, sqlalchemy
import dateutil.parser as parse_date
from shapely import wkb
from psycopg2.extensions import PYINTERVAL
from oedialect import error

def date_handler(obj):
    """
    Implements a handler to serialize dates in JSON-strings
    :param obj: An object
    :return: The str method is called (which is the default serializer for JSON) unless the object has an attribute  *isoformat*
    """
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return str(obj)


class OEConnection:
    __doc__ = '\n\n    '

    def __init__(self, host='localhost', port=80, user='', database='', password=''):
        self._OEConnection__host = host
        self._OEConnection__port = port
        self._OEConnection__user = user
        self._OEConnection__token = password
        response = self.post('advanced/connection/open', {})['content']
        self._id = response['connection_id']
        self._OEConnection__transactions = set()
        self._cursors = set()
        self._OEConnection__closed = False

    def close(self, *args, **kwargs):
        response = self.post('advanced/connection/close', {}, requires_connection_id=True)

    def commit(self, *args, **kwargs):
        response = self.post('advanced/connection/commit', {}, requires_connection_id=True)

    def rollback(self, *args, **kwargs):
        response = self.post('advanced/connection/rollback', {}, requires_connection_id=True)

    def cursor(self, *args, **kwargs):
        cursor = OECursor(self)
        self._cursors.add(cursor)
        return cursor

    def xid(self, *args, **kwargs):
        raise NotImplementedError

    def tpc_begin(self, *args, **kwargs):
        raise NotImplementedError

    def tpc_commit(self, *args, **kwargs):
        raise NotImplementedError

    def tpc_prepare(self, *args, **kwargs):
        raise NotImplementedError

    def tpc_recover(self, *args, **kwargs):
        raise NotImplementedError

    def tpc_rollback(self, *args, **kwargs):
        raise NotImplementedError

    def cancel(self, *args, **kwargs):
        raise NotImplementedError

    def reset(self, *args, **kwargs):
        raise NotImplementedError

    def set_session(self, *args, **kwargs):
        raise NotImplementedError

    def set_client_encoding(self, *args, **kwargs):
        raise NotImplementedError

    def set_isolation_level(self, *args, **kwargs):
        raise NotImplementedError

    def get_backend_pid(self, *args, **kwargs):
        raise NotImplementedError

    def get_dsn_parameters(self, *args, **kwargs):
        raise NotImplementedError

    def get_parameter_status(self, *args, **kwargs):
        raise NotImplementedError

    def get_transaction_status(self, *args, **kwargs):
        raise NotImplementedError

    def lobject(self, *args, **kwargs):
        raise NotImplementedError

    def poll(self, *args, **kwargs):
        raise NotImplementedError

    def fileno(self, *args, **kwargs):
        raise NotImplementedError

    def isexecuting(self, *args, **kwargs):
        raise NotImplementedError

    def post_expect_stream(self, suffix, query, cursor_id=None):
        sender = requests.post
        header = dict(urlheaders)
        if self._OEConnection__token:
            header['Authorization'] = 'Token %s' % self._OEConnection__token
        data = {}
        if cursor_id:
            data['connection_id'] = self._id
            data['cursor_id'] = cursor_id
        host = self._OEConnection__host
        if self._OEConnection__host in ('oep.iks.cs.ovgu.de', 'oep2.iks.cs.ovgu.de',
                                        'oep.iws.cs.ovgu.de', 'oep2.iws.cs.ovgu.de',
                                        'openenergyplatform.org'):
            host = 'openenergy-platform.org'
        port = self._OEConnection__port if self._OEConnection__port != 80 else 443
        protocol = os.environ.get('OEDIALECT_PROTOCOL', 'https')
        assert protocol in ('http', 'https')
        verify = os.environ.get('OEDIALECT_VERIFY_CERTIFICATE', 'TRUE') == 'TRUE'
        response = sender('{protocol}://{host}:{port}/api/v0/{suffix}'.format(protocol=protocol,
          host=host,
          port=port,
          suffix=suffix),
          json=(json.loads(json.dumps(data))),
          headers=header,
          stream=True,
          verify=verify)
        process_returntype(response)
        try:
            i = 0
            for line in response.iter_lines():
                (yield json.loads(line.decode('utf8').replace("'", '\\"')))

        except Exception as e:
            try:
                raise
            finally:
                e = None
                del e

    def post(self, suffix, query, cursor_id=None, requires_connection_id=False):
        sender = requests.post
        if isinstance(query, dict):
            if 'request_type' in query:
                if query['request_type'] == 'put':
                    sender = requests.put
                if query['request_type'] == 'delete':
                    sender = requests.delete
        if 'info_cache' in query:
            del query['info_cache']
        data = {'query': query}
        if requires_connection_id or cursor_id:
            data['connection_id'] = self._id
        if cursor_id:
            data['cursor_id'] = cursor_id
        header = dict(urlheaders)
        if self._OEConnection__token:
            header['Authorization'] = 'Token %s' % self._OEConnection__token
        host = self._OEConnection__host
        if self._OEConnection__host in ('oep.iks.cs.ovgu.de', 'oep2.iks.cs.ovgu.de',
                                        'oep.iws.cs.ovgu.de', 'oep2.iws.cs.ovgu.de',
                                        'openenergyplatform.org'):
            host = 'openenergy-platform.org'
        port = self._OEConnection__port if self._OEConnection__port != 80 else 443
        protocol = os.environ.get('OEDIALECT_PROTOCOL', 'https')
        assert protocol in ('http', 'https')
        verify = os.environ.get('OEDIALECT_VERIFY_CERTIFICATE', 'TRUE') == 'TRUE'
        ans = sender('{protocol}://{host}:{port}/api/v0/{suffix}'.format(protocol=protocol,
          host=host,
          port=port,
          suffix=suffix),
          json=(json.loads(json.dumps(data, default=date_handler))),
          headers=header,
          verify=verify)
        try:
            json_response = ans.json()
        except:
            raise ConnectionException('Answer contains no JSON: ' + repr(ans))
        else:
            process_returntype(ans, json_response)
            return json_response


def process_returntype(response, content=None):
    if content is None:
        content = {}
    if 400 <= response.status_code < 500:
        message = content.get('reason', '')
        raise ConnectionException('HTTP %d (%s): %s' % (response.status_code, response.reason, message))
    else:
        if 500 <= response.status_code < 600:
            raise ConnectionException('Server side error: ' + content.get('reason', 'No reason returned'))


class OECursor:
    description = None
    rowcount = -1

    def __init__(self, connection):
        self._OECursor__connection = connection
        try:
            response = self._OECursor__connection.post('advanced/cursor/open', {}, requires_connection_id=True)
            if 'content' not in response:
                raise error.CursorError('Could not open cursor: ' + str(response['reason']) if 'reason' in response else 'No reason returned')
            response = response['content']
        except:
            raise
        else:
            self._OECursor__id = response['cursor_id']

    def __replace_params(self, jsn, params):
        if type(jsn) == dict:
            for k in jsn:
                jsn[k] = self._OECursor__replace_params(jsn[k], params)
            else:
                return jsn

        if type(jsn) == list:
            return list(map(lambda x: self._OECursor__replace_params(x, params), jsn))
        if type(jsn) in (str, sqlalchemy.sql.elements.quoted_name,
         sqlalchemy.sql.elements._truncated_label):
            return (jsn % params).strip("'<>").replace("'", '"')
        if isinstance(jsn, int):
            return jsn
        if callable(jsn):
            return jsn(params)
        raise Exception('Unknown jsn type (%s) in %s' % (type(jsn), jsn))

    _OECursor__cell_processors = {17:lambda cell: wkb.dumps(wkb.loads(cell, hex=True)), 
     1114:lambda cell: parse_date(cell), 
     1082:lambda cell: parse_date(cell).date(), 
     1186:lambda cell: PYINTERVAL(cell, None)}

    def process_result(self, row):
        for i, x in enumerate(self.description):
            if row[i] and x[1] in self._OECursor__cell_processors:
                row[i] = self._OECursor__cell_processors[x[1]](row[i])
            return row

    def fetchone(self):
        response = self._OECursor__connection.post('advanced/cursor/fetch_one', {}, cursor_id=(self._OECursor__id))['content']
        if response:
            response = self.process_result(response)
        return response

    def fetchall(self):
        result = self._OECursor__connection.post_expect_stream('advanced/cursor/fetch_all', {}, cursor_id=(self._OECursor__id))
        if result:
            for row in result:
                (yield self.process_result(row))

    def fetchmany(self, size):
        result = self._OECursor__connection.post('advanced/cursor/fetch_many', {'size': size}, cursor_id=(self._OECursor__id))['content']
        if result:
            for row in result:
                (yield self.process_result(row))

    def execute(self, query_obj, params=None):
        if query_obj is None:
            return
            if not isinstance(query_obj, dict):
                if isinstance(query_obj, str):
                    raise Exception('Plain string commands are not supported.Please use SQLAlchemy datastructures')
                query = query_obj.string
            else:
                query = query_obj
            query = dict(query)
            requires_connection_id = query.get('requires_connection', False)
            query['connection_id'] = self._OECursor__connection._id
            query['cursor_id'] = self._OECursor__id
            if params:
                if isinstance(params, tuple) and 'values' in query:
                    query['values'] = [self._OECursor__replace_params(query['values'][0], p) for p in params]
        else:
            query = self._OECursor__replace_params(query, params)
        command = query.pop('command')
        return self._OECursor__execute_by_post(command, query, requires_connection_id=requires_connection_id)

    def executemany(self, query, params=None):
        if params is None:
            return self.execute(query)
        if query.isinsert:
            if not query.isdelete:
                if not query.isupdate:
                    return self.execute(query, params)
        return [self.execute(query, p) for p in params]

    def close(self):
        self._OECursor__connection.post('advanced/cursor/close', {}, cursor_id=(self._OECursor__id))

    def __execute_by_post(self, command, query, requires_connection_id=False):
        response = self._OECursor__connection.post(command, query, cursor_id=(self._OECursor__id), requires_connection_id=requires_connection_id)
        if 'content' in response:
            result = response['content']
            if result:
                if isinstance(result, dict):
                    if 'description' in result:
                        self.description = result['description']
                    if 'rowcount' in result:
                        self.rowcount = result['rowcount']
                else:
                    return result
            else:
                return result


urlheaders = {}

class ConnectionException(Exception):
    pass