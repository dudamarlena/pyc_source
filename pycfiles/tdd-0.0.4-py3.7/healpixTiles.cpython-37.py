# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdd/healpixTiles.py
# Compiled at: 2019-04-15 09:04:07
# Size of source mod 2**32: 11069 bytes
"""
Implement a concrete `Tiling` class on the basis of healpix tiles. The
heavy lifting is done by the package OpSimSummary.
"""
from __future__ import absolute_import, print_function, division
import healpy as hp, numpy as np, pandas as pd
from .tessellations import Tiling
from sqlalchemy import create_engine
from .trig import pixelsToAng
from .summarize_opsim import PointingTree
from past.builtins import basestring, xrange
__all__ = [
 'HealpixTiles']

class HealpixTiles(Tiling):
    __doc__ = '\n    A concrete Tiling class based on Healpix Tiles. The user is\n    allowed to choose the following parameters:\n\n    Attributes\n    ----------\n    nside : int, power of 2, defaults to 256\n        healpix nside parameter\n\n    '

    def __init__(self, nside=256, opsimdf=None, healpixelizedOpSim=None, preComputedMap=None, leafsize=50, fovRadius=1.75, raCol='ditheredRA', decCol='ditheredDec'):
        """
        nside : int, power of 2, defaults to 256
            nside parameter of healpix. determines the size of the tiles
            so that there are 12 * nside **2 equally sized tiles covering
            the sphere.
        """
        self.nside = nside
        self.maxradius = hp.max_pixrad(nside=(self.nside))
        self.npix = hp.nside2npix(nside)
        self._tileArea = hp.nside2pixarea(nside)
        self.hpOpSim = healpixelizedOpSim
        self._preComputedMap = preComputedMap
        self.opsimdf = opsimdf
        if self.hpOpSim is None:
            if self.preComputedMap is None:
                if self.opsimdf is None:
                    raise ValueError('hpOpSim and preComputedMap and opsimdf cannot both be None')
        self._preComputedEngine = None
        self.fovRadius = np.radians(fovRadius)
        self.pointingTree = None
        if self.opsimdf is not None:
            self.pointingTree = PointingTree((self.opsimdf), raCol=raCol,
              decCol=decCol,
              leafSize=leafsize,
              indexCol='obsHistID')

    @property
    def preComputedMap(self):
        if self._preComputedMap is not None:
            if isinstance(self._preComputedMap, basestring):
                self._preComputedMap = self._preComputedMap.startswith('sqlite') or 'sqlite:///' + self._preComputedMap
            else:
                if callable(self._preComputedMap):
                    pass
        return self._preComputedMap

    @property
    def preComputedEngine(self):
        engine = self._preComputedEngine
        if engine is None:
            engine = create_engine((self.preComputedMap), echo=False)
        return engine

    @property
    def tileIDSequence(self):
        return xrange(self.npix)

    def area(self, tileID):
        if tileID not in self.tileIDSequence:
            raise ValueError('parameter tileID not in set of healpixIDs')
        return self._tileArea * np.degrees(1.0) * np.degrees(1.0)

    def tileIDsForSN(self, ra, dec):
        """
        Parameters
        ----------
        ra : `numpyp.ndarray` or float, degrees, mandatory
        dec : `numpy.ndarray` or float, degrees, mandatory
        """
        dec = np.ravel(dec)
        ra = np.ravel(ra)
        theta = -np.radians(dec) + np.pi / 2.0
        phi = np.radians(ra)
        inds = hp.ang2pix(nside=(self.nside), theta=theta, phi=phi, nest=True)
        return inds

    def _pointingFromPrecomputedDB(self, tileID, tableName='simlib'):
        if isinstance(self._preComputedMap, basestring):
            sql = 'SELECT obsHistID FROM {0} WHERE ipix == {1}'.format(tableName, tileID)
            return pd.read_sql_query(sql, con=(self.preComputedEngine)).values.flatten()
        if callable(self._preComputedMap):
            return self._preComputedMap(tileID)
        raise ValueError('Only options used are sqlite DB and callable')

    def _pointingFromHpOpSim(self, tileID):
        return self.hpOpSim.obsHistIdsForTile(tileID)

    def _pointingFromPointingTree(self, tileID):
        """
        private method to go from healpix Tile ID (nest) to the maximal set of
        pointings intersecting the tile.

        Parameters
        ----------
        tileID : int
            Healpix TileID in the nested convention for which we are trying to
            calculate the maximal pointings
        """
        ravals, decvals = pixelsToAng(tileID, (self.nside), nest=True, convention='celestial',
          unit='degrees')
        circRadius = np.degrees(self.maxradius)
        fovRadius = np.degrees(self.fovRadius)
        return self.pointingTree.pointingsEnclosing(ravals, decvals, circRadius=circRadius,
          pointingRadius=fovRadius)

    def _tileFromHpOpSim(self, pointing):
        return self.hpOpSim.set_index('obsHistID').ix(pointing)['hids']

    def _tileFromPreComputedDB(self, pointing, tableName='simlib'):
        sql = 'SELECT ipix FROM {0} WHERE obsHistID == {1}'.format(tableName, pointing)
        return pd.read_sql_query(sql, con=(self.preComputedEngine)).values.flatten()

    def tilesForPointing(self, pointing, alltiles=None, **kwargs):
        """
        return a maximal sequence of tile ID s for a particular OpSim pointing
        """
        if self.preComputedMap is not None:
            return self._tileFromPreComputedDB(self,
              pointing, tableName='simlib')
        if self.hpOpSim is not None:
            return self._tileFromHpOpSim(self, pointing)
        raise ValueError('both attributes preComputedMap and hpOpSim cannot be None')

    def pointingSequenceForTile(self, tileID, allPointings=None, columns=None, **kwargs):
        """
        return a maximal sequence of pointings for a particular tileID.
        """
        obsHistIDs = None
        if self.preComputedMap is not None:
            obsHistIDs = self._pointingFromPrecomputedDB(tileID,
              tableName='simlib')
        else:
            if self.hpOpSim is not None:
                obsHistIDs = self._pointingFromHpOpSim(tileID)
            else:
                if self.pointingTree is not None:
                    obsHistIDs = self._pointingFromPointingTree(tileID)
                else:
                    raise ValueError('both attributes preComputedMap and hpOpSim cannot be None')
        obsHistIDs = obsHistIDs[0]
        if allPointings is None or columns is None:
            return obsHistIDs
        names = list(columns)
        return allPointings.ix[obsHistIDs][names]

    def _angularSamples(self, phi_c, theta_c, radius, numSamples, tileID, rng):
        phi, theta = super(self.__class__, self).samplePatchOnSphere(phi=phi_c, theta=theta_c,
          delta=radius,
          size=numSamples,
          degrees=False,
          rng=rng)
        tileIds = hp.ang2pix(nside=(self.nside), theta=theta, phi=phi,
          nest=True)
        inTile = tileIds == tileID
        return (phi[inTile], theta[inTile])

    def positions(self, tileID, numSamples, rng=None):
        """
        Return a tuple of (res_phi, res_theta) where res_phi and res_theta are
        spatially uniform samples  of positions of size numSamples within the
        healpix Tile with ipix=tileID in the nested scheme. The return values
        should be in degrees, with the convention that theta is 0 on the equator and
        90 degrees at the North Pole.

        Parameters
        ----------
        tileID: int, mandatory
            healpix TileID, nested scheme
        numSamples: int, mandatory
            number of positions required
        rng: `np.random.RandomState`
            random state for sampling involved

        Returns
        -------
        tuple
            (ra, dec) where each of those elements are `numpy.ndarray`

        .. note :: 1. The inelegant method is sampling a circle with a radius
            twice that required to have an area equal to the healpix tile. This
            operation can be done by self.samplePatchOnSphere and returns
            numSamples, some of which are not on the healpixTiles.
            2. `self._angularSamples` returns only those of this sequence which
            lie on the original tile.
            3. by repeating the process till the number obtained matches the number
            requested, we obtain nsamples on the tile.
            4. The method works as long as the radius is large enough so that
            corners of the tile are not outside the circle sampled.
        """
        if rng is None:
            rng = np.random.RandomState(tileID)
        res_theta = np.zeros(numSamples)
        res_phi = np.zeros(numSamples)
        theta_c, phi_c = np.degrees(hp.pix2ang(nside=(self.nside), ipix=tileID,
          nest=True))
        radius = 2 * np.sqrt(self.area(tileID) / np.pi)
        num_already = 0
        while numSamples > 0:
            phi, theta = self._angularSamples(phi_c, theta_c, radius=radius, numSamples=numSamples,
              tileID=tileID,
              rng=rng)
            s = rng.get_state()
            num_obtained = len(phi)
            res_phi[num_already:num_obtained + num_already] = phi
            res_theta[num_already:num_obtained + num_already] = theta
            num_already += num_obtained
            numSamples -= num_obtained

        return (
         np.degrees(res_phi), -np.degrees(res_theta) + 90.0)