# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\tools\debug\corestats.py
# Compiled at: 2016-03-08 18:42:10
import sys, math

class Stats:

    def sum(self, sequence):
        if len(sequence) < 1:
            return
        else:
            return sum(sequence)
            return

    def count(self, sequence):
        return len(sequence)

    def min(self, sequence):
        if len(sequence) < 1:
            return
        else:
            return min(sequence)
            return

    def max(self, sequence):
        if len(sequence) < 1:
            return
        else:
            return max(sequence)
            return

    def mean(self, sequence):
        if len(sequence) < 1:
            return
        else:
            return float(sum(sequence)) / len(sequence)
            return

    def median(self, sequence):
        if len(sequence) < 1:
            return
        else:
            sequence.sort()
            element_idx = float(len(sequence)) / 2
            if element_idx != int(element_idx):
                median1 = sequence[int(math.floor(element_idx))]
                median2 = sequence[int(math.ceil(element_idx))]
                return float(median1 + median2) / 2
            return sequence[int(element_idx)]
            return

    def modeold(self, sequence):
        results = {}
        for item in sequence:
            results.setdefault(item, 0)
            results[item] += 1

        results = sorted(results.iteritems(), key=lambda (k, v): (v, k), reverse=True)
        return results

    def mode(self, sequence):
        """
        Enhanced version of mode(), inspired by statlib/stats.py
        The advantage is that this function (as well as mode) can return several modes at once (so you can see the next most frequent values)
        """
        scores = self.unique(sequence)
        scores.sort()
        freq = {}
        for item in scores:
            freq.setdefault(item, 0)
            freq[item] = sequence.count(item)

        results = sorted(freq.iteritems(), key=lambda (k, v): (v, k), reverse=True)
        return results

    def variance(self, sequence):
        if len(sequence) < 1:
            return
        else:
            avg = self.mean(sequence)
            sdsq = 0
            for i in sequence:
                sdsq += (i - avg) ** 2

            variance = float(sdsq) / (len(sequence) - 1)
            return variance
            return

    def stdev(self, sequence):
        if len(sequence) < 1:
            return
        else:
            variance = self.variance(sequence)
            stdev = float(variance) ** 0.5
            return stdev
            return

    def valueforpercentile(self, sequence, percentile):
        if len(sequence) < 1:
            value = None
        elif percentile > 100:
            sys.stderr.write('ERROR: percentile must be <= 100.  you supplied: %s\n' % percentile)
            value = None
        elif percentile == 100:
            value = max(sequence)
        else:
            element_idx = int(len(sequence) * (float(percentile) / 100.0))
            sequence.sort()
            value = sequence[element_idx]
        return value

    def percentileforvalue(self, sequence, value):
        maxnb = max(sequence)
        minnb = min(sequence)
        if len(sequence) < 1:
            percentile = None
        elif value > maxnb or value < minnb:
            if value > maxnb:
                percentile = 100
            else:
                percentile = 0
        else:
            sequence.sort()
            sequence.reverse()
            element_idx = sequence.index(value)
            element_idx = len(sequence) - element_idx
            percentile = float(element_idx) * 100.0 / len(sequence)
        return percentile

    def unique(self, sequence):
        return list(set(sequence))