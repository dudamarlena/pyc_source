# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./cynet.py
# Compiled at: 2018-08-23 00:21:39
"""
Spatio temporal analysis for inferrence of statistical causality
@author zed.uchicago.edu
"""
import numpy as np, random
try:
    import cPickle as pickle
except ImportError:
    import pickle

from datetime import datetime
from datetime import timedelta
from tqdm import tqdm, tqdm_pandas
from haversine import haversine
import json
from sodapy import Socrata
import operator, warnings, os, glob, subprocess, matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
plt.ioff()
from scipy.spatial import Delaunay
import seaborn as sns
__DEBUG__ = False
PRECISION = 5

class spatioTemporal():
    """
    Utilities for spatio temporal analysis
    @author zed.uchicago.edu

    Attributes:
        log_store (Pickle): Pickle storage of class data & dataframes
        log_file (string): path to CSV of legacy dataframe
        ts_store (string): path to CSV containing most recent ts export
        DATE (string):
        EVENT (string): column label for category filter
        coord1 (string): first coordinate level type; is column name
        coord2 (string): second coordinate level type; is column name
        coord3 (string): third coordinate level type;
                         (z coordinate)
        end_date (datetime.date): upper bound of daterange
        freq (string): timeseries increments; e.g. D for date
        columns (list): list of column names to use;
                        required at least 2 coordinates and event type
        types (list of strings): event type list of filters
        value_limits (tuple): boundaries (magnitude of event;
                              above threshold)
        grid (dictionary or list of lists): coordinate dictionary with
                respective ranges and EPS value OR custom list of lists
                of custom grid tiles as [coord1_start, coord1_stop,
                coord2_start, coord2_stop]
        grid_type (string): parameter to determine if grid should be built up
                            from a coordinate start/stop range ('auto') or be
                            built from custom tile coordinates ('custom')
        threshold (float): significance threshold
    """

    def __init__(self, log_store='log.p', log_file=None, ts_store=None, DATE='Date', year=None, month=None, day=None, EVENT='Primary Type', coord1='Latitude', coord2='Longitude', coord3=None, init_date=None, end_date=None, freq=None, columns=None, types=None, value_limits=None, grid=None, threshold=None):
        if not not (types is not None and value_limits is not None):
            raise AssertionError('Either types can be specified                     or value_limits: not both.')
            assert not (DATE is not None and (year is not None or month is not None or day is not None))
            if log_file is not None and year is not None and month is not None and day is not None:
                df = pd.read_csv(log_file, parse_dates={DATE: [year, month, day]})
                if types is not None:
                    for filter_subset in types:
                        for a_filter in filter_subset:
                            if a_filter not in df[EVENT].unique():
                                warnings.warn(('{} filter not in dataset, will produce empty dataframe').format(filter_subset))

                df[DATE] = pd.to_datetime(df[DATE], errors='coerce')
            else:
                df = pd.read_csv(log_file)
                df[DATE] = pd.to_datetime(df[DATE])
            df.to_pickle(log_store)
        else:
            df = pd.read_pickle(log_store)
        self._logdf = df
        self._spatial_tiles = None
        self._dates = None
        self._THRESHOLD = threshold
        if freq is None:
            self._FREQ = 'D'
        else:
            self._FREQ = freq
        self._DATE = DATE
        if init_date is None:
            self._INIT = '1/1/2001'
        else:
            self._INIT = init_date
        if end_date is not None:
            self._END = end_date
        else:
            self._END = None
        self._EVENT = EVENT
        self._coord1 = coord1
        self._coord2 = coord2
        self._coord3 = coord3
        if columns is None:
            self._columns = [
             EVENT, coord1, coord2, DATE]
        else:
            self._columns = columns
        self._types = types
        self._value_limits = value_limits
        self._ts_dict = {}
        self._grid = None
        assert grid is not None, 'Error: no grid parameter specified.'
        if isinstance(grid, dict):
            self._grid = {}
            assert self._coord1 in grid
            assert self._coord2 in grid
            assert 'Eps' in grid
            self._grid[self._coord1] = grid[self._coord1]
            self._grid[self._coord2] = grid[self._coord2]
            self._grid['Eps'] = grid['Eps']
            self._grid_type = 'auto'
        elif isinstance(grid, list):
            self._grid = grid
            self._grid_type = 'custom'
        else:
            raise TypeError('Unsupported grid type.')
        self._trng = pd.date_range(start=self._INIT, end=self._END, freq=self._FREQ)
        return

    def getTS(self, _types=None, tile=None, freq=None, poly_tile=False):
        """
        Utilities for spatio temporal analysis
        @author zed.uchicago.edu

        Given location tile boundaries and type category filter, creates the
        corresponding timeseries as a pandas DataFrame
        (Note: can reassign type filter, does not have to be the same one
        as the one initialized to the dataproc)

        Inputs:
            _types (list of strings): list of category filters
            tile (list of floats): location boundaries for tile OR
            if poly_tile is TRUE, tile is a list of tuples defining the polygon
            freq (string): intervals of time between timeseries columns
            poly_tile (boolean): whether or not input for tiles defines
            a polygon filter

        Outputs:
            pd.Dataframe of timeseries data to corresponding grid tile
            pd.DF index is stringified LAT/LON boundaries
            with the type filter included
        """
        if not self._END is not None:
            raise AssertionError
            TS_NAME = ('#').join(str(x) for x in tile) + '#' + stringify(_types)
            if self._value_limits is None:
                df = self._logdf[self._columns].loc[self._logdf[self._EVENT].isin(_types)].sort_values(by=self._DATE).dropna()
            else:
                df = self._logdf[self._columns].loc[self._logdf[self._EVENT].between(self._value_limits[0], self._value_limits[1])].sort_values(by=self._DATE).dropna()
            if poly_tile:
                poly_lat = [ point[0] for point in tile ]
                poly_lon = [ point[1] for point in tile ]
                hull_pts = np.column_stack((poly_lat, poly_lon))
                pred_pt = np.column_stack((df[self._coord1], df[self._coord2]))
                hull = isinstance(hull_pts, Delaunay) or Delaunay(hull_pts)
            mask = hull.find_simplex(pred_pt) >= 0
            df = df[mask]
        else:
            lat_ = tile[0:2]
            lon_ = tile[2:4]
            df = df.loc[((df[self._coord1] > lat_[0]) & (df[self._coord1] <= lat_[1]) & (df[self._coord2] > lon_[0]) & (df[self._coord2] <= lon_[1]))]
        df.index = df[self._DATE]
        df = df[[self._EVENT]]
        if freq is None:
            ts = [ df.loc[self._trng[i]:self._trng[(i + 1)]].size for i in np.arange(self._trng.size - 1) ]
            out = pd.DataFrame(ts, columns=[TS_NAME], index=self._trng[:-1]).transpose()
        else:
            trng = pd.date_range(start=self._INIT, end=self._END, freq=freq)
            ts = [ df.loc[trng[i]:trng[(i + 1)]].size for i in np.arange(trng.size - 1)
                 ]
            out = pd.DataFrame(ts, columns=[TS_NAME], index=trng[:-1]).transpose()
        return out

    def get_rand_tile(self, tiles=None, LAT=None, LON=None, EPS=None, _types=None, poly_tile=False):
        """
        Utilities for spatio temporal analysis
        @author zed.uchicago.edu

        Picks random tile from options fed into timeseries method which maps to a
        non-empty subset within the larger dataset

        Inputs -
            LAT (float or list of floats): singular coordinate float or list of
                                           coordinate start floats
            LON (float or list of floats): singular coordinate float or list of
                                           coordinate start floats
            EPS (float): coordinate increment ESP
            _types (list): event type filter; accepted event type list
            tiles (list of lists): list of tiles to build where tile can be
            a (list of floats i.e. [lat1 lat2 lon1 lon2]) or tuples (i.e. [(x1,y1),(x2,y2)])
            defining polygons
            poly_tile (boolean): whether input for tile specifies a polygon

        Outputs -
            tile dataframe (pd.DataFrame)
        """
        if self._value_limits is None:
            df = self._logdf[self._columns].loc[self._logdf[self._EVENT].isin(_types)].sort_values(by=self._DATE).dropna()
        else:
            df = self._logdf[self._columns].loc[self._logdf[self._EVENT].between(self._value_limits[0], self._value_limits[1])].sort_values(by=self._DATE).dropna()
        TS_NAME = None
        stop = False
        if tiles is not None:
            while not stop:
                tile = random.choice(tiles)
                TS_NAME = ('#').join(str(x) for x in tile) + '#' + stringify(_types)
                if not poly_tile:
                    lat_ = tile[0:2]
                    lon_ = tile[2:4]
                    test = df.loc[((df[self._coord1] > lat_[0]) & (df[self._coord1] <= lat_[1]) & (df[self._coord2] > lon_[0]) & (df[self._coord2] <= lon_[1]))]
                    if test.shape[0] > 0:
                        stop = True
                else:
                    poly_lat = [ point[0] for point in tile ]
                    poly_lon = [ point[1] for point in tile ]
                    hull_pts = np.column_stack((poly_lat, poly_lon))
                    pred_pt = np.column_stack((df[self._coord1], df[self._coord2]))
                    if not isinstance(hull_pts, Delaunay):
                        hull = Delaunay(hull_pts)
                    mask = hull.find_simplex(pred_pt) >= 0
                    if df[mask].shape[0] > 0:
                        stop = True

        else:
            for i in LAT:
                if stop:
                    break
                for j in LON:
                    tile = [
                     i, i + EPS, j, j + EPS]
                    TS_NAME = ('#').join(str(x) for x in tile) + '#' + stringify(_types)
                    lat_ = tile[0:2]
                    lon_ = tile[2:4]
                    test = df.loc[((df[self._coord1] > lat_[0]) & (df[self._coord1] <= lat_[1]) & (df[self._coord2] > lon_[0]) & (df[self._coord2] <= lon_[1]))]
                    if test.shape[0] > 0:
                        stop = True
                        break

        df.index = df[self._DATE]
        df = df[[self._EVENT]]
        return (
         df, TS_NAME)

    def get_opt_freq(self, df, TS_NAME, incr=6, max_incr=24):
        """
        Utilities for spatio temporal analysis
        @author zed.uchicago.edu

        Returns the optimal frequency for timeseries based on highest non-zero
        to zero timeseries event count

        Input -
            df (pd.DataFrame): filtered subset of dataset corresponding to
            random tile from get_rand_tile
            incr (int): frequency increment
            max_incr (int): user-specified maximum increment
            TS_NAME

        Output -
            (string) to pass to pd.date_range(freq=) argument
        """
        ratios = []
        for i in range(max_incr / incr):
            curr_incr = (i + 1) * incr
            curr_freq = str(curr_incr) + 'H'
            curr_trng = pd.date_range(start=self._INIT, end=self._END, freq=curr_freq)
            ts = [ df.loc[curr_trng[i]:curr_trng[(i + 1)]].size for i in np.arange(curr_trng.size - 1)
                 ]
            out = pd.DataFrame(ts, columns=[TS_NAME], index=curr_trng[:-1]).transpose()
            tot = curr_trng.size + 0.0
            non_zero_ratio = out.astype(bool).sum(axis=1) / tot
            ratios.append((curr_freq, non_zero_ratio[0]))

        ratios.sort(key=operator.itemgetter(1))
        return ratios[(-1)][0]

    def timeseries(self, LAT=None, LON=None, EPS=None, _types=None, CSVfile='TS.csv', THRESHOLD=None, tiles=None, auto_adjust_time=False, incr=6, max_incr=24, poly_tile=False):
        """
        Utilities for spatio temporal analysis
        @author zed.uchicago.edu

        Creates DataFrame of location tiles and their
        respective timeseries from
        input datasource with significance threshold THRESHOLD
        latitude, longitude coordinate boundaries given by LAT, LON and EPS
        or the custom boundaries given by tiles
        calls on getTS for individual tile then concats them together

        Input:
            LAT (float or list of floats): singular coordinate float or list of
                                           coordinate start floats
            LON (float or list of floats): singular coordinate float or list of
                                           coordinate start floats
            EPS (float): coordinate increment ESP
            _types (list): event type filter; accepted event type list
            CSVfile (string): path to output file
            tiles (list of lists): list of tiles to build where tile can be
            a (list of floats i.e. [lat1 lat2 lon1 lon2]) or tuples (i.e. [(x1,y1),(x2,y2)])
            defining polygons
            auto_adjust_time (boolean): if True, within increments specified (6H default),
                determine optimal temporal frequency for timeseries data
            incr (int): frequency increment
            max_incr (int): user-specified maximum increment
            poly_tile (boolean): whether or tiles define polygons

        Output:
            No Output grid pd.Dataframe written out as CSV file to path specified
        """
        if THRESHOLD is None:
            if self._THRESHOLD is None:
                THRESHOLD = 0.1
            else:
                THRESHOLD = self._THRESHOLD
        if self._trng is None:
            self._trng = pd.date_range(start=self._INIT, end=self._END, freq=self._FREQ)
        assert LAT is not None and LON is not None and EPS is not None or tiles is not None, 'Error: (LAT, LON, EPS) or tiles not defined.'
        if tiles is not None:
            if auto_adjust_time:
                rand_tile_df, ts_name = self.get_rand_tile(tiles=tiles, _types=_types, poly_tile=poly_tile)
                opt_freq = self.get_opt_freq(df=rand_tile_df, incr=incr, max_incr=max_incr, TS_NAME=ts_name)
                _TS = pd.concat([ self.getTS(tile=coord_set, _types=_types, freq=opt_freq, poly_tile=poly_tile) for coord_set in tqdm(tiles)
                                ])
            else:
                _TS = pd.concat([ self.getTS(tile=coord_set, _types=_types, poly_tile=poly_tile) for coord_set in tqdm(tiles)
                                ])
        elif auto_adjust_time:
            rand_tile_df, ts_name = self.get_rand_tile(LAT=LAT, LON=LON, EPS=EPS, _types=_types)
            opt_freq = self.get_opt_freq(df=rand_tile_df, incr=incr, max_incr=max_incr, TS_NAME=ts_name)
            _TS = pd.concat([ self.getTS(tile=[i, i + EPS, j, j + EPS], freq=opt_freq, _types=_types) for i in tqdm(LAT) for j in tqdm(LON)
                            ])
        else:
            _TS = pd.concat([ self.getTS(tile=[i, i + EPS, j, j + EPS], _types=_types) for i in tqdm(LAT) for j in tqdm(LON)
                            ])
        LEN = pd.date_range(start=self._INIT, end=self._END, freq=self._FREQ).size + 0.0
        statbool = _TS.astype(bool).sum(axis=1) / LEN
        _TS = _TS.loc[(statbool > THRESHOLD)]
        self._ts_dict[repr(_types)] = _TS
        self._TS = _TS
        if CSVfile is not None:
            _TS.to_csv(CSVfile, sep=' ')
        return

    def fit(self, grid=None, INIT=None, END=None, THRESHOLD=None, csvPREF='TS', auto_adjust_time=False, incr=6, max_incr=24, poly_tile=False):
        """
        Utilities for spatio temporal analysis
        @author zed.uchicago.edu

        Fit dataproc with specified grid parameters and
        create timeseries for
        date boundaries specified by INIT, THRESHOLD,
        and END or by the input list of custom coordinate boundaries
        which do NOT have to match the arguments first input to the dataproc

        Inputs:
            grid (dictionary or list of lists): coordinate dictionary with
                respective ranges and EPS value OR custom list of lists
                of custom grid tiles as [coord1_start, coord1_stop,
                coord2_start, coord2_stop]
            INIT (datetime.date): starting timeseries date
            END (datetime.date): ending timeseries date
            THRESHOLD (float): significance threshold
            auto_adjust_time (boolean): if True, within increments specified (6H default),
                determine optimal temporal frequency for timeseries data
            incr (int): frequency increment
            max_incr (int): user-specified maximum increment
            poly_tile (boolean): whether or not tiles define polygons

        Outputs:
            (No output) grid pd.Dataframe written out as CSV file
                    to path specified
        """
        if INIT is not None:
            self._INIT = INIT
        if END is not None:
            self._END = END
        if grid is not None:
            if isinstance(grid, dict):
                assert self._coord1 in grid
                assert self._coord2 in grid
                assert 'Eps' in grid
                self._grid[self._coord1] = grid[self._coord1]
                self._grid[self._coord2] = grid[self._coord2]
                self._grid['Eps'] = grid['Eps']
                self._grid_type = 'auto'
            elif isinstance(grid, list):
                self._grid = grid
                self._grid_type = 'custom'
            else:
                raise TypeError('Unsupported grid type.')
        assert self._END is not None
        if self._types is not None:
            for key in self._types:
                if self._grid_type == 'auto':
                    self.timeseries(LAT=self._grid[self._coord1], LON=self._grid[self._coord2], EPS=self._grid['Eps'], _types=key, CSVfile=csvPREF + stringify(key) + '.csv', THRESHOLD=THRESHOLD, auto_adjust_time=auto_adjust_time, incr=incr, max_incr=max_incr, poly_tile=poly_tile)
                else:
                    self.timeseries(tiles=self._grid, _types=key, CSVfile=csvPREF + stringify(key) + '.csv', THRESHOLD=THRESHOLD, auto_adjust_time=auto_adjust_time, incr=incr, max_incr=max_incr, poly_tile=poly_tile)

            return
        assert self._value_limits is not None, 'Error: Neither value_limits nor _types has been defined.'
        if self._grid_type == 'auto':
            self.timeseries(LAT=self._grid[self._coord1], LON=self._grid[self._coord2], EPS=self._grid['Eps'], _types=None, CSVfile=csvPREF + '.csv', THRESHOLD=THRESHOLD, auto_adjust_time=auto_adjust_time, incr=incr, max_incr=max_incr, poly_tile=poly_tile)
        else:
            self.timeseries(tiles=self._grid, _types=None, CSVfile=csvPREF + '.csv', THRESHOLD=THRESHOLD, auto_adjust_time=auto_adjust_time, incr=incr, max_incr=max_incr, poly_tile=poly_tile)
        return
        return

    def getGrid(self):
        """
        Returns the tile coordinates of the working as a list of lists

        Input -
            (No inputs)
        Output -
            TILE (list of lists): the grid tiles
        """
        cols = self._TS.index.values
        f = lambda x: x[:-1] if len(x) % 2 == 1 else x
        TILE = None
        for word in cols:
            tile = [ float(i) for i in f(word.replace('#', ' ').split()) ]
            if TILE is None:
                TILE = [
                 tile]
            else:
                TILE.append(tile)

        return TILE

    def pull(self, domain='data.cityofchicago.org', dataset_id='crimes', token=None, store=True, out_fname='pull_df.p', pull_all=False):
        """
        Utilities for spatio temporal analysis
        @author zed.uchicago.edu

        Pulls new entries from datasource
        NOTE: should make flexible but for now use city of Chicago data

        Input -
            domain (string): Socrata database domain hosting data
            dataset_id (string): dataset ID to pull
            token (string): Socrata token for increased pull capacity;
                Note: Requires Socrata account
            store (boolean): whether or not to write out new dataset
            pull_all (boolean): pull complete dataset
            instead of just updating

        Output -
            None (writes out files if store is True and modifies inplace)
        """
        client = Socrata(domain, token)
        if domain == 'data.cityofchicago.org' and dataset_id == 'crimes':
            self._coord1 = 'latitude'
            self._coord2 = 'longitude'
            self._EVENT = 'primary_type'
        if pull_all:
            new_data = client.get(dataset_id)
            pull_df = pd.DataFrame(new_data).dropna(subset=[
             self._coord1, self._coord2, self._DATE, self._EVENT], axis=1).sort_values(self._DATE)
            self._logdf = pull_df
        else:
            self._logdf.sort_values(self._DATE)
            pull_after_date = "'" + str(self._logdf[self._DATE].iloc[(-1)]).replace(' ', 'T') + "'"
            new_data = client.get(dataset_id, where='date > ' + pull_after_date)
            if domain == 'data.cityofchicago.org' and dataset_id == 'crimes':
                self._DATE = 'date'
            pull_df = pd.DataFrame(new_data).dropna(subset=[
             self._coord1, self._coord2, self._DATE, self._EVENT], axis=1).sort_values(self._DATE)
            self._logdf.append(pull_df)
        if store:
            assert out_fname is not None, 'Out filename not specified'
            self._logdf.to_pickle(out_fname)
        return


def stringify(List):
    """
    Utility function
    @author zed.uchicago.edu

    Converts list into string separated by dashes
             or empty string if input list
             is not list or is empty

    Input:
        List (list): input list to be converted

    Output:
        (string)
    """
    if List is None:
        return 'VAR'
    else:
        if not List:
            return ''
        whole_string = ('-').join(str(elem) for elem in List)
        return whole_string.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')


def readTS(TSfile, csvNAME='TS1', BEG=None, END=None):
    """
    Utilities for spatio temporal analysis
    @author zed.uchicago.edu

    Reads in output TS logfile into pd.DF
        and then outputs necessary
        CSV files in XgenESeSS-friendly format

    Input -
        TSfile (string or list of strings): filename of input TS to read
            or list of filenames to read in and concatenate into one TS
        csvNAME (string)
        BEG (string): start datetime
        END (string): end datetime

    Output -
        dfts (pandas.DataFrame)
    """
    dfts = None
    if isinstance(TSfile, list):
        for tsfile in TSfile:
            if dfts is None:
                dfts = pd.read_csv(tsfile, sep=' ', index_col=0)
            else:
                dfts = dfts.append(pd.read_csv(tsfile, sep=' ', index_col=0))

    else:
        dfts = pd.read_csv(TSfile, sep=' ', index_col=0)
    dfts.columns = pd.to_datetime(dfts.columns)
    cols = dfts.columns[np.logical_and(dfts.columns >= pd.to_datetime(BEG), dfts.columns <= pd.to_datetime(END))]
    dfts = dfts[cols]
    indices = []
    for index, row in dfts.iterrows():
        if len(row.unique()) != 1:
            indices.append(index)

    dfts = dfts.loc[indices]
    dfts.to_csv(csvNAME + '.csv', sep=' ', header=None, index=None)
    np.savetxt(csvNAME + '.columns', cols, delimiter=',', fmt='%s')
    np.savetxt(csvNAME + '.coords', dfts.index.values, delimiter=',', fmt='%s')
    return dfts


def splitTS(TSfile, dirname='./', prefix='@', BEG=None, END=None, VARNAME=''):
    """
    Utilities for spatio temporal analysis
    @author zed.uchicago.edu

    Writes out each row of the pd.DataFrame as a separate CSVfile
    For XgenESeSS binary

    Inputs -
        TSfile (pd.DataFrame): DataFrame to write out
        csvNAME (string): output filename
        dirname (string): directory for output file
        prefix (string): prefix for files
        BEG (datetime): start date
        END (datetime): end date
        VARNAME (string): specifer variable for row

    Outputs -
        (No output)
    """
    dfts = None
    if isinstance(TSfile, list):
        for tsfile in TSfile:
            if dfts is None:
                dfts = pd.read_csv(tsfile, sep=' ', index_col=0)
            else:
                dfts = dfts.append(pd.read_csv(tsfile, sep=' ', index_col=0))

    else:
        dfts = pd.read_csv(TSfile, sep=' ', index_col=0)
    dfts.columns = pd.to_datetime(dfts.columns)
    cols = dfts.columns[np.logical_and(dfts.columns >= pd.to_datetime(BEG), dfts.columns <= pd.to_datetime(END))]
    dfts = dfts[cols]
    for row in dfts.index:
        dfts.loc[[row]].to_csv(dirname + '/' + prefix + row + VARNAME, header=None, index=None, sep=' ')

    return


class uNetworkModels():
    """
    Utilities for storing and manipulating XPFSA models
    inferred by XGenESeSS
    @author zed.uchicago.edu

    Attributes:
        jsonFile (string): path to json file containing models
    """

    def __init__(self, jsonFILE):
        with open(jsonFILE) as (data_file):
            self._models = json.load(data_file)

    @property
    def models(self):
        return self._models

    @property
    def df(self):
        return self._df

    def append(self, pydict):
        """
        append models
        @author zed.uchicago.edu
        """
        self._models.update(pydict)

    def select(self, var='gamma', n=None, reverse=False, store=None, high=None, low=None, equal=None, inplace=False):
        """
        Utilities for storing and manipulating XPFSA models
        inferred by XGenESeSS
        @author zed.uchicago.edu

        Selects the N top models as ranked by var specified value
        (in reverse order if reverse is True)

        Inputs -
            var (string): model parameter to rank by
            n (int): number of models to return
            reverse (boolean): return in ascending order (True)
                or descending (False) order
            store (string): name of file to store selection json
            high (float): higher cutoff
            low (float): lower cutoff
            inplace (bool): update models if true

        Output -
            (dictionary): top n models as ranked by var
                         in ascending/descending order
        """
        if equal is not None:
            out = {key:value for key, value in self._models.iteritems() if value[var] == equal}
        else:
            this_dict = {value[var]:key for key, value in self._models.iteritems()}
            if low is not None:
                this_dict = {key:this_dict[key] for key in this_dict.keys() if key >= low}
            if high is not None:
                this_dict = {key:this_dict[key] for key in this_dict.keys() if key <= high}
            if n is None:
                n = len(this_dict)
            if n > len(this_dict):
                n = len(this_dict)
            out = {this_dict[k]:self._models[this_dict[k]] for k in sorted(this_dict.keys(), reverse=reverse)[0:n]}
        if dict:
            if inplace:
                self._models = out
            if store is not None:
                with open(store, 'w') as (outfile):
                    json.dump(out, outfile)
        else:
            warnings.warn('Selection creates empty model dict')
        return out

    def setVarname(self):
        """
        Utilities for storing and manipulating XPFSA models
        inferred by XGenESeSS
        @author zed.uchicago.edu

        Extracts the varname for src and tgt of
        each model and stores under src_var and tgt_var
        keys of each model;

        No I/O
        """
        VARNAME = 'var'
        f = lambda x: x[(-1)] if len(x) % 2 == 1 else VARNAME
        for key, value in self._models.iteritems():
            self._models[key]['src_var'] = f(value['src'].replace('#', ' ').split())
            self._models[key]['tgt_var'] = f(value['tgt'].replace('#', ' ').split())

    def augmentDistance(self):
        """
        Utilities for storing and manipulating XPFSA models
        inferred by XGenESeSS
        @author zed.uchicago.edu

        Calculates the distance between all models and stores
        them under the
        distance key of each model;

        No I/O
        """
        f = lambda x: x[:-1] if len(x) % 2 == 1 else x
        for key, value in self._models.iteritems():
            src = [ float(i) for i in f(value['src'].replace('#', ' ').split()) ]
            tgt = [ float(i) for i in f(value['tgt'].replace('#', ' ').split()) ]
            dist = haversine((np.mean(src[0:2]), np.mean(src[2:])), (
             np.mean(tgt[0:2]), np.mean(tgt[2:])), miles=True)
            self._models[key]['distance'] = dist

    def to_json(self, outFile):
        """
        Utilities for storing and manipulating XPFSA models
        inferred by XGenESeSS
        @author zed.uchicago.edu

        Writes out updated models json to file
        Input -
            outFile (string): name of outfile to write json to

        Output -
            No output
        """
        with open(outFile, 'w') as (outfile):
            json.dump(self._models, outfile)

    def setDataFrame(self, scatter=None):
        """
        Generate dataframe representation of models
        @author zed.uchicago.edu

        Input -
            scatter (string) : prefix of filename to plot 3X3 regression
            matrix between delay, distance and coefficiecient of causality

        Output -
            Pandas.DataFrame with columns
            ['latsrc','lonsrc','lattgt',
             'lontgtt','gamma','delay','distance']
        """
        latsrc = []
        lonsrc = []
        lattgt = []
        lontgt = []
        gamma = []
        delay = []
        distance = []
        src_var = []
        tgt_var = []
        NUM = None
        f = lambda x: x[:-1] if len(x) % 2 == 1 else x
        for key, value in self._models.iteritems():
            src = [ float(i) for i in f(value['src'].replace('#', ' ').split()) ]
            tgt = [ float(i) for i in f(value['tgt'].replace('#', ' ').split()) ]
            if NUM is None:
                NUM = len(src) / 2
            latsrc.append(np.mean(src[0:NUM]))
            lonsrc.append(np.mean(src[NUM:]))
            lattgt.append(np.mean(tgt[0:NUM]))
            lontgt.append(np.mean(tgt[NUM:]))
            gamma.append(value['gamma'])
            delay.append(value['delay'])
            distance.append(value['distance'])
            src_var.append(value['src_var'])
            tgt_var.append(value['tgt_var'])

        self._df = pd.DataFrame({'latsrc': latsrc, 'lonsrc': lonsrc, 
           'lattgt': lattgt, 
           'lontgt': lontgt, 
           'gamma': gamma, 
           'delay': delay, 
           'distance': distance, 
           'src': src_var, 
           'tgt': tgt_var})
        if scatter is not None:
            sns.set_style('darkgrid')
            fig = plt.figure(figsize=(12, 12))
            fig.subplots_adjust(hspace=0.25)
            fig.subplots_adjust(wspace=0.25)
            ax = plt.subplot2grid((3, 3), (0, 0), colspan=1, rowspan=1)
            sns.distplot(self._df.gamma, ax=ax, kde=True, color='#9b59b6')
            ax = plt.subplot2grid((3, 3), (0, 1), colspan=1, rowspan=1)
            sns.regplot(ax=ax, x='gamma', y='distance', data=self._df)
            ax = plt.subplot2grid((3, 3), (0, 2), colspan=1, rowspan=1)
            sns.regplot(ax=ax, x='gamma', y='delay', data=self._df)
            ax = plt.subplot2grid((3, 3), (1, 0), colspan=1, rowspan=1)
            sns.regplot(ax=ax, x='distance', y='gamma', data=self._df)
            ax = plt.subplot2grid((3, 3), (1, 1), colspan=1, rowspan=1)
            sns.distplot(self._df.distance, ax=ax, kde=True, color='#9b59b6')
            ax = plt.subplot2grid((3, 3), (1, 2), colspan=1, rowspan=1)
            sns.regplot(ax=ax, x='distance', y='delay', data=self._df)
            ax = plt.subplot2grid((3, 3), (2, 0), colspan=1, rowspan=1)
            sns.regplot(ax=ax, x='delay', y='gamma', data=self._df)
            ax = plt.subplot2grid((3, 3), (2, 1), colspan=1, rowspan=1)
            sns.regplot(ax=ax, x='delay', y='distance', data=self._df)
            ax = plt.subplot2grid((3, 3), (2, 2), colspan=1, rowspan=1)
            sns.distplot(self._df.delay, ax=ax, kde=True, color='#9b59b6')
            plt.savefig(scatter + '.pdf', dpi=300, bbox_inches='tight', transparent=False)
        return self._df

    def iNet(self, init=0):
        """
        Utilities for storing and manipulating XPFSA models
        inferred by XGenESeSS
        @author zed.uchicago.edu

        Calculates the distance between all models and stores
        them under the
        distance key of each model;

        No I/O
        """
        pass


def to_json(pydict, outFile):
    """
        Writes dictionary json to file
        @author zed.uchicago.edu

        Input -
            pydict (dict): ditionary to store
            outFile (string): name of outfile to write json to

        Output -
            No output
    """
    with open(outFile, 'w') as (outfile):
        json.dump(pydict, outfile)


class simulateModel():
    """
    Use the subprocess library to call cynet on a model to process
    it and then run flexroc on it to obtain statistics: auc, tpr, fuc.
    Input -
        MODEL_PATH(string)- The path to the model being processed.
        DATA_PATH(string)- Path to the split file.
        RUNLEN(integer)- Length of the run.
        READLEN(integer)- Length of split data to read from begining
        CYNET_PATH - path to cynet binary.
        FLEXROC_PATH - path to flexroc binary.    
    """

    def __init__(self, MODEL_PATH, DATA_PATH, RUNLEN, CYNET_PATH, FLEXROC_PATH, READLEN=None):
        assert os.path.exists(CYNET_PATH), 'cynet binary cannot be found.'
        assert os.path.exists(FLEXROC_PATH), 'roc binary cannot be found.'
        assert os.path.exists(MODEL_PATH), 'model file cannot be found.'
        assert any(glob.iglob(DATA_PATH + '*')), 'split data files cannot be found.'
        self.MODEL_PATH = MODEL_PATH
        self.DATA_PATH = DATA_PATH
        self.RUNLEN = RUNLEN
        self.CYNET_PATH = CYNET_PATH
        self.FLEXROC_PATH = FLEXROC_PATH
        self.RUNLEN = RUNLEN
        if READLEN is None:
            self.READLEN = RUNLEN
        else:
            self.READLEN = READLEN
        return

    def run(self, LOG_PATH=None, PARTITION=0.5, DATA_TYPE='continuous', FLEXWIDTH=1, FLEX_TAIL_LEN=100, POSITIVE_CLASS_COLUMN=5, EVENTCOL=3, tpr_thrshold=0.85, fpr_threshold=0.15):
        """
        This function is intended to replace the cynrun.sh shell script. This
        function will use the subprocess library to call cynet on a model to process
        it and then run flexroc on it to obtain statistics: auc, tpr, fuc.
        Input -
           LOG_PATH (string)- Logfile from cynet run
           PARTITION (string)- Partition to use on split data
           FLEXWIDTH (int)-  Parameter to specify flex in flwxroc
           FLEX_TAIL_LEN (int)- tail length of input file to consider [0: all]
           POSITIVE_CLASS_COLUMN (int)- positive class column
           EVENTCOL (int)- event column
           tpr_thershold (float)- minimum tpr threshold
           fpr_threshold (float)- maximum fpr threshold
        
        Output -
            auc (float)- Area under the curve
            tpr (float)- True positive rate at specified maximum false positive rate
            fpr (float)- False positive rate at specified minimum true positive rate

        """
        if LOG_PATH is None:
            LOG_PATH = self.MODEL_PATH + '-XX.log'
        cystr = self.CYNET_PATH + ' -J ' + self.MODEL_PATH + ' -T ' + DATA_TYPE + ' -p ' + str(PARTITION) + ' -N ' + str(self.RUNLEN) + ' -x ' + str(self.READLEN) + ' -l ' + LOG_PATH + ' -w ' + self.DATA_PATH
        subprocess.check_call(cystr, shell=True)
        flexroc_str = self.FLEXROC_PATH + ' -i ' + LOG_PATH + ' -w ' + str(FLEXWIDTH) + ' -x ' + str(FLEX_TAIL_LEN) + ' -C ' + str(POSITIVE_CLASS_COLUMN) + ' -E ' + str(EVENTCOL) + ' -t ' + str(tpr_thrshold) + ' -f ' + str(fpr_threshold)
        output_str = subprocess.check_output(flexroc_str, shell=True)
        results = np.array(output_str.split())
        auc = float(results[1])
        tpr = float(results[7])
        fpr = float(results[13])
        return (
         auc, tpr, fpr)