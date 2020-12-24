# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/daemon.py
# Compiled at: 2015-10-11 07:17:06
import os, sys, BaseHTTPServer, json, urllib2, logging, time, traceback
from dbmanagr.jsonable import Jsonable, as_json
from dbmanagr.utils import mute_stderr
logger = logging.getLogger(__name__)

class Encoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Jsonable):
            return obj.as_json()
        return as_json(obj)


class DaemonHTTPServer(BaseHTTPServer.HTTPServer):

    def __init__(self, *args, **kwargs):
        BaseHTTPServer.HTTPServer.__init__(self, *args, **kwargs)
        self.active = True

    def serve_forever(self, poll_interval=0.5):
        while self.active:
            self.handle_request()


class DaemonHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        from dbmanagr.command import navigator, exporter, differ, executer
        from dbmanagr.command import grapher
        commands = {'navigator': navigator, 
           'exporter': exporter, 
           'differ': differ, 
           'executer': executer, 
           'grapher': grapher}
        parts = self.path.split('/')
        command = parts[1]
        if command == 'server-status':
            self.send_response(200)
            self.end_headers()
            return
        if command == 'server-stop':
            self.send_response(200)
            self.end_headers()
            self.server.active = False
            return
        if command not in commands:
            self.send_error(404)
            return
        args = json.loads(self.rfile.read(int(self.headers.getheader('content-length'))))
        try:
            items = mute_stderr(commands[command].execute)(args)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(items, cls=Encoder))
        except BaseException as e:
            logger.debug(e)
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'__cls__': str(e.__class__.__name__), 
               'message': e.message, 
               'traceback': as_json(traceback.extract_tb(sys.exc_info()[2]))}))

    def log_message(self, format_, *args):
        logger.info(format_, args)


def is_running(config):
    try:
        urllib2.urlopen(('http://{host}:{port}/server-status').format(host=config.host, port=config.port), '')
    except BaseException:
        return False

    return True


def start_server(config):
    try:
        httpd = DaemonHTTPServer((
         config.host, config.port), DaemonHTTPRequestHandler)
        if os.fork() == 0:
            httpd.serve_forever()
            sys.exit(0)
        return True
    except BaseException:
        pass

    return False


def start(config):
    sys.stdout.write('Starting server... ')
    if start_server(config):
        sys.stdout.write('OK\n')
    else:
        sys.stdout.write('already running\n')


def stop(config):
    sys.stdout.write('Stopping server... ')
    try:
        urllib2.urlopen(('http://{host}:{port}/server-stop').format(host=config.host, port=config.port), '')
    except BaseException:
        sys.stdout.write('failed\n')
    else:
        sys.stdout.write('OK\n')


def restart(config):
    stop(config)
    time.sleep(1)
    start(config)


def status(config):
    if is_running(config):
        sys.stdout.write('Status: online\n')
    else:
        sys.stdout.write('Status: offline\n')