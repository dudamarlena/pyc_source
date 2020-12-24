# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/Events\zeniDetector.py
# Compiled at: 2019-03-07 07:04:50
__doc__ = 'Nexus Operation : **plotTemporalEmg**\n\nThe script displays rectified EMG with time as x-axis\n\n:param -fso, --footStrikeOffset [int]: add an offset on all foot strike events\n:param -foo, --footOffOffset [int]: add an offset on all foot off events\n\n\nExamples:\n    In the script argument box of a python nexus operation, you can edit:\n\n    >>>  -fso=10\n    (add 10 frames to all foot strike events)\n\n\n'
import traceback, os, logging, matplotlib.pyplot as plt, argparse, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2 import btk
from pyCGM2.Tools import btkTools
from pyCGM2.Events import events
from pyCGM2.Nexus import nexusTools

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        DEBUG = False
        if DEBUG:
            DATA_PATH = 'C:\\Users\\AAA34169\\Documents\\VICON DATA\\Salford\\Alana MoCap data\\MRI-US-01 - myProcess\\PIG\\'
            reconstructFilenameLabelledNoExt = 'MRI-US-01, 2008-08-08, 3DGA 16'
            NEXUS.OpenTrial(str(DATA_PATH + reconstructFilenameLabelledNoExt), 10)
        else:
            DATA_PATH, reconstructFilenameLabelledNoExt = NEXUS.GetTrialName()
        reconstructFilenameLabelled = reconstructFilenameLabelledNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('calibration file: ' + reconstructFilenameLabelled)
        acqGait = btkTools.smartReader(str(DATA_PATH + reconstructFilenameLabelled))
        if acqGait.GetPoint(0).GetLabel().count(':'):
            raise Exception('[pyCGM2] Your Trial c3d was saved with two activate subject. Re-save it with only one before pyCGM2 calculation')
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        logging.info('Subject name : ' + subject)
        evp = events.ZeniProcedure()
        if args.footStrikeOffset is not None:
            evp.setFootStrikeOffset(args.footStrikeOffset)
        if args.footOffOffset is not None:
            evp.setFootOffOffset(args.footOffOffset)
        evf = events.EventFilter(evp, acqGait)
        evf.detect()
        nexusTools.createEvents(NEXUS, subject, acqGait, ['Foot Strike', 'Foot Off'])
        if DEBUG:
            NEXUS.SaveTrial(30)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ZeniDetector')
    parser.add_argument('-fso', '--footStrikeOffset', type=int, help='systenatic foot strike offset on both side')
    parser.add_argument('-foo', '--footOffOffset', type=int, help='systenatic foot off offset on both side')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise