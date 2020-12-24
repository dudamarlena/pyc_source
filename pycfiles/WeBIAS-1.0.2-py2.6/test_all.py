# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_all.py
# Compiled at: 2015-04-13 16:10:47
"""
generic test harness - runs "all" the test_*.py files and
writes the output to TESTS.OUT-{pyversion}

-- frankm@hiwaay.net
"""
import os, sys, string
from time import time
from gnosis.xml.pickle.util import enumParsers
import funcs, gnosis.pyconfig
from funcs import unlink, touch
py = sys.executable
maintests = '\n    bltin\n    basic\n    mixin\n    compat\n    ftypes\n    getstate\n    getinitargs\n    init\n    modnames\n    paranoia\n    mutators\n    rawp_sre\n    re\n    ref\n    selfref\n    unicode\n    bools_ro\n    misc\n'
import string

def echof(filename, line):
    if os.path.isfile(filename):
        f = open(filename, 'a')
    else:
        f = open(filename, 'w')
    f.write(line + '\n')


def pechof(filename, line):
    print line
    if os.path.isfile(filename):
        f = open(filename, 'a')
    else:
        f = open(filename, 'w')
    f.write(line + '\n')


tout = 'TESTS.OUT-%s-%s' % (sys.platform, sys.version.split()[0])
unlink(tout)
touch(tout)
tests = []
for name in string.split(maintests):
    tests.append('test_%s.py' % name)

if gnosis.pyconfig.Have_Generators() and gnosis.pyconfig.Have_Module('itertools'):
    tests.append('test_objectify.py')
else:
    pechof(tout, '*** OMITTING test_objectify.py')
if gnosis.pyconfig.IsLegal_BaseClass('unicode'):
    tests.append('test_badstring.py')
else:
    pechof(tout, '*** OMITTING test_badstring.py')
if gnosis.pyconfig.Have_BoolClass():
    tests.append('test_bools.py')
else:
    pechof(tout, '** OMITTING test_bools.py')
if gnosis.pyconfig.Have_ObjectClass() and gnosis.pyconfig.Have_Slots():
    tests.append('test_subbltin.py')
    tests.append('test_slots.py')
else:
    pechof(tout, '** OMITTING test_subbltin.py')
    pechof(tout, '** OMITTING test_slots.py')
try:
    import gzip
    tests.append('test_4list.py')
except:
    pechof(tout, '** OMITTING test_4list (missing zlib) **')

try:
    import mx.DateTime
    tests.append('test_mx.py')
    tests.append('test_rawp_mx.py')
except:
    pechof(tout, '** OMITTING test_mx.py & test_rawp_mx.py')

try:
    import random
    r = random.Random()
    import pickle
    pickle.dumps(r)
    tests.append('test_setstate.py')
except:
    pechof(tout, '** OMITTING test_setstate.py')

try:
    import Numeric
    tests.append('test_numpy.py')
except:
    pechof(tout, '** OMITTING test_numpy.py')

def check_harness():
    if os.name == 'posix':
        outstr = '2>&1 > harness_check.out'
    elif os.name == 'nt':
        outstr = '2>1> harness_check.out'
    else:
        outstr = '> harness_check.out'
    for good in ['test_pass_1.py', 'test_pass_2.py', 'test_pass_3.py']:
        r = os.system('%s %s %s' % (py, good, outstr))
        if r != 0:
            pechof(tout, '****** Harness test failed ******')
            sys.exit(1)

    print '***************** INGORE EXCEPTIONS BETWEEN THESE LINES *****************'
    for bad in ['test_fail_exit.py', 'test_fail_raise_1.py',
     'test_fail_raise_2.py', 'test_fail_raise_3.py']:
        r = os.system('%s %s %s' % (py, bad, outstr))
        if r == 0:
            pechof(tout, '****** Harness test failed ******')
            sys.exit(1)

    print '***************** INGORE EXCEPTIONS BETWEEN THESE LINES *****************'
    unlink('harness_check.out')


import gnosis.version
pechof(tout, '*** Running all xml.pickle tests, Gnosis Utils %s' % gnosis.version.VSTRING)
check_harness()
pechof(tout, 'Sanity check: OK')
parser_dict = enumParsers()
if parser_dict.has_key('DOM'):
    unlink('USE_SAX')
    unlink('USE_CEXPAT')
    t1 = time()
    for test in tests:
        print 'Running %s' % test
        echof(tout, '** %s %s DOM PARSER **' % (py, test))
        r = os.system('%s %s >> %s' % (py, test, tout))
        if r != 0:
            pechof(tout, '***ERROR***')
            sys.exit(1)

    pechof(tout, '%.1f seconds' % (time() - t1))
else:
    pechof(tout, '** SKIPPING DOM parser **')
if parser_dict.has_key('SAX'):
    touch('USE_SAX')
    t1 = time()
    for test in tests:
        print 'Running %s' % test
        echof(tout, '** %s %s SAX PARSER **' % (py, test))
        r = os.system('%s %s >> %s' % (py, test, tout))
        if r != 0:
            pechof(tout, '***ERROR***')
            sys.exit(1)

    pechof(tout, '%.1f seconds' % (time() - t1))
    unlink('USE_SAX')
else:
    pechof(tout, '** SKIPPING SAX parser **')
if parser_dict.has_key('cEXPAT'):
    touch('USE_CEXPAT')
    t1 = time()
    for test in tests:
        print 'Running %s' % test
        echof(tout, '** %s %s CEXPAT PARSER **' % (py, test))
        r = os.system('%s %s >> %s' % (py, test, tout))
        if r != 0:
            pechof(tout, '***ERROR***')
            sys.exit(1)

    pechof(tout, '%.1f seconds' % (time() - t1))
    unlink('USE_CEXPAT')
else:
    pechof(tout, '** SKIPPING cEXPAT parser **')
pechof(tout, '***** ALL TESTS COMPLETED *****')