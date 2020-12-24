# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/EMG\plotTemporalEmg.py
# Compiled at: 2019-03-07 07:04:50
__doc__ = 'Nexus Operation : **plotTemporalEmg**\n\nThe script displays rectified EMG with time as x-axis\n\n:param -bpf, --BandpassFrequencies [array]: bandpass frequencies\n:param -ecf, --EnvelopLowpassFrequency [double]: cut-off low pass frequency for getting emg envelop\n:param -fs, --fileSuffix [string]: store the c3d file with addition of a suffix\n:param -r, --raw [bool]: display non-rectified emg instead of rectified\n\nExamples:\n    In the script argument box of a python nexus operation, you can edit:\n\n    >>>  -bpf 20 450 -ecf=8.9 --raw\n    (bandpass frequencies set to 20 and 450Hz and envelop made from a low-pass filter with a cutoff frequency of 8.9Hz,\n    non-rectified EMG  will be displayed)\n\n\n'
import os, logging, argparse, traceback, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
from pyCGM2.Utils import files
from pyCGM2.Lib import analysis
from pyCGM2.Lib import plot
from pyCGM2.Report import normativeDatasets
import ViconNexus

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        if os.path.isfile(pyCGM2.PYCGM2_APPDATA_PATH + 'emg.settings'):
            emgSettings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'emg.settings')
        else:
            emgSettings = files.openFile(pyCGM2.PYCGM2_SETTINGS_FOLDER, 'emg.settings')
        bandPassFilterFrequencies = emgSettings['Processing']['BandpassFrequencies']
        if args.BandpassFrequencies is not None:
            if len(args.BandpassFrequencies) != 2:
                raise Exception('[pyCGM2] - bad configuration of the bandpass frequencies ... set 2 frequencies only')
            else:
                bandPassFilterFrequencies = [
                 float(args.BandpassFrequencies[0]), float(args.BandpassFrequencies[1])]
                logging.info('Band pass frequency set to %i - %i instead of 20-200Hz', bandPassFilterFrequencies[0], bandPassFilterFrequencies[1])
        envelopCutOffFrequency = emgSettings['Processing']['EnvelopLowpassFrequency']
        if args.EnvelopLowpassFrequency is not None:
            envelopCutOffFrequency = args.EnvelopLowpassFrequency
            logging.info('Cut-off frequency set to %i instead of 6Hz ', envelopCutOffFrequency)
        rectifyBool = False if args.raw else True
        fileSuffix = args.fileSuffix
        DEBUG = False
        if DEBUG:
            DATA_PATH = pyCGM2.TEST_DATA_PATH + 'EMG\\SampleNantes_prepost\\'
            inputFileNoExt = 'pre'
            NEXUS.OpenTrial(str(DATA_PATH + inputFileNoExt), 10)
        else:
            DATA_PATH, inputFileNoExt = NEXUS.GetTrialName()
        inputFile = inputFileNoExt + '.c3d'
        EMG_LABELS = []
        EMG_CONTEXT = []
        NORMAL_ACTIVITIES = []
        EMG_MUSCLES = []
        for emg in emgSettings['CHANNELS'].keys():
            if emg != 'None':
                if emgSettings['CHANNELS'][emg]['Muscle'] != 'None':
                    EMG_LABELS.append(str(emg))
                    EMG_MUSCLES.append(str(emgSettings['CHANNELS'][emg]['Muscle']))
                    EMG_CONTEXT.append(str(emgSettings['CHANNELS'][emg]['Context'])) if emgSettings['CHANNELS'][emg]['Context'] != 'None' else EMG_CONTEXT.append(None)
                    NORMAL_ACTIVITIES.append(str(emgSettings['CHANNELS'][emg]['NormalActivity'])) if emgSettings['CHANNELS'][emg]['NormalActivity'] != 'None' else EMG_CONTEXT.append(None)

        analysis.processEMG(DATA_PATH, [inputFile], EMG_LABELS, highPassFrequencies=bandPassFilterFrequencies, envelopFrequency=envelopCutOffFrequency, fileSuffix=fileSuffix)
        if fileSuffix is not None:
            inputfile = inputFile + '_' + fileSuffix
        plot.plotTemporalEMG(DATA_PATH, inputFile, EMG_LABELS, EMG_MUSCLES, EMG_CONTEXT, NORMAL_ACTIVITIES, exportPdf=True, rectify=rectifyBool)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EMG-plot_temporalEMG')
    parser.add_argument('-bpf', '--BandpassFrequencies', nargs='+', help='bandpass filter')
    parser.add_argument('-ecf', '--EnvelopLowpassFrequency', type=int, help='cutoff frequency for emg envelops')
    parser.add_argument('-fs', '--fileSuffix', type=str, help='suffix of the processed file')
    parser.add_argument('-r', '--raw', action='store_true', help='rectified data')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise