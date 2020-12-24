# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/implicit/datasets/million_song_dataset.py
# Compiled at: 2019-10-24 03:58:04
# Size of source mod 2**32: 4602 bytes
import h5py, time
from tqdm.auto import tqdm
import os, logging
from scipy.sparse import coo_matrix, csr_matrix
import numpy as np
from implicit.datasets import _download
log = logging.getLogger('implicit')
URL = 'https://github.com/benfred/recommender_data/releases/download/v1.0/msd_taste_profile.hdf5'

def get_msd_taste_profile():
    """ Returns the taste profile subset from the million song dataset:
    https://labrosa.ee.columbia.edu/millionsong/tasteprofile

    Data returned is a tuple of (trackinfo, user, plays) where
    plays is a CSR matrix of with the rows being the track, columns being
    the user and the values being the number of plays.

    Trackinfo is a an array of tuples (trackid, artist, album, song name),
    with the position corresponding to the rowid of the plays matrix. Likewise
    users is an array of the user identifiers.
    """
    filename = os.path.join(_download.LOCAL_CACHE_DIR, 'msd_taste_profile.hdf5')
    if not os.path.isfile(filename):
        log.info("Downloading dataset to '%s'", filename)
        _download.download_file(URL, filename)
    else:
        log.info("Using cached dataset at '%s'", filename)
    with h5py.File(filename, 'r') as (f):
        m = f.get('track_user_plays')
        plays = csr_matrix((m.get('data'), m.get('indices'), m.get('indptr')))
        return (np.array(f['track']), np.array(f['user']), plays)


def generate_dataset(triplets_filename, summary_filename='msd_summary_file.h5', outputfilename='msd_taste_profile.hdf5'):
    """ Generates a hdf5 datasetfile from the raw datafiles:

    You will need to download the train_triplets from here:
        https://labrosa.ee.columbia.edu/millionsong/tasteprofile#getting
    And the 'Summary File of the whole dataset' from here
    https://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset

    You shouldn't have to run this yourself, and can instead just download the
    output using the 'get_msd_taste_profile' funciton
    """
    data = _read_triplets_dataframe(triplets_filename)
    track_info = _join_summary_file(data, summary_filename)
    _hfd5_from_dataframe(data, track_info, outputfilename)


def _read_triplets_dataframe(filename):
    """ Reads the original dataset TSV as a pandas dataframe """
    import pandas
    start = time.time()
    log.debug('reading data from %s', filename)
    data = pandas.read_table('train_triplets.txt', names=['user', 'track', 'plays'])
    data['user'] = data['user'].astype('category')
    data['track'] = data['track'].astype('category')
    log.debug('read data file in %s', time.time() - start)
    return data


def _join_summary_file(data, summary_filename='msd_summary_file.h5'):
    """ Gets the trackinfo array by joining taste profile to the track summary file """
    msd = h5py.File(summary_filename)
    track_lookup = dict(((t.encode('utf8'), i) for i, t in enumerate(data['track'].cat.categories)))
    track_info = np.empty(shape=(len(track_lookup), 4), dtype=(np.object))
    with tqdm(total=(len(track_info))) as (progress):
        for song in msd['metadata']['songs']:
            trackid = song[17]
            if trackid in track_lookup:
                pos = track_lookup[trackid]
                track_info[pos] = [x.decode('utf8') for x in (trackid, song[9], song[14], song[18])]
                progress.update(1)

    return track_info


def _hfd5_from_dataframe(data, track_info, outputfilename):
    plays = coo_matrix((data['plays'].astype(np.float32),
     (
      data['track'].cat.codes.copy(),
      data['user'].cat.codes.copy()))).tocsr()
    with h5py.File(outputfilename, 'w') as (f):
        g = f.create_group('track_user_plays')
        g.create_dataset('data', data=(plays.data))
        g.create_dataset('indptr', data=(plays.indptr))
        g.create_dataset('indices', data=(plays.indices))
        dt = h5py.special_dtype(vlen=str)
        dset = f.create_dataset('track', (track_info.shape), dtype=dt)
        dset[:] = track_info
        user = list(data['user'].cat.categories)
        dset = f.create_dataset('user', (len(user),), dtype=dt)
        dset[:] = user