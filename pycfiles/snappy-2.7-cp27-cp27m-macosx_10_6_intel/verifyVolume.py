# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/verify/verifyVolume.py
# Compiled at: 2018-08-17 21:53:27
from ..sage_helper import sage_method, _within_sage
from ..number import Number
if _within_sage:
    from sage.rings.complex_interval_field import ComplexIntervalField
    from sage.rings.complex_interval_field import is_ComplexIntervalField
    from sage.rings.complex_arb import ComplexBallField
    from sage.rings.real_mpfi import RealIntervalField
__all__ = [
 'volume']
from . import verifyHyperbolicity

def _unprotected_volume_from_shape(z):
    """
    Computes the Bloch-Wigner dilogarithm for z assuming z is of a type that
    properly supports polylog.
    """
    return (1 - z).arg() * z.abs().log() + z.polylog(2).imag()


def volume_from_shape(z):
    """
    Computes the Bloch-Wigner dilogarithm for z which gives the volume of a
    tetrahedron of the given shape.
    """
    if _within_sage:
        CIF = z.parent()
        if is_ComplexIntervalField(CIF):
            CBF = ComplexBallField(CIF.precision())
            RIF = RealIntervalField(CIF.precision())
            return RIF(_unprotected_volume_from_shape(CBF(z)))
        z = Number(z)
    return z.volume()


def volume(manifold, verified=False, bits_prec=None):
    """
    Computes the volume of the given manifold. If verified is used,
    the hyperbolicity is checked rigorously and the volume is given as
    verified interval.

    >>> M = Manifold('m004')
    >>> vol = M.volume(bits_prec=100)   
    >>> vol # doctest: +ELLIPSIS
    2.029883212819307250042405108...
    
    sage: ver_vol = M.volume(verified=True)
    sage: vol in ver_vol
    True
    sage: 2.02988321283 in ver_vol
    False
    """
    shape_intervals = manifold.tetrahedra_shapes('rect', bits_prec=bits_prec, intervals=verified)
    if verified:
        verifyHyperbolicity.check_logarithmic_gluing_equations_and_positively_oriented_tets(manifold, shape_intervals)
    volume = sum([ volume_from_shape(shape_interval) for shape_interval in shape_intervals
                 ])
    if isinstance(volume, Number):
        volume = manifold._number_(volume)
    return volume