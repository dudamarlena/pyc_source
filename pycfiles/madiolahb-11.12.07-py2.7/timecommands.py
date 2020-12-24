# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/madiolahb/timecommands.py
# Compiled at: 2011-12-07 21:30:37
from hce import max_influence, my_effected_time, other_effected_time, tick, time_range, TIME_READY
from models import INFLUENCES

def _crit(self):
    for char in self.activechars:
        if char.time == 0:
            char.recovery = max(0, char.recovery - 1)
            if char.key() not in self.updated:
                self.updated.append(char.key())


def _tick(self):
    if self.game.hold:
        self.game.hold = []
        self.gameupdated = True
    if self.game.active:
        self.game.active = None
        self.game.lastinfluence = None
        self.game.lastroll = None
        self.game.cureffect = None
        self.game.curtiming = None
        self.gameupdated = True
    self.atready = []
    for char in self.activechars:
        if char.time == TIME_READY:
            self.atready.append(char)

    while not self.atready:
        self.tickselapsed += 1
        for char in self.activechars:
            char.time = tick(char.time)
            if char.time == 0 and not char.recovery:
                char.time = 1
            if char.time == TIME_READY:
                self.atready.append(char)
                exerted = sum(getattr(char, inf) for inf in INFLUENCES)
                char.will_spot = exerted
                for inf in INFLUENCES:
                    setattr(char, inf, 0)

    for char in self.activechars:
        if char.time == 0:
            char.recovery = min(char.recovery - len(self.atready), 0)
        if char.key() not in self.updated:
            self.updated.append(char.key())

    return


def timing(self, subject=None, value=None, **kwargs):
    if value is None:
        return
    else:
        if not self._char(subject):
            return False
        if self.game.active:
            self.errors.append('%s is currently active' % self.game.active)
            return False
        if value.startswith('read'):
            maxpoise = max(max_influence(char, 'poise') for char in self.activechars if char.time == TIME_READY)
            if max_influence(self.char, 'poise') == maxpoise:
                self.game.active = self.char
                self.gameupdated = True
            else:
                self.errors.append('%s does not have the highest poise' % self.char.name)
                return False
        elif value.startswith('hold'):
            if self.char.time == TIME_READY and self.char.key() not in self.game.hold:
                self.game.hold.append(self.char.key())
                self.gameupdated = True
                if all(char.key() in self.game.hold for char in self.activechars if char.time == TIME_READY):
                    self._tick()
            elif self.char.time != TIME_READY:
                self.warnings.append('%s is not ready to hold' % self.char.name)
        elif value.startswith('interrupt'):
            self.game.active = self.char
            self.gameupdated = True
        else:
            self.warnings.append('Unrecognized timing verb "%s"' % value)
        return


def set(self, subject=None, object=None, time=None, **kwargs):
    if not self._char(subject):
        return False
    else:
        if self.game.active is not None:
            if not self._active():
                return False
        object = self._object(object)
        if object is None:
            return
        if time is not None:
            if not time_range(time):
                self.errors.append('%s is out of range for a time.' % time)
                return False
        elif self.game.active is None:
            time = max_influence(object, 'poise')
        elif object.key() == self.char.key():
            time = my_effected_time(self.char, self.game.lastinfluence, self.game.curtiming)
        else:
            time, delta = other_effected_time(object.time, self.game.curtiming)
            if delta != 0:
                self.game.curtiming -= delta
                if self.game not in self.updated:
                    self.updated.append(self.game)
        if time == 0 or time == TIME_READY:
            self._crit()
        object.time = time
        if time == 0:
            object.recovery = 0
            for char in self.activechars:
                if char.time != 0 and char.time != TIME_READY:
                    object.recovery += 1

        if object == self.char:
            self._tick()
        if object.key() not in self.updated:
            self.updated.append(object.key())
        return