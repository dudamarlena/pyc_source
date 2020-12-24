# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/vessel.py
# Compiled at: 2019-12-09 04:20:50
# Size of source mod 2**32: 9308 bytes
"""
回测容器模块, 回测
"""
from datetime import datetime
from threading import Thread
from time import sleep
from ctpbee.constant import ContractData, OrderData, TradeData, AccountData, PositionData, BarData, TickData
from ctpbee.log import VLogger
from ctpbee.looper.data import VessData
from ctpbee.looper.interface import LocalLooper
from ctpbee.cprint_config import CP
from ctpbee.looper.report import render_result
from ctpbee.jsond import dumps

class LooperApi:
    instrument_set = set()

    def __init__(self, name):
        self.name = name
        self.active = True

    def on_bar(self, bar):
        raise NotImplemented

    def on_tick(self, tick):
        raise NotImplemented

    def on_trade(self, trade):
        raise NotImplemented

    def on_order(self, order):
        raise NotImplemented

    def on_position(self, position):
        raise NotImplemented

    def on_account(self, account):
        raise NotImplemented

    def on_contract(self, contract):
        raise NotImplemented

    def init_params(self, data):
        """ 用户需要继承此方法"""
        pass

    def __call__(self, data):
        """
        你必须实现此方法以支持在此层进行中转
        """
        if data.local_symbol not in self.instrument_set:
            return
            if not self.active:
                return
            if isinstance(data, ContractData):
                self.on_contract(data)
        elif isinstance(data, OrderData):
            self.on_order(data)
        else:
            if isinstance(data, TradeData):
                self.on_trade(data)
            else:
                if isinstance(data, AccountData):
                    self.on_account(data)
                else:
                    if isinstance(data, PositionData):
                        self.on_position(data)
                    else:
                        if data['type'] == 'bar':
                            self.on_bar(BarData(**data))
                        else:
                            if data['type'] == 'tick':
                                self.on_tick(TickData(**data))
                            else:
                                raise ValueError('unsupported data')


class LooperLogger:

    def __init__(self, v_logger=None):
        if v_logger:
            self.logger = v_logger
        else:
            self.logger = VLogger(CP, app_name='Vessel')
            self.logger.set_default(name=(self.logger.app_name), owner='App')

    def info(self, msg, **kwargs):
        kwargs['owner'] = 'Looper'
        (self.logger.info)(msg, **kwargs)

    def error(self, msg, **kwargs):
        kwargs['owner'] = 'Looper'
        (self.logger.error)(msg, **kwargs)

    def debug(self, msg, **kwargs):
        kwargs['owner'] = 'Looper'
        (self.logger.debug)(msg, **kwargs)

    def warning(self, msg, **kwargs):
        kwargs['owner'] = 'Looper'
        (self.logger.warning)(msg, **kwargs)

    def __repr__(self):
        return 'LooperLogger -----> just enjoy it'


class Vessel:
    __doc__ = '\n    策略运行容器\n\n    本地回测与在线数据回测\n    >> 基于在线数据推送的模式 是否可以减少本机器的内存使用量\n\n    '

    def __init__(self, logger_class=None, pattern='T0'):
        self.ready = False
        self.looper_data = []
        if logger_class:
            self.logger = logger_class()
        else:
            self.logger = LooperLogger()
        self.risk = None
        self.interface = LocalLooper(logger=(self.logger), risk=(self.risk))
        self.params = dict()
        self.looper_pattern = pattern
        self._data_status = False
        self._looper_status = 'unready'
        self._strategy_status = False
        self._risk_status = True
        self.start_time = None

    def add_strategy(self, strategy: LooperApi):
        """ 添加策略到本容器 """
        if not isinstance(strategy, LooperApi):
            raise ValueError(f"你传入的策略类型出现问题，期望: LooperApi, 当前:{type(strategy)}")
        self.interface.update_strategy(strategy)
        self._strategy_status = True
        self.check_if_ready()

    def add_data(self, data):
        """
        注意此处的Add Data,可以添加多个数据源 ---> 他们的长度应该是一开始就对齐！！！
        ： ---> 必须在时间戳上进行对齐， 否则数据进行回放会出现问题。
        """
        d = VessData(data)
        self.looper_data.append(d)
        self._data_status = True
        self.check_if_ready()

    def check_if_ready(self):
        if self._data_status:
            if self._strategy_status:
                if self._risk_status:
                    self._looper_status = 'ready'
        self.ready = True

    def add_risk(self, risk):
        """ 添加风控 """
        self._risk_status = True
        self.interface.update_risk(risk)
        self.check_if_ready()

    def set_params(self, params):
        """
        设置参数
        :param params: 参数值 dict
        :return:
        """
        if not isinstance(params, dict):
            raise ValueError(f"配置信息格式出现问题， 你当前的配置信息为 {type(params)}")
        self.params = params

    def get_result(self, report: bool=False, **kwargs):
        """
        计算回测结果，生成回测报告
        :param report: bool ,指定是否输出策略报告
        :param auto_open: bool, 是否让浏览器自动打开回测报告
        :param zh:bpol, 是否输出成中文报告
        """
        strategys = list(self.interface.strategy_mapping.keys())
        end_time = datetime.now()
        account_data = self.interface.account.get_mapping('balance')
        cost_time = f"{str(end_time.hour - self.start_time.hour)}h {str(end_time.minute - self.start_time.minute)}m {str(end_time.second - self.start_time.second)}s"
        net_pnl = self.interface.account.get_mapping('net_pnl')
        trade_data = list(map(dumps, self.interface.traded_order_mapping.values()))
        if report:
            path = render_result(self.interface.account.result, trade_data=trade_data, strategy=strategys, net_pnl=net_pnl, 
             account_data=account_data, 
             datetimed=end_time, cost_time=cost_time, **kwargs)
            print(f"请复制下面的路径到浏览器打开----> \n {path}")
            return path
        return self.interface.account.result

    def letsgo--- This code section failed: ---

 L. 249         0  LOAD_CONST               False
                2  LOAD_LISTCOMP            '<code_object <listcomp>>'
                4  LOAD_STR                 'Vessel.letsgo.<locals>.<listcomp>'
                6  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                looper_data
               12  GET_ITER         
               14  CALL_FUNCTION_1       1  ''
               16  COMPARE_OP               not-in
               18  POP_JUMP_IF_FALSE    40  'to 40'

 L. 251        20  LOAD_FAST                'self'
               22  LOAD_ATTR                logger
               24  LOAD_METHOD              info
               26  LOAD_STR                 '回测模式: '
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                looper_pattern
               32  FORMAT_VALUE          0  ''
               34  BUILD_STRING_2        2 
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
             40_0  COME_FROM            18  '18'

 L. 252        40  LOAD_GLOBAL              range
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                looper_data
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_ATTR                length
               52  CALL_FUNCTION_1       1  ''
               54  GET_ITER         
               56  FOR_ITER            146  'to 146'
               58  STORE_FAST               'x'

 L. 253        60  LOAD_FAST                'ready'
               62  POP_JUMP_IF_FALSE   136  'to 136'

 L. 255        64  SETUP_FINALLY       102  'to 102'

 L. 257        66  LOAD_FAST                'self'
               68  LOAD_ATTR                looper_data
               70  GET_ITER         
               72  FOR_ITER             98  'to 98'
               74  STORE_FAST               '_origin_data'

 L. 258        76  LOAD_GLOBAL              next
               78  LOAD_FAST                '_origin_data'
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'p'

 L. 259        84  LOAD_FAST                'self'
               86  LOAD_METHOD              interface
               88  LOAD_FAST                'p'
               90  LOAD_FAST                'parmas'
               92  CALL_METHOD_2         2  ''
               94  POP_TOP          
               96  JUMP_BACK            72  'to 72'
               98  POP_BLOCK        
              100  JUMP_ABSOLUTE       144  'to 144'
            102_0  COME_FROM_FINALLY    64  '64'

 L. 261       102  DUP_TOP          
              104  LOAD_GLOBAL              StopIteration
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   132  'to 132'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 262       116  LOAD_STR                 'finished'
              118  LOAD_FAST                'self'
              120  STORE_ATTR               _looper_status

 L. 263       122  POP_EXCEPT       
              124  POP_TOP          
              126  BREAK_LOOP          146  'to 146'
              128  POP_EXCEPT       
              130  JUMP_ABSOLUTE       144  'to 144'
            132_0  COME_FROM           108  '108'
              132  END_FINALLY      
              134  JUMP_BACK            56  'to 56'
            136_0  COME_FROM            62  '62'

 L. 266       136  LOAD_GLOBAL              sleep
              138  LOAD_CONST               1
              140  CALL_FUNCTION_1       1  ''
              142  POP_TOP          
              144  JUMP_BACK            56  'to 56'

 L. 267       146  LOAD_FAST                'self'
              148  LOAD_ATTR                logger
              150  LOAD_METHOD              info
              152  LOAD_STR                 '回测结束,正在生成回测报告'
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

Parse error at or near `POP_TOP' instruction at offset 124

    def suspend_looper(self):
        """ 暂停回测 """
        self.ready = False
        self._looper_status = 'stopped'

    def enable_looper(self):
        """ 继续回测 """
        self.ready = True
        self._looper_status = 'running'

    @property
    def looper_status(self):
        return self._looper_status

    @property
    def risk_status(self):
        return self._risk_status

    @property
    def data_status(self):
        return self._data_status

    @property
    def strategy_status(self):
        return self._strategy_status

    @property
    def status(self):
        return (self._looper_status, self._risk_status, self._strategy_status, self._data_status)

    def run(self):
        """ 开始运行回测 """
        self.start_time = datetime.now()
        p = Thread(name='looper', target=(self.letsgo), args=(self.params, self.ready))
        p.start()
        p.join()

    def __repr__(self):
        return 'ctpbee Backtesting Vessel powered by ctpbee current version: 0.1'