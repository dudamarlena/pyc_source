# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\netHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 3572 bytes
"""
@File    :   netHelper.py
@Time    :   2018/12/17
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""
import re, os, sys, json, socket, requests
from aigpy.progressHelper import ProgressTool
from aigpy.convertHelper import convertStorageUnit
from aigpy.pathHelper import getFileName

def downloadString--- This code section failed: ---

 L.  24         0  SETUP_FINALLY        22  'to 22'

 L.  25         2  LOAD_GLOBAL              requests
                4  LOAD_METHOD              get
                6  LOAD_FAST                'url'
                8  LOAD_FAST                'timeouts'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               're'

 L.  26        14  LOAD_FAST                're'
               16  LOAD_ATTR                content
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     0  '0'

 L.  27        22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  28        28  POP_EXCEPT       
               30  LOAD_CONST               None
               32  RETURN_VALUE     
               34  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 28


def downloadJson--- This code section failed: ---

 L.  32         0  SETUP_FINALLY        32  'to 32'

 L.  33         2  LOAD_GLOBAL              requests
                4  LOAD_METHOD              get
                6  LOAD_FAST                'url'
                8  LOAD_FAST                'timeouts'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               're'

 L.  34        14  LOAD_GLOBAL              json
               16  LOAD_METHOD              loads
               18  LOAD_FAST                're'
               20  LOAD_ATTR                content
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'info'

 L.  35        26  LOAD_FAST                'info'
               28  POP_BLOCK        
               30  RETURN_VALUE     
             32_0  COME_FROM_FINALLY     0  '0'

 L.  36        32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  37        38  POP_EXCEPT       
               40  LOAD_CONST               None
               42  RETURN_VALUE     
               44  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 38


def getFileSize--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                version_info
                4  LOAD_CONST               (3, 0)
                6  COMPARE_OP               >
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  41        10  LOAD_CONST               0
               12  LOAD_CONST               ('urlopen',)
               14  IMPORT_NAME_ATTR         urllib.request
               16  IMPORT_FROM              urlopen
               18  STORE_FAST               'urlopen'
               20  POP_TOP          
               22  JUMP_FORWARD         36  'to 36'
             24_0  COME_FROM             8  '8'

 L.  43        24  LOAD_CONST               0
               26  LOAD_CONST               ('urlopen',)
               28  IMPORT_NAME              urllib2
               30  IMPORT_FROM              urlopen
               32  STORE_FAST               'urlopen'
               34  POP_TOP          
             36_0  COME_FROM            22  '22'

 L.  45        36  SETUP_FINALLY        80  'to 80'

 L.  46        38  LOAD_FAST                'urlopen'
               40  LOAD_FAST                'url'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'response'

 L.  47        46  LOAD_FAST                'response'
               48  LOAD_METHOD              info
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'info'

 L.  48        54  LOAD_GLOBAL              dict
               56  LOAD_FAST                'info'
               58  CALL_FUNCTION_1       1  ''
               60  STORE_FAST               'dic'

 L.  49        62  LOAD_FAST                'dic'
               64  LOAD_STR                 'Content-Length'
               66  BINARY_SUBSCR    
               68  STORE_FAST               'length'

 L.  50        70  LOAD_GLOBAL              int
               72  LOAD_FAST                'length'
               74  CALL_FUNCTION_1       1  ''
               76  POP_BLOCK        
               78  RETURN_VALUE     
             80_0  COME_FROM_FINALLY    36  '36'

 L.  51        80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L.  52        86  POP_EXCEPT       
               88  LOAD_CONST               -1
               90  RETURN_VALUE     
               92  END_FINALLY      

Parse error at or near `POP_EXCEPT' instruction at offset 86


def downloadFileByUrls(urlArray, fileName, stimeout=None, showprogress=False):
    if os.accessfileName0:
        os.removefileName
    progress = None
    if showprogress:
        desc = getFileName(fileName)
        progress = ProgressTool((len(urlArray)), 10, unit='', desc=desc)
    curcount = 1
    for item in urlArray:
        ret = downloadFile(item, fileName, stimeout, False, append=True)
        if ret != True:
            return False
        if progress:
            progress.setCurCountcurcount
            curcount += 1
        return True


def downloadFile--- This code section failed: ---

 L.  76         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                version_info
                4  LOAD_CONST               (3, 0)
                6  COMPARE_OP               >
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  77        10  LOAD_CONST               0
               12  LOAD_CONST               ('urlopen',)
               14  IMPORT_NAME_ATTR         urllib.request
               16  IMPORT_FROM              urlopen
               18  STORE_FAST               'urlopen'
               20  POP_TOP          
               22  JUMP_FORWARD         36  'to 36'
             24_0  COME_FROM             8  '8'

 L.  79        24  LOAD_CONST               0
               26  LOAD_CONST               ('urlopen',)
               28  IMPORT_NAME              urllib2
               30  IMPORT_FROM              urlopen
               32  STORE_FAST               'urlopen'
               34  POP_TOP          
             36_0  COME_FROM            22  '22'

 L.  81        36  SETUP_FINALLY       256  'to 256'

 L.  82        38  LOAD_FAST                'stimeout'
               40  LOAD_CONST               None
               42  COMPARE_OP               is
               44  POP_JUMP_IF_FALSE    56  'to 56'

 L.  83        46  LOAD_FAST                'urlopen'
               48  LOAD_FAST                'url'
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'response'
               54  JUMP_FORWARD         68  'to 68'
             56_0  COME_FROM            44  '44'

 L.  85        56  LOAD_FAST                'urlopen'
               58  LOAD_FAST                'url'
               60  LOAD_FAST                'stimeout'
               62  LOAD_CONST               ('timeout',)
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  STORE_FAST               'response'
             68_0  COME_FROM            54  '54'

 L.  87        68  LOAD_STR                 'mb'
               70  STORE_FAST               'unit'

 L.  88        72  LOAD_GLOBAL              convertStorageUnit
               74  LOAD_FAST                'response'
               76  LOAD_ATTR                length
               78  LOAD_STR                 'byte'
               80  LOAD_FAST                'unit'
               82  CALL_FUNCTION_3       3  ''
               84  LOAD_CONST               1
               86  COMPARE_OP               <
               88  POP_JUMP_IF_FALSE    94  'to 94'

 L.  89        90  LOAD_STR                 'kb'
               92  STORE_FAST               'unit'
             94_0  COME_FROM            88  '88'

 L.  90        94  LOAD_CONST               None
               96  STORE_FAST               'progress'

 L.  91        98  LOAD_FAST                'showprogress'
              100  POP_JUMP_IF_FALSE   136  'to 136'

 L.  92       102  LOAD_GLOBAL              getFileName
              104  LOAD_FAST                'fileName'
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'desc'

 L.  93       110  LOAD_GLOBAL              ProgressTool
              112  LOAD_GLOBAL              convertStorageUnit
              114  LOAD_FAST                'response'
              116  LOAD_ATTR                length
              118  LOAD_STR                 'byte'
              120  LOAD_FAST                'unit'
              122  CALL_FUNCTION_3       3  ''
              124  LOAD_CONST               10
              126  LOAD_FAST                'unit'
              128  LOAD_FAST                'desc'
              130  LOAD_CONST               ('unit', 'desc')
              132  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              134  STORE_FAST               'progress'
            136_0  COME_FROM           100  '100'

 L.  95       136  LOAD_STR                 'wb'
              138  STORE_FAST               'mode'

 L.  96       140  LOAD_FAST                'append'
              142  POP_JUMP_IF_FALSE   148  'to 148'

 L.  97       144  LOAD_STR                 'ab'
              146  STORE_FAST               'mode'
            148_0  COME_FROM           142  '142'

 L.  99       148  LOAD_CONST               0
              150  STORE_FAST               'curcount'

 L. 100       152  LOAD_CONST               16384
              154  STORE_FAST               'chunksize'

 L. 101       156  LOAD_GLOBAL              open
              158  LOAD_FAST                'fileName'
              160  LOAD_FAST                'mode'
              162  CALL_FUNCTION_2       2  ''
              164  SETUP_WITH          246  'to 246'
              166  STORE_FAST               'f'

 L. 103       168  LOAD_FAST                'response'
              170  LOAD_METHOD              read
              172  LOAD_FAST                'chunksize'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'chunk'

 L. 104       178  LOAD_FAST                'curcount'
              180  LOAD_GLOBAL              len
              182  LOAD_FAST                'chunk'
              184  CALL_FUNCTION_1       1  ''
              186  INPLACE_ADD      
              188  STORE_FAST               'curcount'

 L. 105       190  LOAD_FAST                'progress'
              192  POP_JUMP_IF_FALSE   212  'to 212'

 L. 106       194  LOAD_FAST                'progress'
              196  LOAD_METHOD              setCurCount
              198  LOAD_GLOBAL              convertStorageUnit
              200  LOAD_FAST                'curcount'
              202  LOAD_STR                 'byte'
              204  LOAD_FAST                'unit'
              206  CALL_FUNCTION_3       3  ''
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
            212_0  COME_FROM           192  '192'

 L. 107       212  LOAD_FAST                'chunk'
              214  POP_JUMP_IF_TRUE    218  'to 218'

 L. 108       216  BREAK_LOOP          230  'to 230'
            218_0  COME_FROM           214  '214'

 L. 109       218  LOAD_FAST                'f'
              220  LOAD_METHOD              write
              222  LOAD_FAST                'chunk'
              224  CALL_METHOD_1         1  ''
              226  POP_TOP          
              228  JUMP_BACK           168  'to 168'

 L. 110       230  POP_BLOCK        
              232  BEGIN_FINALLY    
              234  WITH_CLEANUP_START
              236  WITH_CLEANUP_FINISH
              238  POP_FINALLY           0  ''
              240  POP_BLOCK        
              242  LOAD_CONST               True
              244  RETURN_VALUE     
            246_0  COME_FROM_WITH      164  '164'
              246  WITH_CLEANUP_START
              248  WITH_CLEANUP_FINISH
              250  END_FINALLY      
              252  POP_BLOCK        
              254  JUMP_FORWARD        270  'to 270'
            256_0  COME_FROM_FINALLY    36  '36'

 L. 111       256  POP_TOP          
              258  POP_TOP          
              260  POP_TOP          

 L. 112       262  POP_EXCEPT       
              264  LOAD_CONST               False
              266  RETURN_VALUE     
              268  END_FINALLY      
            270_0  COME_FROM           254  '254'

Parse error at or near `WITH_CLEANUP_START' instruction at offset 234


def getIpStatus(host, port, timeouts=1):
    socket.setdefaulttimeouttimeouts
    flag = True
    try:
        s = socket.socketsocket.AF_INETsocket.SOCK_STREAM
        s.connect(host, port)
        s.close
    except:
        flag = False
    else:
        return flag


def getIP():
    text = requests.get'http://txt.go.sohu.com/ip/soip'.text
    ip = re.findall'\\d+.\\d+.\\d+.\\d+'text[0]
    return ip


def getResult(code=0, msg='', data=''):
    ret = {}
    ret['code'] = code
    ret['errmsg'] = msg
    ret['data'] = data
    return json.dumpsret