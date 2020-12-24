# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/uniconnect/client.py
# Compiled at: 2019-08-27 00:58:10
"""

This module implements the uniconnect protocol to submit SQL statements, track
their state and retrieve their result as described in
https://github.com/uniconnect/uniconnect/wiki/HTTP-Protocol
and uniconnect source code.

The outline of a query is:
- Send HTTP POST to the coordinator
- Retrieve HTTP response with ``nextUri``
- Get status of the query execution by sending a HTTP GET to the coordinator

uniconnect queries are managed by the ``uniconnectQuery`` class. HTTP requests are
managed by the ``uniconnectRequest`` class. the status of a query is represented
by ``uniconnectStatus`` and the result by ``uniconnectResult``.

The main interface is :class:`uniconnectQuery`: ::

    >> request = uniconnectRequest(host='coordinator', port=8080, user='test')
    >> query =  uniconnectQuery(request, sql)
    >> rows = list(query.execute())
"""
from __future__ import absolute_import, division, print_function
import os
from typing import Any, Dict, List, Optional, Text, Tuple, Union
import uniconnect.logging, uniconnect.redirect, requests
from uniconnect import constants, exceptions
from uniconnect.transaction import NO_TRANSACTION
__all__ = [
 'uniconnectQuery', 'uniconnectRequest']
logger = uniconnect.logging.get_logger(__name__)
MAX_ATTEMPTS = constants.DEFAULT_MAX_ATTEMPTS
SOCKS_PROXY = os.environ.get('SOCKS_PROXY')
if SOCKS_PROXY:
    PROXIES = {'http': 'socks5://' + SOCKS_PROXY, 'https': 'socks5://' + SOCKS_PROXY}
else:
    PROXIES = None

class ClientSession(object):

    def __init__(self, catalog, schema, source, user, properties=None, headers=None, transaction_id=None):
        self.catalog = catalog
        self.schema = schema
        self.source = source
        self.user = user
        if properties is None:
            properties = {}
        self._properties = properties
        self._headers = headers or {}
        self.transaction_id = transaction_id
        return

    @property
    def properties(self):
        return self._properties

    @property
    def headers(self):
        return self._headers


def get_header_values(headers, header):
    return [ val.strip() for val in headers[header].split(',') ]


def get_session_property_values(headers, header):
    kvs = get_header_values(headers, header)
    return [ (k.strip(), v.strip()) for k, v in (kv.split('=', 1) for kv in kvs) ]


class uniconnectStatus(object):

    def __init__(self, id, stats, warnings, info_uri, next_uri, rows, columns=None):
        self.id = id
        self.stats = stats
        self.warnings = warnings
        self.info_uri = info_uri
        self.next_uri = next_uri
        self.rows = rows
        self.columns = columns

    def __repr__(self):
        return ('uniconnectStatus(id={}, stats={{...}}, warnings={}, info_uri={}, next_uri={}, rows=<count={}>)').format(self.id, len(self.warnings), self.info_uri, self.next_uri, len(self.rows))


class uniconnectRequest(object):
    """
    Manage the HTTP requests of a uniconnect query.

    :param host: name of the coordinator
    :param port: TCP port to connect to the coordinator
    :param user: associated with the query. It is useful for access control
                 and query scheduling.
    :param source: associated with the query. It is useful for access
                   control and query scheduling.
    :param catalog: to query. The *catalog* is associated with a uniconnect
                    connector. This variable sets the default catalog used
                    by SQL statements. For example, if *catalog* is set
                    to ``some_catalog``, the SQL statement
                    ``SELECT * FROM some_schema.some_table`` will actually
                    query the table
                    ``some_catalog.some_schema.some_table``.
    :param schema: to query. The *schema* is a logical abstraction to group
                   table. This variable sets the default schema used by
                   SQL statements. For eample, if *schema* is set to
                   ``some_schema``, the SQL statement
                   ``SELECT * FROM some_table`` will actually query the
                   table ``some_catalog.some_schema.some_table``.
    :param session_properties: set specific uniconnect behavior for the current
                               session. Please refer to the output of
                               ``SHOW SESSION`` to check the available
                               properties.
    :param http_headers: HTTP headers to post/get in the HTTP requests
    :param http_scheme: "http" or "https"
    :param auth: class that manages user authentication. ``None`` means no
                 authentication.
    :max_attempts: maximum number of attempts when sending HTTP requests. An
                   attempt is an HTTP request. 5 attempts means 4 retries.
    :request_timeout: How long (in seconds) to wait for the server to send
                      data before giving up, as a float or a
                      ``(connect timeout, read timeout)`` tuple.

    The client initiates a query by sending an HTTP POST to the
    coordinator. It then gets a response back from the coordinator with:
    - An URI to query to get the status for the query and the remaining
      data
    - An URI to get more information about the execution of the query
    - Statistics about the current query execution

    Please refer to :class:`uniconnectStatus` to access the status returned by
    :meth:`uniconnectRequest.process`.

    When the client makes an HTTP request, it may encounter the following
    errors:
    - Connection or read timeout:
      - There is a network partition and TCP segments are
        either dropped or delayed.
      - The coordinator stalled because of an OS level stall (page allocation
        stall, long time to page in pages, etc...), a JVM stall (full GC), or
        an application level stall (thread starving, lock contention)
    - Connection refused: Configuration or runtime issue on the coordinator
    - Connection closed:

    As most of these errors are transient, the question the caller should set
    retries with respect to when they want to notify the application that uses
    the client.
    """
    http = requests
    HTTP_EXCEPTIONS = (
     http.ConnectionError,
     http.Timeout)

    def __init__(self, host, port, user, source=None, catalog=None, schema=None, session_properties=None, http_session=None, http_headers=None, transaction_id=NO_TRANSACTION, http_scheme=constants.HTTP, auth=constants.DEFAULT_AUTH, redirect_handler=uniconnect.redirect.GatewayRedirectHandler(), max_attempts=MAX_ATTEMPTS, request_timeout=constants.DEFAULT_REQUEST_TIMEOUT, handle_retry=exceptions.RetryWithExponentialBackoff()):
        self._client_session = ClientSession(catalog, schema, source, user, session_properties, http_headers, transaction_id)
        self._host = host
        self._port = port
        self._next_uri = None
        if http_session is not None:
            self._http_session = http_session
        else:
            self._http_session = self.http.Session()
        self._http_session.headers.update(self.http_headers)
        self._exceptions = self.HTTP_EXCEPTIONS
        self._auth = auth
        if self._auth:
            if http_scheme == constants.HTTP:
                raise ValueError('cannot use authentication with HTTP')
            self._auth.set_http_session(self._http_session)
            self._exceptions += self._auth.get_exceptions()
        self._redirect_handler = redirect_handler
        self._request_timeout = request_timeout
        self._handle_retry = handle_retry
        self.max_attempts = max_attempts
        self._http_scheme = http_scheme
        return

    @property
    def transaction_id(self):
        return self._client_session.transaction_id

    @transaction_id.setter
    def transaction_id(self, value):
        self._client_session.transaction_id = value

    @property
    def http_headers(self):
        headers = {}
        headers[constants.HEADER_CATALOG] = self._client_session.catalog
        headers[constants.HEADER_SCHEMA] = self._client_session.schema
        headers[constants.HEADER_SOURCE] = self._client_session.source
        headers[constants.HEADER_USER] = self._client_session.user
        headers[constants.HEADER_SESSION] = (',').join(('{}={}').format(name, value) for name, value in self._client_session.properties.items())
        for key in self._client_session.headers:
            if key in headers.keys():
                raise ValueError(('cannot override reserved HTTP header {}').format(key))

        headers.update(self._client_session.headers)
        transaction_id = self._client_session.transaction_id
        headers[constants.HEADER_TRANSACTION] = transaction_id
        return headers

    @property
    def max_attempts(self):
        return self._max_attempts

    @max_attempts.setter
    def max_attempts(self, value):
        self._max_attempts = value
        if value == 1:
            self._get = self._http_session.get
            self._post = self._http_session.post
            self._delete = self._http_session.delete
            return
        with_retry = exceptions.retry_with(self._handle_retry, exceptions=self._exceptions, conditions=(
         lambda response: getattr(response, 'status_code', None) == 503,), max_attempts=self._max_attempts)
        self._get = with_retry(self._http_session.get)
        self._post = with_retry(self._http_session.post)
        self._delete = with_retry(self._http_session.delete)

    def get_url(self, path):
        return ('{protocol}://{host}:{port}{path}').format(protocol=self._http_scheme, host=self._host, port=self._port, path=path)

    @property
    def statement_url(self):
        return self.get_url(constants.URL_STATEMENT_PATH)

    @property
    def next_uri(self):
        return self._next_uri

    def post(self, sql):
        data = sql.encode('utf-8')
        http_headers = self.http_headers
        http_response = self._post(self.statement_url, data=data, headers=http_headers, timeout=self._request_timeout, allow_redirects=self._redirect_handler is None, proxies=PROXIES)
        if self._redirect_handler is not None:
            while http_response is not None and http_response.is_redirect:
                location = http_response.headers['Location']
                url = self._redirect_handler.handle(location)
                logger.info(('redirect {} from {} to {}').format(http_response.status_code, location, url))
                http_response = self._post(url, data=data, headers=http_headers, timeout=self._request_timeout, allow_redirects=False, proxies=PROXIES)

        return http_response

    def get(self, url):
        return self._get(url, headers=self.http_headers, timeout=self._request_timeout, proxies=PROXIES)

    def delete(self, url):
        return self._delete(url, timeout=self._request_timeout, proxies=PROXIES)

    def _process_error(self, error, query_id):
        error_type = error['errorType']
        if error_type == 'EXTERNAL':
            raise exceptions.uniconnectExternalError(error, query_id)
        elif error_type == 'USER_ERROR':
            return exceptions.uniconnectUserError(error, query_id)
        return exceptions.uniconnectQueryError(error, query_id)

    def raise_response_error(self, http_response):
        if http_response.status_code == 503:
            raise exceptions.Http503Error('error 503: service unavailable')
        raise exceptions.HttpError(('error {}{}').format(http_response.status_code, (': {}').format(http_response.content) if http_response.content else ''))

    def process(self, http_response):
        if not http_response.ok:
            self.raise_response_error(http_response)
        http_response.encoding = 'utf-8'
        response = http_response.json()
        logger.debug(('HTTP {}: {}').format(http_response.status_code, response))
        if 'error' in response:
            raise self._process_error(response['error'], response.get('id'))
        if constants.HEADER_CLEAR_SESSION in http_response.headers:
            for prop in get_header_values(http_response.headers, constants.HEADER_CLEAR_SESSION):
                self._client_session.properties.pop(prop, None)

        if constants.HEADER_SET_SESSION in http_response.headers:
            for key, value in get_session_property_values(http_response.headers, constants.HEADER_SET_SESSION):
                self._client_session.properties[key] = value

        self._next_uri = response.get('nextUri')
        return uniconnectStatus(id=response['id'], stats=response['stats'], warnings=response.get('warnings', []), info_uri=response['infoUri'], next_uri=self._next_uri, rows=response.get('data', []), columns=response.get('columns'))


class uniconnectResult(object):
    """
    Represent the result of a uniconnect query as an iterator on rows.

    This class implements the iterator protocol as a generator type
    https://docs.python.org/3/library/stdtypes.html#generator-types
    """

    def __init__(self, query, rows=None):
        self._query = query
        self._rows = rows or []
        self._rownumber = 0

    @property
    def rownumber(self):
        return self._rownumber

    def __iter__(self):
        for row in self._rows:
            self._rownumber += 1
            yield row

        self._rows = None
        while not self._query.is_finished():
            rows = self._query.fetch()
            for row in rows:
                self._rownumber += 1
                logger.debug(('row {}').format(row))
                yield row

        return


class uniconnectQuery(object):
    """Represent the execution of a SQL statement by uniconnect."""

    def __init__(self, request, sql):
        self.query_id = None
        self._stats = {}
        self._warnings = []
        self._columns = None
        self._finished = False
        self._cancelled = False
        self._request = request
        self._sql = sql
        self._result = uniconnectResult(self)
        return

    @property
    def columns(self):
        return self._columns

    @property
    def stats(self):
        return self._stats

    @property
    def warnings(self):
        return self._warnings

    @property
    def result(self):
        return self._result

    def execute(self):
        """Initiate a uniconnect query by sending the SQL statement

        This is the first HTTP request sent to the coordinator.
        It sets the query_id and returns a Result object used to
        track the rows returned by the query. To fetch all rows,
        call fetch() until is_finished is true.
        """
        if self._cancelled:
            raise exceptions.uniconnectUserError('Query has been cancelled', self.query_id)
        response = self._request.post(self._sql)
        status = self._request.process(response)
        self.query_id = status.id
        self._stats.update({'queryId': self.query_id})
        self._stats.update(status.stats)
        self._warnings = getattr(status, 'warnings', [])
        if status.next_uri is None:
            self._finished = True
        self._result = uniconnectResult(self, status.rows)
        return self._result

    def fetch(self):
        """Continue fetching data for the current query_id"""
        response = self._request.get(self._request.next_uri)
        status = self._request.process(response)
        if status.columns:
            self._columns = status.columns
        self._stats.update(status.stats)
        logger.debug(status)
        if status.next_uri is None:
            self._finished = True
        return status.rows

    def cancel(self):
        """Cancel the current query"""
        if self.query_id is None or self.is_finished():
            return
        self._cancelled = True
        url = self._request.get_url(('/v1/query/{}').format(self.query_id))
        logger.debug('cancelling query: %s', self.query_id)
        response = self._request.delete(url)
        logger.info(response)
        if response.status_code == requests.codes.no_content:
            logger.debug('query cancelled: %s', self.query_id)
            return
        else:
            self._request.raise_response_error(response)
            return

    def is_finished(self):
        return self._finished