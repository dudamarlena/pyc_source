# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/somewheve/PycharmProjects/ctpbee/ctpbee/looper/account.py
# Compiled at: 2019-12-09 04:20:50
# Size of source mod 2**32: 11033 bytes
"""
* 账户模块, 存储资金修改, 负责对外部的成交单进行成交撮合 并扣除手续费 等操作
* 需要向外提供API
    trading: 发起交易
    is_traded: 是否可以进行交易
    result: 回测结果
"""
from collections import defaultdict
import numpy as np
from pandas import DataFrame
from ctpbee.constant import TradeData, OrderData, Offset, PositionData, Direction
from ctpbee.exceptions import ConfigError
from ctpbee.looper.local_position import LocalPositionManager

class AliasDayResult:
    __doc__ = '\n    每天的结果\n    '

    def __init__(self, **kwargs):
        """ 实例化进行调用 """
        for i, v in kwargs.items():
            setattr(self, i, v)

    def __repr__(self):
        result = 'DailyResult: { '
        for x in dir(self):
            if x.startswith('_'):
                continue
            result += f"{x}:{getattr(self, x)} "

        return result + '}'

    def _to_dict(self):
        return self.__dict__


class Account:
    __doc__ = '\n    账户类\n\n    支持成交之后修改资金 ， 对外提供API\n\n    '
    balance = 100000
    frozen = 0
    size = 5
    pricetick = 10
    daily_limit = 20
    commission = 0
    commission: float

    def __init__(self, interface):
        self.interface = interface
        self.pre_balance = 0
        self.daily_life = defaultdict(AliasDayResult)
        self.date = None
        self.commission = 0
        self.commission_expense = 0
        self.pre_commission_expense = 0
        self.count_statistics = 0
        self.pre_count = 0
        self.initial_capital = 0
        self.occupation_margin = 0
        self.init_position_manager_flag = False
        self.init = False

    @property
    def available(self) -> float:
        return self.balance - self.frozen - self.occupation_margin

    def is_traded(self, order: OrderData) -> bool:
        """ 当前账户是否足以支撑成交 """
        if order.price * order.volume * (1 + self.commission) > self.available:
            return False
        return True

    def update_trade(self, trade: TradeData) -> None:
        """
        当前选择调用这个接口的时候就已经确保了这个单子是可以成交的，
        make sure it can be traded if you choose to call this method,
        :param trade:交易单子/trade
        :return:
        """
        if trade.offset == Offset.OPEN:
            if self.commission != 0:
                commission_expense = trade.price * trade.volume * self.commission
            else:
                commission_expense = 0
        elif trade.offset == Offset.CLOSETODAY:
            if self.interface.params.get('today_commission') != 0:
                commission_expense = trade.price * trade.volume * self.interface.params.get('today_commission')
            else:
                commission_expense = 0
        elif trade.offset == Offset.CLOSEYESTERDAY:
            if self.interface.params.get('yesterday_commission') != 0:
                commission_expense = trade.price * trade.volume * self.interface.params.get('yesterday_commission')
            else:
                commission_expense = 0
        elif self.interface.params.get('close_commission') != 0:
            commission_expense = trade.price * trade.volume * self.interface.params.get('close_commission')
        else:
            commission_expense = 0
        if trade.offset == Offset.CLOSETODAY or trade.offset == Offset.CLOSEYESTERDAY or trade.offset == Offset.CLOSE:
            reversed_map = {Direction.LONG: Direction.SHORT, 
             Direction.SHORT: Direction.LONG}
            position = self.position_manager.get_position_by_ld(trade.local_symbol, reversed_map[trade.direction])
            if self.interface.params.get('size_map') is None or self.interface.params.get('size_map').get(trade.local_symbol) is None:
                raise ConfigError(message='请检查你的回测配置中是否存在着size配置', args=('回测配置错误', ))
            elif trade.direction == Direction.LONG:
                pnl = (position.price - trade.price) * trade.volume * self.interface.params.get('size_map').get(trade.local_symbol)
            else:
                pnl = (trade.price - position.price) * trade.volume * self.interface.params.get('size_map').get(trade.local_symbol)
            self.balance += pnl
        self.balance -= commission_expense
        self.commission_expense += commission_expense
        self.count_statistics += 1
        self.position_manager.update_trade(trade=trade)
        if not self.date:
            self.date = self.interface.date
        if self.interface.date != self.date:
            self.get_new_day()
            self.date = self.interface.date

    def update_margin(self, data: OrderData or TradeData, reverse=False):
        """
            更新保证金
            如果出现成交 开方向 ----> 增加保证金--> 默认
            如果出现成交 平方向 ----> 减少保证金
        """
        if reverse:
            self.occupation_margin += data.volume * data.price
            self.balance -= data.volume * data.price
        else:
            self.occupation_margin -= data.price * data.volume
            self.balance += data.volume * data.price

    def update_frozen(self, order, reverse=False):
        """
        根据reverse判断方向
        如果是False， 那么出现冻结，同时从余额里面扣除
        """
        if reverse:
            self.frozen -= order.volume * order.price
            self.balance += order.volume * order.price
        else:
            self.frozen += order.volume * order.price
            self.balance -= order.price * order.volume

    def get_new_day(self, interface_date=None):
        """ 生成今天的交易数据， 同时更新前日数据 ，然后进行持仓结算 """
        if not self.date:
            date = interface_date
        else:
            date = self.date
        p = AliasDayResult(balance=self.balance, 
         frozen=self.frozen, available=self.balance - self.frozen, date=date, 
         commission=self.commission_expense - self.pre_commission_expense, net_pnl=self.balance - self.pre_balance, 
         count=self.count_statistics - self.pre_count)
        self.interface.today_volume = 0
        self.pre_commission_expense = self.commission_expense
        self.pre_balance = self.balance
        self.pre_count = self.count_statistics
        self.position_manager.covert_to_yesterday_holding()
        self.daily_life[date] = p._to_dict()
        self.interface.pending.clear()
        self.balance += self.frozen
        self.frozen = 0

    def via_aisle--- This code section failed: ---

 L. 208         0  LOAD_FAST                'self'
                2  LOAD_ATTR                position_manager
                4  LOAD_METHOD              update_size_map
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                interface
               10  LOAD_ATTR                params
               12  CALL_METHOD_1         1  '1 positional argument'
               14  POP_TOP          

 L. 209        16  LOAD_FAST                'self'
               18  LOAD_ATTR                interface
               20  LOAD_ATTR                date
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                date
               26  COMPARE_OP               !=
               28  POP_JUMP_IF_FALSE    56  'to 56'

 L. 210        30  LOAD_FAST                'self'
               32  LOAD_METHOD              get_new_day
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                interface
               38  LOAD_ATTR                date
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_TOP          

 L. 211        44  LOAD_FAST                'self'
               46  LOAD_ATTR                interface
               48  LOAD_ATTR                date
               50  LOAD_FAST                'self'
               52  STORE_ATTR               date
               54  JUMP_FORWARD         56  'to 56'
             56_0  COME_FROM            54  '54'
             56_1  COME_FROM            28  '28'

Parse error at or near `COME_FROM' instruction at offset 56_0

    def update_params--- This code section failed: ---

 L. 217         0  SETUP_LOOP           76  'to 76'
                2  LOAD_FAST                'params'
                4  LOAD_METHOD              items
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  GET_ITER         
               10  FOR_ITER             74  'to 74'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'i'
               16  STORE_FAST               'v'

 L. 218        18  LOAD_FAST                'i'
               20  LOAD_STR                 'initial_capital'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    60  'to 60'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                init
               30  POP_JUMP_IF_TRUE     60  'to 60'

 L. 219        32  LOAD_FAST                'v'
               34  LOAD_FAST                'self'
               36  STORE_ATTR               balance

 L. 220        38  LOAD_FAST                'v'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               pre_balance

 L. 221        44  LOAD_FAST                'v'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               initial_capital

 L. 222        50  LOAD_CONST               True
               52  LOAD_FAST                'self'
               54  STORE_ATTR               init

 L. 223        56  CONTINUE             10  'to 10'
               58  JUMP_FORWARD         60  'to 60'
             60_0  COME_FROM            58  '58'
             60_1  COME_FROM            30  '30'
             60_2  COME_FROM            24  '24'

 L. 226        60  LOAD_GLOBAL              setattr
               62  LOAD_FAST                'self'
               64  LOAD_FAST                'i'
               66  LOAD_FAST                'v'
               68  CALL_FUNCTION_3       3  '3 positional arguments'
               70  POP_TOP          
               72  JUMP_BACK            10  'to 10'
               74  POP_BLOCK        
             76_0  COME_FROM_LOOP        0  '0'

 L. 227        76  LOAD_FAST                'self'
               78  LOAD_ATTR                init_position_manager_flag
               80  POP_JUMP_IF_TRUE    100  'to 100'

 L. 228        82  LOAD_GLOBAL              LocalPositionManager
               84  LOAD_FAST                'params'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               position_manager

 L. 229        92  LOAD_CONST               True
               94  LOAD_FAST                'self'
               96  STORE_ATTR               init_position_manager_flag
               98  JUMP_FORWARD        100  'to 100'
            100_0  COME_FROM            98  '98'
            100_1  COME_FROM            80  '80'

Parse error at or near `COME_FROM' instruction at offset 100_0

    @property
    def result(self):
        result = defaultdict(list)
        for daily in self.daily_life.values():
            for key, value in daily.items():
                result[key].append(value)

        df = DataFrame.from_dict(result).set_index('date')
        try:
            try:
                import matplotlib.pyplot as plt
                df['balance'].plot()
                plt.show()
            except ImportError as e:
                try:
                    pass
                finally:
                    e = None
                    del e

        finally:
            return

        return self._cal_result(df)

    def get_mapping(self, d):
        mapping = {}
        for i, v in self.daily_life.items():
            mapping[str(i)] = v.get(d)

        return mapping

    def _cal_result(self, df: DataFrame) -> dict:
        result = dict()
        df['return'] = np.log(df['balance'] / df['balance'].shift(1)).fillna(0)
        df['high_level'] = df['balance'].rolling(min_periods=1,
          window=(len(df)),
          center=False).max()
        df['draw_down'] = df['balance'] - df['high_level']
        df['dd_percent'] = df['draw_down'] / df['high_level'] * 100
        result['initial_capital'] = self.initial_capital
        result['start_date'] = df.index[0]
        result['end_date'] = df.index[(-1)]
        result['total_days'] = len(df)
        result['profit_days'] = len(df[(df['net_pnl'] > 0)])
        result['loss_days'] = len(df[(df['net_pnl'] < 0)])
        result['end_balance'] = df['balance'].iloc[(-1)]
        result['max_draw_down'] = df['draw_down'].min()
        result['max_dd_percent'] = df['dd_percent'].min()
        result['total_pnl'] = df['net_pnl'].sum()
        result['daily_pnl'] = result['total_pnl'] / result['total_days']
        result['total_commission'] = df['commission'].sum()
        result['daily_commission'] = result['total_commission'] / result['total_days']
        result['total_count'] = df['count'].sum()
        result['daily_count'] = result['total_count'] / result['total_days']
        result['total_return'] = (result['end_balance'] / self.initial_capital - 1) * 100
        result['annual_return'] = result['total_return'] / result['total_days'] * 240
        result['daily_return'] = df['return'].mean() * 100
        result['return_std'] = df['return'].std() * 100
        return result