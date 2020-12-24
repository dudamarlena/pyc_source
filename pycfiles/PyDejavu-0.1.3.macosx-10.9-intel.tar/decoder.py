# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/.virtualenvs/datasight-backend/lib/python2.7/site-packages/dejavu/decoder.py
# Compiled at: 2015-04-19 17:14:05
import os, fnmatch, numpy as np
from pydub import AudioSegment
from pydub.utils import audioop
import wavio
from hashlib import sha1

def unique_hash(filepath, blocksize=1048576):
    """ Small function to generate a hash to uniquely generate
    a file. Inspired by MD5 version here:
    http://stackoverflow.com/a/1131255/712997

    Works with large files. 
    """
    s = sha1()
    with open(filepath, 'rb') as (f):
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            s.update(buf)

    return s.hexdigest().upper()


def find_files(path, extensions):
    extensions = [ e.replace('.', '') for e in extensions ]
    for dirpath, dirnames, files in os.walk(path):
        for extension in extensions:
            for f in fnmatch.filter(files, '*.%s' % extension):
                p = os.path.join(dirpath, f)
                yield (p, extension)


def read(filename, limit=None):
    """
    Reads any file supported by pydub (ffmpeg) and returns the data contained
    within. If file reading fails due to input being a 24-bit wav file,
    wavio is used as a backup.

    Can be optionally limited to a certain amount of seconds from the start
    of the file by specifying the `limit` parameter. This is the amount of
    seconds from the start of the file.

    returns: (channels, samplerate)
    """
    try:
        audiofile = AudioSegment.from_file(filename)
        if limit:
            audiofile = audiofile[:limit * 1000]
        data = np.fromstring(audiofile._data, np.int16)
        channels = []
        for chn in xrange(audiofile.channels):
            channels.append(data[chn::audiofile.channels])

        fs = audiofile.frame_rate
    except audioop.error:
        fs, _, audiofile = wavio.readwav(filename)
        if limit:
            audiofile = audiofile[:limit * 1000]
        audiofile = audiofile.T
        audiofile = audiofile.astype(np.int16)
        channels = []
        for chn in audiofile:
            channels.append(chn)

    return (
     channels, audiofile.frame_rate, unique_hash(filename))


def path_to_songname(path):
    """
    Extracts song name from a filepath. Used to identify which songs
    have already been fingerprinted on disk.
    """
    return os.path.splitext(os.path.basename(path))[0]