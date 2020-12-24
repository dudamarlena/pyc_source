# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/FileReader.py
# Compiled at: 2018-06-23 04:52:24
# Size of source mod 2**32: 9466 bytes
from __future__ import print_function
import glob, numpy as np
try:
    import dicom
except ImportError:
    import pydicom as dicom

import nrrd, os
import dicom_tools.nrrdFileHandler as nrrdFileHandler
import SimpleITK as sitk

class FileReader:

    def __init__(self, inpath, inpathROI=False, verbose=False):
        self.inpath = inpath
        self.inpathROI = inpathROI
        self.verbose = verbose
        self.scaleFactor = None
        if self.verbose:
            print('FileReader: init verbose\n')
        self.infiles = []
        self.infilesROI = []
        self.data = []
        self.dataRGB = []
        self.ROI = []
        self.PatientName = None

    def loadDCMfiles(self):
        if self.verbose:
            print('FileReader: init verbose\n')
        else:
            inpath = self.inpath
            verbose = self.verbose
            if os.path.isdir(inpath):
                self.infiles = glob.glob(inpath + '/*.dcm')
                if len(self.infiles) == 0:
                    print('FileReader WARNING: there are no .dcm files in dir', inpath, 'trying to open files without extension')
                    allfiles = glob.glob(inpath + '/*')
                    if verbose:
                        print('len(allfiles):', len(allfiles))
                    for thisfile in allfiles:
                        fname = thisfile.split('/')[(-1)]
                        if verbose:
                            print(fname)
                        if '.' not in fname:
                            self.infiles.append(thisfile)

                    if verbose:
                        print('len(self.infiles):', len(self.infiles))
            else:
                self.infiles = inpath
        if verbose:
            print('funciont read file V 1.1')
            print('input directory:\n', inpath)
            print(len(self.infiles), ' files will be imported')

    def read(self, raw=False):
        if self.verbose:
            print('FileReader::read\n')
        else:
            verbose = self.verbose
            inpathROI = self.inpathROI
            self.loadDCMfiles()
            dicoms = []
            for thisfile in self.infiles:
                dicoms.append(dicom.read_file(thisfile))

            dicoms.sort(key=(lambda x: float(x.ImagePositionPatient[2])))
            self.ConstPixelDims = (
             int(dicoms[0].Rows), int(dicoms[0].Columns), len(dicoms))
            self.ConstPixelSpacing = (
             float(dicoms[0].PixelSpacing[0]), float(dicoms[0].PixelSpacing[1]), float(dicoms[0].SliceThickness))
            if verbose:
                print('n dicom files:', len(dicoms))
                print('Voxel dimensions: ', self.ConstPixelSpacing)
            self.scaleFactor = dicoms[0].SliceThickness / dicoms[0].PixelSpacing[0]
            if verbose:
                print('scaleFactor', self.scaleFactor)
            self.data = np.zeros(tuple([len(dicoms)]) + tuple([dicoms[0].pixel_array.shape[1], dicoms[0].pixel_array.shape[0]]))
            self.dataRGB = np.zeros(tuple([len(dicoms)]) + tuple([dicoms[0].pixel_array.shape[1], dicoms[0].pixel_array.shape[0]]) + tuple([3]))
            if verbose:
                print('data.shape', self.data.shape)
                print('dataRGB.shape', self.dataRGB.shape)
            if inpathROI:
                self.readROI()
            else:
                self.ROI = np.full((self.data.shape), False, dtype=bool)
        if len(self.ROI) is not len(self.data):
            print('FileReader ERROR: ROI and data have different length')
            raise ValueError('ROI and data have different length', len(self.data), len(self.ROI), self.inpath, self.inpathROI)
        for i, thisdicom in enumerate(reversed(dicoms)):
            pix_arr = thisdicom.pixel_array
            self.dataRGB[i, :, :, 2] = self.dataRGB[i, :, :, 0] = self.data[i] = pix_arr.T
            self.dataRGB[i, :, :, 1] = pix_arr.T - np.multiply(pix_arr.T, self.ROI[i])

        self.PatientName = dicoms[0].PatientName
        if self.verbose:
            print('FileReader::read type(self.data): ', type(self.data), ' type(self.data[0,0,0]): ', type(self.data[(0,
                                                                                                                      0,
                                                                                                                      0)]), ' \n')
        if raw:
            if self.verbose:
                print('FileReader::read returning raw\n')
            return (self.data[:, :, ::-1], self.ROI[:, :, :])
        if inpathROI:
            ROI = ROI.astype(np.bool)
        return (self.dataRGB[:, :, ::-1, :], self.ROI[:, :, :])

    def readUsingGDCM(self, raw=False, sitkout=False):
        if self.verbose:
            print('FileReader::readUsingGDCM\n')
        reader = sitk.ImageSeriesReader()
        filenamesDICOM = reader.GetGDCMSeriesFileNames(self.inpath)
        reader.SetFileNames(filenamesDICOM)
        imgOriginal = reader.Execute()
        if sitkout:
            return imgOriginal
        self.data = sitk.GetArrayFromImage(imgOriginal)
        self.data = self.data.swapaxes(1, 2)
        self.data = self.data[::-1, :, ::-1]
        if self.verbose:
            print('FileReader::readUsingGDCM type(self.data): ', type(self.data), ' type(self.data[0,0,0]): ', type(self.data[(0,
                                                                                                                               0,
                                                                                                                               0)]), ' \n')
        self.scaleFactor = imgOriginal.GetSpacing()[2] / imgOriginal.GetSpacing()[0]
        if raw:
            if self.verbose:
                print('FileReader::readUsingGDCM returning raw\n')
            return self.data
        self.dataRGB = np.zeros(self.data.shape + tuple([3]))
        self.dataRGB[:, :, :, 0] = self.dataRGB[:, :, :, 1] = self.dataRGB[:, :, :, 2] = self.data
        if self.verbose:
            print('FileReader::readUsingGDCM returning RGB\n')
        return self.dataRGB

    def readROI(self):
        verbose = self.verbose
        inpathROI = self.inpathROI
        inpath = self.inpath
        self.ROI = np.full((self.data.shape), False, dtype=bool)
        if verbose:
            print('ROI requested, path: ', inpathROI)
        infilesROInrrd = glob.glob(inpathROI + '/*.nrrd')
        if verbose:
            print(len(infilesROInrrd), 'nrrd files found in ROI path: ')
        if len(infilesROInrrd) == 1:
            if verbose:
                print('nrrd ROI file: ', infilesROInrrd)
            roiFileReader = nrrdFileHandler(self.verbose)
            self.ROI = roiFileReader.read(infilesROInrrd[0])
            if verbose:
                print('FileRader.readROI non zero elements', np.count_nonzero(self.ROI))
            return self.ROI
        if len(infilesROInrrd) > 1:
            print('ERROR: in the directory ', inpathROI, ' there is more than 1 nrrd file', infilesROInrrd)
            roiFileReader = nrrdFileHandler(self.verbose)
            return roiFileReader.read(infilesROInrrd[0])
        self.infilesROI = glob.glob(inpathROI + '/*.dcm')
        if verbose:
            print(len(self.infilesROI), ' files will be imported for the ROI')
        if len(self.infilesROI) != len(self.infiles):
            print('ERROR: in the directory ', inpath, ' there are ', len(self.infiles), ' dicom files')
            print('while in the ROI directory ', inpathROI, ' there are ', len(self.infilesROI), ' dicom files')
        dicomsROI = []
        for infileROI in self.infilesROI:
            dicomsROI.append(dicom.read_file(infileROI))

        for i, thisROI in enumerate(reversed(dicomsROI)):
            pix_arr = thisROI.pixel_array
            self.ROI[i] = pix_arr.T

        ROI = ROI.astype(np.bool)
        return self.ROI[:, :, ::-1]