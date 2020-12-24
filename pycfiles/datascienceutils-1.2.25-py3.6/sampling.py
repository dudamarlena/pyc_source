# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/sampling.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 3146 bytes
from random import gauss, triangular, choice, vonmisesvariate, uniform
from statistics import mean
import csv, io, random, sys

def posint(x):
    """Positive integer"""
    return max(0, int(round(x)))


def SC():
    return posint(gauss(15.1, 3) + 3 * triangular(1, 4, 13))


def KT():
    return posint(gauss(10.2, 3) + 3 * triangular(1, 3.5, 9))


def DG():
    return posint(vonmisesvariate(30, 2) * 3.08)


def HB():
    return posint(gauss(6.7, 1.5) if choice((True, False)) else gauss(16.7, 2.5))


def OT():
    return posint(triangular(5, 17, 25) + uniform(0, 30) + gauss(6, 3))


def repeated_hist(rv, bins=10, k=100000):
    """Repeat rv() k times and make a histogram of the results."""
    samples = [rv() for _ in range(k)]
    plt.hist(samples, bins=bins)
    return mean(samples)


def reservoir_sampler(filename, sampleThres):
    sample = []
    with open(filename) as (f):
        for n, line in enumerate(f):
            if n < sampleThres:
                sample.append(line.rstrip())
            else:
                r = random.randint(0, n)
                if r < sampleThres:
                    sample[r] = line.rstrip()

    return sample


def constant_width_file_sampler(filename, sampleSize):
    sample = []
    with io.open(filename, 'rb') as (f):
        f.seek(0, 2)
        filesize = f.tell()
        random_set = sorted(random.sample(range(filesize), sampleSize))
        for i in range(sampleSize):
            f.seek(random_set[i])
            f.readline()
            sample.append(f.readline().rstrip())

    return sample


def file_split(filename, sampleSize=50000, k=20):
    fname, ext = filename.split('.')
    with io.open(filename, 'rb') as (stream):
        header = str(stream.readline())
        headers = header.split(',')
        for i in range(k):
            res = []
            j = 0
            while j < sampleSize:
                line = stream.readline()
                line = str(stream.readline())
                line = line.split(',')
                res.append(line)
                j += 1

            new_fnam = '_'.join([fname, 'sample', str(i) + '.']) + ext
            with open(new_fnam, 'w', newline='') as (fd):
                writer = csv.writer(fd, delimiter=',', quoting=(csv.QUOTE_MINIMAL))
                writer.writerow(headers)
                writer.writerows(res)


def reservoir_sample_stream(filename, sampleSize):
    res = []
    with io.open(filename, 'r') as (stream):
        for i, el in enumerate(stream):
            if i <= sampleSize:
                res.append(el)
            else:
                rand = random.sample(range(i), 1)[0]
                if rand < sampleSize:
                    res[random.sample(range(sampleSize), 1)[0]] = el

    return res


if __name__ == '__main__':
    pass