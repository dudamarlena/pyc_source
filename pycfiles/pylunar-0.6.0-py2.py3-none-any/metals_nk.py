# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/robochat/Projects/pyLuminous/pyluminous-code/pyFresnel/transfer_matrix_examples/metals_nk.py
# Compiled at: 2014-09-23 17:41:03
__doc__ = "Material refractive indices for some metals. The data is from Freesnell and \nthe initial motivation is that these are the materials need for the filters in\nIsotropic_metallic_filters.py which are reproductions of Freesnell's metallic.scm\nfor testing purposes"
import numpy as N
from scipy.interpolate import interp1d, splrep, splev
import pyFresnelInit, pyFresnel.constants as C

def loadMAT(fname):
    with file(fname) as (fobj):
        output = []
        for line in fobj:
            linelist = line.split('*')
            if linelist[0] == 'DATA1':
                output.append(map(float, linelist[2:5]))

        return N.array(output)


al = N.loadtxt('al.nk', skiprows=2)
w_axis = al[:, 0] * C.e / C.hbar
Alspline_real = splrep(w_axis, al[:, 1], s=0)
Alspline_imag = splrep(w_axis, al[:, 2], s=0)
Al = lambda w: splev(w, Alspline_real, der=0) + complex(0.0, 1.0) * splev(w, Alspline_imag, der=0)
au2 = loadMAT('AU.MAT')
w_axis = C.c * 2 * C.pi * 1000000000.0 / au2[:, 0]
Au2spline_real = splrep(w_axis[::-1], au2[::-1, 1], s=0)
Au2spline_imag = splrep(w_axis[::-1], au2[::-1, 2], s=0)
Au = lambda w: splev(w, Au2spline_real, der=0) + complex(0.0, 1.0) * splev(w, Au2spline_imag, der=0)