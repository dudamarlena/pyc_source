# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/spectra/spectral_region.py
# Compiled at: 2020-03-19 14:18:03
# Size of source mod 2**32: 9577 bytes
import itertools, sys, numpy as np
import astropy.units as u

class SpectralRegion:
    __doc__ = '\n    A `SpectralRegion` is a container class that enables some simplicty\n    in defining and passing a region (interval) for a spectrum.\n\n    In the future, there might be more functionality added in here, and there\n    is some discussion that this might/could move to\n    `Astropy Regions <http://astropy-regions.readthedocs.io/en/latest/>`_.\n\n    Parameters\n    ----------\n\n    lower : Scalar `~astropy.units.Quantity` with pixel or any valid ``spectral_axis`` unit\n       The lower bound of the region.\n\n    upper : Scalar `~astropy.units.Quantity` with pixel or any valid ``spectral_axis`` unit\n       The upper bound of the region.\n\n    Notes\n    -----\n    The subregions will be ordered based on the lower bound of each subregion.\n\n    '

    @classmethod
    def from_center(cls, center=None, width=None):
        """
        SpectralRegion class method that enables the definition of a `SpectralRegion`
        from the center and width rather than lower and upper bounds.

        Parameters
        ----------

        center : Scalar `~astropy.units.Quantity` with pixel or any valid ``spectral_axis`` unit
           The center of the spectral region.

        width : Scalar `~astropy.units.Quantity` with pixel or any valid ``spectral_axis`` unit
           The width of the spectral region.
        """
        if width.value <= 0:
            raise ValueError('SpectralRegion width must be positive.')
        return cls(center - width, center + width)

    def __init__(self, *args):
        """
        Lower and upper values for the interval.
        """
        self._subregions = None
        if self._is_2_element(args):
            self._subregions = [
             tuple(args)]
        else:
            if isinstance(args, (list, tuple)):
                if all([self._is_2_element(x) for x in args[0]]):
                    self._subregions = [tuple(x) for x in args[0]]
                else:
                    raise ValueError('SpectralRegion input must be a 2-tuple or a list of 2-tuples.')
            else:
                assert self._valid(), 'SpectralRegion 2-tuple lower extent must be less than upper extent.'
            self._reorder()

    def _info(self):
        """
        Pretty print the sub-regions.
        """
        toreturn = 'Spectral Region, {} sub-regions:\n'.format(len(self._subregions))
        subregion_text = []
        for ii, subregion in enumerate(self._subregions):
            subregion_text.append('  ({}, {})'.format(subregion[0], subregion[1]))

        max_len = max((len(srt) for srt in subregion_text)) + 1
        ncols = 70 // max_len
        fmt = '{' + ':<{}'.format(max_len) + '}'
        for ii, srt in enumerate(subregion_text):
            toreturn += fmt.format(srt)
            if ii % ncols == ncols - 1:
                toreturn += '\n'

        return toreturn

    def __str__(self):
        return self._info()

    def __repr__(self):
        return self._info()

    def __add__(self, other):
        """
        Ability to add two SpectralRegion classes together.
        """
        return SpectralRegion(self._subregions + other._subregions)

    def __iadd__(self, other):
        """
        Ability to add one SpectralRegion to another using +=.
        """
        self._subregions += other._subregions
        self._reorder()
        return self

    def __len__(self):
        """
        Number of spectral regions.
        """
        return len(self._subregions)

    def __getslice__(self, item):
        """
        Enable slicing of the SpectralRegion list.
        """
        return SpectralRegion(self._subregions[item])

    def __getitem__(self, item):
        """
        Enable slicing or extracting the SpectralRegion.
        """
        if isinstance(item, slice):
            return self.__getslice__(item)
        return SpectralRegion([self._subregions[item]])

    def __delitem__(self, item):
        """
        Delete a specific item from the list.
        """
        del self._subregions[item]

    def _valid(self):
        sub_regions = [(x[0].to('m'), x[1].to('m')) if x[0].unit.is_equivalent(u.m) else x for x in self._subregions]
        if any((x[0] >= x[1] for x in sub_regions)):
            raise ValueError('Lower bound must be strictly less than the upper bound')
        return True

    def _is_2_element(self, value):
        """
        Helper function to check a variable to see if it
        is a 2-tuple.
        """
        return len(value) == 2 and isinstance(value[0], u.Quantity) and isinstance(value[1], u.Quantity)

    def _reorder(self):
        """
        Re-order the  list based on lower bounds.
        """
        self._subregions.sort(key=(lambda k: k[0]))

    @property
    def subregions(self):
        return self._subregions

    @property
    def bounds(self):
        """
        Compute the lower and upper extent of the SpectralRegion.
        """
        return (
         self.lower, self.upper)

    @property
    def lower(self):
        """
        The most minimum value of the sub-regions.

        The sub-regions are ordered based on the lower bound, so the
        lower bound for this instance is the lower bound of the first
        sub-region.
        """
        return self._subregions[0][0]

    @property
    def upper(self):
        """
        The most maximum value of the sub-regions.

        The sub-regions are ordered based on the lower bound, but the
        upper bound might not be the upper bound of the last sub-region
        so we have to look for it.
        """
        return max((x[1] for x in self._subregions))

    def invert_from_spectrum(self, spectrum):
        """
        Invert a SpectralRegion based on the extent of the
        input spectrum.

        See notes in SpectralRegion.invert() method.
        """
        return self.invert(spectrum.spectral_axis[0], spectrum.spectral_axis[(-1)])

    def _in_range(self, value, lower, upper):
        return value >= lower and value <= upper

    def invert(self, lower_bound, upper_bound):
        """
        Invert this spectral region.  That is, given a set of sub-regions this
        object defines, create a new `SpectralRegion` such that the sub-regions
        are defined in the new one as regions *not* in this `SpectralRegion`.

        Parameters
        ----------

        lower_bound : Scalar `~astropy.units.Quantity` with pixel or any valid ``spectral_axis`` unit
           The lower bound of the region.

        upper_bound : Scalar `~astropy.units.Quantity` with pixel or any valid ``spectral_axis`` unit
           The upper bound of the region.

        Returns
        -------
        spectral_region : `~specutils.SpectralRegion`
           Spectral region of the non-selected regions

        Notes
        -----
        This is applicable if, for example, a `SpectralRegion` has sub-regions
        defined for peaks in a spectrum and then one wants to create a
        `SpectralRegion` defined as all the *non*-peaks, then one could use this
        function.

        As an example, assume this SpectralRegion is defined as
        ``sr = SpectralRegion([(0.45*u.um, 0.6*u.um), (0.8*u.um, 0.9*u.um)])``.
        If we call ``sr_invert = sr.invert(0.3*u.um, 1.0*u.um)`` then
        ``sr_invert`` will be
        ``SpectralRegion([(0.3*u.um, 0.45*u.um), (0.6*u.um, 0.8*u.um), (0.9*u.um, 1*u.um)])``

        """
        min_num = -sys.maxsize - 1
        max_num = sys.maxsize
        rs = self._subregions + [(min_num * u.um, lower_bound),
         (
          upper_bound, max_num * u.um)]
        sorted_regions = sorted(rs, key=(lambda k: k[0]))
        merged = []
        for higher in sorted_regions:
            if not merged:
                merged.append(higher)
            else:
                lower = merged[(-1)]
                if higher[0] <= lower[1]:
                    upper_bound = max(lower[1], higher[1])
                    merged[-1] = (lower[0], upper_bound)
                else:
                    merged.append(higher)

        newlist = list(itertools.chain.from_iterable(merged))
        newlist = newlist[1:-1]
        return SpectralRegion([(x, y) for x, y in zip(newlist[0::2], newlist[1::2])])