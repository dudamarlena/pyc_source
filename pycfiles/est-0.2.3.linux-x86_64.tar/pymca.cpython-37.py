# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/io/utils/pymca.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 2486 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/11/2019'
import PyMca5.PyMcaIO as specfile

def read_spectrum(spec_file):
    """
    
    :param spec_file: path to the spec file containing the spectra definition
    :return: (energy, mu)
    :rtype: tuple
    """
    scan = specfile.Specfile(spec_file)[0]
    data = scan.data()
    if data.shape[0] == 2:
        energy = data[0, :]
        mu = data[1, :]
    else:
        energy = None
        mu = None
        labels = scan.alllabels()
        i = 0
        for label in labels:
            if label.lower() == 'energy':
                energy = data[i, :]
            else:
                if label.lower() in ('counts', 'mu', 'absorption'):
                    mu = data[i, :]
            i = i + 1

        if energy is None or mu is None:
            if len(labels) == 3:
                if labels[0].lower() == 'point':
                    energy = data[1, :]
                    mu = data[2, :]
                else:
                    energy = data[0, :]
                    mu = data[1, :]
            else:
                energy = data[0, :]
                mu = data[1, :]
        return (
         energy, mu)