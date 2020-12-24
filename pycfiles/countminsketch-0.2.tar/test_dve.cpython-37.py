# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/countmemaybe/test_dve.py
# Compiled at: 2019-12-09 06:49:34
# Size of source mod 2**32: 2567 bytes
__doc__ = "\nBenchmark for the DVE's in this package\n\nmicha gorelick, mynameisfiber@gmail.com\nhttp://micha.gd/\n"
import numpy as np, mmh3
from . import hyperloglog as hll
from . import kminvalues as kmv
try:
    import pylab as py
except ImportError:
    py = None

try:
    from progressbar import ProgressBar, Bar, ETA
except ImportError:
    ProgressBar = None

class DVESet(set):

    def cardinality(self):
        return len(self)


MAX_64BIT_INT = 9223372036854775807
MAX_32BIT_INT = 2147483647
MAX_16BIT_INT = 32767
if __name__ == '__main__':
    max_val = 5 * MAX_16BIT_INT
    chunk_size = max_val // 500
    murmur64 = lambda x: mmh3.hash64(x)[0]
    methods = {'actual':DVESet(), 
     '32bit hll m=256':hll.HyperLogLog(b=8), 
     '32bit kmv k=256':kmv.KMinValues(k=256), 
     '64bit kmv k=256':kmv.KMinValues(k=256,
       hasher=murmur64,
       hasher_max=MAX_64BIT_INT)}
    results = {f:[] for f in methods}
    x = np.arange(1, max_val, chunk_size)
    np.random.seed()
    widgets = ['Processing', Bar(), ETA()]
    _iter = iter(x)
    if ProgressBar:
        p = ProgressBar(maxval=(len(x)), widgets=widgets).start()
        _iter = p(x)
    for i in _iter:
        r = np.random.randint(MAX_16BIT_INT, size=chunk_size)
        for name, m in list(methods.items()):
            m.update(r)
            results[name].append(m.cardinality())

    for r in results:
        results[r] = np.asarray(results[r])

    if py:
        py.subplot(211)
        py.title('Comparison of distinct value estimators')
        for name, result in results.items():
            py.plot(x, result, label=name)

        py.legend(loc=2)
        py.ylabel('Cardinality')
        py.xlim(xmax=(x[(-1)]))
        py.subplot(212)
        py.axhline(0)
    actual = results['actual']
    for name, result in results.items():
        if name == 'actual':
            continue
        theoretical_eerror = methods[name].relative_error() * 100.0
        mean_eerror = (np.abs(actual - result) / actual).mean() * 100.0
        label = '%s (theory: %0.2f%%, mean: %0.2f%%)' % (
         name,
         theoretical_eerror,
         mean_eerror)
        print(label)
        if py:
            py.plot(x, ((actual - result) / actual * 100.0), label=label)

    if py:
        py.ylim((-25.0, 25.0))
        py.legend(loc=8, ncol=2, fontsize='small')
        py.ylabel('Relative error')
        py.xlabel('non-unique set size')
        py.xlim(xmax=(x[(-1)]))
        py.savefig('test_dve.png')