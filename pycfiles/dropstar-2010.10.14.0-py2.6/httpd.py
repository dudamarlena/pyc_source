# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dropstar/httpd.py
# Compiled at: 2010-10-14 14:04:21
"""
httpd

Handles all HTTP requests, GET only.  It is intended to be READ only.

Use RPC for doing interaction with the backend, doing this inside a web
rendering request is a total pain in the ass and has all kinds of times
you'd like to have some feature you dont, and this isnt an end-user
oriented service, so is it assumed their JS will be working and can
submit any data we need them to.  Code accordingly for best results.

When querying Cloud data from the Site Control API, we will always get the
cached version, so that web requests are fast.  This is not the place we need
to wait on data.

NOTE(g): I left this a single threaded HTTP server because the requests should
be infrequent enough and fast enough that even "heavy" usage of this server
should not back up.  It's an admin tool.

TODO(g): Clean this file up, break into other modules to separate and harden
    the individual tasks.  Things are working and stable now, so time to harden.
"""
import sys, time, mimetools, re, BaseHTTPServer, SocketServer, SimpleXMLRPCServer, urlparse, cgi, string, Cookie, socket, sys, os, urllib, traceback, threading, select, jsonlib, logging
from unidist.log import log
from unidist import error_info
from unidist import sharedlock
from procblock import processing
from procblock import procyaml
import process
MOUNT_HTTP_PATH_DEFAULT = '/'

def parse_multipart(fp, pdict):
    """Parse multipart input.
    
    Arguments:
    fp   : input file
    pdict: dictionary containing other parameters of content-type header
    
    Returns a dictionary just like parse_qs(): keys are the field names, each
    value is a list of values for that field.  This is easy to use but not
    much good if you are expecting megabytes to be uploaded -- in that case,
    use the FieldStorage class instead which is much more flexible.  Note
    that content-type is the raw, unparsed contents of the content-type
    header.
    
    XXX This does not parse nested multipart parts -- use FieldStorage for
    that.
    
    XXX This should really be subsumed by FieldStorage altogether -- no
    point in having two implementations of the same parsing algorithm.
    
    """
    boundary = ''
    if 'boundary' in pdict:
        boundary = pdict['boundary']
    if not cgi.valid_boundary(boundary):
        raise ValueError, 'Invalid boundary in multipart form: %r' % (
         boundary,)
    nextpart = '--' + boundary
    lastpart = '--' + boundary + '--'
    partdict = {}
    terminator = ''
    while terminator != lastpart:
        bytes = -1
        data = None
        if terminator:
            headers = mimetools.Message(fp)
            filename_result = re.findall('filename="(.*?)"', str(headers))
            if filename_result:
                filename_result = filename_result[0]
                if len(filename_result) > 2 and filename_result[1] == ':':
                    filename_result = filename_result[2:]
                filename_result = filename_result.replace('\\', '/')
                filename_result = os.path.basename(filename_result)
                partdict['_filename'] = [
                 filename_result]
            clength = headers.getheader('content-length')
            if clength:
                try:
                    bytes = int(clength)
                except ValueError:
                    pass

            if bytes > 0:
                if maxlen and bytes > maxlen:
                    raise ValueError, 'Maximum content length exceeded'
                data = fp.read(bytes)
            else:
                data = ''
        lines = []
        while 1:
            line = fp.readline()
            if not line:
                terminator = lastpart
                break
            if line[:2] == '--':
                terminator = line.strip()
                if terminator in (nextpart, lastpart):
                    break
            lines.append(line)

        if data is None:
            continue
        if bytes < 0:
            if lines:
                line = lines[(-1)]
                if line[-2:] == '\r\n':
                    line = line[:-2]
                elif line[-1:] == '\n':
                    line = line[:-1]
                lines[-1] = line
                data = ('').join(lines)
        line = headers['content-disposition']
        if not line:
            continue
        (key, params) = cgi.parse_header(line)
        if key != 'form-data':
            continue
        if 'name' in params:
            name = params['name']
        else:
            continue
        if name in partdict:
            partdict[name].append(data)
        else:
            partdict[name] = [
             data]

    return partdict


def CGIArgsToDict(args):
    """Convert our args string into a dictionary."""
    data = {}
    for item in args.split('&'):
        if '=' in item:
            (key, value) = item.split('=', 1)
            key = urllib.unquote(key.replace('+', ' '))
            if not key.endswith('[]'):
                data[key] = urllib.unquote(value.replace('+', ' '))
            else:
                key_name = key[:-2]
                if key_name not in data:
                    data[key_name] = []
                value = urllib.unquote(value.replace('+', ' '))
                data[key_name].append(value)

    return data


def UriParse(uri):
    """We want to parse the URI into a path and argument section.  Return tuple.
  
  Python's urlparse module fails on more complex data, such as sending Python
  code across the line.  It crops our data, breaking the submit, so we must do
  this ourselves.
  
  Args:
    uri: string, uri (url, minus the protocol and host name)
  
  Returns: tuple (path, args).  Both strings.
  """
    if '?' in uri:
        (path, args) = uri.split('?', 1)
    else:
        path, args = uri, ''
    return (path, args)


class HttpdThread(threading.Thread):
    """HTTP Listener Thread"""

    def __init__(self, port, port_sites, conf):
        self.port = port
        self.port_sites = port_sites
        self.conf = conf
        self.server = None
        self.fd_server = None
        log('Starting HTTP Listener: %s' % port, logging.INFO)
        threading.Thread.__init__(self)
        return

    def run(self):
        """Once start() is called, this function is executed, which is the thread's
    run function.
    """
        self.server = BaseHTTPServer.HTTPServer(('0.0.0.0', self.port), HTTPRequest)
        self.fd_server = self.server.fileno()
        self.server.sites = self.port_sites
        self.server.conf = self.conf
        while sharedlock.IsLocked('__running'):
            try:
                (wait_in, wait_out, wait_err) = select.select([self.fd_server], [self.fd_server], [], 0)
                if self.fd_server in wait_in or self.fd_server in wait_out:
                    self.server.handle_request()
                time.sleep(0.001)
            except Exception, e:
                exception_output = traceback.format_exc()
                log('HttpdThread: Unhandled exception:\n%s' % exception_output, logging.ERROR)

        log('HTTP Listener (%s): Finished' % self.port, logging.INFO)


class HTTPRequest(BaseHTTPServer.BaseHTTPRequestHandler):
    """HTTP Request handler."""

    def do_GET(self):
        path = self.path
        (path, args) = UriParse(path)
        path = path[1:]
        args = CGIArgsToDict(args)
        try:
            self.handle_everything(path, args)
        except:
            text = error_info.GetExceptionDetails()
            log(text, logging.ERROR)

    def do_POST(self):
        path = self.path
        (_, _, path, _, args, _) = urlparse.urlparse(path)
        path = path[1:]
        (ctype, pdict) = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'application/x-www-form-urlencoded':
            clen = self.headers.getheader('content-length')
            if clen:
                clen = string.atoi(clen)
            data = self.rfile.read(clen)
            self.path = '%s?%s' % (self.path, data)
            self.do_GET()
            return
        if ctype == 'multipart/form-data':
            query = parse_multipart(self.rfile, pdict)
            args = {}
            for key in query:
                args[key] = query[key][0]

            try:
                self.handle_everything(path, args)
            except Exception, e:
                text = GetExceptionDetails()
                log.critical(text)
                print text

            return
        log('Uncaught POST error', logging.CRITICAL)

    def handle_everything(self, path, args):
        write_cookies = {}
        write_headers = {}
        cookies = {}
        if self.headers.has_key('Cookie'):
            cookie = Cookie.SimpleCookie(self.headers['Cookie'])
            for name in cookie:
                cookies[name] = cookie[name].value

        if self.headers.has_key('X-Forwarded-Host'):
            host_header = self.headers['X-Forwarded-Host']
        elif self.headers.has_key('Host'):
            host_header = self.headers['Host']
            if ':' in host_header:
                host_header = host_header.split(':')[0]
        else:
            host_header = None
        output = ''
        content_type = 'text/html'
        response_code = 400
        start_time = time.time()
        try:
            (output, content_type, response_code, redirect_url, write_cookies, write_headers) = self.RenderRequest(path, self.headers, cookies, args)
        except Exception, e:
            details = error_info.GetExceptionDetails()
            log('%s' % details, logging.ERROR)
            output = details.replace('\n', '<br>\n')
            content_type = 'text/html'
            response_code = 500

        self.send_response(response_code)
        self.send_header('Content-type', content_type)
        for name in write_cookies:
            self.send_header('Set-Cookie', '%s="%s"; Path=/' % (name,
             write_cookies[name]))

        for name in write_headers:
            self.send_header(name, write_headers[name])

        self.end_headers()
        self.wfile.write(output)
        duration = time.time() - start_time
        return

    def RenderRequest(self, path, headers, cookies, args):
        output = ''
        content_type = 'text/html'
        response_code = 200
        redirect_url = None
        write_cookies = {}
        write_headers = {}
        host = None
        port = None
        if 'host' in headers:
            if ':' in headers['host']:
                (host, port) = headers['host'].split(':', 1)
                port = int(port)
            else:
                host = headers['host']
        site_conf = process.GetSiteConf(self.server.sites, host)
        if site_conf == None:
            raise Exception('No site found for host: %s: %s' % (host, self.server.conf.keys()))
        if 'packages' not in site_conf:
            raise Exception('"packages" not in site conf: %s' % site_conf)
        for package in site_conf['packages']:
            package_block = procyaml.ImportYaml(package['path'])
            if 'mount' in package:
                http_path = package['mount']
            else:
                http_path = MOUNT_HTTP_PATH_DEFAULT
            if 'mount rpc' in package:
                rpc_path = package['mount rpc']
            else:
                rpc_path = '%srpc/' % http_path
            if 'static' in package_block and 'path' in package_block['static']:
                static_file_path = package_block['static']['path']
            else:
                static_file_path = None
            output = None
            test_path = '/%s' % path
            if 'http' in package_block:
                for (page_name, page) in package_block['http'].items():
                    page_mount = '%s%s' % (http_path, page_name)
                    if test_path == page_mount:
                        log('Found page: %s' % page)
                        log('Getting results procblock: "%s": %s' % (page_name, page.keys()))
                        pipe_data_input = dict(args)
                        pipe_data_input['render'] = 'True'
                        request_state_input = {'headers': headers, 'cookies': cookies, 'path': path, 'args': args, 'host': host, 'port': port, 'protocol': 'http', 'page': page_name, 'page_mount': page_mount, 'package': package}
                        render_out = processing.Process(pipe_data_input, page, request_state_input, args, tag=None, cwd=None, env=None, block_parent=None)
                        try:
                            output = render_out['template']
                        except KeyError, e:
                            output = render_out['run']['template']

            else:
                log('No "http" section in site_conf: %s' % site_conf.keys(), logging.WARN)
            if output == None and 'rpc' in package_block:
                for (rpc_name, rpc) in package_block['rpc'].items():
                    rpc_mount = '%s%s' % (rpc_path, rpc_name)
                    if test_path == rpc_mount:
                        log('Found RPC Function: %s: Args: %s' % (rpc, args))
                        log('Getting results procblock: "%s": %s' % (rpc_name, rpc.keys()))
                        pipe_data_input = dict(args)
                        pipe_data_input['render'] = 'True'
                        request_state_input = {'headers': headers, 'cookies': cookies, 'path': path, 'args': args, 'host': host, 'port': port, 'protocol': 'rpc', 'rpc': rpc_name, 'rpc_mount': rpc_mount, 'package': package}
                        render_out = processing.Process(pipe_data_input, rpc, request_state_input, args, tag=None, cwd=None, env=None, block_parent=None)
                        run_output = render_out['run']
                        del run_output['render']
                        del run_output['__start_time']
                        if '__duration' in run_output:
                            del run_output['__duration']
                        json_result = jsonlib.write(run_output)
                        output = json_result.replace('",""]', '"]')

            if output == None and static_file_path != None:
                remaining_path = path[len(http_path) - 1:]
                static_file = '%s%s' % (static_file_path, remaining_path)
                if os.path.exists(static_file):
                    file_flag = 'rb'
                    if path.lower().endswith('.png'):
                        content_type = 'image/png'
                    elif path.lower().endswith('.jpg'):
                        content_type = 'image/jpg'
                    elif path.lower().endswith('.bmp'):
                        content_type = 'image/bmp'
                    elif path.lower().endswith('.gif'):
                        content_type = 'image/gif'
                    elif path.lower().endswith('.css'):
                        content_type = 'text/css'
                        file_flag = 'r'
                    elif path.lower().endswith('.js') or path.split('.')[(-1)] in ('txt',
                                                                                   'html'):
                        content_type = 'text/html'
                        file_flag = 'r'
                    if os.path.isfile(static_file):
                        fp = open(static_file, file_flag)
                        output = fp.read()
                        fp.close()
                    else:
                        log('Tried to read a directory: %s' % static_file)
                        output = ''
            return (
             output, content_type, response_code, redirect_url, write_cookies,
             write_headers)

        return