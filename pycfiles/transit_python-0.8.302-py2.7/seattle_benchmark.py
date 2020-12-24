# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/seattle_benchmark.py
# Compiled at: 2017-12-12 16:52:26
from transit.reader import JsonUnmarshaler
from transit.pyversion import unicode_type
import json, time
from io import StringIO

def run_tests(data):
    datas = StringIO(unicode_type(data))
    t = time.time()
    JsonUnmarshaler().load(datas)
    et = time.time()
    datas = StringIO(unicode_type(data))
    tt = time.time()
    json.load(datas)
    ett = time.time()
    read_delta = (et - t) * 1000.0
    print 'Done: ' + str(read_delta) + '  --  raw JSON in: ' + str((ett - tt) * 1000.0)
    return read_delta


seattle_dir = '../transit-format/examples/0.8/'
means = {}
for jsonfile in [seattle_dir + 'example.json',
 seattle_dir + 'example.verbose.json']:
    data = ''
    with open(jsonfile, 'r') as (fd):
        data = fd.read()
    print '-' * 50
    print 'Running ' + jsonfile
    print '-' * 50
    runs = 200
    deltas = [ run_tests(data) for x in range(runs) ]
    means[jsonfile] = sum(deltas) / runs

for jsonfile, mean in means.items():
    print '\nMean for' + jsonfile + ': ' + str(mean)