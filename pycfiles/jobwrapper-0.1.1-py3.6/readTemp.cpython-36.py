# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/readTemp.py
# Compiled at: 2018-09-07 05:20:19
# Size of source mod 2**32: 1921 bytes
import numpy as np, os, h5py as hp, glob, sys
from LPPic import LPPic

def main(path):
    """This function is the main function of the script.

    It will use the LPPic class from LPPview, a litle bit differently, but quite similare.
    """
    lp = LPPic(path=path)
    lp._data_path = lp._path
    if os.path.isfile(lp._data_path + 'temporal_values.dat'):
        lp.getallfiles('tempor')
    else:
        lp.getallfiles('history')
    data = np.loadtxt(lp.lastfile())
    data[0, :] = 0.0
    time = data[:, 0]
    elec = data[:, 1]
    ions = data[:, 2]
    SUMe_x = data[:, 3]
    SUMe_y = data[:, 4]
    SUMe_z = data[:, 5]
    coll = data[:, 6]
    ioni = data[:, 7]
    mobi = data[:, 8]
    elec_SEE = data[:, 9]
    elec_SEE_sup = data[:, 10]
    elec_wal = data[:, 11]
    elec_cou = data[:, 12]
    elec_Oz = data[:, 13]
    lp.getallfiles(filetype='tabgrid')
    lastFile = lp.lastfile()
    fichier = hp.File(lastFile, 'r')
    ne = np.array(fichier.get('Nume'))
    with open('temporal_file_py.txt', 'w') as (f):
        f.write('t = {}\n'.format(time[(-1)]))
        f.write('Ne = {}\n'.format(elec[(-1)]))
        f.write('Ni = {}\n'.format(ions[(-1)]))
        print(np.shape(ne))
        ne_mean = ne.mean(axis=1)
        print(np.shape(ne_mean))
        ne_max = np.max(ne_mean)
        f.write('n_e,max = {}\n'.format(ne_max))


if __name__ == '__main__':
    path = sys.argv[1]
    main(path)