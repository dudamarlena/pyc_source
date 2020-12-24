# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Work/Python/workplace/pypsd/pypsd\profile_test.py
# Compiled at: 2009-07-12 16:35:38
import cProfile, pstats
from psdfile import PSDFile
import os, psyco
from time import clock

def main():

    def doTest(filename, methodname):
        print '%s:' % methodname
        inf = './../samples/%s' % filename
        cProfile.run('%s()' % methodname, inf)
        p = pstats.Stats(inf)
        p.strip_dirs()
        p.sort_stats('cumulative').print_stats(10)

    parseTest()


def parseTest():
    a = clock()
    psd = PSDFile('./../samples/text_test.psd')
    psd.parse()
    b = clock()
    print b - a
    psd.save('./../samples/')


if __name__ == '__main__':
    main()