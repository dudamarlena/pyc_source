# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pyphoon/io/tsv.py
# Compiled at: 2018-02-05 04:25:06
# Size of source mod 2**32: 2795 bytes
from os import listdir
from os.path import isfile, join
from datetime import datetime as dt

def read_tsvs(directory='original_data/jma/'):
    """ Reads all the files from the jma directory and returns a list of *N*
    elements, each being a list of typhoon features.

    :param directory: Path of the JMA metadata
    :type directory: str
    :return: List with the metadata of the *N* images
    """
    files = listdir(directory)
    metadata = []
    for f in files:
        f = join(directory, f)
        metadata.extend(read_tsv(f))

    return metadata


def read_tsv(path_to_file):
    """ Reads a TSV file from the best track dataset.

    :param path_to_file: Complete path to the TSV file
    :type path_to_file: str
    :return: *NxD* Numpy array (*N*: #samples, *D*: #features)
    """
    metadata = []
    if isfile(path_to_file):
        ff = open(path_to_file, 'r').readlines()
        for fff in ff:
            _metadata = fff.split('\t')
            _metadata[-1] = _metadata[(-1)].split('\n')[0]
            __metadata = list(map(float, _metadata))
            metadata.append(__metadata)

    return metadata


def check_constant_distance_in_tsv(path_best='original_data/jma', time_distance=3600):
    """ Checks that all provided JMA data is correct, i.e. that all samples
    within a typhoon sequence have a constant tome distance between themselves.

    :param path_best: Directory containing TSV files.
    :type path_best: str
    :param time_distance: Distance between frames in seconds.
    :type time_distance: int
    :return: List with the number of samples with distance different than 1h
        with the previous one. Element n:th in the list refers to the n:th
        typhoon sequence.
    """
    assert isinstance(time_distance, int), 'time_distance is not aninteger: %r' % time_distance
    files = listdir(path_best)
    error = []
    for file in files:
        data = np.array(read_tsv(join(path_best, file)))
        _error = 0
        for i in range(len(data) - 1):
            d0 = dt(int(data[i][0]), int(data[i][1]), int(data[i][2]), int(data[i][3]))
            d1 = dt(int(data[(i + 1)][0]), int(data[(i + 1)][1]), int(data[(i + 1)][2]), int(data[(i + 1)][3]))
            delta = (d1 - d0).total_seconds()
            if delta != time_distance:
                _error += 1
                print('Error at', i, 'of', delta, 'seconds')

        error.append(_error)

    return error