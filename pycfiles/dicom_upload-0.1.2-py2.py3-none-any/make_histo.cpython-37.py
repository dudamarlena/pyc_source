# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/make_histo.py
# Compiled at: 2018-09-14 09:20:48
# Size of source mod 2**32: 11709 bytes
from __future__ import print_function
try:
    import ROOT
    ROOTfound = True
except ImportError:
    ROOTfound = False
    print('WARNING make_histo.py: ROOT not found')

import numpy as np
from skimage.feature import greycomatrix, greycoprops
from skimage import exposure
from dicom_tools.rescale import rescale8bit
import dicom_tools.calculateMeanInROI as calculateMeanInROI
import dicom_tools.fractal as fractal
from scipy import ndimage
from dicom_tools.gaussianlaplace import GaussianLaplaceFilter

def make_histo(data, mask, suffix='', verbose=False, ROInorm=False, normalize=False, scala=False, filtered=False):
    nbin = 10000
    binmin = data.min() * 0.8
    binmax = data.max() * 1.2
    if scala:
        binmin = -5
        binmax = 5
    if normalize:
        layerOfMax = np.where(data == data.max())[0][0]
        normformaxbin = calculateMeanInROI(data[layerOfMax], ROInorm[layerOfMax], verbose)
        binmax = data.max() / normformaxbin
        binmin = 0
        nbin = int(data.max() - binmin)
        bindim = (binmax - binmin) / nbin
        if verbose:
            print('make_histo: layerOfMax', layerOfMax, 'data.max()', data.max(), 'binmax', binmax, 'nbin', nbin)
    if verbose:
        print('make_histo: bin min:', binmin, 'bin max:', binmax, 'nbin:', nbin)
    nFette = len(data)
    his = ROOT.TH1F('histo' + suffix, 'histo', nbin, binmin, binmax)
    hEntries = ROOT.TH1F('hEntries' + suffix, 'Entries', nFette, -0.5, nFette + 0.5)
    hMean = ROOT.TH1F('hMean' + suffix, 'Mean', nFette, -0.5, nFette + 0.5)
    hStdDev = ROOT.TH1F('hStdDev' + suffix, 'StdDev', nFette, -0.5, nFette + 0.5)
    hSkewness = ROOT.TH1F('hSkewness' + suffix, 'Skewness', nFette, -0.5, nFette + 0.5)
    hKurtosis = ROOT.TH1F('hKurtosis' + suffix, 'Kurtosis', nFette, -0.5, nFette + 0.5)
    hfra = ROOT.TH1F('hfra' + suffix, 'fra', nFette, -0.5, nFette + 0.5)
    hCfra = ROOT.TH1F('hCfra' + suffix, 'hCfra', nFette, -0.5, nFette + 0.5)
    hdissH = ROOT.TH1F('hdissH' + suffix, 'Horizontal dissimilarity', nFette, -0.5, nFette + 0.5)
    hcorrH = ROOT.TH1F('hcorrH' + suffix, 'Horizontal correlation', nFette, -0.5, nFette + 0.5)
    henerH = ROOT.TH1F('henerH' + suffix, 'Horizontal energy', nFette, -0.5, nFette + 0.5)
    hcontH = ROOT.TH1F('hcontH' + suffix, 'Horizontal contrast', nFette, -0.5, nFette + 0.5)
    hhomoH = ROOT.TH1F('hhomoH' + suffix, 'Horizontal homogeneity', nFette, -0.5, nFette + 0.5)
    hdissV = ROOT.TH1F('hdissV' + suffix, 'Vertical dissimilarity', nFette, -0.5, nFette + 0.5)
    hcorrV = ROOT.TH1F('hcorrV' + suffix, 'Vertical correlation', nFette, -0.5, nFette + 0.5)
    henerV = ROOT.TH1F('henerV' + suffix, 'Vertical energy', nFette, -0.5, nFette + 0.5)
    hcontV = ROOT.TH1F('hcontV' + suffix, 'Vertical contrast', nFette, -0.5, nFette + 0.5)
    hhomoV = ROOT.TH1F('hhomoV' + suffix, 'Vertical homogeneity', nFette, -0.5, nFette + 0.5)
    hdissPQ = ROOT.TH1F('hdissPQ' + suffix, '+45 degree dissimilarity', nFette, -0.5, nFette + 0.5)
    hcorrPQ = ROOT.TH1F('hcorrPQ' + suffix, '+45 degree correlation', nFette, -0.5, nFette + 0.5)
    henerPQ = ROOT.TH1F('henerPQ' + suffix, '+45 degree energy', nFette, -0.5, nFette + 0.5)
    hcontPQ = ROOT.TH1F('hcontPQ' + suffix, '+45 degree contrast', nFette, -0.5, nFette + 0.5)
    hhomoPQ = ROOT.TH1F('hhomoPQ' + suffix, '+45 degree homogeneity', nFette, -0.5, nFette + 0.5)
    hdissMQ = ROOT.TH1F('hdissMQ' + suffix, '-45 degree dissimilarity', nFette, -0.5, nFette + 0.5)
    hcorrMQ = ROOT.TH1F('hcorrMQ' + suffix, '-45 degree correlation', nFette, -0.5, nFette + 0.5)
    henerMQ = ROOT.TH1F('henerMQ' + suffix, '-45 degree energy', nFette, -0.5, nFette + 0.5)
    hcontMQ = ROOT.TH1F('hcontMQ' + suffix, '-45 degree contrast', nFette, -0.5, nFette + 0.5)
    hhomoMQ = ROOT.TH1F('hhomoMQ' + suffix, '-45 degree homogeneity', nFette, -0.5, nFette + 0.5)
    allhistos = []
    histogiafatti = []
    histogclm = []
    for layer in xrange(0, nFette):
        fetta = data[layer]
        if scala:
            media = np.mean(fetta)
            rms = np.std(fetta)
            fetta = (fetta - media) / rms
        fetta8bit = rescale8bit(fetta)
        fettaROI = mask[layer]
        glcmdata = mask[layer] * fetta8bit
        glcm1 = greycomatrix(glcmdata, [1], [0], 256, symmetric=True, normed=True)
        glcm2 = greycomatrix(glcmdata, [1], [np.pi / 2], 256, symmetric=True, normed=True)
        glcm3 = greycomatrix(glcmdata, [1], [np.radians(45)], 256, symmetric=True, normed=True)
        glcm4 = greycomatrix(glcmdata, [1], [np.radians(-45)], 256, symmetric=True, normed=True)
        hdissH.SetBinContent(layer, greycoprops(glcm1, 'dissimilarity')[(0, 0)])
        hcorrH.SetBinContent(layer, greycoprops(glcm1, 'correlation')[(0, 0)])
        henerH.SetBinContent(layer, greycoprops(glcm1, 'energy')[(0, 0)])
        hcontH.SetBinContent(layer, greycoprops(glcm1, 'contrast')[(0, 0)])
        hhomoH.SetBinContent(layer, greycoprops(glcm1, 'homogeneity')[(0, 0)])
        hdissV.SetBinContent(layer, greycoprops(glcm2, 'dissimilarity')[(0, 0)])
        hcorrV.SetBinContent(layer, greycoprops(glcm2, 'correlation')[(0, 0)])
        henerV.SetBinContent(layer, greycoprops(glcm2, 'energy')[(0, 0)])
        hcontV.SetBinContent(layer, greycoprops(glcm2, 'contrast')[(0, 0)])
        hhomoV.SetBinContent(layer, greycoprops(glcm2, 'homogeneity')[(0, 0)])
        hdissPQ.SetBinContent(layer, greycoprops(glcm3, 'dissimilarity')[(0, 0)])
        hcorrPQ.SetBinContent(layer, greycoprops(glcm3, 'correlation')[(0, 0)])
        henerPQ.SetBinContent(layer, greycoprops(glcm3, 'energy')[(0, 0)])
        hcontPQ.SetBinContent(layer, greycoprops(glcm3, 'contrast')[(0, 0)])
        hhomoPQ.SetBinContent(layer, greycoprops(glcm3, 'homogeneity')[(0, 0)])
        hdissMQ.SetBinContent(layer, greycoprops(glcm4, 'dissimilarity')[(0, 0)])
        hcorrMQ.SetBinContent(layer, greycoprops(glcm4, 'correlation')[(0, 0)])
        henerMQ.SetBinContent(layer, greycoprops(glcm4, 'energy')[(0, 0)])
        hcontMQ.SetBinContent(layer, greycoprops(glcm4, 'contrast')[(0, 0)])
        hhomoMQ.SetBinContent(layer, greycoprops(glcm4, 'homogeneity')[(0, 0)])
        thishisto = ROOT.TH1F('h' + str(layer) + suffix, 'h' + str(layer), nbin, binmin, binmax)
        meaninroi = 1
        frattale = 0
        frattalecont = 0
        if fettaROI.max() > 0:
            frattale = fractal().frattali(fettaROI)
            frattalecont = fractal().frattali(fetta * np.subtract(fettaROI, ndimage.binary_erosion(fettaROI).astype(fettaROI.dtype)))
        if fettaROI.any():
            if normalize:
                meaninroi = calculateMeanInROI(fetta, ROInorm[layer], verbose)
                if verbose:
                    print('make_histo: layer', layer, 'meaninroi', meaninroi)
            if fettaROI.any():
                if verbose:
                    print('non zero pixels:', np.count_nonzero(fetta))
            for val, inROI in zip(fetta.ravel(), fettaROI.ravel()):
                if inROI > 0:
                    if normalize:
                        val = val / meaninroi
                    if val > binmax:
                        print('make_histo: Warning in layer', layer, 'there is a value in overflow:', val, 'normalization', meaninroi)
                    if val > 0:
                        his.Fill(val)
                        thishisto.Fill(val)

            hEntries.SetBinContent(layer, thishisto.GetEntries())
            hMean.SetBinContent(layer, thishisto.GetMean())
            hStdDev.SetBinContent(layer, thishisto.GetStdDev())
            hSkewness.SetBinContent(layer, thishisto.GetSkewness())
            hKurtosis.SetBinContent(layer, thishisto.GetKurtosis())
            hfra.SetBinContent(layer, frattale)
            hCfra.SetBinContent(layer, frattalecont)
        if verbose:
            print('make_histo', 'layer', layer, 'entries', thishisto.GetEntries())
        allhistos.append(thishisto)

    histogiafatti.append(hEntries)
    histogiafatti.append(hMean)
    histogiafatti.append(hStdDev)
    histogiafatti.append(hSkewness)
    histogiafatti.append(hKurtosis)
    histogiafatti.append(hfra)
    histogiafatti.append(hCfra)
    histogclm.append(hdissH)
    histogclm.append(hcorrH)
    histogclm.append(henerH)
    histogclm.append(hcontH)
    histogclm.append(hhomoH)
    histogclm.append(hdissV)
    histogclm.append(hcorrV)
    histogclm.append(henerV)
    histogclm.append(hcontV)
    histogclm.append(hhomoV)
    histogclm.append(hdissPQ)
    histogclm.append(hcorrPQ)
    histogclm.append(henerPQ)
    histogclm.append(hcontPQ)
    histogclm.append(hhomoPQ)
    histogclm.append(hdissMQ)
    histogclm.append(hcorrMQ)
    histogclm.append(henerMQ)
    histogclm.append(hcontMQ)
    histogclm.append(hhomoMQ)
    return (
     his, allhistos, histogiafatti, histogclm)