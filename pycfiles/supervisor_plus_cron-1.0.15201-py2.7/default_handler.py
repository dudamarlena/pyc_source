# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\medusa\default_handler.py
# Compiled at: 2015-07-18 10:13:56
RCS_ID = '$Id: default_handler.py,v 1.8 2002/08/01 18:15:45 akuchling Exp $'
import mimetypes, re, stat, supervisor.medusa.http_date as http_date, supervisor.medusa.http_server as http_server, supervisor.medusa.producers as producers
from supervisor.medusa.util import html_repr
unquote = http_server.unquote
from supervisor.medusa.counter import counter

class default_handler:
    valid_commands = [
     'GET', 'HEAD']
    IDENT = 'Default HTTP Request Handler'
    directory_defaults = [
     'index.html',
     'default.html']
    default_file_producer = producers.file_producer

    def __init__(self, filesystem):
        self.filesystem = filesystem
        self.hit_counter = counter()
        self.file_counter = counter()
        self.cache_counter = counter()

    hit_counter = 0

    def __repr__(self):
        return '<%s (%s hits) at %x>' % (
         self.IDENT,
         self.hit_counter,
         id(self))

    def match(self, request):
        return 1

    def handle_request(self, request):
        if request.command not in self.valid_commands:
            request.error(400)
            return
        self.hit_counter.increment()
        path, params, query, fragment = request.split_uri()
        if '%' in path:
            path = unquote(path)
        while path and path[0] == '/':
            path = path[1:]

        if self.filesystem.isdir(path):
            if path and path[(-1)] != '/':
                request['Location'] = 'http://%s/%s/' % (
                 request.channel.server.server_name,
                 path)
                request.error(301)
                return
            found = 0
            if path and path[(-1)] != '/':
                path += '/'
            for default in self.directory_defaults:
                p = path + default
                if self.filesystem.isfile(p):
                    path = p
                    found = 1
                    break

            if not found:
                request.error(404)
                return
        elif not self.filesystem.isfile(path):
            request.error(404)
            return
        file_length = self.filesystem.stat(path)[stat.ST_SIZE]
        ims = get_header_match(IF_MODIFIED_SINCE, request.header)
        length_match = 1
        if ims:
            length = ims.group(4)
            if length:
                try:
                    length = int(length)
                    if length != file_length:
                        length_match = 0
                except:
                    pass

        ims_date = 0
        if ims:
            ims_date = http_date.parse_http_date(ims.group(1))
        try:
            mtime = self.filesystem.stat(path)[stat.ST_MTIME]
        except:
            request.error(404)
            return

        if length_match and ims_date:
            if mtime <= ims_date:
                request.reply_code = 304
                request.done()
                self.cache_counter.increment()
                return
        try:
            file = self.filesystem.open(path, 'rb')
        except IOError:
            request.error(404)
            return

        request['Last-Modified'] = http_date.build_http_date(mtime)
        request['Content-Length'] = file_length
        self.set_content_type(path, request)
        if request.command == 'GET':
            request.push(self.default_file_producer(file))
        self.file_counter.increment()
        request.done()

    def set_content_type(self, path, request):
        typ, encoding = mimetypes.guess_type(path)
        if typ is not None:
            request['Content-Type'] = typ
        else:
            request['Content-Type'] = 'text/plain'
        return

    def status(self):
        return producers.simple_producer('<li>%s' % html_repr(self) + '<ul>' + '  <li><b>Total Hits:</b> %s' % self.hit_counter + '  <li><b>Files Delivered:</b> %s' % self.file_counter + '  <li><b>Cache Hits:</b> %s' % self.cache_counter + '</ul>')


IF_MODIFIED_SINCE = re.compile('If-Modified-Since: ([^;]+)((; length=([0-9]+)$)|$)', re.IGNORECASE)
USER_AGENT = re.compile('User-Agent: (.*)', re.IGNORECASE)
CONTENT_TYPE = re.compile("Content-Type: ([^;]+)((; boundary=([A-Za-z0-9\\'\\(\\)+_,./:=?-]+)$)|$)", re.IGNORECASE)
get_header = http_server.get_header
get_header_match = http_server.get_header_match

def get_extension(path):
    dirsep = path.rfind('/')
    dotsep = path.rfind('.')
    if dotsep > dirsep:
        return path[dotsep + 1:]
    else:
        return ''