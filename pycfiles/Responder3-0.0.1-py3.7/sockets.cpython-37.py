# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\core\sockets.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 7356 bytes
import ipaddress, socket, sys
from responder3.core.commons import ResponderPlatform, get_platform

class SocketConfig:

    def __init__(self):
        """
                Holds all necessary information to create a listening socket
                """
        self.bind_iface = None
        self.bind_port = None
        self.bind_family = None
        self.bind_protocol = None
        self.bind_addr = None
        self.bind_iface_idx = None
        self.reuse_address = True
        self.reuse_port = True
        self.is_ssl_wrapped = False
        self.is_server = True
        self.platform = get_platform()

    def to_dict(self):
        t = {}
        t['bind_iface'] = self.bind_iface
        t['bind_port'] = self.bind_port
        t['bind_family'] = self.bind_family
        t['bind_protocol'] = self.bind_protocol
        t['bind_iface_idx'] = self.bind_iface_idx
        t['reuse_address'] = self.reuse_address
        t['reuse_port'] = self.reuse_port
        t['is_ssl_wrapped'] = self.is_ssl_wrapped
        t['is_server'] = self.is_server
        return t

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_protocolname(self):
        """
                Returns protocol type as string
                :return: str
                """
        if self.bind_protocol == socket.SOCK_STREAM:
            return 'TCP'
        if self.bind_protocol == socket.SOCK_DGRAM:
            return 'UDP'
        return 'UNKNOWN'

    def get_address(self):
        """
                Resturns address as tuple
                :return: tuple
                """
        return (
         str(self.bind_addr), self.bind_port)

    def get_print_address(self):
        """
                Returns address in a printable form
                :return: str
                """
        return '%s:%d' % (str(self.bind_addr), self.bind_port)

    def get_server_kwargs(self):
        """
                Returns a dict to be used in asyncio.create_server function
                :return: dict
                """
        return {'host':str(self.bind_addr), 
         'port':self.bind_port, 
         'family':self.bind_family, 
         'reuse_address':self.reuse_address, 
         'reuse_port':self.reuse_port}

    def __repr__(self):
        return str(self)

    def __str__(self):
        t = '==SocketConfig==\r\n'
        t += 'Interface: %s\r\n' % self.bind_iface
        t += 'Iface idx: %s\r\n' % self.bind_iface_idx
        t += 'Address  : %s\r\n' % str(self.bind_addr)
        t += 'Port     : %s\r\n' % self.bind_port
        t += 'Protocol : %s\r\n' % self.bind_protocol
        t += 'Family   : %s\r\n' % self.bind_family
        return t


def setup_base_socket--- This code section failed: ---

 L. 104       0_2  SETUP_EXCEPT       1046  'to 1046'

 L. 105         4  LOAD_CONST               None
                6  STORE_FAST               'sock'

 L. 106         8  LOAD_FAST                'socket_config'
               10  LOAD_ATTR                bind_protocol
               12  LOAD_GLOBAL              socket
               14  LOAD_ATTR                SOCK_DGRAM
               16  COMPARE_OP               ==
            18_20  POP_JUMP_IF_FALSE   504  'to 504'

 L. 107        22  LOAD_FAST                'socket_config'
               24  LOAD_ATTR                bind_family
               26  LOAD_CONST               4
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE   190  'to 190'

 L. 108        32  LOAD_GLOBAL              socket
               34  LOAD_METHOD              socket
               36  LOAD_GLOBAL              socket
               38  LOAD_ATTR                AF_INET
               40  LOAD_GLOBAL              socket
               42  LOAD_ATTR                SOCK_DGRAM
               44  LOAD_GLOBAL              socket
               46  LOAD_ATTR                IPPROTO_UDP
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  STORE_FAST               'sock'

 L. 109        52  LOAD_FAST                'socket_config'
               54  LOAD_ATTR                platform
               56  LOAD_GLOBAL              ResponderPlatform
               58  LOAD_ATTR                LINUX
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE   116  'to 116'

 L. 110        64  LOAD_FAST                'socket_config'
               66  LOAD_ATTR                reuse_address
               68  POP_JUMP_IF_FALSE    92  'to 92'

 L. 111        70  LOAD_FAST                'sock'
               72  LOAD_METHOD              setsockopt
               74  LOAD_GLOBAL              socket
               76  LOAD_ATTR                SOL_SOCKET
               78  LOAD_CONST               25
               80  LOAD_FAST                'socket_config'
               82  LOAD_ATTR                bind_iface
               84  LOAD_METHOD              encode
               86  CALL_METHOD_0         0  '0 positional arguments'
               88  CALL_METHOD_3         3  '3 positional arguments'
               90  POP_TOP          
             92_0  COME_FROM            68  '68'

 L. 112        92  LOAD_FAST                'socket_config'
               94  LOAD_ATTR                reuse_port
               96  POP_JUMP_IF_FALSE   116  'to 116'

 L. 113        98  LOAD_FAST                'sock'
              100  LOAD_METHOD              setsockopt
              102  LOAD_GLOBAL              socket
              104  LOAD_ATTR                SOL_SOCKET
              106  LOAD_GLOBAL              socket
              108  LOAD_ATTR                SO_REUSEPORT
              110  LOAD_CONST               1
              112  CALL_METHOD_3         3  '3 positional arguments'
              114  POP_TOP          
            116_0  COME_FROM            96  '96'
            116_1  COME_FROM            62  '62'

 L. 114       116  LOAD_FAST                'sock'
              118  LOAD_METHOD              setblocking
              120  LOAD_CONST               False
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_TOP          

 L. 115       126  LOAD_FAST                'sock'
              128  LOAD_METHOD              setsockopt
              130  LOAD_GLOBAL              socket
              132  LOAD_ATTR                SOL_SOCKET
              134  LOAD_GLOBAL              socket
              136  LOAD_ATTR                SO_REUSEADDR
              138  LOAD_CONST               1
              140  CALL_METHOD_3         3  '3 positional arguments'
              142  POP_TOP          

 L. 116       144  LOAD_FAST                'sock'
              146  LOAD_METHOD              bind

 L. 118       148  LOAD_FAST                'bind_ip_override'
              150  LOAD_CONST               None
              152  COMPARE_OP               is-not
              154  POP_JUMP_IF_FALSE   164  'to 164'
              156  LOAD_GLOBAL              str
              158  LOAD_FAST                'bind_ip_override'
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  JUMP_FORWARD        172  'to 172'
            164_0  COME_FROM           154  '154'
              164  LOAD_GLOBAL              str
              166  LOAD_FAST                'socket_config'
              168  LOAD_ATTR                bind_addr
              170  CALL_FUNCTION_1       1  '1 positional argument'
            172_0  COME_FROM           162  '162'

 L. 119       172  LOAD_GLOBAL              int
              174  LOAD_FAST                'socket_config'
              176  LOAD_ATTR                bind_port
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  BUILD_TUPLE_2         2 
              182  CALL_METHOD_1         1  '1 positional argument'
              184  POP_TOP          
          186_188  JUMP_ABSOLUTE      1020  'to 1020'
            190_0  COME_FROM            30  '30'

 L. 123       190  LOAD_FAST                'socket_config'
              192  LOAD_ATTR                bind_family
              194  LOAD_CONST               6
              196  COMPARE_OP               ==
          198_200  POP_JUMP_IF_FALSE   492  'to 492'

 L. 124       202  LOAD_GLOBAL              socket
              204  LOAD_ATTR                has_ipv6
              206  POP_JUMP_IF_TRUE    216  'to 216'

 L. 125       208  LOAD_GLOBAL              Exception
              210  LOAD_STR                 'IPv6 is NOT supported on this platform'
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           206  '206'

 L. 126       216  LOAD_GLOBAL              str
              218  LOAD_FAST                'bind_ip_override'
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  LOAD_STR                 '0.0.0.0'
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   238  'to 238'

 L. 127       228  LOAD_GLOBAL              ipaddress
              230  LOAD_METHOD              ip_address
              232  LOAD_STR                 '::'
              234  CALL_METHOD_1         1  '1 positional argument'
              236  STORE_FAST               'bind_ip_override'
            238_0  COME_FROM           226  '226'

 L. 128       238  LOAD_GLOBAL              socket
              240  LOAD_METHOD              socket
              242  LOAD_GLOBAL              socket
              244  LOAD_ATTR                AF_INET6
              246  LOAD_GLOBAL              socket
              248  LOAD_ATTR                SOCK_DGRAM
              250  LOAD_GLOBAL              socket
              252  LOAD_ATTR                IPPROTO_UDP
              254  CALL_METHOD_3         3  '3 positional arguments'
              256  STORE_FAST               'sock'

 L. 129       258  LOAD_FAST                'sock'
              260  LOAD_METHOD              setblocking
              262  LOAD_CONST               False
              264  CALL_METHOD_1         1  '1 positional argument'
              266  POP_TOP          

 L. 130       268  LOAD_FAST                'sock'
              270  LOAD_METHOD              setsockopt
              272  LOAD_GLOBAL              socket
              274  LOAD_ATTR                SOL_SOCKET
              276  LOAD_GLOBAL              socket
              278  LOAD_ATTR                SO_REUSEADDR
              280  LOAD_CONST               1
              282  CALL_METHOD_3         3  '3 positional arguments'
              284  POP_TOP          

 L. 132       286  LOAD_FAST                'socket_config'
              288  LOAD_ATTR                platform
              290  LOAD_GLOBAL              ResponderPlatform
              292  LOAD_ATTR                LINUX
              294  LOAD_GLOBAL              ResponderPlatform
              296  LOAD_ATTR                MAC
              298  BUILD_LIST_2          2 
              300  COMPARE_OP               in
          302_304  POP_JUMP_IF_FALSE   362  'to 362'

 L. 133       306  LOAD_FAST                'socket_config'
              308  LOAD_ATTR                reuse_address
          310_312  POP_JUMP_IF_FALSE   336  'to 336'

 L. 134       314  LOAD_FAST                'sock'
              316  LOAD_METHOD              setsockopt
              318  LOAD_GLOBAL              socket
              320  LOAD_ATTR                SOL_SOCKET
              322  LOAD_CONST               25
              324  LOAD_FAST                'socket_config'
              326  LOAD_ATTR                bind_iface
              328  LOAD_METHOD              encode
              330  CALL_METHOD_0         0  '0 positional arguments'
              332  CALL_METHOD_3         3  '3 positional arguments'
              334  POP_TOP          
            336_0  COME_FROM           310  '310'

 L. 135       336  LOAD_FAST                'socket_config'
              338  LOAD_ATTR                reuse_port
          340_342  POP_JUMP_IF_FALSE   362  'to 362'

 L. 136       344  LOAD_FAST                'sock'
              346  LOAD_METHOD              setsockopt
              348  LOAD_GLOBAL              socket
              350  LOAD_ATTR                SOL_SOCKET
              352  LOAD_GLOBAL              socket
              354  LOAD_ATTR                SO_REUSEPORT
              356  LOAD_CONST               1
              358  CALL_METHOD_3         3  '3 positional arguments'
              360  POP_TOP          
            362_0  COME_FROM           340  '340'
            362_1  COME_FROM           302  '302'

 L. 138       362  LOAD_FAST                'socket_config'
              364  LOAD_ATTR                platform
              366  LOAD_GLOBAL              ResponderPlatform
              368  LOAD_ATTR                LINUX
              370  LOAD_GLOBAL              ResponderPlatform
              372  LOAD_ATTR                MAC
              374  BUILD_LIST_2          2 
              376  COMPARE_OP               in
          378_380  POP_JUMP_IF_FALSE   432  'to 432'

 L. 139       382  LOAD_FAST                'sock'
              384  LOAD_METHOD              bind

 L. 141       386  LOAD_FAST                'bind_ip_override'
              388  LOAD_CONST               None
              390  COMPARE_OP               is-not
          392_394  POP_JUMP_IF_FALSE   404  'to 404'
              396  LOAD_GLOBAL              str
              398  LOAD_FAST                'bind_ip_override'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  JUMP_FORWARD        412  'to 412'
            404_0  COME_FROM           392  '392'
              404  LOAD_GLOBAL              str
              406  LOAD_FAST                'socket_config'
              408  LOAD_ATTR                bind_addr
              410  CALL_FUNCTION_1       1  '1 positional argument'
            412_0  COME_FROM           402  '402'

 L. 142       412  LOAD_GLOBAL              int
              414  LOAD_FAST                'socket_config'
              416  LOAD_ATTR                bind_port
              418  CALL_FUNCTION_1       1  '1 positional argument'

 L. 143       420  LOAD_FAST                'socket_config'
              422  LOAD_ATTR                bind_iface_idx
              424  BUILD_TUPLE_3         3 
              426  CALL_METHOD_1         1  '1 positional argument'
              428  POP_TOP          
              430  JUMP_FORWARD        490  'to 490'
            432_0  COME_FROM           378  '378'

 L. 146       432  LOAD_FAST                'socket_config'
              434  LOAD_ATTR                platform
              436  LOAD_GLOBAL              ResponderPlatform
              438  LOAD_ATTR                WINDOWS
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   500  'to 500'

 L. 147       446  LOAD_FAST                'sock'
              448  LOAD_METHOD              bind

 L. 149       450  LOAD_FAST                'bind_ip_override'
              452  LOAD_CONST               None
              454  COMPARE_OP               is-not
          456_458  POP_JUMP_IF_FALSE   468  'to 468'
              460  LOAD_GLOBAL              str
              462  LOAD_FAST                'socket_config'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  JUMP_FORWARD        476  'to 476'
            468_0  COME_FROM           456  '456'
              468  LOAD_GLOBAL              str
              470  LOAD_FAST                'socket_config'
              472  LOAD_ATTR                bind_addr
              474  CALL_FUNCTION_1       1  '1 positional argument'
            476_0  COME_FROM           466  '466'

 L. 150       476  LOAD_GLOBAL              int
              478  LOAD_FAST                'socket_config'
              480  LOAD_ATTR                bind_port
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  BUILD_TUPLE_2         2 
              486  CALL_METHOD_1         1  '1 positional argument'
              488  POP_TOP          
            490_0  COME_FROM           430  '430'
              490  JUMP_FORWARD       1020  'to 1020'
            492_0  COME_FROM           198  '198'

 L. 155       492  LOAD_GLOBAL              Exception
              494  LOAD_STR                 'Unknown IP version'
              496  CALL_FUNCTION_1       1  '1 positional argument'
              498  RAISE_VARARGS_1       1  'exception instance'
            500_0  COME_FROM           442  '442'
          500_502  JUMP_FORWARD       1020  'to 1020'
            504_0  COME_FROM            18  '18'

 L. 157       504  LOAD_FAST                'socket_config'
              506  LOAD_ATTR                bind_protocol
              508  LOAD_GLOBAL              socket
              510  LOAD_ATTR                SOCK_STREAM
              512  COMPARE_OP               ==
          514_516  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 158       518  LOAD_FAST                'socket_config'
              520  LOAD_ATTR                bind_family
              522  LOAD_CONST               4
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   696  'to 696'

 L. 159       530  LOAD_GLOBAL              socket
              532  LOAD_METHOD              socket
              534  LOAD_GLOBAL              socket
              536  LOAD_ATTR                AF_INET
              538  LOAD_GLOBAL              socket
              540  LOAD_ATTR                SOCK_STREAM
              542  LOAD_GLOBAL              socket
              544  LOAD_ATTR                IPPROTO_TCP
              546  CALL_METHOD_3         3  '3 positional arguments'
              548  STORE_FAST               'sock'

 L. 160       550  LOAD_FAST                'sock'
              552  LOAD_METHOD              setblocking
              554  LOAD_CONST               False
              556  CALL_METHOD_1         1  '1 positional argument'
              558  POP_TOP          

 L. 161       560  LOAD_FAST                'socket_config'
              562  LOAD_ATTR                platform
              564  LOAD_GLOBAL              ResponderPlatform
              566  LOAD_ATTR                LINUX
              568  COMPARE_OP               ==
          570_572  POP_JUMP_IF_FALSE   630  'to 630'

 L. 162       574  LOAD_FAST                'socket_config'
              576  LOAD_ATTR                reuse_address
          578_580  POP_JUMP_IF_FALSE   604  'to 604'

 L. 163       582  LOAD_FAST                'sock'
              584  LOAD_METHOD              setsockopt
              586  LOAD_GLOBAL              socket
              588  LOAD_ATTR                SOL_SOCKET
              590  LOAD_CONST               25
              592  LOAD_FAST                'socket_config'
              594  LOAD_ATTR                bind_iface
              596  LOAD_METHOD              encode
              598  CALL_METHOD_0         0  '0 positional arguments'
              600  CALL_METHOD_3         3  '3 positional arguments'
              602  POP_TOP          
            604_0  COME_FROM           578  '578'

 L. 164       604  LOAD_FAST                'socket_config'
              606  LOAD_ATTR                reuse_port
          608_610  POP_JUMP_IF_FALSE   630  'to 630'

 L. 165       612  LOAD_FAST                'sock'
              614  LOAD_METHOD              setsockopt
              616  LOAD_GLOBAL              socket
              618  LOAD_ATTR                SOL_SOCKET
              620  LOAD_GLOBAL              socket
              622  LOAD_ATTR                SO_REUSEPORT
              624  LOAD_CONST               1
              626  CALL_METHOD_3         3  '3 positional arguments'
              628  POP_TOP          
            630_0  COME_FROM           608  '608'
            630_1  COME_FROM           570  '570'

 L. 166       630  LOAD_FAST                'sock'
              632  LOAD_METHOD              setsockopt
              634  LOAD_GLOBAL              socket
              636  LOAD_ATTR                SOL_SOCKET
              638  LOAD_GLOBAL              socket
              640  LOAD_ATTR                SO_REUSEADDR
              642  LOAD_CONST               1
              644  CALL_METHOD_3         3  '3 positional arguments'
              646  POP_TOP          

 L. 167       648  LOAD_FAST                'sock'
              650  LOAD_METHOD              bind

 L. 169       652  LOAD_FAST                'bind_ip_override'
              654  LOAD_CONST               None
              656  COMPARE_OP               is-not
          658_660  POP_JUMP_IF_FALSE   670  'to 670'
              662  LOAD_GLOBAL              str
              664  LOAD_FAST                'bind_ip_override'
              666  CALL_FUNCTION_1       1  '1 positional argument'
              668  JUMP_FORWARD        678  'to 678'
            670_0  COME_FROM           658  '658'
              670  LOAD_GLOBAL              str
              672  LOAD_FAST                'socket_config'
              674  LOAD_ATTR                bind_addr
              676  CALL_FUNCTION_1       1  '1 positional argument'
            678_0  COME_FROM           668  '668'

 L. 170       678  LOAD_GLOBAL              int
              680  LOAD_FAST                'socket_config'
              682  LOAD_ATTR                bind_port
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  BUILD_TUPLE_2         2 
              688  CALL_METHOD_1         1  '1 positional argument'
              690  POP_TOP          
          692_694  JUMP_ABSOLUTE      1020  'to 1020'
            696_0  COME_FROM           526  '526'

 L. 174       696  LOAD_FAST                'socket_config'
              698  LOAD_ATTR                bind_family
              700  LOAD_CONST               6
              702  COMPARE_OP               ==
          704_706  POP_JUMP_IF_FALSE  1002  'to 1002'

 L. 175       708  LOAD_GLOBAL              socket
              710  LOAD_ATTR                has_ipv6
          712_714  POP_JUMP_IF_TRUE    724  'to 724'

 L. 176       716  LOAD_GLOBAL              Exception
              718  LOAD_STR                 'IPv6 is NOT supported on this platform'
              720  CALL_FUNCTION_1       1  '1 positional argument'
              722  RAISE_VARARGS_1       1  'exception instance'
            724_0  COME_FROM           712  '712'

 L. 177       724  LOAD_GLOBAL              str
              726  LOAD_FAST                'bind_ip_override'
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  LOAD_STR                 '0.0.0.0'
              732  COMPARE_OP               ==
          734_736  POP_JUMP_IF_FALSE   748  'to 748'

 L. 178       738  LOAD_GLOBAL              ipaddress
              740  LOAD_METHOD              ip_address
              742  LOAD_STR                 '::'
              744  CALL_METHOD_1         1  '1 positional argument'
              746  STORE_FAST               'bind_ip_override'
            748_0  COME_FROM           734  '734'

 L. 179       748  LOAD_GLOBAL              socket
              750  LOAD_METHOD              socket
              752  LOAD_GLOBAL              socket
              754  LOAD_ATTR                AF_INET6
              756  LOAD_GLOBAL              socket
              758  LOAD_ATTR                SOCK_STREAM
              760  LOAD_GLOBAL              socket
              762  LOAD_ATTR                IPPROTO_TCP
              764  CALL_METHOD_3         3  '3 positional arguments'
              766  STORE_FAST               'sock'

 L. 180       768  LOAD_FAST                'sock'
              770  LOAD_METHOD              setblocking
              772  LOAD_CONST               False
              774  CALL_METHOD_1         1  '1 positional argument'
              776  POP_TOP          

 L. 181       778  LOAD_FAST                'socket_config'
              780  LOAD_ATTR                platform
              782  LOAD_GLOBAL              ResponderPlatform
              784  LOAD_ATTR                LINUX
              786  LOAD_GLOBAL              ResponderPlatform
              788  LOAD_ATTR                MAC
              790  BUILD_LIST_2          2 
              792  COMPARE_OP               in
          794_796  POP_JUMP_IF_FALSE   854  'to 854'

 L. 182       798  LOAD_FAST                'socket_config'
              800  LOAD_ATTR                reuse_address
          802_804  POP_JUMP_IF_FALSE   828  'to 828'

 L. 183       806  LOAD_FAST                'sock'
              808  LOAD_METHOD              setsockopt
              810  LOAD_GLOBAL              socket
              812  LOAD_ATTR                SOL_SOCKET
              814  LOAD_CONST               25
              816  LOAD_FAST                'socket_config'
              818  LOAD_ATTR                bind_iface
              820  LOAD_METHOD              encode
              822  CALL_METHOD_0         0  '0 positional arguments'
              824  CALL_METHOD_3         3  '3 positional arguments'
              826  POP_TOP          
            828_0  COME_FROM           802  '802'

 L. 184       828  LOAD_FAST                'socket_config'
              830  LOAD_ATTR                reuse_port
          832_834  POP_JUMP_IF_FALSE   854  'to 854'

 L. 185       836  LOAD_FAST                'sock'
              838  LOAD_METHOD              setsockopt
              840  LOAD_GLOBAL              socket
              842  LOAD_ATTR                SOL_SOCKET
              844  LOAD_GLOBAL              socket
              846  LOAD_ATTR                SO_REUSEPORT
              848  LOAD_CONST               1
              850  CALL_METHOD_3         3  '3 positional arguments'
              852  POP_TOP          
            854_0  COME_FROM           832  '832'
            854_1  COME_FROM           794  '794'

 L. 186       854  LOAD_FAST                'sock'
              856  LOAD_METHOD              setsockopt
              858  LOAD_GLOBAL              socket
              860  LOAD_ATTR                SOL_SOCKET
              862  LOAD_GLOBAL              socket
              864  LOAD_ATTR                SO_REUSEADDR
              866  LOAD_CONST               1
              868  CALL_METHOD_3         3  '3 positional arguments'
              870  POP_TOP          

 L. 187       872  LOAD_FAST                'socket_config'
              874  LOAD_ATTR                platform
              876  LOAD_GLOBAL              ResponderPlatform
              878  LOAD_ATTR                LINUX
              880  LOAD_GLOBAL              ResponderPlatform
              882  LOAD_ATTR                MAC
              884  BUILD_LIST_2          2 
              886  COMPARE_OP               in
          888_890  POP_JUMP_IF_FALSE   942  'to 942'

 L. 188       892  LOAD_FAST                'sock'
              894  LOAD_METHOD              bind

 L. 190       896  LOAD_FAST                'bind_ip_override'
              898  LOAD_CONST               None
              900  COMPARE_OP               is-not
          902_904  POP_JUMP_IF_FALSE   914  'to 914'
              906  LOAD_GLOBAL              str
              908  LOAD_FAST                'bind_ip_override'
              910  CALL_FUNCTION_1       1  '1 positional argument'
              912  JUMP_FORWARD        922  'to 922'
            914_0  COME_FROM           902  '902'
              914  LOAD_GLOBAL              str
              916  LOAD_FAST                'socket_config'
              918  LOAD_ATTR                bind_addr
              920  CALL_FUNCTION_1       1  '1 positional argument'
            922_0  COME_FROM           912  '912'

 L. 191       922  LOAD_GLOBAL              int
              924  LOAD_FAST                'socket_config'
              926  LOAD_ATTR                bind_port
              928  CALL_FUNCTION_1       1  '1 positional argument'

 L. 192       930  LOAD_FAST                'socket_config'
              932  LOAD_ATTR                bind_iface_idx
              934  BUILD_TUPLE_3         3 
              936  CALL_METHOD_1         1  '1 positional argument'
              938  POP_TOP          
              940  JUMP_FORWARD       1000  'to 1000'
            942_0  COME_FROM           888  '888'

 L. 195       942  LOAD_FAST                'socket_config'
              944  LOAD_ATTR                platform
              946  LOAD_GLOBAL              ResponderPlatform
              948  LOAD_ATTR                WINDOWS
              950  COMPARE_OP               ==
          952_954  POP_JUMP_IF_FALSE  1010  'to 1010'

 L. 196       956  LOAD_FAST                'sock'
              958  LOAD_METHOD              bind

 L. 198       960  LOAD_FAST                'bind_ip_override'
              962  LOAD_CONST               None
              964  COMPARE_OP               is-not
          966_968  POP_JUMP_IF_FALSE   978  'to 978'
              970  LOAD_GLOBAL              str
              972  LOAD_FAST                'bind_ip_override'
              974  CALL_FUNCTION_1       1  '1 positional argument'
              976  JUMP_FORWARD        986  'to 986'
            978_0  COME_FROM           966  '966'
              978  LOAD_GLOBAL              str
              980  LOAD_FAST                'socket_config'
              982  LOAD_ATTR                bind_addr
              984  CALL_FUNCTION_1       1  '1 positional argument'
            986_0  COME_FROM           976  '976'

 L. 199       986  LOAD_GLOBAL              int
              988  LOAD_FAST                'socket_config'
              990  LOAD_ATTR                bind_port
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  BUILD_TUPLE_2         2 
              996  CALL_METHOD_1         1  '1 positional argument'
              998  POP_TOP          
           1000_0  COME_FROM           940  '940'
             1000  JUMP_FORWARD       1010  'to 1010'
           1002_0  COME_FROM           704  '704'

 L. 204      1002  LOAD_GLOBAL              Exception
             1004  LOAD_STR                 'Unknown IP version'
             1006  CALL_FUNCTION_1       1  '1 positional argument'
           1008_0  COME_FROM           490  '490'
             1008  RAISE_VARARGS_1       1  'exception instance'
           1010_0  COME_FROM          1000  '1000'
           1010_1  COME_FROM           952  '952'
             1010  JUMP_FORWARD       1020  'to 1020'
           1012_0  COME_FROM           514  '514'

 L. 206      1012  LOAD_GLOBAL              Exception
             1014  LOAD_STR                 'Unknown protocol!'
             1016  CALL_FUNCTION_1       1  '1 positional argument'
             1018  RAISE_VARARGS_1       1  'exception instance'
           1020_0  COME_FROM          1010  '1010'
           1020_1  COME_FROM           500  '500'

 L. 208      1020  LOAD_FAST                'socket_config'
             1022  LOAD_ATTR                is_server
         1024_1026  POP_JUMP_IF_TRUE   1042  'to 1042'

 L. 209      1028  LOAD_GLOBAL              socket
             1030  LOAD_METHOD              gethostname
             1032  CALL_METHOD_0         0  '0 positional arguments'
             1034  LOAD_CONST               1
             1036  BINARY_SUBSCR    
             1038  LOAD_FAST                'socket_config'
             1040  STORE_ATTR               bind_port
           1042_0  COME_FROM          1024  '1024'

 L. 211      1042  LOAD_FAST                'sock'
             1044  RETURN_VALUE     
           1046_0  COME_FROM_EXCEPT      0  '0'

 L. 212      1046  DUP_TOP          
             1048  LOAD_GLOBAL              Exception
             1050  COMPARE_OP               exception-match
         1052_1054  POP_JUMP_IF_FALSE  1150  'to 1150'
             1056  POP_TOP          
             1058  STORE_FAST               'e'
             1060  POP_TOP          
             1062  SETUP_FINALLY      1138  'to 1138'

 L. 214      1064  LOAD_GLOBAL              type
             1066  LOAD_FAST                'e'
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  LOAD_GLOBAL              str
             1072  LOAD_FAST                'e'
             1074  CALL_FUNCTION_1       1  '1 positional argument'

 L. 215      1076  LOAD_STR                 'Failed to set up socket for on IP %s PORT %s FAMILY %s IP_OVERRIDE %s'

 L. 216      1078  LOAD_GLOBAL              str
             1080  LOAD_FAST                'socket_config'
             1082  LOAD_ATTR                bind_addr
             1084  CALL_FUNCTION_1       1  '1 positional argument'

 L. 217      1086  LOAD_FAST                'socket_config'
             1088  LOAD_ATTR                bind_port

 L. 218      1090  LOAD_FAST                'socket_config'
             1092  LOAD_ATTR                bind_family

 L. 219      1094  LOAD_GLOBAL              str
             1096  LOAD_FAST                'bind_ip_override'
             1098  CALL_FUNCTION_1       1  '1 positional argument'
             1100  BUILD_TUPLE_4         4 
             1102  BINARY_MODULO    
             1104  BINARY_ADD       

 L. 220      1106  LOAD_GLOBAL              sys
             1108  LOAD_METHOD              exc_info
             1110  CALL_METHOD_0         0  '0 positional arguments'
             1112  LOAD_CONST               2
             1114  BINARY_SUBSCR    
             1116  CALL_FUNCTION_2       2  '2 positional arguments'
             1118  LOAD_METHOD              with_traceback
             1120  LOAD_GLOBAL              sys
             1122  LOAD_METHOD              exc_info
             1124  CALL_METHOD_0         0  '0 positional arguments'
             1126  LOAD_CONST               2
             1128  BINARY_SUBSCR    
             1130  CALL_METHOD_1         1  '1 positional argument'
             1132  RAISE_VARARGS_1       1  'exception instance'
             1134  POP_BLOCK        
             1136  LOAD_CONST               None
           1138_0  COME_FROM_FINALLY  1062  '1062'
             1138  LOAD_CONST               None
             1140  STORE_FAST               'e'
             1142  DELETE_FAST              'e'
             1144  END_FINALLY      
             1146  POP_EXCEPT       
             1148  JUMP_FORWARD       1152  'to 1152'
           1150_0  COME_FROM          1052  '1052'
             1150  END_FINALLY      
           1152_0  COME_FROM          1148  '1148'

Parse error at or near `COME_FROM' instruction at offset 500_0