# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tescal/detcal/cut.py
# Compiled at: 2018-09-12 19:18:31
# Size of source mod 2**32: 19726 bytes
import numpy as np, random
from tescal.fitting import ofamp
from tescal.utils import removeoutliers, iterstat

def symmetrizedist(vals):
    """
    Function to symmetrize a distribution about zero. Useful for if the distribution of some value
    centers around a nonzero value, but should center around zero. An example of this would be when
    most of the measured slopes are nonzero, but we want the slopes with zero values (e.g. lots of 
    muon tails, which we want to cut out). To do this, the algorithm randomly chooses points in a histogram
    to cut out until the histogram is symmetric about zero.
    
    Parameters
    ----------
        vals : ndarray
            A 1-d array of the values that will be symmetrized.
            
    Returns
    -------
        czeromeanslope : ndarray
            A boolean mask of the values that should be kept.
    """
    nvals = len(vals)
    valsmean, valsstd = iterstat(vals, cut=2, precision=10000.0)[:-1]
    if valsmean > 0.0:
        vals = vals
    else:
        histupr = max(vals)
        histlwr = -histupr
        histbins = int(np.sqrt(nvals))
        if np.mod(histbins, 2) == 0:
            histbins += 1
        if histupr > 0:
            hist_num, bin_edges = np.histogram(vals, bins=histbins, range=(histlwr, histupr))
            if len(hist_num) > 2:
                czeromeanvals = np.zeros(nvals, dtype=bool)
                czeromeanvals[vals > bin_edges[(histbins // 2)]] = True
                for ibin in range(histbins // 2, histbins - 1):
                    cvalsinbin = np.logical_and(vals < bin_edges[(histbins - ibin - 1)], vals >= bin_edges[(histbins - ibin - 2)])
                    ntracesinthisbin = hist_num[(histbins - ibin - 2)]
                    ntracesinoppobin = hist_num[(ibin + 1)]
                    ntracestoremove = ntracesinthisbin - ntracesinoppobin
                    if ntracestoremove > 0.0:
                        cvalsinbininds = np.where(cvalsinbin)[0]
                        crandcut = np.random.choice(cvalsinbininds, ntracestoremove, replace=False)
                        cvalsinbin[crandcut] = False
                    czeromeanvals += cvalsinbin

            else:
                czeromeanvals = np.ones(nvals, dtype=bool)
        else:
            czeromeanvals = np.ones(nvals, dtype=bool)
    return czeromeanvals


def pileupcut(traces, fs=625000.0, outlieralgo='removeoutliers', nsig=2, removemeans=False):
    """
    Function to automatically cut out outliers of the optimum filter amplitudes of the inputted traces.
    
    Parameters
    ----------
        traces : ndarray
            2-dimensional array of traces to do cuts on
        fs : float, optional
            Digitization rate that the data was taken at
        outlieralgo : string, optional
            Which outlier algorithm to use. If set to "removeoutliers", uses the removeoutliers algorithm that
            removes data based on the skewness of the dataset. If set to "iterstat", uses the iterstat algorithm
            to remove data based on being outside a certain number of standard deviations from the mean
        nsig : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the optimum filter amplitudes. Default is 2.
        removemeans : boolean, optional
            Boolean flag on if the mean of each trace should be removed before doing the optimal filter (True) or
            if the means should not be removed (False). This is useful for dIdV traces, when we want to cut out
            pulses that have smaller amplitude than the dIdV overshoot. Default is False.
            
    Returns
    -------
        cpileup : ndarray
            Boolean array giving which indices to keep or throw out based on the outlier algorithm
            
    """
    nbin = len(traces[0])
    ind_trigger = round(nbin / 2)
    time = 1.0 / fs * (np.arange(1, nbin + 1) - ind_trigger)
    lgc_b0 = time < 0.0
    tau_risepulse = 1e-05
    tau_fallpulse = 0.0001
    dummytemplate = (1.0 - np.exp(-time / tau_risepulse)) * np.exp(-time / tau_fallpulse)
    dummytemplate[lgc_b0] = 0.0
    dummytemplate = dummytemplate / max(dummytemplate)
    dummypsd = np.ones(nbin)
    if removemeans:
        mean = np.mean(traces, axis=1)
        traces -= mean[:, np.newaxis]
    else:
        amps = np.zeros(len(traces))
        for itrace in range(0, len(traces)):
            amps[itrace] = ofamp(traces[itrace], dummytemplate, dummypsd, fs)[0]

        if outlieralgo == 'removeoutliers':
            cpileup = removeoutliers(abs(amps))
        else:
            if outlieralgo == 'iterstat':
                cpileup = iterstat((abs(amps)), cut=nsig, precision=10000.0)[2]
            else:
                raise ValueErrror('Unknown outlier algorithm inputted.')
    return cpileup


def slopecut(traces, fs=625000.0, outlieralgo='removeoutliers', nsig=2, is_didv=False, symmetrizeflag=False, sgfreq=100.0):
    """
    Function to automatically cut out outliers of the slopes of the inputted traces. Includes a routine that 
    attempts to symmetrize the distribution of slopes around zero, which is useful when the majority of traces 
    have a slope.
    
    Parameters
    ----------
        traces : ndarray
            2-dimensional array of traces to do cuts on
        fs : float, optional
            Digitization rate that the data was taken at
        outlieralgo : string, optional
            Which outlier algorithm to use. If set to "removeoutliers", uses the removeoutliers algorithm that
            removes data based on the skewness of the dataset. If set to "iterstat", uses the iterstat algorithm
            to remove data based on being outside a certain number of standard deviations from the mean
        nsig : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the slopes. Default is 2.
        is_didv : bool, optional
            Boolean flag on whether or not the trace is a dIdV curve
        symmetrizeflag : bool, optional
            Flag for whether or not the slopes should be forced to have an average value of zero.
            Should be used if most of the traces have a slope
        sgfreq : float, optional
            If is_didv is True, then the sgfreq is used to know where the flat parts of the traces should be
            
    Returns
    -------
        cslope : ndarray
            Boolean array giving which indices to keep or throw out based on the outlier algorithm
            
    """
    nbin = len(traces[0])
    tracebegin = np.zeros(len(traces))
    traceend = np.zeros(len(traces))
    nperiods = np.floor(nbin / fs * sgfreq)
    binsinperiod = fs / sgfreq
    if is_didv:
        if nperiods > 1:
            sloperangebegin = range(int(binsinperiod / 4), int(3 * binsinperiod / 8))
            sloperangeend = range(int((nperiods - 1.0) * binsinperiod + binsinperiod / 4), int((nperiods - 1.0) * binsinperiod + 3 * binsinperiod / 8))
        else:
            sloperangebegin = range(int(binsinperiod / 4), int(5 * binsinperiod / 16))
            sloperangeend = range(int(5 * binsinperiod / 16), int(3 * binsinperiod / 8))
    else:
        sloperangebegin = range(0, int(nbin / 10))
        sloperangeend = range(int(9 * nbin / 10), nbin)
    tracebegin = np.mean((traces[:, sloperangebegin]), axis=1)
    traceend = np.mean((traces[:, sloperangeend]), axis=1)
    slopes = traceend - tracebegin
    if symmetrizeflag:
        czeromeanslope = symmetrizedist(slopes)
        czeromeanslopeinds = np.where(czeromeanslope)[0]
    else:
        czeromeanslopeinds = np.arange(len(traces))
    if outlieralgo == 'removeoutliers':
        cslope = removeoutliers(slopes[czeromeanslopeinds])
    else:
        if outlieralgo == 'iterstat':
            cslope = iterstat((slopes[czeromeanslopeinds]), cut=nsig, precision=10000.0)[2]
        else:
            raise ValueErrror('Unknown outlier algorithm inputted.')
    cslopeinds = czeromeanslopeinds[cslope]
    cslopetot = np.ones((len(traces)), dtype=bool)
    cslopetot[cslopeinds] = True
    return cslopetot


def baselinecut(traces, fs=625000.0, outlieralgo='removeoutliers', nsig=2, is_didv=False, sgfreq=100.0):
    """
    Function to automatically cut out outliers of the baselines of the inputted traces.
    
    Parameters
    ----------
        traces : ndarray
            2-dimensional array of traces to do cuts on
        fs : float, optional
            Digitization rate that the data was taken at
        outlieralgo : string, optional
            Which outlier algorithm to use. If set to "removeoutliers", uses the removeoutliers algorithm that
            removes data based on the skewness of the dataset. If set to "iterstat", uses the iterstat algorithm
            to remove data based on being outside a certain number of standard deviations from the mean
        nsig : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the baselines. Default is 2.
        is_didv : bool, optional
            Boolean flag on whether or not the trace is a dIdV curve
        sgfreq : float, optional
            If is_didv is True, then the sgfreq is used to know where the flat parts of the traces should be
            
    Returns
    -------
        cbaseline : ndarray
            Boolean array giving which indices to keep or throw out based on the outlier algorithm
            
    """
    nbin = len(traces[0])
    tracebegin = np.zeros(len(traces))
    nperiods = np.floor(nbin / fs * sgfreq)
    binsinperiod = fs / sgfreq
    if is_didv:
        if nperiods > 1:
            sloperangebegin = range(int(binsinperiod / 4), int(3 * binsinperiod / 8))
        else:
            sloperangebegin = range(int(binsinperiod / 4), int(5 * binsinperiod / 16))
    else:
        sloperangebegin = range(0, int(nbin / 10))
    tracebegin = np.mean((traces[:, sloperangebegin]), axis=1)
    if outlieralgo == 'removeoutliers':
        cbaseline = removeoutliers(tracebegin)
    else:
        if outlieralgo == 'iterstat':
            cbaseline = iterstat(tracebegin, cut=nsig, precision=10000.0)[2]
        else:
            raise ValueErrror('Unknown outlier algorithm inputted.')
    return cbaseline


def chi2cut(traces, fs=625000.0, outlieralgo='iterstat', nsig=2):
    """
    Function to automatically cut out outliers of the baselines of the inputted traces.
    
    Parameters
    ----------
        traces : ndarray
            2-dimensional array of traces to do cuts on
        fs : float, optional
            Digitization rate that the data was taken at
        outlieralgo : string, optional
            Which outlier algorithm to use. If set to "removeoutliers", uses the removeoutliers algorithm that
            removes data based on the skewness of the dataset. If set to "iterstat", uses the iterstat algorithm
            to remove data based on being outside a certain number of standard deviations from the mean
        nsig : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the Chi2s. Default is 2.
            
    Returns
    -------
        cchi2 : ndarray
            Boolean array giving which indices to keep or throw out based on the outlier algorithm
            
    """
    nbin = len(traces[0])
    ind_trigger = round(nbin / 2)
    time = 1.0 / fs * (np.arange(1, nbin + 1) - ind_trigger)
    lgc_b0 = time < 0.0
    tau_risepulse = 1e-05
    tau_fallpulse = 0.0001
    dummytemplate = (1.0 - np.exp(-time / tau_risepulse)) * np.exp(-time / tau_fallpulse)
    dummytemplate[lgc_b0] = 0.0
    dummytemplate = dummytemplate / max(dummytemplate)
    dummypsd = np.ones(nbin)
    chi2 = np.zeros(len(traces))
    for itrace in range(0, len(traces)):
        chi2[itrace] = ofamp(traces[itrace], dummytemplate, dummypsd, fs)[2]

    if outlieralgo == 'removeoutliers':
        cchi2 = removeoutliers(chi2)
    else:
        if outlieralgo == 'iterstat':
            cchi2 = iterstat(chi2, cut=nsig, precision=10000.0)[2]
        else:
            raise ValueErrror('Unknown outlier algorithm inputted.')
    return cchi2


def autocuts(traces, fs=625000.0, is_didv=False, sgfreq=200.0, symmetrizeflag=False, outlieralgo='removeoutliers', lgcpileup1=True, lgcslope=True, lgcbaseline=True, lgcpileup2=True, lgcchi2=True, nsigpileup1=2, nsigslope=2, nsigbaseline=2, nsigpileup2=2, nsigchi2=3):
    """
    Function to automatically cut out bad traces based on the optimum filter amplitude, slope, baseline, and chi^2
    of the traces.
    
    Parameters
    ----------
        traces : ndarray
            2-dimensional array of traces to do cuts on
        fs : float, optional
            Sample rate that the data was taken at
        is_didv : bool, optional
            Boolean flag on whether or not the trace is a dIdV curve
        sgfreq : float, optional
            If is_didv is True, then the sgfreq is used to know where the flat parts of the traces should be
        symmetrizeflag : bool, optional
            Flag for whether or not the slopes should be forced to have an average value of zero.
            Should be used if most of the traces have a slope
        outlieralgo : string, optional
            Which outlier algorithm to use. If set to "removeoutliers", uses the removeoutliers algorithm that
            removes data based on the skewness of the dataset. If set to "iterstat", uses the iterstat algorithm
            to remove data based on being outside a certain number of standard deviations from the mean
        lgcpileup1 : boolean, optional
            Boolean value on whether or not do the pileup1 cut (this is the initial pileup cut
            that is always done whether or not we have dIdV data). Default is True.
        lgcslope : boolean, optional
            Boolean value on whether or not do the slope cut. Default is True.
        lgcbaseline : boolean, optional
            Boolean value on whether or not do the baseline cut. Default is True.
        lgcpileup2 : boolean, optional
            Boolean value on whether or not do the pileup2 cut (this cut is only done when is_didv is
            also True). Default is True.
        lgcchi2 : boolean, optional
            Boolean value on whether or not do the chi2 cut. Default is True.
        nsigpileup1 : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the optimum filter amplitudes. Default is 2.
        nsigslope : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the slopes. Default is 2.
        nsigbaseline : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the baselines. Default is 2.
        nsigpileup2 : float, optional
            If outlieralgo is "iterstat", this can be used to tune the number of standard deviations from the mean
            to cut outliers from the data when using iterstat on the optimum filter amplitudes after the mean
            has been subtracted. (only used if is_didv is True). Default is 2.
        nsigchi2 : float, optional
            This can be used to tune the number of standard deviations from the mean to cut outliers from the data
            when using iterstat on the chi^2 values. Default is 3. This is always used, as iterstat is always used
            for the chi^2 cut.
            
    Returns
    -------
        ctot : ndarray
            Boolean array giving which indices to keep or throw out based on the autocuts algorithm
            
    """
    if lgcpileup1:
        cpileup1 = pileupcut(traces, fs=fs, outlieralgo=outlieralgo, nsig=nsigpileup1)
        cpileup1inds = np.where(cpileup1)[0]
    else:
        cpileup1inds = np.arange(len(traces))
    if lgcslope:
        cslope = slopecut((traces[cpileup1inds]), fs=fs, outlieralgo=outlieralgo, nsig=nsigslope, is_didv=is_didv, symmetrizeflag=symmetrizeflag,
          sgfreq=sgfreq)
    else:
        cslope = np.ones((cpileup1inds.shape), dtype=bool)
    cslopeinds = cpileup1inds[cslope]
    if lgcbaseline:
        cbaseline = baselinecut((traces[cslopeinds]), fs=fs, outlieralgo=outlieralgo, nsig=nsigbaseline, is_didv=is_didv, sgfreq=sgfreq)
    else:
        cbaseline = np.ones((cslopeinds.shape), dtype=bool)
    cbaselineinds = cslopeinds[cbaseline]
    if lgcpileup2:
        if is_didv:
            cpileup2 = pileupcut((traces[cbaselineinds]), fs=fs, outlieralgo=outlieralgo, nsig=nsigpileup2, removemeans=True)
        else:
            cpileup2 = np.ones((cbaselineinds.shape), dtype=bool)
    else:
        cpileup2inds = cbaselineinds[cpileup2]
        if lgcchi2:
            cchi2 = chi2cut((traces[cpileup2inds]), fs=fs, outlieralgo='iterstat', nsig=nsigchi2)
        else:
            cchi2 = np.ones((cpileup2inds.shape), dtype=bool)
    cchi2inds = cpileup2inds[cchi2]
    ctot = np.zeros((len(traces)), dtype=bool)
    ctot[cchi2inds] = True
    return ctot