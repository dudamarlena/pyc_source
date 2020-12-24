# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/ModelResults.py
# Compiled at: 2019-02-19 08:46:58
# Size of source mod 2**32: 3145 bytes
import numpy as np
import astropy.units as u
from atomicdataMB import gValue
import mathMB

class ModelResult:

    def __init__(self, inputs):
        self.inputs = inputs
        self.filenames, self.packets, self.totalsource = inputs.findpackets()
        self.mod_rate = self.totalsource / inputs.options.endtime
        self.atoms_per_packet = 1e+26 / u.s / self.mod_rate
        print(f"Total number of packets run = {self.packets}")
        print(f"Total source = {self.totalsource} packets")
        print(f"1 packet represents {self.atoms_per_packet} atoms")
        print(f"Model rate = {self.mod_rate} packets/sec")


def read_format(formatfile):
    format_ = {}
    with open(formatfile, 'r') as (f):
        for line in f:
            try:
                p, v = line.split('=')
                format_[p.strip().lower()] = v.strip()
            except:
                pass

    return format_


def results_loadfile(filename):
    """ Load the output and do some error checking

    It may be necessary at some point to add more functionality to this"""
    from .Output import Output
    output = Output.restore(filename)
    try:
        output.x.unit
    except:
        assert 0, 'Output does not contain units like it should.'

    assert np.all(output.frac >= 0), 'Has f < 0'
    assert np.all(np.isfinite(output.frac)), 'Has non-finite f'
    return output


def results_packet_weighting(result, radvel_sun, frac, out_of_shadow, aplanet):
    if result.quantity == 'column':
        weight = frac
    else:
        if result.quantity == 'density':
            weight = frac
        else:
            if result.quantity == 'radiance':
                if 'resscat' in result.mechanism:
                    gg = np.zeros_like(frac) / u.s
                    for w in result.wavelength:
                        gval = gValue(result.inputs.options.atom, w, aplanet)
                        gg += mathMB.interpu(radvel_sun, gval.velocity, gval.g)

                    weight_resscat = frac * out_of_shadow * gg / 1000000.0
                weight = weight_resscat
    assert np.all(np.isfinite(weight)), 'Non-finite weights'
    return weight