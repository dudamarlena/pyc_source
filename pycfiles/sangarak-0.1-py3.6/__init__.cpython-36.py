# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sangarak/__init__.py
# Compiled at: 2018-08-17 02:21:54
# Size of source mod 2**32: 2049 bytes
import numpy as np, math

def convert_to_number_list(string):
    return [float(s) for s in string.split(' ')]


def generate_file_dict(f_name, procs):
    d = {}
    for proc in range(0, procs):
        d[proc] = str(proc) + f_name + '.txt'

    return d


def read_matrix(files, major, n, nb, pb, num_procs):
    """
    Read matrices from files specified inside a dict called 'files'. The key of 
    the dict is the process number from the file was outputted and the
    corresponding value is the actual name of the file. Only works for square matrix (for now).

    This implementation is specific to block cyclic matrices stored on multiple MPI processes.
    
    Parameters
    ----------
    files : dict
        Dict specifying the process names with corresponding file names.

    major : string
        Can be either "row" or "col" depending on storage format.

    n : int
        side size of the matrix.

    nb : int
        Block size of matrix.

    pb : int
        Number of processes in one side.

    num_procs : int
        Total number of processes.

    Returns
    -------
    numpy.array
    """
    matrix = np.zeros([n, n])
    width = math.sqrt(num_procs)
    nb_r = nb // pb
    nb_c = nb // pb
    for proc, file_name in files.items():
        f = open(file_name, 'r')
        r = f.read().strip()
        arr = convert_to_number_list(r)
        f.close()
        myrow = int(proc // width)
        mycol = int(proc - myrow * width)
        if major == 'row':
            for pr in range(pb):
                for r in range(nb_r):
                    for pc in range(pb):
                        for c in range(nb_c):
                            glob_row = int(r + myrow * nb_r + pr * nb)
                            glob_col = int(c + mycol * nb_c + pc * nb)
                            index = (r + pr * nb_r) * nb + c + pc * nb_c
                            matrix[(glob_row, glob_col)] = arr[index]

        else:
            if major == 'col':
                raise NotImplementedError('column-major not implemented.')

    return matrix