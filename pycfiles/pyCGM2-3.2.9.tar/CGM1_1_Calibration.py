# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/CGM1_1\CGM1_1_Calibration.py
# Compiled at: 2019-03-07 07:04:49
"""Nexus Operation : **CGM1.1 Calibration**

:param -l, --leftFlatFoot [int]: enable or disable the flat foot option on the left foot
:param -r, --rightFlatFoot [int]: enable or disable the flat foot option on the right foot
:param -md, --markerDiameter [int]: marker diameter
:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs
:param --check [bool]: add "cgm1.1" as point suffix
:param --resetMP [bool]: reset computation of optional parameters, like interAsisDistance, ShankOffsets...

Examples:
    In the script argument box of a python nexus operation, you can edit:

    >>> -l=1 -r=0 -ps=py
    (if you want to add suffix py and enable the flat foot option on the left side only)
    >>> --leftFlatFoot=1 -r=0 --pointSuffix=py --resetMP
    (if you want to add suffix py, enable the flat foot option on the left side only and reset the computation of optional parameters, like interAsisDistance, ShankOffsets...)

"""
import os, traceback, logging, matplotlib.pyplot as plt, argparse, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters, nexusUtils, nexusTools
from pyCGM2.Configurator import CgmArgsManager
from pyCGM2.Lib.CGM import cgm1_1

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        if os.path.isfile(pyCGM2.PYCGM2_APPDATA_PATH + 'CGM1_1-pyCGM2.settings'):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM1_1-pyCGM2.settings')
        else:
            settings = files.openFile(pyCGM2.PYCGM2_SETTINGS_FOLDER, 'CGM1_1-pyCGM2.settings')
        argsManager = CgmArgsManager.argsManager_cgm1(settings, args)
        leftFlatFoot = argsManager.getLeftFlatFoot()
        rightFlatFoot = argsManager.getRightFlatFoot()
        markerDiameter = argsManager.getMarkerDiameter()
        pointSuffix = argsManager.getPointSuffix('cgm1_1')
        DEBUG = False
        if DEBUG:
            DATA_PATH = 'C:\\Users\\HLS501\\Documents\\VICON DATA\\pyCGM2-Data\\Release Tests\\CGM1\\Kad\\'
            calibrateFilenameLabelledNoExt = 'Static Cal 01-both'
            NEXUS.OpenTrial(str(DATA_PATH + calibrateFilenameLabelledNoExt), 30)
        else:
            DATA_PATH, calibrateFilenameLabelledNoExt = NEXUS.GetTrialName()
        calibrateFilenameLabelled = calibrateFilenameLabelledNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('calibration file: ' + calibrateFilenameLabelled)
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        Parameters = NEXUS.GetSubjectParamNames(subject)
        required_mp, optional_mp = nexusUtils.getNexusSubjectMp(NEXUS, subject, resetFlag=args.resetMP)
        mpInfo, mpFilename = files.getMpFileContent(DATA_PATH, 'mp.pyCGM2', subject)
        translators = files.getTranslators(DATA_PATH, 'CGM1_1.translators')
        if not translators:
            translators = settings['Translators']
        model, acqStatic = cgm1_1.calibrate(DATA_PATH, calibrateFilenameLabelled, translators, required_mp, optional_mp, leftFlatFoot, rightFlatFoot, markerDiameter, pointSuffix)
        files.saveModel(model, DATA_PATH, subject)
        files.saveMp(mpInfo, model, DATA_PATH, mpFilename)
        nexusUtils.updateNexusSubjectMp(NEXUS, model, subject)
        nexusFilters.NexusModelFilter(NEXUS, model, acqStatic, subject, pointSuffix, staticProcessing=True).run()
        if DEBUG:
            NEXUS.SaveTrial(30)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CGM1.1 Calibration')
    parser.add_argument('-l', '--leftFlatFoot', type=int, help='left flat foot option')
    parser.add_argument('-r', '--rightFlatFoot', type=int, help='right flat foot option')
    parser.add_argument('-md', '--markerDiameter', type=float, help='marker diameter')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('--check', action='store_true', help='force model output suffix')
    parser.add_argument('--resetMP', action='store_true', help='reset optional mass parameters')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise