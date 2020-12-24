# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/DataProcessing\plotTemporalKinematics.py
# Compiled at: 2019-03-07 07:04:50
__doc__ = 'Nexus Operation : **plotTemporalKinematics**\n\nThe script displays kinematics with time as x-axis\n\n:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs\n\nExamples:\n    In the script argument box of a python nexus operation, you can edit:\n\n    >>>  -ps=py\n    (all points will be suffixed with py (LHipAngles_py))\n\n\n'
import traceback, logging, argparse, matplotlib.pyplot as plt, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2 import enums
from pyCGM2.Lib import analysis
from pyCGM2.Lib import plot
from pyCGM2.Report import normativeDatasets
from pyCGM2.Nexus import nexusTools
from pyCGM2.Utils import files

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        pointSuffix = args.pointSuffix
        DEBUG = False
        if DEBUG:
            DATA_PATH = 'C:\\Users\\HLS501\\Documents\\VICON DATA\\pyCGM2-Data\\Release Tests\\CGM2.2\\medial\\'
            modelledFilenameNoExt = 'Gait Trial 01'
            NEXUS.OpenTrial(str(DATA_PATH + modelledFilenameNoExt), 30)
        else:
            DATA_PATH, modelledFilenameNoExt = NEXUS.GetTrialName()
        modelledFilename = modelledFilenameNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('file: ' + modelledFilename)
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        logging.info('Subject name : ' + subject)
        model = files.loadModel(DATA_PATH, subject)
        modelVersion = model.version
        if model.m_bodypart in [enums.BodyPart.LowerLimb, enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
            plot.plotTemporalKinematic(DATA_PATH, modelledFilename, 'LowerLimb', pointLabelSuffix=pointSuffix, exportPdf=True)
        if model.m_bodypart in [enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
            plot.plotTemporalKinematic(DATA_PATH, modelledFilename, 'Trunk', pointLabelSuffix=pointSuffix, exportPdf=True)
        if model.m_bodypart in [enums.BodyPart.UpperLimb, enums.BodyPart.FullBody]:
            pass
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    plt.close('all')
    parser = argparse.ArgumentParser(description='CGM Gait Processing')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix of model outputs')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise