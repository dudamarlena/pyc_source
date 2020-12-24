# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dreegdl/preprocessing.py
# Compiled at: 2020-03-05 17:58:16
# Size of source mod 2**32: 14430 bytes
import logging, numpy as np, os, pywt, scipy, subprocess
from statsmodels.tsa.ar_model import AR
from glob import glob
import IPython.utils as ipio
from tqdm import tqdm_notebook as tqdmn
from utils import Utils

class Preprocessing:

    def __init__(self, config={}):
        self.config = config

    def check_src_dest(self, src, dest, destname):
        if not src:
            raise Exception('No source is specified')
        else:
            if not dest:
                raise Exception('No output path is specified for {} files'.format(destname))
            os.path.isdir(dest) or Utils.run_cmd(['mkdir ' + dest])
            if not os.path.isdir(dest):
                raise Exception('Can not create directory :' + dest)

    def install_octave_oct2py_eeglab(self):
        print('Installing Octave, Oct2Py, and EEGLab packages')
        try:
            Utils.run_cmd(['which octave'])
        except Exception as e:
            try:
                Utils.run_cmd(['apt-get update; apt install octave -qq > /dev/null'])
            finally:
                e = None
                del e

        if not os.path.isdir('./eeglab'):
            Utils.run_cmd(['git clone --recurse-submodules -q https://github.com/sccn/eeglab.git'])
        try:
            import oct2py
        except ImportError as e:
            try:
                Utils.run_cmd(['pip install oct2py -q'])
            finally:
                e = None
                del e

        import oct2py
        oct2py.octave.addpath('./eeglab/functions/miscfunc')
        oct2py.octave.addpath('./eeglab/functions/guifunc')
        oct2py.octave.addpath('./eeglab/functions/popfunc')
        oct2py.octave.addpath('./eeglab/functions/adminfunc')
        oct2py.octave.addpath('./eeglab/functions/sigprocfunc')
        oct2py.octave.logger.setLevel(logging.ERROR)

    def install_mne(self):
        try:
            import mne
        except ImportError as e:
            try:
                Utils.run_cmd(['pip install mne -q'])
            finally:
                e = None
                del e

    def process_source(self, mat, fdest):
        import oct2py
        with ipio.capture_output():
            itemLoaded = oct2py.octave.pop_loadset(mat)
            itemChecked = oct2py.octave.eeg_checkset(itemLoaded)
            oct2py.octave.pop_saveset(itemChecked,
              filename=(fdest.split('/')[(-1)]), filepath=('/'.join(fdest.split('/')[:-1])),
              savemode='onefile',
              check='on')
        del itemLoaded
        del itemChecked

    def process_sources(self, src='', dest=''):
        self.check_src_dest(src, dest, 'Set')
        src = src.rstrip('/')
        dest = dest.rstrip('/')
        mats = sorted(glob(src + '/*.mat'))
        if not len(mats):
            raise Exception('No Mat file found')
        self.install_octave_oct2py_eeglab()
        print('Processing Source (.mat) files and converting them to .set files')
        for item in tqdmn(mats, ncols=500):
            fname = item.split('/')[(-1)]
            fdest = dest + '/' + fname[:-4] + '.set'
            if not os.path.isfile(fdest):
                self.process_source(item, fdest)

    def epoching(self, item, fepoch, ftimes):
        import mne
        with ipio.capture_output() as (capt):
            raw = mne.io.read_raw_eeglab(item)
            events, event_id = mne.events_from_annotations(raw)
            event_id = dict(((k.replace('.0', ''), v) for k, v in event_id.items()))
            event_id_swapd = dict(((v, k) for k, v in event_id.items()))
            if self.config.ref_channels:
                raw.set_eeg_reference(ref_channels=(self.config.ref_channels))
            if self.config.bad_channels:
                raw.drop_channels([x for x in self.config.bad_channels if x in raw.ch_names])
            if self.config.rm_baseline:
                raw._data = mne.baseline.rescale(raw.get_data(), raw.times, self.config.rm_baseline)
            if self.config.filter_range:
                raw.filter((self.config.filter_range[0]), (self.config.filter_range[1]), method='iir', verbose='WARNING')
            if self.config.ica_args:
                ica = (mne.preprocessing.ICA)(**(self.config).ica_args)
                ica.fit(raw)
                ica.apply(raw)
            if self.config.butter_filter:
                for key, val in self.config.butter_filter.items():
                    exec(key + '=val')

                nyq = 0.5 * raw.info['sfreq']
                low = lowcut / nyq
                high = highcut / nyq
                b, a = scipy.signal.butter(order, [low, high], btype='band')
                raw._data = scipy.signal.lfilter(b, a, raw.get_data())
        epochs = {}
        times = {}
        maxI = len(events) - 1
        prev_ev_name = None
        for i, ev in enumerate(events):
            ev_name = event_id_swapd[ev[2]]
            if ev_name not in self.config.valid_events:
                continue
            tmin = ev[0]
            if i == maxI:
                tmax = raw._data.shape[1]
            else:
                tmax = events[(i + 1)][0]
                if len(events) > i + 2:
                    if ev[(-1)] not in (14, 15):
                        if events[(i + 1)][(-1)] in (14, 15):
                            ccc, j = (0, 1)
                            while events[(i + j)][(-1)] in (14, 15):
                                ccc += 1
                                j += 1

                            last = events[(i + j)]
                            if ev[(-1)] in (1, 9, 10, 11, 12, 13) and not last[(-1)] == ev[(-1)]:
                                if last[0] - tmin <= 270 or last[(-1)] != ev[(-1)]:
                                    if not tmax - tmin < 174 or last[0] - tmin <= 176:
                                        tmax = last[0]
                dd = raw._data[:, tmin:tmax].transpose()
                tt = raw._times[tmin:tmax]
                if epochs.get(ev_name) is None:
                    epochs[ev_name] = [
                     [
                      dd]]
                    times[ev_name] = [[tt]]
                else:
                    if prev_ev_name == ev_name:
                        epochs[ev_name][(-1)].append(dd)
                        times[ev_name][(-1)].append(tt)
                    else:
                        epochs[ev_name].append([dd])
                        times[ev_name].append([tt])
                prev_ev_name = ev_name

        if len(epochs) < len(self.config.valid_events):
            print('Subject does not have all events:', item)
            return False
        epochsNp = []
        timesNp = []
        for ev in self.config.valid_events:
            epochsNp.append(np.array([(Utils.list2arr)(*x) for x in epochs[ev]]))
            timesNp.append(np.array([(Utils.list2arr)(*x) for x in times[ev]]))

        epochsNp = (Utils.list2arr)(*epochsNp)
        timesNp = (Utils.list2arr)(*timesNp)
        np.save(fepoch, epochsNp)
        np.save(ftimes, timesNp)
        del epochs
        del epochsNp
        del timesNp
        return True

    def do_epoching(self, src='', dest=''):
        print('Epoching method has been called')
        self.check_src_dest(src, dest, 'Epochs')
        src = src.rstrip('/')
        dest = dest.rstrip('/')
        ext1 = self.config.exts.get('set')
        sets = sorted(glob(src + '/*' + ext1))
        if not len(sets):
            raise Exception('No Set file found')
        self.install_mne()
        print('Epoching Set files')
        for fset in tqdmn(sets, ncols=500):
            fname = fset.split('/')[(-1)][:-len(ext1)]
            fepoch, ftimes = [dest + '/' + fname + ext for ext in self.config.exts.list('epo', 'ept')]
            if os.path.isfile(fepoch):
                os.path.isfile(ftimes) or self.epoching(fset, fepoch, ftimes)

    def features_of_channel(self, data, timesdiff):
        if len(data) < 3:
            return
        dwt = 'db4'
        cA, cD = pywt.dwt(data, dwt)
        cAf = np.fft.fft(cA)
        cDf = np.fft.fft(cD)
        diff1 = np.diff(data)
        diff2 = np.diff(data, n=2)
        diff1Var = np.mean(diff1 ** 2)
        activity = np.var(data)
        mobility = np.sqrt(diff1Var / activity)
        complexity = np.sqrt(np.mean(diff2 ** 2) / diff1Var) / mobility
        fft1 = np.fft.fft(data)
        fft1abs = np.abs(fft1.real)
        bands = {'delta':{'freq':(0.5, 4), 
          'sum':0,  'max':0}, 
         'theta':{'freq':(4, 8), 
          'sum':0,  'max':0}, 
         'alpha':{'freq':(8, 13), 
          'sum':0,  'max':0}, 
         'beta':{'freq':(13, 30), 
          'sum':0,  'max':0}}
        shape1sfreq = float(data.shape[0]) / self.config.sfreq
        for band, bandDict in bands.items():
            arange = np.arange((bandDict['freq'][0] * shape1sfreq), (bandDict['freq'][1] * shape1sfreq),
              dtype=int)
            bandDict['sum'] = np.sum(fft1abs.real[arange])
            bandDict['max'] = np.max(fft1abs.real[arange])

        diff1Slope = diff1 / timesdiff
        result = np.array([
         np.min(data),
         np.max(data),
         np.std(data),
         np.mean(data),
         np.median(data),
         activity,
         mobility,
         complexity,
         scipy.stats.kurtosis(data),
         np.mean(diff2),
         np.max(diff2),
         np.mean(diff1),
         np.max(diff1),
         scipy.stats.variation(data),
         scipy.stats.skew(data),
         np.mean(cA),
         np.std(cA),
         np.mean(cD),
         np.std(cD),
         np.sum(np.abs(cAf) ** 2) / cAf.size,
         np.sum(np.abs(cDf) ** 2) / cDf.size,
         -np.sum(cA * np.nan_to_num(np.log(cA))),
         -np.sum(cD * np.nan_to_num(np.log(cD))),
         np.mean(diff1Slope),
         np.var(diff1Slope),
         bands['delta']['max'],
         bands['theta']['max'],
         bands['alpha']['max'],
         bands['beta']['max'],
         bands['delta']['sum'] / bands['alpha']['sum'],
         bands['delta']['sum'] / bands['theta']['sum']])
        return result

    def file_extract(self, fepo, fept, ft1, ft2):
        epochs = np.load(fepo, allow_pickle=True)
        times = np.load(fept, allow_pickle=True)
        ftv1 = []
        ftv2 = []
        for ev in range(len(epochs)):
            ftv1.append([])
            ftv2.append([])
            for epo_gr in range(len(epochs[ev])):
                ftv1[(-1)].append([])
                ftv2[(-1)].append([])
                temp_e = np.concatenate(epochs[ev][epo_gr])
                temp_t = np.concatenate(times[ev][epo_gr])
                temp_td = np.diff(temp_t)
                for epo in range(len(epochs[ev][epo_gr])):
                    timesdiff = np.diff(times[ev][epo_gr][epo])
                    ftv1[(-1)][(-1)].append([])
                    for ch in range(epochs[ev][epo_gr][epo].shape[1]):
                        res = self.features_of_channel(epochs[ev][epo_gr][epo][:, ch], timesdiff)
                        if res is not None:
                            ftv1[(-1)][(-1)][(-1)].append(res)
                        if epo == 0:
                            res = self.features_of_channel(temp_e[:, ch], temp_td)
                            if res is not None:
                                ftv2[(-1)][(-1)].append(res)
                            del (len(ftv1[(-1)][(-1)][(-1)]) or ftv1[(-1)][(-1)])[-1]

                    ftv1[(-1)][(-1)][-1] = np.array(ftv1[(-1)][(-1)][(-1)])

                ftv1[(-1)][-1] = np.array(ftv1[(-1)][(-1)])
                ftv2[(-1)][-1] = np.array(ftv2[(-1)][(-1)])

            ftv1[-1] = np.concatenate(ftv1[(-1)])
            ftv2[-1] = np.array(ftv2[(-1)])

        ftv1 = (Utils.list2arr)(*ftv1)
        ftv2 = (Utils.list2arr)(*ftv2)
        np.save(ft1, ftv1)
        np.save(ft2, ftv2)
        del epochs
        del times
        del ftv1
        del ftv2
        del timesdiff
        del temp_e
        del temp_t
        del temp_td
        return True

    def extract_features(self, src='', dest=''):
        print('Extract Features method has been called')
        self.check_src_dest(src, dest, 'Features')
        src = src.rstrip('/')
        dest = dest.rstrip('/')
        ext1, ext2 = self.config.exts.list('epo', 'ept')
        epochs = sorted(glob(src + '/*' + ext1))
        if not len(epochs):
            raise Exception('No Epochs file found')
        print('Extracting features of epoched files')
        for fepo in tqdmn(epochs, ncols=500):
            fname = fepo.split('/')[(-1)][:-len(ext1)]
            fept = fepo[:-len(ext1)] + ext2
            if not os.path.isfile(fept):
                raise Exception('FileNotFound: ' + fept)
            ft1, ft2 = [dest + '/' + fname + ext for ext in self.config.exts.list('ft1', 'ft2')]
            if os.path.isfile(ft1):
                os.path.isfile(ft2) or self.file_extract(fepo, fept, ft1, ft2)