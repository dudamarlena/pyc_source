# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\ui\matches_observable.py
# Compiled at: 2019-03-24 19:10:11
# Size of source mod 2**32: 920 bytes
from abc import ABC, abstractmethod
from typing import List, Iterable
from bets.model.matches import Match, Matches

class MatchesObserver(ABC):

    @abstractmethod
    def matches_changed(self, matches_observable: 'MatchesObservable'):
        pass


class MatchesObservable(Matches):

    def __init__(self):
        super().__init__()
        self._observers = []

    def notify_observers(self):
        for o in self._observers:
            o.matches_changed(self)

    def add_observer(self, observer: MatchesObserver):
        self._observers.append(observer)

    def append(self, match):
        super().append(match)
        self.notify_observers()

    def clear(self):
        super().clear()
        self.notify_observers()

    def extend(self, matches):
        super().extend(matches)
        self.notify_observers()