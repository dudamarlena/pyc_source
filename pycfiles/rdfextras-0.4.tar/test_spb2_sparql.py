# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/test/test_spb2_sparql.py
# Compiled at: 2012-07-18 11:22:33
import os, sys, platform
from nose.exc import SkipTest
if platform.system() == 'Java':
    raise SkipTest('Skipping, too taxing for Jython')
import unittest, logging, time
from glob import glob
import rdflib
from rdflib.graph import Graph
try:
    maketrans = str.maketrans
except AttributeError:
    from string import maketrans

log = logging.getLogger(__name__)
DEBUG = False
EVALUATE = True
DEBUG_PARSE = False
STORE = 'IOMemory'
configString = ''

def create_graph(n3data):
    g = Graph()
    g.parse(location=n3data, format='n3')
    return g


fn = os.path.dirname(os.path.abspath(__file__)) + '/sp2b/10kdata.n3'
g = create_graph(fn)
skiptests = [
 'q01',
 'q02',
 'q03a',
 'q03b',
 'q03c',
 'q04',
 'q05a',
 'q05b',
 'q06',
 'q07',
 'q08',
 'q09',
 'q10',
 'q11',
 'q12a',
 'q12b',
 'q12c']

class Envelope(object):

    def __init__(self, n, f):
        self.name = n
        self.file = f

    def __repr__(self):
        return self.name


def generictest(e):
    """Documentation"""
    global g
    if e.skip:
        raise SkipTest('long SPARQL test %s skipped' % e.name)
    q = open(e.file).read()
    t1 = time.time()
    result = g.query(q, processor='sparql')
    t2 = time.time()
    if getattr(result, 'result', False):
        if not result.result:

            def stab(result):
                if result.askAnswer[0]:
                    return [True]
                []

            if result.askAnswer:
                res = stab(result)
            else:
                res = []
        else:
            res = result.result
    else:
        res = []
    print 'Q%s\t%s\t%fs' % (e.file[9:-7], len(res), t2 - t1)


def test_cases():
    from copy import deepcopy
    here_dir = os.path.dirname(os.path.abspath(__file__))
    if 'sp2b' not in here_dir:
        os.chdir(here_dir + '/sp2b')
    for idx, testFile in enumerate(glob('queries/*.sparql')):
        if idx in (5, 6):
            continue
        gname = testFile.split('queries/')[1][:-7].translate(maketrans('-/', '__'))
        e = Envelope(gname, testFile)
        if gname in skiptests:
            e.skip = True
        else:
            e.skip = False
        if sys.version_info[:2] == (2, 4):
            import pickle
            gjt = pickle.dumps(generictest)
            gt = pickle.loads(gjt)
        else:
            gt = deepcopy(generictest)
        gt.__doc__ = testFile
        yield (gt, e)


if __name__ == '__main__':
    for f, e in test_cases():
        try:
            f(e)
        except SkipTest:
            pass