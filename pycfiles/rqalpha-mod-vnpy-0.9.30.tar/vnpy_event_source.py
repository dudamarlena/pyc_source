# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-vnpy/rqalpha_mod_vnpy/vnpy_event_source.py
# Compiled at: 2017-05-22 05:49:49
from datetime import timedelta, datetime, date
from dateutil.parser import parse
from threading import Thread
from enum import Enum
from rqalpha.utils.logger import system_log
from rqalpha.interface import AbstractEventSource
from rqalpha.events import Event, EVENT
from rqalpha.utils import RqAttrDict

class TimePeriod(Enum):
    BEFORE_TRADING = 'before_trading'
    AFTER_TRADING = 'after_trading'
    TRADING = 'trading'
    CLOSING = 'closing'


class VNPYEventSource(AbstractEventSource):

    def __init__(self, env, mod_config, gateway):
        self._env = env
        self._mod_config = mod_config
        self._gateway = gateway
        self._before_trading_processed = False
        self._after_trading_processed = False
        self._time_period = None
        return

    def mark_time_period(self, start_date, end_date):
        trading_days = self._env.data_proxy.get_trading_dates(start_date, end_date)

        def in_before_trading_time(time):
            if self._mod_config.all_day:
                return True
            return time.hour == 20 and time.minute < 55

        def in_after_trading(time):
            if self._mod_config.all_day:
                return True
            return time.hour == 15 and time.minute >= 30 or time.hour == 16

        def in_trading_time(time):
            if self._mod_config.all_day:
                return True
            else:
                if time.hour < 15 or time.hour >= 21:
                    return True
                if time.hour == 20 and time.minute >= 55:
                    return True
                if time.hour == 15 and time.minute < 30:
                    return True
                return False

        def in_trading_day(time):
            if self._mod_config.all_day:
                return True
            if time.hour < 20:
                if time.date() in trading_days:
                    return True
            elif (time + timedelta(days=1)).date() in trading_days:
                return True
            return False

        while True:
            now = datetime.now()
            if in_trading_time(now):
                self._time_period = TimePeriod.TRADING
                continue
            if not in_trading_day(now):
                self._time_period = TimePeriod.CLOSING
                continue
            if in_before_trading_time(now):
                self._time_period = TimePeriod.BEFORE_TRADING
                continue
            if in_after_trading(now):
                self._time_period = TimePeriod.AFTER_TRADING
                continue
            else:
                self._time_period = TimePeriod.CLOSING

    def events(self, start_date, end_date, frequency):
        if not self._mod_config.all_day:
            while datetime.now().date() < start_date - timedelta(days=1):
                continue

        mark_time_thread = Thread(target=self.mark_time_period, args=(start_date, date.fromtimestamp(2147483647)))
        mark_time_thread.setDaemon(True)
        mark_time_thread.start()
        while True:
            if self._time_period == TimePeriod.BEFORE_TRADING:
                if self._after_trading_processed:
                    self._after_trading_processed = False
                if not self._before_trading_processed:
                    system_log.debug('VNPYEventSource: before trading event')
                    yield Event(EVENT.BEFORE_TRADING, calendar_dt=datetime.now(), trading_dt=datetime.now() + timedelta(days=1))
                    self._before_trading_processed = True
                    continue
                else:
                    continue
            elif self._time_period == TimePeriod.TRADING:
                if not self._before_trading_processed:
                    system_log.debug('VNPYEventSource: before trading event')
                    yield Event(EVENT.BEFORE_TRADING, calendar_dt=datetime.now(), trading_dt=datetime.now() + timedelta(days=1))
                    self._before_trading_processed = True
                    continue
                else:
                    tick = self._gateway.get_tick()
                    calendar_dt = parse(('').join((str(tick.date), str(tick.time / 1000)))) if tick.time >= 100000000 else parse(('0').join((str(tick.date), str(tick.time / 1000))))
                    if calendar_dt.hour > 20:
                        trading_dt = calendar_dt + timedelta(days=1)
                    else:
                        trading_dt = calendar_dt
                    system_log.debug('VNPYEventSource: tick {}', tick)
                    yield Event(EVENT.TICK, calendar_dt=calendar_dt, trading_dt=trading_dt, tick=RqAttrDict(tick))
            elif self._time_period == TimePeriod.AFTER_TRADING:
                if self._before_trading_processed:
                    self._before_trading_processed = False
                if not self._after_trading_processed:
                    system_log.debug('VNPYEventSource: after trading event')
                    yield Event(EVENT.AFTER_TRADING, calendar_dt=datetime.now(), trading_dt=datetime.now())
                    self._after_trading_processed = True
                else:
                    continue