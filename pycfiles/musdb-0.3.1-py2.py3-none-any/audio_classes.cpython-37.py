# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faro/repositories/sigsep-mus-tools/build/lib/musdb/audio_classes.py
# Compiled at: 2018-02-21 05:20:47
# Size of source mod 2**32: 7602 bytes
from __future__ import print_function
from __future__ import division
import os, soundfile as sf, numpy as np, stempeg

class Source(object):
    __doc__ = '\n    An audio Target which is a linear mixture of several sources\n\n    Attributes\n    ----------\n    name : str\n        Name of this source\n    stem_id : int\n        stem/substream ID is set here.\n    is_wav : boolean\n        If stem is read from wav or mp4 stem\n    path : str\n        Absolute path to audio file\n    gain : float\n        Mixing weight for this source\n    '

    def __init__(self, name=None, path=None, stem_id=None, is_wav=False):
        self.name = name
        self.path = path
        self.stem_id = stem_id
        self.is_wav = is_wav
        self.gain = 1.0
        self._audio = None
        self._rate = None

    @property
    def audio(self):
        """array_like: [shape=(num_samples, num_channels)]
        """
        if self._audio is not None:
            return self._audio
            if os.path.exists(self.path):
                audio, rate = self.is_wav or stempeg.read_stems(filename=(self.path),
                  stem_id=(self.stem_id))
            else:
                audio, rate = sf.read((self.path), always_2d=True)
        else:
            self._rate = rate
            return audio
        self._rate = None
        self._audio = None
        raise ValueError('Oops! %s cannot be loaded' % self.path)

    @property
    def rate(self):
        """int: sample rate in Hz
        """
        if self._rate is None:
            if os.path.exists(self.path):
                if not self.is_wav:
                    audio, rate = stempeg.read_stems(filename=(self.path),
                      stem_id=(self.stem_id))
                else:
                    audio, rate = sf.read((self.path), always_2d=True)
                self._rate = rate
                return rate
            self._rate = None
            self._audio = None
            raise ValueError('Oops! %s cannot be loaded' % self.path)
        return self._rate

    @audio.setter
    def audio(self, array):
        self._audio = array

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    def __repr__(self):
        return self.path


class Target(object):
    __doc__ = '\n    An audio Target which is a linear mixture of several sources\n\n    Attributes\n    ----------\n    sources : list[Source]\n        list of ``Source`` objects for this ``Target``\n    '

    def __init__(self, sources):
        self.sources = sources

    @property
    def audio(self):
        """array_like: [shape=(num_samples, num_channels)]

        mixes audio for targets on the fly
        """
        mix_list = [] * len(self.sources)
        for source in self.sources:
            audio = source.audio
            if audio is not None:
                mix_list.append(source.gain * audio)

        return np.sum((np.array(mix_list)), axis=0)

    def __repr__(self):
        parts = []
        for source in self.sources:
            parts.append(source.name)

        return '+'.join(parts)


class Track(object):
    __doc__ = "\n    An audio Track which is mixture of several sources\n    and provides several targets\n\n    Attributes\n    ----------\n    name : str\n        Track name\n    path : str\n        Absolute path of mixture audio file\n    stem_id : int\n        stem/substream ID\n    is_wav : boolean\n        If stem is read from wav or mp4 stem\n    subset : {'train', 'test'}\n        belongs to subset\n    targets : OrderedDict\n        OrderedDict of mixted Targets for this Track\n    sources : Dict\n        Dict of ``Source`` objects for this ``Track``\n    "

    def __init__(self, name, stem_id=None, is_wav=False, track_artist=None, track_title=None, subset=None, path=None):
        self.name = name.split('.stem.mp4')[0]
        try:
            split_name = name.split(' - ')
            self.artist = split_name[0]
            self.title = split_name[1]
        except IndexError:
            self.artist = track_artist
            self.title = track_title

        self.path = path
        self.subset = subset
        self.stem_id = stem_id
        self.is_wav = is_wav
        self.targets = None
        self.sources = None
        self._audio = None
        self._stems = None
        self._rate = None

    @property
    def stems(self):
        """array_like: [shape=(stems, num_samples, num_channels)]
        """
        if self._stems is not None:
            return self._stems
            if not self.is_wav:
                if os.path.exists(self.path):
                    S, rate = stempeg.read_stems(filename=(self.path))
        else:
            rate = self.rate
            S = []
            S.append(self.audio)
            for k, v in sorted((self.sources.items()),
              key=(lambda x: x[1].stem_id)):
                S.append(v.audio)

            S = np.array(S)
        self._rate = rate
        return S

    @property
    def duration(self):
        """return track duration in seconds"""
        return self.audio.shape[0] / self.rate

    @property
    def audio(self):
        """array_like: [shape=(num_samples, num_channels)]
        """
        if self._audio is not None:
            return self._audio
        if os.path.exists(self.path):
            if self.stem_id is not None:
                audio, rate = stempeg.read_stems(filename=(self.path),
                  stem_id=(self.stem_id))
            else:
                audio, rate = sf.read((self.path), always_2d=True)
            self._rate = rate
            return audio
        self._rate = None
        self._audio = None
        raise ValueError('Oops! %s cannot be loaded' % self.path)

    @property
    def rate(self):
        """int: sample rate in Hz
        """
        if self._rate is None:
            if os.path.exists(self.path):
                if self.stem_id is not None:
                    audio, rate = stempeg.read_stems(filename=(self.path),
                      stem_id=(self.stem_id))
                else:
                    audio, rate = sf.read((self.path), always_2d=True)
                self._rate = rate
                return rate
            self._rate = None
            self._audio = None
            raise ValueError('Oops! %s cannot be loaded' % self.path)
        return self._rate

    @audio.setter
    def audio(self, array):
        self._audio = array

    @rate.setter
    def rate(self, rate):
        self._rate = rate

    def __repr__(self):
        return '\n%s' % self.name