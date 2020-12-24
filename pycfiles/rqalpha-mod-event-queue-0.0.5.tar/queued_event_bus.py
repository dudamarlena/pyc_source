# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cuiziqi/Documents/workspace/rqalpha-mod-event-queue/rqalpha_mod_event_queue/queued_event_bus.py
# Compiled at: 2017-10-22 04:31:09
try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty

from threading import Thread
from rqalpha.events import EventBus, EVENT
EVENT.TIMER = 'timer'

class QueuedEventBus(EventBus):

    def __init__(self, event_bus=None):
        super(QueuedEventBus, self).__init__()
        self._event_queue = Queue()
        self._thread = Thread(target=self.run)
        self._running = False
        if event_bus:
            self._listeners = event_bus._listeners

    DISTINCT_EVENTS = [
     EVENT.TICK,
     EVENT.BAR,
     EVENT.DO_PERSIST,
     EVENT.TIMER]

    def publish_event(self, event):
        self._event_queue.put(event)

    def run(self):
        while self._running:
            try:
                events = [
                 self._event_queue.get(timeout=1)]
            except Empty:
                continue

            while True:
                try:
                    events.append(self._event_queue.get_nowait())
                except Empty:
                    break

            last_pos = {}
            for i, e in enumerate(events):
                if e.event_type in self.DISTINCT_EVENTS:
                    last_pos[e.event_type] = i

            for i, e in enumerate(events):
                if e.event_type in self.DISTINCT_EVENTS and i != last_pos[e.event_type]:
                    continue
                for l in self._listeners[e.event_type]:
                    if l(e):
                        break

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()