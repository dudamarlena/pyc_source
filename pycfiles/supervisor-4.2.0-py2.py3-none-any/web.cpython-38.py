# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/web.py
# Compiled at: 2019-09-16 13:23:31
# Size of source mod 2**32: 23969 bytes
import os, re, time, traceback, datetime
from supervisor import templating
from supervisor.compat import urllib
from supervisor.compat import urlparse
from supervisor.compat import as_string
from supervisor.compat import PY2
from supervisor.compat import unicode
from supervisor.medusa import producers
from supervisor.medusa.http_server import http_date
from supervisor.medusa.http_server import get_header
from supervisor.medusa.xmlrpc_handler import collector
from supervisor.process import ProcessStates
from supervisor.http import NOT_DONE_YET
from supervisor.options import VERSION
from supervisor.options import make_namespec
from supervisor.options import split_namespec
from supervisor.xmlrpc import SystemNamespaceRPCInterface
from supervisor.xmlrpc import RootRPCInterface
from supervisor.xmlrpc import Faults
from supervisor.xmlrpc import RPCError
from supervisor.rpcinterface import SupervisorNamespaceRPCInterface

class DeferredWebProducer:
    __doc__ = ' A medusa producer that implements a deferred callback; requires\n    a subclass of asynchat.async_chat that handles NOT_DONE_YET sentinel '
    CONNECTION = re.compile('Connection: (.*)', re.IGNORECASE)

    def __init__(self, request, callback):
        self.callback = callback
        self.request = request
        self.finished = False
        self.delay = float(callback.delay)

    def more--- This code section failed: ---

 L.  46         0  LOAD_FAST                'self'
                2  LOAD_ATTR                finished
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L.  47         6  LOAD_STR                 ''
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L.  48        10  SETUP_FINALLY        52  'to 52'

 L.  49        12  LOAD_FAST                'self'
               14  LOAD_METHOD              callback
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'response'

 L.  50        20  LOAD_FAST                'response'
               22  LOAD_GLOBAL              NOT_DONE_YET
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    34  'to 34'

 L.  51        28  LOAD_GLOBAL              NOT_DONE_YET
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'

 L.  53        34  LOAD_CONST               True
               36  LOAD_FAST                'self'
               38  STORE_ATTR               finished

 L.  54        40  LOAD_FAST                'self'
               42  LOAD_METHOD              sendresponse
               44  LOAD_FAST                'response'
               46  CALL_METHOD_1         1  ''
               48  POP_BLOCK        
               50  RETURN_VALUE     
             52_0  COME_FROM_FINALLY    10  '10'

 L.  56        52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  57        58  LOAD_GLOBAL              traceback
               60  LOAD_METHOD              format_exc
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'tb'

 L.  59        66  LOAD_FAST                'self'
               68  LOAD_ATTR                request
               70  LOAD_ATTR                channel
               72  LOAD_ATTR                server
               74  LOAD_ATTR                logger
               76  LOAD_METHOD              log
               78  LOAD_STR                 'Web interface error'
               80  LOAD_FAST                'tb'
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L.  60        86  LOAD_CONST               True
               88  LOAD_FAST                'self'
               90  STORE_ATTR               finished

 L.  61        92  LOAD_FAST                'self'
               94  LOAD_ATTR                request
               96  LOAD_METHOD              error
               98  LOAD_CONST               500
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'

Parse error at or near `STORE_FAST' instruction at offset 64

    def sendresponse(self, response):
        headers = response.get('headers', {})
        for header in headers:
            self.request[header] = headers[header]
        else:
            if 'Content-Type' not in self.request:
                self.request['Content-Type'] = 'text/plain'
            if headers.get'Location':
                self.request['Content-Length'] = 0
                self.request.error301
                return
                body = response.get('body', '')
                self.request['Content-Length'] = len(body)
                self.request.pushbody
                connection = get_header(self.CONNECTION, self.request.header)
                close_it = 0
                wrap_in_chunking = 0
                if self.request.version == '1.0':
                    if connection == 'keep-alive':
                        if not self.request.has_key'Content-Length':
                            close_it = 1
                        else:
                            self.request['Connection'] = 'Keep-Alive'
                else:
                    close_it = 1
            else:
                pass

        if self.request.version == '1.1':
            if connection == 'close':
                close_it = 1
            else:
                if 'Content-Length' not in self.request:
                    if 'Transfer-Encoding' in self.request:
                        close_it = self.request['Transfer-Encoding'] == 'chunked' or 1
                    else:
                        if self.request.use_chunked:
                            self.request['Transfer-Encoding'] = 'chunked'
                            wrap_in_chunking = 1
                        else:
                            close_it = 1
        else:
            if self.request.version is None:
                close_it = 1
            else:
                outgoing_header = producers.simple_producerself.request.build_reply_header
                if close_it:
                    self.request['Connection'] = 'close'
                elif wrap_in_chunking:
                    outgoing_producer = producers.chunked_producerproducers.composite_producerself.request.outgoing
                    outgoing_producer = producers.composite_producer[
                     outgoing_header, outgoing_producer]
                else:
                    if PY2:
                        if len(self.request.outgoing) > 0:
                            body = self.request.outgoing[0]
                            if isinstance(body, unicode):
                                self.request.outgoing[0] = producers.simple_producerbody
                self.request.outgoing.insert(0, outgoing_header)
                outgoing_producer = producers.composite_producerself.request.outgoing
            self.request.channel.push_with_producerproducers.globbing_producerproducers.hooked_producer(outgoing_producer, self.request.log)
            self.request.channel.current_request = None
            if close_it:
                self.request.channel.close_when_done


class ViewContext:

    def __init__(self, **kw):
        self.__dict__.updatekw


class MeldView:
    content_type = 'text/html;charset=utf-8'
    delay = 0.5

    def __init__(self, context):
        self.context = context
        template = self.context.template
        if not os.path.isabstemplate:
            here = os.path.abspathos.path.dirname__file__
            template = os.path.join(here, template)
        self.root = templating.parse_xmltemplate
        self.callback = None

    def __call__(self):
        body = self.render
        if body is NOT_DONE_YET:
            return NOT_DONE_YET
        response = self.context.response
        headers = response['headers']
        headers['Content-Type'] = self.content_type
        headers['Pragma'] = 'no-cache'
        headers['Cache-Control'] = 'no-cache'
        headers['Expires'] = http_date.build_http_date0
        response['body'] = as_string(body)
        return response

    def render(self):
        pass

    def clone(self):
        return self.root.clone


class TailView(MeldView):

    def render(self):
        supervisord = self.context.supervisord
        form = self.context.form
        if 'processname' not in form:
            tail = 'No process name found'
            processname = None
        else:
            processname = form['processname']
            offset = 0
            limit = form.get('limit', '1024')
            limit = min(-1024, int(limit) * -1 if limit.isdigit else -1024)
            if not processname:
                tail = 'No process name found'
            else:
                rpcinterface = SupervisorNamespaceRPCInterface(supervisord)
            try:
                tail = rpcinterface.readProcessStdoutLog(processname, limit, offset)
            except RPCError as e:
                try:
                    if e.code == Faults.NO_FILE:
                        tail = 'No file for %s' % processname
                    else:
                        tail = 'ERROR: unexpected rpc fault [%d] %s' % (
                         e.code, e.text)
                finally:
                    e = None
                    del e

            else:
                root = self.clone
                title = root.findmeld'title'
                title.content('Supervisor tail of process %s' % processname)
                tailbody = root.findmeld'tailbody'
                tailbody.contenttail
                refresh_anchor = root.findmeld'refresh_anchor'
                if processname is not None:
                    refresh_anchor.attributes(href=('tail.html?processname=%s&limit=%s' % (
                     urllib.quoteprocessname, urllib.quotestr(abs(limit)))))
                else:
                    refresh_anchor.deparent
                return as_string(root.write_xhtmlstring)


class StatusView(MeldView):

    def actions_for_process(self, process):
        state = process.get_state
        processname = urllib.quotemake_namespec(process.group.config.name, process.config.name)
        start = {'name':'Start', 
         'href':'index.html?processname=%s&amp;action=start' % processname, 
         'target':None}
        restart = {'name':'Restart', 
         'href':'index.html?processname=%s&amp;action=restart' % processname, 
         'target':None}
        stop = {'name':'Stop', 
         'href':'index.html?processname=%s&amp;action=stop' % processname, 
         'target':None}
        clearlog = {'name':'Clear Log', 
         'href':'index.html?processname=%s&amp;action=clearlog' % processname, 
         'target':None}
        tailf = {'name':'Tail -f', 
         'href':'logtail/%s' % processname, 
         'target':'_blank'}
        if state == ProcessStates.RUNNING:
            actions = [
             restart, stop, clearlog, tailf]
        else:
            if state in (ProcessStates.STOPPED, ProcessStates.EXITED,
             ProcessStates.FATAL):
                actions = [
                 start, None, clearlog, tailf]
            else:
                actions = [
                 None, None, clearlog, tailf]
        return actions

    def css_class_for_state(self, state):
        if state == ProcessStates.RUNNING:
            return 'statusrunning'
        if state in (ProcessStates.FATAL, ProcessStates.BACKOFF):
            return 'statuserror'
        return 'statusnominal'

    def make_callback--- This code section failed: ---

 L. 285         0  LOAD_FAST                'self'
                2  LOAD_ATTR                context
                4  LOAD_ATTR                supervisord
                6  STORE_FAST               'supervisord'

 L. 289         8  LOAD_STR                 'supervisor'
               10  LOAD_GLOBAL              SupervisorNamespaceRPCInterface
               12  LOAD_FAST                'supervisord'
               14  CALL_FUNCTION_1       1  ''
               16  BUILD_TUPLE_2         2 
               18  STORE_FAST               'main'

 L. 290        20  LOAD_STR                 'system'
               22  LOAD_GLOBAL              SystemNamespaceRPCInterface
               24  LOAD_FAST                'main'
               26  BUILD_LIST_1          1 
               28  CALL_FUNCTION_1       1  ''
               30  BUILD_TUPLE_2         2 
               32  STORE_FAST               'system'

 L. 292        34  LOAD_GLOBAL              RootRPCInterface
               36  LOAD_FAST                'main'
               38  LOAD_FAST                'system'
               40  BUILD_LIST_2          2 
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'rpcinterface'

 L. 294        46  LOAD_FAST                'action'
            48_50  POP_JUMP_IF_FALSE   922  'to 922'

 L. 296        52  LOAD_FAST                'action'
               54  LOAD_STR                 'refresh'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    78  'to 78'

 L. 297        60  LOAD_CODE                <code_object donothing>
               62  LOAD_STR                 'StatusView.make_callback.<locals>.donothing'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               66  STORE_FAST               'donothing'

 L. 300        68  LOAD_CONST               0.05
               70  LOAD_FAST                'donothing'
               72  STORE_ATTR               delay

 L. 301        74  LOAD_FAST                'donothing'
               76  RETURN_VALUE     
             78_0  COME_FROM            58  '58'

 L. 303        78  LOAD_FAST                'action'
               80  LOAD_STR                 'stopall'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   118  'to 118'

 L. 304        86  LOAD_FAST                'rpcinterface'
               88  LOAD_ATTR                supervisor
               90  LOAD_METHOD              stopAllProcesses
               92  CALL_METHOD_0         0  ''
               94  STORE_DEREF              'callback'

 L. 305        96  LOAD_CLOSURE             'callback'
               98  BUILD_TUPLE_1         1 
              100  LOAD_CODE                <code_object stopall>
              102  LOAD_STR                 'StatusView.make_callback.<locals>.stopall'
              104  MAKE_FUNCTION_8          'closure'
              106  STORE_FAST               'stopall'

 L. 310       108  LOAD_CONST               0.05
              110  LOAD_FAST                'stopall'
              112  STORE_ATTR               delay

 L. 311       114  LOAD_FAST                'stopall'
              116  RETURN_VALUE     
            118_0  COME_FROM            84  '84'

 L. 313       118  LOAD_FAST                'action'
              120  LOAD_STR                 'restartall'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   172  'to 172'

 L. 314       126  LOAD_FAST                'rpcinterface'
              128  LOAD_ATTR                system
              130  LOAD_METHOD              multicall

 L. 315       132  LOAD_STR                 'methodName'
              134  LOAD_STR                 'supervisor.stopAllProcesses'
              136  BUILD_MAP_1           1 

 L. 316       138  LOAD_STR                 'methodName'
              140  LOAD_STR                 'supervisor.startAllProcesses'
              142  BUILD_MAP_1           1 

 L. 315       144  BUILD_LIST_2          2 

 L. 314       146  CALL_METHOD_1         1  ''
              148  STORE_DEREF              'callback'

 L. 317       150  LOAD_CLOSURE             'callback'
              152  BUILD_TUPLE_1         1 
              154  LOAD_CODE                <code_object restartall>
              156  LOAD_STR                 'StatusView.make_callback.<locals>.restartall'
              158  MAKE_FUNCTION_8          'closure'
              160  STORE_FAST               'restartall'

 L. 322       162  LOAD_CONST               0.05
              164  LOAD_FAST                'restartall'
              166  STORE_ATTR               delay

 L. 323       168  LOAD_FAST                'restartall'
              170  RETURN_VALUE     
            172_0  COME_FROM           124  '124'

 L. 325       172  LOAD_DEREF               'namespec'
          174_176  POP_JUMP_IF_FALSE   922  'to 922'

 L. 326       178  LOAD_CLOSURE             'namespec'
              180  BUILD_TUPLE_1         1 
              182  LOAD_CODE                <code_object wrong>
              184  LOAD_STR                 'StatusView.make_callback.<locals>.wrong'
              186  MAKE_FUNCTION_8          'closure'
              188  STORE_FAST               'wrong'

 L. 328       190  LOAD_CONST               0.05
              192  LOAD_FAST                'wrong'
              194  STORE_ATTR               delay

 L. 329       196  LOAD_GLOBAL              split_namespec
              198  LOAD_DEREF               'namespec'
              200  CALL_FUNCTION_1       1  ''
              202  UNPACK_SEQUENCE_2     2 
              204  STORE_FAST               'group_name'
              206  STORE_FAST               'process_name'

 L. 330       208  LOAD_FAST                'supervisord'
              210  LOAD_ATTR                process_groups
              212  LOAD_METHOD              get
              214  LOAD_FAST                'group_name'
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'group'

 L. 331       220  LOAD_FAST                'group'
              222  LOAD_CONST               None
              224  COMPARE_OP               is
              226  POP_JUMP_IF_FALSE   232  'to 232'

 L. 332       228  LOAD_FAST                'wrong'
              230  RETURN_VALUE     
            232_0  COME_FROM           226  '226'

 L. 333       232  LOAD_FAST                'group'
              234  LOAD_ATTR                processes
              236  LOAD_METHOD              get
              238  LOAD_FAST                'process_name'
              240  CALL_METHOD_1         1  ''
              242  STORE_FAST               'process'

 L. 334       244  LOAD_FAST                'process'
              246  LOAD_CONST               None
              248  COMPARE_OP               is
          250_252  POP_JUMP_IF_FALSE   258  'to 258'

 L. 335       254  LOAD_FAST                'wrong'
              256  RETURN_VALUE     
            258_0  COME_FROM           250  '250'

 L. 337       258  LOAD_FAST                'action'
              260  LOAD_STR                 'start'
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   526  'to 526'

 L. 338       268  SETUP_FINALLY       286  'to 286'

 L. 340       270  LOAD_FAST                'rpcinterface'
              272  LOAD_ATTR                supervisor
              274  LOAD_METHOD              startProcess
              276  LOAD_DEREF               'namespec'
              278  CALL_METHOD_1         1  ''

 L. 339       280  STORE_DEREF              'bool_or_callback'
              282  POP_BLOCK        
              284  JUMP_FORWARD        466  'to 466'
            286_0  COME_FROM_FINALLY   268  '268'

 L. 342       286  DUP_TOP          
              288  LOAD_GLOBAL              RPCError
              290  COMPARE_OP               exception-match
          292_294  POP_JUMP_IF_FALSE   464  'to 464'
              296  POP_TOP          
              298  STORE_FAST               'e'
              300  POP_TOP          
              302  SETUP_FINALLY       452  'to 452'

 L. 343       304  LOAD_FAST                'e'
              306  LOAD_ATTR                code
              308  LOAD_GLOBAL              Faults
              310  LOAD_ATTR                NO_FILE
              312  COMPARE_OP               ==
          314_316  POP_JUMP_IF_FALSE   324  'to 324'

 L. 344       318  LOAD_STR                 'no such file'
              320  STORE_DEREF              'msg'
              322  JUMP_FORWARD        420  'to 420'
            324_0  COME_FROM           314  '314'

 L. 345       324  LOAD_FAST                'e'
              326  LOAD_ATTR                code
              328  LOAD_GLOBAL              Faults
              330  LOAD_ATTR                NOT_EXECUTABLE
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   344  'to 344'

 L. 346       338  LOAD_STR                 'file not executable'
              340  STORE_DEREF              'msg'
              342  JUMP_FORWARD        420  'to 420'
            344_0  COME_FROM           334  '334'

 L. 347       344  LOAD_FAST                'e'
              346  LOAD_ATTR                code
              348  LOAD_GLOBAL              Faults
              350  LOAD_ATTR                ALREADY_STARTED
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   364  'to 364'

 L. 348       358  LOAD_STR                 'already started'
              360  STORE_DEREF              'msg'
              362  JUMP_FORWARD        420  'to 420'
            364_0  COME_FROM           354  '354'

 L. 349       364  LOAD_FAST                'e'
              366  LOAD_ATTR                code
              368  LOAD_GLOBAL              Faults
              370  LOAD_ATTR                SPAWN_ERROR
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   384  'to 384'

 L. 350       378  LOAD_STR                 'spawn error'
              380  STORE_DEREF              'msg'
              382  JUMP_FORWARD        420  'to 420'
            384_0  COME_FROM           374  '374'

 L. 351       384  LOAD_FAST                'e'
              386  LOAD_ATTR                code
              388  LOAD_GLOBAL              Faults
              390  LOAD_ATTR                ABNORMAL_TERMINATION
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   404  'to 404'

 L. 352       398  LOAD_STR                 'abnormal termination'
              400  STORE_DEREF              'msg'
              402  JUMP_FORWARD        420  'to 420'
            404_0  COME_FROM           394  '394'

 L. 354       404  LOAD_STR                 'unexpected rpc fault [%d] %s'

 L. 355       406  LOAD_FAST                'e'
              408  LOAD_ATTR                code

 L. 355       410  LOAD_FAST                'e'
              412  LOAD_ATTR                text

 L. 354       414  BUILD_TUPLE_2         2 
              416  BINARY_MODULO    
              418  STORE_DEREF              'msg'
            420_0  COME_FROM           402  '402'
            420_1  COME_FROM           382  '382'
            420_2  COME_FROM           362  '362'
            420_3  COME_FROM           342  '342'
            420_4  COME_FROM           322  '322'

 L. 356       420  LOAD_CLOSURE             'msg'
              422  LOAD_CLOSURE             'namespec'
              424  BUILD_TUPLE_2         2 
              426  LOAD_CODE                <code_object starterr>
              428  LOAD_STR                 'StatusView.make_callback.<locals>.starterr'
              430  MAKE_FUNCTION_8          'closure'
              432  STORE_FAST               'starterr'

 L. 358       434  LOAD_CONST               0.05
              436  LOAD_FAST                'starterr'
              438  STORE_ATTR               delay

 L. 359       440  LOAD_FAST                'starterr'
              442  ROT_FOUR         
              444  POP_BLOCK        
              446  POP_EXCEPT       
              448  CALL_FINALLY        452  'to 452'
              450  RETURN_VALUE     
            452_0  COME_FROM           448  '448'
            452_1  COME_FROM_FINALLY   302  '302'
              452  LOAD_CONST               None
              454  STORE_FAST               'e'
              456  DELETE_FAST              'e'
              458  END_FINALLY      
              460  POP_EXCEPT       
              462  JUMP_FORWARD        466  'to 466'
            464_0  COME_FROM           292  '292'
              464  END_FINALLY      
            466_0  COME_FROM           462  '462'
            466_1  COME_FROM           284  '284'

 L. 361       466  LOAD_GLOBAL              callable
              468  LOAD_DEREF               'bool_or_callback'
              470  CALL_FUNCTION_1       1  ''
          472_474  POP_JUMP_IF_FALSE   500  'to 500'

 L. 362       476  LOAD_CLOSURE             'bool_or_callback'
              478  LOAD_CLOSURE             'namespec'
              480  BUILD_TUPLE_2         2 
              482  LOAD_CODE                <code_object startprocess>
              484  LOAD_STR                 'StatusView.make_callback.<locals>.startprocess'
              486  MAKE_FUNCTION_8          'closure'
              488  STORE_FAST               'startprocess'

 L. 378       490  LOAD_CONST               0.05
              492  LOAD_FAST                'startprocess'
              494  STORE_ATTR               delay

 L. 379       496  LOAD_FAST                'startprocess'
              498  RETURN_VALUE     
            500_0  COME_FROM           472  '472'

 L. 381       500  LOAD_CLOSURE             'namespec'
              502  BUILD_TUPLE_1         1 
              504  LOAD_CODE                <code_object startdone>
              506  LOAD_STR                 'StatusView.make_callback.<locals>.startdone'
              508  MAKE_FUNCTION_8          'closure'
              510  STORE_FAST               'startdone'

 L. 383       512  LOAD_CONST               0.05
              514  LOAD_FAST                'startdone'
              516  STORE_ATTR               delay

 L. 384       518  LOAD_FAST                'startdone'
              520  RETURN_VALUE     
          522_524  JUMP_FORWARD        922  'to 922'
            526_0  COME_FROM           264  '264'

 L. 386       526  LOAD_FAST                'action'
              528  LOAD_STR                 'stop'
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   690  'to 690'

 L. 387       536  SETUP_FINALLY       554  'to 554'

 L. 389       538  LOAD_FAST                'rpcinterface'
              540  LOAD_ATTR                supervisor
              542  LOAD_METHOD              stopProcess
              544  LOAD_DEREF               'namespec'
              546  CALL_METHOD_1         1  ''

 L. 388       548  STORE_DEREF              'bool_or_callback'
              550  POP_BLOCK        
              552  JUMP_FORWARD        632  'to 632'
            554_0  COME_FROM_FINALLY   536  '536'

 L. 391       554  DUP_TOP          
              556  LOAD_GLOBAL              RPCError
              558  COMPARE_OP               exception-match
          560_562  POP_JUMP_IF_FALSE   630  'to 630'
              564  POP_TOP          
              566  STORE_FAST               'e'
              568  POP_TOP          
              570  SETUP_FINALLY       618  'to 618'

 L. 392       572  LOAD_STR                 'unexpected rpc fault [%d] %s'
              574  LOAD_FAST                'e'
              576  LOAD_ATTR                code
              578  LOAD_FAST                'e'
              580  LOAD_ATTR                text
              582  BUILD_TUPLE_2         2 
              584  BINARY_MODULO    
              586  STORE_DEREF              'msg'

 L. 393       588  LOAD_CLOSURE             'msg'
              590  BUILD_TUPLE_1         1 
              592  LOAD_CODE                <code_object stoperr>
              594  LOAD_STR                 'StatusView.make_callback.<locals>.stoperr'
              596  MAKE_FUNCTION_8          'closure'
              598  STORE_FAST               'stoperr'

 L. 395       600  LOAD_CONST               0.05
              602  LOAD_FAST                'stoperr'
              604  STORE_ATTR               delay

 L. 396       606  LOAD_FAST                'stoperr'
              608  ROT_FOUR         
              610  POP_BLOCK        
              612  POP_EXCEPT       
              614  CALL_FINALLY        618  'to 618'
              616  RETURN_VALUE     
            618_0  COME_FROM           614  '614'
            618_1  COME_FROM_FINALLY   570  '570'
              618  LOAD_CONST               None
              620  STORE_FAST               'e'
              622  DELETE_FAST              'e'
              624  END_FINALLY      
              626  POP_EXCEPT       
              628  JUMP_FORWARD        632  'to 632'
            630_0  COME_FROM           560  '560'
              630  END_FINALLY      
            632_0  COME_FROM           628  '628'
            632_1  COME_FROM           552  '552'

 L. 398       632  LOAD_GLOBAL              callable
              634  LOAD_DEREF               'bool_or_callback'
              636  CALL_FUNCTION_1       1  ''
          638_640  POP_JUMP_IF_FALSE   666  'to 666'

 L. 399       642  LOAD_CLOSURE             'bool_or_callback'
              644  LOAD_CLOSURE             'namespec'
              646  BUILD_TUPLE_2         2 
              648  LOAD_CODE                <code_object stopprocess>
              650  LOAD_STR                 'StatusView.make_callback.<locals>.stopprocess'
              652  MAKE_FUNCTION_8          'closure'
              654  STORE_FAST               'stopprocess'

 L. 408       656  LOAD_CONST               0.05
              658  LOAD_FAST                'stopprocess'
              660  STORE_ATTR               delay

 L. 409       662  LOAD_FAST                'stopprocess'
              664  RETURN_VALUE     
            666_0  COME_FROM           638  '638'

 L. 411       666  LOAD_CLOSURE             'namespec'
              668  BUILD_TUPLE_1         1 
              670  LOAD_CODE                <code_object stopdone>
              672  LOAD_STR                 'StatusView.make_callback.<locals>.stopdone'
              674  MAKE_FUNCTION_8          'closure'
              676  STORE_FAST               'stopdone'

 L. 413       678  LOAD_CONST               0.05
              680  LOAD_FAST                'stopdone'
              682  STORE_ATTR               delay

 L. 414       684  LOAD_FAST                'stopdone'
              686  RETURN_VALUE     
              688  JUMP_FORWARD        922  'to 922'
            690_0  COME_FROM           532  '532'

 L. 416       690  LOAD_FAST                'action'
              692  LOAD_STR                 'restart'
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   794  'to 794'

 L. 417       700  LOAD_FAST                'rpcinterface'
              702  LOAD_ATTR                system
              704  LOAD_METHOD              multicall

 L. 418       706  LOAD_STR                 'supervisor.stopProcess'

 L. 419       708  LOAD_DEREF               'namespec'
              710  BUILD_LIST_1          1 

 L. 418       712  LOAD_CONST               ('methodName', 'params')
              714  BUILD_CONST_KEY_MAP_2     2 

 L. 420       716  LOAD_STR                 'supervisor.startProcess'

 L. 421       718  LOAD_DEREF               'namespec'
              720  BUILD_LIST_1          1 

 L. 420       722  LOAD_CONST               ('methodName', 'params')
              724  BUILD_CONST_KEY_MAP_2     2 

 L. 418       726  BUILD_LIST_2          2 

 L. 417       728  CALL_METHOD_1         1  ''
              730  STORE_FAST               'results_or_callback'

 L. 424       732  LOAD_GLOBAL              callable
              734  LOAD_FAST                'results_or_callback'
              736  CALL_FUNCTION_1       1  ''
          738_740  POP_JUMP_IF_FALSE   770  'to 770'

 L. 425       742  LOAD_FAST                'results_or_callback'
              744  STORE_DEREF              'callback'

 L. 426       746  LOAD_CLOSURE             'callback'
              748  LOAD_CLOSURE             'namespec'
              750  BUILD_TUPLE_2         2 
              752  LOAD_CODE                <code_object restartprocess>
              754  LOAD_STR                 'StatusView.make_callback.<locals>.restartprocess'
              756  MAKE_FUNCTION_8          'closure'
              758  STORE_FAST               'restartprocess'

 L. 431       760  LOAD_CONST               0.05
              762  LOAD_FAST                'restartprocess'
              764  STORE_ATTR               delay

 L. 432       766  LOAD_FAST                'restartprocess'
              768  RETURN_VALUE     
            770_0  COME_FROM           738  '738'

 L. 434       770  LOAD_CLOSURE             'namespec'
              772  BUILD_TUPLE_1         1 
              774  LOAD_CODE                <code_object restartdone>
              776  LOAD_STR                 'StatusView.make_callback.<locals>.restartdone'
              778  MAKE_FUNCTION_8          'closure'
              780  STORE_FAST               'restartdone'

 L. 436       782  LOAD_CONST               0.05
              784  LOAD_FAST                'restartdone'
              786  STORE_ATTR               delay

 L. 437       788  LOAD_FAST                'restartdone'
              790  RETURN_VALUE     
              792  JUMP_FORWARD        922  'to 922'
            794_0  COME_FROM           696  '696'

 L. 439       794  LOAD_FAST                'action'
              796  LOAD_STR                 'clearlog'
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   922  'to 922'

 L. 440       804  SETUP_FINALLY       822  'to 822'

 L. 441       806  LOAD_FAST                'rpcinterface'
              808  LOAD_ATTR                supervisor
              810  LOAD_METHOD              clearProcessLogs

 L. 442       812  LOAD_DEREF               'namespec'

 L. 441       814  CALL_METHOD_1         1  ''
              816  STORE_DEREF              'callback'
              818  POP_BLOCK        
              820  JUMP_FORWARD        900  'to 900'
            822_0  COME_FROM_FINALLY   804  '804'

 L. 443       822  DUP_TOP          
              824  LOAD_GLOBAL              RPCError
              826  COMPARE_OP               exception-match
          828_830  POP_JUMP_IF_FALSE   898  'to 898'
              832  POP_TOP          
              834  STORE_FAST               'e'
              836  POP_TOP          
              838  SETUP_FINALLY       886  'to 886'

 L. 444       840  LOAD_STR                 'unexpected rpc fault [%d] %s'
              842  LOAD_FAST                'e'
              844  LOAD_ATTR                code
              846  LOAD_FAST                'e'
              848  LOAD_ATTR                text
              850  BUILD_TUPLE_2         2 
              852  BINARY_MODULO    
              854  STORE_DEREF              'msg'

 L. 445       856  LOAD_CLOSURE             'msg'
              858  BUILD_TUPLE_1         1 
              860  LOAD_CODE                <code_object clearerr>
              862  LOAD_STR                 'StatusView.make_callback.<locals>.clearerr'
              864  MAKE_FUNCTION_8          'closure'
              866  STORE_FAST               'clearerr'

 L. 447       868  LOAD_CONST               0.05
              870  LOAD_FAST                'clearerr'
              872  STORE_ATTR               delay

 L. 448       874  LOAD_FAST                'clearerr'
              876  ROT_FOUR         
              878  POP_BLOCK        
              880  POP_EXCEPT       
              882  CALL_FINALLY        886  'to 886'
              884  RETURN_VALUE     
            886_0  COME_FROM           882  '882'
            886_1  COME_FROM_FINALLY   838  '838'
              886  LOAD_CONST               None
              888  STORE_FAST               'e'
              890  DELETE_FAST              'e'
              892  END_FINALLY      
              894  POP_EXCEPT       
              896  JUMP_FORWARD        900  'to 900'
            898_0  COME_FROM           828  '828'
              898  END_FINALLY      
            900_0  COME_FROM           896  '896'
            900_1  COME_FROM           820  '820'

 L. 450       900  LOAD_CLOSURE             'namespec'
              902  BUILD_TUPLE_1         1 
              904  LOAD_CODE                <code_object clearlog>
              906  LOAD_STR                 'StatusView.make_callback.<locals>.clearlog'
              908  MAKE_FUNCTION_8          'closure'
              910  STORE_FAST               'clearlog'

 L. 452       912  LOAD_CONST               0.05
              914  LOAD_FAST                'clearlog'
              916  STORE_ATTR               delay

 L. 453       918  LOAD_FAST                'clearlog'
              920  RETURN_VALUE     
            922_0  COME_FROM           800  '800'
            922_1  COME_FROM           792  '792'
            922_2  COME_FROM           688  '688'
            922_3  COME_FROM           522  '522'
            922_4  COME_FROM           174  '174'
            922_5  COME_FROM            48  '48'

 L. 455       922  LOAD_GLOBAL              ValueError
              924  LOAD_FAST                'action'
              926  CALL_FUNCTION_1       1  ''
              928  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_BLOCK' instruction at offset 444

    def render(self):
        form = self.context.form
        response = self.context.response
        processname = form.get'processname'
        action = form.get'action'
        message = form.get'message'
        if action:
            if not self.callback:
                self.callback = self.make_callback(processname, action)
                return NOT_DONE_YET
            message = self.callback
            if message is NOT_DONE_YET:
                return NOT_DONE_YET
            if message is not None:
                server_url = form['SERVER_URL']
                location = server_url + '/' + '?message=%s' % urllib.quotemessage
                response['headers']['Location'] = location
        supervisord = self.context.supervisord
        rpcinterface = RootRPCInterface([
         (
          'supervisor',
          SupervisorNamespaceRPCInterface(supervisord))])
        processnames = []
        for group in supervisord.process_groups.values:
            for gprocname in group.processes.keys:
                processnames.append(group.config.name, gprocname)
            else:
                processnames.sort
                data = []
                for groupname, processname in processnames:
                    actions = self.actions_for_processsupervisord.process_groups[groupname].processes[processname]
                    sent_name = make_namespec(groupname, processname)
                    info = rpcinterface.supervisor.getProcessInfosent_name
                    data.append{'status':info['statename'], 
                     'name':processname, 
                     'group':groupname, 
                     'actions':actions, 
                     'state':info['state'], 
                     'description':info['description']}
                else:
                    root = self.clone
                    if message is not None:
                        statusarea = root.findmeld'statusmessage'
                        statusarea.attrib['class'] = 'status_msg'
                        statusarea.contentmessage
                    elif data:
                        iterator = root.findmeld'tr'.repeatdata
                        shaded_tr = False
                        for tr_element, item in iterator:
                            status_text = tr_element.findmeld'status_text'
                            status_text.contentitem['status'].lower
                            status_text.attrib['class'] = self.css_class_for_stateitem['state']
                            info_text = tr_element.findmeld'info_text'
                            info_text.contentitem['description']
                            anchor = tr_element.findmeld'name_anchor'
                            processname = make_namespec(item['group'], item['name'])
                            anchor.attributes(href=('tail.html?processname=%s' % urllib.quoteprocessname))
                            anchor.contentprocessname
                            actions = item['actions']
                            actionitem_td = tr_element.findmeld'actionitem_td'

                        for li_element, actionitem in actionitem_td.repeatactions:
                            anchor = li_element.findmeld'actionitem_anchor'
                            if actionitem is None:
                                anchor.attrib['class'] = 'hidden'
                            else:
                                anchor.attributes(href=(actionitem['href']), name=(actionitem['name']))
                                anchor.contentactionitem['name']
                                if actionitem['target']:
                                    anchor.attributes(target=(actionitem['target']))
                                if shaded_tr:
                                    tr_element.attrib['class'] = 'shade'
                                shaded_tr = not shaded_tr

                    else:
                        table = root.findmeld'statustable'
                        table.replace'No programs to manage'
                    root.findmeld'supervisor_version'.contentVERSION
                    copyright_year = str(datetime.date.today.year)
                    root.findmeld'copyright_date'.contentcopyright_year
                    return as_string(root.write_xhtmlstring)


class OKView:
    delay = 0

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return {'body': 'OK'}


VIEWS = {'index.html':{'template':'ui/status.html', 
  'view':StatusView}, 
 'tail.html':{'template':'ui/tail.html', 
  'view':TailView}, 
 'ok.html':{'template':None, 
  'view':OKView}}

class supervisor_ui_handler:
    IDENT = 'Supervisor Web UI HTTP Request Handler'

    def __init__(self, supervisord):
        self.supervisord = supervisord

    def match(self, request):
        if request.command not in ('POST', 'GET'):
            return False
        else:
            path, params, query, fragment = request.split_uri
            while True:
                if path.startswith'/':
                    path = path[1:]

        if not path:
            path = 'index.html'
        for viewname in VIEWS.keys:
            if viewname == path:
                return True

    def handle_request(self, request):
        if request.command == 'POST':
            request.collector = collector(self, request)
        else:
            self.continue_request('', request)

    def continue_request(self, data, request):
        form = {}
        cgi_env = request.cgi_environment
        form.updatecgi_env
        if 'QUERY_STRING' not in form:
            form['QUERY_STRING'] = ''
        query = form['QUERY_STRING']
        form_urlencoded = urlparse.parse_qsldata
        query_data = urlparse.parse_qsquery
        for k, v in query_data.items:
            form[k] = v[0]
        else:
            for k, v in form_urlencoded:
                form[k] = v
            else:
                form['SERVER_URL'] = request.get_server_url
                path = form['PATH_INFO']
                while path:
                    if path[0] == '/':
                        path = path[1:]

                if not path:
                    path = 'index.html'
                viewinfo = VIEWS.getpath
                if viewinfo is None:
                    return
                response = {'headers': {}}
                viewclass = viewinfo['view']
                viewtemplate = viewinfo['template']
                context = ViewContext(template=viewtemplate, request=request,
                  form=form,
                  response=response,
                  supervisord=(self.supervisord))
                view = viewclass(context)
                pushproducer = request.channel.push_with_producer
                pushproducer(DeferredWebProducer(request, view))