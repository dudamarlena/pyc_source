# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/mashups/iobject.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4191 bytes
import os

def int_val_fn(v):
    try:
        int(v)
        return True
    except:
        return False


class IObject(object):

    def choose_from_list--- This code section failed: ---

 L.  34         0  LOAD_FAST                'item_list'
                3  POP_JUMP_IF_TRUE     20  'to 20'

 L.  35         6  LOAD_GLOBAL              print
                9  LOAD_STR                 'No Choices Available'
               12  CALL_FUNCTION_1       1  '1 positional, 0 named'
               15  POP_TOP          

 L.  36        16  LOAD_CONST               None
               19  RETURN_END_IF    
             20_0  COME_FROM             3  '3'

 L.  37        20  LOAD_CONST               None
               23  STORE_FAST               'choice'

 L.  38        26  SETUP_LOOP          501  'to 501'
               29  LOAD_FAST                'choice'
               32  POP_JUMP_IF_TRUE    500  'to 500'

 L.  39        35  LOAD_CONST               1
               38  STORE_FAST               'n'

 L.  40        41  BUILD_LIST_0          0 
               44  STORE_FAST               'choices'

 L.  41        47  SETUP_LOOP          286  'to 286'
               50  LOAD_FAST                'item_list'
               53  GET_ITER         
               54  FOR_ITER            285  'to 285'
               57  STORE_FAST               'item'

 L.  42        60  LOAD_GLOBAL              isinstance
               63  LOAD_FAST                'item'
               66  LOAD_GLOBAL              basestring
               69  CALL_FUNCTION_2       2  '2 positional, 0 named'
               72  POP_JUMP_IF_FALSE   121  'to 121'

 L.  43        75  LOAD_GLOBAL              print
               78  LOAD_STR                 '[%d] %s'
               81  LOAD_FAST                'n'
               84  LOAD_FAST                'item'
               87  BUILD_TUPLE_2         2 
               90  BINARY_MODULO    
               91  CALL_FUNCTION_1       1  '1 positional, 0 named'
               94  POP_TOP          

 L.  44        95  LOAD_FAST                'choices'
               98  LOAD_ATTR                append
              101  LOAD_FAST                'item'
              104  CALL_FUNCTION_1       1  '1 positional, 0 named'
              107  POP_TOP          

 L.  45       108  LOAD_FAST                'n'
              111  LOAD_CONST               1
              114  INPLACE_ADD      
              115  STORE_FAST               'n'
              118  JUMP_BACK            54  'to 54'

 L.  47       121  LOAD_FAST                'item'
              124  UNPACK_SEQUENCE_3     3 
              127  STORE_FAST               'obj'
              130  STORE_FAST               'id'
              133  STORE_FAST               'desc'

 L.  48       136  LOAD_FAST                'desc'
              139  POP_JUMP_IF_FALSE   215  'to 215'

 L.  49       142  LOAD_FAST                'desc'
              145  LOAD_ATTR                find
              148  LOAD_FAST                'search_str'
              151  CALL_FUNCTION_1       1  '1 positional, 0 named'
              154  LOAD_CONST               0
              157  COMPARE_OP               >=
              160  POP_JUMP_IF_FALSE   282  'to 282'

 L.  50       163  LOAD_GLOBAL              print
              166  LOAD_STR                 '[%d] %s - %s'
              169  LOAD_FAST                'n'
              172  LOAD_FAST                'id'
              175  LOAD_FAST                'desc'
              178  BUILD_TUPLE_3         3 
              181  BINARY_MODULO    
              182  CALL_FUNCTION_1       1  '1 positional, 0 named'
              185  POP_TOP          

 L.  51       186  LOAD_FAST                'choices'
              189  LOAD_ATTR                append
              192  LOAD_FAST                'obj'
              195  CALL_FUNCTION_1       1  '1 positional, 0 named'
              198  POP_TOP          

 L.  52       199  LOAD_FAST                'n'
              202  LOAD_CONST               1
              205  INPLACE_ADD      
              206  STORE_FAST               'n'
              209  JUMP_ABSOLUTE       282  'to 282'
              212  JUMP_BACK            54  'to 54'

 L.  54       215  LOAD_FAST                'id'
              218  LOAD_ATTR                find
              221  LOAD_FAST                'search_str'
              224  CALL_FUNCTION_1       1  '1 positional, 0 named'
              227  LOAD_CONST               0
              230  COMPARE_OP               >=
              233  POP_JUMP_IF_FALSE    54  'to 54'

 L.  55       236  LOAD_GLOBAL              print
              239  LOAD_STR                 '[%d] %s'
              242  LOAD_FAST                'n'
              245  LOAD_FAST                'id'
              248  BUILD_TUPLE_2         2 
              251  BINARY_MODULO    
              252  CALL_FUNCTION_1       1  '1 positional, 0 named'
              255  POP_TOP          

 L.  56       256  LOAD_FAST                'choices'
              259  LOAD_ATTR                append
              262  LOAD_FAST                'obj'
              265  CALL_FUNCTION_1       1  '1 positional, 0 named'
              268  POP_TOP          

 L.  57       269  LOAD_FAST                'n'
              272  LOAD_CONST               1
              275  INPLACE_ADD      
              276  STORE_FAST               'n'
              279  CONTINUE             54  'to 54'
              282  JUMP_BACK            54  'to 54'
              285  POP_BLOCK        
            286_0  COME_FROM_LOOP       47  '47'

 L.  58       286  LOAD_FAST                'choices'
              289  POP_JUMP_IF_FALSE   481  'to 481'

 L.  59       292  LOAD_GLOBAL              raw_input
              295  LOAD_STR                 '%s[1-%d]: '
              298  LOAD_FAST                'prompt'
              301  LOAD_GLOBAL              len
              304  LOAD_FAST                'choices'
              307  CALL_FUNCTION_1       1  '1 positional, 0 named'
              310  BUILD_TUPLE_2         2 
              313  BINARY_MODULO    
              314  CALL_FUNCTION_1       1  '1 positional, 0 named'
              317  STORE_FAST               'val'

 L.  60       320  LOAD_FAST                'val'
              323  LOAD_ATTR                startswith
              326  LOAD_STR                 '/'
              329  CALL_FUNCTION_1       1  '1 positional, 0 named'
              332  POP_JUMP_IF_FALSE   354  'to 354'

 L.  61       335  LOAD_FAST                'val'
              338  LOAD_CONST               1
              341  LOAD_CONST               None
              344  BUILD_SLICE_2         2 
              347  BINARY_SUBSCR    
              348  STORE_FAST               'search_str'
              351  JUMP_ABSOLUTE       497  'to 497'
              354  ELSE                     '478'

 L.  63       354  SETUP_EXCEPT        403  'to 403'

 L.  64       357  LOAD_GLOBAL              int
              360  LOAD_FAST                'val'
              363  CALL_FUNCTION_1       1  '1 positional, 0 named'
              366  STORE_FAST               'int_val'

 L.  65       369  LOAD_FAST                'int_val'
              372  LOAD_CONST               0
              375  COMPARE_OP               ==
              378  POP_JUMP_IF_FALSE   385  'to 385'

 L.  66       381  LOAD_CONST               None
              384  RETURN_END_IF    
            385_0  COME_FROM           378  '378'

 L.  67       385  LOAD_FAST                'choices'
              388  LOAD_FAST                'int_val'
              391  LOAD_CONST               1
              394  BINARY_SUBTRACT  
              395  BINARY_SUBSCR    
              396  STORE_FAST               'choice'
              399  POP_BLOCK        
              400  JUMP_ABSOLUTE       497  'to 497'
            403_0  COME_FROM_EXCEPT    354  '354'

 L.  68       403  DUP_TOP          
              404  LOAD_GLOBAL              ValueError
              407  COMPARE_OP               exception-match
              410  POP_JUMP_IF_FALSE   434  'to 434'
              413  POP_TOP          
              414  POP_TOP          
              415  POP_TOP          

 L.  69       416  LOAD_GLOBAL              print
              419  LOAD_STR                 '%s is not a valid choice'
              422  LOAD_FAST                'val'
              425  BINARY_MODULO    
              426  CALL_FUNCTION_1       1  '1 positional, 0 named'
              429  POP_TOP          
              430  POP_EXCEPT       
              431  JUMP_ABSOLUTE       497  'to 497'

 L.  70       434  DUP_TOP          
              435  LOAD_GLOBAL              IndexError
              438  COMPARE_OP               exception-match
              441  POP_JUMP_IF_FALSE   477  'to 477'
              444  POP_TOP          
              445  POP_TOP          
              446  POP_TOP          

 L.  71       447  LOAD_GLOBAL              print
              450  LOAD_STR                 '%s is not within the range[1-%d]'
              453  LOAD_FAST                'val'

 L.  72       456  LOAD_GLOBAL              len
              459  LOAD_FAST                'choices'
              462  CALL_FUNCTION_1       1  '1 positional, 0 named'
              465  BUILD_TUPLE_2         2 
              468  BINARY_MODULO    
              469  CALL_FUNCTION_1       1  '1 positional, 0 named'
              472  POP_TOP          
              473  POP_EXCEPT       
              474  JUMP_ABSOLUTE       497  'to 497'
              477  END_FINALLY      
              478  JUMP_BACK            29  'to 29'

 L.  74       481  LOAD_GLOBAL              print
              484  LOAD_STR                 'No objects matched your pattern'
              487  CALL_FUNCTION_1       1  '1 positional, 0 named'
              490  POP_TOP          

 L.  75       491  LOAD_STR                 ''
              494  STORE_FAST               'search_str'
            497_0  COME_FROM_EXCEPT_CLAUSE   431  '431'
              497  JUMP_BACK            29  'to 29'
              500  POP_BLOCK        
            501_0  COME_FROM_LOOP       26  '26'

 L.  76       501  LOAD_FAST                'choice'
              504  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 497_0

    def get_string(self, prompt, validation_fn=None):
        okay = False
        while not okay:
            val = raw_input('%s: ' % prompt)
            if validation_fn:
                okay = validation_fn(val)
                if not okay:
                    print('Invalid value: %s' % val)
            else:
                okay = True

        return val

    def get_filename(self, prompt):
        okay = False
        val = ''
        while not okay:
            val = raw_input('%s: %s' % (prompt, val))
            val = os.path.expanduser(val)
            if os.path.isfile(val):
                okay = True
            elif os.path.isdir(val):
                path = val
                val = self.choose_from_list(os.listdir(path))
                if val:
                    val = os.path.joinpathval
                    okay = True
                else:
                    val = ''
            else:
                print('Invalid value: %s' % val)
                val = ''

        return val

    def get_int(self, prompt):
        s = self.get_stringpromptint_val_fn
        return int(s)