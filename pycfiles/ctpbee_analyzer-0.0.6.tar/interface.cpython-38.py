# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/interface.py
# Compiled at: 2019-12-08 11:30:37
# Size of source mod 2**32: 16711 bytes
import collections, random, uuid
from copy import deepcopy
from typing import Text, List
from warnings import warn
from ctpbee.constant import OrderRequest, Offset, Direction, OrderType, OrderData, CancelRequest, TradeData, BarData, TickData, PositionData, Status, Exchange
from ctpbee.exceptions import ConfigError
from ctpbee.func import helper
from ctpbee.looper.account import Account

class Action:

    def __init__(self, looper):
        """ 将action这边报单 """
        self.looper = looper

    def buy(self, price, volume, origin, price_type: OrderType=OrderType.LIMIT, **kwargs):
        req = OrderRequest(price=price, volume=volume, exchange=(origin.exchange), offset=(Offset.OPEN), direction=(Direction.LONG),
          type=price_type,
          symbol=(origin.symbol))
        return self.looper.send_order(req)

    def short(self, price, volume, origin, price_type: OrderType=OrderType.LIMIT, **kwargs):
        req = OrderRequest(price=price, volume=volume, exchange=(origin.exchange), offset=(Offset.OPEN), direction=(Direction.SHORT),
          type=price_type,
          symbol=(origin.symbol))
        return self.looper.send_order(req)

    @property
    def position_manager(self):
        return self.looper.account.position_manager

    def sell(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData]=None, price_type: OrderType=OrderType.LIMIT, stop: bool=False, lock: bool=False, **kwargs):
        if not isinstance(self.looper.params['slippage_sell'], float):
            if not isinstance(self.looper.params['slippage_sell'], int):
                raise ConfigError(message='滑点配置应为浮点小数')
        price = price + self.looper.params['slippage_sell']
        req_list = [helper.generate_order_req_by_var(volume=(x[1]), price=price, offset=(x[0]), direction=(Direction.LONG), type=price_type,
          exchange=(origin.exchange),
          symbol=(origin.symbol)) for x in self.get_req(origin.local_symbol, Direction.SHORT, volume, self.looper)]
        return [self.looper.send_order(req) for req in req_list if req.volume != 0]

    def cover(self, price: float, volume: float, origin: [BarData, TickData, TradeData, OrderData, PositionData], price_type: OrderType=OrderType.LIMIT, stop: bool=False, lock: bool=False, **kwargs):
        if not isinstance(self.looper.params['slippage_cover'], float):
            if not isinstance(self.looper.params['slippage_cover'], int):
                raise ConfigError(message='滑点配置应为浮点小数')
        price = price + self.looper.exec_intercept['slippage_cover']
        req_list = [helper.generate_order_req_by_var(volume=(x[1]), price=price, offset=(x[0]), direction=(Direction.LONG), type=price_type,
          exchange=(origin.exchange),
          symbol=(origin.symbol)) for x in self.get_req(origin.local_symbol, Direction.SHORT, volume, self.looper)]
        return [self.looper.send_order(req) for req in req_list if req.volume != 0]

    def cancel(self, id: Text, origin: [BarData, TickData, TradeData, OrderData, PositionData]=None, **kwargs):
        if '.' in id:
            orderid = id.split('.')[1]
        else:
            if origin is None:
                exchange = kwargs.get('exchange')
                if isinstance(exchange, Exchange):
                    exchange = exchange.value
                local_symbol = kwargs.get('local_symbol')
            elif origin:
                exchange = origin.exchange.value
                local_symbol = origin.local_symbol
            if origin is None and len(kwargs) == 0:
                order = self.app.recorder.get_order(id)
                if not order:
                    print('找不到订单啦... 撤不了哦')
                    return
                exchange = order.exchange.value
                local_symbol = order.local_symbol
        req = helper.generate_cancel_req_by_str(order_id=orderid, exchange=exchange, symbol=local_symbol)
        return self.looper.cancel_order(req)

    @staticmethod
    def get_req(local_symbol, direction, volume: int, looper) -> List:
        """
        generate the offset and volume
        生成平仓所需要的offset和volume
         """

        def cal_req(position, volume, looper) -> List:
            if position.exchange.value not in looper.params['today_exchange']:
                return [[Offset.CLOSE, volume]]
            elif looper.params['close_pattern'] == 'today':
                td_volume = position.volume - position.yd_volume
                if td_volume >= volume:
                    return [[Offset.CLOSETODAY, volume]]
                if td_volume != 0:
                    return [[Offset.CLOSETODAY, td_volume], [Offset.CLOSEYESTERDAY, volume - td_volume]]
                return [[Offset.CLOSEYESTERDAY, volume]]
            elif looper.params['close_pattern'] == 'yesterday':
                if position.yd_volume >= volume:
                    return [
                     [
                      Offset.CLOSEYESTERDAY, volume]]
                if position.yd_volume != 0:
                    return [[Offset.CLOSEYESTERDAY, position.yd_volume], [Offset.CLOSETODAY, volume - position.yd_volume]]
                return [[Offset.CLOSETODAY, volume]]
            else:
                raise ValueError('异常配置, ctpbee只支持today和yesterday两种优先模式')

        position = looper.account.position_manager.get_position_by_ld(local_symbol, direction)
        if not position:
            msg = f"{local_symbol}在{direction.value}上无仓位"
            warn(msg)
            return []
        if position.volume < volume:
            msg = f"{local_symbol}在{direction.value}上仓位不足, 平掉当前 {direction.value} 的所有持仓, 平仓数量: {position.volume}"
            warn(msg)
            return cal_req(position, position.volume, looper)
        return cal_req(position, volume, looper)


class LocalLooper:
    message_box = {-1:'超出下单限制', 
     -2:'超出涨跌价格', 
     -3:'未成交', 
     -4:'资金不足'}

    def __init__(self, logger, risk=None):
        """ 需要构建完整的成交回报以及发单报告,在account里面需要存储大量的存储 """
        self.pending = []
        self.sessionid = random.randint(1000, 10000)
        self.frontid = random.randint(10001, 500000)
        self.logger = logger
        self.strategy_mapping = dict()
        self.upper_price = 99999
        self.drop_price = 0
        self.risk = risk
        self.params = dict(deal_pattern='match',
          single_order_limit=10,
          single_day_limit=100,
          today_exchange=[
         'INE', 'SHFE'])
        self.account = Account(self)
        self.order_ref = 0
        self.order_ref_set = set()
        self.traded_order_mapping = {}
        self.order_id_pending_mapping = {}
        self.today_volume = 0
        self.order_buffer = dict()
        self.date = None
        self.price = None

    def update_strategy(self, strategy):
        setattr(strategy, 'action', Action(self))
        setattr(strategy, 'logger', self.logger)
        setattr(strategy, 'info', self.logger.info)
        setattr(strategy, 'debug', self.logger.debug)
        setattr(strategy, 'error', self.logger.error)
        setattr(strategy, 'warning', self.logger.warning)
        self.strategy_mapping[strategy.name] = strategy

    def enable_extension(self, name):
        if name in self.strategy_mapping.keys():
            self.strategy_mapping.get(name).active = True
        else:
            return

    def suspend_extension(self, name):
        if name in self.strategy_mapping.keys():
            self.strategy_mapping.get(name).active = False
        else:
            return

    def update_risk(self, risk):
        self.risk = risk

    def _generate_order_data_from_req(self, req: OrderRequest):
        """ 将发单请求转换为发单数据 """
        self.order_ref += 1
        order_id = f"{self.frontid}-{self.sessionid}-{self.order_ref}"
        return req._create_order_data(gateway_name='looper', order_id=order_id, time=(self.datetime))

    def _generate_trade_data_from_order(self, order_data: OrderData):
        """ 将orderdata转换成成交单 """
        p = TradeData(price=(order_data.price), istraded=(order_data.volume), volume=(order_data.volume), tradeid=(str(uuid.uuid1())),
          offset=(order_data.offset),
          direction=(order_data.direction),
          gateway_name=(order_data.gateway_name),
          time=(order_data.time),
          order_id=(order_data.order_id),
          symbol=(order_data.symbol),
          exchange=(order_data.exchange))
        return p

    def send_order(self, order_req):
        """ 发单的操作"""
        self.intercept_gateway(order_req)

    def cancel(self, cancel_req):
        """ 撤单机制 """
        self.intercept_gateway(cancel_req)

    def intercept_gateway--- This code section failed: ---

 L. 232         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'data'
                4  LOAD_GLOBAL              OrderRequest
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE   144  'to 144'

 L. 234        10  LOAD_FAST                'self'
               12  LOAD_METHOD              match_deal
               14  LOAD_FAST                'self'
               16  LOAD_METHOD              _generate_order_data_from_req
               18  LOAD_FAST                'data'
               20  CALL_METHOD_1         1  ''
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'result'

 L. 235        26  LOAD_GLOBAL              isinstance
               28  LOAD_FAST                'result'
               30  LOAD_GLOBAL              TradeData
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE   126  'to 126'

 L. 238        36  LOAD_FAST                'self'
               38  LOAD_ATTR                logger
               40  LOAD_METHOD              info

 L. 239        42  LOAD_STR                 '成交时间: '
               44  LOAD_GLOBAL              str
               46  LOAD_FAST                'result'
               48  LOAD_ATTR                time
               50  CALL_FUNCTION_1       1  ''
               52  FORMAT_VALUE          0  ''
               54  LOAD_STR                 ', 成交价格'
               56  LOAD_GLOBAL              str
               58  LOAD_FAST                'result'
               60  LOAD_ATTR                price
               62  CALL_FUNCTION_1       1  ''
               64  FORMAT_VALUE          0  ''
               66  LOAD_STR                 ', 成交笔数: '
               68  LOAD_GLOBAL              str
               70  LOAD_FAST                'result'
               72  LOAD_ATTR                volume
               74  CALL_FUNCTION_1       1  ''
               76  FORMAT_VALUE          0  ''
               78  LOAD_STR                 ', 成交方向: '
               80  LOAD_GLOBAL              str
               82  LOAD_FAST                'result'
               84  LOAD_ATTR                direction
               86  LOAD_ATTR                value
               88  CALL_FUNCTION_1       1  ''
               90  FORMAT_VALUE          0  ''
               92  LOAD_STR                 '，行为: '
               94  LOAD_GLOBAL              str
               96  LOAD_FAST                'result'
               98  LOAD_ATTR                offset
              100  LOAD_ATTR                value
              102  CALL_FUNCTION_1       1  ''
              104  FORMAT_VALUE          0  ''
              106  BUILD_STRING_10      10 

 L. 238       108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 241       112  LOAD_FAST                'result'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                traded_order_mapping
              118  LOAD_FAST                'result'
              120  LOAD_ATTR                order_id
              122  STORE_SUBSCR     
              124  JUMP_FORWARD        144  'to 144'
            126_0  COME_FROM            34  '34'

 L. 244       126  LOAD_FAST                'self'
              128  LOAD_ATTR                logger
              130  LOAD_METHOD              info
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                message_box
              136  LOAD_FAST                'result'
              138  BINARY_SUBSCR    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           124  '124'
            144_1  COME_FROM             8  '8'

 L. 245       144  LOAD_GLOBAL              isinstance
              146  LOAD_FAST                'data'
              148  LOAD_GLOBAL              CancelRequest
              150  CALL_FUNCTION_2       2  ''
              152  POP_JUMP_IF_FALSE   232  'to 232'

 L. 248       154  LOAD_FAST                'self'
              156  LOAD_ATTR                pending
              158  GET_ITER         
            160_0  COME_FROM           174  '174'
              160  FOR_ITER            228  'to 228'
              162  STORE_DEREF              'order'

 L. 249       164  LOAD_FAST                'data'
              166  LOAD_ATTR                order_id
              168  LOAD_DEREF               'order'
              170  LOAD_ATTR                order_id
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   160  'to 160'

 L. 250       176  LOAD_GLOBAL              deepcopy
              178  LOAD_DEREF               'order'
              180  CALL_FUNCTION_1       1  ''
              182  STORE_DEREF              'order'

 L. 251       184  LOAD_CLOSURE             'order'
              186  BUILD_TUPLE_1         1 
              188  LOAD_LISTCOMP            '<code_object <listcomp>>'
              190  LOAD_STR                 'LocalLooper.intercept_gateway.<locals>.<listcomp>'
              192  MAKE_FUNCTION_8          'closure'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                strategy_mapping
              198  LOAD_METHOD              values
              200  CALL_METHOD_0         0  ''
              202  GET_ITER         
              204  CALL_FUNCTION_1       1  ''
              206  POP_TOP          

 L. 252       208  LOAD_FAST                'self'
              210  LOAD_ATTR                pending
              212  LOAD_METHOD              remove
              214  LOAD_DEREF               'order'
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 253       220  POP_TOP          
              222  LOAD_CONST               1
              224  RETURN_VALUE     
              226  JUMP_BACK           160  'to 160'

 L. 254       228  LOAD_CONST               0
              230  RETURN_VALUE     
            232_0  COME_FROM           152  '152'

Parse error at or near `LOAD_CONST' instruction at offset 222

    def match_deal(self, data: OrderData) -> int or :
        """ 撮合成交
            维护一个返回状态
            -1: 超出下单限制
            -2: 超出涨跌价格
            -3: 未成交
            -4: 资金不足
            p : 成交回报

            todo: 处理冻结 ??

        """
        if self.params.get('deal_pattern') == 'match':
            pass
        elif self.params.get('deal_pattern') == 'price' and not data.volume > self.params.get('single_order_limit'):
            if self.today_volume > self.params.get('single_day_limit'):
                return -1
            if not data.price < self.drop_price:
                if data.price > self.upper_price:
                    return -2
                self.account.update_frozen(data)
                long_c = self.price.low_price if self.price.low_price is not None else self.price.ask_price_1
                short_c = self.price.high_price if self.price.low_price is not None else self.price.bid_price_1
                long_b = self.price.open_price if self.price.low_price is not None else long_c
                short_b = self.price.open_price if self.price.low_price is not None else short_c
                long_cross = data.direction == Direction.LONG and data.price >= long_c > 0
                short_cross = data.direction == Direction.SHORT and data.price <= short_c and short_c > 0
                for order in self.pending:
                    index = self.pending.index(order)
                    long_cross = data.direction == Direction.LONG and order.price >= long_c > 0
                    short_cross = data.direction == Direction.SHORT and order.price <= short_c and short_c > 0
                    if not (long_cross or short_cross):
                        pass
                    else:
                        if long_cross:
                            order.price = min(order.price, long_b)
                        else:
                            order.price = max(order.price, short_b)
                        trade = self._generate_trade_data_from_order(order)
                        order.status = Status.ALLTRADED
                        [api(deepcopy(order)) for api in self.strategy_mapping.values()]
                        [api(trade) for api in self.strategy_mapping.values()]
                        self.pending.remove(order)
                        self.account.update_frozen(order=order, reverse=True)
                        self.update_account_margin(trade)

                if not long_cross:
                    if not short_cross:
                        self.pending.append(data)
                        return -3
                elif long_cross:
                    data.price = min(data.price, long_b)
                else:
                    data.price = max(data.price, short_b)
                if self.account.is_traded(data):
                    p = self._generate_trade_data_from_order(data)
                    self.account.update_trade(p)
                    [api(p) for api in self.strategy_mapping.values()]
                    self.today_volume += data.volume
                    self.account.update_frozen(p, reverse=True)
                    self.update_account_margin(p)
                    return p
                return -4
            else:
                raise TypeError('未支持的成交机制')

    def update_account_margin(self, p):
        if p.offset == Offset.OPEN:
            self.account.update_margin(p, reverse=True)
        else:
            self.account.update_margin(p)

    def init_params(self, params):
        """ 回测参数设置 """
        self.params.update(params)
        self.params.update(params)
        self.account.update_params(params)

    def __init_params(self, params):
        """ 初始化参数设置  """
        if not isinstance(params, dict):
            raise AttributeError('回测参数类型错误，请检查是否为字典')
        [strategy.init_params(params.get('strategy')) for strategy in self.strategy_mapping.values()]
        self.init_params(params.get('looper'))

    def __call__(self, *args, **kwargs):
        """ 回测周期 """
        p_data, params = args
        self.price = p_data
        self.datetime = p_data.datetime
        self._LocalLooper__init_params(params)
        if p_data.type == 'tick':
            [api(p_data) for api in self.strategy_mapping.values()]
        if p_data.type == 'bar':
            [api(p_data) for api in self.strategy_mapping.values()]
        self.date = p_data.datetime.date()
        self.account.via_aisle()