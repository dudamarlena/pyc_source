# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/DataProcessing\plotSpatioTemporalParameters.py
# Compiled at: 2019-03-07 07:04:50
"""Nexus Operation : **plotSpatioTemporalParameters**

The script displays spatio-temporal parameters (Velocity, cadence, duration of the gait phases...)

:param -ps, --pointSuffix [string]: suffix adds to the pyCGM2 nomenclature

Examples:
    In the script argument box of a python nexus operation, you can edit:

    >>>  -ps=py

.. note::
    the spatio-temporal parameters are :
        * duration
        * cadence
        * stanceDuration
        * stancePhase
        * swingDuration
        * swingPhase
        * doubleStance1
        * doubleStance2
        * simpleStance
        * strideLength
        * stepLength
        * strideWidth
        * speed

.. warning::
    the spatio-temporal parameters are not stored in the c3d file yet.

"""
import traceback, logging, argparse, matplotlib.pyplot as plt, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
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
        analysisInstance = analysis.makeAnalysis(DATA_PATH, [modelledFilename], pointLabelSuffix=pointSuffix)
        plot.plot_spatioTemporal(DATA_PATH, analysisInstance, exportPdf=True, outputName=modelledFilename)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    plt.close('all')
    parser = argparse.ArgumentParser(description='CGM Gait Processing')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix added to pyCGM2 outputs')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise