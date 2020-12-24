# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/statslib.py
# Compiled at: 2010-10-12 17:55:40
from __future__ import division
from optparse import OptionParser
import sys, re, numpy
from numpy.random import *
import string, re
from rpy2.rpy_classic import *
import rpy2.robjects as robjects
set_default_mode(BASIC_CONVERSION)

def EvaluatePower(errorfile, targetfile, chroms, powerdictfinal):
    from rpy2.rpy_classic import *
    import rpy2.robjects as robjects
    set_default_mode(BASIC_CONVERSION)
    coveragemap = {}
    fileopen = open(errorfile, 'r').readlines()
    for line in fileopen[1:]:
        line = line.rstrip()
        line = line.split()
        chr = line[0]
        offset = line[1]
        chroffset = line[2]
        ref_base = line[3]
        ref_idx = line[4]
        fwdcovg = sum([ int(i) for i in line[5:11] ])
        revcovg = sum([ int(i) for i in line[12:18] ])
        mcratefwd = float(line[11])
        mcraterev = float(line[18])
        coveragemap[(errorfile, chroffset, 'coverage')] = fwdcovg + revcovg
        coveragemap[(errorfile, chroffset, 'coveragefwd')] = fwdcovg
        coveragemap[(errorfile, chroffset, 'coveragerev')] = revcovg
        coveragemap[(errorfile, chroffset, 'mcratefwd')] = mcratefwd
        coveragemap[(errorfile, chroffset, 'mcraterev')] = mcraterev

    exonf = open(targetfile, 'r')
    exonf = exonf.readlines()
    for exonline in exonf[1:]:
        exonline = exonline.split()
        target = exonline[0]
        chr = exonline[1]
        start = int(exonline[2])
        stop = int(exonline[3])
        size = int(exonline[4])
        if start < stop:
            beg = start - 5
            end = stop + 5
        elif stop < start:
            beg = stop - 5
            end = start + 5
        rangelist = r.seq(beg, end, 1)
        for pos in rangelist:
            if 'chr' in chr:
                chroffset = str(chr) + ':' + str(pos)
            else:
                chroffset = 'chr' + str(chr) + ':' + str(pos)
            if (errorfile, chroffset, 'coverage') in coveragemap:
                rejectn = 0
                robjects.globalEnv['reject'] = rejectn
                robjects.globalEnv['covfwd'] = coveragemap[(errorfile, chroffset, 'coveragefwd')]
                robjects.globalEnv['covrev'] = coveragemap[(errorfile, chroffset, 'coveragerev')]
                robjects.globalEnv['mcfwd'] = coveragemap[(errorfile, chroffset, 'mcratefwd')]
                robjects.globalEnv['mcrev'] = coveragemap[(errorfile, chroffset, 'mcraterev')]
                robjects.globalEnv['chromosomes'] = chroms
                num = numpy.sqrt(float(coveragemap[(errorfile, chroffset, 'coveragefwd')] + coveragemap[(errorfile, chroffset, 'coveragerev')]) * numpy.power(float(1) / float(chroms) - (coveragemap[(errorfile, chroffset, 'mcratefwd')] + coveragemap[(errorfile, chroffset, 'mcraterev')]) / float(2), 2)) - 3.09 * numpy.sqrt((coveragemap[(errorfile, chroffset, 'mcratefwd')] + coveragemap[(errorfile, chroffset, 'mcraterev')]) / float(2) * (1 - (coveragemap[(errorfile, chroffset, 'mcratefwd')] + coveragemap[(errorfile, chroffset, 'mcraterev')]) / float(2)))
                den = numpy.sqrt(float(1) / float(chroms) * (1 - float(1) / float(chroms)))
                pz = float(num) / float(den)
                powereval = r.pnorm(pz)[0]
                pfwd = robjects.r['covfwd']
                frev = robjects.r['covrev']
                mcf = robjects.r['mcfwd']
                mcr = robjects.r['mcrev']
                robjects.r.remove(list=robjects.r.objects())
            else:
                powereval = 0
            powerdictfinal[(errorfile, chroffset)] = powereval

    return powerdictfinal


def cval(p, n, m):
    theta = numpy.log(p / (1 - p))
    B2 = -n * p * (1 - p)
    B3 = n * (numpy.exp(theta) * (numpy.exp(theta) - 1) / (1 + numpy.exp(theta)) ^ 3)
    B4 = n * (numpy.exp(theta) * (1 - 4 * numpy.exp(theta) + numpy.exp(2 * theta)) / (1 + numpy.exp(theta)) ^ 4)
    cc = m * (2 * (B2 ^ 2) - B4 + B3 ^ 2 / B2)
    return cc


def calpha(m, n, y):
    phat = 0.5
    sigma2 = phat * (1 - phat) * n
    S = r.sum(y - n * phat ^ 2 - sigma2)[0]
    cc = cval(phat, n, m)
    Z = S / numpy.sqrt(cc)
    return Z


def simm(m, n, p1, p2, w1, w2, niter):
    out = r.rep(0, niter)
    for i in range(1, iter + 1):
        y = r.c(r.binom(m * w1, n, p1)[0], r.binom(m * w2, n, p2)[0], r.binom(m * (1 - w1 - w2), n, 0.5)[0])
        out[i] = calpha(m, n, y)

    return out


def return_fraction_rare_all(chr, start, stop, probweightsdictcases, probweightsdictcontrols, snplist):
    casecnts = 0
    controlcnts = 0
    if 'chr' in chr:
        chr = chr
    else:
        chr = 'chr' + str(chr)
    if start < stop:
        poscurrent = int(start)
        while start <= stop:
            chroffset = chr + ':' + poscurrent
            for i in range(0, len(probweightsdict[chroffset])):
                casecnts += probweightsdictcases[chroffset][i] * i
                controlcnts += probweightsdictcontrols[chroffset][i] * i

            poscurrent += 1

    elif start > stop:
        poscurrent = int(stop)
        while stop <= start:
            chroffset = chr + ':' + poscurrent
            for i in range(0, len(probweightsdict[chroffset])):
                casecnts += probweightsdictcases[chroffset][i]
                controlcnts += probweightsdictcontrol[chroffset][i]

            poscurrent += 1

    statsum = casecnts / (casecnts + controlcnts)
    return statsum


def return_phat(raresnplist, snpsall, caseall):
    casesum = 0
    allsum = 0
    for key in raresnplist.keys():
        casesum += caseall[key]
        allsum += snpsall[key]

    phat = int(casesum) / int(allsum)
    return phat


def return_rare_snplist(snplistall, frequencydict, freqcutoff):
    raredict = {}
    for key in snplistall.keys():
        if frequencydict[key] <= freqcutoff:
            raredict[key] = key

    return raredict


def reparameterize(p):
    p = float(p)
    theta = numpy.log(p / (1 - p))
    return theta


def likelihood_single_variant(nonrefalleles, populationschroms, estimatefreq):
    likelihood_single = r.dbinom(nonrefalleles, populationschroms, estimatefreq)[0]
    return likelihood_single


def reparam_likelihood(nonrefalleles, populationschroms, reparameterize):
    likelihood = numpy.exp(nonrefalleles * reparameterize + populationschroms * numpy.log(exp(reparameterize) / (1 + exp(reparameterize))))
    return likelihood


def B_theta(populationschroms, theta, probweightscases, probweightscontrols):
    Bstat = populationschroms * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))
    return Bstat


def numerator_stat_rare(probweightscases, probweightscontrols, probweightsall, raresnplist, fractionparam):
    stat = 0
    for key in raresnplist.keys():
        for i in range(0, len(probweightscases[key])):
            for j in range(0, len(probweightscontrols[key])):
                stat += probweightscases[key][i] * probweightscontrols[key][j] * (i - (i + j) * fractionparam ^ 2 - (i + j) * (fractionparam * (1 - fractionparam)))

    return stat


def denominator_stat_rare(Bstat, raresnplist, Bstatdotdot, Bstatdotdotdot, Bstatdotdotdotdot):
    rarevariantnum = len(raresnplist.keys())
    cstat = rarevariantnum * (2 * Bstatdotdot ^ 2 - Bstatdotdotdotdot + Bstatdotdotdot ^ 2 / Bstatdotdot)
    return cstat


def return_max(estimaterare):
    maxceil = numpy.ceil(estimaterare)
    return maxceil


def return_rarelist(snplist, min, max):
    rarelist = {}
    for key in snplist.keys():
        if snplist[key] <= max and snplist[key] >= min:
            rarelist[key] = key

    return rarelist


def return_rarelist_region(snprarelist, start, stop, chr, bounds):
    rarelistregion = {}
    if start < stop:
        starttmp = start - bounds
        while starttmp <= stop + bounds:
            chroffsettmp = str(chr) + ':' + str(starttmp)
            if chroffsettmp in snprarelist:
                rarelistregion[chroffsettmp] = chroffsettmp
            starttmp += 1

    elif stop < start:
        starttmp = stop - bounds
        while starttmp <= start + bounds:
            chroffsettmp = str(chr) + ':' + str(starttmmp)
            if chroffsettmp in snprarelist:
                rarelistregion[chroffsettmp] = chroffsettmp
            starttmp += 1

    return rarelistregion


def getme_1mixpinit(Ncases, Ncontrol):
    phat1 = int(Ncases) / (int(Ncases) + int(Ncontrol))
    return phat1


def getme_2mixpinit(Ncases, Ncontrol):
    phat1 = int(Ncases) / (int(Ncases) + int(Ncontrol))
    phat2 = 1.4 * phat1
    return (phat1, phat2)


def getme_3mixpinit(Ncases, Ncontrol):
    phat1 = int(Ncases) / (int(Ncases) + int(Ncontrol))
    phat2 = 1.4 * phat1
    phat3 = 0.7 * phat1
    return (phat1, phat2, phat3)


def return_mixture_number_diagnostics(snpslist, caselist, rarelist, minvariant, maxvariant):
    mixture_number = 1
    return mixture_number


def Calpha_Gen(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    mnum = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                mnum += 1
                cstat += float(fdouble(varcnts[key], casecnts[key], theta)) / float(fsingle(varcnts[key], casecnts[key], theta))

    cstat = cstat / mnum
    return (mnum, variants, cstat)


def Calpha_GenTnew(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    mnum = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                mnum += 1
                cstat += float(TnewRoeder(casecnts[key], varcnts[key], phat))

    cstat = cstat
    return (mnum, cstat)


def Calpha_GenTnewF(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    casesingletons = 0
    allsingletons = 0
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if int(varcnts[key]) == 1:
                    allsingletons += 1
                    if casecnts[key] == 1:
                        casesingletons += 1
                if (
                 str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    mnum = len(m)
    for i in range(minvar, maxvar + 1):
        if int(i) == 1:
            cstat += TnewRoeder(casesingletons, allsingletons, phat)
        elif (
         str(i), 'all') in numberswalk:
            statpre = float(numberswalk[(str(i), 'all')])
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                if (
                 str(i), str(j), 'cases') in numberswalk:
                    statenddenom += float(numberswalk[(str(i), str(j), 'cases')]) / float(numberswalk[(str(i), 'all')]) * TnewRoeder(j, i, phat)
                else:
                    statenddenom += 0

            cstat += statpre * statenddenom

    return (
     mnum, cstat)


def Calpha_GenCnew(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    casesingletons = 0
    allsingletons = 0
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if int(varcnts[key]) == 1:
                    allsingletons += 1
                    if casecnts[key] == 1:
                        casesingletons += 1
                if (
                 str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statdenom = 0
    mnum = len(m)
    for i in range(minvar, maxvar + 1):
        if int(i) == 1:
            for j in range(0, allsingletons + 1):
                statdenom += r.dbinom(j, allsingletons, phat)[0] * CnewRoeder(j, allsingletons, phat)

        elif (
         str(i), 'all') in numberswalk:
            statpre = numberswalk[(str(i), 'all')]
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                statenddenom += r.dbinom(j, i, phat)[0] * CnewRoeder(j, i, phat)

            statdenom += statpre * statenddenom

    statdenom = statdenom
    return (mnum, statdenom)


def EvalWeightSimm(CaseInds, ControlInds, CaseCounts, ControlCounts):
    totalinds = int(CaseInds) + int(ControlInds)
    qhat = float(int(ControlCounts) + 1) / float(2 * ControlInds + 2)
    weightrtn = numpy.sqrt(totalinds * qhat * (1 - qhat))
    return weightrtn


def Calpha_GenTnewWeight(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds, weights):
    numberswalk = {}
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    mnum = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                mnum += 1
                cstat += 1 / float(weights[key]) * float(TnewRoeder(casecnts[key], varcnts[key], phat))

    cstat = cstat
    return (mnum, cstat)


def Calpha_GenCnewWeight(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds, weights):
    numberswalk = {}
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    mnum = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                mnum += 1
                cstatexp = 0
                for k in range(0, int(varcnts[key]) + 1):
                    cstatexp += float(CnewRoeder(k, varcnts[key], phat)) * r.dbinom(k, varcnts[key], phat)[0]

                cstat += 1 / numpy.power(float(weights[key]), 2) * cstatexp

    cstat = cstat
    return (mnum, cstat)


def Calpha_GenDenP(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    cs = []
    variants = 0
    num = []
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                cstat += float(numpy.power(fdouble(varcnts[key], casecnts[key], theta) / float(fsingle(varcnts[key], casecnts[key], theta)), 2))
                cs.append(cstat)
                variants += 1

    return (
     num, variants, cstat)


def Calpha_Gencpy(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    cs = []
    variants = 0
    num = []
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                statnumerator = numpy.exp(theta * (varcnts[key] + casecnts[key])) * numpy.power(1 + numpy.exp(theta), -(varcnts[key] + 2)) * (numpy.exp(2 * theta) * numpy.power(casecnts[key], 2) + numpy.power(varcnts[key] + casecnts[key], 2) + numpy.exp(theta) * (2 * numpy.power(casecnts[key], 2) + varcnts[key] * (2 * casecnts[key] - 1)))
                num.append(statnumerator)
                statdenominator = numpy.exp(casecnts[key] * theta + varcnts[key] * numpy.log(float(numpy.exp(theta)) / float(1 + numpy.exp(theta))))
                cstat += float(statnumerator) / float(statdenominator)
                cs.append(cstat)
                variants += 1

    return (
     num, variants, cstat)


def Calpha_GendenomFinal(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                statnumerator = numpy.exp(theta * (varcnts[key] + casecnts[key])) * numpy.power(1 + numpy.exp(theta), -(varcnts[key] + 2)) * (numpy.exp(2 * theta) * numpy.power(casecnts[key], 2) + numpy.power(varcnts[key] + casecnts[key], 2) + numpy.exp(theta) * (2 * numpy.power(casecnts[key], 2) + varcnts[key] * (2 * casecnts[key] - 1)))
                statdenominator = numpy.exp(casecnts[key] * theta + varcnts[key] * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta))))
                cstat += numpy.power(statnumerator / statdenominator, 2)

    return cstat


def stat1num(i, j, theta):
    stat = numpy.power(numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1))) / numpy.exp(j * theta + i * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))), 1)
    return stat


def fdouble(i, j, theta):
    fpp = numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1)))
    return fpp


def fsingle(i, j, theta):
    fp = numpy.exp(j * theta + i * numpy.log(float(numpy.exp(theta)) / float(1 + numpy.exp(theta))))
    return fp


def TnewRoeder(y, n, phat):
    T = numpy.power(y - n * phat, 2) - n * phat * (1 - phat)
    return T


def CnewRoeder(y, n, phat):
    C = numpy.power(TnewRoeder(y, n, phat), 2)
    return C


def Calpha_Gentry(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    mnum = len(m)
    for i in range(minvar, maxvar + 1):
        if (
         str(i), 'all') in numberswalk:
            statpre = float(numberswalk[(str(i), 'all')]) / mnum
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                if (
                 str(i), str(j), 'cases') in numberswalk:
                    statenddenom += float(numberswalk[(str(i), str(j), 'cases')]) / float(numberswalk[(str(i), 'all')]) * fdouble(i, j, theta) / fsingle(i, j, theta)
                else:
                    statenddenom += 0

            cstat += statpre * statenddenom

    return (
     mnum, cstat)


def Calpha_Genpseudo(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                statnumerator = numpy.exp(theta * (varcnts[key] + casecnts[key])) * numpy.power(1 + numpy.exp(theta), -(varcnts[key] + 2)) * (numpy.exp(2 * theta) * numpy.power(casecnts[key], 2) + numpy.power(varcnts[key] + casecnts[key], 2) + numpy.exp(theta) * (2 * numpy.power(casecnts[key], 2) + varcnts[key] * (2 * casecnts[key] - 1)))
                statdenominator = numpy.exp(casecnts[key] * theta + varcnts[key] * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta))))
                cstat += numpy.power(statnumerator / statdenominator, 2)

    return cstat


def Calpha_Gendenom(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statdenom = 0
    mnum = len(m)
    for i in range(minvar, maxvar + 1):
        if (
         str(i), 'all') in numberswalk:
            statpre = numberswalk[(str(i), 'all')] / mnum
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                if (str(i), str(j), 'cases') in numberswalk:
                    statenddenom += r.dbinom(j, i, phat)[0] * numpy.power(float(fdouble(i, j, theta)) / float(fsingle(i, j, theta)), 2)

            statdenom += statpre * statenddenom

    statdenom = statdenom
    return (mnum, statdenom)


def Calpha_GendenomTheor(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statdenom = 0
    statnum = 0
    mnum = len(m)
    v = []
    d = []
    g = []
    for i in range(minvar, maxvar + 1):
        if (
         str(i), 'all') in numberswalk:
            statpre = numberswalk[(str(i), 'all')] / mnum
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                statenddenom += r.dbinom(j, i, phat)[0] * numpy.power(numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1))) / numpy.exp(j * theta + i * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))), 2)
                v.append(r.dbinom(j, i, phat)[0])
                d.append(numpy.power(numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1))) / numpy.exp(j * theta + i * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))), 2))

            statdenom += statpre * statenddenom
            g.append(statpre)

    statdenom = statdenom
    return statdenom


def Calpha_Gendenom2(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statdenom = 0
    statnum = 0
    mnum = len(m)
    for i in range(minvar, maxvar + 1):
        if (
         str(i), 'all') in numberswalk:
            statpre = numberswalk[(str(i), 'all')] / mnum
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                statenddenom += r.dbinom(j, i, phat)[0] * numpy.power(numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1))) / numpy.exp(j * theta + i * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))), 2)

            statdenom += statpre * statenddenom

    statdenom = statdenom * mnum
    return statdenom


def Calpha_Gendenom3(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    cstat = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statdenom = 0
    statnum = 0
    mnum = len(m)
    for i in range(minvar, maxvar + 1):
        if (
         str(i), 'all') in numberswalk:
            statpre = numberswalk[(str(i), 'all')] / mnum
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                statenddenom += r.dbinom(j, i, phat)[0] * numpy.power(numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1))) / numpy.exp(j * theta + i * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))), 2)

            statdenom += statpre * statenddenom

    statdenom = statdenom * mnum
    return statdenom


def stat_calpha(varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    statnumt = 0
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                statnumt += numpy.exp(theta * (varcnts[key] + casecnts[key])) * numpy.power(1 + numpy.exp(theta), -(varcnts[key] + 2)) * (numpy.exp(2 * theta) * numpy.power(casecnts[key], 2) + numpy.power(casecnts[key] + varcnts[key], 2) + numpy.exp(theta) * (2 * numpy.power(casecnts[key], 2) + varcnts[key] * (2 * casecnts[key] - 1))) / numpy.exp(casecnts[key] * theta + varcnts[key] * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta))))
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statnum = 0
    statdenom = 0
    mnum = len(m)
    for i in range(minvar, maxvar + 1):
        if (str(i), 'all') in numberswalk:
            statpre = numberswalk[(str(i), 'all')] / mnum
            statend = 0
            statenddenom = 0
            for j in range(0, i + 1):
                if (
                 str(i), str(j), 'cases') in numberswalk:
                    statend += numberswalk[(str(i), str(j), 'cases')] / numberswalk[(str(i), 'all')] * (numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1))) / numpy.exp(j * theta + i * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))))
                statenddenom += r.dbinom(j, i, phat)[0] * numpy.power(numpy.exp(theta * (i + j)) * numpy.power(1 + numpy.exp(theta), -(i + 2)) * (numpy.exp(2 * theta) * numpy.power(j, 2) + numpy.power(j + i, 2) + numpy.exp(theta) * (2 * numpy.power(j, 2) + i * (2 * j - 1))) / numpy.exp(j * theta + i * numpy.log(numpy.exp(theta) / (1 + numpy.exp(theta)))), 2)

            statnum += statpre * statend
            statdenom += statpre * statenddenom

    return (
     statnum, statdenom)


def return_EM_paramsfixedneut(probarray, varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statnum = 0
    statdenom = 0
    mnum = len(m)
    Dgradient = []
    for k in probarray:
        Dgrad = 0
        for i in range(minvar, maxvar + 1):
            if (
             str(i), 'all') in numberswalk:
                statpre = numberswalk[(str(i), 'all')] / mnum
                statend = 0
                statenddenom = 0
                for j in range(0, i + 1):
                    if (
                     str(i), str(j), 'cases') in numberswalk:
                        statend += numberswalk[(str(i), str(j), 'cases')] / numberswalk[(str(i), 'all')] * (r.dbinom(j, i, k)[0] / r.dbinom(j, i, phat)[0] - 1)

                Dgrad += statpre * statend
                statnum += statpre * statend
                statdenom += statpre * statenddenom

        Dgradient.append(Dgrad)

    piarray = [
     [
      1], [0.5, 0.5], [0.5, 0.5], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333]]
    probcomps = [[0.5], [0.5, 0.3], [0.5, 0.7], [0.5, 0.3, 0.7]]
    weightsprobvariant = {}
    for step in range(0, 50):
        for key in raresnplist.keys():
            weightsprobvariant[('1', key, '1')] = piarray[0][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[0][0])[0] / r.dbinom(casecnts[key], varcnts[key], probcomps[0][0])[0]

        piblah = 0
        for key in raresnplist.keys():
            piblah += weightsprobvariant[('1', key, '1')]

        piarray[0][0] = 1 / mnum * piblah
        prob1num = 0
        prob1denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('1', key, '1')] * casecnts[key]
            prob1denom += weightsprobvariant[('1', key, '1')] * varcnts[key]

        probcomps[0][0] = 0.5
        for key in raresnplist.keys():
            weightsprobvariant[('2', key, '1b')] = piarray[1][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][0])[0] / (piarray[1][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][0])[0] + piarray[1][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][1])[0])
            weightsprobvariant[('2', key, '2b')] = piarray[1][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][1])[0] / (piarray[1][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][0])[0] + piarray[1][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][1])[0])
            weightsprobvariant[('2', key, '1d')] = piarray[2][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][0])[0] / (piarray[2][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][0])[0] + piarray[2][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][1])[0])
            weightsprobvariant[('2', key, '2d')] = piarray[2][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][1])[0] / (piarray[2][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][0])[0] + piarray[2][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][1])[0])

        piblah1 = 0
        piblah2 = 0
        for key in raresnplist.keys():
            piblah1 += weightsprobvariant[('2', key, '1b')]
            piblah2 += weightsprobvariant[('2', key, '2b')]

        piarray[1][0] = 1 / mnum * piblah1
        piarray[1][1] = 1 / mnum * piblah2
        prob1num = 0
        prob1denom = 0
        prob2num = 0
        prob2denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('2', key, '1b')] * casecnts[key]
            prob1denom += weightsprobvariant[('2', key, '1b')] * varcnts[key]
            prob2num += weightsprobvariant[('2', key, '2b')] * casecnts[key]
            prob2denom += weightsprobvariant[('2', key, '2b')] * varcnts[key]

        probcomps[1][0] = 0.5
        probcomps[1][1] = prob2num / prob2denom
        piblah1 = 0
        piblah2 = 0
        for key in raresnplist.keys():
            piblah1 += weightsprobvariant[('2', key, '1d')]
            piblah2 += weightsprobvariant[('2', key, '2d')]

        piarray[2][0] = 1 / mnum * piblah1
        piarray[2][1] = 1 / mnum * piblah2
        prob1num = 0
        prob1denom = 0
        prob2num = 0
        prob2denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('2', key, '1d')] * casecnts[key]
            prob1denom += weightsprobvariant[('2', key, '1d')] * varcnts[key]
            prob2num += weightsprobvariant[('2', key, '2d')] * casecnts[key]
            prob2denom += weightsprobvariant[('2', key, '2d')] * varcnts[key]

        probcomps[2][0] = 0.5
        probcomps[2][1] = prob2num / prob2denom
        for key in raresnplist.keys():
            weightsprobvariant[('3', key, '1')] = piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] / (piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] + piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] + piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0])
            weightsprobvariant[('3', key, '2')] = piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] / (piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] + piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] + piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0])
            weightsprobvariant[('3', key, '3')] = piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0] / (piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] + piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] + piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0])

        piblah1 = 0
        piblah2 = 0
        piblah3 = 0
        for key in raresnplist.keys():
            piblah1 += weightsprobvariant[('3', key, '1')]
            piblah2 += weightsprobvariant[('3', key, '2')]
            piblah3 += weightsprobvariant[('3', key, '3')]

        piarray[3][0] = 1 / mnum * piblah1
        piarray[3][1] = 1 / mnum * piblah2
        piarray[3][2] = 1 / mnum * piblah3
        prob1num = 0
        prob1denom = 0
        prob2num = 0
        prob2denom = 0
        prob3num = 0
        prob3denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('3', key, '1')] * casecnts[key]
            prob1denom += weightsprobvariant[('3', key, '1')] * varcnts[key]
            prob2num += weightsprobvariant[('3', key, '2')] * casecnts[key]
            prob2denom += weightsprobvariant[('3', key, '2')] * varcnts[key]
            prob3num += weightsprobvariant[('3', key, '3')] * casecnts[key]
            prob3denom += weightsprobvariant[('3', key, '3')] * varcnts[key]

        probcomps[3][0] = 0.5
        probcomps[3][1] = prob2num / prob2denom
        probcomps[3][2] = prob3num / prob3denom

    return (
     weightsprobvariant, probcomps, piarray)


def return_EM_params(probarray, varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statnum = 0
    statdenom = 0
    mnum = len(m)
    Dgradient = []
    for k in probarray:
        Dgrad = 0
        for i in range(minvar, maxvar + 1):
            if (
             str(i), 'all') in numberswalk:
                statpre = numberswalk[(str(i), 'all')] / mnum
                statend = 0
                statenddenom = 0
                for j in range(0, i + 1):
                    if (
                     str(i), str(j), 'cases') in numberswalk:
                        statend += numberswalk[(str(i), str(j), 'cases')] / numberswalk[(str(i), 'all')] * (r.dbinom(j, i, k)[0] / r.dbinom(j, i, phat)[0] - 1)

                Dgrad += statpre * statend
                statnum += statpre * statend
                statdenom += statpre * statenddenom

        Dgradient.append(Dgrad)

    piarray = [
     [
      1], [0.5, 0.5], [0.5, 0.5], [0.3333333333333333, 0.3333333333333333, 0.3333333333333333]]
    probcomps = [[0.5], [0.5, 0.3], [0.5, 0.7], [0.5, 0.3, 0.7]]
    weightsprobvariant = {}
    for step in range(0, 50):
        for key in raresnplist.keys():
            weightsprobvariant[('1', key, '1')] = piarray[0][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[0][0])[0] / r.dbinom(casecnts[key], varcnts[key], probcomps[0][0])[0]

        piblah = 0
        for key in raresnplist.keys():
            piblah += weightsprobvariant[('1', key, '1')]

        piarray[0][0] = 1 / mnum * piblah
        prob1num = 0
        prob1denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('1', key, '1')] * casecnts[key]
            prob1denom += weightsprobvariant[('1', key, '1')] * varcnts[key]

        probcomps[0][0] = prob1num / prob1denom
        for key in raresnplist.keys():
            weightsprobvariant[('2', key, '1b')] = piarray[1][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][0])[0] / (piarray[1][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][0])[0] + piarray[1][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][1])[0])
            weightsprobvariant[('2', key, '2b')] = piarray[1][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][1])[0] / (piarray[1][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][0])[0] + piarray[1][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[1][1])[0])
            weightsprobvariant[('2', key, '1d')] = piarray[2][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][0])[0] / (piarray[2][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][0])[0] + piarray[2][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][1])[0])
            weightsprobvariant[('2', key, '2d')] = piarray[2][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][1])[0] / (piarray[2][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][0])[0] + piarray[2][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[2][1])[0])

        piblah1 = 0
        piblah2 = 0
        for key in raresnplist.keys():
            piblah1 += weightsprobvariant[('2', key, '1b')]
            piblah2 += weightsprobvariant[('2', key, '2b')]

        piarray[1][0] = 1 / mnum * piblah1
        piarray[1][1] = 1 / mnum * piblah2
        prob1num = 0
        prob1denom = 0
        prob2num = 0
        prob2denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('2', key, '1b')] * casecnts[key]
            prob1denom += weightsprobvariant[('2', key, '1b')] * varcnts[key]
            prob2num += weightsprobvariant[('2', key, '2b')] * casecnts[key]
            prob2denom += weightsprobvariant[('2', key, '2b')] * varcnts[key]

        probcomps[1][0] = prob1num / prob1denom
        probcomps[1][1] = prob2num / prob2denom
        piblah1 = 0
        piblah2 = 0
        for key in raresnplist.keys():
            piblah1 += weightsprobvariant[('2', key, '1d')]
            piblah2 += weightsprobvariant[('2', key, '2d')]

        piarray[2][0] = 1 / mnum * piblah1
        piarray[2][1] = 1 / mnum * piblah2
        prob1num = 0
        prob1denom = 0
        prob2num = 0
        prob2denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('2', key, '1d')] * casecnts[key]
            prob1denom += weightsprobvariant[('2', key, '1d')] * varcnts[key]
            prob2num += weightsprobvariant[('2', key, '2d')] * casecnts[key]
            prob2denom += weightsprobvariant[('2', key, '2d')] * varcnts[key]

        probcomps[2][0] = prob1num / prob1denom
        probcomps[2][1] = prob2num / prob2denom
        for key in raresnplist.keys():
            weightsprobvariant[('3', key, '1')] = piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] / (piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] + piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] + piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0])
            weightsprobvariant[('3', key, '2')] = piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] / (piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] + piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] + piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0])
            weightsprobvariant[('3', key, '3')] = piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0] / (piarray[3][0] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][0])[0] + piarray[3][1] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][1])[0] + piarray[3][2] * r.dbinom(casecnts[key], varcnts[key], probcomps[3][2])[0])

        piblah1 = 0
        piblah2 = 0
        piblah3 = 0
        for key in raresnplist.keys():
            piblah1 += weightsprobvariant[('3', key, '1')]
            piblah2 += weightsprobvariant[('3', key, '2')]
            piblah3 += weightsprobvariant[('3', key, '3')]

        piarray[3][0] = 1 / mnum * piblah1
        piarray[3][1] = 1 / mnum * piblah2
        piarray[3][2] = 1 / mnum * piblah3
        prob1num = 0
        prob1denom = 0
        prob2num = 0
        prob2denom = 0
        prob3num = 0
        prob3denom = 0
        for key in raresnplist.keys():
            prob1num += weightsprobvariant[('3', key, '1')] * casecnts[key]
            prob1denom += weightsprobvariant[('3', key, '1')] * varcnts[key]
            prob2num += weightsprobvariant[('3', key, '2')] * casecnts[key]
            prob2denom += weightsprobvariant[('3', key, '2')] * varcnts[key]
            prob3num += weightsprobvariant[('3', key, '3')] * casecnts[key]
            prob3denom += weightsprobvariant[('3', key, '3')] * varcnts[key]

        probcomps[3][0] = prob1num / prob1denom
        probcomps[3][1] = prob2num / prob2denom
        probcomps[3][2] = prob3num / prob3denom

    return (
     weightsprobvariant, probcomps, piarray)


def return_gradient(probarray, varcnts, casecnts, chr, start, end, raresnplist, minvar, maxvar, theta, phat, bounds, probcomps, piarray):
    numberswalk = {}
    m = []
    start = int(start)
    end = int(end)
    theta = float(theta)
    phat = float(phat)
    for key in raresnplist.keys():
        (i, j) = key.split(':')
        pos = int(j)
        if i == chr:
            if start <= end and pos >= start - bounds and pos <= end + bounds or start >= end and pos <= start + bounds and pos >= end - bounds:
                m.append(key)
                if (str(varcnts[key]), 'all') not in numberswalk:
                    numberswalk[(str(varcnts[key]), 'all')] = 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1
                else:
                    numberswalk[(str(varcnts[key]), 'all')] += 1
                    if (str(varcnts[key]), str(casecnts[key]), 'cases') not in numberswalk:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] = 1
                    else:
                        numberswalk[(str(varcnts[key]), str(casecnts[key]), 'cases')] += 1

    statnum = 0
    statdenom = 0
    mnum = len(m)
    Dgradient1 = []
    Dgradient2a = []
    Dgradient2b = []
    Dgradient3 = []
    for k in probarray:
        Dgrad1 = 0
        Dgrad2a = 0
        Dgrad2b = 0
        Dgrad3 = 0
        for i in range(minvar, maxvar + 1):
            if (
             str(i), 'all') in numberswalk:
                statpre = numberswalk[(str(i), 'all')] / mnum
                statend1 = 0
                statend2a = 0
                statend2b = 0
                statend3 = 0
                statenddenom = 0
                for j in range(0, i + 1):
                    if (
                     str(i), str(j), 'cases') in numberswalk:
                        mnm = numberswalk[(str(i), str(j), 'cases')] / numberswalk[(str(i), 'all')]
                        statend1 += mnm * (r.dbinom(j, i, k)[0] / (piarray[0][0] * r.dbinom(j, i, probcomps[0][0])[0]) - 1)
                        statend2a += mnm * (r.dbinom(j, i, k)[0] / (piarray[1][0] * r.dbinom(j, i, probcomps[1][0])[0] + piarray[1][1] * r.dbinom(j, i, probcomps[1][1])[0]) - 1)
                        statend2b += mnm * (r.dbinom(j, i, k)[0] / (piarray[2][0] * r.dbinom(j, i, probcomps[2][0])[0] + piarray[2][1] * r.dbinom(j, i, probcomps[2][1])[0]) - 1)
                        statend3 += mnm * (r.dbinom(j, i, k)[0] / (piarray[3][0] * r.dbinom(j, i, probcomps[3][0])[0] + piarray[3][1] * r.dbinom(j, i, probcomps[3][1])[0] + piarray[3][2] * r.dbinom(j, i, probcomps[3][2])[0]) - 1)

                Dgrad1 += statpre * statend1
                Dgrad2a += statpre * statend2a
                Dgrad2b += statpre * statend2b
                Dgrad3 += statpre * statend3

        Dgradient1.append(Dgrad1)
        Dgradient2a.append(Dgrad2a)
        Dgradient2b.append(Dgrad2b)
        Dgradient3.append(Dgrad3)

    return (
     Dgradient1, Dgradient2a, Dgradient2b, Dgradient3)


def ChooseKGradDiag(pval, alpha, gradientarray1, gradientarray2a, gradientarray2b, gradientarray3, probarray, probcompvec):
    K = '1'
    if pval <= alpha:
        if len([ k for k in gradientarray2a if k > 0.6 ]) == 0 and probcompvec[1][1] < probcompvec[1][0]:
            K = '2a'
        elif len([ k for k in gradientarray2b if k > 0.6 ]) == 0 and probcompvec[2][1] > probcompvec[2][0]:
            K = '2b'
        elif len([ k for k in gradientarray3 if k > 0.6 ]) == 0:
            K = '3'
        else:
            K = 'nan'
    else:
        K = '1'
    return K