# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/CGM2_5\CGM2_5_Calibration.py
# Compiled at: 2019-03-07 07:04:50
__doc__ = 'Nexus Operation : **CGM2.5 Calibration**\n\n:param -l, --leftFlatFoot [int]: enable or disable the flat foot option on the left foot\n:param -r, --rightFlatFoot [int]: enable or disable the flat foot option on the right foot\n:param -md, --markerDiameter [int]: marker diameter\n:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs\n:param --check [bool]: add "cgm2.5" as point suffix\n:param --resetMP [bool]: reset computation of optional parameters, like interAsisDistance, ShankOffsets...\n:param --forceLHJC [array]: force the local position of the left hip joint centre in the pelvic coordinate system\n:param --forceRHJC [array]: force the local position of the left hip joint centre in the pelvic coordinate system\n\n\nExamples:\n    In the script argument box of a python nexus operation, you can edit:\n\n    >>> -l=1 -r=0 -ps=py\n    (if you want to add suffix py and enable the flat foot option on the left side only)\n    >>> --leftFlatFoot=1 -r=0 --pointSuffix=py --resetMP\n    (if you want to add suffix py, enable the flat foot option on the left side only and reset the computation of optional parameters, like interAsisDistance, ShankOffsets...)\n    >>>  --forceLHJC 10 20 30  --forceRHJC 10 20 30\n    (force the left and right hip joint centre positions (10 mm along the pelvic X-axis, 20 mm along the pelvic Y-axis, 30 mm along the pelvic Z-axis)\n\n'
import os, traceback, logging, argparse, matplotlib.pyplot as plt, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters, nexusUtils, nexusTools
from pyCGM2.Configurator import CgmArgsManager
from pyCGM2.Lib.CGM import cgm2_5

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        if os.path.isfile(pyCGM2.PYCGM2_APPDATA_PATH + 'CGM2_5-pyCGM2.settings'):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_5-pyCGM2.settings')
        else:
            settings = files.openFile(pyCGM2.PYCGM2_SETTINGS_FOLDER, 'CGM2_5-pyCGM2.settings')
        argsManager = CgmArgsManager.argsManager_cgm(settings, args)
        leftFlatFoot = argsManager.getLeftFlatFoot()
        rightFlatFoot = argsManager.getRightFlatFoot()
        markerDiameter = argsManager.getMarkerDiameter()
        pointSuffix = argsManager.getPointSuffix('cgm2.5')
        ik_flag = argsManager.enableIKflag()
        hjcMethod = settings['Calibration']['HJC']
        lhjc = argsManager.forceHjc('left')
        rhjc = argsManager.forceHjc('right')
        if lhjc is not None:
            hjcMethod['Left'] = lhjc
        if rhjc is not None:
            hjcMethod['Right'] = rhjc
        DEBUG = False
        if DEBUG:
            DATA_PATH = pyCGM2.TEST_DATA_PATH + 'Release Tests\\CGM2.5\\fullBody\\'
            calibrateFilenameLabelledNoExt = 'static'
            NEXUS.OpenTrial(str(DATA_PATH + calibrateFilenameLabelledNoExt), 30)
            args.noIk = False
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
        translators = files.getTranslators(DATA_PATH, 'CGM2_5.translators')
        if not translators:
            translators = settings['Translators']
        model, finalAcqStatic = cgm2_5.calibrate(DATA_PATH, calibrateFilenameLabelled, translators, settings, required_mp, optional_mp, ik_flag, leftFlatFoot, rightFlatFoot, markerDiameter, hjcMethod, pointSuffix)
        files.saveModel(model, DATA_PATH, subject)
        files.saveMp(mpInfo, model, DATA_PATH, mpFilename)
        nexusUtils.updateNexusSubjectMp(NEXUS, model, subject)
        nexusFilters.NexusModelFilter(NEXUS, model, finalAcqStatic, subject, pointSuffix, staticProcessing=True).run()
        if DEBUG:
            NEXUS.SaveTrial(30)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')
    return


if __name__ == '__main__':
    plt.close('all')
    parser = argparse.ArgumentParser(description='CGM2.5 Calibration')
    parser.add_argument('-l', '--leftFlatFoot', type=int, help='left flat foot option')
    parser.add_argument('-r', '--rightFlatFoot', type=int, help='right flat foot option')
    parser.add_argument('-md', '--markerDiameter', type=float, help='marker diameter')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('--check', action='store_true', help='force model output suffix')
    parser.add_argument('--noIk', action='store_true', help='cancel inverse kinematic')
    parser.add_argument('--resetMP', action='store_true', help='reset optional mass parameters')
    parser.add_argument('--forceLHJC', nargs='+')
    parser.add_argument('--forceRHJC', nargs='+')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise