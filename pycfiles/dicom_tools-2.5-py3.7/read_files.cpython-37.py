# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/read_files.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 6001 bytes
import glob, numpy as np, dicom, nrrd

def read_files(inpath, inpathROI=False, verbose=False, raw=False):
    infiles = glob.glob(inpath + '/*.dcm')
    if verbose:
        print('funciont read file V 1.0')
        print('input directory:\n', inpath)
        print(len(infiles), ' files will be imported')
    else:
        dicoms = []
        for thisfile in infiles:
            dicoms.append(dicom.read_file(thisfile))

        dicoms.sort(key=(lambda x: float(x.ImagePositionPatient[2])))
        ConstPixelDims = (
         int(dicoms[0].Rows), int(dicoms[0].Columns), len(dicoms))
        ConstPixelSpacing = (
         float(dicoms[0].PixelSpacing[0]), float(dicoms[0].PixelSpacing[1]), float(dicoms[0].SliceThickness))
        if verbose:
            print('Voxel dimensions: ', ConstPixelSpacing)
        xsize = np.arange(0.0, (ConstPixelDims[0] + 1) * ConstPixelSpacing[0], ConstPixelSpacing[0])
        ysize = np.arange(0.0, (ConstPixelDims[1] + 1) * ConstPixelSpacing[1], ConstPixelSpacing[1])
        zsize = np.arange(0.0, (ConstPixelDims[2] + 1) * ConstPixelSpacing[2], ConstPixelSpacing[2])
        scaleFactor = dicoms[0].SliceThickness / dicoms[0].PixelSpacing[0]
        scaleFactorInt = int(scaleFactor + 0.5)
        if verbose:
            print('scaleFactor', scaleFactor)
            print('scaleFactorInt', scaleFactorInt)
        data = np.zeros(tuple([len(dicoms)]) + dicoms[0].pixel_array.shape)
        dataRGB = np.zeros(tuple([len(dicoms) * scaleFactorInt]) + dicoms[0].pixel_array.shape + tuple([3]))
        rawROI = np.full((tuple([len(dicoms)]) + dicoms[0].pixel_array.shape), False, dtype=bool)
        ROI = np.full((tuple([len(dicoms) * scaleFactorInt]) + dicoms[0].pixel_array.shape), False, dtype=bool)
        if inpathROI:
            if verbose:
                print('ROI requested, path: ', inpathROI)
            else:
                infilesROInrrd = glob.glob(inpathROI + '/*.nrrd')
                if verbose:
                    print(len(infilesROInrrd), 'nrrd files found in ROI path: ')
                if len(infilesROInrrd) == 1:
                    if verbose:
                        print('nrrd ROI file: ', infilesROInrrd)
                    nrrdROItmp, nrrdROIoptions = nrrd.read(infilesROInrrd[0])
                    nrrdROI = nrrdROItmp.swapaxes(0, 1).swapaxes(0, 2)
                    for i, fetta in enumerate(reversed(nrrdROI)):
                        rawROI[i] = fetta
                        ROI[i * scaleFactorInt] = fetta
                        if i < len(nrrdROI) - 1:
                            for j in xrange(1, int(scaleFactorInt / 2) + 1):
                                ROI[i * scaleFactorInt + j] = fetta

                        if i > 0:
                            for j in xrange(int(-scaleFactorInt / 2) + 1, 0):
                                ROI[i * scaleFactorInt + j] = fetta

                else:
                    if len(infilesROInrrd) > 1:
                        print('ERROR: in the directory ', inpathROI, ' there is more than 1 nrrd file', infilesROInrrd)
                    else:
                        infilesROI = glob.glob(inpathROI + '/*.dcm')
                        if verbose:
                            print(len(infilesROI), ' files will be imported for the ROI')
                        if len(infilesROI) != len(infiles):
                            print('ERROR: in the directory ', inpath, ' there are ', len(infiles), ' dicom files')
                            print('while in the ROI directory ', inpathROI, ' there are ', len(infilesROI), ' dicom files')
                        dicomsROI = []
                        for infileROI in infilesROI:
                            dicomsROI.append(dicom.read_file(infileROI))

                        for i, thisROI in enumerate(reversed(dicomsROI)):
                            pix_arr = thisROI.pixel_array
                            ROI[i * scaleFactorInt] = pix_arr.T
                            rawROI[i] = pix_arr.T
                            if i < len(dicomsROI) - 1:
                                for j in xrange(1, int(scaleFactorInt / 2) + 1):
                                    ROI[i * scaleFactorInt + j] = pix_arr.T

                            if i > 0:
                                for j in xrange(int(-scaleFactorInt / 2) + 1, 0):
                                    ROI[i * scaleFactorInt + j] = pix_arr.T

    for i, thisdicom in enumerate(reversed(dicoms)):
        pix_arr = thisdicom.pixel_array
        data[i] = pix_arr.T
        dataRGB[i * scaleFactorInt, :, :, 2] = dataRGB[i * scaleFactorInt, :, :, 0] = pix_arr.T
        dataRGB[i * scaleFactorInt, :, :, 1] = pix_arr.T - np.multiply(pix_arr.T, ROI[(i * scaleFactorInt)])
        if i < len(dicoms) - 1:
            for j in xrange(1, int(scaleFactorInt / 2) + 1):
                dataRGB[i * scaleFactorInt + j, :, :, 2] = dataRGB[i * scaleFactorInt + j, :, :, 0] = pix_arr.T
                dataRGB[i * scaleFactorInt + j, :, :, 1] = pix_arr.T - np.multiply(pix_arr.T, ROI[(i * scaleFactorInt + j)])

        if i > 0:
            for j in xrange(int(-scaleFactorInt / 2) + 1, 0):
                dataRGB[i * scaleFactorInt + j, :, :, 2] = dataRGB[i * scaleFactorInt + j, :, :, 0] = pix_arr.T
                dataRGB[i * scaleFactorInt + j, :, :, 1] = pix_arr.T - np.multiply(pix_arr.T, ROI[(i * scaleFactorInt + j)])

    if raw:
        if verbose:
            print('returning raw data')
        return (
         data, rawROI)
    return (
     dataRGB, ROI)