# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/default_handler.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 6355 bytes
RCS_ID = '$Id: default_handler.py,v 1.8 2002/08/01 18:15:45 akuchling Exp $'
import mimetypes, re, stat
import supervisor.medusa.http_date as http_date
import supervisor.medusa.http_server as http_server
import supervisor.medusa.producers as producers
from supervisor.medusa.util import html_repr
unquote = http_server.unquote
import supervisor.medusa.counter as counter

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

    def handle_request--- This code section failed: ---

 L.  79         0  LOAD_FAST                'request'
                2  LOAD_ATTR                command
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                valid_commands
                8  COMPARE_OP               not-in
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L.  80        12  LOAD_FAST                'request'
               14  LOAD_METHOD              error
               16  LOAD_CONST               400
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L.  81        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            10  '10'

 L.  83        26  LOAD_FAST                'self'
               28  LOAD_ATTR                hit_counter
               30  LOAD_METHOD              increment
               32  CALL_METHOD_0         0  ''
               34  POP_TOP          

 L.  85        36  LOAD_FAST                'request'
               38  LOAD_METHOD              split_uri
               40  CALL_METHOD_0         0  ''
               42  UNPACK_SEQUENCE_4     4 
               44  STORE_FAST               'path'
               46  STORE_FAST               'params'
               48  STORE_FAST               'query'
               50  STORE_FAST               'fragment'

 L.  87        52  LOAD_STR                 '%'
               54  LOAD_FAST                'path'
               56  COMPARE_OP               in
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L.  88        60  LOAD_GLOBAL              unquote
               62  LOAD_FAST                'path'
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'path'
             68_0  COME_FROM            58  '58'

 L.  91        68  LOAD_FAST                'path'
               70  POP_JUMP_IF_FALSE    98  'to 98'
               72  LOAD_FAST                'path'
               74  LOAD_CONST               0
               76  BINARY_SUBSCR    
               78  LOAD_STR                 '/'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    98  'to 98'

 L.  92        84  LOAD_FAST                'path'
               86  LOAD_CONST               1
               88  LOAD_CONST               None
               90  BUILD_SLICE_2         2 
               92  BINARY_SUBSCR    
               94  STORE_FAST               'path'
               96  JUMP_BACK            68  'to 68'
             98_0  COME_FROM            82  '82'
             98_1  COME_FROM            70  '70'

 L.  94        98  LOAD_FAST                'self'
              100  LOAD_ATTR                filesystem
              102  LOAD_METHOD              isdir
              104  LOAD_FAST                'path'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_FALSE   254  'to 254'

 L.  95       110  LOAD_FAST                'path'
              112  POP_JUMP_IF_FALSE   162  'to 162'
              114  LOAD_FAST                'path'
              116  LOAD_CONST               -1
              118  BINARY_SUBSCR    
              120  LOAD_STR                 '/'
              122  COMPARE_OP               !=
              124  POP_JUMP_IF_FALSE   162  'to 162'

 L.  96       126  LOAD_STR                 'http://%s/%s/'

 L.  97       128  LOAD_FAST                'request'
              130  LOAD_ATTR                channel
              132  LOAD_ATTR                server
              134  LOAD_ATTR                server_name

 L.  98       136  LOAD_FAST                'path'

 L.  96       138  BUILD_TUPLE_2         2 
              140  BINARY_MODULO    
              142  LOAD_FAST                'request'
              144  LOAD_STR                 'Location'
              146  STORE_SUBSCR     

 L. 100       148  LOAD_FAST                'request'
              150  LOAD_METHOD              error
              152  LOAD_CONST               301
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L. 101       158  LOAD_CONST               None
              160  RETURN_VALUE     
            162_0  COME_FROM           124  '124'
            162_1  COME_FROM           112  '112'

 L. 106       162  LOAD_CONST               0
              164  STORE_FAST               'found'

 L. 107       166  LOAD_FAST                'path'
              168  POP_JUMP_IF_FALSE   190  'to 190'
              170  LOAD_FAST                'path'
              172  LOAD_CONST               -1
              174  BINARY_SUBSCR    
              176  LOAD_STR                 '/'
              178  COMPARE_OP               !=
              180  POP_JUMP_IF_FALSE   190  'to 190'

 L. 108       182  LOAD_FAST                'path'
              184  LOAD_STR                 '/'
              186  INPLACE_ADD      
              188  STORE_FAST               'path'
            190_0  COME_FROM           180  '180'
            190_1  COME_FROM           168  '168'

 L. 109       190  LOAD_FAST                'self'
              192  LOAD_ATTR                directory_defaults
              194  GET_ITER         
            196_0  COME_FROM           218  '218'
              196  FOR_ITER            234  'to 234'
              198  STORE_FAST               'default'

 L. 110       200  LOAD_FAST                'path'
              202  LOAD_FAST                'default'
              204  BINARY_ADD       
              206  STORE_FAST               'p'

 L. 111       208  LOAD_FAST                'self'
              210  LOAD_ATTR                filesystem
              212  LOAD_METHOD              isfile
              214  LOAD_FAST                'p'
              216  CALL_METHOD_1         1  ''
              218  POP_JUMP_IF_FALSE   196  'to 196'

 L. 112       220  LOAD_FAST                'p'
              222  STORE_FAST               'path'

 L. 113       224  LOAD_CONST               1
              226  STORE_FAST               'found'

 L. 114       228  POP_TOP          
              230  BREAK_LOOP          234  'to 234'
              232  JUMP_BACK           196  'to 196'

 L. 115       234  LOAD_FAST                'found'
              236  POP_JUMP_IF_TRUE    252  'to 252'

 L. 116       238  LOAD_FAST                'request'
              240  LOAD_METHOD              error
              242  LOAD_CONST               404
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 117       248  LOAD_CONST               None
              250  RETURN_VALUE     
            252_0  COME_FROM           236  '236'
              252  JUMP_FORWARD        282  'to 282'
            254_0  COME_FROM           108  '108'

 L. 119       254  LOAD_FAST                'self'
              256  LOAD_ATTR                filesystem
              258  LOAD_METHOD              isfile
              260  LOAD_FAST                'path'
              262  CALL_METHOD_1         1  ''
          264_266  POP_JUMP_IF_TRUE    282  'to 282'

 L. 120       268  LOAD_FAST                'request'
              270  LOAD_METHOD              error
              272  LOAD_CONST               404
              274  CALL_METHOD_1         1  ''
              276  POP_TOP          

 L. 121       278  LOAD_CONST               None
              280  RETURN_VALUE     
            282_0  COME_FROM           264  '264'
            282_1  COME_FROM           252  '252'

 L. 123       282  LOAD_FAST                'self'
              284  LOAD_ATTR                filesystem
              286  LOAD_METHOD              stat
              288  LOAD_FAST                'path'
              290  CALL_METHOD_1         1  ''
              292  LOAD_GLOBAL              stat
              294  LOAD_ATTR                ST_SIZE
              296  BINARY_SUBSCR    
              298  STORE_FAST               'file_length'

 L. 125       300  LOAD_GLOBAL              get_header_match
              302  LOAD_GLOBAL              IF_MODIFIED_SINCE
              304  LOAD_FAST                'request'
              306  LOAD_ATTR                header
              308  CALL_FUNCTION_2       2  ''
              310  STORE_FAST               'ims'

 L. 127       312  LOAD_CONST               1
              314  STORE_FAST               'length_match'

 L. 128       316  LOAD_FAST                'ims'
          318_320  POP_JUMP_IF_FALSE   378  'to 378'

 L. 129       322  LOAD_FAST                'ims'
              324  LOAD_METHOD              group
              326  LOAD_CONST               4
              328  CALL_METHOD_1         1  ''
              330  STORE_FAST               'length'

 L. 130       332  LOAD_FAST                'length'
          334_336  POP_JUMP_IF_FALSE   378  'to 378'

 L. 131       338  SETUP_FINALLY       366  'to 366'

 L. 132       340  LOAD_GLOBAL              int
              342  LOAD_FAST                'length'
              344  CALL_FUNCTION_1       1  ''
              346  STORE_FAST               'length'

 L. 133       348  LOAD_FAST                'length'
              350  LOAD_FAST                'file_length'
              352  COMPARE_OP               !=
          354_356  POP_JUMP_IF_FALSE   362  'to 362'

 L. 134       358  LOAD_CONST               0
              360  STORE_FAST               'length_match'
            362_0  COME_FROM           354  '354'
              362  POP_BLOCK        
              364  JUMP_FORWARD        378  'to 378'
            366_0  COME_FROM_FINALLY   338  '338'

 L. 135       366  POP_TOP          
              368  POP_TOP          
              370  POP_TOP          

 L. 136       372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
              376  END_FINALLY      
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           364  '364'
            378_2  COME_FROM           334  '334'
            378_3  COME_FROM           318  '318'

 L. 138       378  LOAD_CONST               0
              380  STORE_FAST               'ims_date'

 L. 140       382  LOAD_FAST                'ims'
          384_386  POP_JUMP_IF_FALSE   404  'to 404'

 L. 141       388  LOAD_GLOBAL              http_date
              390  LOAD_METHOD              parse_http_date
              392  LOAD_FAST                'ims'
              394  LOAD_METHOD              group
              396  LOAD_CONST               1
              398  CALL_METHOD_1         1  ''
              400  CALL_METHOD_1         1  ''
              402  STORE_FAST               'ims_date'
            404_0  COME_FROM           384  '384'

 L. 143       404  SETUP_FINALLY       428  'to 428'

 L. 144       406  LOAD_FAST                'self'
              408  LOAD_ATTR                filesystem
              410  LOAD_METHOD              stat
              412  LOAD_FAST                'path'
              414  CALL_METHOD_1         1  ''
              416  LOAD_GLOBAL              stat
              418  LOAD_ATTR                ST_MTIME
              420  BINARY_SUBSCR    
              422  STORE_FAST               'mtime'
              424  POP_BLOCK        
              426  JUMP_FORWARD        452  'to 452'
            428_0  COME_FROM_FINALLY   404  '404'

 L. 145       428  POP_TOP          
              430  POP_TOP          
              432  POP_TOP          

 L. 146       434  LOAD_FAST                'request'
              436  LOAD_METHOD              error
              438  LOAD_CONST               404
              440  CALL_METHOD_1         1  ''
              442  POP_TOP          

 L. 147       444  POP_EXCEPT       
              446  LOAD_CONST               None
              448  RETURN_VALUE     
              450  END_FINALLY      
            452_0  COME_FROM           426  '426'

 L. 149       452  LOAD_FAST                'length_match'
          454_456  POP_JUMP_IF_FALSE   502  'to 502'
              458  LOAD_FAST                'ims_date'
          460_462  POP_JUMP_IF_FALSE   502  'to 502'

 L. 150       464  LOAD_FAST                'mtime'
              466  LOAD_FAST                'ims_date'
              468  COMPARE_OP               <=
          470_472  POP_JUMP_IF_FALSE   502  'to 502'

 L. 151       474  LOAD_CONST               304
              476  LOAD_FAST                'request'
              478  STORE_ATTR               reply_code

 L. 152       480  LOAD_FAST                'request'
              482  LOAD_METHOD              done
              484  CALL_METHOD_0         0  ''
              486  POP_TOP          

 L. 153       488  LOAD_FAST                'self'
              490  LOAD_ATTR                cache_counter
              492  LOAD_METHOD              increment
              494  CALL_METHOD_0         0  ''
              496  POP_TOP          

 L. 154       498  LOAD_CONST               None
              500  RETURN_VALUE     
            502_0  COME_FROM           470  '470'
            502_1  COME_FROM           460  '460'
            502_2  COME_FROM           454  '454'

 L. 155       502  SETUP_FINALLY       522  'to 522'

 L. 156       504  LOAD_FAST                'self'
              506  LOAD_ATTR                filesystem
              508  LOAD_METHOD              open
              510  LOAD_FAST                'path'
              512  LOAD_STR                 'rb'
              514  CALL_METHOD_2         2  ''
              516  STORE_FAST               'file'
              518  POP_BLOCK        
              520  JUMP_FORWARD        556  'to 556'
            522_0  COME_FROM_FINALLY   502  '502'

 L. 157       522  DUP_TOP          
              524  LOAD_GLOBAL              IOError
              526  COMPARE_OP               exception-match
          528_530  POP_JUMP_IF_FALSE   554  'to 554'
              532  POP_TOP          
              534  POP_TOP          
              536  POP_TOP          

 L. 158       538  LOAD_FAST                'request'
              540  LOAD_METHOD              error
              542  LOAD_CONST               404
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          

 L. 159       548  POP_EXCEPT       
              550  LOAD_CONST               None
              552  RETURN_VALUE     
            554_0  COME_FROM           528  '528'
              554  END_FINALLY      
            556_0  COME_FROM           520  '520'

 L. 161       556  LOAD_GLOBAL              http_date
              558  LOAD_METHOD              build_http_date
              560  LOAD_FAST                'mtime'
              562  CALL_METHOD_1         1  ''
              564  LOAD_FAST                'request'
              566  LOAD_STR                 'Last-Modified'
              568  STORE_SUBSCR     

 L. 162       570  LOAD_FAST                'file_length'
              572  LOAD_FAST                'request'
              574  LOAD_STR                 'Content-Length'
              576  STORE_SUBSCR     

 L. 163       578  LOAD_FAST                'self'
              580  LOAD_METHOD              set_content_type
              582  LOAD_FAST                'path'
              584  LOAD_FAST                'request'
              586  CALL_METHOD_2         2  ''
              588  POP_TOP          

 L. 165       590  LOAD_FAST                'request'
              592  LOAD_ATTR                command
              594  LOAD_STR                 'GET'
              596  COMPARE_OP               ==
          598_600  POP_JUMP_IF_FALSE   618  'to 618'

 L. 166       602  LOAD_FAST                'request'
              604  LOAD_METHOD              push
              606  LOAD_FAST                'self'
              608  LOAD_METHOD              default_file_producer
              610  LOAD_FAST                'file'
              612  CALL_METHOD_1         1  ''
              614  CALL_METHOD_1         1  ''
              616  POP_TOP          
            618_0  COME_FROM           598  '598'

 L. 168       618  LOAD_FAST                'self'
              620  LOAD_ATTR                file_counter
              622  LOAD_METHOD              increment
              624  CALL_METHOD_0         0  ''
              626  POP_TOP          

 L. 169       628  LOAD_FAST                'request'
              630  LOAD_METHOD              done
              632  CALL_METHOD_0         0  ''
              634  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 446

    def set_content_type(self, path, request):
        typ, encoding = mimetypes.guess_typepath
        if typ is not None:
            request['Content-Type'] = typ
        else:
            request['Content-Type'] = 'text/plain'

    def status(self):
        return producers.simple_producer('<li>%s' % html_repr(self) + '<ul>' + '  <li><b>Total Hits:</b> %s' % self.hit_counter + '  <li><b>Files Delivered:</b> %s' % self.file_counter + '  <li><b>Cache Hits:</b> %s' % self.cache_counter + '</ul>')


IF_MODIFIED_SINCE = re.compile('If-Modified-Since: ([^;]+)((; length=([0-9]+)$)|$)', re.IGNORECASE)
USER_AGENT = re.compile('User-Agent: (.*)', re.IGNORECASE)
CONTENT_TYPE = re.compile("Content-Type: ([^;]+)((; boundary=([A-Za-z0-9\\'\\(\\)+_,./:=?-]+)$)|$)", re.IGNORECASE)
get_header = http_server.get_header
get_header_match = http_server.get_header_match

def get_extension(path):
    dirsep = path.rfind'/'
    dotsep = path.rfind'.'
    if dotsep > dirsep:
        return path[dotsep + 1:]
    return ''