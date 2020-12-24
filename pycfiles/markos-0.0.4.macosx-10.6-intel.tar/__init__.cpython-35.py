# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/blazaid/Projects/markos/env/lib/python3.5/site-packages/markos/__init__.py
# Compiled at: 2016-05-27 16:17:30
# Size of source mod 2**32: 2752 bytes
import random
from collections import defaultdict
__version__ = '0.0.4'

class MarkovChain:

    class Start:
        pass

    START = Start()

    class End:
        pass

    END = End()

    def __init__(self, grade=0):
        self.events = defaultdict(lambda : defaultdict(lambda : 0))
        self.grade = grade

    def train(self, chain):
        chain = [
         MarkovChain.START] + chain + [MarkovChain.END]
        previous_event = [chain[0]]
        for event in chain[1:]:
            self.events[tuple(previous_event)][event] += 1
            if len(previous_event) > self.grade:
                previous_event.pop(0)
            previous_event.append(event)

    def select(self, choices):
        choices = list(choices)
        total_events = sum(weight for event, weight in choices)
        r = random.uniform(0, total_events)
        upto = 0
        for event, weight in choices:
            if upto + weight >= r:
                return event
            upto += weight

    def next_events(self, event, end):
        return ((event, weight) for event, weight in self.events[tuple(event)].items() if event is not MarkovChain.END or event is MarkovChain.END and end)

    def generate(self, event=None, max_events=None, end=True):
        selected_event = event or self.select(self.next_events([MarkovChain.START], end))
        yield selected_event
        previous_event = [MarkovChain.START]
        if len(previous_event) > self.grade:
            previous_event.pop(0)
        previous_event += [selected_event] if isinstance(selected_event, str) else list(selected_event)
        stop = tuple(previous_event) not in self.events or MarkovChain.END in previous_event
        while not stop:
            choices = self.next_events(previous_event, end)
            if choices:
                event = self.select(choices)
                if event is not MarkovChain.END:
                    yield event
                if len(previous_event) > self.grade:
                    previous_event.pop(0)
                previous_event.append(event)
                if max_events is not None:
                    max_events -= 1
                event_starts_transition = tuple(previous_event) in self.events
                last_element = max_events is not None and max_events <= 1
                stop = not event_starts_transition or last_element
            else:
                stop = True