# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/check_dir.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2923 bytes
import os, glob
import dicom_tools.info_file_parser as info_file_parser
import dicom_tools.nrrdFileHandler as nrrdFileHandler

def check_dir(inputdir, verbose=False):
    if verbose:
        print('inputdir', inputdir)
    table = []
    patientdirs = glob.glob(inputdir + '*/')
    for patientdir in patientdirs:
        if verbose:
            print(patientdir)
        elif patientdir[(-1)] == '/':
            patID = patientdir.split('/')[(-2)].replace('.', '')
        else:
            patID = patientdir.split('/')[(-1)].replace('.', '')
        if verbose:
            print('id:', patID)
        analasisysdirs = glob.glob(patientdir + '*/')
        for analasisysdir in analasisysdirs:
            patient = []
            patient.append(patID)
            if verbose:
                print('\t', analasisysdir)
            else:
                pathT2 = analasisysdir + 'T2/'
                pathROI = analasisysdir + 'ROI/'
                if verbose:
                    print('reading on patient: ' + patID)
                    print('T2 directory: ' + pathT2)
                else:
                    if os.path.isdir(pathT2):
                        dicomfiles = glob.glob(pathT2 + '/*.dcm')
                        allfiles = glob.glob(pathT2 + '/*')
                        patient.append(len(dicomfiles))
                        patient.append(len(allfiles) - len(dicomfiles))
                    else:
                        patient.append(0)
                        patient.append(0)
                    pathROI = analasisysdir + 'ROI/'
                    if os.path.isdir(pathROI):
                        nrrdfiles = glob.glob(pathROI + '/*.nrrd')
                        if len(nrrdfiles) > 0:
                            fr = nrrdFileHandler(False)
                            nrrdROI = fr.read(nrrdfiles[0])
                            dicomfiles = glob.glob(pathROI + '/*.dcm')
                            allfiles = glob.glob(pathROI + '/*')
                            patient.append(len(nrrdROI))
                            patient.append(len(dicomfiles))
                            patient.append(len(allfiles) - len(dicomfiles) - len(nrrdfiles))
                        else:
                            patient.append(0)
                            patient.append(0)
                            patient.append(0)
                    else:
                        patient.append(0)
                        patient.append(0)
                        patient.append(0)
                infofilename = analasisysdir + 'info.txt'
                if os.path.isfile(infofilename):
                    infos = info_file_parser(infofilename)
                    patient.append(infos['time'])
                    patient.append(infos['ypT'])
                    patient.append(infos['name'])
                else:
                    patient.append('None')
                    patient.append('None')
                    patient.append('None')
            table.append(patient)

    return table