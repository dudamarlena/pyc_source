# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\servers\HTTP.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 9879 bytes
import enum, logging, asyncio
from urllib.parse import urlparse
import base64
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import R3ConnectionClosed
from responder3.core.commons import *
from responder3.protocols.HTTP import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession
from responder3.protocols.authentication.loader import *

class HTTPProxy:

    def __init__(self):
        pass


class HTTPSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.server_mode = HTTPServerMode.CREDSTEALER
        self.current_state = HTTPState.UNAUTHENTICATED
        self.log_data = False
        self.parser = HTTPRequest
        self.http_version = HTTPVersion.HTTP11
        self.http_content_encoding = HTTPContentEncoding.IDENTITY
        self.http_connect_charset = 'utf8'
        self.auth_mecha = None
        self.auth_mecha_name = None
        self.http_cookie = None
        self.http_server_banner = None
        self.proxy_invisible = False
        self.proxy_ssl_intercept = False
        self.proxy_closed = asyncio.Event()
        self.close_session = asyncio.Event()

    def __repr__(self):
        t = '== HTTPSession ==\r\n'
        t += 'http_version:      %s\r\n' % repr(self.http_version)
        t += 'http_content_encoding: %s\r\n' % repr(self.http_content_encoding)
        t += 'http_connect_charset: %s\r\n' % repr(self.http_connect_charset)
        t += 'auth_mecha: %s\r\n' % repr(self.auth_mecha)
        t += 'http_cookie:       %s\r\n' % repr(self.http_cookie)
        t += 'http_server_banner: %s\r\n' % repr(self.http_server_banner)
        t += 'mode:     %s\r\n' % repr(self.server_mode)
        t += 'current_state:     %s\r\n' % repr(self.current_state)
        return t


class HTTP(ResponderServer):

    def init(self):
        self.parse_settings()

    def parse_settings(self):
        if self.settings is None:
            self.session.server_mode = HTTPServerMode.CREDSTEALER
            self.session.auth_mecha_name, self.session.auth_mecha = AuthMechaLoader.from_dict({'auth_mecha': 'NTLM'})
        else:
            if 'mode' in self.settings:
                self.session.server_mode = HTTPServerMode(self.settings['mode'].upper())
            if 'authentication' in self.settings:
                self.session.auth_mecha_name, self.session.auth_mecha = AuthMechaLoader.from_dict(self.settings['authentication'])

    async def parse_message(self, timeout=None):
        try:
            req = await asyncio.wait_for((self.session.parser.from_streamreader(self.creader)), timeout=timeout)
            return req
        except asyncio.TimeoutError:
            await self.log('Timeout!', logging.DEBUG)

    async def send_data(self, data):
        self.cwriter.write(data)
        await self.cwriter.drain()

    async def modify_data(self, data):
        return data

    async def proxy_forwarder(self, reader, writer, laddr, raddr):
        while not self.session.close_session.is_set():
            try:
                data = await asyncio.wait_for((reader.read(1024)), timeout=None)
            except asyncio.TimeoutError:
                await self.log('Timeout!', logging.DEBUG)
                self.session.close_session.set()
                break

            if data == b'' or reader.at_eof():
                await self.log('Connection closed!', logging.DEBUG)
                self.session.close_session.set()
                break
            modified_data = await self.modify_data(data)
            if modified_data != data:
                pass
            try:
                writer.write(modified_data)
                await asyncio.wait_for((writer.drain()), timeout=1)
            except asyncio.TimeoutError:
                await self.log('Timeout!', logging.DEBUG)
                self.session.close_session.set()
                break
            except OSError as e:
                try:
                    await self.log('Socket probably got closed!', logging.DEBUG)
                    self.session.close_session.set()
                    break
                finally:
                    e = None
                    del e

    async def httpproxy--- This code section failed: ---

 L. 123         0  LOAD_FAST                'req'
                2  LOAD_ATTR                method
                4  LOAD_STR                 'CONNECT'
                6  COMPARE_OP               ==
             8_10  POP_JUMP_IF_FALSE   452  'to 452'

 L. 124        12  LOAD_FAST                'req'
               14  LOAD_ATTR                uri
               16  LOAD_METHOD              split
               18  LOAD_STR                 ':'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'rhost'
               26  STORE_FAST               'rport'

 L. 126        28  LOAD_FAST                'self'
               30  LOAD_ATTR                session
               32  LOAD_ATTR                proxy_ssl_intercept
            34_36  POP_JUMP_IF_TRUE    296  'to 296'

 L. 128        38  SETUP_EXCEPT         82  'to 82'

 L. 129        40  LOAD_GLOBAL              asyncio
               42  LOAD_ATTR                wait_for
               44  LOAD_GLOBAL              asyncio
               46  LOAD_ATTR                open_connection
               48  LOAD_FAST                'rhost'
               50  LOAD_GLOBAL              int
               52  LOAD_FAST                'rport'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  LOAD_CONST               ('host', 'port')
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  LOAD_CONST               1
               62  LOAD_CONST               ('timeout',)
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  GET_AWAITABLE    
               68  LOAD_CONST               None
               70  YIELD_FROM       
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'remote_reader'
               76  STORE_FAST               'remote_writer'
               78  POP_BLOCK        
               80  JUMP_FORWARD        142  'to 142'
             82_0  COME_FROM_EXCEPT     38  '38'

 L. 130        82  DUP_TOP          
               84  LOAD_GLOBAL              Exception
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   140  'to 140'
               90  POP_TOP          
               92  STORE_FAST               'e'
               94  POP_TOP          
               96  SETUP_FINALLY       128  'to 128'

 L. 131        98  LOAD_FAST                'self'
              100  LOAD_ATTR                logger
              102  LOAD_METHOD              exception
              104  LOAD_STR                 'Failed to create remote connection to %s:%s!'
              106  LOAD_FAST                'rhost'
              108  LOAD_FAST                'rport'
              110  BUILD_TUPLE_2         2 
              112  BINARY_MODULO    
              114  CALL_METHOD_1         1  '1 positional argument'
              116  GET_AWAITABLE    
              118  LOAD_CONST               None
              120  YIELD_FROM       
              122  POP_TOP          

 L. 132       124  LOAD_CONST               None
              126  RETURN_VALUE     
            128_0  COME_FROM_FINALLY    96  '96'
              128  LOAD_CONST               None
              130  STORE_FAST               'e'
              132  DELETE_FAST              'e'
              134  END_FINALLY      
              136  POP_EXCEPT       
              138  JUMP_FORWARD        142  'to 142'
            140_0  COME_FROM            88  '88'
              140  END_FINALLY      
            142_0  COME_FROM           138  '138'
            142_1  COME_FROM            80  '80'

 L. 135       142  LOAD_GLOBAL              asyncio
              144  LOAD_ATTR                wait_for
              146  LOAD_FAST                'self'
              148  LOAD_METHOD              send_data
              150  LOAD_GLOBAL              HTTP200Resp
              152  CALL_FUNCTION_0       0  '0 positional arguments'
              154  LOAD_METHOD              to_bytes
              156  CALL_METHOD_0         0  '0 positional arguments'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  LOAD_CONST               1
              162  LOAD_CONST               ('timeout',)
              164  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              166  GET_AWAITABLE    
              168  LOAD_CONST               None
              170  YIELD_FROM       
              172  POP_TOP          

 L. 136       174  LOAD_FAST                'self'
              176  LOAD_ATTR                loop
              178  LOAD_METHOD              create_task
              180  LOAD_FAST                'self'
              182  LOAD_METHOD              proxy_forwarder
              184  LOAD_FAST                'remote_reader'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                cwriter
              190  LOAD_STR                 '%s:%d'
              192  LOAD_FAST                'rhost'
              194  LOAD_GLOBAL              int
              196  LOAD_FAST                'rport'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  BUILD_TUPLE_2         2 
              202  BINARY_MODULO    
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                session
              208  LOAD_ATTR                connection
              210  LOAD_METHOD              get_local_address
              212  CALL_METHOD_0         0  '0 positional arguments'
              214  CALL_METHOD_4         4  '4 positional arguments'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  POP_TOP          

 L. 137       220  LOAD_FAST                'self'
              222  LOAD_ATTR                loop
              224  LOAD_METHOD              create_task
              226  LOAD_FAST                'self'
              228  LOAD_METHOD              proxy_forwarder
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                creader
              234  LOAD_FAST                'remote_writer'
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                session
              240  LOAD_ATTR                connection
              242  LOAD_METHOD              get_local_address
              244  CALL_METHOD_0         0  '0 positional arguments'
              246  LOAD_STR                 '%s:%d'
              248  LOAD_FAST                'rhost'
              250  LOAD_GLOBAL              int
              252  LOAD_FAST                'rport'
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  BUILD_TUPLE_2         2 
              258  BINARY_MODULO    
              260  CALL_METHOD_4         4  '4 positional arguments'
              262  CALL_METHOD_1         1  '1 positional argument'
              264  POP_TOP          

 L. 138       266  LOAD_GLOBAL              asyncio
              268  LOAD_ATTR                wait_for
              270  LOAD_FAST                'self'
              272  LOAD_ATTR                session
              274  LOAD_ATTR                proxy_closed
              276  LOAD_METHOD              wait
              278  CALL_METHOD_0         0  '0 positional arguments'
              280  LOAD_CONST               None
              282  LOAD_CONST               ('timeout',)
              284  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              286  GET_AWAITABLE    
              288  LOAD_CONST               None
              290  YIELD_FROM       
              292  POP_TOP          
              294  JUMP_FORWARD        990  'to 990'
            296_0  COME_FROM            34  '34'

 L. 141       296  LOAD_GLOBAL              print
              298  LOAD_STR                 'a'
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  POP_TOP          

 L. 142       304  SETUP_LOOP          448  'to 448'
              306  LOAD_FAST                'self'
              308  LOAD_ATTR                session
              310  LOAD_ATTR                close_session
              312  LOAD_METHOD              is_set
              314  CALL_METHOD_0         0  '0 positional arguments'
          316_318  POP_JUMP_IF_TRUE    446  'to 446'

 L. 143       320  LOAD_GLOBAL              print
              322  LOAD_STR                 'aa'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  POP_TOP          

 L. 144       328  LOAD_FAST                'self'
              330  LOAD_ATTR                creader
              332  LOAD_METHOD              read
              334  LOAD_CONST               -1
              336  CALL_METHOD_1         1  '1 positional argument'
              338  GET_AWAITABLE    
              340  LOAD_CONST               None
              342  YIELD_FROM       
              344  STORE_FAST               'data'

 L. 145       346  LOAD_GLOBAL              print
              348  LOAD_STR                 '=====request======'
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  POP_TOP          

 L. 146       354  LOAD_GLOBAL              print
              356  LOAD_FAST                'data'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  POP_TOP          

 L. 150       362  LOAD_FAST                'remote_writer'
              364  LOAD_METHOD              write
              366  LOAD_FAST                'data'
              368  CALL_METHOD_1         1  '1 positional argument'
              370  POP_TOP          

 L. 151       372  LOAD_FAST                'remote_writer'
              374  LOAD_METHOD              drain
              376  CALL_METHOD_0         0  '0 positional arguments'
              378  GET_AWAITABLE    
              380  LOAD_CONST               None
              382  YIELD_FROM       
              384  POP_TOP          

 L. 153       386  LOAD_FAST                'remote_reader'
              388  LOAD_METHOD              read
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  GET_AWAITABLE    
              394  LOAD_CONST               None
              396  YIELD_FROM       
              398  STORE_FAST               'data_return'

 L. 154       400  LOAD_GLOBAL              print
              402  LOAD_STR                 '=======response==============='
              404  CALL_FUNCTION_1       1  '1 positional argument'
              406  POP_TOP          

 L. 155       408  LOAD_GLOBAL              print
              410  LOAD_FAST                'data_return'
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  POP_TOP          

 L. 157       416  LOAD_GLOBAL              asyncio
              418  LOAD_ATTR                wait_for
              420  LOAD_FAST                'self'
              422  LOAD_METHOD              send_data
              424  LOAD_FAST                'data_return'
              426  CALL_METHOD_1         1  '1 positional argument'
              428  LOAD_CONST               1
              430  LOAD_CONST               ('timeout',)
              432  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              434  GET_AWAITABLE    
              436  LOAD_CONST               None
              438  YIELD_FROM       
              440  POP_TOP          
          442_444  JUMP_BACK           306  'to 306'
            446_0  COME_FROM           316  '316'
              446  POP_BLOCK        
            448_0  COME_FROM_LOOP      304  '304'
          448_450  JUMP_FORWARD        990  'to 990'
            452_0  COME_FROM             8  '8'

 L. 162   452_454  SETUP_LOOP          990  'to 990'
              456  LOAD_FAST                'self'
              458  LOAD_ATTR                session
              460  LOAD_ATTR                close_session
              462  LOAD_METHOD              is_set
              464  CALL_METHOD_0         0  '0 positional arguments'
          466_468  POP_JUMP_IF_TRUE    988  'to 988'

 L. 163       470  LOAD_GLOBAL              urlparse
              472  LOAD_FAST                'req'
              474  LOAD_ATTR                uri
              476  CALL_FUNCTION_1       1  '1 positional argument'
              478  STORE_FAST               'o'

 L. 164       480  LOAD_FAST                'o'
              482  LOAD_ATTR                netloc
              484  LOAD_METHOD              find
              486  LOAD_STR                 ':'
              488  CALL_METHOD_1         1  '1 positional argument'
              490  LOAD_CONST               -1
              492  COMPARE_OP               !=
          494_496  POP_JUMP_IF_FALSE   516  'to 516'

 L. 165       498  LOAD_FAST                'o'
              500  LOAD_ATTR                netloc
              502  LOAD_METHOD              split
              504  LOAD_STR                 ':'
              506  CALL_METHOD_1         1  '1 positional argument'
              508  UNPACK_SEQUENCE_2     2 
              510  STORE_FAST               'rhost'
              512  STORE_FAST               'rport'
              514  JUMP_FORWARD        526  'to 526'
            516_0  COME_FROM           494  '494'

 L. 167       516  LOAD_FAST                'o'
              518  LOAD_ATTR                netloc
              520  STORE_FAST               'rhost'

 L. 168       522  LOAD_CONST               80
              524  STORE_FAST               'rport'
            526_0  COME_FROM           514  '514'

 L. 170       526  LOAD_FAST                'o'
              528  LOAD_ATTR                query
              530  LOAD_STR                 ''
              532  COMPARE_OP               !=
          534_536  POP_JUMP_IF_FALSE   558  'to 558'

 L. 171       538  LOAD_STR                 '?'
              540  LOAD_METHOD              join
              542  LOAD_FAST                'o'
              544  LOAD_ATTR                path
              546  LOAD_FAST                'o'
              548  LOAD_ATTR                query
              550  BUILD_LIST_2          2 
              552  CALL_METHOD_1         1  '1 positional argument'
              554  STORE_FAST               'uri'
              556  JUMP_FORWARD        564  'to 564'
            558_0  COME_FROM           534  '534'

 L. 173       558  LOAD_FAST                'o'
              560  LOAD_ATTR                path
              562  STORE_FAST               'uri'
            564_0  COME_FROM           556  '556'

 L. 176       564  LOAD_FAST                'req'
              566  LOAD_METHOD              remove_header
              568  LOAD_STR                 'proxy-authorization'
              570  CALL_METHOD_1         1  '1 positional argument'
              572  POP_TOP          

 L. 178       574  LOAD_GLOBAL              HTTPRequest
              576  LOAD_METHOD              construct
              578  LOAD_FAST                'req'
              580  LOAD_ATTR                method
              582  LOAD_FAST                'uri'
              584  LOAD_FAST                'req'
              586  LOAD_ATTR                headers
              588  LOAD_FAST                'req'
              590  LOAD_ATTR                body
              592  LOAD_FAST                'req'
              594  LOAD_ATTR                version
              596  CALL_METHOD_5         5  '5 positional arguments'
              598  STORE_FAST               'req_new'

 L. 179       600  LOAD_FAST                'self'
              602  LOAD_METHOD              log
              604  LOAD_STR                 '======== request sent ============'
              606  LOAD_GLOBAL              logging
              608  LOAD_ATTR                DEBUG
              610  CALL_METHOD_2         2  '2 positional arguments'
              612  GET_AWAITABLE    
              614  LOAD_CONST               None
              616  YIELD_FROM       
              618  POP_TOP          

 L. 182       620  SETUP_EXCEPT        664  'to 664'

 L. 183       622  LOAD_GLOBAL              asyncio
              624  LOAD_ATTR                wait_for
              626  LOAD_GLOBAL              asyncio
              628  LOAD_ATTR                open_connection
              630  LOAD_FAST                'rhost'
              632  LOAD_GLOBAL              int
              634  LOAD_FAST                'rport'
              636  CALL_FUNCTION_1       1  '1 positional argument'
              638  LOAD_CONST               ('host', 'port')
              640  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              642  LOAD_CONST               1
              644  LOAD_CONST               ('timeout',)
              646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              648  GET_AWAITABLE    
              650  LOAD_CONST               None
              652  YIELD_FROM       
              654  UNPACK_SEQUENCE_2     2 
              656  STORE_FAST               'remote_reader'
              658  STORE_FAST               'remote_writer'
              660  POP_BLOCK        
              662  JUMP_FORWARD        716  'to 716'
            664_0  COME_FROM_EXCEPT    620  '620'

 L. 184       664  DUP_TOP          
              666  LOAD_GLOBAL              Exception
              668  COMPARE_OP               exception-match
          670_672  POP_JUMP_IF_FALSE   714  'to 714'
              674  POP_TOP          
              676  STORE_FAST               'e'
              678  POP_TOP          
              680  SETUP_FINALLY       702  'to 702'

 L. 185       682  LOAD_FAST                'self'
              684  LOAD_ATTR                logger
              686  LOAD_METHOD              exception
              688  CALL_METHOD_0         0  '0 positional arguments'
              690  GET_AWAITABLE    
              692  LOAD_CONST               None
              694  YIELD_FROM       
              696  POP_TOP          

 L. 186       698  LOAD_CONST               None
              700  RETURN_VALUE     
            702_0  COME_FROM_FINALLY   680  '680'
              702  LOAD_CONST               None
              704  STORE_FAST               'e'
              706  DELETE_FAST              'e'
              708  END_FINALLY      
              710  POP_EXCEPT       
              712  JUMP_FORWARD        716  'to 716'
            714_0  COME_FROM           670  '670'
              714  END_FINALLY      
            716_0  COME_FROM           712  '712'
            716_1  COME_FROM           662  '662'

 L. 190       716  LOAD_FAST                'remote_writer'
              718  LOAD_METHOD              write
              720  LOAD_FAST                'req_new'
              722  LOAD_METHOD              to_bytes
              724  CALL_METHOD_0         0  '0 positional arguments'
              726  CALL_METHOD_1         1  '1 positional argument'
              728  POP_TOP          

 L. 191       730  LOAD_FAST                'remote_writer'
              732  LOAD_METHOD              drain
              734  CALL_METHOD_0         0  '0 positional arguments'
              736  GET_AWAITABLE    
              738  LOAD_CONST               None
              740  YIELD_FROM       
              742  POP_TOP          

 L. 193       744  LOAD_GLOBAL              asyncio
              746  LOAD_ATTR                wait_for
              748  LOAD_GLOBAL              HTTPResponse
              750  LOAD_METHOD              from_streamreader
              752  LOAD_FAST                'remote_reader'
              754  CALL_METHOD_1         1  '1 positional argument'
              756  LOAD_CONST               1
              758  LOAD_CONST               ('timeout',)
              760  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              762  GET_AWAITABLE    
              764  LOAD_CONST               None
              766  YIELD_FROM       
              768  STORE_FAST               'resp'

 L. 194       770  LOAD_FAST                'self'
              772  LOAD_METHOD              log
              774  LOAD_STR                 '=== proxyying response ===='
              776  LOAD_GLOBAL              logging
              778  LOAD_ATTR                DEBUG
              780  CALL_METHOD_2         2  '2 positional arguments'
              782  GET_AWAITABLE    
              784  LOAD_CONST               None
              786  YIELD_FROM       
              788  POP_TOP          

 L. 195       790  LOAD_GLOBAL              asyncio
              792  LOAD_ATTR                wait_for
              794  LOAD_FAST                'self'
              796  LOAD_METHOD              send_data
              798  LOAD_FAST                'resp'
              800  LOAD_METHOD              to_bytes
              802  CALL_METHOD_0         0  '0 positional arguments'
              804  CALL_METHOD_1         1  '1 positional argument'
              806  LOAD_CONST               None
              808  LOAD_CONST               ('timeout',)
              810  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              812  GET_AWAITABLE    
              814  LOAD_CONST               None
              816  YIELD_FROM       
              818  POP_TOP          

 L. 197       820  LOAD_FAST                'self'
              822  LOAD_METHOD              log
              824  LOAD_STR                 '=== PROXY === \r\n %s \r\n %s ======'
              826  LOAD_FAST                'req_new'
              828  LOAD_FAST                'resp'
              830  BUILD_TUPLE_2         2 
              832  BINARY_MODULO    
            834_0  COME_FROM           294  '294'
              834  CALL_METHOD_1         1  '1 positional argument'
              836  GET_AWAITABLE    
              838  LOAD_CONST               None
              840  YIELD_FROM       
              842  POP_TOP          

 L. 199       844  LOAD_FAST                'req'
              846  LOAD_ATTR                props
              848  LOAD_ATTR                connection
              850  LOAD_CONST               None
              852  COMPARE_OP               is-not
          854_856  POP_JUMP_IF_FALSE   930  'to 930'
              858  LOAD_FAST                'req'
              860  LOAD_ATTR                props
              862  LOAD_ATTR                connection
              864  LOAD_GLOBAL              HTTPConnection
              866  LOAD_ATTR                KEEP_ALIVE
              868  COMPARE_OP               ==
          870_872  POP_JUMP_IF_FALSE   930  'to 930'

 L. 200       874  LOAD_GLOBAL              asyncio
              876  LOAD_ATTR                wait_for
              878  LOAD_FAST                'self'
              880  LOAD_ATTR                parse_message
              882  LOAD_CONST               None
              884  LOAD_CONST               ('timeout',)
              886  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              888  LOAD_CONST               None
              890  LOAD_CONST               ('timeout',)
              892  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              894  GET_AWAITABLE    
              896  LOAD_CONST               None
              898  YIELD_FROM       
              900  STORE_FAST               'req'

 L. 201       902  LOAD_FAST                'req'
              904  LOAD_CONST               None
              906  COMPARE_OP               is
          908_910  POP_JUMP_IF_FALSE   984  'to 984'

 L. 202       912  LOAD_FAST                'self'
              914  LOAD_ATTR                session
              916  LOAD_ATTR                close_session
              918  LOAD_METHOD              set
              920  CALL_METHOD_0         0  '0 positional arguments'
              922  POP_TOP          

 L. 203       924  LOAD_CONST               None
              926  RETURN_VALUE     
              928  JUMP_BACK           456  'to 456'
            930_0  COME_FROM           870  '870'
            930_1  COME_FROM           854  '854'

 L. 205       930  LOAD_FAST                'self'
              932  LOAD_METHOD              log
              934  LOAD_STR                 'Closing connection!'
              936  LOAD_GLOBAL              logging
              938  LOAD_ATTR                DEBUG
              940  CALL_METHOD_2         2  '2 positional arguments'
              942  GET_AWAITABLE    
              944  LOAD_CONST               None
              946  YIELD_FROM       
              948  POP_TOP          

 L. 206       950  LOAD_FAST                'self'
              952  LOAD_ATTR                session
              954  LOAD_ATTR                close_session
              956  LOAD_METHOD              set
              958  CALL_METHOD_0         0  '0 positional arguments'
              960  POP_TOP          

 L. 207       962  LOAD_FAST                'remote_writer'
              964  LOAD_METHOD              close
              966  CALL_METHOD_0         0  '0 positional arguments'
              968  POP_TOP          

 L. 208       970  LOAD_FAST                'self'
              972  LOAD_ATTR                cwriter
              974  LOAD_METHOD              close
              976  CALL_METHOD_0         0  '0 positional arguments'
              978  POP_TOP          

 L. 209       980  LOAD_CONST               None
              982  RETURN_VALUE     
            984_0  COME_FROM           908  '908'
          984_986  JUMP_BACK           456  'to 456'
            988_0  COME_FROM           466  '466'
              988  POP_BLOCK        
            990_0  COME_FROM_LOOP      452  '452'
            990_1  COME_FROM           448  '448'

Parse error at or near `COME_FROM' instruction at offset 834_0

    @r3trafficlogexception
    async def run(self):
        while self.shutdown_evt.is_set():
            if not self.session.close_session.is_set():
                try:
                    result = await (asyncio.gather)(*[asyncio.wait_for((self.session.parser.from_streamreader(self.creader)), timeout=None)], **{'return_exceptions': True})
                except asyncio.CancelledError as e:
                    try:
                        raise e
                    finally:
                        e = None
                        del e

                if isinstance(result[0], R3ConnectionClosed):
                    return
                elif isinstance(result[0], Exception):
                    raise result[0]
                else:
                    req = result[0]
                if self.session.current_state == HTTPState.UNAUTHENTICATED:
                    if self.session.auth_mecha is None:
                        self.session.current_state = HTTPState.AUTHENTICATED
                if self.session.current_state == HTTPState.UNAUTHENTICATED:
                    auth_header_key = 'Authorization' if self.session.server_mode != HTTPServerMode.PROXY else 'Proxy-Authorization'
                    authline = req.headers.get(auth_header_key)
                    authdata = None
                    if authline:
                        m = authline.find(' ')
                        authdata = authline[m + 1:]
                        if authline:
                            if self.session.auth_mecha_name == AuthMecha.NTLM:
                                authdata = base64.b64decode(authdata)
                if self.session.auth_mecha_name == AuthMecha.NTLM:
                    if authdata is None:
                        if self.session.server_mode == HTTPServerMode.PROXY:
                            await self.send_data(HTTP407Resp('NTLM').to_bytes())
                    else:
                        await self.send_data(HTTP401Resp('NTLM').to_bytes())
                        continue
                else:
                    status, data = self.session.auth_mecha.do_auth(authdata)
                if not status == AuthResult.OK:
                    if status == AuthResult.FAIL:
                        await self.logger.credential(data.to_credential())
                    if status == AuthResult.OK:
                        self.session.current_state = HTTPState.AUTHENTICATED
                        if self.session.server_mode == HTTPServerMode.PROXY:
                            await self.httpproxy(req)
                        else:
                            await self.send_data(HTTP200Resp.to_bytes())
                            return
                else:
                    if status == AuthResult.FAIL:
                        self.session.current_state = HTTPState.AUTHFAILED
                        await self.send_data(HTTP403Resp('Auth failed!').to_bytes())
                        return
                    if status == AuthResult.CONTINUE:
                        rdata = self.session.auth_mecha_name.name
                        if data is not None:
                            if self.session.auth_mecha_name == AuthMecha.NTLM:
                                rdata += ' %s' % base64.b64encode(data).decode()
                            else:
                                rdata += ' %s' % data
                        if self.session.server_mode == HTTPServerMode.PROXY:
                            await self.send_data(HTTP407Resp(rdata).to_bytes())
            else:
                await self.send_data(HTTP401Resp(rdata).to_bytes())
                continue