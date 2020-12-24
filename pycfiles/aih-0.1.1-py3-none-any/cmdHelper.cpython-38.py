# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\cmdHelper.py
# Compiled at: 2020-02-14 02:12:36
# Size of source mod 2**32: 4788 bytes
__doc__ = '\n@File    :   cmdHelper.py\n@Time    :   2019/02/27\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import sys
from enum import Enum
from colorama import init
init(autoreset=True)

def isInputYes(inputstr):
    """Return: bool"""
    if inputstr is None:
        return False
    inputstr = str(inputstr).lower()
    if inputstr == 'yes' or inputstr == 'y':
        return True
    return False


def myinput(desc):
    if sys.version_info[0] > 2:
        return input(desc)
    ret = raw_input(desc)
    if len(ret) > 0:
        if '\r' == ret[len(ret) - 1:]:
            ret = ret[:len(ret) - 1]
    return ret


def myinputInt--- This code section failed: ---

 L.  41         0  SETUP_FINALLY        24  'to 24'

 L.  42         2  LOAD_GLOBAL              myinput
                4  LOAD_FAST                'desc'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'stri'

 L.  43        10  LOAD_GLOBAL              int
               12  LOAD_FAST                'stri'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'ret'

 L.  44        18  LOAD_FAST                'ret'
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.  45        24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  46        30  LOAD_FAST                'default'
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
               38  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 20


def myinputFloat--- This code section failed: ---

 L.  50         0  SETUP_FINALLY        24  'to 24'

 L.  51         2  LOAD_GLOBAL              myinput
                4  LOAD_FAST                'desc'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'stri'

 L.  52        10  LOAD_GLOBAL              float
               12  LOAD_FAST                'stri'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'ret'

 L.  53        18  LOAD_FAST                'ret'
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.  54        24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  55        30  LOAD_FAST                'default'
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
               38  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 20


def myprintNoEnter(desc):
    sys.stdout.write(desc)


def findInArgv(stri):
    if sys.argv is None or len(sys.argv) == 0:
        return
    for item in sys.argv:
        if item == sys.argv[0]:
            pass
        elif item.find(stri) >= 0:
            return item


def converArgvToStr(array):
    stri = ''
    for item in array:
        if stri != '':
            stri = stri + ' '
        stri = stri + '"' + item + '"'

    return stri


class TextColor(Enum):
    """TextColor"""
    Black = 30
    Blue = 34
    Green = 32
    Red = 31
    Yellow = 33
    White = 37


class BackGroundColor(Enum):
    Black = 40
    Blue = 44
    Green = 42
    Red = 41
    Yellow = 43
    White = 47


def myprint(desc, textColor=None, bgColor=None):
    if textColor is None and bgColor is None:
        sys.stdout.write(desc)
    else:
        color = ''
        if textColor is not None:
            color = str(textColor.value)
        if bgColor is not None:
            if color != '':
                color = color + ';'
            color = color + str(bgColor.value)
        color = color + 'm'
        sys.stdout.write('\x1b[' + color + str(desc) + '\x1b[0m')


def showTable--- This code section failed: ---

 L. 124       0_2  SETUP_FINALLY       450  'to 450'

 L. 126         4  BUILD_LIST_0          0 
                6  STORE_FAST               'widths'

 L. 127         8  LOAD_FAST                'columns'
               10  GET_ITER         
               12  FOR_ITER             40  'to 40'
               14  STORE_FAST               'item'

 L. 128        16  LOAD_GLOBAL              str
               18  LOAD_FAST                'item'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'name'

 L. 129        24  LOAD_FAST                'widths'
               26  LOAD_METHOD              append
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'name'
               32  CALL_FUNCTION_1       1  ''
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
               38  JUMP_BACK            12  'to 12'

 L. 131        40  LOAD_FAST                'rows'
               42  GET_ITER         
               44  FOR_ITER            124  'to 124'
               46  STORE_FAST               'rObj'

 L. 132        48  LOAD_CONST               0
               50  STORE_FAST               'index'

 L. 133        52  LOAD_FAST                'rObj'
               54  GET_ITER         
             56_0  COME_FROM           114  '114'
               56  FOR_ITER            122  'to 122'
               58  STORE_FAST               'item'

 L. 134        60  LOAD_GLOBAL              len
               62  LOAD_GLOBAL              str
               64  LOAD_FAST                'item'
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_FAST                'widths'
               72  LOAD_FAST                'index'
               74  BINARY_SUBSCR    
               76  COMPARE_OP               >
               78  POP_JUMP_IF_FALSE    96  'to 96'

 L. 135        80  LOAD_GLOBAL              len
               82  LOAD_GLOBAL              str
               84  LOAD_FAST                'item'
               86  CALL_FUNCTION_1       1  ''
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_FAST                'widths'
               92  LOAD_FAST                'index'
               94  STORE_SUBSCR     
             96_0  COME_FROM            78  '78'

 L. 136        96  LOAD_FAST                'index'
               98  LOAD_CONST               1
              100  BINARY_ADD       
              102  STORE_FAST               'index'

 L. 137       104  LOAD_GLOBAL              len
              106  LOAD_FAST                'widths'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_FAST                'index'
              112  COMPARE_OP               <=
              114  POP_JUMP_IF_FALSE    56  'to 56'

 L. 138       116  POP_TOP          
              118  CONTINUE             44  'to 44'
              120  JUMP_BACK            56  'to 56'
              122  JUMP_BACK            44  'to 44'

 L. 140       124  LOAD_STR                 '-'
              126  STORE_FAST               'boardstr'

 L. 141       128  LOAD_FAST                'widths'
              130  GET_ITER         
              132  FOR_ITER            168  'to 168'
              134  STORE_FAST               'item'

 L. 142       136  LOAD_GLOBAL              range
              138  LOAD_FAST                'item'
              140  LOAD_CONST               2
              142  BINARY_ADD       
              144  LOAD_CONST               1
              146  BINARY_ADD       
              148  CALL_FUNCTION_1       1  ''
              150  GET_ITER         
              152  FOR_ITER            166  'to 166'
              154  STORE_FAST               'i'

 L. 143       156  LOAD_FAST                'boardstr'
              158  LOAD_STR                 '-'
              160  BINARY_ADD       
              162  STORE_FAST               'boardstr'
              164  JUMP_BACK           152  'to 152'
              166  JUMP_BACK           132  'to 132'

 L. 146       168  LOAD_GLOBAL              print
              170  LOAD_FAST                'boardstr'
              172  CALL_FUNCTION_1       1  ''
              174  POP_TOP          

 L. 147       176  LOAD_CONST               0
              178  STORE_FAST               'index'

 L. 148       180  LOAD_FAST                'columns'
              182  GET_ITER         
            184_0  COME_FROM           242  '242'
              184  FOR_ITER            250  'to 250'
              186  STORE_FAST               'item'

 L. 149       188  LOAD_FAST                'item'
              190  LOAD_METHOD              center
              192  LOAD_FAST                'widths'
              194  LOAD_FAST                'index'
              196  BINARY_SUBSCR    
              198  LOAD_CONST               2
              200  BINARY_ADD       
              202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'item'

 L. 150       206  LOAD_GLOBAL              myprintNoEnter
              208  LOAD_STR                 '|'
              210  CALL_FUNCTION_1       1  ''
              212  POP_TOP          

 L. 151       214  LOAD_GLOBAL              myprint
              216  LOAD_FAST                'item'
              218  LOAD_FAST                'colheadColor'
              220  CALL_FUNCTION_2       2  ''
              222  POP_TOP          

 L. 152       224  LOAD_FAST                'index'
              226  LOAD_CONST               1
              228  BINARY_ADD       
              230  STORE_FAST               'index'

 L. 153       232  LOAD_GLOBAL              len
              234  LOAD_FAST                'widths'
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_FAST                'index'
              240  COMPARE_OP               <=
              242  POP_JUMP_IF_FALSE   184  'to 184'

 L. 154       244  POP_TOP          
              246  BREAK_LOOP          250  'to 250'
              248  JUMP_BACK           184  'to 184'

 L. 155       250  LOAD_GLOBAL              print
              252  LOAD_STR                 '|'
              254  CALL_FUNCTION_1       1  ''
              256  POP_TOP          

 L. 156       258  LOAD_GLOBAL              print
              260  LOAD_FAST                'boardstr'
              262  CALL_FUNCTION_1       1  ''
              264  POP_TOP          

 L. 159       266  LOAD_FAST                'rows'
              268  GET_ITER         
              270  FOR_ITER            436  'to 436'
              272  STORE_FAST               'rObj'

 L. 160       274  LOAD_CONST               0
              276  STORE_FAST               'index'

 L. 161       278  LOAD_GLOBAL              range
              280  LOAD_GLOBAL              len
              282  LOAD_FAST                'columns'
              284  CALL_FUNCTION_1       1  ''
              286  CALL_FUNCTION_1       1  ''
              288  GET_ITER         
            290_0  COME_FROM           410  '410'
              290  FOR_ITER            424  'to 424'
              292  STORE_FAST               'index'

 L. 162       294  LOAD_GLOBAL              len
              296  LOAD_FAST                'rObj'
              298  CALL_FUNCTION_1       1  ''
              300  LOAD_FAST                'index'
              302  COMPARE_OP               >
          304_306  POP_JUMP_IF_FALSE   318  'to 318'

 L. 163       308  LOAD_FAST                'rObj'
              310  LOAD_FAST                'index'
              312  BINARY_SUBSCR    
              314  STORE_FAST               'item'
              316  JUMP_FORWARD        322  'to 322'
            318_0  COME_FROM           304  '304'

 L. 165       318  LOAD_STR                 ''
              320  STORE_FAST               'item'
            322_0  COME_FROM           316  '316'

 L. 166       322  LOAD_CONST               None
              324  STORE_FAST               'color'

 L. 167       326  LOAD_GLOBAL              len
              328  LOAD_FAST                'colsColor'
              330  CALL_FUNCTION_1       1  ''
              332  LOAD_FAST                'index'
              334  COMPARE_OP               >
          336_338  POP_JUMP_IF_FALSE   348  'to 348'

 L. 168       340  LOAD_FAST                'colsColor'
              342  LOAD_FAST                'index'
              344  BINARY_SUBSCR    
              346  STORE_FAST               'color'
            348_0  COME_FROM           336  '336'

 L. 170       348  LOAD_STR                 ' '
              350  LOAD_GLOBAL              str
              352  LOAD_FAST                'item'
              354  CALL_FUNCTION_1       1  ''
              356  BINARY_ADD       
              358  LOAD_METHOD              ljust
              360  LOAD_FAST                'widths'
              362  LOAD_FAST                'index'
              364  BINARY_SUBSCR    
              366  LOAD_CONST               2
              368  BINARY_ADD       
              370  CALL_METHOD_1         1  ''
              372  STORE_FAST               'item'

 L. 171       374  LOAD_GLOBAL              myprintNoEnter
              376  LOAD_STR                 '|'
              378  CALL_FUNCTION_1       1  ''
              380  POP_TOP          

 L. 172       382  LOAD_GLOBAL              myprint
              384  LOAD_FAST                'item'
              386  LOAD_FAST                'color'
              388  CALL_FUNCTION_2       2  ''
              390  POP_TOP          

 L. 173       392  LOAD_FAST                'index'
              394  LOAD_CONST               1
              396  BINARY_ADD       
              398  STORE_FAST               'index'

 L. 174       400  LOAD_GLOBAL              len
              402  LOAD_FAST                'widths'
              404  CALL_FUNCTION_1       1  ''
              406  LOAD_FAST                'index'
              408  COMPARE_OP               <=
          410_412  POP_JUMP_IF_FALSE   290  'to 290'

 L. 175       414  POP_TOP          
          416_418  BREAK_LOOP          424  'to 424'
          420_422  JUMP_BACK           290  'to 290'

 L. 176       424  LOAD_GLOBAL              print
              426  LOAD_STR                 '|'
              428  CALL_FUNCTION_1       1  ''
              430  POP_TOP          
          432_434  JUMP_BACK           270  'to 270'

 L. 177       436  LOAD_GLOBAL              print
              438  LOAD_FAST                'boardstr'
              440  CALL_FUNCTION_1       1  ''
              442  POP_TOP          

 L. 178       444  POP_BLOCK        
              446  LOAD_CONST               True
              448  RETURN_VALUE     
            450_0  COME_FROM_FINALLY     0  '0'

 L. 179       450  POP_TOP          
              452  POP_TOP          
              454  POP_TOP          

 L. 180       456  POP_EXCEPT       
              458  LOAD_CONST               False
              460  RETURN_VALUE     
              462  END_FINALLY      

Parse error at or near `COME_FROM_FINALLY' instruction at offset 450_0