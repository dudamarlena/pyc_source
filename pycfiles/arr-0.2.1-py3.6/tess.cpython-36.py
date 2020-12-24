# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/arr/tess.py
# Compiled at: 2019-09-30 09:40:12
# Size of source mod 2**32: 3278 bytes
import lightkurve as lk
from tess_stars2px import tess_stars2px_function_entry as tess_stars2px
from astropy.coordinates import SkyCoord
from astroquery.mast import Catalogs
import eleanor
from eleanor.utils import SearchError
import astropy.units as u
from matplotlib.axes import Axes
import matplotlib.pyplot as pl
from arr.simbad import Simbad

class TessPointing:

    def __init__(self, result):
        self.sectors = result[3]
        self.cameras = result[4]
        self.ccds = result[5]
        if self.observed:
            self.pixel_pos = [(x, y) for x, y in zip(result[6], result[7])]
        else:
            self.pixel_pos = None

    @property
    def observed(self):
        return len(self.sectors) > 0 and self.sectors[0] != -1


class Tess:

    def __init__(self, target: Simbad, name: str):
        if not Tess.pointing(target.coord).observed:
            self.lc = None
        else:
            tic_entry = Catalogs.query_region(f"{target.coord.ra.degree} {target.coord.dec.degree}", radius=0.0001,
              catalog='TIC')
            tic_entry = tic_entry[0]
            self.extract_tic(tic_entry, self.pointing(target.coord))
            res = lk.search_lightcurvefile((target.coord), mission='TESS')
            if len(res) != 0:
                self.download_lc(res)
            else:
                self.extract_from_ffi()

    def download_lc(self, res: lk.SearchResult):
        lcs = res.download_all()
        self.lc = lcs.PDCSAP_FLUX.stitch()

    def extract_from_ffi(self):
        try:
            stars = eleanor.multi_sectors(tic=(self.tic_id), sectors='all')
        except SearchError:
            self.lc = None
            return
        except:
            stars = eleanor.multi_sectors(tic=(self.tic_id), sectors='all', tc=True)

        lcs = lk.LightCurveCollection([])
        self.data_list = []
        self.q_list = []
        for star in stars:
            data = eleanor.TargetData(star, height=15, width=15, bkg_size=31, do_psf=False, do_pca=False)
            q = data.quality == 0
            lcs.append(lk.TessLightCurve(time=(data.time[q]), flux=(data.corr_flux[q]), targetid=(self.tic_id)))
            self.data_list.append(data)
            self.q_list.append(q)

        self.lc = lcs.stitch(lambda x: x.remove_nans().normalize())

    def extract_tic(self, tic_entry, pointing: TessPointing):
        self.tic_id = int(tic_entry['ID'])
        self.t_mag = float(tic_entry['Tmag']) * u.mag
        self.tic_entry = tic_entry
        self.sectors = pointing.sectors
        self.cameras = pointing.cameras
        self.ccds = pointing.ccds
        self.pixel_pos = pointing.pixel_pos

    @property
    def observed(self):
        return self.lc is not None

    @staticmethod
    def pointing(coord: SkyCoord):
        result = tess_stars2px(8675309, coord.ra.degree, coord.dec.degree)
        return TessPointing(result)

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