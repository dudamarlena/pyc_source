# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\pathHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 3509 bytes
__doc__ = '\n@File    :   pathHelper.py\n@Time    :   2018/12/17\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import os, shutil

def getDiffTmpPathName(basePath):
    """Get tmp file name like 'Tmp1'"""
    count = 0
    basePath = basePath.replace('\\', '/')
    basePath = basePath.strip()
    basePath = basePath.rstrip('/')
    path = basePath + '/Tmp' + str(count)
    while os.path.exists(path):
        count = count + 1
        path = basePath + '/Tmp' + str(count)

    return path


def mkdirs(path):
    path = path.replace('\\', '/')
    path = path.strip()
    path = path.rstrip('/')
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False


def remove--- This code section failed: ---

 L.  40         0  SETUP_FINALLY        82  'to 82'

 L.  41         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              exists
                8  LOAD_FAST                'path'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               False
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L.  42        18  POP_BLOCK        
               20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L.  43        24  LOAD_GLOBAL              os
               26  LOAD_ATTR                path
               28  LOAD_METHOD              isfile
               30  LOAD_FAST                'path'
               32  CALL_METHOD_1         1  ''
               34  LOAD_CONST               True
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    50  'to 50'

 L.  44        40  LOAD_GLOBAL              os
               42  LOAD_METHOD              remove
               44  LOAD_FAST                'path'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
             50_0  COME_FROM            38  '38'

 L.  45        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              isdir
               56  LOAD_FAST                'path'
               58  CALL_METHOD_1         1  ''
               60  LOAD_CONST               True
               62  COMPARE_OP               is
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L.  46        66  LOAD_GLOBAL              shutil
               68  LOAD_METHOD              rmtree
               70  LOAD_FAST                'path'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
             76_0  COME_FROM            64  '64'

 L.  47        76  POP_BLOCK        
               78  LOAD_CONST               True
               80  RETURN_VALUE     
             82_0  COME_FROM_FINALLY     0  '0'

 L.  48        82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L.  49        88  POP_EXCEPT       
               90  LOAD_CONST               False
               92  RETURN_VALUE     
               94  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 20


def copyFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        return False
    fpath, fname = os.path.split(dstfile)
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    shutil.copyfile(srcfile, dstfile)
    return True


def replaceLimitChar(path, newChar):
    if path is None:
        return ''
    if newChar is None:
        newChar = ''
    path = path.replace(':', newChar)
    path = path.replace('/', newChar)
    path = path.replace('?', newChar)
    path = path.replace('<', newChar)
    path = path.replace('>', newChar)
    path = path.replace('|', newChar)
    path = path.replace('\\', newChar)
    path = path.replace('*', newChar)
    path = path.replace('"', newChar)
    return path


def getDirName(filepath):
    """e:/test/file.txt --> e:/test/"""
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index == -1:
        return './'
    return filepath[0:index + 1]


def getFileName(filepath):
    """e:/test/file.txt --> file.txt"""
    filepath = filepath.replace('\\', '/')
    index = filepath.rfind('/')
    if index == -1:
        return filepath
    return filepath[index + 1:len(filepath)]


def getFileNameWithoutExtension(filepath):
    """e:/test/file.txt --> file"""
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return filepath
    return filepath[0:index]


def getFileExtension(filepath):
    """e:/test/file.txt --> .txt"""
    filepath = getFileName(filepath)
    index = filepath.rfind('.')
    if index == -1:
        return
    return filepath[index:len(filepath)]


def getDirSize--- This code section failed: ---

 L. 113         0  SETUP_FINALLY        82  'to 82'

 L. 114         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              isdir
                8  LOAD_FAST                'path'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               False
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L. 115        18  POP_BLOCK        
               20  LOAD_CONST               0
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L. 116        24  LOAD_CONST               0
               26  STORE_FAST               'size'

 L. 117        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              walk
               32  LOAD_FAST                'path'
               34  CALL_METHOD_1         1  ''
               36  GET_ITER         
               38  FOR_ITER             76  'to 76'
               40  UNPACK_SEQUENCE_3     3 
               42  STORE_DEREF              'root'
               44  STORE_FAST               'dirs'
               46  STORE_FAST               'files'

 L. 118        48  LOAD_FAST                'size'
               50  LOAD_GLOBAL              sum
               52  LOAD_CLOSURE             'root'
               54  BUILD_TUPLE_1         1 
               56  LOAD_LISTCOMP            '<code_object <listcomp>>'
               58  LOAD_STR                 'getDirSize.<locals>.<listcomp>'
               60  MAKE_FUNCTION_8          'closure'
               62  LOAD_FAST                'files'
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  INPLACE_ADD      
               72  STORE_FAST               'size'
               74  JUMP_BACK            38  'to 38'

 L. 119        76  LOAD_FAST                'size'
               78  POP_BLOCK        
               80  RETURN_VALUE     
             82_0  COME_FROM_FINALLY     0  '0'

 L. 120        82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L. 121        88  POP_EXCEPT       
               90  LOAD_CONST               0
               92  RETURN_VALUE     
               94  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 20


def getDirFiles--- This code section failed: ---

 L. 124         0  SETUP_FINALLY        96  'to 96'

 L. 125         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              isdir
                8  LOAD_FAST                'path'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               False
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L. 126        18  BUILD_LIST_0          0 
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L. 127        24  BUILD_LIST_0          0 
               26  STORE_FAST               'ret'

 L. 128        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              walk
               32  LOAD_FAST                'path'
               34  CALL_METHOD_1         1  ''
               36  GET_ITER         
               38  FOR_ITER             90  'to 90'
               40  UNPACK_SEQUENCE_3     3 
               42  STORE_FAST               'root'
               44  STORE_FAST               'dirs'
               46  STORE_FAST               'files'

 L. 129        48  LOAD_FAST                'root'
               50  LOAD_METHOD              replace
               52  LOAD_STR                 '\\'
               54  LOAD_STR                 '/'
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'root'

 L. 130        60  LOAD_FAST                'files'
               62  GET_ITER         
               64  FOR_ITER             88  'to 88'
               66  STORE_FAST               'item'

 L. 131        68  LOAD_FAST                'ret'
               70  LOAD_METHOD              append
               72  LOAD_FAST                'root'
               74  LOAD_STR                 '/'
               76  BINARY_ADD       
               78  LOAD_FAST                'item'
               80  BINARY_ADD       
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          
               86  JUMP_BACK            64  'to 64'
               88  JUMP_BACK            38  'to 38'

 L. 132        90  LOAD_FAST                'ret'
               92  POP_BLOCK        
               94  RETURN_VALUE     
             96_0  COME_FROM_FINALLY     0  '0'

 L. 133        96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 134       102  BUILD_LIST_0          0 
              104  ROT_FOUR         
              106  POP_EXCEPT       
              108  RETURN_VALUE     
              110  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 20