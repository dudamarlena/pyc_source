# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ies\local_runner.py
# Compiled at: 2018-11-24 23:51:42
# Size of source mod 2**32: 5794 bytes
from strategycontainer.var import Var
import requests
from strategycontainer.server import IESServer
import sys, pytz
from ._version import ies_version

class LocalRunner(object):

    def __init__(self, user_name, user_password, host=None):
        print('IES localrunner version:' + ies_version)
        try:
            requests.packages.urllib3.disable_warnings()
            self.user_name = user_name
            self.user_password = user_password
            self._LocalRunner__host = 'https://service.gopipa.com' if host is None else host
            self._LocalRunner__login()
        except Exception as msg:
            sys.stderr.writelines(str(msg) + '\n')

    def runbacktest(self, strategy_id, investment_amount, test_start, test_end, train_start=None, train_end=None):
        try:
            print('Strategy:' + str(strategy_id) + ' starting backtest......')
            var = Var()
            var.HTTP_HEADERS = {'Authorization': 'Bearer ' + self._access_token}
            param = {'id': strategy_id}
            strategies = self._LocalRunner__http_get(self._LocalRunner__host + '/api/strategies', param, var.HTTP_HEADERS)
            if not strategies:
                raise Exception('Strategy:' + str(strategy_id) + ' not exist')
            self._strategy = strategies[0]
            self._LocalRunner__log(self._strategy)
            if self._user['userId'] != self._strategy['authorId']:
                raise Exception("You can't backtest other's strategy")
            param = {'userId':self._user['userId'], 
             'strategyId':strategy_id,  'investmentAmount':investment_amount,  'startDate':test_start,  'endDate':test_end,  'localRunner':True}
            if train_start is not None:
                param['trainStartDate'] = train_start
            if train_end is not None:
                param['trainEndDate'] = train_end
            headers = {'Authorization': var.HTTP_HEADERS['Authorization']}
            headers['Content-Type'] = 'text/plain;charset=UTF-8'
            var.IES_DEBUG = True
            var.PIPA_HOST = self._LocalRunner__host + ('/backtest' if 'http://localhost:' not in self._LocalRunner__host else '')
            var._FRAMEWORK_PORTFOLIOID = self._LocalRunner__http_put(var.PIPA_HOST + '/ts-mng/startBacktestRunner', param, None, headers)
            self._LocalRunner__log(var._FRAMEWORK_PORTFOLIOID)
            if var._FRAMEWORK_PORTFOLIOID == 0:
                raise Exception('A backtest of strategy ' + str(strategy_id) + ' has started already.')
            var._FRAMEWORK_BT_STARTDATE = test_start
            var._FRAMEWORK_BT_ENDDATE = test_end
            var._FRAMEWORK_TRAIN_STARTDATE = train_start
            var._FRAMEWORK_TRAIN_ENDDATE = train_end
            var._FRAMEWORK_IS_TEST_STRATEGY = True if self._strategy['backtestType'] == 'Test' else False
            var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY = True if self._strategy['backtestType'] == 'TrainAndTest' else False
            var._FRAMEWORK_IS_BACKTEST = True
            var._FRAMEWORK_IS_LIVETRADE = False
            var._FRAMEWORK_IS_DATAFETCHER = False
            var._FRAMEWORK_CURRENT_PHASE = 'train' if var._FRAMEWORK_IS_TRAIN_TEST_STRATEGY else 'test'
            var._FRAMEWORK_MARKETTYPE = 'CN' if self._strategy['marketType'] == 'CN' else 'US'
            if self._strategy['marketType'] == 'CN':
                var._TIMEZONE = pytz.timezone('Asia/Shanghai')
            ies_server = IESServer(var)
            ies_server.startServer()
            print('Strategy:' + str(strategy_id) + ' finish backtest')
        except Exception as msg:
            sys.stderr.writelines(str(msg) + '\n')

    def __extract_resp(self, resp):
        if resp['code'] == 0:
            return resp['data']
        raise Exception('[' + str(resp['code']) + ']' + resp['errMsg'])

    def __login(self):
        param = {'clientId':'PiPA', 
         'clientSecret':'secret',  'userNameOrEmail':self.user_name,  'password':self.user_password}
        login_return = self._LocalRunner__http_get(self._LocalRunner__host + '/api/public/login', param)
        if 'error' in login_return.keys():
            if login_return['error'] == '0':
                self._access_token = login_return['access_token']
        else:
            raise Exception(self.user_name + ' login failed, error code is ' + login_return['errMsg'])
        self._user = self._LocalRunner__http_get(self._LocalRunner__host + '/api/users/currentLoginUser', {}, {'Authorization': 'Bearer ' + self._access_token})
        if self._user['appId'] is None or self._user['developerState'] is None or self._user['developerState'] == 'Disabled':
            raise Exception('You must enable developer membership first.')
        self._LocalRunner__log(self._user)
        print(self.user_name + ' login success.')

    def __http_get(self, url, param, headers=None):
        try:
            r = requests.get(url, params=param, headers=headers, verify=False)
        except:
            raise Exception('call api failed, please check network connection.')

        if r.status_code == 200:
            return r.json()
        raise Exception('call api failed, status_code=' + str(r.status_code) + ',err_msg=' + r.json()['message'])

    def __http_put(self, url, param, json, headers=None):
        try:
            r = requests.put(url, params=param, headers=headers, data=json, verify=False)
        except:
            raise Exception('call api failed, please check network connection.')

        if r.status_code == 200:
            return r.json()
        raise Exception('call api failed, status_code=' + str(r.status_code) + ',err_msg=' + r.json()['message'])

    def __log(self, content):
        if 'http://localhost:' in self._LocalRunner__host:
            print(content)