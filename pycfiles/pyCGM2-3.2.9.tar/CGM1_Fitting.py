# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/CGM1\CGM1_Fitting.py
# Compiled at: 2019-03-07 07:04:49
"""Nexus Operation : **CGM1 Fitting**

:param --proj [string]: define in which coordinate system joint moment will be expressed (Choice : Distal, Proximal, Global)
:param -md, --markerDiameter [int]: marker diameter
:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs
:param --check [bool]: add "cgm1" as point suffix

Examples:
    In the script argument box of a python nexus operation, you can edit:

    >>> --proj=Global
    (means joint moments will be expressed into the Global Coordinate system)

"""
import os, traceback, logging, argparse, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2.Configurator import CgmArgsManager
from pyCGM2.Lib.CGM import cgm1
from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters, nexusUtils, nexusTools

def main(args):
    if NEXUS_PYTHON_CONNECTED:
        if os.path.isfile(pyCGM2.PYCGM2_APPDATA_PATH + 'CGM1-pyCGM2.settings'):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM1-pyCGM2.settings')
        else:
            settings = files.openFile(pyCGM2.PYCGM2_SETTINGS_FOLDER, 'CGM1-pyCGM2.settings')
        argsManager = CgmArgsManager.argsManager_cgm1(settings, args)
        markerDiameter = argsManager.getMarkerDiameter()
        pointSuffix = argsManager.getPointSuffix('cgm1')
        momentProjection = argsManager.getMomentProjection()
        DEBUG = False
        if DEBUG:
            DATA_PATH = 'C:\\Users\\HLS501\\Documents\\VICON DATA\\pyCGM2-Data\\Release Tests\\CGM1\\Kad\\'
            reconstructFilenameLabelledNoExt = 'Gait Trial 01'
            NEXUS.OpenTrial(str(DATA_PATH + reconstructFilenameLabelledNoExt), 10)
        else:
            DATA_PATH, reconstructFilenameLabelledNoExt = NEXUS.GetTrialName()
        reconstructFilenameLabelled = reconstructFilenameLabelledNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('calibration file: ' + reconstructFilenameLabelled)
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        logging.info('Subject name : ' + subject)
        model = files.loadModel(DATA_PATH, subject)
        logging.info('loaded model : %s' % model.version)
        if model.version != 'CGM1.0':
            raise Exception('%s-pyCGM2.model file was not calibrated from the CGM1.0 calibration pipeline' % model.version)
        translators = files.getTranslators(DATA_PATH, 'CGM1.translators')
        if not translators:
            translators = settings['Translators']
        mfpa = nexusTools.getForcePlateAssignment(NEXUS)
        acqGait = cgm1.fitting(model, DATA_PATH, reconstructFilenameLabelled, translators, markerDiameter, pointSuffix, mfpa, momentProjection)
        nexusFilters.NexusModelFilter(NEXUS, model, acqGait, subject, pointSuffix).run()
        nexusTools.createGeneralEvents(NEXUS, subject, acqGait, ['Left-FP', 'Right-FP'])
        if DEBUG:
            NEXUS.SaveTrial(30)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    parser = argparse.ArgumentParser(description='CGM1 Fitting')
    parser.add_argument('--proj', type=str, help='Moment Projection. Choice : Distal, Proximal, Global')
    parser.add_argument('-md', '--markerDiameter', type=float, help='marker diameter')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('--check', action='store_true', help='force model output suffix')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise