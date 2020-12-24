# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/chardet/charsetgroupprober.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 3787 bytes
from .enums import ProbingState
from .charsetprober import CharSetProber

class CharSetGroupProber(CharSetProber):

    def __init__(self, lang_filter=None):
        super(CharSetGroupProber, self).__init__(lang_filter=lang_filter)
        self._active_num = 0
        self.probers = []
        self._best_guess_prober = None

    def reset(self):
        super(CharSetGroupProber, self).reset()
        self._active_num = 0
        for prober in self.probers:
            if prober:
                prober.reset()
                prober.active = True
                self._active_num += 1
        else:
            self._best_guess_prober = None

    @property
    def charset_name(self):
        if not self._best_guess_prober:
            self.get_confidence()
            if not self._best_guess_prober:
                return
        return self._best_guess_prober.charset_name

    @property
    def language(self):
        if not self._best_guess_prober:
            self.get_confidence()
            if not self._best_guess_prober:
                return
        return self._best_guess_prober.language

    def feed(self, byte_str):
        for prober in self.probers:
            if not prober:
                pass
            elif not prober.active:
                pass
            else:
                state = prober.feed(byte_str)
                if not state:
                    pass
                else:
                    if state == ProbingState.FOUND_IT:
                        self._best_guess_prober = prober
                        return self.state
                    if state == ProbingState.NOT_ME:
                        prober.active = False
                        self._active_num -= 1
                        if self._active_num <= 0:
                            self._state = ProbingState.NOT_ME
                            return self.state
                    return self.state

    def get_confidence(self):
        state = self.state
        if state == ProbingState.FOUND_IT:
            return 0.99
        if state == ProbingState.NOT_ME:
            return 0.01
        best_conf = 0.0
        self._best_guess_prober = None
        for prober in self.probers:
            if not prober:
                pass
            elif not prober.active:
                self.logger.debug('%s not active', prober.charset_name)
            else:
                conf = prober.get_confidence()
                self.logger.debug('%s %s confidence = %s', prober.charset_name, prober.language, conf)
                if best_conf < conf:
                    best_conf = conf
                    self._best_guess_prober = prober
                if not self._best_guess_prober:
                    return 0.0
                return best_conf