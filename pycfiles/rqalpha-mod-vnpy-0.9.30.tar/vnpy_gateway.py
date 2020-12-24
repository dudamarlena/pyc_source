# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-vnpy/rqalpha_mod_vnpy/vnpy_gateway.py
# Compiled at: 2017-05-12 03:41:08
from Queue import Empty
from .vnpy import *
EVENT_QRY_ORDER = 'eQryOrder'
EVENT_COMMISSION = 'eCommission'

def _id_gen(start=1):
    i = start
    while True:
        yield i
        i += 1


class RQPositionData(VtPositionData):

    def __init__(self):
        super(RQPositionData, self).__init__()
        self.todayPosition = EMPTY_FLOAT
        self.commission = EMPTY_FLOAT
        self.closeProfit = EMPTY_FLOAT
        self.openCost = EMPTY_FLOAT
        self.preSettlementPrice = EMPTY_FLOAT
        self.avgOpenPrice = EMPTY_FLOAT


class RQContractData(VtContractData):

    def __init__(self):
        super(RQContractData, self).__init__()
        self.openDate = EMPTY_STRING
        self.expireDate = EMPTY_STRING
        self.longMarginRatio = EMPTY_FLOAT
        self.shortMarginRatio = EMPTY_FLOAT


class RQCommissionData(VtBaseData):

    def __init__(self):
        super(RQCommissionData, self).__init__()
        self.symbol = EMPTY_STRING
        self.OpenRatioByMoney = EMPTY_FLOAT
        self.CloseRatioByMoney = EMPTY_FLOAT
        self.OpenRatioByVolume = EMPTY_FLOAT
        self.CloseRatioByVolume = EMPTY_FLOAT
        self.CloseTodayRatioByMoney = EMPTY_FLOAT
        self.CloseTodayRatioByVolume = EMPTY_FLOAT


class RQOrderReq(VtOrderReq):

    def __init__(self):
        super(RQOrderReq, self).__init__()
        self.orderID = EMPTY_INT


class RQVNEventEngine(EventEngine2):

    def __init__(self):
        super(RQVNEventEngine, self).__init__()

    def __run(self):
        u"""引擎运行"""
        print 'event_engine run'
        while self.__active == True:
            try:
                event = self.__queue.get(block=True, timeout=10)
                print str(event)
                self.__process(event)
            except Empty:
                pass
            except Exception as e:
                system_log.exception('event engine process fail')
                system_log.error('We can not handle this exception exiting.')
                os._exit(-1)