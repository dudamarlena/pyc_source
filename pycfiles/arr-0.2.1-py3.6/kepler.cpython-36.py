# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/arr/kepler.py
# Compiled at: 2019-09-30 04:56:03
# Size of source mod 2**32: 1691 bytes
import lightkurve as lk
from astroquery.vizier import Vizier
import astropy.units as u, matplotlib.pyplot as pl
from matplotlib.axes import Axes
from arr.simbad import Simbad

class Kepler:

    def __init__(self, target: Simbad, name: str):
        v = Vizier(columns=['KIC', 'kepmag', 'Teff', 'logg', '[Fe/H]', 'E(B-V)', 'Av', 'R*'])
        try:
            kic_entry = v.query_region((target.coord), radius=(1 * u.arcsecond), catalog='V/133/kic')[0]
        except IndexError:
            self.kic_id = None
            self.t_eff = None
            self.kepmag = None
            self.log_g = None
            self.fe_h = None
            self.e_b_v = None
            self.radius = None
            self.lc = None
            return
        else:
            self.kic_id = kic_entry['KIC'][0]
            self.t_eff = float(kic_entry['Teff'][0]) * u.K
            self.kepmag = float(kic_entry['kepmag'][0]) * u.mag
            self.log_g = float(kic_entry['logg'][0])
            self.fe_h = float(kic_entry['__Fe_H_'][0])
            self.e_b_v = float(kic_entry['E_B-V_'][0])
            self.radius = float(kic_entry['R_'][0]) * u.solRad
            res = lk.search_lightcurvefile(name, mission='Kepler')
            lcs = res.download_all()
            self.lc = lcs.stitch()

    def plot(self, show=False, **kwargs):
        for i in ('color', 'ylabel', 'normalize'):
            try:
                del kwargs[i]
            except KeyError:
                pass

        ax = (self.lc.scatter)(color='k', normalize=True, **kwargs)
        if show:
            pl.show()
        else:
            return ax

    @property
    def observed(self):
        return self.kic_id is not None