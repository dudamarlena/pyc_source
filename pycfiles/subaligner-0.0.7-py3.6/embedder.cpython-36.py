# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/subaligner/embedder.py
# Compiled at: 2020-05-09 20:07:50
# Size of source mod 2**32: 11358 bytes
import librosa, numpy as np
from datetime import datetime, timedelta
from .singleton import Singleton
from .subtitle import Subtitle
from .exception import UnsupportedFormatException, TerminalException
from .logger import Logger

class FeatureEmbedder(Singleton):
    __doc__ = 'Audio and subtitle feature embedding.\n    '
    _FeatureEmbedder__LOGGER = Logger().get_logger(__name__)

    def __init__(self, n_mfcc=13, frequency=16000, hop_len=512, step_sample=0.04, len_sample=0.075):
        """Feature embedder initialiser.

        Keyword Arguments:
            n_mfcc {int} -- The number of MFCC components (default: {13}).
            frequency {float} -- The sample rate  (default: {16000}).
            hop_len {int} -- The number of samples per frame (default: {512}).
            step_sample {float} -- The space (in seconds) between the beginning of each sample (default: 1s / 25 FPS = 0.04s).
            len_sample {float} -- The length in seconds for the input samples (default: {0.075}).
        """
        self._FeatureEmbedder__n_mfcc = n_mfcc
        self._FeatureEmbedder__frequency = frequency
        self._FeatureEmbedder__hop_len = hop_len
        self._FeatureEmbedder__step_sample = step_sample
        self._FeatureEmbedder__len_sample = len_sample
        self._FeatureEmbedder__item_time = 1.0 / frequency * hop_len

        def __setattr__(self, *args):
            raise NotImplementedError('Cannot modify the immutable object')

        def __delattr__(self, *args):
            raise NotImplementedError('Cannot modify the immutable object')

    @property
    def n_mfcc(self):
        """Get the number of MFCC components.

        Returns:
            int -- The number of MFCC components.
        """
        return self._FeatureEmbedder__n_mfcc

    @property
    def frequency(self):
        """Get the sample rate.

        Returns:
            int -- The sample rate.
        """
        return self._FeatureEmbedder__frequency

    @property
    def hop_len(self):
        """Get the number of samples per frame.

        Returns:
            int -- The number of samples per frame.
        """
        return self._FeatureEmbedder__hop_len

    @property
    def step_sample(self):
        """The space (in seconds) between the begining of each sample.

        Returns:
            int -- The space (in seconds) between the begining of each sample.
        """
        return self._FeatureEmbedder__step_sample

    @step_sample.setter
    def step_sample(self, step_sample):
        """Configure the step sample

        Arguments:
            step_sample {float} -- the value of the step sample (1 / frame_rate)
        """
        self._FeatureEmbedder__step_sample = step_sample

    @property
    def len_sample(self):
        """Get the length in seconds for the input samples.

        Returns:
            int -- The length in seconds for the input samples.
        """
        return self._FeatureEmbedder__item_time

    @classmethod
    def time_to_sec(cls, pysrt_time):
        """Convert timestamp to seconds.

        Arguments:
            pysrt_time {pysrt.SubRipTime} -- SubRipTime or coercible.

        Returns:
            float -- The number of seconds.
        """
        if str(pysrt_time) == '00:00:00,000':
            return float(0)
        else:
            total_sec = pysrt_time.milliseconds / float(1000)
            total_sec += int(pysrt_time.seconds)
            total_sec += int(pysrt_time.minutes) * 60
            total_sec += int(pysrt_time.hours) * 60 * 60
            return round(total_sec, 3)

    def get_len_mfcc(self):
        """Get the number of samples to get LEN_SAMPLE: LEN_SAMPLE/(HOP_LEN/FREQUENCY).

        Returns:
            float -- The number of samples.
        """
        return self._FeatureEmbedder__len_sample / (self._FeatureEmbedder__hop_len / self._FeatureEmbedder__frequency)

    def get_step_mfcc(self):
        """Get the number of samples to get STEP_SAMPLE: STEP_SAMPLE/(HOP_LEN/FREQUENCY).

        Returns:
            flaot -- The number of samples.
        """
        return self._FeatureEmbedder__step_sample / (self._FeatureEmbedder__hop_len / self._FeatureEmbedder__frequency)

    def time_to_pos(self, pysrt_time):
        """Return a cell position from timestamp.

        Arguments:
            pysrt_time {pysrt.SubRipTime} -- SubRipTime or coercible.

        Returns:
            int -- The cell position.
        """
        return int(float(self._FeatureEmbedder__frequency * FeatureEmbedder.time_to_sec(pysrt_time)) / self._FeatureEmbedder__hop_len / self.get_step_mfcc())

    def sec_to_pos(self, seconds):
        """Return the cell position from a time in seconds.

        Arguments:
            seconds {float} -- The duration in seconds.

        Returns:
            int -- The cell position.
        """
        return int(float(self._FeatureEmbedder__frequency * seconds) / self._FeatureEmbedder__hop_len / self.get_step_mfcc())

    def pos_to_sec(self, position):
        """Return the time in seconds from a cell position.

        Arguments:
            position {int} -- The cell position.

        Returns:
            int -- The number of seconds.
        """
        return float(position) * self.get_step_mfcc() * self._FeatureEmbedder__hop_len / self._FeatureEmbedder__frequency

    def pos_to_time_str(self, position):
        """Return the time string from a cell position.

        Arguments:
            position {int} -- The cell position.

        Returns:
            string -- The time string (e.g., 01:23:20,150).
        """
        td = timedelta(seconds=(float(position) * self.get_step_mfcc() * self._FeatureEmbedder__hop_len / self._FeatureEmbedder__frequency))
        dt = datetime(1, 1, 1) + td
        hh = str(dt.hour) if len(str(dt.hour)) > 1 else '0{}'.format(str(dt.hour))
        mm = str(dt.minute) if len(str(dt.minute)) > 1 else '0{}'.format(str(dt.minute))
        ss = str(dt.second) if len(str(dt.second)) > 1 else '0{}'.format(str(dt.second))
        ms = int(dt.microsecond / 1000)
        if len(str(ms)) == 3:
            fff = str(ms)
        else:
            if len(str(ms)) == 2:
                fff = '0{}'.format(str(ms))
            else:
                fff = '00{}'.format(str(ms))
        return '{}:{}:{},{}'.format(hh, mm, ss, fff)

    def extract_data_and_label_from_audio(self, audio_file_path, subtitle_file_path, subtitles=None, ignore_sound_effects=False):
        """Generate a train dataset from an audio file and its subtitles

        Arguments:
            audio_file_path {string} -- The path to the audio file.
            subtitle_file_path {string} -- The path to the subtitle file.

        Keyword Arguments:
            subtitles {pysrt.SubRipFile} -- The SubRipFile object (default: {None})
            ignore_sound_effects {boolean} -- Ignore subtitles which are sound effects.

        Returns:
            tuple -- The training data and the training lables.
        """
        len_mfcc = self.get_len_mfcc()
        step_mfcc = self.get_step_mfcc()
        total_time = datetime.now()
        if subtitle_file_path is None:
            if subtitles is not None:
                subs = subtitles
        elif subtitle_file_path is not None:
            try:
                subs = Subtitle.load(subtitle_file_path).subs
                FeatureEmbedder._FeatureEmbedder__LOGGER.info('Subtitle file loaded: {}'.format(subtitle_file_path))
            except UnsupportedFormatException:
                raise

        else:
            raise TerminalException('Subtitles are missing')
        if ignore_sound_effects:
            original_size = len(subs)
            subs = Subtitle.remove_sound_effects_by_affixes(subs,
              se_prefix='(', se_suffix=')')
            subs = Subtitle.remove_sound_effects_by_case(subs,
              se_uppercase=True)
            FeatureEmbedder._FeatureEmbedder__LOGGER.debug('{} sound effects removed'.format(original_size - len(subs)))
        t = datetime.now()
        audio_time_series, sample_rate = librosa.load(audio_file_path,
          sr=(self.frequency))
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('Audio file loaded with sample rate {}: {}'.format(sample_rate, audio_file_path))
        audio_load_time = datetime.now() - t
        t = datetime.now()
        mfcc = librosa.feature.mfcc(y=audio_time_series,
          sr=sample_rate,
          hop_length=(int(self._FeatureEmbedder__hop_len)),
          n_mfcc=(self._FeatureEmbedder__n_mfcc))
        samples = []
        for i in np.arange(0, mfcc.shape[1], step_mfcc):
            samples.append(mfcc[:, int(i):int(i) + int(len_mfcc)])

        samples = samples[:int((mfcc.shape[1] - len_mfcc) / step_mfcc) + 1]
        train_data = np.stack(samples)
        mfcc_extration_time = datetime.now() - t
        t = datetime.now()
        labels = np.zeros(len(train_data))
        for sub in subs:
            for i in np.arange(self.time_to_pos(sub.start), self.time_to_pos(sub.end) + 1):
                if i < len(labels):
                    labels[i] = 1

        label_extraction_time = datetime.now() - t
        total_time = datetime.now() - total_time
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('----- Feature Embedding Metrics --------')
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('| Audio file path: {}'.format(audio_file_path))
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('| Subtitle file path: {}'.format(subtitle_file_path))
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('| Audio load time: {}'.format(str(audio_load_time)))
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('| MFCC extration time: {}'.format(str(mfcc_extration_time)))
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('| Label extraction time: {}'.format(str(label_extraction_time)))
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('| Total time: {}'.format(str(total_time)))
        FeatureEmbedder._FeatureEmbedder__LOGGER.debug('----------------------------------------')
        return (
         train_data, labels)