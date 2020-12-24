# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grs/twseno.py
# Compiled at: 2011-10-05 02:42:28
import csv
_CSVFILEPATH = __name__.split('.')[(-2)]

class twseno(object):

    def __init__(self):
        self.allstockno = self.importcsv()
        self.ind_code = self.industry_code()
        self.indcomps = self.loadindcomps()

    def importcsv(self):
        f = csv.reader(open('./%s/stock_no.csv' % _CSVFILEPATH, 'r'))
        re = {}
        for i in f:
            try:
                re[int(i[0])] = str(i[1])
            except:
                if i[0] == 'UPDATE':
                    self.last_update = str(i[1])

        return re

    def industry_code(self):
        f = csv.reader(open('./%s/industry_code.csv' % _CSVFILEPATH, 'r'))
        re = {}
        for i in f:
            re[int(i[0])] = i[1]

        return re

    def loadindcomps(self):
        f = csv.reader(open('./%s/stock_no.csv' % _CSVFILEPATH, 'r'))
        re = {}
        for i in f:
            try:
                re[int(i[2])].append(i[0])
            except:
                try:
                    re[int(i[2])] = [
                     i[0]]
                except:
                    pass

        return re

    @property
    def allstock(self):
        """ Return all stock no and name by dict. """
        return self.allstockno

    def search(self, q):
        """ Search. """
        import re
        pattern = re.compile('%s' % q)
        result = {}
        for i in self.allstockno:
            b = re.search(pattern, self.allstockno[i])
            try:
                b.group()
                result[i] = self.allstockno[i]
            except:
                pass

        return result

    def searchbyno(self, q):
        """ Search by no. """
        import re
        pattern = re.compile('%s' % q[0:2])
        result = {}
        for i in self.allstockno:
            b = re.search(pattern, i)
            try:
                b.group()
                result[i] = self.allstockno[i]
            except:
                pass

        return result