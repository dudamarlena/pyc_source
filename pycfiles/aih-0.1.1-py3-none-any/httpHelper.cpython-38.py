# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\httpHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 8110 bytes
__doc__ = '\n@File    :   httpHelper.py\n@Time    :   2019/04/10\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'
import os, xml.dom.minidom
CONTENT_404 = '\n<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n    <style type="text/css">\n        div{\n            width: 100%;\n            text-align:center;\n        }\n    </style>\n</head>\n<body>\n    <div>\n        <h1>404 Not Found</h1>\n    </div>\n</body>\n<html>\n'

class ErrorCode(object):
    OK = 'HTTP/1.1 200 OK\r\n'
    NOT_FOUND = 'HTTP/1.1 404 Not Found\r\n'


def dict2str(d):
    s = ''
    for i in d:
        s = s + i + ': ' + d[i] + '\r\n'

    return s


class Session(object):

    def __init__(self):
        self.data = dict()
        self.cook_file = None

    def getCookie(self, key):
        if key in self.data.keys():
            return self.data[key]

    def setCookie(self, key, value):
        self.data[key] = value

    def loadFromXML(self):
        import xml.dom.minidom as minidom
        root = minidom.parse(self.cook_file).documentElement
        for node in root.childNodes:
            if node.nodeName == '#text':
                continue
            else:
                self.setCookie(node.nodeName, node.childNodes[0].nodeValue)

    def write2XML--- This code section failed: ---

 L.  73         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         xml.dom.minidom
                6  IMPORT_FROM              dom
                8  ROT_TWO          
               10  POP_TOP          
               12  IMPORT_FROM              minidom
               14  STORE_FAST               'minidom'
               16  POP_TOP          

 L.  74        18  LOAD_GLOBAL              xml
               20  LOAD_ATTR                dom
               22  LOAD_ATTR                minidom
               24  LOAD_METHOD              getDOMImplementation
               26  CALL_METHOD_0         0  ''
               28  LOAD_METHOD              createDocument
               30  LOAD_CONST               None
               32  LOAD_STR                 'Root'
               34  LOAD_CONST               None
               36  CALL_METHOD_3         3  ''
               38  STORE_FAST               'dom'

 L.  75        40  LOAD_FAST                'dom'
               42  LOAD_ATTR                documentElement
               44  STORE_FAST               'root'

 L.  76        46  LOAD_FAST                'self'
               48  LOAD_ATTR                data
               50  GET_ITER         
               52  FOR_ITER            100  'to 100'
               54  STORE_FAST               'key'

 L.  77        56  LOAD_FAST                'dom'
               58  LOAD_METHOD              createElement
               60  LOAD_FAST                'key'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'node'

 L.  78        66  LOAD_FAST                'node'
               68  LOAD_METHOD              appendChild
               70  LOAD_FAST                'dom'
               72  LOAD_METHOD              createTextNode
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                data
               78  LOAD_FAST                'key'
               80  BINARY_SUBSCR    
               82  CALL_METHOD_1         1  ''
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L.  79        88  LOAD_FAST                'root'
               90  LOAD_METHOD              appendChild
               92  LOAD_FAST                'node'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            52  'to 52'

 L.  80       100  LOAD_GLOBAL              print
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                cook_file
              106  CALL_FUNCTION_1       1  ''
              108  POP_TOP          

 L.  81       110  LOAD_GLOBAL              open
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                cook_file
              116  LOAD_STR                 'w'
              118  CALL_FUNCTION_2       2  ''
              120  SETUP_WITH          146  'to 146'
              122  STORE_FAST               'f'

 L.  82       124  LOAD_FAST                'dom'
              126  LOAD_ATTR                writexml
              128  LOAD_FAST                'f'
              130  LOAD_STR                 '\t'
              132  LOAD_STR                 '\n'
              134  LOAD_STR                 'utf-8'
              136  LOAD_CONST               ('addindent', 'newl', 'encoding')
              138  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              140  POP_TOP          
              142  POP_BLOCK        
              144  BEGIN_FINALLY    
            146_0  COME_FROM_WITH      120  '120'
              146  WITH_CLEANUP_START
              148  WITH_CLEANUP_FINISH
              150  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 144


class HttpRequest(object):

    def __init__(self, rootDir, cookieDir, fileOf404=None):
        self.RootDir = rootDir
        self.CookieDir = cookieDir
        self.NotFoundHtml = fileOf404
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.Cookie = None
        self.session = None
        self.request_data = dict()
        self.response_line = ''
        self.response_head = dict()
        self.response_body = ''

    def __readNotFoundHtml__--- This code section failed: ---

 L. 102         0  SETUP_FINALLY        50  'to 50'

 L. 103         2  LOAD_FAST                'self'
                4  LOAD_ATTR                NotFoundHtml
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    46  'to 46'

 L. 104        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                NotFoundHtml
               18  LOAD_STR                 'r'
               20  CALL_FUNCTION_2       2  ''
               22  STORE_FAST               'fd'

 L. 105        24  LOAD_FAST                'fd'
               26  LOAD_METHOD              read
               28  CALL_METHOD_0         0  ''
               30  STORE_FAST               'ret'

 L. 106        32  LOAD_FAST                'fd'
               34  LOAD_METHOD              close
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L. 107        40  LOAD_FAST                'ret'
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM            10  '10'
               46  POP_BLOCK        
               48  JUMP_FORWARD         62  'to 62'
             50_0  COME_FROM_FINALLY     0  '0'

 L. 108        50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 109        56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            48  '48'

 L. 110        62  LOAD_GLOBAL              CONTENT_404
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 42

    def __passRequestLine__(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url = header_list[1]
        if self.url == '/':
            self.url = '/index.html'
        self.protocol = header_list[2]

    def __passRequestHead__(self, request_head):
        head_options = request_head.split('\r\n')
        for option in head_options:
            key, val = option.split(': ', 1)
            self.head[key] = val

        if 'Cookie' in self.head:
            self.Cookie = self.head['Cookie']

    def passRequest(self, request):
        request = request.decode('utf-8')
        if len(request.split('\r\n', 1)) != 2:
            return
        request_line, body = request.split('\r\n', 1)
        request_head = body.split('\r\n\r\n', 1)[0]
        self.__passRequestLine__(request_line)
        self.__passRequestHead__(request_head)
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            parameters = request_body.split('&')
            for i in parameters:
                if i == '':
                    pass
                else:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val

            self.dynamicRequest(self.RootDir + self.url)
        elif self.method == 'GET':
            if self.url.find('?') != -1:
                self.request_data = {}
                req = self.url.split('?', 1)[1]
                s_url = self.url.split('?', 1)[0]
                parameters = req.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val

                self.dynamicRequest(self.RootDir + s_url)
            else:
                self.staticRequest(self.RootDir + self.url)

    def staticRequest(self, path):
        bIsNotFound = True
        if os.path.isfile(path):
            bIsNotFound = False
            extension_name = os.path.splitext(path)[1]
            extension_set = {'.css', '.html', '.js'}
            if extension_name == '.py':
                self.dynamicRequest(path)
            else:
                fd = openpath'rb'
                txt = fd.read()
                fd.close()
                self.response_line = ErrorCode.OK
                self.response_body = txt
                if extension_name == '.png':
                    self.response_head['Content-Type'] = 'text/png'
                elif extension_name in extension_set:
                    self.response_head['Content-Type'] = 'text/html'
                else:
                    bIsNotFound = True
        if bIsNotFound:
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = self.__readNotFoundHtml__()

    def __processSession__(self):
        self.session = Session()
        if self.Cookie is None:
            self.Cookie = self.__generateCookie__()
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            self.session.write2XML()
        else:
            cookie_file = self.CookieDir + self.Cookie
            self.session.cook_file = cookie_file
            if os.path.exists(cookie_file):
                self.session.loadFromXML()
            else:
                self.Cookie = self.__generateCookie__()
                cookie_file = self.CookieDir + self.Cookie
                self.session.cook_file = cookie_file
                self.session.write2XML()
        return self.session

    def __generateCookie__(self):
        import time, hashlib
        cookie = str(int(round(time.time() * 1000)))
        hl = hashlib.md5()
        hl.update(cookie.encode(encoding='utf-8'))
        return cookie

    def dynamicRequest(self, path):
        if not os.path.isfile(path) or os.path.splitext(path)[1] != '.py':
            self.response_line = ErrorCode.NOT_FOUND
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = self.__readNotFoundHtml__()
        else:
            file_path = path.split('.', 1)[0].replace('/', '.')
            self.response_line = ErrorCode.OK
            m = __import__(file_path)
            m.main.SESSION = self.__processSession__()
            if self.method == 'POST':
                m.main.POST = self.request_data
                m.main.GET = None
            else:
                m.main.POST = None
                m.main.GET = self.request_data
            self.response_body = m.main.app()
            self.response_head['Content-Type'] = 'text/html'
            self.response_head['Set-Cookie'] = self.Cookie

    def getResponse(self, body=None):
        if body is None:
            return self.response_line + dict2str(self.response_head) + '\r\n' + self.response_body
        return self.response_line + dict2str(self.response_head) + '\r\n' + body