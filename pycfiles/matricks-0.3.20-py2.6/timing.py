# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/matricks/timing.py
# Compiled at: 2011-02-09 21:10:28
import sys
sys.path.append('..')
import re, matricks, time, random

def timing(dataset, output=None, rsep='\n', fsep='\t', cvt=None, null=None, skiprows=1, skipcols=1, aggfn=None):
    if cvt is None:
        cvt = --- This code section failed: ---

 L.  16         0  LOAD_FAST             0  'x'
                3  LOAD_CONST               0
                6  BINARY_SUBSCR    
                7  LOAD_CONST               '+-0123456789.'
               10  COMPARE_OP            6  in
               13  JUMP_IF_FALSE        11  'to 27'
             16_0  THEN                     27
               16  POP_TOP          
               17  LOAD_GLOBAL           0  'float'
               20  LOAD_FAST             0  'x'
               23  CALL_FUNCTION_1       1  None
               26  RETURN_END_IF_LAMBDA
               27  POP_TOP          
               28  LOAD_FAST             0  'x'
               31  LOAD_DEREF            0  'null'
               34  COMPARE_OP            2  ==
               37  JUMP_IF_FALSE         5  'to 45'
             40_0  THEN                     45
               40  POP_TOP          
               41  LOAD_CONST               None
               44  RETURN_END_IF_LAMBDA
               45  POP_TOP          
               46  LOAD_FAST             0  'x'
               49  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    ctpat = re.compile('([\\w\\_\\+\\-]+)(\\.\\w+)?')
    ctfn = lambda x: ctpat.match(x).group(1)
    t0 = time.time()
    csl = matricks.Matricks(dataset, rsep=rsep, fsep=fsep, skiprows=skiprows, skipcols=skipcols, cvt=cvt)
    t1 = time.time()
    print 'loaded', len(csl), 'records in', t1 - t0, 'sec'
    if aggfn:
        t0 = time.time()
        csl_ct = csl.aggregate(aggfn)
        t1 = time.time()
        print 'aggregated', len(csl.getLabels()), 'samples into', len(csl_ct.getLabels()), 'in', t1 - t0, 'sec'
    t0 = time.time()
    for i in range(10):
        x = [ y for y in csl ][random.randint(0, len(csl))]
        p = csl.pearson(x[0])

    t1 = time.time()
    print '10 random profiles chosen and ppm correlated in', t1 - t0, 'sec'
    if output is None:
        output = sys.stdout
    t0 = time.time()
    csl.dump(output)
    t1 = time.time()
    print len(csl), 'written to', output, 'in', t1 - t0, 'sec'
    return