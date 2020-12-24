# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\responder3\servers\SMB.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 11949 bytes
import logging, asyncio
from urllib.parse import urlparse
import uuid, random
from responder3.core.logging.logger import *
from responder3.core.asyncio_helpers import *
from responder3.core.commons import *
import responder3.protocols.SMB.SMBTransport as SMBTransport
from responder3.protocols.SMB.SMB import *
from responder3.protocols.SMB.SMB2 import *
from responder3.protocols.SMB.ntstatus import *
from responder3.protocols.authentication.GSSAPI import *
from responder3.protocols.authentication.common import *
from responder3.core.servertemplate import ResponderServer, ResponderServerSession

class SMB2ServerState(enum.Enum):
    UNAUTHENTICATED = enum.auto()
    AUTHENTICATED = enum.auto()


class SMBSession(ResponderServerSession):

    def __init__(self, connection, log_queue):
        ResponderServerSession.__init__(self, connection, log_queue, self.__class__.__name__)
        self.parser = SMBTransport
        self.SMBprotocol = None
        self.SMBdialect = [
         'SMB 2.002', 'NT LM 0.12']
        self.commondialect = None
        self.current_state = SMB2ServerState.UNAUTHENTICATED
        self.gssapihandler = GSSAPIAuthHandler()
        self.serverUUID = uuid.UUID(bytes=(os.urandom(16)))
        self.SMBSessionID = os.urandom(8)
        self.SMBMessageCnt = 0

    def __repr__(self):
        t = '== SMBSession ==\r\n'
        t += 'SMBprotocol:      %s\r\n' % repr(self.SMBprotocol)
        t += 'SMBdialect: %s\r\n' % repr(self.SMBdialect)
        t += 'commondialect: %s\r\n' % repr(self.commondialect)
        t += 'current_state: %s\r\n' % repr(self.current_state)
        t += 'gssapihandler:       %s\r\n' % repr(self.gssapihandler)
        t += 'serverUUID: %s\r\n' % repr(self.serverUUID)
        t += 'SMBSessionID:     %s\r\n' % repr(self.SMBSessionID)
        t += 'SMBMessageCnt:     %s\r\n' % repr(self.SMBMessageCnt)
        return t


class SMB(ResponderServer):

    def init(self):
        if self.settings:
            self.parse_settings()
            return
        self.set_default_settings()

    def set_default_settings(self):
        pass

    def parse_settings(self):
        self.set_default_settings()

    async def parse_message(self, timeout=10):
        try:
            smbtransport = await asyncio.wait_for((self.session.parser.from_streamreader(self.creader)), timeout=timeout)
            return smbtransport.smbmessage
        except asyncio.TimeoutError:
            await self.log('Timeout!', logging.DEBUG)

    async def send_data(self, smbmessage):
        data = self.session.parser.construct(smbmessage)
        self.cwriter.write(data.to_bytes())
        await self.cwriter.drain()

    async def send_authfailed(self, smbmessage):
        pass

    @r3trafficlogexception
    async def run--- This code section failed: ---

 L.  86       0_2  SETUP_LOOP         1646  'to 1646'
              4_0  COME_FROM          1632  '1632'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                shutdown_evt
                8  LOAD_METHOD              is_set
               10  CALL_METHOD_0         0  '0 positional arguments'
            12_14  POP_JUMP_IF_TRUE   1644  'to 1644'

 L.  87        16  SETUP_EXCEPT         68  'to 68'

 L.  88        18  LOAD_GLOBAL              asyncio
               20  LOAD_ATTR                gather
               22  LOAD_GLOBAL              asyncio
               24  LOAD_ATTR                wait_for
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                session
               30  LOAD_ATTR                parser
               32  LOAD_METHOD              from_streamreader
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                creader
               38  CALL_METHOD_1         1  '1 positional argument'
               40  LOAD_CONST               None
               42  LOAD_CONST               ('timeout',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  BUILD_LIST_1          1 
               48  LOAD_STR                 'return_exceptions'
               50  LOAD_CONST               True
               52  BUILD_MAP_1           1 
               54  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               56  GET_AWAITABLE    
               58  LOAD_CONST               None
               60  YIELD_FROM       
               62  STORE_FAST               'result'
               64  POP_BLOCK        
               66  JUMP_FORWARD        108  'to 108'
             68_0  COME_FROM_EXCEPT     16  '16'

 L.  89        68  DUP_TOP          
               70  LOAD_GLOBAL              asyncio
               72  LOAD_ATTR                CancelledError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE   106  'to 106'
               78  POP_TOP          
               80  STORE_FAST               'e'
               82  POP_TOP          
               84  SETUP_FINALLY        94  'to 94'

 L.  90        86  LOAD_FAST                'e'
               88  RAISE_VARARGS_1       1  'exception instance'
               90  POP_BLOCK        
               92  LOAD_CONST               None
             94_0  COME_FROM_FINALLY    84  '84'
               94  LOAD_CONST               None
               96  STORE_FAST               'e'
               98  DELETE_FAST              'e'
              100  END_FINALLY      
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            76  '76'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            66  '66'

 L.  91       108  LOAD_GLOBAL              isinstance
              110  LOAD_FAST                'result'
              112  LOAD_CONST               0
              114  BINARY_SUBSCR    
              116  LOAD_GLOBAL              R3ConnectionClosed
              118  CALL_FUNCTION_2       2  '2 positional arguments'
              120  POP_JUMP_IF_FALSE   126  'to 126'

 L.  92       122  LOAD_CONST               None
              124  RETURN_VALUE     
            126_0  COME_FROM           120  '120'

 L.  93       126  LOAD_GLOBAL              isinstance
              128  LOAD_FAST                'result'
              130  LOAD_CONST               0
              132  BINARY_SUBSCR    
              134  LOAD_GLOBAL              Exception
              136  CALL_FUNCTION_2       2  '2 positional arguments'
              138  POP_JUMP_IF_FALSE   150  'to 150'

 L.  94       140  LOAD_FAST                'result'
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  RAISE_VARARGS_1       1  'exception instance'
              148  JUMP_FORWARD        160  'to 160'
            150_0  COME_FROM           138  '138'

 L.  96       150  LOAD_FAST                'result'
              152  LOAD_CONST               0
              154  BINARY_SUBSCR    
              156  LOAD_ATTR                smbmessage
              158  STORE_FAST               'msg'
            160_0  COME_FROM           148  '148'

 L.  98       160  LOAD_FAST                'self'
              162  LOAD_ATTR                session
              164  LOAD_ATTR                current_state
              166  LOAD_GLOBAL              SMB2ServerState
              168  LOAD_ATTR                UNAUTHENTICATED
              170  COMPARE_OP               ==
          172_174  POP_JUMP_IF_FALSE  1620  'to 1620'

 L. 100       176  LOAD_FAST                'msg'
              178  LOAD_ATTR                type
              180  LOAD_CONST               1
              182  COMPARE_OP               ==
          184_186  POP_JUMP_IF_FALSE  1322  'to 1322'

 L. 101       188  LOAD_FAST                'msg'
              190  LOAD_ATTR                header
              192  LOAD_ATTR                Command
              194  LOAD_GLOBAL              SMBCommand
              196  LOAD_ATTR                SMB_COM_NEGOTIATE
              198  COMPARE_OP               ==
          200_202  POP_JUMP_IF_FALSE   806  'to 806'

 L. 103       204  LOAD_FAST                'self'
              206  LOAD_ATTR                logger
              208  LOAD_METHOD              debug
              210  LOAD_LISTCOMP            '<code_object <listcomp>>'
              212  LOAD_STR                 'SMB.run.<locals>.<listcomp>'
              214  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              216  LOAD_FAST                'msg'
              218  LOAD_ATTR                command
              220  LOAD_ATTR                Dialects
              222  GET_ITER         
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  GET_AWAITABLE    
              230  LOAD_CONST               None
              232  YIELD_FROM       
              234  POP_TOP          

 L. 105       236  LOAD_GLOBAL              set
              238  LOAD_LISTCOMP            '<code_object <listcomp>>'
              240  LOAD_STR                 'SMB.run.<locals>.<listcomp>'
              242  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              244  LOAD_FAST                'msg'
              246  LOAD_ATTR                command
              248  LOAD_ATTR                Dialects
              250  GET_ITER         
              252  CALL_FUNCTION_1       1  '1 positional argument'
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  STORE_FAST               'clinet_dialects'

 L. 106       258  LOAD_GLOBAL              set
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                session
              264  LOAD_ATTR                SMBdialect
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  STORE_FAST               'server_dialects'

 L. 107       270  LOAD_FAST                'server_dialects'
              272  LOAD_METHOD              intersection
              274  LOAD_FAST                'clinet_dialects'
              276  CALL_METHOD_1         1  '1 positional argument'
              278  STORE_FAST               'common_dialects'

 L. 108       280  LOAD_FAST                'common_dialects'
              282  LOAD_CONST               None
              284  COMPARE_OP               is
          286_288  POP_JUMP_IF_FALSE   312  'to 312'

 L. 109       290  LOAD_FAST                'self'
              292  LOAD_ATTR                logger
              294  LOAD_METHOD              info
              296  LOAD_STR                 'No matching dialects between client and server, terminating connection!'
              298  CALL_METHOD_1         1  '1 positional argument'
              300  GET_AWAITABLE    
              302  LOAD_CONST               None
              304  YIELD_FROM       
              306  POP_TOP          

 L. 110       308  LOAD_CONST               None
              310  RETURN_VALUE     
            312_0  COME_FROM           286  '286'

 L. 111       312  LOAD_CONST               None
              314  STORE_FAST               'preferred_dialect'

 L. 112       316  SETUP_LOOP          374  'to 374'
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                session
              322  LOAD_ATTR                SMBdialect
              324  GET_ITER         
              326  FOR_ITER            372  'to 372'
              328  STORE_FAST               'dialect'

 L. 113       330  SETUP_LOOP          366  'to 366'
              332  LOAD_FAST                'common_dialects'
              334  GET_ITER         
            336_0  COME_FROM           346  '346'
              336  FOR_ITER            360  'to 360'
              338  STORE_FAST               'cd'

 L. 114       340  LOAD_FAST                'cd'
              342  LOAD_FAST                'dialect'
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_FALSE   336  'to 336'

 L. 115       350  LOAD_FAST                'dialect'
              352  STORE_FAST               'preferred_dialect'

 L. 116       354  BREAK_LOOP       
          356_358  JUMP_BACK           336  'to 336'
              360  POP_BLOCK        

 L. 118   362_364  CONTINUE            326  'to 326'
            366_0  COME_FROM_LOOP      330  '330'

 L. 119       366  BREAK_LOOP       
          368_370  JUMP_BACK           326  'to 326'
              372  POP_BLOCK        
            374_0  COME_FROM_LOOP      316  '316'

 L. 121       374  LOAD_CONST               0
              376  STORE_FAST               'preferred_dialect_idx'

 L. 122       378  SETUP_LOOP          428  'to 428'
              380  LOAD_LISTCOMP            '<code_object <listcomp>>'
              382  LOAD_STR                 'SMB.run.<locals>.<listcomp>'
              384  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              386  LOAD_FAST                'msg'
              388  LOAD_ATTR                command
              390  LOAD_ATTR                Dialects
              392  GET_ITER         
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  GET_ITER         
              398  FOR_ITER            426  'to 426'
              400  STORE_FAST               'dialect'

 L. 123       402  LOAD_FAST                'dialect'
              404  LOAD_FAST                'preferred_dialect'
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   414  'to 414'

 L. 125       412  BREAK_LOOP       
            414_0  COME_FROM           408  '408'

 L. 126       414  LOAD_FAST                'preferred_dialect_idx'
              416  LOAD_CONST               1
              418  INPLACE_ADD      
              420  STORE_FAST               'preferred_dialect_idx'
          422_424  JUMP_BACK           398  'to 398'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP      378  '378'

 L. 128       428  LOAD_FAST                'self'
              430  LOAD_ATTR                logger
              432  LOAD_METHOD              info
              434  LOAD_FAST                'preferred_dialect_idx'
              436  CALL_METHOD_1         1  '1 positional argument'
              438  GET_AWAITABLE    
              440  LOAD_CONST               None
              442  YIELD_FROM       
              444  POP_TOP          

 L. 130       446  LOAD_FAST                'preferred_dialect'
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                session
              452  STORE_ATTR               commondialect

 L. 132       454  LOAD_FAST                'self'
              456  LOAD_ATTR                session
              458  LOAD_ATTR                commondialect
              460  LOAD_STR                 'SMB 2.002'
              462  COMPARE_OP               ==
          464_466  POP_JUMP_IF_FALSE   604  'to 604'

 L. 133       468  LOAD_FAST                'self'
              470  LOAD_ATTR                logger
              472  LOAD_METHOD              debug
              474  LOAD_STR                 'client is capable of smbv2, using SMBv2'
              476  CALL_METHOD_1         1  '1 positional argument'
              478  GET_AWAITABLE    
              480  LOAD_CONST               None
              482  YIELD_FROM       
              484  POP_TOP          

 L. 134       486  LOAD_FAST                'self'
              488  LOAD_ATTR                session
              490  LOAD_ATTR                gssapihandler
              492  LOAD_METHOD              do_auth
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  UNPACK_SEQUENCE_3     3 
              498  STORE_FAST               'status'
              500  STORE_FAST               'data'
              502  STORE_FAST               't'

 L. 135       504  LOAD_GLOBAL              SMB2Message
              506  CALL_FUNCTION_0       0  '0 positional arguments'
              508  STORE_FAST               'resp'

 L. 136       510  LOAD_GLOBAL              SMB2Header_ASYNC
              512  LOAD_METHOD              construct
              514  LOAD_GLOBAL              SMB2Command
              516  LOAD_ATTR                NEGOTIATE
              518  LOAD_GLOBAL              SMB2HeaderFlag
              520  LOAD_ATTR                SMB2_FLAGS_SERVER_TO_REDIR
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                session
              526  LOAD_ATTR                SMBMessageCnt
              528  CALL_METHOD_3         3  '3 positional arguments'
              530  LOAD_FAST                'resp'
              532  STORE_ATTR               header

 L. 137       534  LOAD_GLOBAL              NEGOTIATE_REPLY
              536  LOAD_METHOD              construct
              538  LOAD_FAST                'data'
              540  LOAD_GLOBAL              NegotiateSecurityMode
              542  LOAD_ATTR                SMB2_NEGOTIATE_SIGNING_ENABLED

 L. 138       544  LOAD_GLOBAL              NegotiateDialects
              546  LOAD_ATTR                SMB202
              548  LOAD_FAST                'self'
              550  LOAD_ATTR                session
              552  LOAD_ATTR                serverUUID
              554  LOAD_GLOBAL              NegotiateCapabilities
              556  LOAD_ATTR                SMB2_GLOBAL_CAP_DFS
              558  LOAD_GLOBAL              NegotiateCapabilities
              560  LOAD_ATTR                SMB2_GLOBAL_CAP_LEASING
              562  BINARY_OR        
              564  LOAD_GLOBAL              NegotiateCapabilities
              566  LOAD_ATTR                SMB2_GLOBAL_CAP_LARGE_MTU
              568  BINARY_OR        
              570  CALL_METHOD_5         5  '5 positional arguments'
              572  LOAD_FAST                'resp'
              574  STORE_ATTR               command

 L. 141       576  LOAD_GLOBAL              asyncio
              578  LOAD_ATTR                wait_for
              580  LOAD_FAST                'self'
              582  LOAD_METHOD              send_data
              584  LOAD_FAST                'resp'
              586  CALL_METHOD_1         1  '1 positional argument'
              588  LOAD_CONST               1
              590  LOAD_CONST               ('timeout',)
              592  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              594  GET_AWAITABLE    
              596  LOAD_CONST               None
              598  YIELD_FROM       
              600  STORE_FAST               'a'
              602  JUMP_ABSOLUTE      1620  'to 1620'
            604_0  COME_FROM           464  '464'

 L. 144       604  LOAD_FAST                'self'
              606  LOAD_ATTR                logger
              608  LOAD_METHOD              debug
              610  LOAD_STR                 'using SMBv1'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  GET_AWAITABLE    
              616  LOAD_CONST               None
              618  YIELD_FROM       
              620  POP_TOP          

 L. 145       622  LOAD_FAST                'self'
              624  LOAD_ATTR                session
              626  LOAD_ATTR                gssapihandler
              628  LOAD_ATTR                do_auth
              630  LOAD_CONST               True
              632  LOAD_CONST               ('smbv1',)
              634  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              636  UNPACK_SEQUENCE_3     3 
              638  STORE_FAST               'status'
              640  STORE_FAST               'data'
              642  STORE_FAST               't'

 L. 146       644  LOAD_GLOBAL              SMBMessage
              646  CALL_FUNCTION_0       0  '0 positional arguments'
              648  STORE_FAST               'resp'

 L. 147       650  LOAD_GLOBAL              SMBHeader
              652  LOAD_ATTR                construct
              654  LOAD_GLOBAL              SMBCommand
              656  LOAD_ATTR                SMB_COM_NEGOTIATE

 L. 148       658  LOAD_GLOBAL              NTStatus
              660  LOAD_ATTR                STATUS_SUCCESS

 L. 150       662  LOAD_GLOBAL              SMBHeaderFlagsEnum
              664  LOAD_ATTR                SMB_FLAGS_REPLY

 L. 151       666  LOAD_GLOBAL              SMBHeaderFlagsEnum
              668  LOAD_ATTR                SMB_FLAGS_CASE_INSENSITIVE
              670  BINARY_OR        

 L. 154       672  LOAD_GLOBAL              SMBHeaderFlags2Enum
              674  LOAD_ATTR                SMB_FLAGS2_UNICODE
              676  LOAD_GLOBAL              SMBHeaderFlags2Enum
              678  LOAD_ATTR                SMB_FLAGS2_EXTENDED_SECURITY
              680  BINARY_OR        
              682  LOAD_GLOBAL              SMBHeaderFlags2Enum
              684  LOAD_ATTR                SMB_FLAGS2_NT_STATUS
              686  BINARY_OR        

 L. 155       688  LOAD_GLOBAL              SMBHeaderFlags2Enum
              690  LOAD_ATTR                SMB_FLAGS2_LONG_NAMES
              692  BINARY_OR        

 L. 156       694  LOAD_FAST                'msg'
              696  LOAD_ATTR                header
              698  LOAD_ATTR                MID

 L. 157       700  LOAD_FAST                'msg'
              702  LOAD_ATTR                header
              704  LOAD_ATTR                PIDHigh

 L. 158       706  LOAD_FAST                'msg'
              708  LOAD_ATTR                header
              710  LOAD_ATTR                PIDLow
              712  LOAD_CONST               ('mid', 'pidhigh', 'pidlow')
              714  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              716  LOAD_FAST                'resp'
              718  STORE_ATTR               header

 L. 162       720  LOAD_GLOBAL              SMB_COM_NEGOTIATE_REPLY
              722  LOAD_METHOD              construct
              724  LOAD_FAST                'preferred_dialect_idx'

 L. 163       726  LOAD_GLOBAL              SMBSecurityMode
              728  LOAD_ATTR                NEGOTIATE_ENCRYPT_PASSWORDS
              730  LOAD_GLOBAL              SMBSecurityMode
              732  LOAD_ATTR                NEGOTIATE_USER_SECURITY
              734  BINARY_OR        

 L. 164       736  LOAD_CONST               b'\x00\x00\x00\x00'

 L. 165       738  LOAD_GLOBAL              SMBCapabilities
              740  LOAD_ATTR                CAP_UNICODE
              742  LOAD_GLOBAL              SMBCapabilities
              744  LOAD_ATTR                CAP_NT_SMBS
              746  BINARY_OR        
              748  LOAD_GLOBAL              SMBCapabilities
              750  LOAD_ATTR                CAP_LARGE_FILES
              752  BINARY_OR        
              754  LOAD_GLOBAL              SMBCapabilities
              756  LOAD_ATTR                CAP_NT_EXTENDED_SECURITY
              758  BINARY_OR        

 L. 166       760  LOAD_FAST                'self'
              762  LOAD_ATTR                session
              764  LOAD_ATTR                serverUUID
              766  LOAD_FAST                'data'
              768  CALL_METHOD_6         6  '6 positional arguments'
              770  LOAD_FAST                'resp'
              772  STORE_ATTR               command

 L. 169       774  LOAD_GLOBAL              asyncio
              776  LOAD_ATTR                wait_for
              778  LOAD_FAST                'self'
              780  LOAD_METHOD              send_data
              782  LOAD_FAST                'resp'
              784  CALL_METHOD_1         1  '1 positional argument'
              786  LOAD_CONST               1
              788  LOAD_CONST               ('timeout',)
              790  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              792  GET_AWAITABLE    
              794  LOAD_CONST               None
              796  YIELD_FROM       
              798  STORE_FAST               'a'

 L. 170       800  CONTINUE              4  'to 4'
          802_804  JUMP_ABSOLUTE      1620  'to 1620'
            806_0  COME_FROM           200  '200'

 L. 172       806  LOAD_FAST                'msg'
              808  LOAD_ATTR                header
              810  LOAD_ATTR                Command
              812  LOAD_GLOBAL              SMBCommand
              814  LOAD_ATTR                SMB_COM_SESSION_SETUP_ANDX
              816  COMPARE_OP               ==
          818_820  POP_JUMP_IF_FALSE  1310  'to 1310'

 L. 173       822  LOAD_FAST                'self'
              824  LOAD_ATTR                session
              826  LOAD_ATTR                gssapihandler
              828  LOAD_METHOD              do_auth
              830  LOAD_FAST                'msg'
              832  LOAD_ATTR                command
              834  LOAD_ATTR                SecurityBlob
              836  CALL_METHOD_1         1  '1 positional argument'
              838  UNPACK_SEQUENCE_3     3 
              840  STORE_FAST               'status'
              842  STORE_FAST               'data'
              844  STORE_FAST               'cred'

 L. 175       846  LOAD_FAST                'status'
              848  LOAD_GLOBAL              AuthResult
              850  LOAD_ATTR                FAIL
              852  LOAD_GLOBAL              AuthResult
              854  LOAD_ATTR                OK
              856  BUILD_LIST_2          2 
              858  COMPARE_OP               in
          860_862  POP_JUMP_IF_FALSE   886  'to 886'

 L. 176       864  LOAD_FAST                'self'
              866  LOAD_ATTR                logger
              868  LOAD_METHOD              credential
              870  LOAD_FAST                'cred'
              872  LOAD_METHOD              to_credential
              874  CALL_METHOD_0         0  '0 positional arguments'
              876  CALL_METHOD_1         1  '1 positional argument'
              878  GET_AWAITABLE    
              880  LOAD_CONST               None
              882  YIELD_FROM       
              884  POP_TOP          
            886_0  COME_FROM           860  '860'

 L. 179       886  LOAD_FAST                'status'
              888  LOAD_GLOBAL              AuthResult
              890  LOAD_ATTR                CONTINUE
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_FALSE  1028  'to 1028'

 L. 180       898  LOAD_GLOBAL              SMBHeader
              900  LOAD_ATTR                construct
              902  LOAD_GLOBAL              SMBCommand
              904  LOAD_ATTR                SMB_COM_SESSION_SETUP_ANDX

 L. 181       906  LOAD_GLOBAL              NTStatus
              908  LOAD_ATTR                STATUS_MORE_PROCESSING_REQUIRED

 L. 183       910  LOAD_GLOBAL              SMBHeaderFlagsEnum
              912  LOAD_ATTR                SMB_FLAGS_REPLY

 L. 184       914  LOAD_GLOBAL              SMBHeaderFlagsEnum
              916  LOAD_ATTR                SMB_FLAGS_CASE_INSENSITIVE
              918  BINARY_OR        

 L. 187       920  LOAD_GLOBAL              SMBHeaderFlags2Enum
              922  LOAD_ATTR                SMB_FLAGS2_UNICODE
              924  LOAD_GLOBAL              SMBHeaderFlags2Enum
              926  LOAD_ATTR                SMB_FLAGS2_EXTENDED_SECURITY
              928  BINARY_OR        
              930  LOAD_GLOBAL              SMBHeaderFlags2Enum
              932  LOAD_ATTR                SMB_FLAGS2_NT_STATUS
              934  BINARY_OR        

 L. 188       936  LOAD_GLOBAL              SMBHeaderFlags2Enum
              938  LOAD_ATTR                SMB_FLAGS2_LONG_NAMES
              940  BINARY_OR        

 L. 189       942  LOAD_GLOBAL              random
              944  LOAD_METHOD              randint
              946  LOAD_CONST               1
              948  LOAD_CONST               5000
              950  CALL_METHOD_2         2  '2 positional arguments'

 L. 190       952  LOAD_FAST                'msg'
              954  LOAD_ATTR                header
              956  LOAD_ATTR                MID

 L. 191       958  LOAD_FAST                'msg'
              960  LOAD_ATTR                header
              962  LOAD_ATTR                PIDHigh

 L. 192       964  LOAD_FAST                'msg'
              966  LOAD_ATTR                header
              968  LOAD_ATTR                PIDLow
              970  LOAD_CONST               ('uid', 'mid', 'pidhigh', 'pidlow')
              972  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
              974  LOAD_FAST                'resp'
              976  STORE_ATTR               header

 L. 194       978  LOAD_GLOBAL              SMB_COM_SESSION_SETUP_ANDX_REPLY
              980  LOAD_ATTR                construct
              982  LOAD_FAST                'data'

 L. 195       984  LOAD_STR                 'Windows 2003'

 L. 196       986  LOAD_STR                 'blabla'
              988  LOAD_CONST               ('secblob', 'nativeos', 'nativelanman')
              990  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              992  LOAD_FAST                'resp'
              994  STORE_ATTR               command

 L. 198       996  LOAD_GLOBAL              asyncio
              998  LOAD_ATTR                wait_for
             1000  LOAD_FAST                'self'
             1002  LOAD_METHOD              send_data
             1004  LOAD_FAST                'resp'
             1006  CALL_METHOD_1         1  '1 positional argument'
             1008  LOAD_CONST               1
             1010  LOAD_CONST               ('timeout',)
             1012  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1014  GET_AWAITABLE    
             1016  LOAD_CONST               None
             1018  YIELD_FROM       
             1020  STORE_FAST               'a'

 L. 199      1022  CONTINUE              4  'to 4'
         1024_1026  JUMP_ABSOLUTE      1318  'to 1318'
           1028_0  COME_FROM           894  '894'

 L. 201      1028  LOAD_FAST                'status'
             1030  LOAD_GLOBAL              AuthResult
             1032  LOAD_ATTR                FAIL
             1034  COMPARE_OP               ==
         1036_1038  POP_JUMP_IF_FALSE  1164  'to 1164'

 L. 202      1040  LOAD_GLOBAL              SMBHeader
             1042  LOAD_ATTR                construct
             1044  LOAD_GLOBAL              SMBCommand
             1046  LOAD_ATTR                SMB_COM_SESSION_SETUP_ANDX

 L. 203      1048  LOAD_GLOBAL              NTStatus
             1050  LOAD_ATTR                STATUS_ACCOUNT_DISABLED

 L. 205      1052  LOAD_GLOBAL              SMBHeaderFlagsEnum
             1054  LOAD_ATTR                SMB_FLAGS_REPLY

 L. 206      1056  LOAD_GLOBAL              SMBHeaderFlagsEnum
             1058  LOAD_ATTR                SMB_FLAGS_CASE_INSENSITIVE
             1060  BINARY_OR        

 L. 209      1062  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1064  LOAD_ATTR                SMB_FLAGS2_UNICODE
             1066  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1068  LOAD_ATTR                SMB_FLAGS2_EXTENDED_SECURITY
             1070  BINARY_OR        
             1072  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1074  LOAD_ATTR                SMB_FLAGS2_NT_STATUS
             1076  BINARY_OR        

 L. 210      1078  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1080  LOAD_ATTR                SMB_FLAGS2_LONG_NAMES
             1082  BINARY_OR        

 L. 211      1084  LOAD_FAST                'msg'
             1086  LOAD_ATTR                header
             1088  LOAD_ATTR                UID

 L. 212      1090  LOAD_FAST                'msg'
             1092  LOAD_ATTR                header
             1094  LOAD_ATTR                MID

 L. 213      1096  LOAD_FAST                'msg'
             1098  LOAD_ATTR                header
             1100  LOAD_ATTR                PIDHigh

 L. 214      1102  LOAD_FAST                'msg'
             1104  LOAD_ATTR                header
             1106  LOAD_ATTR                PIDLow
             1108  LOAD_CONST               ('uid', 'mid', 'pidhigh', 'pidlow')
             1110  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1112  LOAD_FAST                'resp'
             1114  STORE_ATTR               header

 L. 216      1116  LOAD_GLOBAL              SMB_COM_SESSION_SETUP_ANDX_REPLY
             1118  LOAD_ATTR                construct
             1120  LOAD_FAST                'data'

 L. 217      1122  LOAD_STR                 'Windows 2003'

 L. 218      1124  LOAD_STR                 'blabla'
             1126  LOAD_CONST               ('secblob', 'nativeos', 'nativelanman')
             1128  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1130  LOAD_FAST                'resp'
             1132  STORE_ATTR               command

 L. 220      1134  LOAD_GLOBAL              asyncio
             1136  LOAD_ATTR                wait_for
             1138  LOAD_FAST                'self'
             1140  LOAD_METHOD              send_data
             1142  LOAD_FAST                'resp'
             1144  CALL_METHOD_1         1  '1 positional argument'
             1146  LOAD_CONST               1
             1148  LOAD_CONST               ('timeout',)
             1150  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1152  GET_AWAITABLE    
             1154  LOAD_CONST               None
             1156  YIELD_FROM       
             1158  STORE_FAST               'a'

 L. 221      1160  LOAD_CONST               None
             1162  RETURN_VALUE     
           1164_0  COME_FROM          1036  '1036'

 L. 223      1164  LOAD_FAST                'status'
             1166  LOAD_GLOBAL              AuthResult
             1168  LOAD_ATTR                OK
             1170  COMPARE_OP               ==
         1172_1174  POP_JUMP_IF_FALSE  1318  'to 1318'

 L. 224      1176  LOAD_GLOBAL              SMB2ServerState
             1178  LOAD_ATTR                AUTHENTICATED
             1180  LOAD_FAST                'self'
             1182  LOAD_ATTR                session
             1184  STORE_ATTR               current_state

 L. 225      1186  LOAD_GLOBAL              SMBHeader
             1188  LOAD_ATTR                construct
             1190  LOAD_GLOBAL              SMBCommand
             1192  LOAD_ATTR                SMB_COM_SESSION_SETUP_ANDX

 L. 226      1194  LOAD_GLOBAL              NTStatus
             1196  LOAD_ATTR                STATUS_SUCCESS

 L. 228      1198  LOAD_GLOBAL              SMBHeaderFlagsEnum
             1200  LOAD_ATTR                SMB_FLAGS_REPLY

 L. 229      1202  LOAD_GLOBAL              SMBHeaderFlagsEnum
             1204  LOAD_ATTR                SMB_FLAGS_CASE_INSENSITIVE
             1206  BINARY_OR        

 L. 232      1208  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1210  LOAD_ATTR                SMB_FLAGS2_UNICODE
             1212  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1214  LOAD_ATTR                SMB_FLAGS2_EXTENDED_SECURITY
             1216  BINARY_OR        
             1218  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1220  LOAD_ATTR                SMB_FLAGS2_NT_STATUS
             1222  BINARY_OR        

 L. 233      1224  LOAD_GLOBAL              SMBHeaderFlags2Enum
             1226  LOAD_ATTR                SMB_FLAGS2_LONG_NAMES
             1228  BINARY_OR        

 L. 234      1230  LOAD_FAST                'msg'
             1232  LOAD_ATTR                header
             1234  LOAD_ATTR                UID

 L. 235      1236  LOAD_FAST                'msg'
             1238  LOAD_ATTR                header
             1240  LOAD_ATTR                MID

 L. 236      1242  LOAD_FAST                'msg'
             1244  LOAD_ATTR                header
             1246  LOAD_ATTR                PIDHigh

 L. 237      1248  LOAD_FAST                'msg'
             1250  LOAD_ATTR                header
             1252  LOAD_ATTR                PIDLow
             1254  LOAD_CONST               ('uid', 'mid', 'pidhigh', 'pidlow')
             1256  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1258  LOAD_FAST                'resp'
             1260  STORE_ATTR               header

 L. 239      1262  LOAD_GLOBAL              SMB_COM_SESSION_SETUP_ANDX_REPLY
             1264  LOAD_ATTR                construct

 L. 240      1266  LOAD_FAST                'data'

 L. 241      1268  LOAD_STR                 'Windows 2003'

 L. 242      1270  LOAD_STR                 'blabla'
             1272  LOAD_CONST               ('secblob', 'nativeos', 'nativelanman')
             1274  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1276  LOAD_FAST                'resp'
             1278  STORE_ATTR               command

 L. 244      1280  LOAD_GLOBAL              asyncio
             1282  LOAD_ATTR                wait_for
             1284  LOAD_FAST                'self'
             1286  LOAD_METHOD              send_data
             1288  LOAD_FAST                'resp'
             1290  CALL_METHOD_1         1  '1 positional argument'
             1292  LOAD_CONST               1
             1294  LOAD_CONST               ('timeout',)
             1296  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1298  GET_AWAITABLE    
             1300  LOAD_CONST               None
             1302  YIELD_FROM       
             1304  STORE_FAST               'a'

 L. 245      1306  CONTINUE              4  'to 4'
             1308  JUMP_FORWARD       1620  'to 1620'
           1310_0  COME_FROM           818  '818'

 L. 249      1310  LOAD_GLOBAL              Exception
             1312  LOAD_STR                 'not implemented!'
             1314  CALL_FUNCTION_1       1  '1 positional argument'
             1316  RAISE_VARARGS_1       1  'exception instance'
           1318_0  COME_FROM          1172  '1172'
         1318_1320  JUMP_FORWARD       1620  'to 1620'
           1322_0  COME_FROM           184  '184'

 L. 253      1322  LOAD_FAST                'msg'
             1324  LOAD_ATTR                header
             1326  LOAD_ATTR                Command
             1328  LOAD_GLOBAL              SMB2Command
             1330  LOAD_ATTR                NEGOTIATE
             1332  COMPARE_OP               ==
         1334_1336  POP_JUMP_IF_FALSE  1456  'to 1456'

 L. 254      1338  LOAD_FAST                'self'
             1340  LOAD_ATTR                session
             1342  LOAD_ATTR                gssapihandler
             1344  LOAD_METHOD              do_auth
             1346  CALL_METHOD_0         0  '0 positional arguments'
             1348  UNPACK_SEQUENCE_3     3 
             1350  STORE_FAST               'status'
             1352  STORE_FAST               'data'
             1354  STORE_FAST               't'

 L. 255      1356  LOAD_GLOBAL              SMB2Message
             1358  CALL_FUNCTION_0       0  '0 positional arguments'
             1360  STORE_FAST               'resp'

 L. 256      1362  LOAD_GLOBAL              SMB2Header_ASYNC
             1364  LOAD_METHOD              construct
             1366  LOAD_GLOBAL              SMB2Command
             1368  LOAD_ATTR                NEGOTIATE
             1370  LOAD_GLOBAL              SMB2HeaderFlag
             1372  LOAD_ATTR                SMB2_FLAGS_SERVER_TO_REDIR
             1374  LOAD_FAST                'self'
             1376  LOAD_ATTR                session
             1378  LOAD_ATTR                SMBMessageCnt
             1380  CALL_METHOD_3         3  '3 positional arguments'
             1382  LOAD_FAST                'resp'
             1384  STORE_ATTR               header

 L. 257      1386  LOAD_GLOBAL              NEGOTIATE_REPLY
             1388  LOAD_METHOD              construct
             1390  LOAD_FAST                'data'
             1392  LOAD_GLOBAL              NegotiateSecurityMode
             1394  LOAD_ATTR                SMB2_NEGOTIATE_SIGNING_ENABLED

 L. 258      1396  LOAD_GLOBAL              NegotiateDialects
             1398  LOAD_ATTR                SMB202
             1400  LOAD_FAST                'self'
             1402  LOAD_ATTR                session
             1404  LOAD_ATTR                serverUUID

 L. 259      1406  LOAD_GLOBAL              NegotiateCapabilities
             1408  LOAD_ATTR                SMB2_GLOBAL_CAP_DFS
             1410  LOAD_GLOBAL              NegotiateCapabilities
             1412  LOAD_ATTR                SMB2_GLOBAL_CAP_LEASING
             1414  BINARY_OR        
             1416  LOAD_GLOBAL              NegotiateCapabilities
             1418  LOAD_ATTR                SMB2_GLOBAL_CAP_LARGE_MTU
             1420  BINARY_OR        
             1422  CALL_METHOD_5         5  '5 positional arguments'
             1424  LOAD_FAST                'resp'
             1426  STORE_ATTR               command

 L. 262      1428  LOAD_GLOBAL              asyncio
             1430  LOAD_ATTR                wait_for
             1432  LOAD_FAST                'self'
             1434  LOAD_METHOD              send_data
             1436  LOAD_FAST                'resp'
             1438  CALL_METHOD_1         1  '1 positional argument'
             1440  LOAD_CONST               1
             1442  LOAD_CONST               ('timeout',)
             1444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1446  GET_AWAITABLE    
             1448  LOAD_CONST               None
             1450  YIELD_FROM       
             1452  STORE_FAST               'a'
             1454  JUMP_FORWARD       1620  'to 1620'
           1456_0  COME_FROM          1334  '1334'

 L. 264      1456  LOAD_FAST                'msg'
             1458  LOAD_ATTR                header
             1460  LOAD_ATTR                Command
             1462  LOAD_GLOBAL              SMB2Command
             1464  LOAD_ATTR                SESSION_SETUP
             1466  COMPARE_OP               ==
         1468_1470  POP_JUMP_IF_FALSE  1612  'to 1612'

 L. 265      1472  LOAD_FAST                'self'
             1474  LOAD_ATTR                session
             1476  LOAD_ATTR                gssapihandler
             1478  LOAD_METHOD              do_auth
             1480  LOAD_FAST                'msg'
             1482  LOAD_ATTR                command
             1484  LOAD_ATTR                Buffer
             1486  CALL_METHOD_1         1  '1 positional argument'
             1488  UNPACK_SEQUENCE_3     3 
             1490  STORE_FAST               'status'
             1492  STORE_FAST               'data'
             1494  STORE_FAST               'cred'

 L. 266      1496  LOAD_FAST                'cred'
             1498  LOAD_CONST               None
             1500  COMPARE_OP               is-not
         1502_1504  POP_JUMP_IF_FALSE  1528  'to 1528'

 L. 267      1506  LOAD_FAST                'self'
             1508  LOAD_ATTR                logger
             1510  LOAD_METHOD              credential
             1512  LOAD_FAST                'cred'
             1514  LOAD_METHOD              to_credential
             1516  CALL_METHOD_0         0  '0 positional arguments'
             1518  CALL_METHOD_1         1  '1 positional argument'
             1520  GET_AWAITABLE    
             1522  LOAD_CONST               None
             1524  YIELD_FROM       
             1526  POP_TOP          
           1528_0  COME_FROM          1502  '1502'

 L. 269      1528  LOAD_GLOBAL              SMB2Message
             1530  CALL_FUNCTION_0       0  '0 positional arguments'
             1532  STORE_FAST               'resp'

 L. 270      1534  LOAD_GLOBAL              SMB2Header_ASYNC
             1536  LOAD_ATTR                construct
             1538  LOAD_GLOBAL              SMB2Command
             1540  LOAD_ATTR                SESSION_SETUP
             1542  LOAD_GLOBAL              SMB2HeaderFlag
             1544  LOAD_ATTR                SMB2_FLAGS_SERVER_TO_REDIR
             1546  LOAD_CONST               1
             1548  LOAD_GLOBAL              NTStatus
             1550  LOAD_ATTR                STATUS_MORE_PROCESSING_REQUIRED

 L. 271      1552  LOAD_CONST               1
             1554  LOAD_CONST               1
             1556  LOAD_FAST                'self'
             1558  LOAD_ATTR                session
             1560  LOAD_ATTR                SMBSessionID
             1562  LOAD_CONST               ('status', 'Credit', 'CreditCharge', 'SessionId')
             1564  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1566  LOAD_FAST                'resp'
             1568  STORE_ATTR               header

 L. 272      1570  LOAD_GLOBAL              SESSION_SETUP_REPLY
             1572  LOAD_METHOD              construct
             1574  LOAD_FAST                'data'
             1576  LOAD_CONST               0
             1578  CALL_METHOD_2         2  '2 positional arguments'
             1580  LOAD_FAST                'resp'
             1582  STORE_ATTR               command

 L. 274      1584  LOAD_GLOBAL              asyncio
             1586  LOAD_ATTR                wait_for
             1588  LOAD_FAST                'self'
             1590  LOAD_METHOD              send_data
             1592  LOAD_FAST                'resp'
             1594  CALL_METHOD_1         1  '1 positional argument'
             1596  LOAD_CONST               1
             1598  LOAD_CONST               ('timeout',)
             1600  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1602  GET_AWAITABLE    
             1604  LOAD_CONST               None
             1606  YIELD_FROM       
           1608_0  COME_FROM          1308  '1308'
             1608  STORE_FAST               'a'
             1610  JUMP_FORWARD       1620  'to 1620'
           1612_0  COME_FROM          1468  '1468'

 L. 276      1612  LOAD_GLOBAL              Exception
             1614  LOAD_STR                 'Dunno!'
             1616  CALL_FUNCTION_1       1  '1 positional argument'
             1618  RAISE_VARARGS_1       1  'exception instance'
           1620_0  COME_FROM          1610  '1610'
           1620_1  COME_FROM          1454  '1454'
           1620_2  COME_FROM          1318  '1318'
           1620_3  COME_FROM           172  '172'

 L. 278      1620  LOAD_FAST                'self'
             1622  LOAD_ATTR                session
             1624  LOAD_ATTR                current_state
             1626  LOAD_GLOBAL              SMB2ServerState
             1628  LOAD_ATTR                AUTHENTICATED
             1630  COMPARE_OP               ==
             1632  POP_JUMP_IF_FALSE     4  'to 4'

 L. 279      1634  LOAD_GLOBAL              Exception
             1636  LOAD_STR                 'Dunno what to do now that authentication was sucsessfull'
             1638  CALL_FUNCTION_1       1  '1 positional argument'
             1640  RAISE_VARARGS_1       1  'exception instance'
             1642  JUMP_BACK             4  'to 4'
           1644_0  COME_FROM            12  '12'
             1644  POP_BLOCK        
           1646_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 1608_0