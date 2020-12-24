# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\test.py
# Compiled at: 2018-03-29 16:31:03
# Size of source mod 2**32: 8712 bytes
"""
Created on Wed Jan 31 20:00:34 2018

@author: dkita
"""
import numpy as np, meep as mp, argparse

def str2bool(v):
    """ Allow proper argparse handling of boolean inputs """
    if v.lower() in ('yes', 'true', 'True', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'False', 'f', 'n', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')


def main(args):
    """ Calculates transmission/reflection spectra of a width-varying PhC distributed Bragg reflector (DBR) with the following inputs
    USER-SPECIFIED INPUTS:
        period = period of the PhC
        DBRlength = length of the PhC DBR region
        dc = duty-cycle of the PhC
        width = width of the waveguide
        height = height of the waveguide
        w_phc = PhC width (PhC region varies between w and w_phc)
        rib = height of the unetched waveguide material (surrounding the core)
    """
    period = args.period
    DBRlength = args.len
    dc = args.dc
    w = args.width
    h = args.height
    w_phc = args.wphc
    rib = args.rib
    res = args.res
    wgLength = args.wgl
    taperLength = args.tl
    wg_n = args.wgn
    clad_n = args.cln
    dpml = args.dpml
    wl_center = args.wlc
    wl_span = args.wls
    norm = args.norm
    pad = args.pad
    nfreq = args.nfreq
    fields = args.fields
    if dc > 1.0 or dc < 0.0:
        print('WARNING! Duty Cycle (dc=' + str(dc) + ') is outside of the acceptable range (0,1). Aborting simulation.')
        return
    elif wgLength < dpml + 0.5:
        print('WARNING! wgLength (' + str(wgLength) + ') is less than the max allowed value ' + str(dpml + 0.5) + '.  Aborting simulation.')
        return
        if pad < dpml + wl_center:
            print('WARNING! pad (' + str(pad) + ') is less than the max allowed value ' + str(dpml + wl_center) + '.  Aborting simulation.')
            return
        elif norm:
            sx = 2 * wgLength
        else:
            if taperLength < 0.001:
                sx = DBRlength + 2 * wgLength
            else:
                sx = DBRlength + 2 * taperLength + 2 * wgLength
        sy = 2 * pad + h
        sz = 2 * pad + max(w, w_phc)
        fmax = 1.0 / (wl_center - 0.5 * wl_span)
        fmin = 1.0 / (wl_center + 0.5 * wl_span)
        fcen = (fmax + fmin) / 2.0
        df = fmax - fmin
        sources = [
         mp.EigenModeSource(src=mp.GaussianSource(fcen, fwidth=df, cutoff=30), component=(mp.ALL_COMPONENTS),
           size=(mp.Vector3(0, 4 * h, 3 * w)),
           center=(mp.Vector3(-sx / 2.0 + 1.5 * dpml, 0, 0)),
           eig_match_freq=True,
           eig_parity=(mp.ODD_Z),
           eig_kpoint=(mp.Vector3(wl_center, 0, 0)),
           eig_resolution=(2 * res if res > 16 else 32))]
        sim = mp.Simulation(cell_size=(mp.Vector3(sx, sy, sz)), boundary_layers=[
         mp.PML(dpml)],
          epsilon_input_file='epsilon-input.h5',
          sources=sources,
          dimensions=3,
          default_material=mp.Medium(index=clad_n),
          resolution=res)
        trans_flux_region = mp.FluxRegion(size=(mp.Vector3(0, 1.5 * h, 1.5 * w)), center=(mp.Vector3(sx / 2.0 - dpml, 0, 0)))
        refl_flux_region = mp.FluxRegion(size=(mp.Vector3(0, 1.5 * h, 1.5 * w)), center=(mp.Vector3(-sx / 2.0 + dpml, 0, 0)))
        transmission = sim.add_flux(fcen, df, nfreq, trans_flux_region)
        reflection = sim.add_flux(fcen, df, nfreq, refl_flux_region)
        sim.use_output_directory()
        decay_pt = mp.Vector3(sx / 2.0 - 1.1 * dpml, 0, 0)
        sv = mp.Volume(size=(mp.Vector3(sx, sy, 0)), center=(mp.Vector3(0, 0, 0)))
        tv = mp.Volume(size=(mp.Vector3(sx, 0, sz)), center=(mp.Vector3(0, 0, 0)))
        if fields:
            sim.run((mp.at_beginning(mp.output_epsilon)), (mp.at_beginning(mp.with_prefix('sideview-', mp.in_volume(sv, mp.output_epsilon)))),
              (mp.at_beginning(mp.with_prefix('topview-', mp.in_volume(tv, mp.output_epsilon)))),
              (mp.at_every(1.0, mp.to_appended('ez-sideview', mp.in_volume(sv, mp.output_efield_z)))),
              (mp.at_every(1.0, mp.to_appended('ez-topview', mp.in_volume(tv, mp.output_efield_z)))),
              until_after_sources=(mp.stop_when_fields_decayed(20, mp.Ez, decay_pt, 0.0001)))
    else:
        sim.run(until_after_sources=(mp.stop_when_fields_decayed(20, mp.Ez, decay_pt, 0.0001)))
    if norm:
        sim.save_flux('refl-flux', reflection)
    sim.display_fluxes(transmission, reflection)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-period', type=float, default=0.5, help='Period of the PhC (default=0.5)')
    parser.add_argument('-len', type=float, default=10.0, help='Length of the PhC DBR region (default=5)')
    parser.add_argument('-dc', type=float, default=0.5, help='Duty cycle of the PhC DBR region (default=0.5)')
    parser.add_argument('-width', type=float, default=0.85, help='Width of the waveguide (default=0.85)')
    parser.add_argument('-height', type=float, default=0.22, help='Height of the waveguide (default=0.22)')
    parser.add_argument('-wphc', type=float, default=0.6, help='Width of the PhC modulated region, PhC region varies between w and w_phc (default=0.6)')
    parser.add_argument('-rib', type=float, default=0.07, help='rib = height of the unetched waveguide material surrounding the core (default=0.07)')
    parser.add_argument('-fields', type=str2bool, nargs='?', const=True, default=False, help='If True, saves the field information (vs time) for top-down and side-view')
    parser.add_argument('-res', type=float, default=10, help='Resolution of the simulation [pixels/um] (default=10)')
    parser.add_argument('-wgl', type=float, default=2.5, help='Length of the waveguide before the taper begins (default=2.5)')
    parser.add_argument('-tl', type=float, default=5.0, help='Length of the taper region (default=5.0)')
    parser.add_argument('-wgn', type=float, default=1.996, help='Index of the waveguide material (default=1.996)')
    parser.add_argument('-cln', type=float, default=1.4532, help='Index of the cladding material (default=1.4532)')
    parser.add_argument('-dpml', type=float, default=1.0, help='Thickness of the PML region (default=1.0)')
    parser.add_argument('-wlc', type=float, default=0.925, help='Center wavelength [in um] of the Gaussian pulse (default=0.925)')
    parser.add_argument('-wls', type=float, default=0.3, help='Width of the Gaussian pulse [in um] (default=0.300)')
    parser.add_argument('-norm', type=str2bool, nargs='?', const=True, default=False, help='If True, indicates a normalization run without any MMI structure (defulat=False)')
    parser.add_argument('-pad', type=float, default=2.5, help='Spacing (in y- & z-directions) between structure & simulation boundary (default=2.5)')
    parser.add_argument('-nfreq', type=float, default=800, help='Number of frequencies sampled (for flux) between fcen-df/2 and fcen+df/2 (default=100)')
    args = parser.parse_args()
    main(args)