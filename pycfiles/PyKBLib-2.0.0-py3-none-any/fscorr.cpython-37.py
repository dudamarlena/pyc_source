# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pykbi/fscorr.py
# Compiled at: 2019-01-09 17:08:46
# Size of source mod 2**32: 3504 bytes
__doc__ = '\nPerform finite size correction on the radial distribution fuction.\n\nWe have two methods:\n    - InverseN- correction, as described by Kruger\n    - van der Vegt correction, as described by ...\n\nThe InverseN correction method takes two RDF objects as input, and returns a new RDF object.\n\nThe van der Vegt correction takes onw RDF object, and returns a new RDF object.\n'
import numpy as np, scipy
import pykbi.rdf as _rdf
__all__ = [
 'CorrectInverseN', 'CorrectVanDerVegt']

def CorrectInverseN(rdf1, rdf2):
    """
    Correct the rdf based on scaling between systems.
    """
    if abs(rdf1.r[1] - rdf2.r[1]) > 0.0001:
        print("CorrectInverseN correction requires rdf's with same resolution")
        return False
        if rdf1.npart is None or rdf2.npart is None:
            print('RDFs must have a defined number of particles')
            return False
        if rdf1.npart == rdf2.npart:
            print('Equal number of particles in each of the RDFs. ')
            print('Cannot do Inverse-N finite size correction when same number of atoms')
            return False
        if len(rdf1.r) > len(rdf2.r):
            rdfref = rdf2
            rdfext = rdf1
    else:
        rdfref = rdf1
        rdfext = rdf2
    bins = len(rdfref.r)
    correction_mask = (rdfref.gr - rdfext.gr[:bins]) / (rdfext.npart / rdfref.npart - 1.0)
    out_rdf = _rdf.RDF((rdfref.r.copy()), (rdfref.gr - correction_mask),
      npart=(rdfref.npart),
      box_size=(rdfref.lt),
      eqint=(rdfref.eqint),
      name=(rdfref.name + ' invN-corrected'))
    return out_rdf


def CorrectVanDerVegt(rdf):
    """
    Using the van der Vegt correction method to correct the Finite size effect of
    a rdf.

    We only do this up to half the box size.

    """
    if rdf.npart is None:
        print('Cannot do VDV correction on this system. No particles defined')
        return False
    if rdf.lt is None or rdf.volume is None:
        print('Cannot do VDV correction on this system. ')
        print('RDF without box side lengths or volume')
        return False
    if rdf.eqint is None:
        print('Cannot do VDV correction on this system. ')
        print('RDF must have eqint value set.')
        return False
    rho_ref = rdf.npart / rdf.volume
    krondelta = int(rdf.eqint)
    c1 = rdf.npart * (1.0 - 4.0 * np.pi * rdf.r ** 3 / 3.0 / rdf.volume)
    c2 = rho_ref * 4.0 * np.pi * scipy.integrate.cumtrapz((rdf.gr[:] - 1.0) * rdf.r[:] ** 2, rdf.r[:])
    c2 = np.concatenate((np.array([0.0]), c2))
    c3 = c1 / (c1 - c2 - krondelta)
    out_rdf = _rdf.RDF((rdf.r.copy()), (rdf.gr * c3),
      npart=(rdf.npart),
      box_size=(rdf.lt),
      eqint=(rdf.eqint),
      name=(rdf.name))
    return out_rdf