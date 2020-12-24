# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/fits_align/ident.py
# Compiled at: 2018-11-14 07:46:58
# Size of source mod 2**32: 8069 bytes
"""
    FITS Align - Align and reproject FITS files from Las Cumbres Observatory
    Copyright (C) 2018 Edward Gomez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import
from . import imgcat
from . import quad
from . import star
import sys, os, numpy as np, logging
logger = logging.getLogger(__name__)

class Identification:
    __doc__ = '\n    Represents the identification of a transform between two ImgCat objects.\n    Regroups all the star catalogs, the transform, the quads, the candidate, etc.\n\n    All instance attributes are listed below.\n\n    :ivar ref: ImgCat object of the reference image\n    :ivar ukn: ImgCat object of the unknown image\n    :ivar ok: boolean, True if the idendification was successful.\n    :ivar trans: The SimpleTransform object that represents the geometrical transform from ukn to ref.\n    :ivar uknmatchstars: A list of Star objects of the catalog of the unknown image...\n    :ivar refmatchstars: ... that correspond to these Star objects of the reference image.\n    :ivar medfluxratio: Median flux ratio between the images: "ukn * medfluxratio = ref"\n        A high value corresponds to a shallow unknown image.\n        It gets computed by the method calcfluxratio, using the matched stars.\n    :ivar stdfluxratio: Standard error on the flux ratios of the matched stars.\n\n\n\n    '

    def __init__(self, ref, ukn):
        """

        :param ref: The reference image
        :type ref: ImgCat object
        :param ukn: The unknown image, whose transform will be adjusted to match the ref
        :type ukn: ImgCat object

        """
        self.ref = ref
        self.ukn = ukn
        self.ok = False
        self.trans = None
        self.uknmatchstars = []
        self.refmatchstars = []
        self.cand = None
        self.medfluxratio = None
        self.stdfluxratio = None

    def findtrans(self, r=5.0, verbose=True):
        """
        Find the best trans given the quads, and tests if the match is sufficient
        """
        if len(self.ref.starlist) < 4:
            logger.debug('Not enough stars in the reference catalog.')
            return
        else:
            if len(self.ukn.starlist) < 4:
                logger.debug('Not enough stars in the unknown catalog.')
                return
            else:
                if len(self.ukn.starlist) < 5:
                    minnident = 4
                else:
                    minnident = max(4, min(8, len(self.ukn.starlist) / 5.0))
                minquaddist = 0.005
                if self.ref.quadlevel == 0:
                    self.ref.makemorequads(verbose=verbose)
                if self.ukn.quadlevel == 0:
                    self.ukn.makemorequads(verbose=verbose)
            while self.ok == False:
                cands = quad.proposecands((self.ukn.quadlist), (self.ref.quadlist), n=4, verbose=verbose)
                if len(cands) != 0 and cands[0]['dist'] < minquaddist:
                    for cand in cands:
                        nident = star.identify((self.ukn.starlist), (self.ref.starlist), trans=(cand['trans']), r=r, getstars=False)
                        if nident >= minnident:
                            self.trans = cand['trans']
                            self.cand = cand
                            self.ok = True
                            break

                if self.ok == False:
                    addedmorerefquads = self.ref.makemorequads(verbose=verbose)
                    addedmoreuknquads = self.ukn.makemorequads(verbose=verbose)
                    if addedmorerefquads == False:
                        if addedmoreuknquads == False:
                            break

            if self.ok:
                self.uknmatchstars, self.refmatchstars = star.identify((self.ukn.starlist), (self.ref.starlist), trans=(self.trans), r=r, getstars=True)
                logger.debug('Refitting transform (before/after) :')
                logger.debug(self.trans)
                newtrans = star.fitstars(self.uknmatchstars, self.refmatchstars)
                if newtrans != None:
                    self.trans = newtrans
                    logger.debug(self.trans)
                self.uknmatchstars, self.refmatchstars = star.identify((self.ukn.starlist), (self.ref.starlist), trans=(self.trans), r=r, getstars=True)
                logger.debug("I'm done !")
            else:
                logger.debug('Failed to find transform !')

    def calcfluxratio(self, verbose=True):
        """
        Computes a very simple median flux ratio between the images.
        The purpose is simply to get a crude guess, for images with e.g. different exposure times.
        Given that we have these corresponding star lists in hand, this is trivial to do once findtrans was run.
        """
        assert len(self.uknmatchstars) == len(self.refmatchstars)
        if len(self.refmatchstars) == 0:
            logger.debug('No matching stars to compute flux ratio !')
            return
        reffluxes = star.listtoarray((self.refmatchstars), full=True)[:, 2]
        uknfluxes = star.listtoarray((self.uknmatchstars), full=True)[:, 2]
        fluxratios = reffluxes / uknfluxes
        self.medfluxratio = float(np.median(fluxratios))
        self.stdfluxratio = float(np.std(fluxratios))
        logger.debug('Computed flux ratio from %i matches : median %.2f, std %.2f' % (len(reffluxes), self.medfluxratio, self.stdfluxratio))


def make_transforms(ref, ukns, hdu=0, skipsaturated=False, r=5.0, n=500):
    """
    Top-level function to identify transforms between images.
    Returns a list of Identification objects that contain all the info to go further.

    :param ref: path to a FITS image file that will act as the "reference".
    :type ref: string

    :param ukns: list of paths to FITS files to be "aligned" on the reference. **ukn** stands for unknown.
    :type ref: list of strings

    :param hdu: The hdu of the fits files (same for all) that you want me to use. 0 is somehow "automatic". If multihdu, 1 is usually science.

    :param skipsaturated: Should I skip saturated stars ?
    :type skipsaturated: boolean

    :param r: Identification radius in pixels of the reference image (default 5.0 should be fine).
    :type r: float
    :param n: Number of brightest stars of each image to consider (default 500 should be fine).
    :type n: int

    """
    logger.debug('Preparing reference ...')
    ref = imgcat.ImgCat(ref, hdu=hdu)
    ref.makecat()
    ref.makestarlist(skipsaturated=skipsaturated, n=n)
    ref.makemorequads()
    identifications = []
    for ukn in ukns:
        logger.debug('Processing {}'.format(ukn))
        ukn = imgcat.ImgCat(ukn, hdu=hdu)
        ukn.makecat()
        ukn.makestarlist(skipsaturated=skipsaturated, n=n)
        idn = Identification(ref, ukn)
        idn.findtrans(r=r)
        idn.calcfluxratio()
        identifications.append(idn)

    return identifications