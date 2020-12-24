# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/graphit/server.py
# Compiled at: 2010-03-28 16:45:42
import cgi, json, sqlite3, calendar
from urllib import unquote
from base64 import b64decode
from datetime import datetime, timedelta
from urlparse import urlparse, parse_qs
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class GraphItRequestHandler(BaseHTTPRequestHandler):
    """ Request handler for the GraphIT's http interface. """

    def do_GET(self):
        """ Callback called by integrated server on GET requests.
                        Get requests are used in GraphIT to get monitoring data
                        from server. """
        url_path = urlparse(self.path)
        path = [ unquote(x).decode('utf8') for x in url_path.path.strip('/').split('/')
               ]
        options = parse_qs(url_path.query)
        since = timedelta(seconds=3600)
        start = datetime.now()
        if 'since' in options:
            try:
                since = timedelta(seconds=int(options['since'][0]))
            except ValueError:
                self.send_error(400, 'since must be an integer')

        if 'start' in options:
            try:
                start = datetime.strptime(options['start'][0], '%Y%m%d%H%M%S')
            except ValueError:
                self.send_error(400, 'start must be a date with format : YYYYMMDDHHMMSS')

        if len(path) == 1 and path[0]:
            data = self.server._graphit_server.get_monitoring_data(set=path[0], start=start, since=since)
        elif len(path) == 2:
            data = self.server._graphit_server.get_monitoring_data(set=path[0], feed=path[1], start=start, since=since)
        else:
            self.send_error(400, '/$set$/ or /$set$/$feed$')
            return
        for f in data.values():
            for d in f:
                d[0] = self._to_js_timestamp(d[0])

        json_data = json.dumps(data)
        if 'callback' in options:
            json_data = '%s(%s)' % (options['callback'][0], json_data)
        self.send_response(200)
        self.send_header('Connection', 'close')
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(json_data))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.end_headers()
        self.wfile.write(json_data)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.send_header('Content-Length', '0')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

    def _authenticate(self):
        if 'authorization' in self.headers:
            (method, data) = self.headers.get('authorization').split(' ')
            if method == 'Basic':
                (login, passwd) = b64decode(data).split(':', 1)
                if self.server._settings.login == login and self.server._settings.passwd == passwd:
                    return True
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Basic realm="GraphIT"')
                self.end_headers()
                self.wfile.write('Authentication failure.')
                return False
            else:
                self.send_error(400, 'Method not implemented (basic http auth only).')
                return False
        else:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="GraphIT"')
            self.end_headers()
            self.wfile.write('Authentication failure.')
            return False

    def do_POST(self):
        """ Callback called by integrated server on POST requests.
                        Post requests are used in GraphIT by agents to update
                        monitoring data of server. """
        url_path = urlparse(self.path)
        path = [ unquote(x).decode('utf8').replace('%2F', '/') for x in url_path.path.strip('/').split('/')
               ]
        options = parse_qs(url_path.query)
        if self.server._graphit_server.need_auth():
            if not self._authenticate():
                return
        if len(path) == 2:
            request = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST', 
               'CONTENT_TYPE': self.headers['Content-Type']})
            if 'value' in request:
                try:
                    value = float(request['value'].value.decode('utf8'))
                except ValueError:
                    self.send_error(400, 'value must be a float.')
                    return

            else:
                self.send_error(400, 'value post data required.')
                return
            if 'unit' in request:
                unit = request['unit'].value.decode('utf8')
            else:
                unit = ''
            if 'date' in request:
                try:
                    date = datetime.strptime(request['date'].value, '%Y%m%d%H%M%S')
                except ValueError:
                    self.send_error(400, 'date must be a date with format : YYYYMMDDHHMMSS')
                    return

            else:
                date = datetime.now()
            data = self.server._graphit_server.insert_monitoring_data(set=path[0], feed=path[1], date=date, value=value, unit=unit)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('OK.\n')
        else:
            self.send_error(400, '/$set$/$feed$')
            return

    def _to_js_timestamp(self, date_time):
        return calendar.timegm(date_time.timetuple()) * 1000

    def log_message(self, format, *args):
        """ Callback used to log HTTP requests. """
        self.server._debug(format % args)


class GraphItHTTPServer(HTTPServer):
    """ Integrated web-server of GraphIT which is used to give data
                to web interface and to take monitoring data from agents. """

    def __init__(self, graphit_server, settings, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self._settings = settings
        self._graphit_server = graphit_server
        self._debug('Started web server on %s:%s' % args[0])

    def _debug(self, text):
        """ Print a debug message on STDOUT if verbose mode is
                        enabled. """
        if self._settings.verbose:
            print '[HTTP Server] %s' % text


class GraphItServer:

    def __init__(self, settings):
        self._settings = settings
        self._dbconn = None
        self._httpd = GraphItHTTPServer(self, self._settings, (
         self._settings.interface, self._settings.port), GraphItRequestHandler)
        return

    def init_db(self):
        """ Initialize database if it doesnt exists. """
        try:
            self._dbconn = sqlite3.connect(self._settings.database_file, detect_types=sqlite3.PARSE_DECLTYPES)
        except sqlite3.OperationalError, err:
            self._debug('Unable to open/create database : %s' % err)
        else:
            self._dbcursor = self._dbconn.cursor()
            self._dbcursor.execute('CREATE TABLE  IF NOT EXISTS "monitdata" ("id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_DATE, "set" VARCHAR NOT NULL , "feed" VARCHAR NOT NULL , "value" REAL NOT NULL , "unit" VARCHAR)')
            self._dbcursor.execute('CREATE INDEX IF NOT EXISTS "main"."idx" ON "monitdata" ("date" DESC, "set" ASC, "feed" ASC)')

    def serve_forever(self):
        self._httpd.serve_forever()

    def insert_monitoring_data(self, set, feed, value, unit, date=None):
        """ Insert a monitoring data into database. """
        if date is None:
            date = datetime.now()
        cursor = self._dbconn.cursor()
        cursor.execute('INSERT INTO monitdata VALUES (null, ?,?,?,?,?)', (
         date, set, feed, value, unit))
        self._debug('Adding %s/%s %s%s' % (set, feed, value, unit))
        self._dbconn.commit()
        return

    def get_monitoring_data(self, set, feed=None, since=None, start=None):
        """ Get monitoring data from database.
                
                         - set is the dataset to retrieve
                         - since is a timedelta which determine since when retrieve
                           data from `start`. 
                         - start is a datetime object used with since to calculate
                           date limit. """
        if start is None:
            start = datetime.now()
        sqlrequest = 'SELECT *\nFROM monitdata\nWHERE `set` = :set\n'
        if feed is not None:
            sqlrequest += 'AND feed = :feed\n'
        if since:
            date = start - since
            sqlrequest += 'AND `date` > :date\n'
        else:
            date = None
        sqlrequest += 'ORDER BY date ASC\n'
        cursor = self._dbconn.cursor()
        cursor.execute(sqlrequest, {'set': set, 'date': date, 'feed': feed})
        feeds = {}
        for (id, date, set, feed, value, unit) in cursor:
            if feed not in feeds:
                feeds[feed] = []
            feeds[feed].append([date, value, unit])

        return feeds

    def need_auth(self):
        """ Return True if authentication is required. """
        return bool(self._settings.login is not None and self._settings.passwd is not None)

    def _debug(self, text):
        """ Print a debug message on STDOUT if verbose mode is 
                        enabled """
        if self._settings.verbose:
            print '[Server] %s' % text


if __name__ == '__main__':

    class Settings:
        database_file = '/tmp/test2.db'
        verbose = True
        interface = '0.0.0.0'
        port = 8081


    s = GraphItServer(Settings())
    s.init_db()