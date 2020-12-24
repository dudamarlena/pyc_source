# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\atapibasiclib\apirequest.py
# Compiled at: 2019-12-26 01:42:29
# Size of source mod 2**32: 5766 bytes
import atApiBasicLibrary.log as logger
import re, requests

def getPostInterfaceResponse(url, reqbody, headers):
    """
    【功能】根据接口uri、请求body、请求headers请求post接口
    【参数】url:被请求的接口全路径
            reqbody:请求参数，字典类型
            headers:请求头参数，字典类型
    【返回】包含：请求响应码status_code,响应头信息headers,响应体body
    """
    logger.info(('getInterfaceResponse.reqbody=%s' % reqbody), html=True, also_console=True)
    try:
        resp = requests.post(url, json=reqbody, headers=headers)
        respdict = {}
        respdict['status_code'] = resp.status_code
        respdict['headers'] = resp.headers
        respdict['body'] = resp.text
        return respdict
    except requests.exceptions.RequestException as e:
        try:
            logger.error('getInterfaceResponse异常：%s' % e)
            raise AssertionError('getInterfaceResponse异常:%s' % e)
        finally:
            e = None
            del e


def httppostresponsebody--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              logger
                2  LOAD_ATTR                info
                4  LOAD_STR                 'url='
                6  LOAD_FAST                'url'
                8  BINARY_ADD       
               10  LOAD_CONST               True
               12  LOAD_CONST               True
               14  LOAD_CONST               ('html', 'also_console')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_TOP          

 L.  34        20  LOAD_GLOBAL              logger
               22  LOAD_ATTR                info
               24  LOAD_STR                 'getInterfaceResponse.reqbody=%s'
               26  LOAD_FAST                'reqbody'
               28  BINARY_MODULO    
               30  LOAD_CONST               True
               32  LOAD_CONST               True
               34  LOAD_CONST               ('html', 'also_console')
               36  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               38  POP_TOP          

 L.  35        40  SETUP_FINALLY        90  'to 90'

 L.  36        42  LOAD_FAST                'reqbody'
               44  BUILD_MAP_0           0 
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    66  'to 66'

 L.  37        50  LOAD_GLOBAL              requests
               52  LOAD_ATTR                post
               54  LOAD_FAST                'url'
               56  LOAD_FAST                'headers'
               58  LOAD_CONST               ('headers',)
               60  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               62  STORE_FAST               'resp'
               64  JUMP_FORWARD         82  'to 82'
             66_0  COME_FROM            48  '48'

 L.  39        66  LOAD_GLOBAL              requests
               68  LOAD_ATTR                post
               70  LOAD_FAST                'url'
               72  LOAD_FAST                'reqbody'
               74  LOAD_FAST                'headers'
               76  LOAD_CONST               ('json', 'headers')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  STORE_FAST               'resp'
             82_0  COME_FROM            64  '64'

 L.  41        82  LOAD_FAST                'resp'
               84  LOAD_ATTR                text
               86  POP_BLOCK        
               88  RETURN_VALUE     
             90_0  COME_FROM_FINALLY    40  '40'

 L.  42        90  DUP_TOP          
               92  LOAD_GLOBAL              requests
               94  LOAD_ATTR                exceptions
               96  LOAD_ATTR                RequestException
               98  COMPARE_OP               exception-match
              100  POP_JUMP_IF_FALSE   146  'to 146'
              102  POP_TOP          
              104  STORE_FAST               'e'
              106  POP_TOP          
              108  SETUP_FINALLY       134  'to 134'

 L.  43       110  LOAD_GLOBAL              logger
              112  LOAD_METHOD              error
              114  LOAD_STR                 'getInterfaceResponse异常：%s'
              116  LOAD_FAST                'e'
              118  BINARY_MODULO    
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L.  44       124  POP_BLOCK        
              126  POP_EXCEPT       
              128  CALL_FINALLY        134  'to 134'
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'
            134_1  COME_FROM_FINALLY   108  '108'

 L.  45       134  LOAD_CONST               None
              136  STORE_FAST               'e'
              138  DELETE_FAST              'e'
              140  END_FINALLY      
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           100  '100'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'

Parse error at or near `POP_EXCEPT' instruction at offset 126


def httpputresponsebody(url, headers=None, json=None):
    logger.info(('url=' + url), html=True, also_console=True)
    if url is None:
        logger.error('url参数是None!', False)
        raise AssertionError('url参数是None')
    try:
        if headers is None:
            headers = {}
        else:
            headers.update({'Content-Type': 'application/json;charset=UTF-8'})
            if json is None:
                response = requests.put(url, headers=headers)
            else:
                response = requests.put(url, headers=headers, json=json)
        return response.text
    except requests.exceptions.RequestException as e:
        try:
            logger.error('发送请求失败，原因：%s' % e)
            raise AssertionError('发送请求失败，原因：%s' % e)
        finally:
            e = None
            del e


def httpdeleteresponsebody(url, params=None, headers=None):
    if url is None:
        logger.error('uri参数是None!', False)
        raise AssertionError('uri参数是None')
    try:
        response = requests.delete(url, headers=headers, params=params)
        return response.text
    except requests.exceptions.RequestException as e:
        try:
            logger.error('发送请求失败，原因：%s' % e)
            raise AssertionError('发送请求失败，原因：%s' % e)
        finally:
            e = None
            del e


def httpgetresponsebody(url, params=None, headers=None, timeout=None):
    """
       【功能】处理GET方式的接口请求
       【参数】url:接口地址
               params:请求参数，字典类型
               headers:请求头信息，字典类型
               timeout:请求超时时间
       【返回】响应Body,即response.text
       """
    logger.info(('url=' + url), html=True, also_console=True)
    if url is None:
        logger.error('url参数是None!', False)
        raise AssertionError('url参数是None')
    try:
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        return response.text
    except requests.exceptions.RequestException as e:
        try:
            logger.error('发送请求失败，原因：%s' % e)
            raise AssertionError('发送请求失败，原因：%s' % e)
        finally:
            e = None
            del e


def getxforcesaastoken(url, reqbody, headers):
    """
    【功能】根据接口uri、请求body、请求headers请求登录接口
    【参数】url:被请求的接口全路径
            reqbody:请求参数，字典类型
            headers:请求头参数，字典类型
    【返回】token,string类型
    """
    logger.info(('getInterfaceResponse.reqbody=%s' % reqbody), html=True, also_console=True)
    try:
        resp = requests.post(url, json=reqbody, headers=headers)
        xforcesaastoken = eval(resp.text).get('data').get('xforce-saas-token')
        return xforcesaastoken
    except requests.exceptions.RequestException as e:
        try:
            logger.error('getInterfaceResponse异常：%s' % e)
            raise AssertionError('getInterfaceResponse异常:%s' % e)
        finally:
            e = None
            del e


def gettoken(url, reqbody, headers):
    """
    【功能】根据接口uri、请求body、请求headers请求登录接口
    【参数】url:被请求的接口全路径
            reqbody:请求参数，字典类型
            headers:请求头参数，字典类型
    【返回】token,string类型
    """
    logger.info(('getInterfaceResponse.reqbody=%s' % reqbody), html=True, also_console=True)
    try:
        resp = requests.post(url, json=reqbody, headers=headers)
        respheader = resp.headers['Set-Cookie']
        token = re.search('xforce-saas-token=(.*)', respheader).group(0).split(';')[0].split('=')[1]
        return token
    except requests.exceptions.RequestException as e:
        try:
            logger.error('getInterfaceResponse异常：%s' % e)
            raise AssertionError('getInterfaceResponse异常:%s' % e)
        finally:
            e = None
            del e