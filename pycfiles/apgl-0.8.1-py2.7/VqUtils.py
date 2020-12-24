# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/util/VqUtils.py
# Compiled at: 2011-08-07 12:01:30


class VqUtils(object):

    @staticmethod
    def whiten(obs):
        """
          care about null standard deviation
        """
        mean = obs.mean(axis=0)
        stdDev = obs.std(axis=0)
        stdDev[stdDev == 0] = 1
        return (obs - mean) / stdDev