# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\versionHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 3369 bytes
import os, platform
import aigpy.configHelper as ConfigHelper

def getVersion--- This code section failed: ---

 L.  10         0  SETUP_FINALLY       166  'to 166'

 L.  11         2  LOAD_GLOBAL              os
                4  LOAD_ATTR                path
                6  LOAD_METHOD              isfile
                8  LOAD_FAST                'in_filepath'
               10  CALL_METHOD_1         1  ''
               12  LOAD_CONST               False
               14  COMPARE_OP               is
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L.  12        18  POP_BLOCK        
               20  LOAD_STR                 ''
               22  RETURN_VALUE     
             24_0  COME_FROM            16  '16'

 L.  13        24  LOAD_GLOBAL              os
               26  LOAD_ATTR                path
               28  LOAD_METHOD              exists
               30  LOAD_FAST                'in_filepath'
               32  CALL_METHOD_1         1  ''
               34  LOAD_CONST               False
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L.  14        40  POP_BLOCK        
               42  LOAD_STR                 ''
               44  RETURN_VALUE     
             46_0  COME_FROM            38  '38'

 L.  17        46  LOAD_GLOBAL              platform
               48  LOAD_METHOD              system
               50  CALL_METHOD_0         0  ''
               52  STORE_FAST               'sysName'

 L.  18        54  LOAD_FAST                'sysName'
               56  LOAD_STR                 'Windows'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   146  'to 146'

 L.  19        62  LOAD_CONST               0
               64  LOAD_CONST               None
               66  IMPORT_NAME              win32api
               68  STORE_FAST               'win32api'

 L.  20        70  LOAD_FAST                'win32api'
               72  LOAD_METHOD              GetFileVersionInfo
               74  LOAD_FAST                'in_filepath'
               76  LOAD_GLOBAL              os
               78  LOAD_ATTR                sep
               80  CALL_METHOD_2         2  ''
               82  STORE_FAST               'info'

 L.  21        84  LOAD_FAST                'info'
               86  LOAD_STR                 'FileVersionMS'
               88  BINARY_SUBSCR    
               90  STORE_FAST               'ms'

 L.  22        92  LOAD_FAST                'info'
               94  LOAD_STR                 'FileVersionLS'
               96  BINARY_SUBSCR    
               98  STORE_FAST               'ls'

 L.  23       100  LOAD_STR                 '%d.%d.%d.%04d'
              102  LOAD_FAST                'win32api'
              104  LOAD_METHOD              HIWORD
              106  LOAD_FAST                'ms'
              108  CALL_METHOD_1         1  ''
              110  LOAD_FAST                'win32api'
              112  LOAD_METHOD              LOWORD
              114  LOAD_FAST                'ms'
              116  CALL_METHOD_1         1  ''

 L.  24       118  LOAD_FAST                'win32api'
              120  LOAD_METHOD              HIWORD
              122  LOAD_FAST                'ls'
              124  CALL_METHOD_1         1  ''

 L.  24       126  LOAD_FAST                'win32api'
              128  LOAD_METHOD              LOWORD
              130  LOAD_FAST                'ls'
              132  CALL_METHOD_1         1  ''

 L.  23       134  BUILD_TUPLE_4         4 
              136  BINARY_MODULO    
              138  STORE_FAST               'version'

 L.  25       140  LOAD_FAST                'version'
              142  POP_BLOCK        
              144  RETURN_VALUE     
            146_0  COME_FROM            60  '60'

 L.  26       146  LOAD_FAST                'sysName'
              148  LOAD_STR                 'Linux'
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   160  'to 160'

 L.  27       154  POP_BLOCK        
              156  LOAD_STR                 ''
              158  RETURN_VALUE     
            160_0  COME_FROM           152  '152'

 L.  28       160  POP_BLOCK        
              162  LOAD_STR                 ''
              164  RETURN_VALUE     
            166_0  COME_FROM_FINALLY     0  '0'

 L.  29       166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L.  30       172  POP_EXCEPT       
              174  LOAD_STR                 ''
              176  RETURN_VALUE     
              178  END_FINALLY      

Parse error at or near `LOAD_STR' instruction at offset 20


def cmpVersion(ver1, ver2):
    vlist1 = ver1.split'.'
    vlist2 = ver2.split'.'
    iIndex = 0
    for obj in vlist1:
        if len(vlist2) <= iIndex:
            break
        if obj > vlist2[iIndex]:
            return 1
            if obj < vlist2[iIndex]:
                return -1
            iIndex = iIndex + 1
    else:
        return 0


class VersionFile(object):

    def __init__(self, path=None):
        self.version = None
        self.mainFile = None
        self.elseFileList = []
        self.isZip = 0
        self.zipFile = ''
        if path != None:
            self.readFilepath

    def saveFile(self, path):
        if path is None or self.version is None or self.mainFile is None:
            return False
        if self.isZip != 0:
            if self.zipFile == '':
                return False
        check = ConfigHelper.SetValue('common', 'version', self.version, path)
        check = ConfigHelper.SetValue('common', 'mainfile', self.mainFile, path)
        if check is False:
            return False
        check = ConfigHelper.SetValue('common', 'iszip', self.isZip, path)
        check = ConfigHelper.SetValue('common', 'zipfile', self.isZip, path)
        if self.elseFileList is None or len(self.elseFileList) == 0:
            return True
        ConfigHelper.SetValue('common', 'elsenum', len(self.elseFileList), path)
        index = 0
        for item in self.elseFileList:
            ConfigHelper.SetValue('common', 'else' + index, item, path)
            index = index + 1
        else:
            return True

    def readFile(self, path):
        if path is None:
            return False
        ver = ConfigHelper.GetValue('common', 'version', '', path)
        mainFile = ConfigHelper.GetValue('common', 'mainfile', '', path)
        if ver == '' or mainFile == '':
            return False
        isZip = ConfigHelper.GetValue('common', 'iszip', 0, path)
        isZip = int(isZip)
        zipFile = ConfigHelper.GetValue('common', 'zipfile', '', path)
        if isZip != 0 or zipFile == '':
            return False
        elseNum = ConfigHelper.GetValue('common', 'elsenum', 0, path)
        elseNum = int(elseNum)
        elseList = []
        index = 0
        if elseNum > 0:
            obj = ConfigHelper.GetValue('common', 'else' + index, '', path)
            index = index + 1
            elseList.appendobj
        self.version = ver
        self.mainFile = mainFile
        self.elseFileList = elseList
        self.isZip = isZip
        self.zipFile = zipFile
        return True