# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\export\AudioClipConverter.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 1112 bytes
try:
    from fsb5 import FSB5
except ImportError:
    print("Couldn't import fsb5.\nfsb5 is required to process convert audio clips.")

def extract_audioclip_samples(audio) -> dict:
    """extracts all the sample data from an AudioClip
        Copied from unitypack
        https://github.com/HearthSim/UnityPack/blob/d9ce99fac3c917fa44b0042c9114b7cd03aa9884/unitypack/utils.py#L14

        :param audio: AudioClip
        :type audio: AudioClip
        :return: {filename : sample(bytes)}
        :rtype: dict
        """
    ret = {}
    if not audio.m_AudioData:
        return {}
    else:
        af = FSB5(audio.m_AudioData)
        for i, sample in enumerate(af.samples):
            if i > 0:
                filename = '%s-%i.%s' % (audio.name, i, af.get_sample_extension())
            else:
                filename = '%s.%s' % (audio.name, af.get_sample_extension())
            try:
                sample = af.rebuild_sample(sample)
            except ValueError as e:
                print('WARNING: Could not extract %r (%s)' % (audio, e))
                continue

            ret[filename] = sample

        return ret