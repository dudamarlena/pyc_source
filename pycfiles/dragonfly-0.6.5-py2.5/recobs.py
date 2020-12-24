# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\recobs.py
# Compiled at: 2009-04-06 11:19:21
"""
Recognition observer base class
============================================================================

"""
import time
from ..log import get_log
from ..actions.actions import Playback
from ..engines.engine import get_engine

class RecognitionObserver(object):
    _log = get_log('grammar')

    def __init__(self):
        pass

    def __del__(self):
        try:
            self.unregister()
        except Exception, e:
            pass

    def register(self):
        engine = get_engine()
        engine.register_recognition_observer(self)

    def unregister(self):
        engine = get_engine()
        engine.unregister_recognition_observer(self)


class RecognitionHistory(list, RecognitionObserver):

    def __init__(self, length=10):
        list.__init__(self)
        RecognitionObserver.__init__(self)
        self._complete = True
        if length is None or isinstance(length, int) and length >= 1:
            self._length = length
        else:
            raise ValueError('length must be a positive int or None, received %r.' % length)
        return

    @property
    def complete(self):
        """ *False* if phrase-start detected but no recognition yet. """
        return self._complete

    def on_begin(self):
        self._complete = False

    def on_recognition(self, result, words):
        self._complete = True
        self.append(self._recognition_to_item(result, words))
        if self._length:
            while len(self) > self._length:
                self.pop(0)

    def _recognition_to_item(self, result, words):
        return words


class PlaybackHistory(RecognitionHistory):

    def __init__(self, length=10):
        RecognitionHistory.__init__(self, length)

    def _recognition_to_item(self, result, words):
        return (
         words, time.time())

    def __getitem__(self, key):
        result = RecognitionHistory.__getitem__(self, key)
        if len(result) == 1:
            return Playback([(result[0][0], 0)])
        elif len(result) == 2 and isinstance(result[1], float):
            return Playback([(result[0], 0)])
        elif len(result) == 0:
            return Playback(())
        else:
            pairs = [ (w1, t2 - t1) for ((w1, t1), (w2, t2)) in zip(result[:-1], result[1:]) ]
            pairs.append((result[(-1)][0], 0))
            return Playback(pairs)

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))