# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/preprocessing/speech.py
# Compiled at: 2019-04-23 04:20:21
# Size of source mod 2**32: 55614 bytes
"""
Note
----
The following order is recommended for extracting spectra:
+ AudioReader:
    - Loading raw audio
    - remove DC offeset and dithering
    - preemphasis
+ SpectraExtractor (or CQTExtractor):
    - Extracting the Spectra
# ===== SAD ===== #
+ SADgmm:
    - Extracting SAD (optional)
+ Read3ColSAD:
    - Generating SAD labels from 3-cols files
# ===== Normalization ===== #
+ Rastafilt:
    - Rastafilt (optional for MFCC)
+ DeltaExtractor (calculated before applying SAD)
    - Calculate Deltas (and shifted delta for MFCCs).
+ ApplyingSAD:
    - Applying SAD indexing on features
+ BNFExtractor:
    - Extracting bottleneck features
+ AcousticNorm
    - Applying CMVN and WCMVN (This is important so the SAD frames
    are not affected by the nosie).
"""
from __future__ import print_function, division, absolute_import
import os, re, six, math, copy, base64, shutil, inspect, warnings
from numbers import Number
from six import string_types
from collections import OrderedDict, Mapping, defaultdict
import numpy as np, tensorflow as tf
from scipy.signal import lfilter
from odin.fuel import Dataset, MmapData, MmapDict
from odin.utils import is_number, cache_memory, is_string, as_tuple, get_all_files, is_pickleable, Progbar, mpi, ctext, is_fileobj, batching
from odin.preprocessing.base import Extractor, ExtractorSignal
from odin.preprocessing.signal import smooth, pre_emphasis, get_window, get_energy, spectra, vad_energy, pitch_track, resample, rastafilt, mvn, wmvn, shifted_deltas, stack_frames, stft, power_spectrogram, mels_spectrogram, ceps_spectrogram, power2db, anything2wav
from odin.preprocessing._opensmile import *
timit_61 = [
 'aa', 'ae', 'ah', 'ao', 'aw', 'ax', 'ax-h', 'axr', 'ay',
 'b', 'bcl', 'ch', 'd', 'dcl', 'dh', 'dx', 'eh', 'el', 'em', 'en',
 'eng', 'epi', 'er', 'ey', 'f', 'g', 'gcl', 'h#', 'hh', 'hv', 'ih',
 'ix', 'iy', 'jh', 'k', 'kcl', 'l', 'm', 'n', 'ng', 'nx', 'ow',
 'oy', 'p', 'pau', 'pcl', 'q', 'r', 's', 'sh', 't', 'tcl', 'th',
 'uh', 'uw', 'ux', 'v', 'w', 'y', 'z', 'zh']
timit_39 = ['aa', 'ae', 'ah', 'aw', 'ay', 'b', 'ch', 'd',
 'dh', 'dx', 'eh', 'er', 'ey', 'f', 'g', 'hh', 'ih', 'iy', 'jh', 'k',
 'l', 'm', 'n', 'ng', 'ow', 'oy', 'p', 'r', 's', 'sh', 'sil', 't',
 'th', 'uh', 'uw', 'v', 'w', 'y', 'z']
timit_map = {'ao':'aa',  'ax':'ah',  'ax-h':'ah',  'axr':'er',  'hv':'hh', 
 'ix':'ih',  'el':'l',  'em':'m',  'en':'n', 
 'nx':'n',  'eng':'ng', 
 'zh':'sh',  'ux':'uw',  'pcl':'sil', 
 'tcl':'sil',  'kcl':'sil',  'bcl':'sil',  'dcl':'sil', 
 'gcl':'sil',  'h#':'sil',  'pau':'sil',  'epi':'sil'}

def _read_pcm(path, encode):
    dtype = np.int16
    sr = None
    if encode is not None:
        if 'ulaw' in encode.lower():
            dtype = np.int8
            sr = 8000
        elif 'vast' in encode.lower():
            dtype = np.int16
            sr = 44000
    raw = np.memmap(path, dtype=dtype, mode='r')
    return (raw, sr)


def read(path_or_file, encode=None):
    """
  Returns
  -------
  audio_array : [n_samples, nb_channels]
    the audio array
  sr : {int, None}
    sample rate
  """
    if is_fileobj(path_or_file):
        f = path_or_file
        f.seek(0)
        path = f.name
    else:
        if os.path.isfile(path_or_file):
            f = None
            path = path_or_file
        else:
            raise ValueError('Invalid type of `path_or_file` %s' % str(type(path_or_file)))
        if '.pcm' in path.lower():
            f = open(path_or_file, 'rb')
            raw, sr = _read_pcm(f, encode=encode)
        else:
            import soundfile
            try:
                f = open(path_or_file, 'rb')
                raw, sr = soundfile.read(f)
            except Exception as e:
                if '.sph' in f.name.lower():
                    f = open(path_or_file, 'rb')
                    raw, sr = _read_pcm(f, encode=encode)
                else:
                    raw, sr = anything2wav(inpath=path, outpath=None, codec=encode,
                      return_data=True)

    if f is not None:
        f.close()
    return (
     raw, sr)


def save(file_or_path, s, sr, subtype=None):
    """
  Parameters
  ----------
  s : array_like
      The data to write.  Usually two-dimensional (channels x frames),
      but one-dimensional `data` can be used for mono files.
      Only the data types ``'float64'``, ``'float32'``, ``'int32'``
      and ``'int16'`` are supported.

      .. note:: The data type of `data` does **not** select the data
                type of the written file. Audio data will be
                converted to the given `subtype`. Writing int values
                to a float file will *not* scale the values to
                [-1.0, 1.0). If you write the value ``np.array([42],
                dtype='int32')``, to a ``subtype='FLOAT'`` file, the
                file will then contain ``np.array([42.],
                dtype='float32')``.
  subtype: str
      'PCM_24': 'Signed 24 bit PCM'
      'PCM_16': 'Signed 16 bit PCM'
      'PCM_S8': 'Signed 8 bit PCM'

  Return
  ------
  waveform (ndarray), sample rate (int)
  """
    from soundfile import write
    return write(file_or_path, s, sr, subtype=subtype)


def _extract_frame_step_length(sr, frame_length, step_length):
    if frame_length < 1.0:
        frame_length = int(sr * frame_length)
    else:
        frame_length = int(frame_length)
    if step_length is None:
        step_length = frame_length // 4
    else:
        if step_length < 1.0:
            step_length = int(sr * step_length)
        else:
            step_length = int(step_length)
    return (
     frame_length, step_length)


@cache_memory
def _num_two_factors(x):
    """return number of times x is divideable for 2"""
    if x <= 0:
        return 0
    else:
        num_twos = 0
        while x % 2 == 0:
            num_twos += 1
            x //= 2

        return num_twos


@cache_memory
def _max_fft_bins(sr, n_fft, fmax):
    return [i + 1 for i, j in enumerate(np.linspace(0, (float(sr) / 2), (int(1 + n_fft // 2)), endpoint=True)) if j >= fmax][0]


def audio_segmenter(files, outpath, max_duration, sr=None, sr_new=None, best_resample=True, override=False):
    """ Segment all given files into small chunks, the new file
  name is formatted as:
   - [name_without_extension].[ID].wav

  The information for each segment is saved at a csv file:
   - [outpath]/segments.csv

  Note
  ----
  We separated the segmenter from FeatureProcessor, since you can try
  different configuration for the features on the same set of segments,
  it is efficient to do this once-for-all.
  """
    info_path = os.path.join(outpath, 'segments.csv')
    max_duration = int(max_duration)
    files = [f for f in as_tuple(files, t=str) if os.path.isfile(f)]
    outpath = str(outpath)
    if os.path.isfile(outpath):
        raise ValueError('outpath at: %s is a file.' % outpath)
    if os.path.isdir(outpath):
        if not override:
            return info_path
        shutil.rmtree(outpath)
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
    reader = AudioReader(sr=sr, sr_new=sr_new, best_resample=best_resample, remove_dc_n_dither=False,
      preemphasis=None)

    def segmenting(f):
        raw = reader.transform(f)
        path, sr, raw = raw['path'], raw['sr'], raw['raw']
        segs = [int(np.round(i)) for i in np.linspace(start=0,
          stop=(raw.shape[0]),
          num=(int(np.ceil(raw.shape[0] / (sr * max_duration))) + 1),
          endpoint=True)]
        indices = list(zip(segs, segs[1:]))
        name = os.path.basename(path)
        info = []
        for idx, (s, e) in enumerate(indices):
            y = raw[s:e]
            seg_name = name.split('.')[:-1] + [str(idx), 'wav']
            seg_name = '.'.join(seg_name)
            save(os.path.join(outpath, seg_name), y, sr)
            info.append((seg_name, s / sr, e / sr))

        return (
         path, info)

    nb_files = len(files)
    prog = Progbar(target=nb_files, print_summary=True, print_report=True, name=('Segmenting to path: %s' % outpath))
    task = mpi.MPI(jobs=files, func=segmenting, ncpu=None,
      batch=1,
      backend='python')
    seg_indices = []
    for f, info in task:
        prog['File'] = f
        prog['#Segs'] = len(info)
        assert all(e - s <= max_duration for name, s, e in info), 'Results contain segments > max duration, file: %s, segs: %s' % (
         f, str(info))
        for seg, s, e in info:
            seg_indices.append((seg, os.path.basename(f), s, e))

        prog.add(1)

    header = ' '.join(['segment', 'origin', 'start', 'end'])
    np.savetxt(info_path, seg_indices, fmt='%s',
      delimiter=' ',
      header=header,
      comments='')
    print('Segment info saved at:', ctext(info_path, 'cyan'))
    return info_path


class AudioReader(Extractor):
    __doc__ = " Return a dictionary of\n  {\n      'raw': loaded_signal,\n      'duration': in second,\n      'sr': sample rate,\n      'path': path_to_loaded_file\n  }\n\n  Parameters\n  ----------\n  sr: int or None\n      provided sr for missing sr audio (i.e. pcm files),\n      NOTE this value only used when cannot find `sr` information\n      from audio file (example: reading raw pcm).\n  sr_new: int or None\n      resample sample rate for all provided audio, only\n      support downsample (i.e. must be smaller than sr).\n  remove_dc_n_dither : bool\n    dithering adds noise to the signal to remove periodic noise\n\n  Input\n  -----\n  path_or_array: string, tuple, list, mapping\n      - string for path\n      - tuple or list for (path-or-raw, sr)\n      - mapping for provding additional information include:\n      sr, encode (ulaw, vast), 'raw' or 'path'\n\n  Note\n  ----\n  Dithering introduces white noise when you save the raw array into\n  audio file.\n  For now only support one channel\n  "

    def __init__(self, sr=None, sr_new=None, best_resample=True, remove_dc=True, dataset=None):
        super(AudioReader, self).__init__(is_input_layer=True)
        self.sr = sr
        self.sr_new = sr_new
        self.best_resample = best_resample
        self.remove_dc = bool(remove_dc)
        if is_string(dataset):
            if os.path.isdir(dataset):
                dataset = Dataset(dataset)
        if dataset is not None:
            if not isinstance(dataset, Dataset):
                raise ValueError('dataset can be instance of odin.fuel.Dataset or None')
        self.dataset = dataset

    def _transform(self, path_or_array):
        raw = None
        sr = None
        name = None
        path = None
        duration = None
        encode = None
        channel = None
        if isinstance(path_or_array, Mapping):
            if 'sr' in path_or_array:
                sr = int(path_or_array['sr'])
            else:
                if 'encode' in path_or_array:
                    encode = str(path_or_array['encode'])
                if 'channel' in path_or_array:
                    channel = int(path_or_array['channel'])
                if 'raw' in path_or_array:
                    raw = path_or_array['raw']
                else:
                    if 'path' in path_or_array:
                        path = str(path_or_array['path'])
                        raw, sr = read(path, encode=encode)
                    else:
                        raise ValueError('`path_or_array` can be a dictionary, contains following key: sr, raw, path. One of the key `raw` for raw array signal, or `path` for path to audio file must be specified.')
        elif is_string(path_or_array):
            path = path_or_array
            if os.path.isfile(path_or_array):
                raw, sr = read(path_or_array, encode=encode)
            else:
                if self.dataset is not None:
                    start, end = self.dataset['indices'][path_or_array]
                    raw = self.dataset['raw'][start:end]
                    sr = int(self.dataset['sr'][path_or_array])
                    name = path_or_array
                    if 'path' in self.dataset:
                        path = self.dataset['path'][path_or_array]
                else:
                    raise ValueError('Cannot locate file at path: %s' % path_or_array)
        else:
            if is_fileobj(path_or_array):
                path = path_or_array.name
                raw, sr = read(path_or_array, encode=encode)
            else:
                raise ValueError('`path_or_array` can be: list, tuple, Mapping, string, file. But given: %s' % str(type(path_or_array)))
            raw = raw.astype('float32')
            if raw.ndim == 1:
                pass
            else:
                if raw.ndim == 2:
                    if raw.shape[0] == 2:
                        raw = raw.T
                    else:
                        if channel is not None:
                            raw = raw[:, channel]
                        else:
                            raise ValueError('No support for %d-D signal from file: %s' % (
                             raw.ndim, path))
                        if sr is None:
                            if self.sr is not None:
                                sr = int(self.sr)
                        if sr is not None:
                            if self.sr_new is not None:
                                raw = resample(raw, sr, (self.sr_new), best_algorithm=(self.best_resample))
                                sr = int(self.sr_new)
                        if self.remove_dc:
                            raw = raw - np.mean(raw, 0).astype(raw.dtype)
                    if sr is not None:
                        duration = max(raw.shape) / sr
                else:
                    if path is not None:
                        if not is_string(path):
                            path = str(path, 'utf-8')
                        if '/' != path[0]:
                            path = os.path.abspath(path)
                    ret = {'raw':raw, 
                     'sr':sr,  'duration':duration,  'path':path}
                    if name is not None:
                        ret['name'] = name
                return ret


class AudioAugmentor(Extractor):
    __doc__ = ' SREAugmentor\n\n  New name for each utterance is:\n    [utt_name]/[noise1_name]/[noise2_name]...\n  '

    def __init__(self, musan_path, rirs_path):
        super(AudioAugmentor, self).__init__(is_input_layer=False)

    def _transform(self, row):
        pass


class Dithering(Extractor):
    __doc__ = ' Dithering '

    def __init__(self, input_name=('raw', 'sr'), output_name='raw'):
        super(Dithering, self).__init__(input_name=as_tuple(input_name, t=string_types),
          output_name=(str(output_name)))

    def _transform(self, feat):
        raw, sr = [feat[name] for name in self.input_name]
        if max(abs(raw)) <= 1.0:
            raw = raw * 32768
        else:
            if sr == 16000:
                alpha = 0.99
            else:
                if sr == 8000:
                    alpha = 0.999
                else:
                    raise ValueError('Sampling frequency %s not supported' % sr)
        slen = raw.size
        raw = lfilter([1, -1], [1, -alpha], raw)
        dither = np.random.rand(slen) + np.random.rand(slen) - 1
        s_pow = max(raw.std(), 1e-20)
        raw = raw + 1e-06 * s_pow * dither
        return {self.output_name: raw}


class PreEmphasis(Extractor):
    __doc__ = ' PreEmphasis\n\n  Parameters\n  ----------\n  coeff : float (0-1)\n      pre-emphasis filter, if 0 or None, no filter applied\n  input_name : string\n      name of raw signal in the features pipeline dictionary\n\n  '

    def __init__(self, coeff=0.97, input_name='raw', output_name='raw'):
        super(PreEmphasis, self).__init__(input_name=(str(input_name)), output_name=(str(output_name)))
        assert 0.0 < coeff < 1.0
        self.coeff = float(coeff)

    def _transform(self, feat):
        raw = feat[self.input_name]
        if not 0 < raw.ndim <= 2:
            raise ValueError('Only supper 1 or 2 channel audio but given shape: %s' % str(raw.shape))
        return {self.output_name: pre_emphasis(raw, coeff=(self.coeff))}


class Framing(Extractor):
    __doc__ = ' Framing\n\n  Parameters\n  ----------\n\n  '

    def __init__(self, frame_length, step_length=None, window='hamm', padding=False, input_name=('raw', 'sr'), output_name='frames'):
        if isinstance(input_name, string_types):
            input_name = (
             input_name, 'sr')
        else:
            assert isinstance(output_name, string_types), '`output_name` must be string'
            super(Framing, self).__init__(input_name=input_name, output_name=output_name)
            if step_length is None:
                step_length = frame_length // 4
        self.frame_length = frame_length
        self.step_length = step_length
        self.window = window
        self.padding = bool(padding)

    def _transform(self, y_sr):
        y, sr = [y_sr[name] for name in self.input_name]
        frame_length, step_length = _extract_frame_step_length(sr, self.frame_length, self.step_length)
        if self.padding:
            y = np.pad(y, (int(frame_length // 2)), mode='constant')
        else:
            shape = y.shape[:-1] + (y.shape[(-1)] - frame_length + 1, frame_length)
            strides = y.strides + (y.strides[(-1)],)
            y_frames = np.lib.stride_tricks.as_strided(y, shape=shape, strides=strides)
            if y_frames.ndim > 2:
                y_frames = np.rollaxis(y_frames, 1)
            y_frames = y_frames[::step_length]
            if self.window is not None:
                fft_window = get_window((self.window),
                  frame_length, periodic=True).reshape(1, -1)
                y_frames = fft_window * y_frames
                scale = np.sqrt(1.0 / fft_window.sum() ** 2)
            else:
                scale = np.sqrt(1.0 / frame_length ** 2)
        return {self.output_name: y_frames, 
         'scale': scale}


class CalculateEnergy(Extractor):
    __doc__ = '\n  Parameters\n  ----------\n  log : bool (default: True)\n    take the natural logarithm of the energy\n\n  Input\n  -----\n  numpy.ndarray : 2D [n_samples, n_features]\n\n  Output\n  ------\n  numpy.ndarray : 1D [n_samples,]\n    Energy for each frames\n\n  '

    def __init__(self, log=True, input_name='frames', output_name='energy'):
        super(CalculateEnergy, self).__init__(input_name=(str(input_name)), output_name=(str(output_name)))
        self.log = bool(log)

    def _transform(self, X):
        frames = X[self.input_name]
        energy = get_energy(frames, log=(self.log)).astype('float32')
        return {self.output_name: energy}


class STFTExtractor(Extractor):
    __doc__ = " Short time Fourier transform\n  `window` should be `None` if input is windowed framed signal\n\n  Parameters\n  ----------\n  frame_length: {int, float}\n      number of samples point for 1 frame, or length of frame in millisecond\n  step_length: {int, float}\n      number of samples point for 1 step (when shifting the frames),\n      or length of step in millisecond\n      If unspecified, defaults `win_length / 4`.\n  n_fft: int > 0 [scalar]\n      FFT window size\n      If not provided, uses the smallest power of 2 enclosing `frame_length`.\n\n  scale : {None, string, float}\n      value for scaling the matrix after STFT, important for\n      iSTFT afterward\n      if None, no extra scale is performed\n      if string, looking for feature with given name in the pipeline\n      if float, directly using given value for scaling\n\n  Input\n  -----\n  numpy.ndarray : [n_samples,] or [n_frames, frame_length]\n    raw signal or framed signal\n  integer : > 0\n    sample rate of the audio\n\n  Output\n  ------\n  'stft' : complex64 array [time, frequency]\n  'stft_energy' : float32 array [time, 1]\n  "

    def __init__(self, frame_length=None, step_length=None, n_fft=512, window='hamm', padding=False, energy=True, scale=None, input_name=('raw', 'sr'), output_name='stft'):
        if isinstance(input_name, string_types):
            input_name = (
             input_name, 'sr')
        else:
            assert isinstance(output_name, string_types), '`output_name` must be string'
            super(STFTExtractor, self).__init__(input_name=input_name, output_name=output_name)
            self.frame_length = frame_length
            self.step_length = step_length
            self.n_fft = n_fft
            self.window = window
            self.padding = bool(padding)
            self.energy = bool(energy)
            assert isinstance(scale, (string_types, Number, type(None)))
        self.scale = scale

    def _transform(self, y_sr):
        y, sr = [y_sr[name] for name in self.input_name]
        scale = self.scale
        if isinstance(scale, string_types):
            scale = y_sr[scale]
        else:
            if self.frame_length is None:
                if y.ndim == 2:
                    if y.shape[1] > 2:
                        frame_length = y.shape[1]
                        step_length = None
                raise ValueError('`frame_length` is not provided, the input to the extractor must be framed signal from `odin.preprocessing.speech.Framing`')
            else:
                frame_length, step_length = _extract_frame_step_length(sr, self.frame_length, self.step_length)
        results = stft(y=y, frame_length=frame_length,
          step_length=step_length,
          n_fft=(self.n_fft),
          window=(self.window),
          scale=scale,
          padding=(self.padding),
          energy=(self.energy))
        if self.energy:
            s, e = results
            return {self.output_name: s, 
             '%s_energy' % self.output_name: e}
        else:
            return {self.output_name: results}


class PowerSpecExtractor(Extractor):
    __doc__ = " Extract power spectrogram from complex STFT array\n\n  Output\n  ------\n  'spec' : [time, n_fft / 2 + 1]\n\n  "

    def __init__(self, power=2.0, input_name='stft', output_name='spec'):
        super(PowerSpecExtractor, self).__init__(input_name=input_name, output_name=output_name)
        self.power = float(power)

    def _transform(self, X):
        return power_spectrogram(S=(X[self.input_name]), power=(self.power))


class MelsSpecExtractor(Extractor):
    __doc__ = "\n  Parameters\n  ----------\n  input_name : (string, string) (default: ('spec', 'sr'))\n    the name of spectrogram and sample rate in the feature pipeline\n\n  Output\n  ------\n  'mspec' : [time, n_mels]\n\n  "

    def __init__(self, n_mels, fmin=64, fmax=None, top_db=80.0, input_name=('spec', 'sr'), output_name='mspec'):
        if isinstance(input_name, string_types):
            input_name = (
             input_name, 'sr')
        super(MelsSpecExtractor, self).__init__(input_name=input_name, output_name=output_name)
        self.n_mels = int(n_mels)
        self.fmin = fmin
        self.fmax = fmax
        self.top_db = top_db

    def _transform(self, X):
        return mels_spectrogram(spec=(X[self.input_name[0]]), sr=(X[self.input_name[1]]), n_mels=(self.n_mels),
          fmin=(self.fmin),
          fmax=(self.fmax),
          top_db=(self.top_db))


class MFCCsExtractor(Extractor):
    __doc__ = '\n  '

    def __init__(self, n_ceps, remove_first_coef=True, first_coef_energy=False, input_name='mspec', output_name='mfcc'):
        super(MFCCsExtractor, self).__init__(input_name=input_name, output_name=output_name)
        self.n_ceps = int(n_ceps)
        self.remove_first_coef = bool(remove_first_coef)
        self.first_coef_energy = bool(first_coef_energy)

    def _transform(self, X):
        n_ceps = self.n_ceps
        if self.remove_first_coef:
            n_ceps += 1
        mfcc = ceps_spectrogram(mspec=(X[self.input_name]), n_ceps=n_ceps,
          remove_first_coef=False)
        ret = {self.output_name: mfcc[:, 1:] if self.remove_first_coef else mfcc}
        if self.first_coef_energy:
            ret['%s_energy' % self.output_name] = mfcc[:, 0]
        return ret


class Power2Db(Extractor):
    __doc__ = ' Convert power spectrogram to Decibel spectrogram\n\n  '

    def __init__(self, input_name, output_name=None, top_db=80.0):
        input_name = as_tuple(input_name, t=string_types)
        super(Power2Db, self).__init__(input_name=input_name, output_name=output_name)
        self.top_db = float(top_db)

    def _transform(self, X):
        return [power2db(S=(X[name]), top_db=(self.top_db)) for name in self.input_name]


class SpectraExtractor(Extractor):
    __doc__ = 'AcousticExtractor\n\n  Parameters\n  ----------\n  frame_length: {int, float}\n      number of samples point for 1 frame, or length of frame in millisecond\n  step_length: {int, float}\n      number of samples point for 1 step (when shifting the frames),\n      or length of step in millisecond\n      If unspecified, defaults `win_length / 4`.\n  n_fft: int > 0 [scalar]\n      FFT window size\n      If not provided, uses the smallest power of 2 enclosing `frame_length`.\n  window : string, tuple, number, function, or np.ndarray [shape=(n_fft,)]\n      - a window specification (string, tuple, or number);\n        see `scipy.signal.get_window`\n      - a window function, such as `scipy.signal.hanning`\n      - a vector or array of length `n_fft`\n  power : float > 0 [scalar]\n      Exponent for the magnitude spectrogram.\n      e.g., 1 for energy (or magnitude), 2 for power, etc.\n  log: bool\n      if True, convert all power spectrogram to DB\n  padding : bool\n      - If `True`, the signal `y` is padded so that frame\n        `D[:, t]` is centered at `y[t * hop_length]`.\n      - If `False`, then `D[:, t]` begins at `y[t * hop_length]`\n  '

    def __init__(self, frame_length, step_length=None, n_fft=512, window='hann', n_mels=None, n_ceps=None, fmin=64, fmax=None, power=2.0, log=True, padding=False, input_name=('raw', 'sr')):
        super(SpectraExtractor, self).__init__(input_name=input_name)
        self.frame_length = frame_length
        self.step_length = step_length
        self.n_fft = n_fft
        self.window = window
        self.n_mels = n_mels
        self.n_ceps = n_ceps
        self.fmin = fmin
        self.fmax = fmax
        self.power = float(power)
        self.log = bool(log)
        self.padding = bool(padding)

    def _transform(self, y_sr):
        y, sr = [y_sr[i] for i in self.input_name]
        frame_length, step_length = _extract_frame_step_length(sr, self.frame_length, self.step_length)
        feat = spectra(sr=sr, frame_length=frame_length, y=y, S=None, step_length=step_length,
          n_fft=(self.n_fft),
          window=(self.window),
          n_mels=(self.n_mels),
          n_ceps=(self.n_ceps),
          fmin=(self.fmin),
          fmax=(self.fmax),
          top_db=80.0,
          power=(self.power),
          log=(self.log),
          padding=(self.padding))
        return feat


class CQTExtractor(Extractor):
    __doc__ = ' Constant-Q transform\n  Using log-scale instead of linear-scale frequencies for\n  signal analysis\n\n  '

    def __init__(self, frame_length, step_length=None, n_bins=96, window='hann', n_mels=None, n_ceps=None, fmin=64, fmax=None, padding=False, input_name=('raw', 'sr')):
        super(CQTExtractor, self).__init__(input_name=input_name)
        self.frame_length = frame_length
        self.step_length = step_length
        self.n_bins = int(n_bins)
        self.window = window
        self.n_mels = n_mels
        self.n_ceps = n_ceps
        self.fmin = fmin
        self.fmax = fmax
        self.padding = padding

    def _transform(self, y_sr):
        y, sr = [y_sr[name] for name in self.input_name]
        frame_length, step_length = _extract_frame_step_length(sr, self.frame_length, self.step_length)
        from librosa.core import constantq
        bins_per_octave = np.ceil(float(self.n_bins - 1) / np.log2(sr / 2.0 / self.fmin)) + 1
        if _num_two_factors(step_length) < np.ceil(self.n_bins / bins_per_octave) - 1:
            bins_per_octave = np.ceil(self.n_bins / (_num_two_factors(step_length) + 1))
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=DeprecationWarning)
            qtrans = constantq.cqt(y=y, sr=sr, hop_length=step_length, n_bins=(self.n_bins), bins_per_octave=(int(bins_per_octave)),
              fmin=(self.fmin),
              tuning=0.0,
              norm=1,
              filter_scale=1.0,
              sparsity=0.01).astype('complex64')
        feat = spectra(sr=sr, frame_length=frame_length, y=None, S=(qtrans.T), step_length=step_length,
          n_fft=None,
          window='hann',
          n_mels=(self.n_mels),
          n_ceps=(self.n_ceps),
          fmin=64,
          fmax=(self.fmax),
          top_db=80.0,
          power=2.0,
          log=True,
          padding=(self.padding))
        feat = {'q' + name:X for name, X in feat.items()}
        return feat


class _BNFExtractorBase(Extractor):
    __doc__ = ' _BNFExtractorBase '

    def __init__(self, input_name, network, output_name='bnf', sad_name='sad', remove_non_speech=True, stack_context=10, pre_mvn=True, batch_size=2048):
        if not isinstance(input_name, string_types):
            raise AssertionError('`input_name` must be string')
        else:
            if isinstance(sad_name, string_types):
                input_name = (
                 input_name, sad_name)
                self.use_sad = True
            else:
                self.use_sad = False
        self.remove_non_speech = bool(remove_non_speech)
        super(_BNFExtractorBase, self).__init__(input_name=input_name,
          output_name=output_name)
        if stack_context is None:
            stack_context = 0
        self.stack_context = int(stack_context)
        self.pre_mvn = bool(pre_mvn)
        self.batch_size = int(batch_size)
        self._prepare_network(network)

    def _prepare_input(self, X, sad):
        X_sad = X[sad] if sad is not None else X
        if self.pre_mvn:
            X = (X - X_sad.mean(0, keepdims=True)) / (X_sad.std(0, keepdims=True) + 1e-18)
        if self.stack_context > 0:
            X = stack_frames(X, frame_length=(self.stack_context * 2 + 1), step_length=1,
              keep_length=True,
              make_contigous=True)
        if self.remove_non_speech:
            if sad is not None:
                X = X[sad]
        return X

    def _transform(self, feat):
        if self.use_sad:
            X, sad = feat[self.input_name[0]], feat[self.input_name[1]]
            sad = sad.astype('bool')
            assert len(sad) == len(X), 'Input mismatch, `sad` has shape: %s, and input feature with name: %s; shape: %s' % (
             sad.shape, self.input_name[0], X.shape)
        else:
            X = feat[self.input_name]
            sad = None
        X = self._prepare_input(X, sad)
        y = []
        for s, e in batching(n=(X.shape[0]), batch_size=(self.batch_size)):
            y.append(self._apply_dnn(X[s:e]))

        return np.concatenate(y, axis=0)

    def _prepare_network(self, network):
        raise NotImplementedError

    def _apply_dnn(self, X):
        raise NotImplementedError


class BNFExtractorCPU(_BNFExtractorBase):
    __doc__ = " Deep bottleneck feature extractor\n  The following order of preprocessing features for BNF are suggested:\n  * extract input features: `X`\n  * extract sad: `S`\n  * normalize by speech activities: `X = (X - X[S].mean()) / X[S].std()`\n  * Stacking features: `X = stacking(X, context=10)`\n  => X_bnf = network(X)\n\n  Parameters\n  ----------\n  input_feat : str\n    name of input feature\n  network : odin.nnet.base.NNOp\n    instance pre-trained NNOp\n  pre_mvn : bool (default: False)\n    perform mean-variance normalization before stacking,\n    then, feeding data to network.\n  sad_name : {str, None}\n    if None, or `sad_name` not found, don't applying SAD to\n    the input feature before BNF\n  remove_non_speech : bool (default: True)\n    if True, remove non-speech frames using given SAD\n  batch_size : int\n    batch size when feeding data to the network, suggest\n    to have as much data as possible.\n\n  Note\n  ----\n  Order of preprocessing for BNF:\n   - delta and delta delta extraction (optional)\n   - mean_var_norm based on SAD frames statistics.\n   - Stacking the left and right context frames.\n   - Applying SAD indices.\n   - Mean-variance normalization\n   => BNFExtractor\n\n  "

    def _prepare_network(self, network):
        from odin.nnet.models.bnf import _BNFbase
        if isinstance(network, _BNFbase):
            network = network.__class__
        else:
            assert isinstance(network, type) and issubclass(network, _BNFbase), '`network` must be a subclass of odin.nnet.models.Model, but given: %s' % str(network)
            params = network.load_parameters()
            self.weights = [params[name][:] for name in sorted([key for key in params.keys() if 'w' == key[0]])]
            self.biases = [params[name][:] for name in sorted([key for key in params.keys() if 'b' == key[0]])]
            assert len(self.weights) == len(self.biases), 'Number of weights is: %d; but number of biases is: %s' % (
             len(self.weights), len(self.biases))

    def _renorm_rms(self, x, target_rms=1.0, axis=0):
        """ scales the data such that RMS is 1.0 """
        D = np.sqrt(x.shape[axis])
        x_rms = np.sqrt(np.sum((x * x), axis=axis, keepdims=True)) / D
        x_rms[x_rms == 0] = 1.0
        return target_rms * x / x_rms

    def _apply_dnn(self, X):
        assert X.shape[1] == self.weights[0].shape[1], 'Input must has dimension (?, %d) but given tensor with shape: %s' % (
         self.weights[0].shape[0], str(X.shape))
        X = X.T
        for wi, bi in zip(self.weights[:-1], self.biases[:-1]):
            X = wi.dot(X) + bi
            np.maximum(X, 0, out=X)
            X = self._renorm_rms(X, axis=0)

        X = self.weights[(-1)].dot(X) + self.biases[(-1)]
        return X.T


class BNFExtractor(_BNFExtractorBase):
    __doc__ = " Deep bottleneck feature extractor\n  The following order of preprocessing features for BNF are suggested:\n  * extract input features: `X`\n  * extract sad: `S`\n  * normalize by speech activities: `X = (X - X[S].mean()) / X[S].std()`\n  * Stacking features: `X = stacking(X, context=10)`\n  => X_bnf = network(X)\n\n  Parameters\n  ----------\n  input_feat : str\n    name of input feature\n  network : odin.nnet.base.NNOp\n    instance pre-trained NNOp\n  pre_mvn : bool (default: False)\n    perform mean-variance normalization before stacking,\n    then, feeding data to network.\n  sad_name : {str, None}\n    if None, or `sad_name` not found, don't applying SAD to\n    the input feature before BNF\n  remove_non_speech : bool (default: True)\n    if True, remove non-speech frames using given SAD\n  batch_size : int\n    batch size when feeding data to the network, suggest\n    to have as much data as possible.\n\n  Note\n  ----\n  Order of preprocessing for BNF:\n   - delta and delta delta extraction (optional)\n   - mean_var_norm based on SAD frames statistics.\n   - Stacking the left and right context frames.\n   - Applying SAD indices.\n   - Mean-variance normalization\n   => BNFExtractor\n\n  "

    def _prepare_network(self, network):
        from odin.nnet import NNOp
        if not isinstance(network, NNOp):
            raise ValueError('`network` must be instance of odin.nnet.NNOp')
        self.network = network

    def _apply_dnn(self, X):
        return self.network(X)

    def __getstate__(self):
        from odin import nnet as N, backend as K
        if not self.network.is_initialized:
            self.network()
        K.initialize_all_variables()
        return (self._input_name, self._output_name,
         self.use_sad, self.batch_size, self.stack_context, self.pre_mvn,
         N.serialize((self.network), binary_output=True))

    def __setstate__(self, states):
        from odin import nnet as N
        self._input_name, self._output_name, self.use_sad, self.batch_size, self.stack_context, self.pre_mvn, self.network = states
        self.network = N.deserialize((self.network), force_restore_vars=False)


class PitchExtractor(Extractor):
    __doc__ = "\n  Parameters\n  ----------\n  threshold : float, optional\n      Voice/unvoiced threshold. Default is 0.3 (as suggested for SWIPE)\n      Threshold >= 1.0 is suggested for RAPT\n  algo: 'swipe', 'rapt', 'avg'\n      swipe - A Saw-tooth Waveform Inspired Pitch Estimation.\n      rapt - a robust algorithm for pitch tracking.\n      avg - apply swipe and rapt at the same time, then take average.\n      Default is 'swipe'\n\n  "

    def __init__(self, frame_length, step_length=None, threshold=0.5, fmin=20, fmax=400, algo='swipe', f0=False, input_name=('raw', 'sr')):
        super(PitchExtractor, self).__init__(input_name=input_name)
        self.threshold = threshold
        self.fmin = int(fmin)
        self.fmax = int(fmax)
        self.algo = algo
        self.f0 = f0
        self.frame_length = frame_length
        self.step_length = step_length

    def _transform(self, y_sr):
        y, sr = [y_sr[name] for name in self.input_name]
        frame_length, step_length = _extract_frame_step_length(sr, self.frame_length, self.step_length)
        pitch_freq = pitch_track(y=y, sr=sr, step_length=step_length, fmin=(self.fmin), fmax=(self.fmax),
          threshold=(self.threshold),
          otype='pitch',
          algorithm=(self.algo))
        pitch_freq = np.expand_dims(pitch_freq, axis=(-1))
        if self.f0:
            f0_freq = pitch_track(y=y, sr=sr, step_length=step_length, fmin=(self.fmin), fmax=(self.fmax),
              threshold=(self.threshold),
              otype='f0',
              algorithm=(self.algo))
            f0_freq = np.expand_dims(f0_freq, axis=(-1))
            return {'pitch':pitch_freq, 
             'f0':f0_freq}
        else:
            return {'pitch': pitch_freq}


def _numba_thresholding(energy, energy_threshold, energy_mean_scale, frame_context, proportion_threshold):
    """ Using this numba function if at least 5 time faster than
  python/numpy implementation """
    n_frames = len(energy)
    e_min = np.min(energy)
    e_max = np.max(energy)
    energy = (energy - e_min) / (e_max - e_min)
    if energy_mean_scale != 0:
        energy_threshold += energy_mean_scale * np.sum(energy) / n_frames
    sad = np.empty(shape=(n_frames,))
    for t in range(n_frames):
        num_count = 0
        den_count = 0
        for t2 in range(t - frame_context, t + frame_context + 1):
            if 0 <= t2 < n_frames:
                den_count += 1
                if energy[t2] > energy_threshold:
                    num_count += 1

        if num_count >= den_count * proportion_threshold:
            sad[t] = 1
        else:
            sad[t] = 0

    return (
     sad, energy_threshold)


try:
    import numba as nb
    _numba_thresholding = nb.jit(nopython=True, nogil=True)(_numba_thresholding)
except ImportError as e:
    pass

class SADthreshold(Extractor):
    __doc__ = ' Compute voice-activity vector for a file: 1 if we judge the frame as\n  voiced, 0 otherwise.  There are no continuity constraints.\n  This method is a very simple energy-based method which only looks\n  at the first coefficient of "input_features", which is assumed to\n  be a log-energy or something similar.  A cutoff is set-- we use\n  a formula of the general type: cutoff = 5.0 + 0.5 * (average log-energy\n  in this file), and for each frame the decision is based on the\n  proportion of frames in a context window around the current frame,\n  which are above this cutoff.\n\n  This method is geared toward speaker-id applications and is not suitable\n  for automatic speech recognition (ASR) because it makes independent\n  decisions for each frame without imposing any notion of continuity.\n\n  This function is optimized by numba, hence, the performance is\n  comparable to kaldi-C code\n\n  Parameters\n  ----------\n  energy_threshold : float (default: 0.55)\n    value from [0., 1.], constant term in energy threshold\n    for MFCC0 for SAD, the higher the value, the more strict\n    the SAD\n\n  energy_mean_scale : float (default: 0.5)\n    If this is set, to get the actual threshold we let m be the mean\n    log-energy of the file, and use `s*m + vad-energy-threshold`\n\n  frames_context : float (default: 2)\n    Number of frames of context on each side of central frame,\n    in window for which energy is monitored\n\n  proportion_threshold : float (default: 0.12)\n    Parameter controlling the proportion of frames within\n    the window that need to have more energy than the\n    threshold\n\n  smooth_window : int (default: 5)\n    smooth the transition between SAD windows, the higher the value\n    the more continuity of the SAD\n\n  Note\n  ----\n  This implementation is slightly different from kaldi implementation,\n  we normalize the energy to [0, 1] and thresholding based on\n  these values\n\n  This algorithm could fail if there is significant amount\n  of noise in the audio, then it treats all frames as non-speech\n\n  Copyright\n  ---------\n  Daniel Povey, voice-activity-detection.cc, kaldi toolkit\n\n  '

    def __init__(self, energy_threshold=0.55, energy_mean_scale=0.5, frame_context=2, proportion_threshold=0.12, smooth_window=5, input_name='energy', output_name='sad'):
        super(SADthreshold, self).__init__(input_name=(str(input_name)), output_name=(str(output_name)))
        self.energy_threshold = float(energy_threshold)
        self.energy_mean_scale = float(energy_mean_scale)
        self.proportion_threshold = float(proportion_threshold)
        self.frame_context = int(frame_context)
        self.smooth_window = int(smooth_window)
        if not self.energy_mean_scale > 0:
            raise AssertionError('energy_mean_scale > 0, given: %.2f' % self.energy_mean_scale)
        else:
            assert self.frame_context >= 0, 'frame_context >= 0, given: %d' % self.frame_context
            assert 0.0 < self.proportion_threshold < 1.0, '0 < proportion_threshold < 1, given: %.2f' % self.proportion_threshold

    def _transform(self, X):
        energy = X[self.input_name]
        if energy.ndim > 1:
            energy = np.squeeze(energy)
        elif not energy.ndim == 1:
            raise AssertionError('Only support 1-D energy')
        sad, energy_threshold = _numba_thresholding(energy.astype('float32'), self.energy_threshold, self.energy_mean_scale, self.frame_context, self.proportion_threshold)
        sad = sad.astype('uint8')
        if self.smooth_window > 0:
            threshold = 2.0 / self.smooth_window
            sad = smooth(x=sad, win=(self.smooth_window), window='flat') >= threshold
        return {self.output_name: sad, 
         '%s_threshold' % self.output_name: energy_threshold}


class SADgmm(Extractor):
    __doc__ = ' GMM-based SAD extractor\n\n  Note\n  ----\n  This method can completely fail for very noisy audio, or audio\n  with very long silence\n  '

    def __init__(self, nb_mixture=3, nb_train_it=25, smooth_window=3, input_name='energy', output_name='sad'):
        super(SADgmm, self).__init__(input_name=input_name, output_name=output_name)
        self.nb_mixture = int(nb_mixture)
        self.nb_train_it = int(nb_train_it)
        self.smooth_window = int(smooth_window)

    def _transform(self, feat):
        features = feat[self.input_name]
        if features.ndim > 1:
            features = features.sum(axis=(-1))
        sad, sad_threshold = vad_energy(log_energy=(features.ravel()), distrib_nb=(self.nb_mixture),
          nb_train_it=(self.nb_train_it))
        if self.smooth_window > 0:
            threshold = 2.0 / self.smooth_window
            sad = smooth(sad, win=(self.smooth_window), window='flat') >= threshold
        sad = sad.astype('uint8')
        return {self.output_name: sad, 
         '%s_threshold' % self.output_name: float(sad_threshold)}


class RASTAfilter(Extractor):
    __doc__ = ' RASTAfilter\n\n  Specialized "Relative Spectral Transform" applying for MFCCs\n  and PLP\n\n  RASTA is a separate technique that applies a band-pass filter\n  to the energy in each frequency subband in order to smooth over\n  short-term noise variations and to remove any constant offset\n  resulting from static spectral coloration in the speech channel\n  e.g. from a telephone line\n\n  Parameters\n  ----------\n  RASTA : bool\n    R.A.S.T.A filter\n  sdc : int (default: 1)\n      Lag size for delta feature computation for\n      "Shifted Delta Coefficients", if `sdc` > 0, the\n      shifted delta features will be append to MFCCs\n\n  References\n  ----------\n  [PLP and RASTA](http://www.ee.columbia.edu/ln/rosa/matlab/rastamat/)\n\n  '

    def __init__(self, rasta=True, sdc=1, input_name='mfcc', output_name=None):
        super(RASTAfilter, self).__init__(input_name=as_tuple(input_name, t=string_types), output_name=output_name)
        self.rasta = bool(rasta)
        self.sdc = int(sdc)

    def _transform(self, feat):
        new_feat = []
        for name in self.input_name:
            mfcc = feat[name]
            if self.rasta:
                mfcc = rastafilt(mfcc)
            if self.sdc >= 1:
                n_ceps = mfcc.shape[(-1)]
                mfcc = np.hstack([
                 mfcc,
                 shifted_deltas(mfcc, N=n_ceps, d=(self.sdc), P=3,
                   k=n_ceps)])
            new_feat.append(mfcc.astype('float32'))

        return new_feat


class AcousticNorm(Extractor):
    __doc__ = '\n  Parameters\n  ----------\n  mean_var_norm : bool (default: True)\n    mean-variance normalization\n  windowed_mean_var_norm : bool (default: False)\n    perform standardization on small windows, very computaiton\n    intensive.\n  sad_name : {str, None} (default: None)\n    feature name of SAD indices, and only using statistics from\n    SAD indexed frames for normalization\n  ignore_sad_error : bool\n    if True, when length of SAD and feature mismatch, still perform\n    normalization, otherwise raise `RuntimeError`.\n\n  '

    def __init__(self, input_name, output_name=None, mean_var_norm=True, windowed_mean_var_norm=False, win_length=301, var_norm=True, sad_name=None, ignore_sad_error=True):
        self.sad_name = str(sad_name) if isinstance(sad_name, string_types) else None
        self.ignore_sad_error = bool(ignore_sad_error)
        super(AcousticNorm, self).__init__(input_name=as_tuple(input_name, t=string_types), output_name=output_name)
        self.mean_var_norm = bool(mean_var_norm)
        self.windowed_mean_var_norm = bool(windowed_mean_var_norm)
        self.var_norm = bool(var_norm)
        win_length = int(win_length)
        if win_length % 2 == 0:
            raise ValueError('win_length must be odd number')
        if win_length < 3:
            raise ValueError('win_length must >= 3')
        self.win_length = win_length

    def _transform(self, feat):
        sad = None
        if self.sad_name is not None:
            sad = feat[self.sad_name]
            if sad.dtype != np.bool:
                sad = sad.astype(np.bool)
        feat_normalized = []
        for name in self.input_name:
            X = feat[name]
            X_sad = sad
            if sad is not None:
                if len(sad) != len(X):
                    raise self.ignore_sad_error or RuntimeError("Features with name: '%s' have length %d, but given SAD has length %d" % (
                     name, len(X), len(sad)))
                else:
                    X_sad = None
            if self.mean_var_norm:
                X = mvn(X, varnorm=(self.var_norm), indices=X_sad)
            if self.windowed_mean_var_norm:
                X = wmvn(X, w=(self.win_length), varnorm=False, indices=X_sad)
            feat_normalized.append(X)

        return feat_normalized


class Read3ColSAD(Extractor):
    __doc__ = " Read3ColSAD simple helper for applying 3 col\n  SAD (name, start-in-second, end-in-second) to extracted acoustic features\n\n  Parameters\n  ----------\n  path_or_map : {str, Mapping}\n      path to folder contain all SAD files\n      if Mapping, it is a map from `ref_key` to SAD dictionary\n  step_length : float\n      step length to convert second to frame index.\n  ref_feat : str\n      name of a reference features that must have the\n      same length with the SAD.\n  input_name : str (default: path)\n      reference key in the pipeline can be use to get the coordinate value\n      of SAD from given dictionary.\n  file_regex: str\n      regular expression for filtering the files name\n\n  Return\n  ------\n   - add 'sad': array of SAD indexing\n\n  "

    def __init__(self, path_or_map, step_length, ref_feat, input_name='path', output_name='sad', file_regex='.*'):
        super(Read3ColSAD, self).__init__(input_name=(str(input_name)))
        self.step_length = float(step_length)
        self.ref_feat = str(ref_feat)
        file_regex = re.compile(str(file_regex))
        if is_string(path_or_map):
            sad = defaultdict(list)
            for f in get_all_files(path_or_map):
                if file_regex.search(os.path.basename(f)) is not None:
                    with open(f, 'r') as (f):
                        for line in f:
                            name, start, end = line.strip().split(' ')
                            sad[name].append((float(start), float(end)))

        else:
            if isinstance(path_or_map, Mapping):
                sad = path_or_map
            else:
                raise ValueError('`path` must be path to folder, or dictionary.')
        self._sad = sad

    def _transform(self, feat):
        name = feat[self.input_name]
        ref_feat = feat[self.ref_feat]
        n_samples = len(ref_feat)
        step_length = self.step_length
        if step_length >= 1:
            step_length = step_length / feat['sr']
        sad_indices = np.zeros(shape=(n_samples,), dtype=(np.uint8))
        if name in self.sad:
            if len(self.sad[name]) > 0:
                for start_sec, end_sec in self.sad[name]:
                    start_idx = int(start_sec / step_length)
                    end_idx = int(end_sec / step_length)
                    if end_idx - start_idx == 0:
                        continue
                    sad_indices[start_idx:end_idx] = 1

        return {self.output_name: sad_indices}


class ApplyingSAD(Extractor):
    __doc__ = " Applying SAD index to given features\n  This extractor cutting voiced segments out, using extracted\n  SAD labels previously\n\n\n  Parameters\n  ----------\n  sad_name: str\n      specific feature will be used name for the cutting\n  threshold: None or float\n      if `sad`, is continuous value, threshold need to be applied\n  smooth_window: int (> 0)\n      amount of adjacent frames will be taken into the SAD\n  keep_unvoiced: bool\n      if True, keep the whole audio file even though no SAD found\n  stack_context : dict\n      a dictionary mapping from feature name to number of\n      context frames (a scalar for both left and right context)\n      NOTE: the final frame length is: `context * 2 + 1`\n  feat_name: str, or list of str\n      all features' name will be applied.\n\n  "

    def __init__(self, input_name, output_name=None, sad_name='sad', threshold=None, smooth_window=None, keep_unvoiced=False):
        super(ApplyingSAD, self).__init__(input_name=as_tuple(input_name, t=string_types), output_name=output_name)
        self.sad_name = str(sad_name)
        self.threshold = float(threshold) if is_number(threshold) else None
        self.smooth_window = int(smooth_window) if is_number(smooth_window) else None
        self.keep_unvoiced = bool(keep_unvoiced)

    def _transform(self, X):
        sad = X[self.sad_name]
        if is_number(self.threshold):
            sad = (sad >= self.threshold).astype('int32')
        if np.isclose(np.sum(sad), 0.0):
            if not self.keep_unvoiced:
                return
            sad[:] = 1
        if is_number(self.smooth_window):
            if self.smooth_window > 0:
                sad = smooth(sad, win=(self.smooth_window), window='flat') > 0.0
        sad = sad.astype('bool')
        X_new = []
        for name in self.input_name:
            X_feat = X[name]
            assert len(sad) == max(X_feat.shape), 'Feature with name: %s, length of sad labels is: %d, but number of sample is: %s' % (
             name, len(sad), max(X_feat.shape))
            X_new.append(X_feat[sad])

        return X_new