# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\pipHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 1093 bytes
__doc__ = '\n@File    :   pipHelper.py\n@Time    :   2019/03/11\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   pip server tool\n'
import aigpy.netHelper as netHelper

def getInfo(projectName):
    """Get project information from pypi
    - Return: json or None                              
    """
    url = 'https://pypi.org/pypi/' + projectName + '/json'
    ret = netHelper.downloadJson(url, None)
    return ret


def getLastVersion--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        38  'to 38'

 L.  27         2  LOAD_GLOBAL              getInfo
                4  LOAD_FAST                'projectName'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'ret'

 L.  28        10  LOAD_FAST                'ret'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L.  29        18  POP_BLOCK        
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L.  30        24  LOAD_FAST                'ret'
               26  LOAD_STR                 'info'
               28  BINARY_SUBSCR    
               30  LOAD_STR                 'version'
               32  BINARY_SUBSCR    
               34  POP_BLOCK        
               36  RETURN_VALUE     
             38_0  COME_FROM_FINALLY     0  '0'

 L.  31        38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  32        44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  RETURN_VALUE     
               50  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 20


def getVersionList--- This code section failed: ---

 L.  38         0  SETUP_FINALLY        34  'to 34'

 L.  39         2  LOAD_GLOBAL              getInfo
                4  LOAD_FAST                'projectName'
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'ret'

 L.  40        10  LOAD_FAST                'ret'
               12  LOAD_CONST               None
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L.  41        18  POP_BLOCK        
               20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L.  42        24  LOAD_FAST                'ret'
               26  LOAD_STR                 'releases'
               28  BINARY_SUBSCR    
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY     0  '0'

 L.  43        34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  44        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
               46  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 20