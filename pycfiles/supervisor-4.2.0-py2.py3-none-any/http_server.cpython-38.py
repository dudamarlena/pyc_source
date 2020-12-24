# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/http_server.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 29555 bytes
RCS_ID = '$Id: http_server.py,v 1.12 2004/04/21 15:11:44 akuchling Exp $'
import re, socket, sys, time
from supervisor.compat import as_bytes
import supervisor.medusa.asyncore_25 as asyncore
import supervisor.medusa.asynchat_25 as asynchat
import supervisor.medusa.http_date as http_date
import supervisor.medusa.producers as producers
import supervisor.medusa.logger as logger
VERSION_STRING = RCS_ID.split()[2]
import supervisor.medusa.counter as counter
try:
    from urllib import unquote, splitquery
except ImportError:
    from urllib.parse import unquote, splitquery
else:

    class http_request:
        reply_code = 200
        request_counter = counter()
        use_chunked = 1
        collector = None

        def __init__(self, *args):
            self.channel, self.request, self.command, self.uri, self.version, self.header = args
            self.outgoing = []
            self.reply_headers = {'Server':'Medusa/%s' % VERSION_STRING, 
             'Date':http_date.build_http_date(time.time())}
            self._http_request__reply_header_list = []
            self.request_number = http_request.request_counter.increment()
            self._split_uri = None
            self._header_cache = {}

        def __setitem__(self, key, value):
            self.reply_headers[key] = value

        def __getitem__(self, key):
            return self.reply_headers[key]

        def __contains__(self, key):
            return key in self.reply_headers

        def has_key(self, key):
            return key in self.reply_headers

        def build_reply_header(self):
            header_items = ['%s: %s' % item for item in self.reply_headers.items()]
            result = '\r\n'.join([
             self.response(self.reply_code)] + header_items) + '\r\n\r\n'
            return as_bytes(result)

        def add_header(self, name, value):
            """ Adds a header to the reply headers """
            self._http_request__reply_header_list.append((name, value))

        def clear_headers(self):
            """ Clears the reply header list """
            self.reply_headers.clear()
            self._http_request__reply_header_list[:] = []

        def remove_header(self, name, value=None):
            """ Removes the specified header.
        If a value is provided, the name and
        value must match to remove the header.
        If the value is None, removes all headers
        with that name."""
            found_it = 0
            if name in self.reply_headers and not value is None:
                if self.reply_headers[name] == value:
                    del self.reply_headers[name]
                    found_it = 1
            else:
                removed_headers = []
                if value is not None:
                    if (
                     name, value) in self._http_request__reply_header_list:
                        removed_headers = [
                         (
                          name, value)]
                        found_it = 1
                else:
                    for h in self._http_request__reply_header_list:
                        if h[0] == name:
                            removed_headers.append(h)
                            found_it = 1

            if not found_it:
                if value is None:
                    search_value = '%s' % name
                else:
                    search_value = '%s: %s' % (name, value)
                raise LookupError("Header '%s' not found" % search_value)
            for h in removed_headers:
                self._http_request__reply_header_list.remove(h)

        def get_reply_headers(self):
            """ Get the tuple of headers that will be used
        for generating reply headers"""
            header_tuples = self._http_request__reply_header_list[:]
            header_names = [n for n, v in header_tuples]
            for n, v in self.reply_headers.items():
                if n not in header_names:
                    header_tuples.append((n, v))
                    header_names.append(n)
                return header_tuples

        def get_reply_header_text(self):
            """ Gets the reply header (including status and
        additional crlf)"""
            header_tuples = self.get_reply_headers()
            headers = [
             self.response(self.reply_code)]
            headers += ['%s: %s' % h for h in header_tuples]
            return '\r\n'.join(headers) + '\r\n\r\n'

        path_regex = re.compile('([^;?#]*)(;[^?#]*)?(\\?[^#]*)?(#.*)?')

        def split_uri(self):
            if self._split_uri is None:
                m = self.path_regex.match(self.uri)
                if m.end() != len(self.uri):
                    raise ValueError('Broken URI')
                else:
                    self._split_uri = m.groups()
            return self._split_uri

        def get_header_with_regex(self, head_reg, group):
            for line in self.header:
                m = head_reg.match(line)
                if m.end() == len(line):
                    return m.group(group)
                return ''

        def get_header(self, header):
            header = header.lower()
            hc = self._header_cache
            if header not in hc:
                h = header + ': '
                hl = len(h)
                for line in self.header:
                    if line[:hl].lower() == h:
                        r = line[hl:]
                        hc[header] = r
                        return r
                    hc[header] = None
                    return

            return hc[header]

        def collect_incoming_data(self, data):
            if self.collector:
                self.collector.collect_incoming_data(data)
            else:
                self.log_info('Dropping %d bytes of incoming request data' % len(data), 'warning')

        def found_terminator(self):
            if self.collector:
                self.collector.found_terminator()
            else:
                self.log_info('Unexpected end-of-record for incoming request', 'warning')

        def push(self, thing):
            if isinstance(thing, str):
                thing = as_bytes(thing)
            if isinstance(thing, bytes):
                thing = producers.simple_producer(thing, buffer_size=(len(thing)))
            self.outgoing.append(thing)

        def response(self, code=200):
            message = self.responses[code]
            self.reply_code = code
            return 'HTTP/%s %d %s' % (self.version, code, message)

        def error(self, code):
            self.reply_code = code
            message = self.responses[code]
            s = self.DEFAULT_ERROR_MESSAGE % {'code':code, 
             'message':message}
            s = as_bytes(s)
            self['Content-Length'] = len(s)
            self['Content-Type'] = 'text/html'
            self.push(s)
            self.done()

        reply_now = error

        def done(self):
            """finalize this transaction - send output to the http channel"""
            connection = get_header(CONNECTION, self.header).lower()
            close_it = 0
            wrap_in_chunking = 0
            if self.version == '1.0':
                if connection == 'keep-alive':
                    if 'Content-Length' not in self:
                        close_it = 1
                    else:
                        self['Connection'] = 'Keep-Alive'
                else:
                    close_it = 1
            elif self.version == '1.1':
                if connection == 'close':
                    close_it = 1
                elif 'Content-Length' not in self:
                    if 'Transfer-Encoding' in self:
                        if not self['Transfer-Encoding'] == 'chunked':
                            close_it = 1
                        elif self.use_chunked:
                            self['Transfer-Encoding'] = 'chunked'
                            wrap_in_chunking = 1
                    else:
                        close_it = 1
            elif self.version is None:
                close_it = 1
            outgoing_header = producers.simple_producer(self.get_reply_header_text())
            if close_it:
                self['Connection'] = 'close'
            elif wrap_in_chunking:
                outgoing_producer = producers.chunked_producer(producers.composite_producer(self.outgoing))
                outgoing_producer = producers.composite_producer([
                 outgoing_header, outgoing_producer])
            else:
                self.outgoing.insert(0, outgoing_header)
                outgoing_producer = producers.composite_producer(self.outgoing)
            self.channel.push_with_producer(producers.globbing_producer(producers.hooked_producer(outgoing_producer, self.log)))
            self.channel.current_request = None
            if close_it:
                self.channel.close_when_done()

        def log_date_string(self, when):
            gmt = time.gmtime(when)
            if time.daylight:
                if gmt[8]:
                    tz = time.altzone
                else:
                    tz = time.timezone
            else:
                if tz > 0:
                    neg = 1
                else:
                    neg = 0
                    tz = -tz
                h, rem = divmod(tz, 3600)
                m, rem = divmod(rem, 60)
                if neg:
                    offset = '-%02d%02d' % (h, m)
                else:
                    offset = '+%02d%02d' % (h, m)
            return time.strftime('%d/%b/%Y:%H:%M:%S ', gmt) + offset

        def log(self, bytes):
            self.channel.server.logger.log(self.channel.addr[0], '%d - - [%s] "%s" %d %d\n' % (
             self.channel.addr[1],
             self.log_date_string(time.time()),
             self.request,
             self.reply_code,
             bytes))

        responses = {100:'Continue', 
         101:'Switching Protocols', 
         200:'OK', 
         201:'Created', 
         202:'Accepted', 
         203:'Non-Authoritative Information', 
         204:'No Content', 
         205:'Reset Content', 
         206:'Partial Content', 
         300:'Multiple Choices', 
         301:'Moved Permanently', 
         302:'Moved Temporarily', 
         303:'See Other', 
         304:'Not Modified', 
         305:'Use Proxy', 
         400:'Bad Request', 
         401:'Unauthorized', 
         402:'Payment Required', 
         403:'Forbidden', 
         404:'Not Found', 
         405:'Method Not Allowed', 
         406:'Not Acceptable', 
         407:'Proxy Authentication Required', 
         408:'Request Time-out', 
         409:'Conflict', 
         410:'Gone', 
         411:'Length Required', 
         412:'Precondition Failed', 
         413:'Request Entity Too Large', 
         414:'Request-URI Too Large', 
         415:'Unsupported Media Type', 
         500:'Internal Server Error', 
         501:'Not Implemented', 
         502:'Bad Gateway', 
         503:'Service Unavailable', 
         504:'Gateway Time-out', 
         505:'HTTP Version not supported'}
        DEFAULT_ERROR_MESSAGE = '\r\n'.join(('<head>', '<title>Error response</title>',
                                             '</head>', '<body>', '<h1>Error response</h1>',
                                             '<p>Error code %(code)d.', '<p>Message: %(message)s.',
                                             '</body>', ''))

        def log_info(self, msg, level):
            pass


    class http_channel(asynchat.async_chat):
        ac_out_buffer_size = 65536
        current_request = None
        channel_counter = counter()

        def __init__(self, server, conn, addr):
            self.channel_number = http_channel.channel_counter.increment()
            self.request_counter = counter()
            asynchat.async_chat.__init__(self, conn)
            self.server = server
            self.addr = addr
            self.set_terminator(b'\r\n\r\n')
            self.in_buffer = b''
            self.creation_time = int(time.time())
            self.last_used = self.creation_time
            self.check_maintenance()

        def __repr__(self):
            ar = asynchat.async_chat.__repr__(self)[1:-1]
            return '<%s channel#: %s requests:%s>' % (
             ar,
             self.channel_number,
             self.request_counter)

        maintenance_interval = 500

        def check_maintenance(self):
            if not self.channel_number % self.maintenance_interval:
                self.maintenance()

        def maintenance(self):
            self.kill_zombies()

        zombie_timeout = 1800

        def kill_zombies(self):
            now = int(time.time())
            for channel in list(asyncore.socket_map.values()):
                if channel.__class__ == self.__class__ and now - channel.last_used > channel.zombie_timeout:
                    channel.close()

        def send(self, data):
            result = asynchat.async_chat.send(self, data)
            self.server.bytes_out.increment(len(data))
            self.last_used = int(time.time())
            return result

        def recv--- This code section failed: ---

 L. 527         0  SETUP_FINALLY        54  'to 54'

 L. 528         2  LOAD_GLOBAL              asynchat
                4  LOAD_ATTR                async_chat
                6  LOAD_METHOD              recv
                8  LOAD_FAST                'self'
               10  LOAD_FAST                'buffer_size'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'result'

 L. 529        16  LOAD_FAST                'self'
               18  LOAD_ATTR                server
               20  LOAD_ATTR                bytes_in
               22  LOAD_METHOD              increment
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'result'
               28  CALL_FUNCTION_1       1  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 530        34  LOAD_GLOBAL              int
               36  LOAD_GLOBAL              time
               38  LOAD_METHOD              time
               40  CALL_METHOD_0         0  ''
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_FAST                'self'
               46  STORE_ATTR               last_used

 L. 531        48  LOAD_FAST                'result'
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY     0  '0'

 L. 532        54  DUP_TOP          
               56  LOAD_GLOBAL              MemoryError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    82  'to 82'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 539        68  LOAD_GLOBAL              sys
               70  LOAD_METHOD              exit
               72  LOAD_STR                 'Out of Memory!'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
             82_0  COME_FROM            60  '60'
               82  END_FINALLY      
             84_0  COME_FROM            80  '80'

Parse error at or near `POP_TOP' instruction at offset 64

        def handle_error(self):
            t, v = sys.exc_info()[:2]
            if t is SystemExit:
                raise t(v)
            else:
                asynchat.async_chat.handle_error(self)

        def log(self, *args):
            pass

        def collect_incoming_data(self, data):
            if self.current_request:
                self.current_request.collect_incoming_data(data)
            else:
                self.in_buffer = self.in_buffer + data

        def found_terminator(self):
            if self.current_request:
                self.current_request.found_terminator()
            else:
                header = self.in_buffer
                self.in_buffer = b''
                lines = header.split(b'\r\n')
                while lines:
                    if not lines[0]:
                        lines = lines[1:]

                if not lines:
                    self.close_when_done()
                    return None
                request = lines[0]
                command, uri, version = crack_request(request)
                header = join_headers(lines[1:])
                rpath, rquery = splitquery(uri)
                if '%' in rpath:
                    if rquery:
                        uri = unquote(rpath) + '?' + rquery
                    else:
                        uri = unquote(rpath)
                r = http_request(self, request, command, uri, version, header)
                self.request_counter.increment()
                self.server.total_requests.increment()
                if command is None:
                    self.log_info('Bad HTTP request: %s' % repr(request), 'error')
                    r.error(400)
                    return None
                for h in self.server.handlers:
                    if h.match(r):
                        try:
                            self.current_request = r
                            h.handle_request(r)
                        except:
                            self.server.exceptions.increment()
                            (file, fun, line), t, v, tbinfo = asyncore.compact_traceback()
                            self.log_info('Server Error: %s, %s: file: %s line: %s' % (t, v, file, line), 'error')
                            try:
                                r.error(500)
                            except:
                                pass

                        else:
                            return None
                else:
                    r.error(404)

        def writable_for_proxy(self):
            if self.ac_out_buffer:
                return 1
            if len(self.producer_fifo):
                p = self.producer_fifo.first()
                if hasattr(p, 'stalled'):
                    return not p.stalled()
                return 1


    class http_server(asyncore.dispatcher):
        SERVER_IDENT = 'HTTP Server (V%s)' % VERSION_STRING
        channel_class = http_channel

        def __init__(self, ip, port, resolver=None, logger_object=None):
            self.ip = ip
            self.port = port
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.handlers = []
            if not logger_object:
                logger_object = logger.file_logger(sys.stdout)
            self.set_reuse_addr()
            self.bind((ip, port))
            self.listen(1024)
            host, port = self.socket.getsockname()
            if not ip:
                self.log_info('Computing default hostname', 'warning')
                ip = socket.gethostbyname(socket.gethostname())
            try:
                self.server_name = socket.gethostbyaddr(ip)[0]
            except socket.error:
                self.log_info('Cannot do reverse lookup', 'warning')
                self.server_name = ip
            else:
                self.server_port = port
                self.total_clients = counter()
                self.total_requests = counter()
                self.exceptions = counter()
                self.bytes_out = counter()
                self.bytes_in = counter()
                if not logger_object:
                    logger_object = logger.file_logger(sys.stdout)
                elif resolver:
                    self.logger = logger.resolving_logger(resolver, logger_object)
                else:
                    self.logger = logger.unresolving_logger(logger_object)
                self.log_info('Medusa (V%s) started at %s\n\tHostname: %s\n\tPort:%d\n' % (
                 VERSION_STRING,
                 time.ctime(time.time()),
                 self.server_name,
                 port))

        def writable(self):
            return 0

        def handle_read(self):
            pass

        def readable(self):
            return self.accepting

        def handle_connect(self):
            pass

        def handle_accept--- This code section failed: ---

 L. 727         0  LOAD_FAST                'self'
                2  LOAD_ATTR                total_clients
                4  LOAD_METHOD              increment
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 728        10  SETUP_FINALLY        28  'to 28'

 L. 729        12  LOAD_FAST                'self'
               14  LOAD_METHOD              accept
               16  CALL_METHOD_0         0  ''
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'conn'
               22  STORE_FAST               'addr'
               24  POP_BLOCK        
               26  JUMP_FORWARD         96  'to 96'
             28_0  COME_FROM_FINALLY    10  '10'

 L. 730        28  DUP_TOP          
               30  LOAD_GLOBAL              socket
               32  LOAD_ATTR                error
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    62  'to 62'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 735        44  LOAD_FAST                'self'
               46  LOAD_METHOD              log_info
               48  LOAD_STR                 'warning: server accept() threw an exception'
               50  LOAD_STR                 'warning'
               52  CALL_METHOD_2         2  ''
               54  POP_TOP          

 L. 736        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            36  '36'

 L. 737        62  DUP_TOP          
               64  LOAD_GLOBAL              TypeError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    94  'to 94'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 742        76  LOAD_FAST                'self'
               78  LOAD_METHOD              log_info
               80  LOAD_STR                 'warning: server accept() threw EWOULDBLOCK'
               82  LOAD_STR                 'warning'
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          

 L. 743        88  POP_EXCEPT       
               90  LOAD_CONST               None
               92  RETURN_VALUE     
             94_0  COME_FROM            68  '68'
               94  END_FINALLY      
             96_0  COME_FROM            26  '26'

 L. 745        96  LOAD_FAST                'self'
               98  LOAD_METHOD              channel_class
              100  LOAD_FAST                'self'
              102  LOAD_FAST                'conn'
              104  LOAD_FAST                'addr'
              106  CALL_METHOD_3         3  ''
              108  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 58

        def install_handler(self, handler, back=0):
            if back:
                self.handlers.append(handler)
            else:
                self.handlers.insert(0, handler)

        def remove_handler(self, handler):
            self.handlers.remove(handler)

        def status(self):
            from supervisor.medusa.util import english_bytes

            def nice_bytes(n):
                return ''.join(english_bytes(n))

            handler_stats = [_f for _f in map(maybe_status, self.handlers) if _f]
            if self.total_clients:
                ratio = self.total_requests.as_long() / float(self.total_clients.as_long())
            else:
                ratio = 0.0
            return producers.composite_producer([
             producers.lines_producer([
              '<h2>%s</h2>' % self.SERVER_IDENT,
              '<br>Listening on: <b>Host:</b> %s' % self.server_name,
              '<b>Port:</b> %d' % self.port,
              '<p><ul><li>Total <b>Clients:</b> %s' % self.total_clients,
              '<b>Requests:</b> %s' % self.total_requests,
              '<b>Requests/Client:</b> %.1f' % ratio,
              '<li>Total <b>Bytes In:</b> %s' % nice_bytes(self.bytes_in.as_long()),
              '<b>Bytes Out:</b> %s' % nice_bytes(self.bytes_out.as_long()),
              '<li>Total <b>Exceptions:</b> %s' % self.exceptions,
              '</ul><p><b>Extension List</b><ul>'])] + handler_stats + [
             producers.simple_producer('</ul>')])


    def maybe_status(thing):
        if hasattr(thing, 'status'):
            return thing.status()
        return


    CONNECTION = re.compile('Connection: (.*)', re.IGNORECASE)

    def join_headers(headers):
        r = []
        for i in range(len(headers)):
            if headers[i][0] in ' \t':
                r[-1] = r[(-1)] + headers[i][1:]
            else:
                r.append(headers[i])
        else:
            return r


    def get_header(head_reg, lines, group=1):
        for line in lines:
            m = head_reg.match(line)
            if m and m.end() == len(line):
                return m.group(group)
            return ''


    def get_header_match(head_reg, lines):
        for line in lines:
            m = head_reg.match(line)
            if m and m.end() == len(line):
                return m
            return ''


    REQUEST = re.compile('([^ ]+) ([^ ]+)(( HTTP/([0-9.]+))$|$)')

    def crack_request(r):
        m = REQUEST.match(r)
        if m:
            if m.end() == len(r):
                if m.group(3):
                    version = m.group(5)
                else:
                    version = None
                return (
                 m.group(1), m.group(2), version)
        return (None, None, None)


    if __name__ == '__main__':
        if len(sys.argv) < 2:
            print('usage: %s <root> <port>' % sys.argv[0])
        else:
            import supervisor.medusa.monitor as monitor
            import supervisor.medusa.filesys as filesys
            import supervisor.medusa.default_handler as default_handler
            import supervisor.medusa.ftp_server as ftp_server
            import supervisor.medusa.chat_server as chat_server
            import supervisor.medusa.resolver as resolver
            rs = resolver.caching_resolver('127.0.0.1')
            lg = logger.file_logger(sys.stdout)
            ms = monitor.secure_monitor_server('fnord', '127.0.0.1', 9999)
            fs = filesys.os_filesystem(sys.argv[1])
            dh = default_handler.default_handler(fs)
            hs = http_server('', int(sys.argv[2]), rs, lg)
            hs.install_handler(dh)
            ftp = ftp_server.ftp_server((ftp_server.dummy_authorizer(sys.argv[1])),
              port=8021,
              resolver=rs,
              logger_object=lg)
            cs = chat_server.chat_server('', 7777)
            if '-p' in sys.argv:

                def profile_loop():
                    try:
                        asyncore.loop()
                    except KeyboardInterrupt:
                        pass


                import profile
                profile.run('profile_loop()', 'profile.out')
            else:
                asyncore.loop()