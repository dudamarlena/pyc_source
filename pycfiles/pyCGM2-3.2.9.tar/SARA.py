# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/CGM2_6\SARA.py
# Compiled at: 2019-03-07 07:04:50
"""Nexus Operation : **SARA**

Calibration of the knee with the SARA method.

The script considers all frames of the c3d and detects the side autmaticallt from ANK marker trajectories

:param -s, --side [string]: lower limb side ( choice: Left or Right )
:param -b, --beginFrame [int]:  manual selection of the first  frame
:param -e, --endFrame [int]:   manual selection of the last  frame

Examples:
    In the script argument box of a python nexus operation, you can edit:

    >>>  -side=Left -b=50 -e=100
    (Left knee calibration between frames 50 and 100)
"""
import traceback, logging, argparse, matplotlib.pyplot as plt, numpy as np, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2 import enums
from pyCGM2.Tools import btkTools
from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters, nexusUtils, nexusTools
from pyCGM2.Model import modelFilters
from pyCGM2.Configurator import CgmArgsManager
from pyCGM2.Lib.CGM import kneeCalibration

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        DEBUG = False
        if DEBUG:
            DATA_PATH = pyCGM2.TEST_DATA_PATH + 'CGM2\\knee calibration\\CGM2.3-calibrationSara\\'
            reconstructedFilenameLabelledNoExt = 'Right Knee'
            NEXUS.OpenTrial(str(DATA_PATH + reconstructedFilenameLabelledNoExt), 30)
        else:
            DATA_PATH, reconstructedFilenameLabelledNoExt = NEXUS.GetTrialName()
        reconstructFilenameLabelled = reconstructedFilenameLabelledNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('reconstructed file: ' + reconstructFilenameLabelled)
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        logging.info('Subject name : ' + subject)
        model = files.loadModel(DATA_PATH, subject)
        logging.info('loaded model : %s' % model.version)
        if model.version in ('CGM1.0', 'CGM1.1', 'CGM2.1', 'CGM2.2'):
            raise Exception('Can t use SARA method with your model %s [minimal version : CGM2.3]' % model.version)
        elif model.version == 'CGM2.3':
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_3-pyCGM2.settings')
        elif model.version in ('CGM2.4', ):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_4-pyCGM2.settings')
        else:
            raise Exception('model version not found [contact admin]')
        mpInfo, mpFilename = files.getMpFileContent(DATA_PATH, 'mp.pyCGM2', subject)
        if model.version in ('CGM2.3', ):
            translators = files.getTranslators(DATA_PATH, 'CGM2-3.translators')
        elif model.version in ('CGM2.4', ):
            translators = files.getTranslators(DATA_PATH, 'CGM2-4.translators')
        if not translators:
            translators = settings['Translators']
        model, acqFunc, side = kneeCalibration.sara(model, DATA_PATH, reconstructFilenameLabelled, translators, args.side, args.beginFrame, args.endFrame)
        files.saveModel(model, DATA_PATH, subject)
        logging.warning('model updated with a  %s knee calibrated with SARA method' % side)
        files.saveMp(mpInfo, model, DATA_PATH, mpFilename)
        nexusUtils.updateNexusSubjectMp(NEXUS, model, subject)
        if side == 'Left':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'LFE0', model.getSegment('Left Thigh'), OriginValues=acqFunc.GetPoint('LKJC').GetValues())
        elif side == 'Right':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'RFE0', model.getSegment('Right Thigh'), OriginValues=acqFunc.GetPoint('RKJC').GetValues())
        proximalSegmentLabel = str(side + ' Thigh')
        distalSegmentLabel = str(side + ' Shank')
        meanOr_inThigh = model.getSegment(proximalSegmentLabel).getReferential('TF').getNodeTrajectory('KJC_Sara')
        meanAxis_inThigh = model.getSegment(proximalSegmentLabel).getReferential('TF').getNodeTrajectory('KJC_SaraAxis')
        btkTools.smartAppendPoint(acqFunc, side + '_KJC_Sara', meanOr_inThigh)
        btkTools.smartAppendPoint(acqFunc, side + '_KJC_SaraAxis', meanAxis_inThigh)
        nexusTools.appendModelledMarkerFromAcq(NEXUS, subject, side + '_KJC_Sara', acqFunc)
        nexusTools.appendModelledMarkerFromAcq(NEXUS, subject, side + '_KJC_SaraAxis', acqFunc)
        scp = modelFilters.StaticCalibrationProcedure(model)
        modMotion = modelFilters.ModelMotionFilter(scp, acqFunc, model, enums.motionMethod.Sodervisk)
        modMotion.segmentalCompute([proximalSegmentLabel, distalSegmentLabel])
        if side == 'Left':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'LFE1', model.getSegment('Left Thigh'), OriginValues=acqFunc.GetPoint('LKJC').GetValues())
            print model.mp_computed['LeftKneeFuncCalibrationOffset']
            logging.warning('offset %s' % str(model.mp_computed['LeftKneeFuncCalibrationOffset']))
        elif side == 'Right':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'RFE1', model.getSegment('Right Thigh'), OriginValues=acqFunc.GetPoint('RKJC').GetValues())
            logging.warning('offset %s' % str(model.mp_computed['RightKneeFuncCalibrationOffset']))
            print model.mp_computed['RightKneeFuncCalibrationOffset']
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    plt.close('all')
    parser = argparse.ArgumentParser(description='SARA Functional Knee Calibration')
    parser.add_argument('-s', '--side', type=str, help='Side : Left or Right')
    parser.add_argument('-b', '--beginFrame', type=int, help='begin frame')
    parser.add_argument('-e', '--endFrame', type=int, help='end frame')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise