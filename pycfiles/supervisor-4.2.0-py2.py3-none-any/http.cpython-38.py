# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/http.py
# Compiled at: 2019-09-16 13:23:54
# Size of source mod 2**32: 31385 bytes
import os, stat, time, sys, socket, errno, weakref, traceback
try:
    import pwd
except ImportError:
    import getpass as pwd
else:
    from supervisor.compat import urllib
    from supervisor.compat import sha1
    from supervisor.compat import as_bytes
    from supervisor.compat import as_string
    import supervisor.medusa as asyncore
    from supervisor.medusa import http_date
    from supervisor.medusa import http_server
    from supervisor.medusa import producers
    from supervisor.medusa import filesys
    from supervisor.medusa import default_handler
    import supervisor.medusa.auth_handler as auth_handler

    class NOT_DONE_YET:
        pass


    class deferring_chunked_producer:
        __doc__ = "A producer that implements the 'chunked' transfer coding for HTTP/1.1.\n    Here is a sample usage:\n            request['Transfer-Encoding'] = 'chunked'\n            request.push (\n                    producers.chunked_producer (your_producer)\n                    )\n            request.done()\n    "

        def __init__(self, producer, footers=None):
            self.producer = producer
            self.footers = footers
            self.delay = 0.1

        def more(self):
            if self.producer:
                data = self.producer.more()
                if data is NOT_DONE_YET:
                    return NOT_DONE_YET
                if data:
                    s = '%x' % len(data)
                    return as_bytes(s) + b'\r\n' + data + b'\r\n'
                self.producer = None
                if self.footers:
                    return (b'\r\n').join([b'0'] + self.footers) + b'\r\n\r\n'
                return b'0\r\n\r\n'
            else:
                return b''


    class deferring_composite_producer:
        __doc__ = 'combine a fifo of producers into one'

        def __init__(self, producers):
            self.producers = producers
            self.delay = 0.1

        def more(self):
            while len(self.producers):
                p = self.producers[0]
                d = p.more()
                if d is NOT_DONE_YET:
                    return NOT_DONE_YET
                if d:
                    return d
                self.producers.pop(0)

            return b''


    class deferring_globbing_producer:
        __doc__ = "\n    'glob' the output from a producer into a particular buffer size.\n    helps reduce the number of calls to send().  [this appears to\n    gain about 30% performance on requests to a single channel]\n    "

        def __init__(self, producer, buffer_size=65536):
            self.producer = producer
            self.buffer = b''
            self.buffer_size = buffer_size
            self.delay = 0.1

        def more--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                buffer
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                buffer_size
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE   106  'to 106'

 L.  98        16  LOAD_FAST                'self'
               18  LOAD_ATTR                producer
               20  LOAD_METHOD              more
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'data'

 L.  99        26  LOAD_FAST                'data'
               28  LOAD_GLOBAL              NOT_DONE_YET
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 100        34  LOAD_GLOBAL              NOT_DONE_YET
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 101        38  LOAD_FAST                'data'
               40  POP_JUMP_IF_FALSE   106  'to 106'

 L. 102        42  SETUP_FINALLY        60  'to 60'

 L. 103        44  LOAD_FAST                'self'
               46  LOAD_ATTR                buffer
               48  LOAD_FAST                'data'
               50  BINARY_ADD       
               52  LOAD_FAST                'self'
               54  STORE_ATTR               buffer
               56  POP_BLOCK        
               58  JUMP_ABSOLUTE       104  'to 104'
             60_0  COME_FROM_FINALLY    42  '42'

 L. 104        60  DUP_TOP          
               62  LOAD_GLOBAL              TypeError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    98  'to 98'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 105        74  LOAD_GLOBAL              as_bytes
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                buffer
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_GLOBAL              as_bytes
               84  LOAD_FAST                'data'
               86  CALL_FUNCTION_1       1  ''
               88  BINARY_ADD       
               90  LOAD_FAST                'self'
               92  STORE_ATTR               buffer
               94  POP_EXCEPT       
               96  JUMP_ABSOLUTE       104  'to 104'
             98_0  COME_FROM            66  '66'
               98  END_FINALLY      
              100  JUMP_BACK             0  'to 0'

 L. 107       102  BREAK_LOOP          106  'to 106'
              104  JUMP_BACK             0  'to 0'
            106_0  COME_FROM            40  '40'
            106_1  COME_FROM            14  '14'

 L. 108       106  LOAD_FAST                'self'
              108  LOAD_ATTR                buffer
              110  STORE_FAST               'r'

 L. 109       112  LOAD_CONST               b''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               buffer

 L. 110       118  LOAD_FAST                'r'
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 120


    class deferring_hooked_producer:
        __doc__ = '\n    A producer that will call <function> when it empties,.\n    with an argument of the number of bytes produced.  Useful\n    for logging/instrumentation purposes.\n    '

        def __init__(self, producer, function):
            self.producer = producer
            self.function = function
            self.bytes = 0
            self.delay = 0.1

        def more(self):
            if self.producer:
                result = self.producer.more()
                if result is NOT_DONE_YET:
                    return NOT_DONE_YET
                elif not result:
                    self.producer = None
                    self.function(self.bytes)
                else:
                    self.bytes += len(result)
                return result
            return b''


    class deferring_http_request(http_server.http_request):
        __doc__ = " The medusa http_request class uses the default set of producers in\n    medusa.producers.  We can't use these because they don't know anything\n    about deferred responses, so we override various methods here.  This was\n    added to support tail -f like behavior on the logtail handler "

        def done(self, *arg, **kw):
            """ I didn't want to override this, but there's no way around
        it in order to support deferreds - CM

        finalize this transaction - send output to the http channel"""
            connection = http_server.get_header(http_server.CONNECTION, self.header)
            connection = connection.lower()
            close_it = 0
            wrap_in_chunking = 0
            globbing = 1
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
                            globbing = 0
                    else:
                        close_it = 1
            elif self.version is None:
                close_it = 1
            outgoing_header = producers.simple_producer(self.build_reply_header())
            if close_it:
                self['Connection'] = 'close'
            elif wrap_in_chunking:
                outgoing_producer = deferring_chunked_producer(deferring_composite_producer(self.outgoing))
                outgoing_producer = deferring_composite_producer([
                 outgoing_header, outgoing_producer])
            else:
                self.outgoing.insert(0, outgoing_header)
                outgoing_producer = deferring_composite_producer(self.outgoing)
            outgoing_producer = deferring_hooked_producer(outgoing_producer, self.log)
            if globbing:
                outgoing_producer = deferring_globbing_producer(outgoing_producer)
            self.channel.push_with_producer(outgoing_producer)
            self.channel.current_request = None
            if close_it:
                self.channel.close_when_done()

        def log(self, bytes):
            """ We need to override this because UNIX domain sockets return
        an empty string for the addr rather than a (host, port) combination """
            if self.channel.addr:
                host = self.channel.addr[0]
                port = self.channel.addr[1]
            else:
                host = 'localhost'
                port = 0
            self.channel.server.logger.log(host, '%d - - [%s] "%s" %d %d\n' % (
             port,
             self.log_date_string(time.time()),
             self.request,
             self.reply_code,
             bytes))

        def cgi_environment(self):
            env = {}
            header2env = {'content-length':'CONTENT_LENGTH', 
             'content-type':'CONTENT_TYPE', 
             'connection':'CONNECTION_TYPE'}
            workdir = os.getcwd()
            path, params, query, fragment = self.split_uri()
            if params:
                path = path + params
            if path:
                if path[0] == '/':
                    path = path[1:]
            else:
                if '%' in path:
                    path = http_server.unquote(path)
                if query:
                    query = query[1:]
                server = self.channel.server
                env['REQUEST_METHOD'] = self.command.upper()
                env['SERVER_PORT'] = str(server.port)
                env['SERVER_NAME'] = server.server_name
                env['SERVER_SOFTWARE'] = server.SERVER_IDENT
                env['SERVER_PROTOCOL'] = 'HTTP/' + self.version
                env['channel.creation_time'] = self.channel.creation_time
                env['SCRIPT_NAME'] = ''
                env['PATH_INFO'] = '/' + path
                env['PATH_TRANSLATED'] = os.path.normpath(os.path.join(workdir, env['PATH_INFO']))
                if query:
                    env['QUERY_STRING'] = query
                env['GATEWAY_INTERFACE'] = 'CGI/1.1'
                if self.channel.addr:
                    env['REMOTE_ADDR'] = self.channel.addr[0]
                else:
                    env['REMOTE_ADDR'] = '127.0.0.1'
            for header in self.header:
                key, value = header.split(':', 1)
                key = key.lower()
                value = value.strip()
                if key in header2env and value:
                    env[header2env.get(key)] = value
                else:
                    key = 'HTTP_%s' % '_'.join(key.split('-')).upper()
                    if value and key not in env:
                        env[key] = value
                    return env

        def get_server_url(self):
            """ Functionality that medusa's http request doesn't have; set an
        attribute named 'server_url' on the request based on the Host: header
        """
            default_port = {'http':'80', 
             'https':'443'}
            environ = self.cgi_environment()
            if environ.get('HTTPS') in ('on', 'ON') or environ.get('SERVER_PORT_SECURE') == '1':
                protocol = 'https'
            else:
                protocol = 'http'
            if 'HTTP_HOST' in environ:
                host = environ['HTTP_HOST'].strip()
                hostname, port = urllib.splitport(host)
            else:
                hostname = environ['SERVER_NAME'].strip()
                port = environ['SERVER_PORT']
            if port is None or default_port[protocol] == port:
                host = hostname
            else:
                host = hostname + ':' + port
            server_url = '%s://%s' % (protocol, host)
            if server_url[-1:] == '/':
                server_url = server_url[:-1]
            return server_url


    class deferring_http_channel(http_server.http_channel):
        ac_out_buffer_size = 4096
        delay = 0
        last_writable_check = 0

        def writable(self, now=None):
            if now is None:
                now = time.time()
            if self.delay:
                elapsed = now - self.last_writable_check
                if elapsed > self.delay or elapsed < 0:
                    self.last_writable_check = now
                    return True
                return False
            return http_server.http_channel.writable(self)

        def refill_buffer(self):
            """ Implement deferreds """
            while len(self.producer_fifo):
                p = self.producer_fifo.first()
                if p is None:
                    if not self.ac_out_buffer:
                        self.producer_fifo.pop()
                        self.close()
                    return
                    if isinstance(p, bytes):
                        self.producer_fifo.pop()
                        self.ac_out_buffer += p
                        return
                    data = p.more()
                    if data is NOT_DONE_YET:
                        self.delay = p.delay
                        return
                    if data:
                        self.ac_out_buffer = self.ac_out_buffer + data
                        self.delay = False
                        return
                    self.producer_fifo.pop()
                else:
                    return

        def found_terminator(self):
            """ We only override this to use 'deferring_http_request' class
        instead of the normal http_request class; it sucks to need to override
        this """
            if self.current_request:
                self.current_request.found_terminator()
            else:
                header = as_string(self.in_buffer)
                self.in_buffer = b''
                lines = header.split('\r\n')
                while lines:
                    if not lines[0]:
                        lines = lines[1:]

                if not lines:
                    self.close_when_done()
                    return None
                request = lines[0]
                command, uri, version = http_server.crack_request(request)
                header = http_server.join_headers(lines[1:])
                rpath, rquery = http_server.splitquery(uri)
                if '%' in rpath:
                    if rquery:
                        uri = http_server.unquote(rpath) + '?' + rquery
                    else:
                        uri = http_server.unquote(rpath)
                r = deferring_http_request(self, request, command, uri, version, header)
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
                            self.server.log_info('Server Error: %s, %s: file: %s line: %s' % (
                             t, v, file, line), 'error')
                            try:
                                r.error(500)
                            except:
                                pass

                        else:
                            return None
                else:
                    r.error(404)


    class supervisor_http_server(http_server.http_server):
        channel_class = deferring_http_channel
        ip = None

        def prebind(self, sock, logger_object):
            """ Override __init__ to do logger setup earlier so it can
        go to our logger object instead of stdout """
            from supervisor.medusa import logger
            if not logger_object:
                logger_object = logger.file_logger(sys.stdout)
            logger_object = logger.unresolving_logger(logger_object)
            self.logger = logger_object
            asyncore.dispatcher.__init__(self)
            self.set_socket(sock)
            self.handlers = []
            sock.setblocking(0)
            self.set_reuse_addr()

        def postbind(self):
            import supervisor.medusa.counter as counter
            from supervisor.medusa.http_server import VERSION_STRING
            self.listen(1024)
            self.total_clients = counter()
            self.total_requests = counter()
            self.exceptions = counter()
            self.bytes_out = counter()
            self.bytes_in = counter()
            self.log_info('Medusa (V%s) started at %s\n\tHostname: %s\n\tPort:%s\n' % (
             VERSION_STRING,
             time.ctime(time.time()),
             self.server_name,
             self.port))

        def log_info(self, message, type='info'):
            ip = ''
            if getattr(self, 'ip', None) is not None:
                ip = self.ip
            self.logger.log(ip, message)


    class supervisor_af_inet_http_server(supervisor_http_server):
        __doc__ = ' AF_INET version of supervisor HTTP server '

        def __init__(self, ip, port, logger_object):
            self.ip = ip
            self.port = port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.prebind(sock, logger_object)
            self.bind((ip, port))
            ip or self.log_info('Computing default hostname', 'warning')
            hostname = socket.gethostname()
            try:
                ip = socket.gethostbyname(hostname)
            except socket.error:
                raise ValueError('Could not determine IP address for hostname %s, please try setting an explicit IP address in the "port" setting of your [inet_http_server] section.  For example, instead of "port = 9001", try "port = 127.0.0.1:9001."' % hostname)
            else:
                try:
                    self.server_name = socket.gethostbyaddr(ip)[0]
                except socket.error:
                    self.log_info('Cannot do reverse lookup', 'warning')
                    self.server_name = ip
                else:
                    self.postbind()


    class supervisor_af_unix_http_server(supervisor_http_server):
        __doc__ = ' AF_UNIX version of supervisor HTTP server '

        def __init__--- This code section failed: ---

 L. 555         0  LOAD_FAST                'socketname'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               ip

 L. 556         6  LOAD_FAST                'socketname'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               port

 L. 564        12  LOAD_STR                 '%s.%d'
               14  LOAD_FAST                'socketname'
               16  LOAD_GLOBAL              os
               18  LOAD_METHOD              getpid
               20  CALL_METHOD_0         0  ''
               22  BUILD_TUPLE_2         2 
               24  BINARY_MODULO    
               26  STORE_FAST               'tempname'

 L. 566        28  SETUP_FINALLY        44  'to 44'

 L. 567        30  LOAD_GLOBAL              os
               32  LOAD_METHOD              unlink
               34  LOAD_FAST                'tempname'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         64  'to 64'
             44_0  COME_FROM_FINALLY    28  '28'

 L. 568        44  DUP_TOP          
               46  LOAD_GLOBAL              OSError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    62  'to 62'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 569        58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            50  '50'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            42  '42'

 L. 572        64  LOAD_GLOBAL              socket
               66  LOAD_METHOD              socket
               68  LOAD_GLOBAL              socket
               70  LOAD_ATTR                AF_UNIX
               72  LOAD_GLOBAL              socket
               74  LOAD_ATTR                SOCK_STREAM
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'sock'

 L. 573     80_82  SETUP_FINALLY       394  'to 394'

 L. 574        84  LOAD_FAST                'sock'
               86  LOAD_METHOD              bind
               88  LOAD_FAST                'tempname'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 575        94  LOAD_GLOBAL              os
               96  LOAD_METHOD              chmod
               98  LOAD_FAST                'tempname'
              100  LOAD_FAST                'sockchmod'
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          

 L. 576       106  SETUP_FINALLY       124  'to 124'

 L. 578       108  LOAD_GLOBAL              os
              110  LOAD_METHOD              link
              112  LOAD_FAST                'tempname'
              114  LOAD_FAST                'socketname'
              116  CALL_METHOD_2         2  ''
              118  POP_TOP          
              120  POP_BLOCK        
              122  JUMP_FORWARD        244  'to 244'
            124_0  COME_FROM_FINALLY   106  '106'

 L. 579       124  DUP_TOP          
              126  LOAD_GLOBAL              OSError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   242  'to 242'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 581       138  LOAD_FAST                'self'
              140  LOAD_METHOD              checkused
              142  LOAD_FAST                'socketname'
              144  CALL_METHOD_1         1  ''
              146  STORE_FAST               'used'

 L. 582       148  LOAD_FAST                'used'
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 584       152  LOAD_GLOBAL              socket
              154  LOAD_METHOD              error
              156  LOAD_GLOBAL              errno
              158  LOAD_ATTR                EADDRINUSE
              160  CALL_METHOD_1         1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
            164_0  COME_FROM           150  '150'

 L. 587       164  LOAD_STR                 'Unlinking stale socket %s\n'
              166  LOAD_FAST                'socketname'
              168  BINARY_MODULO    
              170  STORE_FAST               'msg'

 L. 588       172  LOAD_GLOBAL              sys
              174  LOAD_ATTR                stderr
              176  LOAD_METHOD              write
              178  LOAD_FAST                'msg'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 589       184  SETUP_FINALLY       200  'to 200'

 L. 590       186  LOAD_GLOBAL              os
              188  LOAD_METHOD              unlink
              190  LOAD_FAST                'socketname'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  POP_BLOCK        
              198  JUMP_FORWARD        212  'to 212'
            200_0  COME_FROM_FINALLY   184  '184'

 L. 591       200  POP_TOP          
              202  POP_TOP          
              204  POP_TOP          

 L. 592       206  POP_EXCEPT       
              208  JUMP_FORWARD        212  'to 212'
              210  END_FINALLY      
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           198  '198'

 L. 593       212  LOAD_FAST                'sock'
              214  LOAD_METHOD              close
              216  CALL_METHOD_0         0  ''
              218  POP_TOP          

 L. 594       220  LOAD_GLOBAL              time
              222  LOAD_METHOD              sleep
              224  LOAD_CONST               0.3
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 595       230  POP_EXCEPT       
              232  POP_BLOCK        
              234  CALL_FINALLY        394  'to 394'
              236  JUMP_BACK            64  'to 64'
              238  POP_EXCEPT       
              240  JUMP_FORWARD        390  'to 390'
            242_0  COME_FROM           130  '130'
              242  END_FINALLY      
            244_0  COME_FROM           122  '122'

 L. 597       244  SETUP_FINALLY       272  'to 272'

 L. 598       246  LOAD_GLOBAL              os
              248  LOAD_METHOD              chown
              250  LOAD_FAST                'socketname'
              252  LOAD_FAST                'sockchown'
              254  LOAD_CONST               0
              256  BINARY_SUBSCR    
              258  LOAD_FAST                'sockchown'
              260  LOAD_CONST               1
              262  BINARY_SUBSCR    
              264  CALL_METHOD_3         3  ''
              266  POP_TOP          
              268  POP_BLOCK        
              270  JUMP_FORWARD        370  'to 370'
            272_0  COME_FROM_FINALLY   244  '244'

 L. 599       272  DUP_TOP          
              274  LOAD_GLOBAL              OSError
              276  COMPARE_OP               exception-match
          278_280  POP_JUMP_IF_FALSE   368  'to 368'
              282  POP_TOP          
              284  STORE_FAST               'why'
              286  POP_TOP          
              288  SETUP_FINALLY       356  'to 356'

 L. 600       290  LOAD_FAST                'why'
              292  LOAD_ATTR                args
              294  LOAD_CONST               0
              296  BINARY_SUBSCR    
              298  LOAD_GLOBAL              errno
              300  LOAD_ATTR                EPERM
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   350  'to 350'

 L. 601       308  LOAD_STR                 'Not permitted to chown %s to uid/gid %s; adjust "sockchown" value in config file or on command line to values that the current user (%s) can successfully chown'
              310  STORE_FAST               'msg'

 L. 605       312  LOAD_GLOBAL              ValueError
              314  LOAD_FAST                'msg'
              316  LOAD_FAST                'socketname'

 L. 606       318  LOAD_GLOBAL              repr
              320  LOAD_FAST                'sockchown'
              322  CALL_FUNCTION_1       1  ''

 L. 607       324  LOAD_GLOBAL              pwd
              326  LOAD_METHOD              getpwuid

 L. 608       328  LOAD_GLOBAL              os
              330  LOAD_METHOD              geteuid
              332  CALL_METHOD_0         0  ''

 L. 607       334  CALL_METHOD_1         1  ''

 L. 608       336  LOAD_CONST               0

 L. 607       338  BINARY_SUBSCR    

 L. 605       340  BUILD_TUPLE_3         3 
              342  BINARY_MODULO    
              344  CALL_FUNCTION_1       1  ''
              346  RAISE_VARARGS_1       1  'exception instance'
              348  JUMP_FORWARD        352  'to 352'
            350_0  COME_FROM           304  '304'

 L. 612       350  RAISE_VARARGS_0       0  'reraise'
            352_0  COME_FROM           348  '348'
              352  POP_BLOCK        
              354  BEGIN_FINALLY    
            356_0  COME_FROM_FINALLY   288  '288'
              356  LOAD_CONST               None
              358  STORE_FAST               'why'
              360  DELETE_FAST              'why'
              362  END_FINALLY      
              364  POP_EXCEPT       
              366  JUMP_FORWARD        370  'to 370'
            368_0  COME_FROM           278  '278'
              368  END_FINALLY      
            370_0  COME_FROM           366  '366'
            370_1  COME_FROM           270  '270'

 L. 613       370  LOAD_FAST                'self'
              372  LOAD_METHOD              prebind
              374  LOAD_FAST                'sock'
              376  LOAD_FAST                'logger_object'
              378  CALL_METHOD_2         2  ''
              380  POP_TOP          

 L. 614       382  POP_BLOCK        
              384  CALL_FINALLY        394  'to 394'
          386_388  BREAK_LOOP          436  'to 436'
            390_0  COME_FROM           240  '240'
              390  POP_BLOCK        
              392  BEGIN_FINALLY    
            394_0  COME_FROM           384  '384'
            394_1  COME_FROM           234  '234'
            394_2  COME_FROM_FINALLY    80  '80'

 L. 617       394  SETUP_FINALLY       410  'to 410'

 L. 618       396  LOAD_GLOBAL              os
              398  LOAD_METHOD              unlink
              400  LOAD_FAST                'tempname'
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          
              406  POP_BLOCK        
              408  JUMP_FORWARD        432  'to 432'
            410_0  COME_FROM_FINALLY   394  '394'

 L. 619       410  DUP_TOP          
              412  LOAD_GLOBAL              OSError
              414  COMPARE_OP               exception-match
          416_418  POP_JUMP_IF_FALSE   430  'to 430'
              420  POP_TOP          
              422  POP_TOP          
              424  POP_TOP          

 L. 620       426  POP_EXCEPT       
              428  JUMP_FORWARD        432  'to 432'
            430_0  COME_FROM           416  '416'
              430  END_FINALLY      
            432_0  COME_FROM           428  '428'
            432_1  COME_FROM           408  '408'
              432  END_FINALLY      
              434  JUMP_BACK            64  'to 64'

 L. 622       436  LOAD_STR                 '<unix domain socket>'
              438  LOAD_FAST                'self'
              440  STORE_ATTR               server_name

 L. 623       442  LOAD_FAST                'self'
              444  LOAD_METHOD              postbind
              446  CALL_METHOD_0         0  ''
              448  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 232

        def checkused(self, socketname):
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                s.connect(socketname)
                s.send(as_bytes('GET / HTTP/1.0\r\n\r\n'))
                s.recv(1)
                s.close()
            except socket.error:
                return False
            else:
                return True


    class tail_f_producer:

        def __init__(self, request, filename, head):
            self.request = weakref.ref(request)
            self.filename = filename
            self.delay = 0.1
            self._open()
            sz = self._fsize()
            if sz >= head:
                self.sz = sz - head

        def __del__(self):
            self._close()

        def more(self):
            self._follow()
            try:
                newsz = self._fsize()
            except (OSError, ValueError):
                return b''
            else:
                bytes_added = newsz - self.sz
                if bytes_added < 0:
                    self.sz = 0
                    return '==> File truncated <==\n'
                if bytes_added > 0:
                    self.file.seek(-bytes_added, 2)
                    bytes = self.file.read(bytes_added)
                    self.sz = newsz
                    return bytes
                return NOT_DONE_YET

        def _open(self):
            self.file = open(self.filename, 'rb')
            self.ino = os.fstat(self.file.fileno())[stat.ST_INO]
            self.sz = 0

        def _close(self):
            self.file.close()

        def _follow(self):
            try:
                ino = os.stat(self.filename)[stat.ST_INO]
            except (OSError, ValueError):
                return
            else:
                if self.ino != ino:
                    self._close()
                    self._open()

        def _fsize(self):
            return os.fstat(self.file.fileno())[stat.ST_SIZE]


    class logtail_handler:
        IDENT = 'Logtail HTTP Request Handler'
        path = '/logtail'

        def __init__(self, supervisord):
            self.supervisord = supervisord

        def match(self, request):
            return request.uri.startswith(self.path)

        def handle_request(self, request):
            if request.command != 'GET':
                request.error(400)
                return None
            else:
                path, params, query, fragment = request.split_uri()
                if '%' in path:
                    path = http_server.unquote(path)
                while path:
                    if path[0] == '/':
                        path = path[1:]

            path, process_name_and_channel = path.split('/', 1)
            try:
                process_name, channel = process_name_and_channel.split('/', 1)
            except ValueError:
                process_name = process_name_and_channel
                channel = 'stdout'
            else:
                from supervisor.options import split_namespec
                group_name, process_name = split_namespec(process_name)
                group = self.supervisord.process_groups.get(group_name)
                if group is None:
                    request.error(404)
                    return None
                else:
                    process = group.processes.get(process_name)
                    if process is None:
                        request.error(404)
                        return None
                    logfile = getattr(process.config, '%s_logfile' % channel, None)
                    logfile is None or os.path.exists(logfile) or request.error(410)
                    return None
                mtime = os.stat(logfile)[stat.ST_MTIME]
                request['Last-Modified'] = http_date.build_http_date(mtime)
                request['Content-Type'] = 'text/plain;charset=utf-8'
                request.push(tail_f_producer(request, logfile, 1024))
                request.done()


    class mainlogtail_handler:
        IDENT = 'Main Logtail HTTP Request Handler'
        path = '/mainlogtail'

        def __init__(self, supervisord):
            self.supervisord = supervisord

        def match(self, request):
            return request.uri.startswith(self.path)

        def handle_request(self, request):
            if request.command != 'GET':
                request.error(400)
                return None
            else:
                logfile = self.supervisord.options.logfile
                logfile is None or os.path.exists(logfile) or request.error(410)
                return None
            mtime = os.stat(logfile)[stat.ST_MTIME]
            request['Last-Modified'] = http_date.build_http_date(mtime)
            request['Content-Type'] = 'text/plain;charset=utf-8'
            request.push(tail_f_producer(request, logfile, 1024))
            request.done()


    def make_http_servers(options, supervisord):
        servers = []
        wrapper = LogWrapper(options.logger)
        for config in options.server_configs:
            family = config['family']
            if family == socket.AF_INET:
                host, port = config['host'], config['port']
                hs = supervisor_af_inet_http_server(host, port, logger_object=wrapper)
            else:
                if family == socket.AF_UNIX:
                    socketname = config['file']
                    sockchmod = config['chmod']
                    sockchown = config['chown']
                    hs = supervisor_af_unix_http_server(socketname, sockchmod, sockchown, logger_object=wrapper)
                else:
                    raise ValueError('Cannot determine socket type %r' % family)
            from supervisor.xmlrpc import supervisor_xmlrpc_handler
            from supervisor.xmlrpc import SystemNamespaceRPCInterface
            from supervisor.web import supervisor_ui_handler
            subinterfaces = []
            for name, factory, d in options.rpcinterface_factories:
                try:
                    inst = factory(supervisord, **d)
                except:
                    tb = traceback.format_exc()
                    options.logger.warn(tb)
                    raise ValueError('Could not make %s rpc interface' % name)
                else:
                    subinterfaces.append((name, inst))
                    options.logger.info('RPC interface %r initialized' % name)
            else:
                subinterfaces.append(('system',
                 SystemNamespaceRPCInterface(subinterfaces)))
                xmlrpchandler = supervisor_xmlrpc_handler(supervisord, subinterfaces)
                tailhandler = logtail_handler(supervisord)
                maintailhandler = mainlogtail_handler(supervisord)
                uihandler = supervisor_ui_handler(supervisord)
                here = os.path.abspath(os.path.dirname(__file__))
                templatedir = os.path.join(here, 'ui')
                filesystem = filesys.os_filesystem(templatedir)
                defaulthandler = default_handler.default_handler(filesystem)
                username = config['username']
                password = config['password']
                if username:
                    users = {username: password}
                    xmlrpchandler = supervisor_auth_handler(users, xmlrpchandler)
                    tailhandler = supervisor_auth_handler(users, tailhandler)
                    maintailhandler = supervisor_auth_handler(users, maintailhandler)
                    uihandler = supervisor_auth_handler(users, uihandler)
                    defaulthandler = supervisor_auth_handler(users, defaulthandler)
                else:
                    options.logger.critical('Server %r running without any HTTP authentication checking' % config['section'])
                hs.install_handler(defaulthandler)
                hs.install_handler(uihandler)
                hs.install_handler(maintailhandler)
                hs.install_handler(tailhandler)
                hs.install_handler(xmlrpchandler)
                servers.append((config, hs))

        else:
            return servers


    class LogWrapper:
        __doc__ = 'Receives log messages from the Medusa servers and forwards\n    them to the Supervisor logger'

        def __init__(self, logger):
            self.logger = logger

        def log(self, msg):
            """Medusa servers call this method.  There is no log level so
        we have to sniff the message.  We want "Server Error" messages
        from medusa.http_server logged as errors at least."""
            if msg.endswith('\n'):
                msg = msg[:-1]
            elif 'error' in msg.lower():
                self.logger.error(msg)
            else:
                self.logger.trace(msg)


    class encrypted_dictionary_authorizer:

        def __init__(self, dict):
            self.dict = dict

        def authorize(self, auth_info):
            username, password = auth_info
            if username in self.dict:
                stored_password = self.dict[username]
                if stored_password.startswith('{SHA}'):
                    password_hash = sha1(as_bytes(password)).hexdigest()
                    return stored_password[5:] == password_hash
                return stored_password == password
            else:
                return False


    class supervisor_auth_handler(auth_handler):

        def __init__(self, dict, handler, realm='default'):
            auth_handler.__init__(self, dict, handler, realm)
            self.authorizer = encrypted_dictionary_authorizer(dict)