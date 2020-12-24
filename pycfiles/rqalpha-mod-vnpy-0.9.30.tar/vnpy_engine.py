# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-vnpy/rqalpha_mod_vnpy/vnpy_engine.py
# Compiled at: 2017-05-12 03:46:08
from Queue import Queue, Empty
from six import iteritems
from rqalpha.events import EVENT
from rqalpha.events import Event as RqEvent
from rqalpha.utils.logger import system_log
from rqalpha.const import ACCOUNT_TYPE, ORDER_STATUS
from rqalpha.model.portfolio import Portfolio
from rqalpha.environment import Environment
from .vnpy import *
from .utils import make_order_book_id, make_trade, make_tick
from .vnpy_gateway import EVENT_COMMISSION, EVENT_QRY_ORDER
from .ctp_gateway import RQCtpGateway
_engine = None
EVENT_ENGINE_CONNECT = 'eEngineConnect'

class RQVNPYEngine(object):

    def __init__(self, env, config, data_factory, event_engine):
        self._env = env
        self._config = config
        self.event_engine = event_engine
        self.event_engine = event_engine
        self.event_engine.start()
        self.accounts = {}
        self.gateway_type = None
        self.vnpy_gateway = None
        self._init_gateway()
        self._data_factory = data_factory
        self._tick_que = Queue()
        self.strategy_subscribed = set()
        self._register_event()
        self._account_inited = False
        return

    def send_order(self, order):
        account = Environment.get_instance().get_account(order.order_book_id)
        self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_PENDING_NEW, account=account, order=order))
        order_req = self._data_factory.make_order_req(order)
        if order_req is None:
            self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_PENDING_CANCEL))
            order.mark_cancelled('No contract exists whose order_book_id is %s' % order.order_book_id)
            self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_CANCELLATION_PASS))
        if order.is_final():
            return
        else:
            self.vnpy_gateway.sendOrder(order_req)
            self._data_factory.cache_order(order)
            return

    def cancel_order(self, order):
        account = Environment.get_instance().get_account(order.order_book_id)
        self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_PENDING_CANCEL, account=account, order=order))
        cancel_order_req = self._data_factory.make_cancel_order_req(order)
        if cancel_order_req is None:
            system_log.warn('Cannot find VN.PY order in order cache.')
        self.vnpy_gateway.cancelOrder(cancelOrderReq=cancel_order_req)
        return

    def on_order(self, event):
        vnpy_order = event.dict_['data']
        system_log.debug('on_order {}', vnpy_order.__dict__)
        if vnpy_order.status == STATUS_UNKNOWN:
            return
        order = self._data_factory.get_order(vnpy_order)
        if self._account_inited:
            account = Environment.get_instance().get_account(order.order_book_id)
            order.active()
            self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_CREATION_PASS, account=account, order=order))
            self._data_factory.cache_vnpy_order(order.order_id, vnpy_order)
            if vnpy_order.status == STATUS_NOTTRADED or vnpy_order.status == STATUS_PARTTRADED:
                self._data_factory.cache_open_order(order)
            elif vnpy_order.status == STATUS_ALLTRADED:
                self._data_factory.del_open_order(int(vnpy_order.orderID))
            elif vnpy_order.status == STATUS_CANCELLED:
                self._data_factory.del_open_order(int(vnpy_order.orderID))
                if order.status == ORDER_STATUS.PENDING_CANCEL:
                    order.mark_cancelled('%d order has been cancelled by user.' % order.order_id)
                    self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_CANCELLATION_PASS, account=account, order=order))
                else:
                    order.mark_rejected('Order was rejected or cancelled by vnpy.')
                    self._env.event_bus.publish_event(RqEvent(EVENT.ORDER_UNSOLICITED_UPDATE, account=account, order=order))

    def on_qry_order(self, event):
        vnpy_order_dict = event.dict_['data']
        system_log.debug('on_qry_order {}', str(vnpy_order_dict.keys()))
        if not self._account_inited:
            for order_id, vnpy_order in iteritems(vnpy_order_dict):
                self._data_factory.cache_vnpy_order_before_init(vnpy_order)

    def get_open_orders(self, order_book_id):
        return self._data_factory.get_open_orders(order_book_id)

    def on_trade(self, event):
        vnpy_trade = event.dict_['data']
        system_log.debug('on_trade {}', vnpy_trade.__dict__)
        if not self._account_inited:
            self._data_factory.cache_vnpy_trade_before_init(vnpy_trade)
        else:
            order = self._data_factory.get_order(vnpy_trade)
            trade = make_trade(vnpy_trade, order.order_id)
            account = Environment.get_instance().get_account(order.order_book_id)
            self._env.event_bus.publish_event(RqEvent(EVENT.TRADE, account=account, trade=trade))

    def on_contract(self, event):
        contract_dict = event.dict_['data']
        system_log.debug('on_contract {}', len(contract_dict))
        for _, contract in iteritems(contract_dict):
            self._data_factory.cache_contract(contract)

    def on_commission(self, event):
        commission_dict = event.dict_['data']
        system_log.debug('on_commission {}', len(commission_dict))
        self._data_factory.put_commission(commission_dict)

    def on_universe_changed(self, event):
        universe = event.universe
        for order_book_id in universe:
            self.subscribe(order_book_id)

    def subscribe(self, order_book_id):
        if order_book_id not in self.strategy_subscribed:
            self.strategy_subscribed.add(order_book_id)

    def _subscribe(self, order_book_id):
        subscribe_req = self._data_factory.make_subscribe_req(order_book_id)
        if subscribe_req is None:
            system_log.error('Cannot find con tract whose order_book_id is %s' % order_book_id)
            return
        else:
            self.vnpy_gateway.subscribe(subscribeReq=subscribe_req)
            return

    def on_tick(self, event):
        vnpy_tick = event.dict_['data']
        tick = make_tick(vnpy_tick)
        if tick['order_book_id'] in self.strategy_subscribed:
            system_log.debug('on_tick {}', vnpy_tick.__dict__)
            self._tick_que.put(tick)
        self._data_factory.put_tick_snapshot(tick)

    def get_tick(self):
        while True:
            try:
                return self._tick_que.get(block=True, timeout=1)
            except Empty:
                system_log.debug('get tick timeout')
                continue

    def on_positions(self, event):
        vnpy_position_dict = event.dict_['data']
        system_log.debug('on_positions {}', vnpy_position_dict.keys())
        for _, vnpy_position in iteritems(vnpy_position_dict):
            self._data_factory.cache_vnpy_position(vnpy_position)

    def on_account(self, event):
        vnpy_account = event.dict_['data']
        system_log.debug('on_account {}', vnpy_account.__dict__)
        if not self._account_inited:
            self._data_factory.cache_vnpy_account_before_init(vnpy_account)

    def get_portfolio(self):
        future_account, static_value = self._data_factory.make_account_before_init()
        start_date = self._env.config.base.start_date
        future_starting_cash = self._env.config.base.future_starting_cash
        return Portfolio(start_date, static_value / future_starting_cash, future_starting_cash, {ACCOUNT_TYPE.FUTURE: future_account})

    def _init_gateway(self):
        self.gateway_type = self._config.gateway_type
        if self.gateway_type == 'CTP':
            self.vnpy_gateway = RQCtpGateway(self.event_engine, self.gateway_type, getattr(self._config, self.gateway_type))
        else:
            system_log.error('No Gateway named {}', self.gateway_type)

    def connect(self):
        self.vnpy_gateway.connect()
        self.vnpy_gateway.qrySettlementInfoConfirm()
        self.vnpy_gateway.qryContract()
        self.vnpy_gateway.qryOrder()
        self.vnpy_gateway.qryAccount()
        self.vnpy_gateway.qryAccount()
        self.vnpy_gateway.qryPosition()
        self.vnpy_gateway.qryCommission(self._data_factory.get_contract_cache().keys())
        for symbol in self._data_factory.get_contract_cache().keys():
            order_book_id = make_order_book_id(symbol)
            self._subscribe(order_book_id)

    @property
    def account_inited(self):
        return self._account_inited

    def exit(self):
        self.vnpy_gateway.close()
        self.event_engine.stop()

    def _register_event(self):
        self.event_engine.register(EVENT_ORDER, self.on_order)
        self.event_engine.register(EVENT_CONTRACT, self.on_contract)
        self.event_engine.register(EVENT_TRADE, self.on_trade)
        self.event_engine.register(EVENT_TICK, self.on_tick)
        self.event_engine.register(EVENT_ACCOUNT, self.on_account)
        self.event_engine.register(EVENT_POSITION, self.on_positions)
        self.event_engine.register(EVENT_COMMISSION, self.on_commission)
        self.event_engine.register(EVENT_QRY_ORDER, self.on_qry_order)
        self._env.event_bus.add_listener(EVENT.POST_UNIVERSE_CHANGED, self.on_universe_changed)