# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdd/lightcurve.py
# Compiled at: 2019-06-03 05:38:56
# Size of source mod 2**32: 19423 bytes
"""
Class for holding Light Curve Data
"""
from __future__ import absolute_import, print_function, division
from future.utils import with_metaclass
from future.moves.itertools import zip_longest
import abc
from collections import Sequence
import numpy as np, pandas as pd
from astropy.table import Table
import sncosmo
from .aliases import aliasDictionary
__all__ = [
 'BaseLightCurve', 'LightCurve']

class BaseLightCurve(with_metaclass(abc.ABCMeta, object)):
    __doc__ = '\n    Abstract Base Class for Light Curve Data showing methods that need to be\n    implemented.\n    '

    @abc.abstractproperty
    def props(self):
        pass

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractproperty
    def lightCurve(self):
        """
        `pd.DataFrame` holding the lightCurve information. There can be more
        columns, but the following columns are mandatory:
        ['mjd', 'band', 'flux', 'fluxerr', 'zp', 'zpsys']
        """
        pass

    @abc.abstractmethod
    def snCosmoLC(self, coaddTimes=None):
        pass

    @abc.abstractmethod
    def coaddedLC(self, coaddTimes=None, timeOffset=0.0, timeStep=1.0, *args, **kwargs):
        pass

    @abc.abstractmethod
    def remap_filters(names, bandNameDict, ignore_case):
        pass

    @abc.abstractmethod
    def missingColumns(self, lcdf):
        notFound = self.mandatoryColumns - set(lcdf.columns)
        return notFound

    @staticmethod
    def requiredColumns():
        """
        """
        reqd = set(['mjd', 'band', 'flux', 'fluxerr', 'zp', 'zpsys'])
        return reqd

    @property
    def mandatoryColumns(self):
        """
        A list of mandatory columns in the light curve dataFrame with
        possible aliases in `self.mandatoryColumnAliases`.

        mjd : time
        band : string
        flux : model flux
        """
        return self.requiredColumns()

    @property
    def columnAliases(self):
        """
        dictionary that maps standard names as keys to a possible set of
        aliases
        """
        aliases = {}
        aliases['zp'] = [
         'zp']
        aliases['mjd'] = ['time', 'expmjd', 'date']
        aliases['zpsys'] = ['magsys']
        aliases['band'] = ['filter', 'filtername', 'bandname', 'bands', 'flt']
        aliases['flux'] = ['fluxcal']
        aliases['fluxerr'] = ['flux_err', 'flux_errs', 'fluxerror', 'fluxcalerr']
        return aliases


class LightCurve(BaseLightCurve):
    __doc__ = "\n    A Class to represent light curve data.  Light curve data is often available\n    with different kinds of column names. This class homogenizes them to a set\n    of standard names, and allows simple calculations to be based on the same\n    variable names 'mjd', 'band', 'flux', 'fluxerr', 'zp', 'zpsys' which denote\n    the time of observation, bandpass of observation, the flux and flux\n    uncertainty of the observation.\n\n    zp represents the zero point to convert the flux value to the phsyical flux\n    using the zero point system zpsys.\n    "

    def __init__(self, lcdf, bandNameDict=None, ignore_case=True, propDict=None, cleanNans=True):
        """
        Instantiate Light Curve class

        Parameters
        ----------
        lcdf : `pd.DataFrame`, mandatory
            light curve information, must contain columns `mjd`, `band`, `flux`,
            `flux_err`, `zp`, `zpsys`
        bandNameDict : dictionary, optional, default to None
            dictionary of the values in the 'band' column or its alias, and
            values that it should be mapped to.
        ignore_case : bool, optional, defaults to True
            ignore the case of the characters in the strings representing
            bandpasses
        propDict : Dictionary, optional, defaults to None
            a dictionary of properties associated with the light curve
        cleanNans : Bool, defaults to True
            if True, ensures that at the time of returning `snCosmoLC()` objects
            which are used in fits, any row that has a `NAN` in it will be
            dropped
        Example
        -------
        >>> from analyzeSN import LightCurve
        >>> ex_data = sncosmo.load_example_data()
        >>> lc = LightCurve(ex_data.to_pandas()) 
        """
        aliases = self.columnAliases
        standardNamingDict = aliasDictionary(lcdf.columns, aliases)
        if len(standardNamingDict) > 0:
            lcdf.rename(columns=standardNamingDict, inplace=True)
        missingColumns = self.missingColumns(lcdf)
        if len(missingColumns) > 0:
            raise ValueError('light curve data has missing columns', missingColumns)
        self.bandNameDict = bandNameDict
        self._lightCurve = lcdf
        self.ignore_case = ignore_case
        self._propDict = propDict
        self.cleanNans = cleanNans

    @property
    def props(self):
        return self._propDict

    @classmethod
    def fromSALTFormat(cls, fname):
        _lc = sncosmo.read_lc(fname, format='salt2')
        lc = _lc.to_pandas()
        lc.MagSys = 'ab'

        def filtername(x):
            if 'megacam' in x.lower():
                return 'megacam'
            return x[:-3].lower()

        banddict = dict(((key.lower(), filtername(key) + key[(-1)]) for key in lc.Filter.unique()))
        return cls(lc, bandNameDict=banddict,
          ignore_case=True,
          propDict=(_lc.meta))

    def missingColumns(self, lcdf):
        """
        return a set of columns in the light curve dataframe that are missing
        from the mandatory set of columns

        Parameters
        ----------
        lcdf : `pd.dataFrame`
            a light curve represented as a pandas dataframe
        """
        notFound = self.mandatoryColumns - set(lcdf.columns)
        return notFound

    @staticmethod
    def remap_filters(name, nameDicts, ignore_case=True):
        """
        """
        try:
            if ignore_case:
                _nameDicts = dict(((key.lower(), value) for key, value in nameDicts.items()))
                return _nameDicts[name.lower()]
            return nameDicts[name]
        except:
            raise NotImplementedError('values for old filter {} not implemented', name)

    @property
    def lightCurve(self):
        """
        The lightcurve in native format
        """
        _lc = self._lightCurve.copy()
        _lc.band = _lc.band.apply(lambda x: x.decode())
        _lc.band = _lc.band.apply(lambda x: x.strip())
        if self.bandNameDict is not None:
            _lc.band = _lc.band.apply(lambda x: self.remap_filters(x, self.bandNameDict, self.ignore_case))
        return _lc

    def snCosmoLC(self, coaddTimes=None, mjdBefore=0.0, minmjd=None):
        lc = self.coaddedLC(coaddTimes=coaddTimes, mjdBefore=mjdBefore, minmjd=minmjd).rename(columns=dict(mjd='time'))
        if self.cleanNans:
            lc.dropna(inplace=True)
        return Table.from_pandas(lc)

    @staticmethod
    def sanitize_nan(lcs):
        """
        .. note:: These methods are meant to be applied to photometric tables
        as well
        """
        lcs = lcs.copy()
        avg_error = lcs.fluxerr.mean(skipna=True)
        lcs.fillna(dict(flux=0.0, fluxerr=avg_error), inplace=True)
        return lcs

    @staticmethod
    def discretize_time(lcs, timeOffset=0.0, timeStep=1.0):
        """
        .. note:: These methods are meant to be applied to photometric tables
        as well
        """
        lcs['night'] = (lcs.mjd - timeOffset) // timeStep
        lcs.night = lcs.night.astype(np.int)
        return lcs

    @staticmethod
    def add_weightedColumns(lcs, avg_cols=('mjd', 'flux', 'fluxerr', 'zp'), additional_cols=None, copy=False):
        avg_cols = list(tuple(avg_cols))
        if additional_cols is not None:
            avg_cols += list(additional_cols)
        if copy:
            lcs = lcs.copy()
        if 'weights' not in lcs.columns:
            if 'fluxerr' not in lcs.columns:
                raise ValueError('Either fluxerr or weights must be a column in the dataFrame')
            lcs['weights'] = 1.0 / lcs['fluxerr'] ** 2
        for col in avg_cols:
            if col != 'fluxerr':
                lcs['weighted_' + col] = lcs[col] * lcs['weights']

        return lcs

    @staticmethod
    def coaddpreprocessed(preProcessedlcs, include_snid=True, cols=('mjd', 'flux', 'fluxerr', 'zp', 'zpsys'), additionalAvgCols=None, additionalColsKept=None, additionalAggFuncs='first', keepAll=False, keepCounts=True):
        """
        Parameters
        ----------
        preProcessedlcs :
        include_snid :
        cols :
        additionalAvgCols : list of strings
        
        .. note:: These methods are meant to be applied to photometric tables
        as well
        """
        grouping = [
         'band', 'night']
        if include_snid:
            grouping = [
             'snid'] + grouping
        default_avg_cols = ['mjd', 'flux', 'zp']
        avg_cols = default_avg_cols
        if additionalAvgCols is not None:
            avg_cols += additionalAvgCols
        default_add_cols = ['zpsys']
        lcs = preProcessedlcs
        grouped = lcs.groupby(grouping)
        aggdict = dict((('weighted_' + col, np.sum) for col in avg_cols))
        aggdict['weights'] = np.sum
        if keepCounts:
            lcs['numExpinCoadd'] = lcs.mjd.copy()
            aggdict['numExpinCoadd'] = 'count'
            aggdict['zpsys'] = 'first'
        keptcols = grouping + ['zpsys']
        if additionalColsKept is not None:
            aggFuncScalar = True
            if isinstance(additionalAggFuncs, basestring):
                aggFuncScalar = True
            else:
                if isinstance(additionalAggFuncs, Sequence):
                    aggFuncScalar = False
                    if len(additionalAggFuncs) != len(additionalColsKept):
                        raise ValueError('if sequence, length of aggfuncs and additionalColsKept should match')
                    else:
                        aggFuncScalar = True
                elif aggFuncScalar:
                    newaggs = zip_longest(additionalColsKept, (additionalAggFuncs,), fillvalue=additionalAggFuncs)
                else:
                    newaggs = zip(additionalColsKept, additionalAggFuncs)
                for col, val in newaggs:
                    aggdict[col] = val

            keptcols += list(additionalColsKept)
        x = grouped.agg(aggdict)
        weighted_cols = list((col for col in x.reset_index().columns if col.startswith('weighted') if col != 'weighted_fluxerr'))
        yy = x.reset_index()[weighted_cols].apply((lambda y: y / x.weights.values), axis=0)
        yy['weighted_fluxerr_coadded'] = 1.0 / np.sqrt(x.reset_index()['weights'])
        yy.rename(columns=(dict(((col, col.split('_')[1]) for col in yy.columns))), inplace=True)
        if keepCounts:
            keptcols += ['numExpinCoadd']
        return x.reset_index()[keptcols].join(yy)

    @staticmethod
    def summarize(lcdf, vals=('SNR', 'mjd', 'zp'), aggfuncs=(
 max, [max, min], 'count'), SNRmin=-10000.0, paramsdf=None, grouping=('snid', 'band'), summary_prefix='', prefix_interpret='', useSNR=True):
        """
        summarize a light curve of set of light curves using the functions
        `aggfunctions` to aggregate over the values in `vals` over groups
        defined by grouping

        Parameters
        ----------
        lcdf : `pd.DataFrame`
            light curve(s) to aggregate over
        vals : tuple of strings
            column names to aggregate over
        aggfunctions : tuple of functions
            tuple of functions to use to aggregate the values in `vals`. Must
            have the same length as vals.
        paramsdf : `pd.DataFrame`, defaults to None
            dataframe with one or more rows of truth parameters indexed by the
            snid.

        .. note ::
        """
        lcdf = lcdf.copy()
        noSNID = False
        if 'snid' not in lcdf.columns:
            lcdf['snid'] = 0
            noSNID = True
            raise Warning('SNID not supplied, assuming that all records for a single SN')
        else:
            fluxcol = prefix_interpret + 'flux'
            fluxerrcol = prefix_interpret + 'fluxerr'
            if 'SNR' not in lcdf.columns and useSNR:
                if not (fluxcol in lcdf.columns and fluxerrcol in lcdf.columns):
                    raise ValueError('The flux and flux error columns cannot be found to calculate SNR', fluxcol, fluxerrcol)
                lcdf['SNR'] = lcdf[fluxcol] / lcdf[fluxerrcol]
        lcdf = lcdf.query('SNR > @SNRmin')
        grouped = lcdf.groupby(list(grouping))
        mapdict = dict(tuple(zip(vals, aggfuncs)))
        summary = grouped.agg(mapdict)
        unstackvars = set(grouping) - set(('snid', ))
        if len(unstackvars) > 0:
            summary = summary.unstack()
        else:
            columns = list(('_'.join(col).strip() for col in summary.columns.values))
            summary.columns = columns
            namedicts = dict(((col, 'NOBS' + col.split('count')[(-1)]) for col in columns if 'count' in col))
            summary.rename(columns=namedicts, inplace=True)
            summary.rename(columns=(dict(((col, summary_prefix + col) for col in summary.columns))),
              inplace=True)
            if paramsdf is None:
                return summary
                if noSNID:
                    if len(paramsdf) > 1:
                        raise ValueError('Cannot crossmatch SN with paramsdf without SNID')
                else:
                    if 'snid' == paramsdf.index.name:
                        summary.index = paramsdf.index.values
                        return summary.join(paramsdf)
                    paramsdf.index = 0
                    return summary.join(paramsdf)
            else:
                if len(set(lcdf.snid.unique()) - set(paramsdf.index.values)) > 0:
                    raise ValueError('There are  SN in lcdf not in paramsdf')
                return summary.join(paramsdf)

    def coaddedLC(self, coaddTimes=None, minmjd=None, coaddedValues=[
 'mjd', 'flux', 'fluxerr', 'zp'], additionalValues=[
 'zpsys'], mjdBefore=None, sanitize=True):
        """
        """
        if minmjd is None:
            if mjdBefore is None:
                minmjd = 0.0
            else:
                minmjd = self.lightCurve.mjd.min() - mjdBefore
        include_snid = 'snid' in self.lightCurve.columns
        if not sanitize:
            raise NotImplementedError('nan sanitization must be used for coadds\n')
        lc = self.sanitize_nan(self.lightCurve)
        if coaddTimes is None:
            if self.cleanNans:
                lc = self.lightCurve.dropna(inplace=False)
            return lc
        lc = self.discretize_time(lc, timeOffset=minmjd, timeStep=coaddTimes)
        lc = self.add_weightedColumns(lc, avg_cols=coaddedValues,
          additional_cols=None,
          copy=True)
        lc = self.coaddpreprocessed(lc, include_snid=include_snid,
          cols=coaddedValues,
          additionalAvgCols=None,
          additionalColsKept=None,
          keepAll=False,
          keepCounts=True)
        return lc

    def _coaddedLC(self, coaddTimes=None, mjdBefore=None, minmjd=None):
        """
        return a coadded light curve
        """
        if coaddTimes is None:
            return self.lightCurve
        if minmjd is None:
            if mjdBefore is None:
                mjdBefore = 0.0
            minmjd = self.lightCurve.mjd.min() - mjdBefore
        lc = self.lightCurve.copy()
        lc['discreteTime'] = (lc['mjd'] - minmjd) // coaddTimes
        lc['discreteTime'] = lc.discreteTime.astype(int)
        aggregations = {'mjd':np.mean, 
         'flux':np.mean, 
         'fluxerr':lambda x: np.sqrt(np.sum(x ** 2)) / len(x), 
         'discreteTime':'count', 
         'zp':np.mean, 
         'zpsys':'first'}
        groupedbynightlyfilters = lc.groupby(['discreteTime', 'band'])
        glc = groupedbynightlyfilters.agg(aggregations)
        glc.reset_index('band', inplace=True)
        glc.rename(columns=dict(discreteTime='numCoadded'), inplace=True)
        glc['CoaddedSNR'] = glc['flux'] / glc['fluxerr']
        return glc