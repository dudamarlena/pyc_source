# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/MFEprimer/chilli/TmDeltaG.py
# Compiled at: 2017-07-16 05:34:29
from __future__ import division
Author = 'Wubin Qu <quwubin@gmail.com>, BIRM, China'
Date = '2010-3-2'
License = 'GPL v3'
Version = '1.0'
import math, Seq, ThermodynamicsParameters as TP

def calDeltaHS(qseq, sseq):
    """ Calculate deltaH and deltaS """
    init_begin = 'init%s%s' % (qseq[0], sseq[0])
    init_end = 'init%s%s' % (qseq[(-1)], sseq[(-1)])
    if init_begin in TP.dH_full and init_end in TP.dH_full:
        deltaH = TP.dH_full[init_begin] + TP.dH_full[init_end]
        deltaS = TP.dS_full[init_begin] + TP.dS_full[init_end]
    else:
        deltaH = 0
        deltaS = 0
    for i in xrange(len(qseq) - 1):
        dinuc = '%s%s' % (qseq[i:i + 2], sseq[i:i + 2])
        if dinuc in TP.dH_full and dinuc in TP.dS_full:
            deltaH += TP.dH_full[dinuc]
            deltaS += TP.dS_full[dinuc]

    return (
     deltaH, deltaS)


def calDeltaG(qseq, sseq, mono_conc=50, diva_conc=1.5, dntp_conc=0.25, deltaH=None, deltaS=None):
    """ Calculate the free Gibbs energy """
    mono_conc = float(mono_conc)
    diva_conc = float(diva_conc)
    dntp_conc = float(dntp_conc)
    if not (deltaH and deltaS):
        deltaH, deltaS = calDeltaHS(qseq, sseq)
    tao = 310.15
    mono_conc = mono_conc + divalent2monovalent(diva_conc, dntp_conc)
    mono_conc = mono_conc / 1000
    deltaS_adjust = deltaS + 0.368 * (len(sseq) - 1) * math.log(mono_conc, math.e)
    deltaG = (deltaH * 1000 - tao * deltaS_adjust) / 1000
    return deltaG


def calTm(qseq, sseq, mono_conc=50, diva_conc=1.5, oligo_conc=50, dntp_conc=0.25, deltaH=None, deltaS=None):
    """ Calculate Tm value of amplicon"""
    mono_conc = float(mono_conc)
    diva_conc = float(diva_conc)
    oligo_conc = float(oligo_conc)
    dntp_conc = float(dntp_conc)
    if not (deltaH and deltaS):
        deltaH, deltaS = calDeltaHS(qseq, sseq)
    deltaH = deltaH * 1000
    oligo_conc = oligo_conc / 1000000000
    mono_conc = mono_conc + divalent2monovalent(diva_conc, dntp_conc)
    mono_conc = mono_conc / 1000
    deltaS = deltaS + 0.368 * (len(qseq) - 1) * math.log(mono_conc, math.e)
    Tm = deltaH / (deltaS + 1.987 * math.log(oligo_conc / 4, math.e)) - 273.15
    return Tm


def divalent2monovalent(divalent, dntp):
    """Divalent to monovalent"""
    if divalent == 0:
        dntp = 0
    if divalent < 0 or dntp < 0:
        print >> sys.stderr, 'Error: divalent2monovalent, please contact Wubin Qu <quwubin@gmail.com>.'
        exit()
    if divalent < dntp:
        divalent = dntp
    return 120 * math.sqrt(divalent - dntp)


class Cal:

    def __init__(self, qseq, sseq, mono_conc=50, diva_conc=1.5, oligo_conc=50, dntp_conc=0.25):
        deltaH, deltaS = calDeltaHS(qseq, sseq)
        self.Tm = calTm(qseq, sseq, mono_conc=mono_conc, diva_conc=diva_conc, oligo_conc=oligo_conc, dntp_conc=dntp_conc, deltaH=deltaH, deltaS=deltaS)
        self.DeltaG = calDeltaG(qseq, sseq, mono_conc=mono_conc, diva_conc=diva_conc, dntp_conc=dntp_conc, deltaH=deltaH, deltaS=deltaS)


def main():
    qseq = 'TATACTTT'
    sseq = Seq.complement(qseq)
    qseq = 'GGACTGACG'
    sseq = 'CCTGGCTGC'
    mono = 50
    diva = 1.5
    oligo = 50
    dntp = 0.25
    seq = Cal(qseq, sseq, mono_conc=50, diva_conc=1.5, oligo_conc=50, dntp_conc=0.25)
    print 'Tm: ', seq.Tm
    print 'DeltaG: ', seq.DeltaG


if __name__ == '__main__':
    main()