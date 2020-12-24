# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/Normalizer.py
# Compiled at: 2018-09-14 09:20:48
# Size of source mod 2**32: 5643 bytes
try:
    import ROOT
    ROOTfound = True
except ImportError:
    ROOTfound = False
    print('WARNING Normalizer.py: ROOT not found')

import numpy as np
import dicom_tools.FileReader as FileReader

class Normalizer:

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.RootOutput = False
        self.layer = -1
        self.NormLayer = -1
        if self.verbose:
            print('Normalizer: init verbose\n')
        self.externalTemplateSetted = False
        self.externalTemplate = None

    def setExternalTemplate(self, dcmfile):
        freader = FileReader(dcmfile, False, self.verbose)
        dataRGB, unusedROI = freader.read(False)
        self.externalTemplateSetted = True
        self.externalTemplate = dataRGB[:, :, 0]
        self.NormLayer = -1

    def setNormLayer(self, layer=-1):
        self.NormLayer = layer
        self.externalTemplateSetted = False
        self.externalTemplate = None

    def setRootOutput(self, prefix=''):
        self.RootOutput = True
        self.allHistos = []
        self.RootPrefix = prefix

    def writeRootOutputOnFile(self, outfname='out.root'):
        outfile = ROOT.TFile(outfname, 'RECREATE')
        for histo in self.allHistos:
            histo.Write()

        outfile.Write()
        outfile.Close()

    def hist_match(self, source, template):
        """
        Adjust the pixel values of a grayscale image such that its histogram
        matches that of a target image
        
        Arguments:
        -----------
        source: np.ndarray
        Image to transform; the histogram is computed over the flattened array
        template: np.ndarray
        Template image; can have different dimensions to source
        Returns:
        -----------
        matched: np.ndarray
        The transformed output image
        """
        oldshape = source.shape
        source = source.ravel()
        template = template.ravel()
        s_values, bin_idx, s_counts = np.unique(source, return_inverse=True, return_counts=True)
        t_values, t_counts = np.unique(template, return_counts=True)
        s_quantiles = np.cumsum(s_counts).astype(np.float64)
        s_quantiles /= s_quantiles[(-1)]
        t_quantiles = np.cumsum(t_counts).astype(np.float64)
        t_quantiles /= t_quantiles[(-1)]
        interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)
        if self.RootOutput:
            suffix = str(self.layer)
            prefix = self.RootPrefix
            nBin = 500
            cumsumOrig = ROOT.TH1F(prefix + 'cumsumOrig' + suffix, prefix + 'cumsumOrig' + suffix, nBin, s_values.min(), s_values.max())
            cumsumTemplate = ROOT.TH1F(prefix + 'cumsumTemplate' + suffix, prefix + 'cumsumTemplate' + suffix, nBin, t_values.min(), t_values.max())
            cumsumInterp = ROOT.TH1F(prefix + 'cumsumInterp' + suffix, prefix + 'cumsumInterp' + suffix, nBin, interp_t_values.min(), interp_t_values.max())
            for s_value in s_values:
                cumsumOrig.Fill(s_value)

            for t_value in t_values:
                cumsumTemplate.Fill(s_value)

            for interp_t_value in interp_t_values:
                cumsumInterp.Fill(interp_t_value)

            self.allHistos.append(cumsumTemplate)
            self.allHistos.append(cumsumOrig)
            self.allHistos.append(cumsumInterp)
        return interp_t_values[bin_idx].reshape(oldshape)

    def match_all(self, data):
        norm_layer = self.NormLayer
        matched = np.zeros(data.shape)
        if len(data.shape) == 4:
            layers = len(data[:, :, :, 0])
            if not self.externalTemplateSetted:
                if norm_layer < 0:
                    norm_layer = int(layers / 2 + 0.5)
                matched[norm_layer, :, :, 0] = matched[norm_layer, :, :, 1] = matched[norm_layer, :, :, 2] = data[norm_layer, :, :, 0]
                template = data[norm_layer, :, :, 0]
            else:
                template = self.externalTemplate
            for self.layer in xrange(0, layers):
                if self.layer == norm_layer:
                    continue
                matched[self.layer, :, :, 0] = matched[self.layer, :, :, 1] = matched[self.layer, :, :, 2] = self.hist_match(data[self.layer, :, :, 0], template)

        elif len(data.shape) == 3:
            layers = len(data)
            if norm_layer < 0:
                norm_layer = int(layers / 2 + 0.5)
            matched[norm_layer] = data[norm_layer]
            for self.layer in xrange(0, layers):
                if self.layer == norm_layer:
                    continue
                matched[self.layer] = self.hist_match(data[self.layer], data[norm_layer])

        else:
            print('ERROR hist_match data has not 4 axis nor 3')
        return matched