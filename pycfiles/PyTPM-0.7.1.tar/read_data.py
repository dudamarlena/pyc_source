# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phn/projects/pytpm/doc/examples/read_data.py
# Compiled at: 2011-08-22 05:44:57
import csv, math

def get_hipdata():
    """Return data in hip_full.txt.

    The data was created with hip_full.py file. Assumes that the file
    hip_full.txt is in the current directory.
    """
    f = open('hip_full.txt', 'r')
    s = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=' ', skipinitialspace=True)
    d = dict(ra_icrs=[], dec_icrs=[], px=[], pma=[], pmd=[], raj2=[], decj2=[], rab1=[], decb1=[], glon=[], glat=[], elon2=[], elat2=[])
    for i in s:
        d['ra_icrs'].append(math.radians(i[0]))
        d['dec_icrs'].append(math.radians(i[1]))
        d['raj2'].append(math.radians(i[5]))
        d['decj2'].append(math.radians(i[6]))
        d['rab1'].append(math.radians(i[7]))
        d['decb1'].append(math.radians(i[8]))
        d['glon'].append(math.radians(i[9]))
        d['glat'].append(math.radians(i[10]))
        d['elon2'].append(math.radians(i[11]))
        d['elat2'].append(math.radians(i[12]))
        d['pma'].append(i[3] / math.cos(d['decj2'][(-1)]) / 1000.0 * 100.0)
        d['pmd'].append(i[4] / 1000.0 * 100.0)
        d['px'].append(i[2] / 1000.0)

    f.close()
    return d