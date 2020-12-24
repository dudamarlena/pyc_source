# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/altnick.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 3758 bytes
__doc__ = 'Some alternate nick handlers.\n\nThis contains an underscore-appending handler and a number-substituting\n(leetifying) handler.\n\n'
from logging import getLogger
from taillight.signal import SignalStop
from PyIRC.signal import event
from PyIRC.numerics import Numerics
from PyIRC.extensions import BaseExtension
_logger = getLogger(__name__)

class UnderscoreAlt(BaseExtension):
    """UnderscoreAlt"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attempt_nick = self.nick
        self.attempts = 0

    @event('commands', Numerics.ERR_NICKNAMEINUSE, priority=-1000)
    @event('commands', Numerics.ERR_ERRONEOUSNICKNAME, priority=-1000)
    @event('commands', Numerics.ERR_NONICKNAMEGIVEN, priority=-1000)
    def change_nick(self, _, line):
        """Try to complete registration with a long _."""
        if self.registered:
            raise SignalStop()
        isupport = self.get_extension('ISupport')
        if not isupport:
            if self.attempts_count >= 5:
                return
        elif len(self.attempt_nick) == isupport.get('NICKLEN'):
            return
        self.attempt_nick += '_'
        self.attempts += 1
        self.send('NICK', [self.attempt_nick])
        raise SignalStop()


class NumberSubstitueAlt(BaseExtension):
    """NumberSubstitueAlt"""
    leetmap = {'A': '4', 
     'a': '4', 
     'B': '8', 
     'E': '3', 
     'e': '3', 
     'G': '6', 
     'g': '9', 
     'I': '1', 
     'i': '1', 
     'O': '0', 
     'o': '0', 
     'S': '5', 
     's': '5', 
     'T': '7', 
     't': '7', 
     '`': '\\'}
    unleetmap = {v:k for k, v in leetmap.items()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attempt_nick = self.nick
        self.index = 0

    @event('commands', Numerics.ERR_NICKNAMEINUSE, priority=-1000)
    @event('commands', Numerics.ERR_ERRONEOUSNICKNAME, priority=-1000)
    @event('commands', Numerics.ERR_NONICKNAMEGIVEN, priority=-1000)
    def change_nick(self, _, line):
        """Try to complete registration by being a 1337 h4x0r."""
        if self.registered:
            raise SignalStop()
        while self.index < len(self.attempt_nick):
            char = self.attempt_nick[self.index]
            if self.index > 0 and char in self.leetmap:
                char = self.leetmap[char]
            else:
                if char in self.unleetmap:
                    char = self.unleetmap[char]
                else:
                    self.index += 1
                    continue
            self.attempt_nick = self.attempt_nick[:self.index] + char + self.attempt_nick[self.index + 1:]
            self.send('NICK', [self.attempt_nick])
            self.index += 1
            raise SignalStop()