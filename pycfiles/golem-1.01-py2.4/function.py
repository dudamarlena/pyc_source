# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/helpers/function.py
# Compiled at: 2008-08-22 15:02:55
import sys, simplejson, golem

class FitFunction(object):
    __module__ = __name__

    def __init__(self, function, params):
        self.function = function
        self.params = params


class Fit(object):
    __module__ = __name__

    def __init__(self, datasource, xconcepts, yconcepts, xreducer=None, yreducer=None, cache=None):
        self.db = datasource
        self.xconcepts = xconcepts
        self.yconcepts = yconcepts
        if xreducer != None:
            self.xreducer = xreducer
        else:
            self.xreducer = lambda x: float(x)
        if yreducer != None:
            self.yreducer = yreducer
        else:
            self.yreducer = lambda x: float(x)
        self.fitters = {}
        self.data = None
        return

    def getdata(self, cache=None):
        try:
            import numpy
        except NameError:
            try:
                import numpy
            except ImportError:
                print >> sys.stderr, 'You need to have scipy installed to do function fitting'
                sys.exit(1)

        if not self.data:
            if cache == None:
                data_raw = self.db.query(self.xconcepts, self.yconcepts)
            else:
                data_raw = self.db.query_cached(cache, self.xconcepts, self.yconcepts)
            if isinstance(data_raw[0], golem.db.resultlist):
                data = [ golem.db.resultlist([self.xreducer(row[0]), self.yreducer(row[1])], filename=row.filename) for row in data_raw ]
            else:
                data = [ (self.xreducer(x), self.yreducer(y)) for (x, y) in data_raw ]
            self.data = data
        xdata = numpy.array([ a[0] for a in self.data ])
        ydata = numpy.array([ a[1] for a in self.data ])
        return (numpy.array(xdata), numpy.array(ydata))

    def addfunction(self, name, function, params):
        assert name not in self.fitters
        self.fitters[name] = FitFunction(function, params)

    def getresult(self, name):
        return self.fitters[name].result

    def getfndata(self, name):
        fn = self.fitters[name]
        return [ (v[0], -fn.function(fn.result, v[0], 0)) for v in self.data ]

    def __fitsingle(self, function, cache=None):
        try:
            scipy
        except NameError:
            try:
                import scipy
            except ImportError:
                print >> sys.stderr, 'You need to have scipy installed to do function fitting'
                sys.exit(1)

        data = self.getdata(cache=cache)
        (function.result, success) = scipy.optimize.leastsq(function.function, function.params, args=data)
        try:
            assert success == 1
        except AssertionError:
            sys.stderr.write('Warning: Fit %s failed; treat with caution.\n' % function)

    def fit(self, name=None, cache=None):
        if name:
            self.__fitsingle(self.fitters[name], cache=cache)
        else:
            for n in self.fitters:
                self.__fitsingle(self.fitters[n], cache=cache)


def linear(args, x, y):
    (m, c) = args
    return y - (m * x + c)


def quadratic(args, x, y):
    (a, b, c) = args
    return y - (a * x ** 2 + b * x + c)


def cubic(args, x, y):
    (a, b, c, d) = args
    return y - (a * x ** 3 + b * x ** 2 + c * x + d)


def quartic(args, x, y):
    (a, b, c, d, e) = args
    return y - (a * x ** 3 + b * x ** 2 + c * x + d)


def lnlinear(args, x, y):
    try:
        numpy
    except NameError:
        try:
            import numpy
        except ImportError:
            print >> sys.stderr, 'You need to have scipy installed to do function fitting'
            sys.exit(1)

    (m, c) = args
    return y - (m * numpy.log(x) + c)


def powerlaw(args, x, y):
    (a, b, c) = args
    return y - (a * x ** b + c)


def trace(arr):
    for line in arr:
        assert len(line) == len(arr)

    tr = 0
    for i in range(len(arr)):
        tr += arr[i][i]

    return tr


def meantrace(arr):
    return float(trace(arr)) / len(arr)


def mean(arr):
    return float(sum(arr)) / len(arr)