# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/CGM2_6\2DofCalibration.py
# Compiled at: 2019-03-07 07:04:50
__doc__ = 'Nexus Operation : **2DofCalibration**\n\nCalibration of the knee with the Calibration2Dof method (dynaKad like method).\n\nThe script considers all frames of the c3d and detects the side autmaticallt from ANK marker trajectories\n\n:param -s, --side [string]: lower limb side ( choice: Left or Right )\n:param -b, --beginFrame [int]:  manual selection of the first  frame\n:param -e, --endFrame [int]:   manual selection of the last  frame\n\n\nExamples:\n    In the script argument box of a python nexus operation, you can edit:\n\n    >>>  -side=Left -b=50 -e=100\n    (Left knee calibration between frames 50 and 100)\n\n\n'
import traceback, logging, argparse, matplotlib.pyplot as plt, numpy as np, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2 import enums
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
            DATA_PATH = pyCGM2.TEST_DATA_PATH + 'CGM2\\knee calibration\\CGM2.4-calibration2Dof\\'
            reconstructedFilenameLabelledNoExt = 'PN01OP01S01FUNC01'
            args.side = 'Left'
            args.beginFrame = 932
            args.endFrame = 1278
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
        if model.version == 'CGM1.0':
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM1-pyCGM2.settings')
        elif model.version == 'CGM1.1':
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM1_1-pyCGM2.settings')
        elif model.version == 'CGM2.1':
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_1-pyCGM2.settings')
        elif model.version == 'CGM2.2':
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_2-pyCGM2.settings')
        elif model.version == 'CGM2.3':
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_3-pyCGM2.settings')
        elif model.version in ('CGM2.4', ):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_4-pyCGM2.settings')
        else:
            raise Exception('model version not found [contact admin]')
        mpInfo, mpFilename = files.getMpFileContent(DATA_PATH, 'mp.pyCGM2', subject)
        if model.version in ('CGM1.0', ):
            translators = files.getTranslators(DATA_PATH, 'CGM1.translators')
        elif model.version in ('CGM1.1', ):
            translators = files.getTranslators(DATA_PATH, 'CGM1_1.translators')
        elif model.version in ('CGM2.1', ):
            translators = files.getTranslators(DATA_PATH, 'CGM2_1.translators')
        elif model.version in ('CGM2.2', ):
            translators = files.getTranslators(DATA_PATH, 'CGM2_2.translators')
        elif model.version in ('CGM2.3', ):
            translators = files.getTranslators(DATA_PATH, 'CGM2_3.translators')
        elif model.version in ('CGM2.4', ):
            translators = files.getTranslators(DATA_PATH, 'CGM2_4.translators')
        if not translators:
            translators = settings['Translators']
        model, acqFunc, side = kneeCalibration.calibration2Dof(model, DATA_PATH, reconstructFilenameLabelled, translators, args.side, args.beginFrame, args.endFrame, None)
        files.saveModel(model, DATA_PATH, subject)
        logging.warning('model updated with a  %s knee calibrated with 2Dof method' % side)
        files.saveMp(mpInfo, model, DATA_PATH, mpFilename)
        nexusUtils.updateNexusSubjectMp(NEXUS, model, subject)
        if side == 'Left':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'LFE0', model.getSegment('Left Thigh'), OriginValues=acqFunc.GetPoint('LKJC').GetValues())
        elif side == 'Right':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'RFE0', model.getSegment('Right Thigh'), OriginValues=acqFunc.GetPoint('RKJC').GetValues())
        scp = modelFilters.StaticCalibrationProcedure(model)
        if model.version in ('CGM1.0', 'CGM1.1', 'CGM2.1', 'CGM2.2'):
            modMotion = modelFilters.ModelMotionFilter(scp, acqFunc, model, enums.motionMethod.Determinist)
            modMotion.compute()
        elif model.version in ('CGM2.3', 'CGM2.4'):
            proximalSegmentLabel = str(side + ' Thigh')
            distalSegmentLabel = str(side + ' Shank')
            modMotion = modelFilters.ModelMotionFilter(scp, acqFunc, model, enums.motionMethod.Sodervisk)
            modMotion.segmentalCompute([proximalSegmentLabel, distalSegmentLabel])
        if side == 'Left':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'LFE1', model.getSegment('Left Thigh'), OriginValues=acqFunc.GetPoint('LKJC').GetValues())
            logging.warning('offset %s' % str(model.mp_computed['LeftKneeFuncCalibrationOffset']))
        elif side == 'Right':
            nexusTools.appendBones(NEXUS, subject, acqFunc, 'RFE1', model.getSegment('Right Thigh'), OriginValues=acqFunc.GetPoint('RKJC').GetValues())
            logging.warning('offset %s' % str(model.mp_computed['RightKneeFuncCalibrationOffset']))
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')
    return


if __name__ == '__main__':
    plt.close('all')
    parser = argparse.ArgumentParser(description='2Dof Knee Calibration')
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