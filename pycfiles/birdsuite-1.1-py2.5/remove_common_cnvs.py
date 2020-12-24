# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plink_pipeline/remove_common_cnvs.py
# Compiled at: 2009-01-27 09:41:59
import sys
print sys.path
sys.exit(1)
import numpy
from numpy import *
import scipy, pylab

def computeMax(stringVals):
    max = -inf
    for s in stringVals:
        f = float(s)
        if f > max:
            max = f

    return max


overlap_dist = float(sys.argv[3])
overlap_pct = float(sys.argv[4])
commoncnps = pylab.load(sys.argv[5], skiprows=1)
cnpstotoss = zeros(shape(commoncnps)[0])
freqfile = open(sys.argv[6], 'r')
freqfile.readline()
for line in freqfile:
    values = line.split()
    if computeMax(values[4:]) < 0.02:
        cnpstotoss[where(commoncnps[:, 0] == int(values[0]))] = 1

freqfile.close()
commoncnps = commoncnps[cnpstotoss == 0, 1:4]
cnvfile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')
for line in cnvfile:
    values = line.split()
    chrcnps = commoncnps[commoncnps[:, 0] == float(values[3]), :]
    bigstart = chrcnps[:, 1].clip(float(values[4]), Inf)
    smallstart = chrcnps[:, 1].clip(0, float(values[4]))
    bigend = chrcnps[:, 2].clip(float(values[5]), Inf)
    smallend = chrcnps[:, 2].clip(0, float(values[5]))
    overlap = smallend - bigstart
    union = float(values[5]) - float(values[4])
    startdiff = chrcnps[:, 1] - float(values[4])
    enddiff = float(values[5]) - chrcnps[:, 2]
    if not ((overlap / union > overlap_pct) & (startdiff < overlap_dist) & (enddiff < overlap_dist)).any():
        print >> outfile, line,