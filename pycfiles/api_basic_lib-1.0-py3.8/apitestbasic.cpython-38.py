# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\atapibasiclib\apitestbasic.py
# Compiled at: 2019-12-26 03:58:36
# Size of source mod 2**32: 9283 bytes
"""
此模块包含api测试的相关基础方法
"""
import json, time, pymysql
from atapibasiclib import apirequest, jsoncompare
import atApiBasicLibrary.log as logger
from atapibasiclib.mysqllib import excutemysql, queryfrommysql, queryonefrommysql
config = {'host':'phoenix-t.xforceplus.com', 
 'port':23315,  'user':'root',  'password':'xplat',  'db':'bdt-config',  'charset':'utf8mb4'}

def getmysqlconnwithconfig--- This code section failed: ---

 L.  21         0  SETUP_FINALLY        60  'to 60'

 L.  22         2  LOAD_GLOBAL              logger
                4  LOAD_METHOD              info
                6  LOAD_STR                 '数据库连接'
                8  LOAD_GLOBAL              str
               10  LOAD_GLOBAL              config
               12  CALL_FUNCTION_1       1  ''
               14  BINARY_ADD       
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L.  23        20  LOAD_GLOBAL              config
               22  LOAD_METHOD              get
               24  LOAD_STR                 'charset'
               26  CALL_METHOD_1         1  ''
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    42  'to 42'

 L.  24        34  LOAD_STR                 'utf8'
               36  LOAD_GLOBAL              config
               38  LOAD_STR                 'charset'
               40  STORE_SUBSCR     
             42_0  COME_FROM            32  '32'

 L.  25        42  LOAD_GLOBAL              pymysql
               44  LOAD_ATTR                connect
               46  BUILD_TUPLE_0         0 
               48  LOAD_GLOBAL              config
               50  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               52  STORE_FAST               'connection'

 L.  26        54  LOAD_FAST                'connection'
               56  POP_BLOCK        
               58  RETURN_VALUE     
             60_0  COME_FROM_FINALLY     0  '0'

 L.  27        60  DUP_TOP          
               62  LOAD_GLOBAL              pymysql
               64  LOAD_ATTR                OperationalError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE   116  'to 116'
               70  POP_TOP          
               72  STORE_FAST               'e'
               74  POP_TOP          
               76  SETUP_FINALLY       104  'to 104'

 L.  28        78  LOAD_GLOBAL              logger
               80  LOAD_METHOD              error
               82  LOAD_STR                 '连接数据库失败，原因：%s'
               84  LOAD_FAST                'e'
               86  BINARY_MODULO    
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L.  29        92  LOAD_GLOBAL              AssertionError
               94  LOAD_FAST                'e'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
              100  POP_BLOCK        
              102  BEGIN_FINALLY    
            104_0  COME_FROM_FINALLY    76  '76'
              104  LOAD_CONST               None
              106  STORE_FAST               'e'
              108  DELETE_FAST              'e'
              110  END_FINALLY      
              112  POP_EXCEPT       
              114  JUMP_FORWARD        178  'to 178'
            116_0  COME_FROM            68  '68'

 L.  30       116  DUP_TOP          
              118  LOAD_GLOBAL              pymysql
              120  LOAD_ATTR                MySQLError
              122  COMPARE_OP               exception-match
              124  POP_JUMP_IF_FALSE   176  'to 176'
              126  POP_TOP          
              128  STORE_FAST               'e'
              130  POP_TOP          
              132  SETUP_FINALLY       164  'to 164'

 L.  31       134  LOAD_GLOBAL              logger
              136  LOAD_METHOD              error
              138  LOAD_STR                 '连接数据库失败，原因：%s'
              140  LOAD_FAST                'e'
              142  BINARY_MODULO    
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L.  32       148  LOAD_GLOBAL              AssertionError
              150  LOAD_STR                 '连接数据库失败，原因：%s'
              152  LOAD_FAST                'e'
              154  BINARY_MODULO    
              156  CALL_FUNCTION_1       1  ''
              158  RAISE_VARARGS_1       1  'exception instance'
              160  POP_BLOCK        
              162  BEGIN_FINALLY    
            164_0  COME_FROM_FINALLY   132  '132'
              164  LOAD_CONST               None
              166  STORE_FAST               'e'
              168  DELETE_FAST              'e'
              170  END_FINALLY      
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           124  '124'
              176  END_FINALLY      
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           114  '114'

Parse error at or near `DUP_TOP' instruction at offset 116


def apitest(case_data):
    """
    【功能】接口测试执行脚本
    【参数】case_data:测试用例数据
    【结果】预期结果和实际结果校验，如果相同，用例通过，否则用例执行失败
    """
    if case_data.get'database_setup' is not None:
        sqlsetups = str(case_data.get'database_setup').split';'
        print('setupsqls=%s' % sqlsetups)
        for i in range(len(sqlsetups)):
            if sqlsetups[i] != '':
                excutemysql(getmysqlconnwithconfig(), sqlsetups[i])
            else:
                url = case_data.get'loginUrl' + case_data.get'loginPath'
                header = eval(case_data.get'header')
                token = apirequest.getxforcesaastoken(url=url, reqbody=(eval(case_data.get'loginBody')), headers=header)
                header['xforce-saas-token'] = token
                if case_data.get'database_query' is not None:
                    if case_data.get'return_value' is None:
                        logger.info'database_query和return_value的数量不一致，请修改用例数据......'
                        assert 1 == 0
                        return
                    querysqls = str(case_data.get'database_query').split';'
                    returnvalues = str(case_data.get'return_value').split';'
                    if len(querysqls) != len(returnvalues):
                        logger.info('database_query和return_value的数量不一致，请修改用例数据......', html=True, also_console=True)
                        assert 1 == 0
                        return
                    for m in range(len(querysqls)):
                        if querysqls[m] != '':
                            queryresult = queryonefrommysql(getmysqlconnwithconfig(), querysqls[m])
                            case_data[returnvalues[m]] = list(queryresult[0].values())[0]
                            print('case_data=%s' % json.dumpscase_data)
                            logger.info(('case_data==%s' + json.dumpscase_data), html=True, also_console=True)

                method = str(case_data.get'method').upper()
                url = case_data.get'hostUrl' + case_data.get'path'
                if case_data.get'data' is not None:
                    if case_data.get'urlParameter' is not None:
                        datasqls = str(case_data.get'data').split';'
                        dataresultdict = {}
                        for n in range(len(datasqls)):
                            if datasqls[n] != '':
                                dataresultdict[list(queryonefrommysql(getmysqlconnwithconfig(), datasqls[n])[0].keys())[0]] = list(queryonefrommysql(getmysqlconnwithconfig(), datasqls[n])[0].values())[0]
                        else:
                            urlParameter = str(case_data.get'urlParameter')
                            for key in dataresultdict:
                                urlParameter = urlParameter.replace('${' + key + '}', str(dataresultdict[key]))
                            else:
                                logger.info(('urlParameter=%s' % urlParameter), html=True, also_console=True)

                resp = None
                if method == 'POST':
                    resp = apirequest.httppostresponsebody(url=url, reqbody=(eval(case_data.get'request_body')), headers=header)
                else:
                    if method == 'GET':
                        url = url + urlParameter
                        resp = apirequest.httpgetresponsebody(url=url, headers=header)
                    else:
                        if method == 'PUT':
                            url = url + urlParameter
                            resp = apirequest.httpputresponsebody(url=url, json=(eval(case_data.get'request_body')), headers=header)
                        else:
                            if method == 'DELETE':
                                url = url + urlParameter
                                resp = apirequest.httpdeleteresponsebody(url=url, headers=header)
                            print('resp=%s' % resp)
                            if resp is None:
                                logger.info('接口请求失败，无响应', html=True, also_console=True)
                                if case_data.get'database_teardown' is not None:
                                    teardownsqls = str(case_data.get'database_teardown').split';'
                                    for j in range(len(teardownsqls)):
                                        if teardownsqls[j] != '':
                                            excutemysql(getmysqlconnwithconfig(), teardownsqls[j])

                                else:
                                    raise AssertionError('接口无响应，用例执行失败......')
                result1 = True
                result2 = True
                logger.info('开始进行响应结果验证......', html=True, also_console=True)
                expected_resp = eval(case_data.get'expected_response')
                result1 = jsoncompare.json_comp(resp, expected_resp)
                print('result1=%s' % result1)
                if result1 == False:
                    raise AssertionError('实际结果和期望结果不一致......')
                else:
                    logger.info('开始进行数据库验证......', html=True, also_console=True)
                    if case_data.get'database_verification' is not None:
                        verificationsqls = str(case_data.get'database_verification').split';'
                        if case_data.get'expected_rowcount' is None:
                            raise AssertionError('用例参数expected_rowcount不能为空，请补充数据......')
                        else:
                            expectedrowcount = str(case_data.get'expected_rowcount').split';'
                        logger.info(('expectedrowcount=%s' % expectedrowcount), html=True, also_console=True)
                        if len(verificationsqls) != len(expectedrowcount):
                            raise AssertionError('expected_rowcount数量和database_verification数量不一致，请检查用例数据.......')

    else:
        for k in range(len(verificationsqls)):
            if verificationsqls[k] != '':
                if queryfrommysql(getmysqlconnwithconfig(), verificationsqls[k]) is not None:
                    count = len(queryfrommysql(getmysqlconnwithconfig(), verificationsqls[k]))
                else:
                    count = 0
                logger.info(('count=%d' % count), html=True, also_console=True)
                if count == int(expectedrowcount[k]):
                    result2 = True
                else:
                    time.sleep10
                    if case_data.get'database_delete' is not None:
                        print('数据库校验失败，开始清理数据.......')
                        deletesqls = str(case_data.get'database_delete').split';'
                        for m in range(len(deletesqls)):
                            if deletesqls[m] != '':
                                excutemysql(getmysqlconnwithconfig(), deletesqls[m])

                    else:
                        print('数据库校验失败，开始重新请求.......')
                        resp = apirequest.getpostresponsebody(url=url, reqbody=(eval(case_data.get'request_body')), headers=header)
                        print('resp=%s' % resp)
                        result2 = False
        else:
            if case_data.get'database_teardown' is not None:
                teardownsqls = str(case_data.get'database_teardown').split';'
                for j in range(len(teardownsqls)):
                    if teardownsqls[j] != '':
                        excutemysql(getmysqlconnwithconfig(), teardownsqls[j])

            assert result1 & result2 == True