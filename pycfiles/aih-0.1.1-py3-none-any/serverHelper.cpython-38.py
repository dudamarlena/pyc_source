# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\serverHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 3051 bytes
__doc__ = '\n@File    :   serverHelper.py\n@Time    :   2019/04/10\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import socket
from aigpy.threadHelper import ThreadTool
from aigpy.threadHelper import ThreadPoolManger
from aigpy.httpHelper import HttpRequest

class ServerTool(object):

    def __init__(self, rootDir, cookieDir, fileOf404=None, scfamily=socket.AF_INET, sctype=socket.SOCK_STREAM):
        """
        #Func    :   初始化     
        #Param   :   rootDir    [in] 根目录     
        #Param   :   cookieDir  [in] cookie目录     
        #Param   :   fileOf404  [in] 404文件        
        #Param   :   scfamily   [in] 网络family     
        #Param   :   sctype     [in] 网络类型       
        """
        rootDir.replace('\\', '/')
        cookieDir.replace('\\', '/')
        self._ServerTool__sockHandle = None
        self._ServerTool__sockFamily = scfamily
        self._ServerTool__sockType = sctype
        self._ServerTool__rootDir = rootDir + '/'
        self._ServerTool__cookieDir = cookieDir + '/'
        self._ServerTool__fileOf404 = fileOf404
        self._ServerTool__requestFunc = None
        self._ServerTool__listenThread = ThreadTool(1)
        self._ServerTool__requestThread = ThreadPoolManger(5)
        self._ServerTool__revieveLen = 1024

    def __requestThreadCall__(self, sock, addr):
        body = None
        request = sock.recv(self._ServerTool__revieveLen)
        http_req = HttpRequest(self._ServerTool__rootDir, self._ServerTool__cookieDir, self._ServerTool__fileOf404)
        http_req.passRequest(request)
        if self._ServerTool__requestFunc is not None:
            body = self._ServerTool__requestFunc(http_req)
        sock.send(http_req.getResponse(body).encode('utf-8'))
        sock.close()

    def __listenThreadCall__(self):
        while True:
            sock, addr = self._ServerTool__sockHandle.accept()
            (self._ServerTool__requestThread.addWork)(self.__requestThreadCall__, *(sock, addr))

        self.start()

    def start--- This code section failed: ---

 L.  69         0  SETUP_FINALLY        92  'to 92'

 L.  70         2  LOAD_FAST                'self'
                4  LOAD_METHOD              stop
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L.  71        10  LOAD_FAST                'recieveLen'
               12  LOAD_FAST                'self'
               14  STORE_ATTR               _ServerTool__revieveLen

 L.  72        16  LOAD_FAST                'requestFuc'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               _ServerTool__requestFunc

 L.  73        22  LOAD_GLOBAL              socket
               24  LOAD_METHOD              socket
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _ServerTool__sockFamily
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _ServerTool__sockType
               34  CALL_METHOD_2         2  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               _ServerTool__sockHandle

 L.  74        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _ServerTool__sockHandle
               44  LOAD_METHOD              bind
               46  LOAD_FAST                'address'
               48  LOAD_GLOBAL              int
               50  LOAD_FAST                'port'
               52  CALL_FUNCTION_1       1  ''
               54  BUILD_TUPLE_2         2 
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.  75        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _ServerTool__sockHandle
               64  LOAD_METHOD              listen
               66  LOAD_FAST                'listenNum'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L.  76        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _ServerTool__listenThread
               76  LOAD_METHOD              start
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                __listenThreadCall__
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L.  77        86  POP_BLOCK        
               88  LOAD_CONST               True
               90  RETURN_VALUE     
             92_0  COME_FROM_FINALLY     0  '0'

 L.  78        92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L.  79        98  POP_EXCEPT       
              100  LOAD_CONST               False
              102  RETURN_VALUE     
              104  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 90

    def stop(self):
        if self._ServerTool__sockHandle is None:
            return
        self._ServerTool__listenThread.close()
        self._ServerTool__requestThread.close()
        self._ServerTool__sockHandle.close()