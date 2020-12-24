# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/bw_atom.py
# Compiled at: 2019-12-01 22:29:38
# Size of source mod 2**32: 3121 bytes
from collections import OrderedDict
from pytwig.src.lib.luts import field_lists
from pytwig import bw_object

class Atom(bw_object.BW_Object):
    __doc__ = 'Any BW_Object that has a settings field (fieldnum 6194) that contains component_settings\n\t'

    def __init__(self, classnum=None, fields=None):
        if classnum == None:
            self.data['settings(6194)'] = bw_object.BW_Object('float_core.component_settings(236)')
            self.data['settings(6194)'].data['desktop_settings(612)'] = bw_object.BW_Object('float_core.desktop_settings(17)')
            return
        if classnum in field_lists.class_type_list:
            if field_lists.class_type_list[classnum][0] != 6194:
                raise TypeError('Non-atom initialized with atom initializer: {}'.format(classnum))
        super().__init__(classnum, fields)
        self.data['settings(6194)'] = bw_object.BW_Object('float_core.component_settings(236)')
        self.data['settings(6194)'].data['desktop_settings(612)'] = bw_object.BW_Object('float_core.desktop_settings(17)')

    def connect--- This code section failed: ---

 L.  25         0  LOAD_FAST                'self_index'
                2  LOAD_CONST               -1
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    38  'to 38'

 L.  26         8  LOAD_FAST                'self'
               10  LOAD_METHOD              get
               12  LOAD_CONST               6194
               14  CALL_METHOD_1         1  ''
               16  LOAD_METHOD              get
               18  LOAD_CONST               614
               20  CALL_METHOD_1         1  ''
               22  LOAD_METHOD              append
               24  LOAD_GLOBAL              bw_object
               26  LOAD_METHOD              BW_Object
               28  LOAD_CONST               105
               30  CALL_METHOD_1         1  ''
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          
               36  JUMP_FORWARD        100  'to 100'
             38_0  COME_FROM             6  '6'

 L.  27        38  LOAD_FAST                'self_index'
               40  LOAD_CONST               0
               42  COMPARE_OP               >=
               44  POP_JUMP_IF_FALSE   100  'to 100'

 L.  28        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'self'
               50  LOAD_METHOD              get
               52  LOAD_CONST               6194
               54  CALL_METHOD_1         1  ''
               56  LOAD_METHOD              get
               58  LOAD_CONST               614
               60  CALL_METHOD_1         1  ''
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_FAST                'self_index'
               66  COMPARE_OP               <=
               68  POP_JUMP_IF_FALSE   100  'to 100'

 L.  29        70  LOAD_FAST                'self'
               72  LOAD_METHOD              get
               74  LOAD_CONST               6194
               76  CALL_METHOD_1         1  ''
               78  LOAD_METHOD              get
               80  LOAD_CONST               614
               82  CALL_METHOD_1         1  ''
               84  LOAD_METHOD              append
               86  LOAD_GLOBAL              bw_object
               88  LOAD_METHOD              BW_Object
               90  LOAD_CONST               105
               92  CALL_METHOD_1         1  ''
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            46  'to 46'
            100_0  COME_FROM            68  '68'
            100_1  COME_FROM            44  '44'
            100_2  COME_FROM            36  '36'

 L.  32       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'obj'
              104  LOAD_GLOBAL              int
              106  CALL_FUNCTION_2       2  ''
          108_110  POP_JUMP_IF_FALSE   270  'to 270'

 L.  33       112  SETUP_FINALLY       248  'to 248'

 L.  34       114  LOAD_FAST                'obj'
              116  LOAD_CONST               (60, 154)
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   156  'to 156'

 L.  35       122  LOAD_FAST                'self'
              124  LOAD_METHOD              get
              126  LOAD_CONST               6194
              128  CALL_METHOD_1         1  ''
              130  LOAD_METHOD              get
              132  LOAD_CONST               614
              134  CALL_METHOD_1         1  ''
              136  LOAD_FAST                'self_index'
              138  BINARY_SUBSCR    
              140  LOAD_METHOD              set
              142  LOAD_CONST               248
              144  LOAD_GLOBAL              Proxy_Port
              146  LOAD_FAST                'obj'
              148  CALL_FUNCTION_1       1  ''
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          
              154  JUMP_FORWARD        188  'to 188'
            156_0  COME_FROM           120  '120'

 L.  37       156  LOAD_FAST                'self'
              158  LOAD_METHOD              get
              160  LOAD_CONST               6194
              162  CALL_METHOD_1         1  ''
              164  LOAD_METHOD              get
              166  LOAD_CONST               614
              168  CALL_METHOD_1         1  ''
              170  LOAD_FAST                'self_index'
              172  BINARY_SUBSCR    
              174  LOAD_METHOD              set
              176  LOAD_CONST               248
              178  LOAD_GLOBAL              Atom
              180  LOAD_FAST                'obj'
              182  CALL_FUNCTION_1       1  ''
              184  CALL_METHOD_2         2  ''
              186  POP_TOP          
            188_0  COME_FROM           154  '154'

 L.  38       188  LOAD_FAST                'quality'
              190  POP_JUMP_IF_FALSE   220  'to 220'

 L.  39       192  LOAD_FAST                'self'
              194  LOAD_METHOD              get
              196  LOAD_CONST               6194
              198  CALL_METHOD_1         1  ''
              200  LOAD_METHOD              get
              202  LOAD_CONST               614
              204  CALL_METHOD_1         1  ''
              206  LOAD_FAST                'self_index'
              208  BINARY_SUBSCR    
              210  LOAD_METHOD              set
              212  LOAD_CONST               1943
              214  LOAD_CONST               True
              216  CALL_METHOD_2         2  ''
              218  POP_TOP          
            220_0  COME_FROM           190  '190'

 L.  40       220  LOAD_FAST                'self'
              222  LOAD_METHOD              get
              224  LOAD_CONST               6194
              226  CALL_METHOD_1         1  ''
              228  LOAD_METHOD              get
              230  LOAD_CONST               614
              232  CALL_METHOD_1         1  ''
              234  LOAD_FAST                'self_index'
              236  BINARY_SUBSCR    
              238  LOAD_METHOD              get
              240  LOAD_CONST               248
              242  CALL_METHOD_1         1  ''
              244  POP_BLOCK        
              246  RETURN_VALUE     
            248_0  COME_FROM_FINALLY   112  '112'

 L.  41       248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L.  42       254  LOAD_GLOBAL              KeyError
              256  LOAD_STR                 "There was an issue adding an inport. Perhaps this isn't an atom?"
              258  CALL_FUNCTION_1       1  ''
              260  RAISE_VARARGS_1       1  'exception instance'
              262  POP_EXCEPT       
              264  JUMP_FORWARD        268  'to 268'
              266  END_FINALLY      
            268_0  COME_FROM           264  '264'
              268  JUMP_FORWARD        412  'to 412'
            270_0  COME_FROM           108  '108'

 L.  43       270  LOAD_GLOBAL              isinstance
              272  LOAD_FAST                'obj'
              274  LOAD_GLOBAL              Atom
              276  CALL_FUNCTION_2       2  ''
          278_280  POP_JUMP_IF_FALSE   404  'to 404'

 L.  44       282  LOAD_FAST                'self'
              284  LOAD_METHOD              get
              286  LOAD_CONST               6194
              288  CALL_METHOD_1         1  ''
              290  LOAD_METHOD              get
              292  LOAD_CONST               614
              294  CALL_METHOD_1         1  ''
              296  LOAD_FAST                'self_index'
              298  BINARY_SUBSCR    
              300  LOAD_METHOD              set
              302  LOAD_CONST               248
              304  LOAD_FAST                'obj'
              306  CALL_METHOD_2         2  ''
              308  POP_TOP          

 L.  45       310  LOAD_FAST                'quality'
          312_314  POP_JUMP_IF_FALSE   344  'to 344'

 L.  46       316  LOAD_FAST                'self'
              318  LOAD_METHOD              get
              320  LOAD_CONST               6194
              322  CALL_METHOD_1         1  ''
              324  LOAD_METHOD              get
              326  LOAD_CONST               614
              328  CALL_METHOD_1         1  ''
              330  LOAD_FAST                'self_index'
              332  BINARY_SUBSCR    
              334  LOAD_METHOD              set
              336  LOAD_CONST               1943
              338  LOAD_CONST               True
              340  CALL_METHOD_2         2  ''
              342  POP_TOP          
            344_0  COME_FROM           312  '312'

 L.  47       344  LOAD_FAST                'outport_index'
          346_348  POP_JUMP_IF_FALSE   378  'to 378'

 L.  48       350  LOAD_FAST                'self'
              352  LOAD_METHOD              get
              354  LOAD_CONST               6194
              356  CALL_METHOD_1         1  ''
              358  LOAD_METHOD              get
              360  LOAD_CONST               614
              362  CALL_METHOD_1         1  ''
              364  LOAD_FAST                'self_index'
              366  BINARY_SUBSCR    
              368  LOAD_METHOD              set
              370  LOAD_CONST               249
              372  LOAD_FAST                'outport_index'
              374  CALL_METHOD_2         2  ''
              376  POP_TOP          
            378_0  COME_FROM           346  '346'

 L.  49       378  LOAD_FAST                'self'
              380  LOAD_METHOD              get
              382  LOAD_CONST               6194
              384  CALL_METHOD_1         1  ''
              386  LOAD_METHOD              get
              388  LOAD_CONST               614
              390  CALL_METHOD_1         1  ''
              392  LOAD_FAST                'self_index'
              394  BINARY_SUBSCR    
              396  LOAD_METHOD              get
              398  LOAD_CONST               248
              400  CALL_METHOD_1         1  ''
              402  RETURN_VALUE     
            404_0  COME_FROM           278  '278'

 L.  51       404  LOAD_GLOBAL              TypeError
              406  LOAD_STR                 'Input is not a valid inport type'
              408  CALL_FUNCTION_1       1  ''
              410  RAISE_VARARGS_1       1  'exception instance'
            412_0  COME_FROM           268  '268'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 260

    def set_XY(self, x, y):
        self.get(6194).get(612).set(17, x).set(18, y)
        return self


class Proxy_Port(Atom):

    def set_port(self, type):
        if type == 'audio':
            port = bw_object.BW_Object('float_core.audio_port(242)')
            if self.classnum == 154:
                port.set_multi({499:' Audio out (PARENT)',  372:3})
            elif self.classnum == 50:
                port.set_multi({499:' Audio in (PARENT)',  372:3,  500:True})
            else:
                print(self.classnum)
                raise Error()
        elif type == 'note':
            port = bw_object.BW_Object('float_core.note_port(61)')
            if self.classnum == 154:
                port.set_multi({499: ' Note out'})
            elif self.classnum == 50:
                port.set_multi({499:' Note in',  500:True})
            else:
                raise Error()
        else:
            raise Error()
        self.set(301, port)
        return self