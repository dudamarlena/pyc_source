# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\systemHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 2601 bytes
"""
@File    :   systemHelper.py
@Time    :   2018/12/20
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""
import os, platform, subprocess

def getOwnPath(in__file__):
    return os.path.dirname(os.path.realpath(in__file__))


def isWindows():
    sysName = platform.system()
    return sysName == 'Windows'


def isLinux():
    sysName = platform.system()
    return sysName == 'Linux'


def getProcessID(name):
    """get processid by name"""
    try:
        retid = []
        if isLinux():
            lines = os.popen('ps aux | grep "' + name + '" | grep -v grep').readlines()
            if len(lines) <= 0:
                return []
            for item in lines:
                array = item.split()
                retid.append(int(array[1]))

        else:
            import psutil
        pidList = list(psutil.process_iter())
        for item in pidList:
            stri = str(item)
            stri = stri[15:-1]
            itname = stri[stri.find('name') + 6:-1]
            indx = itname.find(',')
            if indx >= 0:
                itname = itname[0:indx - 1]
            if itname != name:
                pass
            else:
                pid = stri[stri.find('pid') + 4:stri.find('name') - 2]
                retid.append(int(pid))

        return retid
    except:
        return []


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