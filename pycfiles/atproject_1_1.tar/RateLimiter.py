# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: att/Client/RateLimiter.py
# Compiled at: 2017-03-18 13:14:58
import math
from att.clock import clock
from .CurrentRateMeasure import Measure
DEBUG = False
MAX_RATE_PERIOD = 20.0
MAX_RATE = 100000000000.0
PING_BOUNDARY = 1.2
PING_SAMPLES = 7
PING_DISCARDS = 1
PING_THRESHHOLD = 5
PING_DELAY = 5
PING_DELAY_NEXT = 2
ADJUST_UP = 1.05
ADJUST_DOWN = 0.95
UP_DELAY_FIRST = 5
UP_DELAY_NEXT = 2
SLOTS_STARTING = 6
SLOTS_FACTOR = 1.66 / 1000

class RateLimiter:

    def __init__(self, sched, unitsize, slotsfunc=lambda x: None):
        self.sched = sched
        self.last = None
        self.unitsize = unitsize
        self.slotsfunc = slotsfunc
        self.measure = Measure(MAX_RATE_PERIOD)
        self.autoadjust = False
        self.upload_rate = MAX_RATE * 1000
        self.slots = SLOTS_STARTING
        return

    def set_upload_rate(self, rate):
        if rate < 0:
            if self.autoadjust:
                return
            self.autoadjust = True
            self.autoadjustup = 0
            self.pings = []
            rate = MAX_RATE
            self.slots = SLOTS_STARTING
            self.slotsfunc(self.slots)
        else:
            self.autoadjust = False
        if not rate:
            rate = MAX_RATE
        self.upload_rate = rate * 1000
        self.lasttime = clock()
        self.bytes_sent = 0

    def queue(self, conn):
        assert conn.next_upload is None
        if self.last is None:
            self.last = conn
            conn.next_upload = conn
            self.try_send(True)
        else:
            conn.next_upload = self.last.next_upload
            self.last.next_upload = conn
            self.last = conn
        return

    def try_send(self, check_time=False):
        t = clock()
        self.bytes_sent -= (t - self.lasttime) * self.upload_rate
        self.lasttime = t
        if check_time:
            self.bytes_sent = max(self.bytes_sent, 0)
        cur = self.last.next_upload
        while self.bytes_sent <= 0:
            bytes = cur.send_partial(self.unitsize)
            self.bytes_sent += bytes
            self.measure.update_rate(bytes)
            if bytes == 0 or cur.backlogged():
                if self.last is cur:
                    self.last = None
                    cur.next_upload = None
                    break
                else:
                    self.last.next_upload = cur.next_upload
                    cur.next_upload = None
                    cur = self.last.next_upload
            else:
                self.last = cur
                cur = cur.next_upload
        else:
            self.sched(self.try_send, self.bytes_sent / self.upload_rate)

        return

    def adjust_sent(self, bytes):
        self.bytes_sent = min(self.bytes_sent + bytes, self.upload_rate * 3)
        self.measure.update_rate(bytes)

    def ping(self, delay):
        if DEBUG:
            print delay
        if not self.autoadjust:
            return
        self.pings.append(delay > PING_BOUNDARY)
        if len(self.pings) < PING_SAMPLES + PING_DISCARDS:
            return
        if DEBUG:
            print 'cycle'
        pings = sum(self.pings[PING_DISCARDS:])
        del self.pings[:]
        if pings >= PING_THRESHHOLD:
            if self.upload_rate == MAX_RATE:
                self.upload_rate = self.measure.get_rate() * ADJUST_DOWN
            else:
                self.upload_rate = min(self.upload_rate, self.measure.get_rate() * 1.1)
            self.upload_rate = max(int(self.upload_rate * ADJUST_DOWN), 2)
            self.slots = int(math.sqrt(self.upload_rate * SLOTS_FACTOR))
            self.slotsfunc(self.slots)
            if DEBUG:
                print 'adjust down to ' + str(self.upload_rate)
            self.lasttime = clock()
            self.bytes_sent = 0
            self.autoadjustup = UP_DELAY_FIRST
        else:
            if self.upload_rate == MAX_RATE:
                return
            self.autoadjustup -= 1
            if self.autoadjustup:
                return
            self.upload_rate = int(self.upload_rate * ADJUST_UP)
            self.slots = int(math.sqrt(self.upload_rate * SLOTS_FACTOR))
            self.slotsfunc(self.slots)
            if DEBUG:
                print 'adjust up to ' + str(self.upload_rate)
            self.lasttime = clock()
            self.bytes_sent = 0
            self.autoadjustup = UP_DELAY_NEXT