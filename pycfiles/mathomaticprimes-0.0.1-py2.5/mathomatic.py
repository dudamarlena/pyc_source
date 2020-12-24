# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mathomatic/mathomatic.py
# Compiled at: 2010-01-16 04:31:59
import os
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array
from soaplib.serializers.binary import Attachment

class MathomaticPrimes(SimpleWSGISoapApp):

    def __init__(self):
        SimpleWSGISoapApp.__init__(self)
        self.limit = 10000000

    @soapmethod(Integer, Integer, _returns=Array(Integer))
    def getprimes(self, lowerbound, upperbound):
        if upperbound > self.limit:
            print 'Limit boundary to %i' % self.limit
            upperbound = self.limit
        print 'calculate primes from %i to %i' % (lowerbound, upperbound)
        primestr = os.popen('matho-primes %i %i' % (lowerbound, upperbound)).read()
        primelines = primestr.split('\n')
        primes = []
        for line in primelines:
            if line:
                primes.append(int(line))

        return primes


if __name__ == '__main__':
    mp = MathomaticPrimes()
    print mp.getprimes(0, 1200)