# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\serverHelper.py
# Compiled at: 2019-08-30 12:41:18
# Size of source mod 2**32: 3141 bytes
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

    def start(self, address, port, requestFuc=None, listenNum=10, recieveLen=1024):
        """
        #Func    :   启动
        #Param   :   address    [in] ip地址 
        #Param   :   port       [in] 端口号
        #Param   :   requestFuc [in] 响应函数,参数为httpRequest,返回body     
        #Param   :   listenNum  [in] 监听的数量
        #Param   :   recieveLen [in] 数据包的长度
        #Return  :   True/False   
        """
        try:
            self.stop()
            self._ServerTool__revieveLen = recieveLen
            self._ServerTool__requestFunc = requestFuc
            self._ServerTool__sockHandle = socket.socket(self._ServerTool__sockFamily, self._ServerTool__sockType)
            self._ServerTool__sockHandle.bind((address, int(port)))
            self._ServerTool__sockHandle.listen(listenNum)
            self._ServerTool__listenThread.start(self.__listenThreadCall__)
            return True
        except:
            return False

    def stop(self):
        if self._ServerTool__sockHandle is None:
            return
        self._ServerTool__listenThread.close()
        self._ServerTool__requestThread.close()
        self._ServerTool__sockHandle.close()