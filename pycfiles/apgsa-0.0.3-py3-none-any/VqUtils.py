# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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