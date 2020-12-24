# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/asynchat_25.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 10828 bytes
r"""A class supporting chat-style (command/response) protocols.

This class adds support for 'chat' style protocols - where one side
sends a 'command', and the other sends a response (examples would be
the common internet protocols - smtp, nntp, ftp, etc..).

The handle_read() method looks at the input stream for the current
'terminator' (usually '\r\n' for single-line responses, '\r\n.\r\n'
for multi-line output), calling self.found_terminator() on its
receipt.

for example:
Say you build an async nntp client using this class.  At the start
of the connection, you'll have self.terminator set to '\r\n', in
order to process the single-line greeting.  Just before issuing a
'LIST' command you'll set it to '\r\n.\r\n'.  The output of the LIST
command will be accumulated (using your own 'collect_incoming_data'
method) up to the terminator, and then control will be returned to
you - by calling your self.found_terminator() method.
"""
import socket
import supervisor.medusa as asyncore
from supervisor.compat import long
from supervisor.compat import as_bytes

class async_chat(asyncore.dispatcher):
    __doc__ = 'This is an abstract class.  You must derive from this class, and add\n    the two methods collect_incoming_data() and found_terminator()'
    ac_in_buffer_size = 4096
    ac_out_buffer_size = 4096

    def __init__(self, conn=None, map=None):
        self.ac_in_buffer = b''
        self.ac_out_buffer = b''
        self.producer_fifo = fifo()
        asyncore.dispatcher.__init__(self, conn, map)

    def collect_incoming_data(self, data):
        raise NotImplementedError('must be implemented in subclass')

    def found_terminator(self):
        raise NotImplementedError('must be implemented in subclass')

    def set_terminator(self, term):
        """Set the input delimiter.  Can be a fixed string of any length, an integer, or None"""
        self.terminator = term

    def get_terminator(self):
        return self.terminator

    def handle_read--- This code section failed: ---

 L.  88         0  SETUP_FINALLY        18  'to 18'

 L.  89         2  LOAD_FAST                'self'
                4  LOAD_METHOD              recv
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                ac_in_buffer_size
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'data'
               14  POP_BLOCK        
               16  JUMP_FORWARD         50  'to 50'
             18_0  COME_FROM_FINALLY     0  '0'

 L.  90        18  DUP_TOP          
               20  LOAD_GLOBAL              socket
               22  LOAD_ATTR                error
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    48  'to 48'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  91        34  LOAD_FAST                'self'
               36  LOAD_METHOD              handle_error
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L.  92        42  POP_EXCEPT       
               44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            26  '26'
               48  END_FINALLY      
             50_0  COME_FROM            16  '16'

 L.  94        50  LOAD_FAST                'self'
               52  DUP_TOP          
               54  LOAD_ATTR                ac_in_buffer
               56  LOAD_FAST                'data'
               58  INPLACE_ADD      
               60  ROT_TWO          
               62  STORE_ATTR               ac_in_buffer

 L. 101        64  LOAD_FAST                'self'
               66  LOAD_ATTR                ac_in_buffer
            68_70  POP_JUMP_IF_FALSE   416  'to 416'

 L. 102        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                ac_in_buffer
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'lb'

 L. 103        82  LOAD_FAST                'self'
               84  LOAD_METHOD              get_terminator
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'terminator'

 L. 104        90  LOAD_FAST                'terminator'
               92  POP_JUMP_IF_TRUE    114  'to 114'

 L. 106        94  LOAD_FAST                'self'
               96  LOAD_METHOD              collect_incoming_data
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                ac_in_buffer
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 107       106  LOAD_CONST               b''
              108  LOAD_FAST                'self'
              110  STORE_ATTR               ac_in_buffer
              112  JUMP_BACK            64  'to 64'
            114_0  COME_FROM            92  '92'

 L. 108       114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'terminator'
              118  LOAD_GLOBAL              int
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_TRUE    134  'to 134'
              124  LOAD_GLOBAL              isinstance
              126  LOAD_FAST                'terminator'
              128  LOAD_GLOBAL              long
              130  CALL_FUNCTION_2       2  ''
              132  POP_JUMP_IF_FALSE   232  'to 232'
            134_0  COME_FROM           122  '122'

 L. 110       134  LOAD_FAST                'terminator'
              136  STORE_FAST               'n'

 L. 111       138  LOAD_FAST                'lb'
              140  LOAD_FAST                'n'
              142  COMPARE_OP               <
              144  POP_JUMP_IF_FALSE   180  'to 180'

 L. 112       146  LOAD_FAST                'self'
              148  LOAD_METHOD              collect_incoming_data
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                ac_in_buffer
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L. 113       158  LOAD_CONST               b''
              160  LOAD_FAST                'self'
              162  STORE_ATTR               ac_in_buffer

 L. 114       164  LOAD_FAST                'self'
              166  DUP_TOP          
              168  LOAD_ATTR                terminator
              170  LOAD_FAST                'lb'
              172  INPLACE_SUBTRACT 
              174  ROT_TWO          
              176  STORE_ATTR               terminator
              178  JUMP_FORWARD        230  'to 230'
            180_0  COME_FROM           144  '144'

 L. 116       180  LOAD_FAST                'self'
              182  LOAD_METHOD              collect_incoming_data
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                ac_in_buffer
              188  LOAD_CONST               None
              190  LOAD_FAST                'n'
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          

 L. 117       200  LOAD_FAST                'self'
              202  LOAD_ATTR                ac_in_buffer
              204  LOAD_FAST                'n'
              206  LOAD_CONST               None
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_FAST                'self'
              214  STORE_ATTR               ac_in_buffer

 L. 118       216  LOAD_CONST               0
              218  LOAD_FAST                'self'
              220  STORE_ATTR               terminator

 L. 119       222  LOAD_FAST                'self'
              224  LOAD_METHOD              found_terminator
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          
            230_0  COME_FROM           178  '178'
              230  JUMP_BACK            64  'to 64'
            232_0  COME_FROM           132  '132'

 L. 128       232  LOAD_GLOBAL              len
              234  LOAD_FAST                'terminator'
              236  CALL_FUNCTION_1       1  ''
              238  STORE_FAST               'terminator_len'

 L. 129       240  LOAD_FAST                'self'
              242  LOAD_ATTR                ac_in_buffer
              244  LOAD_METHOD              find
              246  LOAD_FAST                'terminator'
              248  CALL_METHOD_1         1  ''
              250  STORE_FAST               'index'

 L. 130       252  LOAD_FAST                'index'
              254  LOAD_CONST               -1
              256  COMPARE_OP               !=
          258_260  POP_JUMP_IF_FALSE   322  'to 322'

 L. 132       262  LOAD_FAST                'index'
              264  LOAD_CONST               0
              266  COMPARE_OP               >
          268_270  POP_JUMP_IF_FALSE   292  'to 292'

 L. 134       272  LOAD_FAST                'self'
              274  LOAD_METHOD              collect_incoming_data
              276  LOAD_FAST                'self'
              278  LOAD_ATTR                ac_in_buffer
              280  LOAD_CONST               None
              282  LOAD_FAST                'index'
              284  BUILD_SLICE_2         2 
              286  BINARY_SUBSCR    
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          
            292_0  COME_FROM           268  '268'

 L. 135       292  LOAD_FAST                'self'
              294  LOAD_ATTR                ac_in_buffer
              296  LOAD_FAST                'index'
              298  LOAD_FAST                'terminator_len'
              300  BINARY_ADD       
              302  LOAD_CONST               None
              304  BUILD_SLICE_2         2 
              306  BINARY_SUBSCR    
              308  LOAD_FAST                'self'
              310  STORE_ATTR               ac_in_buffer

 L. 137       312  LOAD_FAST                'self'
              314  LOAD_METHOD              found_terminator
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          
              320  JUMP_BACK            64  'to 64'
            322_0  COME_FROM           258  '258'

 L. 140       322  LOAD_GLOBAL              find_prefix_at_end
              324  LOAD_FAST                'self'
              326  LOAD_ATTR                ac_in_buffer
              328  LOAD_FAST                'terminator'
              330  CALL_FUNCTION_2       2  ''
              332  STORE_FAST               'index'

 L. 141       334  LOAD_FAST                'index'
          336_338  POP_JUMP_IF_FALSE   396  'to 396'

 L. 142       340  LOAD_FAST                'index'
              342  LOAD_FAST                'lb'
              344  COMPARE_OP               !=
          346_348  POP_JUMP_IF_FALSE   416  'to 416'

 L. 144       350  LOAD_FAST                'self'
              352  LOAD_METHOD              collect_incoming_data
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                ac_in_buffer
              358  LOAD_CONST               None
              360  LOAD_FAST                'index'
              362  UNARY_NEGATIVE   
              364  BUILD_SLICE_2         2 
              366  BINARY_SUBSCR    
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          

 L. 145       372  LOAD_FAST                'self'
              374  LOAD_ATTR                ac_in_buffer
              376  LOAD_FAST                'index'
              378  UNARY_NEGATIVE   
              380  LOAD_CONST               None
              382  BUILD_SLICE_2         2 
              384  BINARY_SUBSCR    
              386  LOAD_FAST                'self'
              388  STORE_ATTR               ac_in_buffer

 L. 146   390_392  BREAK_LOOP          416  'to 416'
              394  JUMP_BACK            64  'to 64'
            396_0  COME_FROM           336  '336'

 L. 149       396  LOAD_FAST                'self'
              398  LOAD_METHOD              collect_incoming_data
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                ac_in_buffer
              404  CALL_METHOD_1         1  ''
              406  POP_TOP          

 L. 150       408  LOAD_CONST               b''
              410  LOAD_FAST                'self'
              412  STORE_ATTR               ac_in_buffer
              414  JUMP_BACK            64  'to 64'
            416_0  COME_FROM           346  '346'
            416_1  COME_FROM            68  '68'

Parse error at or near `LOAD_CONST' instruction at offset 44

    def handle_write(self):
        self.initiate_send

    def handle_close(self):
        self.close

    def push(self, data):
        data = as_bytes(data)
        self.producer_fifo.pushsimple_producer(data)
        self.initiate_send

    def push_with_producer(self, producer):
        self.producer_fifo.pushproducer
        self.initiate_send

    def readable(self):
        """predicate for inclusion in the readable for select()"""
        return len(self.ac_in_buffer) <= self.ac_in_buffer_size

    def writable(self):
        """predicate for inclusion in the writable for select()"""
        return not (self.ac_out_buffer == b'' and self.producer_fifo.is_empty and self.connected)

    def close_when_done(self):
        """automatically close this channel once the outgoing queue is empty"""
        self.producer_fifo.pushNone

    def refill_buffer(self):
        while len(self.producer_fifo):
            p = self.producer_fifo.first
            if p is None:
                if not self.ac_out_buffer:
                    self.producer_fifo.pop
                    self.close
                return
                if isinstance(p, bytes):
                    self.producer_fifo.pop
                    self.ac_out_buffer += p
                    return
                data = p.more
                if data:
                    self.ac_out_buffer = self.ac_out_buffer + data
                    return
                self.producer_fifo.pop
            else:
                return

    def initiate_send--- This code section failed: ---

 L. 212         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ac_out_buffer_size
                4  STORE_FAST               'obs'

 L. 214         6  LOAD_GLOBAL              len
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                ac_out_buffer
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_FAST                'obs'
               16  COMPARE_OP               <
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 215        20  LOAD_FAST                'self'
               22  LOAD_METHOD              refill_buffer
               24  CALL_METHOD_0         0  ''
               26  POP_TOP          
             28_0  COME_FROM            18  '18'

 L. 217        28  LOAD_FAST                'self'
               30  LOAD_ATTR                ac_out_buffer
               32  POP_JUMP_IF_FALSE   118  'to 118'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                connected
               38  POP_JUMP_IF_FALSE   118  'to 118'

 L. 219        40  SETUP_FINALLY        86  'to 86'

 L. 220        42  LOAD_FAST                'self'
               44  LOAD_METHOD              send
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                ac_out_buffer
               50  LOAD_CONST               None
               52  LOAD_FAST                'obs'
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'num_sent'

 L. 221        62  LOAD_FAST                'num_sent'
               64  POP_JUMP_IF_FALSE    82  'to 82'

 L. 222        66  LOAD_FAST                'self'
               68  LOAD_ATTR                ac_out_buffer
               70  LOAD_FAST                'num_sent'
               72  LOAD_CONST               None
               74  BUILD_SLICE_2         2 
               76  BINARY_SUBSCR    
               78  LOAD_FAST                'self'
               80  STORE_ATTR               ac_out_buffer
             82_0  COME_FROM            64  '64'
               82  POP_BLOCK        
               84  JUMP_FORWARD        118  'to 118'
             86_0  COME_FROM_FINALLY    40  '40'

 L. 224        86  DUP_TOP          
               88  LOAD_GLOBAL              socket
               90  LOAD_ATTR                error
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   116  'to 116'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 225       102  LOAD_FAST                'self'
              104  LOAD_METHOD              handle_error
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          

 L. 226       110  POP_EXCEPT       
              112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM            94  '94'
              116  END_FINALLY      
            118_0  COME_FROM            84  '84'
            118_1  COME_FROM            38  '38'
            118_2  COME_FROM            32  '32'

Parse error at or near `LOAD_CONST' instruction at offset 112

    def discard_buffers(self):
        self.ac_in_buffer = b''
        self.ac_out_buffer = b''
        while self.producer_fifo:
            self.producer_fifo.pop


class simple_producer:

    def __init__(self, data, buffer_size=512):
        self.data = data
        self.buffer_size = buffer_size

    def more(self):
        if len(self.data) > self.buffer_size:
            result = self.data[:self.buffer_size]
            self.data = self.data[self.buffer_size:]
            return result
        result = self.data
        self.data = b''
        return result


class fifo:

    def __init__(self, list=None):
        if not list:
            self.list = []
        else:
            self.list = list

    def __len__(self):
        return len(self.list)

    def is_empty(self):
        return self.list == []

    def first(self):
        return self.list[0]

    def push(self, data):
        self.list.appenddata

    def pop(self):
        if self.list:
            return (
             1, self.list.pop0)
        return (0, None)


def find_prefix_at_end(haystack, needle):
    l = len(needle) - 1
    while l:
        if not haystack.endswithneedle[:l]:
            l -= 1

    return l