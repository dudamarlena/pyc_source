# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\systemHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 2601 bytes
__doc__ = '\n@File    :   systemHelper.py\n@Time    :   2018/12/20\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import os, platform, subprocess

def getOwnPath(in__file__):
    return os.path.dirname(os.path.realpath(in__file__))


def isWindows():
    sysName = platform.system()
    return sysName == 'Windows'


def isLinux():
    sysName = platform.system()
    return sysName == 'Linux'


def getProcessID--- This code section failed: ---

 L.  30       0_2  SETUP_FINALLY       260  'to 260'

 L.  31         4  BUILD_LIST_0          0 
                6  STORE_FAST               'retid'

 L.  32         8  LOAD_GLOBAL              isLinux
               10  CALL_FUNCTION_0       0  ''
               12  POP_JUMP_IF_FALSE    92  'to 92'

 L.  33        14  LOAD_GLOBAL              os
               16  LOAD_METHOD              popen
               18  LOAD_STR                 'ps aux | grep "'
               20  LOAD_FAST                'name'
               22  BINARY_ADD       
               24  LOAD_STR                 '" | grep -v grep'
               26  BINARY_ADD       
               28  CALL_METHOD_1         1  ''
               30  LOAD_METHOD              readlines
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'lines'

 L.  34        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'lines'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_CONST               0
               44  COMPARE_OP               <=
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L.  35        48  BUILD_LIST_0          0 
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM            46  '46'

 L.  36        54  LOAD_FAST                'lines'
               56  GET_ITER         
               58  FOR_ITER             90  'to 90'
               60  STORE_FAST               'item'

 L.  37        62  LOAD_FAST                'item'
               64  LOAD_METHOD              split
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'array'

 L.  38        70  LOAD_FAST                'retid'
               72  LOAD_METHOD              append
               74  LOAD_GLOBAL              int
               76  LOAD_FAST                'array'
               78  LOAD_CONST               1
               80  BINARY_SUBSCR    
               82  CALL_FUNCTION_1       1  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  JUMP_BACK            58  'to 58'
               90  JUMP_FORWARD        254  'to 254'
             92_0  COME_FROM            12  '12'

 L.  40        92  LOAD_CONST               0
               94  LOAD_CONST               None
               96  IMPORT_NAME              psutil
               98  STORE_FAST               'psutil'

 L.  41       100  LOAD_GLOBAL              list
              102  LOAD_FAST                'psutil'
              104  LOAD_METHOD              process_iter
              106  CALL_METHOD_0         0  ''
              108  CALL_FUNCTION_1       1  ''
              110  STORE_FAST               'pidList'

 L.  42       112  LOAD_FAST                'pidList'
              114  GET_ITER         
              116  FOR_ITER            254  'to 254'
              118  STORE_FAST               'item'

 L.  44       120  LOAD_GLOBAL              str
              122  LOAD_FAST                'item'
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'stri'

 L.  45       128  LOAD_FAST                'stri'
              130  LOAD_CONST               15
              132  LOAD_CONST               -1
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  STORE_FAST               'stri'

 L.  47       140  LOAD_FAST                'stri'
              142  LOAD_FAST                'stri'
              144  LOAD_METHOD              find
              146  LOAD_STR                 'name'
              148  CALL_METHOD_1         1  ''
              150  LOAD_CONST               6
              152  BINARY_ADD       
              154  LOAD_CONST               -1
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  STORE_FAST               'itname'

 L.  48       162  LOAD_FAST                'itname'
              164  LOAD_METHOD              find
              166  LOAD_STR                 ','
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'indx'

 L.  49       172  LOAD_FAST                'indx'
              174  LOAD_CONST               0
              176  COMPARE_OP               >=
              178  POP_JUMP_IF_FALSE   196  'to 196'

 L.  50       180  LOAD_FAST                'itname'
              182  LOAD_CONST               0
              184  LOAD_FAST                'indx'
              186  LOAD_CONST               1
              188  BINARY_SUBTRACT  
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  STORE_FAST               'itname'
            196_0  COME_FROM           178  '178'

 L.  51       196  LOAD_FAST                'itname'
              198  LOAD_FAST                'name'
              200  COMPARE_OP               !=
              202  POP_JUMP_IF_FALSE   206  'to 206'

 L.  52       204  JUMP_BACK           116  'to 116'
            206_0  COME_FROM           202  '202'

 L.  54       206  LOAD_FAST                'stri'
              208  LOAD_FAST                'stri'
              210  LOAD_METHOD              find
              212  LOAD_STR                 'pid'
              214  CALL_METHOD_1         1  ''
              216  LOAD_CONST               4
              218  BINARY_ADD       
              220  LOAD_FAST                'stri'
              222  LOAD_METHOD              find
              224  LOAD_STR                 'name'
              226  CALL_METHOD_1         1  ''
              228  LOAD_CONST               2
              230  BINARY_SUBTRACT  
              232  BUILD_SLICE_2         2 
              234  BINARY_SUBSCR    
              236  STORE_FAST               'pid'

 L.  55       238  LOAD_FAST                'retid'
              240  LOAD_METHOD              append
              242  LOAD_GLOBAL              int
              244  LOAD_FAST                'pid'
              246  CALL_FUNCTION_1       1  ''
              248  CALL_METHOD_1         1  ''
              250  POP_TOP          
              252  JUMP_BACK           116  'to 116'
            254_0  COME_FROM            90  '90'

 L.  56       254  LOAD_FAST                'retid'
              256  POP_BLOCK        
              258  RETURN_VALUE     
            260_0  COME_FROM_FINALLY     0  '0'

 L.  57       260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          

 L.  58       266  BUILD_LIST_0          0 
              268  ROT_FOUR         
              270  POP_EXCEPT       
              272  RETURN_VALUE     
              274  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 50


def killProcess--- This code section failed: ---

 L.  62         0  SETUP_FINALLY       132  'to 132'

 L.  63         2  LOAD_GLOBAL              isLinux
                4  CALL_FUNCTION_0       0  ''
                6  POP_JUMP_IF_FALSE    68  'to 68'

 L.  64         8  LOAD_GLOBAL              os
               10  LOAD_METHOD              popen
               12  LOAD_STR                 'kill -9 '
               14  LOAD_GLOBAL              str
               16  LOAD_FAST                'proid'
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_ADD       
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L.  65        26  LOAD_GLOBAL              os
               28  LOAD_METHOD              popen
               30  LOAD_STR                 'ps '
               32  LOAD_GLOBAL              str
               34  LOAD_FAST                'proid'
               36  CALL_FUNCTION_1       1  ''
               38  BINARY_ADD       
               40  CALL_METHOD_1         1  ''
               42  LOAD_METHOD              readlines
               44  CALL_METHOD_0         0  ''
               46  STORE_FAST               'lines'

 L.  66        48  LOAD_GLOBAL              len
               50  LOAD_FAST                'lines'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_CONST               1
               56  COMPARE_OP               <=
               58  POP_JUMP_IF_FALSE   126  'to 126'

 L.  67        60  POP_BLOCK        
               62  LOAD_CONST               True
               64  RETURN_VALUE     
               66  JUMP_FORWARD        126  'to 126'
             68_0  COME_FROM             6  '6'

 L.  69        68  LOAD_GLOBAL              os
               70  LOAD_METHOD              popen
               72  LOAD_STR                 'tasklist | findstr '
               74  LOAD_GLOBAL              str
               76  LOAD_FAST                'proid'
               78  CALL_FUNCTION_1       1  ''
               80  BINARY_ADD       
               82  CALL_METHOD_1         1  ''
               84  LOAD_METHOD              readlines
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'lines'

 L.  70        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'lines'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_CONST               0
               98  COMPARE_OP               <=
              100  POP_JUMP_IF_FALSE   108  'to 108'

 L.  71       102  POP_BLOCK        
              104  LOAD_CONST               True
              106  RETURN_VALUE     
            108_0  COME_FROM           100  '100'

 L.  72       108  LOAD_GLOBAL              os
              110  LOAD_METHOD              popen
              112  LOAD_STR                 'taskkill /pid %s /f'
              114  LOAD_GLOBAL              str
              116  LOAD_FAST                'proid'
              118  CALL_FUNCTION_1       1  ''
              120  BINARY_MODULO    
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'unread2'
            126_0  COME_FROM            66  '66'
            126_1  COME_FROM            58  '58'

 L.  73       126  POP_BLOCK        
              128  LOAD_CONST               False
              130  RETURN_VALUE     
            132_0  COME_FROM_FINALLY     0  '0'

 L.  74       132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L.  75       138  POP_EXCEPT       
              140  LOAD_CONST               False
              142  RETURN_VALUE     
              144  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 62


def openPort(port):
    cmds = [
     'iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport ' + str(port) + ' -j ACCEPT',
     'iptables -I INPUT -m state --state NEW -m udp -p udp --dport ' + str(port) + ' -j ACCEPT',
     'ip6tables -I INPUT -m state --state NEW -m tcp -p tcp --dport ' + str(port) + ' -j ACCEPT',
     'ip6tables -I INPUT -m state --state NEW -m udp -p udp --dport ' + str(port) + ' -j ACCEPT']
    for item in cmds:
        subprocess.call(item, shell=False)