# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ll/nightshade.py
# Compiled at: 2009-03-09 12:01:05
"""
This module provides a class :class:`Call` that allows you to use Oracle PL/SQL
procedures/functions as CherryPy__ response handlers. A :class:`Call` objects
wraps a :class:`ll.orasql.Procedure` or :class:`ll.orasql.Function` object from
the :mod:`ll.orasql` module.

__ http://www.cherrypy.org/

For example, you might have the following PL/SQL function::

        create or replace function helloworld
        (
                who varchar2
        )
        return varchar2
        as
        begin
                return '<html><head><h>Hello ' || who || '</h></head><body><h1>Hello, ' || who || '!</h1></body></html>';
        end;

Using this function as a CherryPy response handler can be done like this::

        import cherrypy

        from ll import orasql, nightshade

        proc = nightshade.Call(orasql.Function("helloworld"), connectstring="user/pwd")

        class HelloWorld(object):
                @cherrypy.expose
                def default(self, who="World"):
                        cherrypy.response.headers["Content-Type"] = "text/html"
                        return proc(who=who)

        cherrypy.quickstart(HelloWorld())
"""
import time, datetime, threading, cherrypy
from ll import orasql
__docformat__ = 'reStructuredText'
weekdayname = [
 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

class UTC(datetime.tzinfo):
    """
        Timezone object for UTC
        """

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'


utc = UTC()

def getnow():
    """
        Get the current date and time as a :class:`datetime.datetime` object in UTC
        with timezone info.
        """
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def httpdate(dt):
    """
        Return a string suitable for a "Last-Modified" and "Expires" header.
        
        :var:`dt` is a :class:`datetime.datetime` object. If ``:var:`dt`.tzinfo`` is
        :const:`None` :var:`dt` is assumed to be in the local timezone (using the
        current UTC offset which might be different from the one used by :var:`dt`).
        """
    if dt.tzinfo is None:
        dt += datetime.timedelta(seconds=[time.timezone, time.altzone][time.daylight])
    else:
        dt -= dt.tzinfo.utcoffset(dt)
    return '%s, %02d %3s %4d %02d:%02d:%02d GMT' % (weekdayname[dt.weekday()], dt.day, monthname[dt.month], dt.year, dt.hour, dt.minute, dt.second)


class Connect(object):
    """
        :class:`Connect` objects can be used as decorators that wraps a function
        that needs a database connection.
        
        If calling the wrapped function results in a database exception that has
        been caused by a lost connection to the database or similar problems,
        the function is retried with a new database connection.
        """
    _badoracleexceptions = set((28, 1012, 1014, 1033, 1034, 1035, 1089, 1090, 1092,
                                3106, 3113, 3114, 3135, 12154, 12540, 12541, 12543))

    def __init__(self, connectstring=None, pool=None, retry=3, **kwargs):
        """
                Create a new parameterized :class:`Connect` decorator. Either
                :var:`connectstring` or :var:`pool` (a database pool object) must be
                specified. :var:`retry` specifies how often to retry calling the wrapped
                function after a database exception. :var:`kwargs` will be passed on to
                the :func:`connect` call.
                """
        if (connectstring is not None) == (pool is not None):
            raise TypeError('either connectstring or pool must be specified')
        self.pool = pool
        self._connection = None
        self.connectstring = connectstring
        self.retry = retry
        self.kwargs = kwargs
        return

    def _isbadoracleexception(self, exc):
        if exc.args:
            code = getattr(exc[0], 'code', 0)
            if code in self._badoracleexceptions:
                return True
        return False

    def _getconnection(self):
        if self.pool is not None:
            return self.pool.acquire()
        elif self._connection is None:
            self._connection = orasql.connect(self.connectstring, threaded=True, **self.kwargs)
        return self._connection

    def _dropconnection(self, connection):
        if self.pool is not None:
            self.pool.drop(connection)
        else:
            self._connection = None
        return

    def cursor(self, **kwargs):
        connection = self._getconnection()
        return connection.cursor(**kwargs)

    def commit(self):
        self._getconnection().commit()

    def rollback(self):
        self._getconnection().rollback()

    def close(self):
        connection = self._getconnection()
        connection.close()
        self._dropconnection(connection)

    def cancel(self):
        self._getconnection().cancel()

    def __call__(self, func):

        def wrapper(*args, **kwargs):
            for i in xrange(self.retry):
                connection = self._getconnection()
                try:
                    return func(*args, **kwargs)
                except orasql.DatabaseError, exc:
                    if i < self.retry - 1 and self._isbadoracleexception(exc):
                        self._dropconnection(connection)
                    else:
                        raise

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__dict__.update(func.__dict__)
        return wrapper


class Call(object):
    """
        Wrap an Oracle procedure or function in a CherryPy handler.

        A :class:`Call` object wraps a procedure or function object from
        :mod:`ll.orasql` and makes it callable just like a CherryPy handler.
        """

    def __init__(self, callable, connection):
        """
                Create a :class:`Call` object wrapping the function or procedure
                :var:`callable`.
                """
        self.callable = callable
        self.connection = connection
        callable._calcargs(connection.cursor())

    def __call__(self, *args, **kwargs):
        """
                Call the procedure/function with the arguments :var:`args` and
                :var:`kwargs` mapping Python function arguments to
                Oracle procedure/function arguments. On return from the procedure the
                :var:`c_out` parameter is mapped to the CherryPy response body, and the
                parameters :var:`p_expires` (the number of days from now),
                :var:`p_lastmodified` (a date in UTC), :var:`p_mimetype`: (a string),
                :var:`p_encoding` (a string), :var:`p_etag` (a string) and
                :var:`p_cachecontrol` (a string) are mapped to the appropriate CherryPy
                response headers. If :var:`p_etag` is not specified a value is calculated.
        
                If the procedure/function raised a PL/SQL exception with a code between
                20200 and 20599, 20000 will be substracted from this value and the
                resulting value will be used as the HTTP response code, i.e. 20404 will
                give a "Not Found" response.
                """

        @self.connection
        def call(*args, **kwargs):
            cursor = self.connection.cursor()
            try:
                if isinstance(self.callable, orasql.Procedure):
                    result = (
                     None, self.callable(cursor, *args, **kwargs))
                else:
                    result = self.callable(cursor, *args, **kwargs)
                cursor.connection.commit()
                return result
            except orasql.DatabaseError, exc:
                if exc.args:
                    code = getattr(exc[0], 'code', 0)
                    if 20200 <= code <= 20599:
                        raise cherrypy.HTTPError(code - 20000)
                    else:
                        raise

            return

        now = getnow()
        (body, result) = call(*args, **kwargs)
        expires = result.get('p_expires', None)
        if expires is not None:
            cherrypy.response.headers['Expires'] = httpdate(now + datetime.timedelta(days=expires))
        lastmodified = result.get('p_lastmodified', None)
        if lastmodified is not None:
            cherrypy.response.headers['Last-Modified'] = httpdate(lastmodified)
        encoding = None
        if isinstance(result, unicode):
            encoding = 'utf-8'
            result = result.encoding(encoding)
        mimetype = result.get('p_mimetype', None)
        if mimetype is not None:
            if encoding is None:
                encoding = result.get('p_encoding', None)
            if encoding is not None:
                cherrypy.response.headers['Content-Type'] = '%s; charset=%s' % (mimetype, encoding)
            else:
                cherrypy.response.headers['Content-Type'] = mimetype
        hasetag = False
        etag = result.get('p_etag', None)
        if etag is not None:
            cherrypy.response.headers['ETag'] = etag
            hasetag = True
        cachecontrol = result.get('p_cachecontrol', None)
        if cachecontrol is not None:
            cherrypy.response.headers['Cache-Control'] = cachecontrol
        status = result.get('p_status', None)
        if status is not None:
            cherrypy.response.status = status
        if 'c_out' in result:
            body = result.c_out
            if hasattr(result, 'read'):
                result = result.read()
            if not hasetag:
                cherrypy.response.headers['ETag'] = '"%x"' % hash(body)
        if hasattr(body, 'read'):
            body = body.read()
        return body