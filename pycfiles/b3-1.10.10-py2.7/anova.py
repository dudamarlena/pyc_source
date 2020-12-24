# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\tools\debug\statlib\anova.py
# Compiled at: 2016-03-08 18:42:10
import numpy as N
from b3.tools.debug.statlib.pstat import *
from b3.tools.debug.statlib.stats import *
from numpy import linalg as LA
import math

def aanova(data, effects=[
 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']):
    """
    Prints the results of single-variable between- and within-subject ANOVA
    designs.  The function can only handle univariate ANOVAs with a single
    random factor.  The random factor is coded in column 0 of the input
    list/array (see below) and the measured variable is coded in the last
    column of the input list/array. The following were used as references
    when writing the code:

    Maxwell, SE, Delaney HD (1990)  Designing Experiments and Analyzing
        Data, Wadsworth: Belmont, CA.
    Lindman, HR (1992) Analysis of Variance in Experimental Design,
        Springer-Verlag: New York.

    TO DO:  Increase Current Max Of 10 Levels Per W/I-Subject Factor
            Consolidate Between-Subj Analyses For Between And Within/Between
            Front-end for different input data-array shapes/organization
            Axe mess of 'global' statements (particularly for Drestrict fcns)

    Usage:   anova(data,                         data = |Stat format
                   effects=['A','B','C','D','E','F','G','H','I','J','K'])

    Note: |Stat format is as follows ... one datum per row, first element of
    row is the subject identifier, followed by all within/between subject
    variable designators, and the measured data point as the last element in the
    row.  Thus, [1, 'short', 'drugY', 2, 14.7] represents subject 1 when measured
    in the short / drugY / 2 condition, and subject 1 gave a measured value of
    14.7 in this combination of conditions.  Thus, all input lists are '2D'
    lists-of-lists.
    """
    global Bbetweens
    global Bscols
    global Bwithins
    global Bwonly_sources
    global D
    global DM
    global DN
    global Nallsources
    global Nblevels
    global Nfactors
    global Nlevels
    global Nsubjects
    global SSlist
    global SSsources
    global alleffects
    global alleffsources
    global alluniqueslist
    outputlist = []
    SSbtw = []
    SSbtwsources = []
    SSwb = []
    SSwbsources = []
    alleffects = []
    alleffsources = []
    SSlist = []
    SSsources = []
    print
    variables = 1
    if type(data) != type([]):
        data = data.tolist()
    alluniqueslist = [
     0] * (len(data[0]) - variables)
    Nlevels = [0] * (len(data[0]) - variables)
    for column in range(len(Nlevels)):
        alluniqueslist[column] = pstat.unique(pstat.colex(data, column))
        Nlevels[column] = len(alluniqueslist[column])

    Ncells = N.multiply.reduce(Nlevels[1:])
    Nfactors = len(Nlevels[1:])
    Nallsources = 2 ** (Nfactors + 1)
    Nsubjects = len(alluniqueslist[0])
    Bwithins = findwithin(data)
    Bbetweens = ~Bwithins & Nallsources - 1 - 1
    Wcolumns = makelist(Bwithins, Nfactors + 1)
    Wscols = [0] + Wcolumns
    Bscols = makelist(Bbetweens + 1, Nfactors + 1)
    Nwifactors = len(Wscols) - 1
    Nwlevels = N.take(N.array(Nlevels), Wscols)
    Nbtwfactors = len(Bscols) - 1
    Nblevels = N.take(N.array(Nlevels), Bscols)
    Nwsources = 2 ** Nwifactors - 1
    Nbsources = Nallsources - Nwsources
    M = pstat.collapse(data, Bscols, -1, None, None, mean)
    Marray = N.zeros(Nblevels[1:], 'f')
    Narray = N.zeros(Nblevels[1:], 'f')
    for row in M:
        idx = []
        for i in range(len(row[:-1])):
            idx.append(alluniqueslist[Bscols[i]].index(row[i]))

        idx = idx[1:]
        Marray[idx] = Marray[idx] + row[(-1)]
        Narray[idx] = Narray[idx] + 1

    Marray = Marray / Narray
    coefflist = [
     [
      [
       1]],
     [
      [
       -1, 1]],
     [
      [
       -1, 0, 1], [1, -2, 1]],
     [
      [
       -3, -1, 1, 3], [1, -1, -1, 1], [-1, 3, -3, 1]],
     [
      [
       -2, -1, 0, 1, 2], [2, -1, -2, -1, 2], [-1, 2, 0, -2, 1], [1, -4, 6, -4, 1]],
     [
      [
       -5, -3, -1, 1, 3, 5], [5, -1, -4, -4, -1, 5], [-5, 7, 4, -4, -7, 5],
      [
       1, -3, 2, 2, -3, 1], [-1, 5, -10, 10, -5, 1]],
     [
      [
       -3, -2, -1, 0, 1, 2, 3], [5, 0, -3, -4, -3, 0, 5], [-1, 1, 1, 0, -1, -1, 1],
      [
       3, -7, 1, 6, 1, -7, 3], [-1, 4, -5, 0, 5, -4, 1], [1, -6, 15, -20, 15, -6, 1]],
     [
      [
       -7, -5, -3, -1, 1, 3, 5, 7], [7, 1, -3, -5, -5, -3, 1, 7],
      [
       -7, 5, 7, 3, -3, -7, -5, 7], [7, -13, -3, 9, 9, -3, -13, 7],
      [
       -7, 23, -17, -15, 15, 17, -23, 7], [1, -5, 9, -5, -5, 9, -5, 1],
      [
       -1, 7, -21, 35, -35, 21, -7, 1]],
     [
      [
       -4, -3, -2, -1, 0, 1, 2, 3, 4], [28, 7, -8, -17, -20, -17, -8, 7, 28],
      [
       -14, 7, 13, 9, 0, -9, -13, -7, 14], [14, -21, -11, 9, 18, 9, -11, -21, 14],
      [
       -4, 11, -4, -9, 0, 9, 4, -11, 4], [4, -17, 22, 1, -20, 1, 22, -17, 4],
      [
       -1, 6, -14, 14, 0, -14, 14, -6, 1], [1, -8, 28, -56, 70, -56, 28, -8, 1]],
     [
      [
       -9, -7, -5, -3, -1, 1, 3, 5, 7, 9], [6, 2, -1, -3, -4, -4, -3, -1, 2, 6],
      [
       -42, 14, 35, 31, 12, -12, -31, -35, -14, 42],
      [
       18, -22, -17, 3, 18, 18, 3, -17, -22, 18],
      [
       -6, 14, -1, -11, -6, 6, 11, 1, -14, 6], [3, -11, 10, 6, -8, -8, 6, 10, -11, 3],
      [
       9, -47, 86, -42, -56, 56, 42, -86, 47, -9],
      [
       1, -7, 20, -28, 14, 14, -28, 20, -7, 1],
      [
       -1, 9, -36, 84, -126, 126, -84, 36, -9, 1]]]
    dindex = 0
    NDs = [
     0] * Nwsources
    for source in range(Nwsources):
        if subset(source, Bwithins):
            NDs[dindex] = numlevels(source, Nlevels)
            dindex = dindex + 1

    cdata = pstat.collapse(data, range(Nfactors + 1), -1, None, None, mean)
    dummyval = -1
    datavals = pstat.colex(data, -1)
    while dummyval in datavals:
        dummyval = dummyval - 1

    DA = N.ones(Nlevels, 'f') * dummyval
    if len(Bscols) == 1:
        subjslots = N.ones((Nsubjects, 1))
    else:
        subjslots = N.zeros(Nblevels)
    for i in range(len(data)):
        idx = []
        for j in range(Nfactors + 1):
            new = alluniqueslist[j].index(data[i][j])
            idx.append(new)

        DA[idx] = data[i][(-1)]
        btwidx = N.take(idx, N.array(Bscols))
        subjslots[btwidx] = 1

    dcount = -1
    Bwsources = []
    Bwonly_sources = []
    D = N.zeros(Nwsources, N.PyObject)
    DM = [0] * Nwsources
    DN = [0] * Nwsources
    for source in range(3, Nallsources, 2):
        if source - 1 & Bwithins != 0:
            Bwsources.append(source - 1)
        if subset(source - 1, Bwithins):
            dcount = dcount + 1
            Bwonly_sources.append(source - 1)
            dwsc = 1.0 * DA
            Bnonsource = Nallsources - 1 & ~source
            Bwscols = makebin(Wscols)
            Bwithinnonsource = Bnonsource & Bwscols
            Lwithinnonsource = makelist(Bwithinnonsource, Nfactors + 1)
            for i in range(len(Lwithinnonsource) - 1, -1, -1):
                dwsc = amean(dwsc, Lwithinnonsource[i])

            mns = dwsc
            Bwithinsource = source & Bwscols
            Lwithinsourcecol = makelist(Bwithinsource, Nfactors + 1)
            Lsourceandbtws = makelist(source | Bbetweens, Nfactors + 1)
            if Lwithinnonsource != []:
                Lwithinsourcecol = map(Lsourceandbtws.index, Lwithinsourcecol)
            dvarshape = N.array(N.take(mns.shape, Lwithinsourcecol[1:])) - 1
            idxarray = N.indices(dvarshape)
            newshape = N.array([idxarray.shape[0],
             N.multiply.reduce(idxarray.shape[1:])])
            indxlist = N.swapaxes(N.reshape(idxarray, newshape), 0, 1)
            for i in range(len(indxlist)):
                coeffmatrix = N.ones(mns.shape, N.Float)
                Wsourcecol = makelist(Bwscols & source, Nfactors + 1)
                for wfactor in range(len(Lwithinsourcecol[1:])):
                    coeffmatrix = N.swapaxes(coeffmatrix, 0, Lwithinsourcecol[(wfactor + 1)])
                    nlevels = coeffmatrix.shape[0]
                    try:
                        nextcoeff = coefflist[(nlevels - 1)][indxlist[(i, wfactor)]]
                    except IndexError:
                        raise IndexError, 'anova() can only handle up to 10 levels on a within-subject factors'

                    for j in range(nlevels):
                        coeffmatrix[j] = coeffmatrix[j] * nextcoeff[j]

                    coeffmatrix = N.swapaxes(coeffmatrix, 0, Lwithinsourcecol[(wfactor + 1)])

                scratch = coeffmatrix * mns
                for j in range(len(coeffmatrix.shape[1:])):
                    scratch = N.add.reduce(scratch, 1)

                if len(scratch.shape) == 1:
                    scratch.shape = list(scratch.shape) + [1]
                try:
                    tmp = D[dcount].shape
                    D[dcount] = pstat.aabut(D[dcount], scratch)
                except AttributeError:
                    D[dcount] = scratch

            variables = D[dcount].shape[1]
            tidx = range(1, len(subjslots.shape)) + [0]
            tsubjslots = N.transpose(subjslots, tidx)
            DMarray = N.zeros(list(tsubjslots.shape[0:-1]) + [
             variables], 'f')
            DNarray = N.zeros(list(tsubjslots.shape[0:-1]) + [
             variables], 'f')
            idx = [0] * len(tsubjslots.shape[0:-1])
            idx[0] = -1
            loopcap = N.array(tsubjslots.shape[0:-1]) - 1
            while incr(idx, loopcap) != -1:
                DNarray[idx] = float(asum(tsubjslots[idx]))
                thismean = N.add.reduce(tsubjslots[idx] * N.transpose(D[dcount]), 1) / DNarray[idx]
                thismean = N.array(thismean, N.PyObject)
                DMarray[idx] = thismean

            DM[dcount] = DMarray
            DN[dcount] = DNarray
        if Bscols[1:] != []:
            BNs = pstat.colex([Nlevels], Bscols[1:])
        else:
            BNs = [
             1]
        if source - 1 & Bwithins == 0:
            sourcecols = makelist(source - 1, Nfactors + 1)
            Lsource = makelist(Nallsources - 1 & Bbetweens, Nfactors + 1)
            btwcols = map(Bscols.index, Lsource)
            hn = aharmonicmean(Narray, -1)
            SSw = 0.0
            idxlist = pstat.unique(pstat.colex(M, btwcols))
            for row in M:
                idx = []
                for i in range(len(row[:-1])):
                    idx.append(alluniqueslist[Bscols[i]].index(row[i]))

                idx = idx[1:]
                newval = row[(-1)] - Marray[idx]
                SSw = SSw + newval ** 2

            Lsource = makelist(source - 1, Nfactors + 1)
            btwsourcecols = (N.array(map(Bscols.index, Lsource)) - 1).tolist()
            Bbtwnonsourcedims = ~source & Bbetweens
            Lbtwnonsourcedims = makelist(Bbtwnonsourcedims, Nfactors + 1)
            btwnonsourcedims = (N.array(map(Bscols.index, Lbtwnonsourcedims)) - 1).tolist()
            sourceMarray = amean(Marray, btwnonsourcedims, 1)
            sourceNarray = aharmonicmean(Narray, btwnonsourcedims, 1)
            ga = asum(sourceMarray * sourceNarray / asum(sourceNarray))
            ga = N.reshape(ga, N.ones(len(Marray.shape)))
            if source == Nallsources - 1:
                sourceNarray = aharmonicmean(Narray)
            sub_effects = 1.0 * ga
            for subsource in range(3, source, 2):
                if subset(subsource - 1, source - 1):
                    sub_effects = sub_effects + alleffects[alleffsources.index(subsource)]

            effect = sourceMarray - sub_effects
            alleffects.append(effect)
            alleffsources.append(source)
            SS = asum(effect ** 2 * sourceNarray * N.multiply.reduce(N.take(Marray.shape, btwnonsourcedims)))
            SSlist.append(SS)
            SSsources.append(source)
            collapsed = pstat.collapse(M, btwcols, -1, None, len, mean)
            contrastmns = pstat.collapse(collapsed, btwsourcecols, -2, sterr, len, mean)
            contrastns = pstat.collapse(collapsed, btwsourcecols, -1, None, None, N.sum)
            contrasthns = pstat.collapse(collapsed, btwsourcecols, -1, None, None, harmonicmean)
            sourceNs = pstat.colex([Nlevels], makelist(source - 1, Nfactors + 1))
            dfnum = N.multiply.reduce(N.ravel(N.array(sourceNs) - 1))
            dfden = Nsubjects - N.multiply.reduce(N.ravel(BNs))
            MS = SS / dfnum
            MSw = SSw / dfden
            if MSw != 0:
                f = MS / MSw
            else:
                f = 0
            if f >= 0:
                prob = fprob(dfnum, dfden, f)
            else:
                prob = 1.0
        else:
            sourcewithins = source - 1 & Bwithins
            workD = D[Bwonly_sources.index(sourcewithins)]
            if len(workD.shape) == 1:
                workD = workD[:, N.NewAxis]
            if len(subjslots.shape) == 1:
                subjslots = subjslots[:, N.NewAxis]
            ef = Dfull_model(workD, subjslots)
            if subset(source - 1, Bwithins):
                er = Drestrict_mean(workD, subjslots)
            else:
                er = Drestrict_source(workD, subjslots, source) + ef
            SSw = LA.determinant(ef)
            SS = LA.determinant(er) - SSw
            sourceNs = pstat.colex([Nlevels], makelist(source, Nfactors + 1))
            dfnum = N.multiply.reduce(N.ravel(N.array(sourceNs) - 1)[1:])
            if subset(source - 1, Bwithins):
                dfden = Nsubjects - N.multiply.reduce(N.ravel(BNs)) - dfnum + 1
                MS = SS / dfnum
                MSw = SSw / dfden
                if MSw != 0:
                    f = MS / MSw
                else:
                    f = 0
                if f >= 0:
                    prob = fprob(dfnum, dfden, f)
                else:
                    prob = 1.0
            else:
                try:
                    p = workD.shape[1]
                except IndexError:
                    p = 1

                k = N.multiply.reduce(N.ravel(BNs))
                m = Nsubjects - 1 - (p + k) / 2.0
                d_en = float(p ** 2 + (k - 1) ** 2 - 5)
                if d_en == 0.0:
                    s = 1.0
                else:
                    s = math.sqrt(((p * (k - 1)) ** 2 - 4) / d_en)
                dfden = m * s - dfnum / 2.0 + 1
                if LA.determinant(er) != 0:
                    lmbda = LA.determinant(ef) / LA.determinant(er)
                    W = math.pow(lmbda, 1.0 / s)
                    f = (1.0 - W) / W * (dfden / dfnum)
                else:
                    f = 0
                if f >= 0:
                    prob = fprob(dfnum, dfden, f)
                else:
                    prob = 1.0
                suffix = ''
                if prob < 0.001:
                    suffix = '***'
                else:
                    if prob < 0.01:
                        suffix = '**'
                    elif prob < 0.05:
                        suffix = '*'
                    adjsourcecols = N.array(makelist(source - 1, Nfactors + 1)) - 1
                    thiseffect = ''
                    for col in adjsourcecols:
                        if len(adjsourcecols) > 1:
                            thiseffect = thiseffect + effects[col][0]
                        else:
                            thiseffect = thiseffect + effects[col]

                outputlist = outputlist + [[thiseffect, round4(SS), dfnum, round4(SS / float(dfnum)), round4(f), round4(prob), suffix]] + [[thiseffect + '/w', round4(SSw), dfden, round4(SSw / float(dfden)), '', '', '']] + [['\n']]
                Lsource = makelist(source - 1, Nfactors + 1)
                collapsed = pstat.collapse(cdata, Lsource, -1, sterr, len, mean)
                prefixcols = range(len(collapsed[0][:-3]))
                outlist = pstat.colex(collapsed, prefixcols)
                eff = []
                for col in Lsource:
                    eff.append(effects[(col - 1)])

            for item in ['MEAN', 'STERR', 'N']:
                eff.append(item)

        outlist = pstat.abut(outlist, map(round4, pstat.colex(collapsed, -3)), map(round4, pstat.colex(collapsed, -2)), map(round4, pstat.colex(collapsed, -1)))
        outlist = [eff] + outlist
        pstat.printcc(outlist)
        print

    print
    title = [
     [
      'FACTORS: ', 'RANDOM'] + effects[:Nfactors]]
    title = title + [['LEVELS:  '] + Nlevels]
    facttypes = ['BETWEEN'] * Nfactors
    for i in range(len(Wscols[1:])):
        facttypes[Wscols[(i + 1)] - 1] = 'WITHIN'

    title = title + [['TYPE:    ', 'RANDOM'] + facttypes]
    pstat.printcc(title)
    print
    title = [
     [
      'Effect', 'SS', 'DF', 'MS', 'F', 'p', 'sig']] + ['dashes']
    outputlist = title + outputlist
    pstat.printcc(outputlist)
    return


def Dfull_model(workd, subjslots):
    """
        RESTRICTS NOTHING (i.e., FULL MODEL CALCULATION).  Subtracts D-variable
   cell-mean for each between-subj group and then calculates the SS array.
        """
    workd = subtr_cellmeans(workd, subjslots)
    sserr = multivar_SScalc(workd)
    return sserr


def Drestrict_mean(workd, subjslots):
    """
        RESTRICTS GRAND MEAN.  Subtracts D-variable cell-mean for each between-
   subj group, and then adds back each D-variable's grand mean.
        """
    errors = subtr_cellmeans(workd, subjslots)
    grandDmeans = amean(workd, 0, 1)
    errors = errors + N.transpose(grandDmeans)
    sserr = multivar_SScalc(errors)
    return sserr


def Drestrict_source(workd, subjslots, source):
    """
   Calculates error for a given model on array workd.  Subjslots is an
   array of 1s and 0s corresponding to whether or not the subject is a
   member of that between-subjects variable combo.  source is the code
   for the type of model to calculate.  source=-1 means no restriction;
   source=0 means to restrict workd's grand mean; source>0 means to
   restrict the columns of the main data array, DA, specified (in binary)
   by the source-value.

   Usage:   Derrorcalc(workd,subjslots,source)  source:-1=nothing, 0=mean
   Returns: SS array for multivariate F calculation
   """
    if source > 0:
        sourcewithins = source - 1 & Bwithins
        sourcebetweens = source - 1 & Bbetweens
        dindex = Bwonly_sources.index(sourcewithins)
        all_cellmeans = N.transpose(DM[dindex], [-1] + range(0, len(DM[dindex].shape) - 1))
        all_cellns = N.transpose(DN[dindex], [-1] + range(0, len(DN[dindex].shape) - 1))
        hn = aharmonicmean(all_cellns)
        levels = D[dindex].shape[1]
        SSm = N.zeros((levels, levels), 'f')
        tworkd = N.transpose(D[dindex])
        RSw = N.zeros((levels, levels), 'f')
        RSinter = N.zeros((levels, levels), N.PyObject)
        for i in range(levels):
            for j in range(i, levels):
                RSw[(i, j)] = RSw[(j, i)] = N.sum(tworkd[i] * tworkd[j])
                cross = all_cellmeans[i] * all_cellmeans[j]
                multfirst = asum(cross * all_cellns[i])
                RSinter[(i, j)] = RSinter[(j, i)] = N.asarray(multfirst)
                SSm[(i, j)] = SSm[(j, i)] = amean(all_cellmeans[i]) * amean(all_cellmeans[j]) * len(all_cellmeans[i]) * hn

        SSw = RSw - RSinter
        Lsource = makelist(sourcebetweens, Nfactors + 1)
        btwsourcecols = (N.array(map(Bscols.index, Lsource)) - 1).tolist()
        Bbtwnonsourcedims = ~source & Bbetweens
        Lbtwnonsourcedims = makelist(Bbtwnonsourcedims, Nfactors + 1)
        btwnonsourcedims = (N.array(map(Bscols.index, Lbtwnonsourcedims)) - 1).tolist()
        sourceDMarray = DM[dindex] * 1.0
        for dim in btwnonsourcedims:
            if dim == len(DM[dindex].shape) - 1:
                raise ValueError, "Crashing ... shouldn't ever collapse ACROSS variables"
            sourceDMarray = amean(sourceDMarray, dim, 1)

        sourceDNarray = aharmonicmean(DN[dindex], btwnonsourcedims, 1)
        variableNs = asum(sourceDNarray, range(len(sourceDMarray.shape) - 1))
        ga = asum(sourceDMarray * sourceDNarray / variableNs, range(len(sourceDMarray.shape) - 1), 1)
        if source == Nallsources - 1:
            sourceDNarray = aharmonicmean(DN[dindex], range(len(sourceDMarray.shape) - 1))
        sub_effects = ga * 1.0
        for subsource in range(3, source - 2, 2):
            subsourcebtw = subsource - 1 & Bbetweens
            if propersubset(subsource - 1, source - 1) and subsource - 1 & Bwithins == source - 1 & Bwithins and subsource - 1 != source - 1 & Bwithins:
                sub_effects = sub_effects + alleffects[alleffsources.index(subsource)]

        effect = sourceDMarray - sub_effects
        alleffects.append(effect)
        alleffsources.append(source)
        SS = N.zeros((levels, levels), 'f')
        SS = asum(effect ** 2 * sourceDNarray * N.multiply.reduce(N.take(DM[dindex].shape, btwnonsourcedims)), range(len(sourceDMarray.shape) - 1))
        SSlist.append(SS)
        SSsources.append(source)
        return SS


def multivar_SScalc(workd):
    if len(workd.shape) == 1:
        levels = 1
    else:
        levels = workd.shape[0]
    sserr = N.zeros((levels, levels), 'f')
    for i in range(levels):
        for j in range(i, levels):
            ssval = N.add.reduce(workd[i] * workd[j])
            sserr[(i, j)] = ssval
            sserr[(j, i)] = ssval

    return sserr


def subtr_cellmeans(workd, subjslots):
    """
   Subtract all cell means when within-subjects factors are present ...
   i.e., calculate full-model using a D-variable.
   """
    sourcedims = makelist(Bbetweens, Nfactors + 1)
    transidx = range(len(subjslots.shape))[1:] + [0]
    tsubjslots = N.transpose(subjslots, transidx)
    tworkd = N.transpose(workd)
    errors = 1.0 * tworkd
    if len(sourcedims) == 0:
        idx = [
         -1]
        loopcap = [0]
    if len(sourcedims) != 0:
        btwsourcedims = map(Bscols.index, sourcedims)
        idx = [0] * len(btwsourcedims)
        idx[0] = -1
        loopcap = N.take(N.array(Nlevels), sourcedims) - 1
    while incr(idx, loopcap) != -1:
        mask = tsubjslots[idx]
        thisgroup = tworkd * mask[N.NewAxis, :]
        groupmns = amean(N.compress(mask, thisgroup), 1)
        errors = errors - N.multiply.outer(groupmns, mask)

    return errors


def F_value_wilks_lambda(ER, EF, dfnum, dfden, a, b):
    """
   Calculation of Wilks lambda F-statistic for multivarite data, per
   Maxwell & Delaney p.657.

   Usage:   F_value_wilks_lambda(ER,EF,dfnum,dfden,a,b)
   """
    if type(ER) in [IntType, FloatType]:
        ER = N.array([[ER]])
    if type(EF) in [IntType, FloatType]:
        EF = N.array([[EF]])
    lmbda = LA.determinant(EF) / LA.determinant(ER)
    if (a - 1) ** 2 + (b - 1) ** 2 == 5:
        q = 1
    else:
        q = math.sqrt(((a - 1) ** 2 * (b - 1) ** 2 - 2) / ((a - 1) ** 2 + (b - 1) ** 2 - 5))
    n_um = (1 - lmbda ** (1.0 / q)) * (a - 1) * (b - 1)
    d_en = lmbda ** (1.0 / q) / (m * q - 0.5 * (a - 1) * (b - 1) + 1)
    return n_um / d_en


def member(factor, source):
    return 1 << factor & source != 0


def setsize(source):
    size = 0
    for bit in source:
        if bit == 1:
            size = size + 1

    return size


def subset(a, b):
    return a & b == a


def propersubset(a, b):
    sub = a & b == a
    if a == b:
        sub = 0
    return sub


def numlevels(source, Nlevels):
    for i in range(30):
        if 1 << i >= source:
            break

    levelcount = 1
    for j in range(i):
        if subset(1 << j, source):
            levelcount = levelcount * Nlevels[j] - 1

    return levelcount


def numbitson(a):
    numon = 0
    while a > 0:
        numon = numon + a % 2
        a = a >> 1

    return numon


def makebin(sourcelist):
    outbin = 0
    for item in sourcelist:
        outbin = outbin + 2 ** item

    return outbin


def makelist(source, ncols):
    levellist = []
    for j in range(ncols):
        if subset(1 << j, source):
            levellist.append(j)

    return levellist


def round4(num):
    try:
        return round(num, 4)
    except:
        return 'N/A'