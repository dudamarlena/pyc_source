# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/xmlrpc.py
# Compiled at: 2019-09-16 13:23:54
# Size of source mod 2**32: 21532 bytes
import datetime, re, socket, sys, time, traceback, types
from xml.etree.ElementTree import iterparse
from supervisor.compat import xmlrpclib
from supervisor.compat import StringIO
from supervisor.compat import urllib
from supervisor.compat import as_bytes
from supervisor.compat import as_string
from supervisor.compat import encodestring
from supervisor.compat import decodestring
from supervisor.compat import httplib
from supervisor.compat import PY2
from supervisor.medusa.http_server import get_header
import supervisor.medusa.xmlrpc_handler as xmlrpc_handler
from supervisor.medusa import producers
from supervisor.http import NOT_DONE_YET

class Faults:
    UNKNOWN_METHOD = 1
    INCORRECT_PARAMETERS = 2
    BAD_ARGUMENTS = 3
    SIGNATURE_UNSUPPORTED = 4
    SHUTDOWN_STATE = 6
    BAD_NAME = 10
    BAD_SIGNAL = 11
    NO_FILE = 20
    NOT_EXECUTABLE = 21
    FAILED = 30
    ABNORMAL_TERMINATION = 40
    SPAWN_ERROR = 50
    ALREADY_STARTED = 60
    NOT_RUNNING = 70
    SUCCESS = 80
    ALREADY_ADDED = 90
    STILL_RUNNING = 91
    CANT_REREAD = 92


def getFaultDescription(code):
    for faultname in Faults.__dict__:
        if getattr(Faults, faultname) == code:
            return faultname
        return 'UNKNOWN'


class RPCError(Exception):

    def __init__(self, code, extra=None):
        self.code = code
        self.text = getFaultDescription(code)
        if extra is not None:
            self.text = '%s: %s' % (self.text, extra)

    def __str__(self):
        return 'code=%r, text=%r' % (self.code, self.text)


class DeferredXMLRPCResponse:
    __doc__ = ' A medusa producer that implements a deferred callback; requires\n    a subclass of asynchat.async_chat that handles NOT_DONE_YET sentinel '
    CONNECTION = re.compile('Connection: (.*)', re.IGNORECASE)

    def __init__(self, request, callback):
        self.callback = callback
        self.request = request
        self.finished = False
        self.delay = float(callback.delay)

    def more--- This code section failed: ---

 L.  74         0  LOAD_FAST                'self'
                2  LOAD_ATTR                finished
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L.  75         6  LOAD_STR                 ''
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L.  76        10  SETUP_FINALLY       118  'to 118'

 L.  77        12  SETUP_FINALLY        42  'to 42'

 L.  78        14  LOAD_FAST                'self'
               16  LOAD_METHOD              callback
               18  CALL_METHOD_0         0  ''
               20  STORE_FAST               'value'

 L.  79        22  LOAD_FAST                'value'
               24  LOAD_GLOBAL              NOT_DONE_YET
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L.  80        30  LOAD_GLOBAL              NOT_DONE_YET
               32  POP_BLOCK        
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM            28  '28'
               38  POP_BLOCK        
               40  JUMP_FORWARD         92  'to 92'
             42_0  COME_FROM_FINALLY    12  '12'

 L.  81        42  DUP_TOP          
               44  LOAD_GLOBAL              RPCError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    90  'to 90'
               50  POP_TOP          
               52  STORE_FAST               'err'
               54  POP_TOP          
               56  SETUP_FINALLY        78  'to 78'

 L.  82        58  LOAD_GLOBAL              xmlrpclib
               60  LOAD_METHOD              Fault
               62  LOAD_FAST                'err'
               64  LOAD_ATTR                code
               66  LOAD_FAST                'err'
               68  LOAD_ATTR                text
               70  CALL_METHOD_2         2  ''
               72  STORE_FAST               'value'
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM_FINALLY    56  '56'
               78  LOAD_CONST               None
               80  STORE_FAST               'err'
               82  DELETE_FAST              'err'
               84  END_FINALLY      
               86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
             90_0  COME_FROM            48  '48'
               90  END_FINALLY      
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            40  '40'

 L.  84        92  LOAD_GLOBAL              xmlrpc_marshal
               94  LOAD_FAST                'value'
               96  CALL_FUNCTION_1       1  ''
               98  STORE_FAST               'body'

 L.  86       100  LOAD_CONST               True
              102  LOAD_FAST                'self'
              104  STORE_ATTR               finished

 L.  88       106  LOAD_FAST                'self'
              108  LOAD_METHOD              getresponse
              110  LOAD_FAST                'body'
              112  CALL_METHOD_1         1  ''
              114  POP_BLOCK        
              116  RETURN_VALUE     
            118_0  COME_FROM_FINALLY    10  '10'

 L.  90       118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L.  91       124  LOAD_GLOBAL              traceback
              126  LOAD_METHOD              format_exc
              128  CALL_METHOD_0         0  ''
              130  STORE_FAST               'tb'

 L.  92       132  LOAD_FAST                'self'
              134  LOAD_ATTR                request
              136  LOAD_ATTR                channel
              138  LOAD_ATTR                server
              140  LOAD_ATTR                logger
              142  LOAD_METHOD              log

 L.  93       144  LOAD_STR                 'XML-RPC response callback error'

 L.  93       146  LOAD_FAST                'tb'

 L.  92       148  CALL_METHOD_2         2  ''
              150  POP_TOP          

 L.  95       152  LOAD_CONST               True
              154  LOAD_FAST                'self'
              156  STORE_ATTR               finished

 L.  96       158  LOAD_FAST                'self'
              160  LOAD_ATTR                request
              162  LOAD_METHOD              error
              164  LOAD_CONST               500
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  POP_EXCEPT       
              172  JUMP_FORWARD        176  'to 176'
              174  END_FINALLY      
            176_0  COME_FROM           172  '172'

Parse error at or near `POP_BLOCK' instruction at offset 34

    def getresponse(self, body):
        self.request['Content-Type'] = 'text/xml'
        self.request['Content-Length'] = len(body)
        self.request.pushbody
        connection = get_header(self.CONNECTION, self.request.header)
        close_it = 0
        if self.request.version == '1.0':
            if connection == 'keep-alive':
                self.request['Connection'] = 'Keep-Alive'
            else:
                close_it = 1
        elif self.request.version == '1.1':
            if connection == 'close':
                close_it = 1
        elif self.request.version is None:
            close_it = 1
        outgoing_header = producers.simple_producerself.request.build_reply_header
        if close_it:
            self.request['Connection'] = 'close'
        self.request.outgoing.insert(0, outgoing_header)
        outgoing_producer = producers.composite_producerself.request.outgoing
        self.request.channel.push_with_producerproducers.globbing_producerproducers.hooked_producer(outgoing_producer, self.request.log)
        self.request.channel.current_request = None
        if close_it:
            self.request.channel.close_when_done


def xmlrpc_marshal(value):
    ismethodresponse = not isinstance(value, xmlrpclib.Fault)
    if ismethodresponse:
        if not isinstance(value, tuple):
            value = (
             value,)
        body = xmlrpclib.dumps(value, methodresponse=ismethodresponse)
    else:
        body = xmlrpclib.dumpsvalue
    return body


class SystemNamespaceRPCInterface:

    def __init__(self, namespaces):
        self.namespaces = {}
        for name, inst in namespaces:
            self.namespaces[name] = inst
        else:
            self.namespaces['system'] = self

    def _listMethods(self):
        methods = {}
        for ns_name in self.namespaces:
            namespace = self.namespaces[ns_name]
            for method_name in namespace.__class__.__dict__:
                func = getattr(namespace, method_name)
                if callable(func):
                    sig = method_name.startswith'_' or '%s.%s' % (ns_name, method_name)
                    methods[sig] = str(func.__doc__)
            else:
                return methods

    def listMethods(self):
        """ Return an array listing the available method names

        @return array result  An array of method names available (strings).
        """
        methods = self._listMethods
        keys = list(methods.keys)
        keys.sort
        return keys

    def methodHelp(self, name):
        """ Return a string showing the method's documentation

        @param string name   The name of the method.
        @return string result The documentation for the method name.
        """
        methods = self._listMethods
        for methodname in methods.keys:
            if methodname == name:
                return methods[methodname]
        else:
            raise RPCError(Faults.SIGNATURE_UNSUPPORTED)

    def methodSignature(self, name):
        """ Return an array describing the method signature in the
        form [rtype, ptype, ptype...] where rtype is the return data type
        of the method, and ptypes are the parameter data types that the
        method accepts in method argument order.

        @param string name  The name of the method.
        @return array result  The result.
        """
        methods = self._listMethods
        for method in methods:
            if method == name:
                rtype = None
                ptypes = []
                parsed = gettags(methods[method])

        for thing in parsed:
            if thing[1] == 'return':
                rtype = thing[2]
            else:
                if thing[1] == 'param':
                    ptypes.appendthing[2]
                if rtype is None:
                    raise RPCError(Faults.SIGNATURE_UNSUPPORTED)
                return [
                 rtype] + ptypes
        else:
            raise RPCError(Faults.SIGNATURE_UNSUPPORTED)

    def multicall(self, calls):
        """Process an array of calls, and return an array of
        results. Calls should be structs of the form {'methodName':
        string, 'params': array}. Each result will either be a
        single-item array containing the result value, or a struct of
        the form {'faultCode': int, 'faultString': string}. This is
        useful when you need to make lots of small calls without lots
        of round trips.

        @param array calls  An array of call requests
        @return array result  An array of results
        """
        remaining_calls = calls[:]
        callbacks = []
        results = []

        def multi(remaining_calls=remaining_calls, callbacks=callbacks, results=results):
            if callbacks:
                try:
                    value = callbacks[0]()
                except RPCError as exc:
                    try:
                        value = {'faultCode':exc.code, 
                         'faultString':exc.text}
                    finally:
                        exc = None
                        del exc

                except:
                    info = sys.exc_info
                    errmsg = '%s:%s' % (info[0], info[1])
                    value = {'faultCode':Faults.FAILED,  'faultString':'FAILED: ' + errmsg}

            elif value is not NOT_DONE_YET:
                callbacks.pop0
                results.appendvalue
            else:
                while not callbacks:
                    if remaining_calls:
                        call = remaining_calls.pop0
                        name = call.get('methodName', None)
                        params = call.get('params', [])
                        try:
                            if name is None:
                                raise RPCError(Faults.INCORRECT_PARAMETERS, 'No methodName')
                            if name == 'system.multicall':
                                raise RPCError(Faults.INCORRECT_PARAMETERS, 'Recursive system.multicall forbidden')
                            root = AttrDict(self.namespaces)
                            value = traverse(root, name, params)
                        except RPCError as exc:
                            try:
                                value = {'faultCode':exc.code, 
                                 'faultString':exc.text}
                            finally:
                                exc = None
                                del exc

                        except:
                            info = sys.exc_info
                            errmsg = '%s:%s' % (info[0], info[1])
                            value = {'faultCode':Faults.FAILED,  'faultString':'FAILED: ' + errmsg}
                        else:
                            if isinstance(value, types.FunctionType):
                                callbacks.appendvalue
                    else:
                        results.appendvalue

            if callbacks or remaining_calls:
                return NOT_DONE_YET
            return results

        multi.delay = 0.05
        value = multi()
        if value is NOT_DONE_YET:
            return multi
        return value


class AttrDict(dict):

    def __getattr__(self, name):
        return self.getname


class RootRPCInterface:

    def __init__(self, subinterfaces):
        for name, rpcinterface in subinterfaces:
            setattr(self, name, rpcinterface)


def capped_int(value):
    i = int(value)
    if i < xmlrpclib.MININT:
        i = xmlrpclib.MININT
    else:
        if i > xmlrpclib.MAXINT:
            i = xmlrpclib.MAXINT
    return i


def make_datetime(text):
    return (datetime.datetime)(*time.strptime(text, '%Y%m%dT%H:%M:%S')[:6])


class supervisor_xmlrpc_handler(xmlrpc_handler):
    path = '/RPC2'
    IDENT = 'Supervisor XML-RPC Handler'
    unmarshallers = {'int':lambda x: int(x.text), 
     'i4':lambda x: int(x.text), 
     'boolean':lambda x: x.text == '1', 
     'string':lambda x: x.text or '', 
     'double':lambda x: float(x.text), 
     'dateTime.iso8601':lambda x: make_datetime(x.text), 
     'array':lambda x: x[0].text, 
     'data':lambda x: [v.text for v in x], 
     'struct':lambda x: dict([(k.text or '', v.text) for k, v in x]), 
     'base64':lambda x: as_string(decodestring(as_bytes(x.text or ''))), 
     'param':lambda x: x[0].text}

    def __init__(self, supervisord, subinterfaces):
        self.rpcinterface = RootRPCInterface(subinterfaces)
        self.supervisord = supervisord

    def loads(self, data):
        params = method = None
        for action, elem in iterparse(StringIO(data)):
            unmarshall = self.unmarshallers.getelem.tag
            if unmarshall:
                data = unmarshall(elem)
                elem.clear
                elem.text = data
            elif elem.tag == 'value':
                try:
                    data = elem[0].text
                except IndexError:
                    data = elem.text or ''
                else:
                    elem.clear
                    elem.text = data
            elif elem.tag == 'methodName':
                method = elem.text
            else:
                if elem.tag == 'params':
                    params = tuple([v.text for v in elem])
                return (
                 params, method)

    def match(self, request):
        return request.uri.startswithself.path

    def continue_request--- This code section failed: ---

 L. 375         0  LOAD_FAST                'self'
                2  LOAD_ATTR                supervisord
                4  LOAD_ATTR                options
                6  LOAD_ATTR                logger
                8  STORE_FAST               'logger'

 L. 377     10_12  SETUP_FINALLY       354  'to 354'

 L. 378        14  SETUP_FINALLY        50  'to 50'

 L. 383        16  LOAD_GLOBAL              PY2
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 384        20  LOAD_FAST                'data'
               22  LOAD_METHOD              encode
               24  LOAD_STR                 'ascii'
               26  LOAD_STR                 'xmlcharrefreplace'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'data'
             32_0  COME_FROM            18  '18'

 L. 385        32  LOAD_FAST                'self'
               34  LOAD_METHOD              loads
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'params'
               44  STORE_FAST               'method'
               46  POP_BLOCK        
               48  JUMP_FORWARD         92  'to 92'
             50_0  COME_FROM_FINALLY    14  '14'

 L. 386        50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 387        56  LOAD_FAST                'logger'
               58  LOAD_METHOD              error

 L. 388        60  LOAD_STR                 'XML-RPC request data %r is invalid: unmarshallable'

 L. 389        62  LOAD_FAST                'data'
               64  BUILD_TUPLE_1         1 

 L. 388        66  BINARY_MODULO    

 L. 387        68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 391        72  LOAD_FAST                'request'
               74  LOAD_METHOD              error
               76  LOAD_CONST               400
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 392        82  POP_EXCEPT       
               84  POP_BLOCK        
               86  LOAD_CONST               None
               88  RETURN_VALUE     
               90  END_FINALLY      
             92_0  COME_FROM            48  '48'

 L. 395        92  LOAD_FAST                'method'
               94  POP_JUMP_IF_TRUE    128  'to 128'

 L. 396        96  LOAD_FAST                'logger'
               98  LOAD_METHOD              error

 L. 397       100  LOAD_STR                 'XML-RPC request data %r is invalid: no method name'

 L. 398       102  LOAD_FAST                'data'
              104  BUILD_TUPLE_1         1 

 L. 397       106  BINARY_MODULO    

 L. 396       108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 400       112  LOAD_FAST                'request'
              114  LOAD_METHOD              error
              116  LOAD_CONST               400
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 401       122  POP_BLOCK        
              124  LOAD_CONST               None
              126  RETURN_VALUE     
            128_0  COME_FROM            94  '94'

 L. 405       128  LOAD_FAST                'params'
              130  LOAD_CONST               None
              132  COMPARE_OP               is
              134  POP_JUMP_IF_FALSE   140  'to 140'

 L. 406       136  LOAD_CONST               ()
              138  STORE_FAST               'params'
            140_0  COME_FROM           134  '134'

 L. 408       140  SETUP_FINALLY       186  'to 186'

 L. 409       142  LOAD_FAST                'logger'
              144  LOAD_METHOD              trace
              146  LOAD_STR                 'XML-RPC method called: %s()'
              148  LOAD_FAST                'method'
              150  BINARY_MODULO    
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 410       156  LOAD_FAST                'self'
              158  LOAD_METHOD              call
              160  LOAD_FAST                'method'
              162  LOAD_FAST                'params'
              164  CALL_METHOD_2         2  ''
              166  STORE_FAST               'value'

 L. 411       168  LOAD_FAST                'logger'
              170  LOAD_METHOD              trace
              172  LOAD_STR                 'XML-RPC method %s() returned successfully'

 L. 412       174  LOAD_FAST                'method'

 L. 411       176  BINARY_MODULO    
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          
              182  POP_BLOCK        
              184  JUMP_FORWARD        262  'to 262'
            186_0  COME_FROM_FINALLY   140  '140'

 L. 413       186  DUP_TOP          
              188  LOAD_GLOBAL              RPCError
              190  COMPARE_OP               exception-match
          192_194  POP_JUMP_IF_FALSE   260  'to 260'
              196  POP_TOP          
              198  STORE_FAST               'err'
              200  POP_TOP          
              202  SETUP_FINALLY       248  'to 248'

 L. 415       204  LOAD_GLOBAL              xmlrpclib
              206  LOAD_METHOD              Fault
              208  LOAD_FAST                'err'
              210  LOAD_ATTR                code
              212  LOAD_FAST                'err'
              214  LOAD_ATTR                text
              216  CALL_METHOD_2         2  ''
              218  STORE_FAST               'value'

 L. 416       220  LOAD_FAST                'logger'
              222  LOAD_METHOD              trace
              224  LOAD_STR                 'XML-RPC method %s() returned fault: [%d] %s'

 L. 417       226  LOAD_FAST                'method'

 L. 418       228  LOAD_FAST                'err'
              230  LOAD_ATTR                code

 L. 418       232  LOAD_FAST                'err'
              234  LOAD_ATTR                text

 L. 416       236  BUILD_TUPLE_3         3 
              238  BINARY_MODULO    
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          
              244  POP_BLOCK        
              246  BEGIN_FINALLY    
            248_0  COME_FROM_FINALLY   202  '202'
              248  LOAD_CONST               None
              250  STORE_FAST               'err'
              252  DELETE_FAST              'err'
              254  END_FINALLY      
              256  POP_EXCEPT       
              258  JUMP_FORWARD        262  'to 262'
            260_0  COME_FROM           192  '192'
              260  END_FINALLY      
            262_0  COME_FROM           258  '258'
            262_1  COME_FROM           184  '184'

 L. 420       262  LOAD_GLOBAL              isinstance
              264  LOAD_FAST                'value'
              266  LOAD_GLOBAL              types
              268  LOAD_ATTR                FunctionType
              270  CALL_FUNCTION_2       2  ''
          272_274  POP_JUMP_IF_FALSE   300  'to 300'

 L. 423       276  LOAD_FAST                'request'
              278  LOAD_ATTR                channel
              280  LOAD_ATTR                push_with_producer
              282  STORE_FAST               'pushproducer'

 L. 424       284  LOAD_FAST                'pushproducer'
              286  LOAD_GLOBAL              DeferredXMLRPCResponse
              288  LOAD_FAST                'request'
              290  LOAD_FAST                'value'
              292  CALL_FUNCTION_2       2  ''
              294  CALL_FUNCTION_1       1  ''
              296  POP_TOP          
              298  JUMP_FORWARD        350  'to 350'
            300_0  COME_FROM           272  '272'

 L. 430       300  LOAD_GLOBAL              as_bytes
              302  LOAD_GLOBAL              xmlrpc_marshal
              304  LOAD_FAST                'value'
              306  CALL_FUNCTION_1       1  ''
              308  CALL_FUNCTION_1       1  ''
              310  STORE_FAST               'body'

 L. 431       312  LOAD_STR                 'text/xml'
              314  LOAD_FAST                'request'
              316  LOAD_STR                 'Content-Type'
              318  STORE_SUBSCR     

 L. 432       320  LOAD_GLOBAL              len
              322  LOAD_FAST                'body'
              324  CALL_FUNCTION_1       1  ''
              326  LOAD_FAST                'request'
              328  LOAD_STR                 'Content-Length'
              330  STORE_SUBSCR     

 L. 433       332  LOAD_FAST                'request'
              334  LOAD_METHOD              push
              336  LOAD_FAST                'body'
              338  CALL_METHOD_1         1  ''
              340  POP_TOP          

 L. 434       342  LOAD_FAST                'request'
              344  LOAD_METHOD              done
              346  CALL_METHOD_0         0  ''
              348  POP_TOP          
            350_0  COME_FROM           298  '298'
              350  POP_BLOCK        
              352  JUMP_FORWARD        402  'to 402'
            354_0  COME_FROM_FINALLY    10  '10'

 L. 436       354  POP_TOP          
              356  POP_TOP          
              358  POP_TOP          

 L. 437       360  LOAD_GLOBAL              traceback
              362  LOAD_METHOD              format_exc
              364  CALL_METHOD_0         0  ''
              366  STORE_FAST               'tb'

 L. 438       368  LOAD_FAST                'logger'
              370  LOAD_METHOD              critical

 L. 439       372  LOAD_STR                 'Handling XML-RPC request with data %r raised an unexpected exception: %s'

 L. 440       374  LOAD_FAST                'data'
              376  LOAD_FAST                'tb'
              378  BUILD_TUPLE_2         2 

 L. 439       380  BINARY_MODULO    

 L. 438       382  CALL_METHOD_1         1  ''
              384  POP_TOP          

 L. 443       386  LOAD_FAST                'request'
              388  LOAD_METHOD              error
              390  LOAD_CONST               500
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
              396  POP_EXCEPT       
              398  JUMP_FORWARD        402  'to 402'
              400  END_FINALLY      
            402_0  COME_FROM           398  '398'
            402_1  COME_FROM           352  '352'

Parse error at or near `POP_BLOCK' instruction at offset 84

    def call(self, method, params):
        return traverse(self.rpcinterface, method, params)


def traverse--- This code section failed: ---

 L. 449         0  LOAD_FAST                'method'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '.'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'dotted_parts'

 L. 451        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'dotted_parts'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               2
               18  COMPARE_OP               !=
               20  POP_JUMP_IF_FALSE    32  'to 32'

 L. 452        22  LOAD_GLOBAL              RPCError
               24  LOAD_GLOBAL              Faults
               26  LOAD_ATTR                UNKNOWN_METHOD
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            20  '20'

 L. 453        32  LOAD_FAST                'dotted_parts'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'namespace'
               38  STORE_FAST               'method'

 L. 457        40  LOAD_FAST                'method'
               42  LOAD_METHOD              startswith
               44  LOAD_STR                 '_'
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 458        50  LOAD_GLOBAL              RPCError
               52  LOAD_GLOBAL              Faults
               54  LOAD_ATTR                UNKNOWN_METHOD
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            48  '48'

 L. 460        60  LOAD_GLOBAL              getattr
               62  LOAD_FAST                'ob'
               64  LOAD_FAST                'namespace'
               66  LOAD_CONST               None
               68  CALL_FUNCTION_3       3  ''
               70  STORE_FAST               'rpcinterface'

 L. 461        72  LOAD_FAST                'rpcinterface'
               74  LOAD_CONST               None
               76  COMPARE_OP               is
               78  POP_JUMP_IF_FALSE    90  'to 90'

 L. 462        80  LOAD_GLOBAL              RPCError
               82  LOAD_GLOBAL              Faults
               84  LOAD_ATTR                UNKNOWN_METHOD
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            78  '78'

 L. 464        90  LOAD_GLOBAL              getattr
               92  LOAD_FAST                'rpcinterface'
               94  LOAD_FAST                'method'
               96  LOAD_CONST               None
               98  CALL_FUNCTION_3       3  ''
              100  STORE_FAST               'func'

 L. 465       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'func'
              106  LOAD_GLOBAL              types
              108  LOAD_ATTR                MethodType
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_TRUE    124  'to 124'

 L. 466       114  LOAD_GLOBAL              RPCError
              116  LOAD_GLOBAL              Faults
              118  LOAD_ATTR                UNKNOWN_METHOD
              120  CALL_FUNCTION_1       1  ''
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM           112  '112'

 L. 468       124  SETUP_FINALLY       136  'to 136'

 L. 469       126  LOAD_FAST                'func'
              128  LOAD_FAST                'params'
              130  CALL_FUNCTION_EX      0  'positional arguments only'
              132  POP_BLOCK        
              134  RETURN_VALUE     
            136_0  COME_FROM_FINALLY   124  '124'

 L. 470       136  DUP_TOP          
              138  LOAD_GLOBAL              TypeError
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   164  'to 164'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 471       150  LOAD_GLOBAL              RPCError
              152  LOAD_GLOBAL              Faults
              154  LOAD_ATTR                INCORRECT_PARAMETERS
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
              160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           142  '142'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'

Parse error at or near `POP_TOP' instruction at offset 146


class SupervisorTransport(xmlrpclib.Transport):
    __doc__ = '\n    Provides a Transport for xmlrpclib that uses\n    httplib.HTTPConnection in order to support persistent\n    connections.  Also support basic auth and UNIX domain socket\n    servers.\n    '
    connection = None

    def __init__(self, username=None, password=None, serverurl=None):
        xmlrpclib.Transport.__init__self
        self.username = username
        self.password = password
        self.verbose = False
        self.serverurl = serverurl
        if serverurl.startswith'http://':
            type, uri = urllib.splittypeserverurl
            host, path = urllib.splithosturi
            host, port = urllib.splitporthost
            if port is None:
                port = 80
            else:
                port = int(port)

            def get_connection(host=host, port=port):
                return httplib.HTTPConnection(host, port)

            self._get_connection = get_connection
        else:
            if serverurl.startswith'unix://':

                def get_connection(serverurl=serverurl):
                    conn = UnixStreamHTTPConnection('localhost')
                    conn.socketfile = serverurl[7:]
                    return conn

                self._get_connection = get_connection
            else:
                raise ValueError('Unknown protocol for serverurl %s' % serverurl)

    def close(self):
        if self.connection:
            self.connection.close
            self.connection = None

    def request(self, host, handler, request_body, verbose=0):
        request_body = as_bytes(request_body)
        if not self.connection:
            self.connection = self._get_connection
            self.headers = {'User-Agent':self.user_agent, 
             'Content-Type':'text/xml', 
             'Accept':'text/xml'}
            if self.username is not None:
                if self.password is not None:
                    unencoded = '%s:%s' % (self.username, self.password)
                    encoded = as_string(encodestring(as_bytes(unencoded)))
                    encoded = encoded.replace('\n', '')
                    encoded = encoded.replace('\n', '')
                    self.headers['Authorization'] = 'Basic %s' % encoded
        self.headers['Content-Length'] = str(len(request_body))
        self.connection.request('POST', handler, request_body, self.headers)
        r = self.connection.getresponse
        if r.status != 200:
            self.connection.close
            self.connection = None
            raise xmlrpclib.ProtocolError(host + handler, r.status, r.reason, '')
        data = r.read
        data = as_string(data)
        data = data.encode('ascii', 'xmlcharrefreplace')
        p, u = self.getparser
        p.feeddata
        p.close
        return u.close


class UnixStreamHTTPConnection(httplib.HTTPConnection):

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connectself.socketfile


def gettags(comment):
    """ Parse documentation strings into JavaDoc-like tokens """
    tags = []
    tag = None
    datatype = None
    name = None
    tag_lineno = lineno = 0
    tag_text = []
    for line in comment.split'\n':
        line = line.strip
        if line.startswith'@':
            tags.append(tag_lineno, tag, datatype, name, '\n'.jointag_text)
            parts = line.split(None, 3)
            if len(parts) == 1:
                datatype = ''
                name = ''
                tag_text = []
            else:
                if len(parts) == 2:
                    datatype = parts[1]
                    name = ''
                    tag_text = []
                else:
                    if len(parts) == 3:
                        datatype = parts[1]
                        name = parts[2]
                        tag_text = []
                    else:
                        if len(parts) == 4:
                            datatype = parts[1]
                            name = parts[2]
                            tag_text = [parts[3].lstrip]
            tag = parts[0][1:]
            tag_lineno = lineno
        else:
            if line:
                tag_text.appendline
        lineno += 1
    else:
        tags.append(tag_lineno, tag, datatype, name, '\n'.jointag_text)
        return tags