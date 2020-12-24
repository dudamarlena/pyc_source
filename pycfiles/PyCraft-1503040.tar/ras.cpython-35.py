# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/antenna/ras.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 4029 bytes
from __future__ import absolute_import, unicode_literals, division, print_function
from astropy import units as apu
import numpy as np
from .cyantenna import ras_pattern_cython
from .. import conversions as cnv
from .. import utils
__all__ = [
 'ras_pattern']

@utils.ranged_quantity_input(phi=(
 -180, 180, apu.deg), diameter=(
 0.1, 1000.0, apu.m), wavelength=(
 0.001, 2, apu.m), eta_a=(
 0, None, cnv.dimless), strip_input_units=True, output_unit=cnv.dBi)
def ras_pattern(phi, diameter, wavelength, eta_a=100.0 * apu.percent, do_bessel=False):
    """
    Antenna gain as a function of angular distance after `ITU-R Rec RA.1631
    <https://www.itu.int/rec/R-REC-RA.1631-0-200305-I/en>`_.

    Parameters
    ----------
    phi : `~astropy.units.Quantity`
        Angular distance from looking direction [deg]
    diameter : `~astropy.units.Quantity`
        Antenna diameter [m]
    wavelength : `~astropy.units.Quantity`
        Observing wavelength [m]
    eta_a : `~astropy.units.Quantity`
        Antenna efficiency (default: 100%)
    do_bessel : bool, optional
        If set to True, use Bessel function approximation for inner 1 deg
        of the pattern (see RA.1631 for details). (default: False)

    Returns
    -------
    gain : `~astropy.units.Quantity`
        Antenna gain [dBi]

    Notes
    -----
    - See `ITU-R Rec. RA.1631-0
      <https://www.itu.int/rec/R-REC-RA.1631-0-200305-I/en>`_ for further
      explanations and applicability of this model.
    """
    phi = np.abs(phi)
    d_wlen = diameter / wavelength
    gmax = 10 * np.log10(eta_a * (np.pi * d_wlen) ** 2)
    g1 = -1.0 + 15.0 * np.log10(d_wlen)
    phi_m = 20.0 / d_wlen * np.sqrt(gmax - g1)
    phi_r = 15.85 * d_wlen ** (-0.6)
    gain = ras_pattern_cython(phi, d_wlen, gmax, g1, phi_m, phi_r)
    if do_bessel:
        from scipy.special import j1
        phi, d_wlen, gmax = np.broadcast_arrays(phi, d_wlen, gmax)
        phi_0 = 69.88 / d_wlen
        x_pi = np.radians(np.pi / 2.0 * d_wlen * phi)
        mask = (1e-32 < phi) & (phi < phi_0)
        tmp_x = x_pi[mask]
        gain[mask] = gmax[mask] + 20 * np.log10(j1(2 * tmp_x) / tmp_x)
        mask = (phi_0 <= phi) & (phi < 1.0)
        B_sqrt = 39.810717055349734 * np.radians(np.pi * d_wlen[mask] / 2.0)
        tmp_x = x_pi[mask]
        gain[mask] = 20 * np.log10(B_sqrt * np.cos(2 * tmp_x - 0.75 * np.pi + 0.0953) / tmp_x)
    return gain


if __name__ == '__main__':
    print('This not a standalone python program! Use as module.')