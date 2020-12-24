# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/requests/requests/packages/chardet/charsetgroupprober.py
# Compiled at: 2018-07-11 18:15:32
from . import constants
import sys
from .charsetprober import CharSetProber

class CharSetGroupProber(CharSetProber):

    def __init__(self):
        CharSetProber.__init__(self)
        self._mActiveNum = 0
        self._mProbers = []
        self._mBestGuessProber = None
        return

    def reset(self):
        CharSetProber.reset(self)
        self._mActiveNum = 0
        for prober in self._mProbers:
            if prober:
                prober.reset()
                prober.active = True
                self._mActiveNum += 1

        self._mBestGuessProber = None
        return

    def get_charset_name(self):
        if not self._mBestGuessProber:
            self.get_confidence()
            if not self._mBestGuessProber:
                return None
        return self._mBestGuessProber.get_charset_name()

    def feed(self, aBuf):
        for prober in self._mProbers:
            if not prober:
                continue
            if not prober.active:
                continue
            st = prober.feed(aBuf)
            if not st:
                continue
            if st == constants.eFoundIt:
                self._mBestGuessProber = prober
                return self.get_state()
            if st == constants.eNotMe:
                prober.active = False
                self._mActiveNum -= 1
                if self._mActiveNum <= 0:
                    self._mState = constants.eNotMe
                    return self.get_state()

        return self.get_state()

    def get_confidence(self):
        st = self.get_state()
        if st == constants.eFoundIt:
            return 0.99
        else:
            if st == constants.eNotMe:
                return 0.01
            bestConf = 0.0
            self._mBestGuessProber = None
            for prober in self._mProbers:
                if not prober:
                    continue
                if not prober.active:
                    if constants._debug:
                        sys.stderr.write(prober.get_charset_name() + ' not active\n')
                    continue
                cf = prober.get_confidence()
                if constants._debug:
                    sys.stderr.write('%s confidence = %s\n' % (
                     prober.get_charset_name(), cf))
                if bestConf < cf:
                    bestConf = cf
                    self._mBestGuessProber = prober

            if not self._mBestGuessProber:
                return 0.0
            return bestConf