# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/data/rs_data.py
# Compiled at: 2016-03-23 12:35:00
import os, glob, datetime, numpy as np
from pyhdf.SD import SD, SDC
from altimetry.tools import in_limits, interp1d, interp2d2d, cnes_convert, modis2cnes, nearest

def modis_sst(file_name, limit=None, flagLevel=None, param='sst'):
    flagTable = np.zeros(32, dtype=bool)
    if flagLevel == 0:
        flagTable[[1]] = True
    elif flagLevel == 1:
        flagTable[[1, 3, 5, 15, 16, 19, 25, 26]] = True
    elif flagLevel == 2:
        flagTable[[0, 1, 3, 4, 5, 8, 9, 10, 14, 15, 16, 19, 21, 22, 23, 25, 26]] = True
    elif flagLevel >= 3:
        flagTable[[0, 1, 3, 4, 5, 8, 9, 10, 14, 15, 16, 19, 21, 22, 23, 25, 26]] = True
    flags = np.where(flagTable)[0]
    f = SD(file_name, SDC.READ)
    fattr = f.attributes()
    nScans = fattr['Number of Scan Lines']
    sCtl = fattr['Number of Scan Control Points']
    pCtl = fattr['Number of Pixel Control Points']
    nPix = fattr['Pixels per Scan Line']
    lonsel = f.select('longitude')
    latsel = f.select('latitude')
    info_sst = f.datasets()[param]
    dnames = info_sst[0]
    d = info_sst[1]
    lonvec = lonsel.get().reshape(d[0] * d[1])
    latvec = latsel.get().reshape(d[0] * d[1])
    if limit is not None:
        indvec, flagvec = in_limits(lonvec, latvec, limit)
    flagmat = flagvec.reshape(d[0], d[1])
    rowsum = np.sum(flagmat, 0)
    colsum = np.sum(flagmat, 1)
    yflag = rowsum >= 1
    xflag = colsum >= 1
    xid = np.arange(d[0])
    xid = xid.compress(xflag)
    xcnt = np.int(xid.size)
    yid = np.arange(d[1])
    yid = yid.compress(yflag)
    ycnt = np.int(yid.size)
    if xcnt == 0:
        raise Exception('Error : no longitude within limits')
    if ycnt == 0:
        raise Exception('Error : no latitude within limits')
    xst = np.int(xid.min())
    yst = np.int(yid.min())
    lon_var = lonsel.get(start=[xst, yst], count=[xcnt, ycnt])
    lat_var = latsel.get(start=[xst, yst], count=[xcnt, ycnt])
    sst = f.select(param)
    attr = sst.attributes()
    slope = attr['slope']
    intercept = attr['intercept']
    flagValue = attr['bad_value_scaled']
    sst_var = sst.get(start=[xst, yst], count=[xcnt, ycnt])
    if param == 'sst' or param == 'sst4':
        fg = f.select('qual_' + param)
        fg_var = fg.get(start=[xst, yst], count=[xcnt, ycnt])
        if flagLevel is None:
            mask = sst_var == flagValue
        else:
            mask = (sst_var == flagValue) | (fg_var >= flagLevel)
    elif param == 'chlor_a':
        fg = f.select('l2_flags')
        fg_var = fg.get(start=[xst, yst], count=[xcnt, ycnt]).flatten()
        dumfg = [ [ np.int(b) for b in np.binary_repr(f, 32)[::-1] ] for f in fg_var ]
        dumvar = np.sum(np.array(dumfg)[:, flags], 1) >= 1
        mask = np.reshape(dumvar, (xcnt, ycnt))
    sst_var = np.ma.masked_array(sst_var * slope + intercept, mask=mask, type=float)
    return {'lon': lon_var, 'lat': lat_var, 'sst': sst_var}


def modis_oc(file_name, limit=None, flagLevel=None, param='sst'):
    f = SD(file_name, SDC.READ)
    fattr = f.attributes()
    lon = f.select('longitude')
    lat = f.select('latitude')
    info_sst = f.datasets()[param]
    dnames = info_sst[0]
    d = info_sst[1]
    lonvec = lon.get().reshape(d[0] * d[1])
    latvec = lat.get().reshape(d[0] * d[1])
    if limit is not None:
        indvec, flagvec = in_limits(lonvec, latvec, limit)
    flagmat = flagvec.reshape(d[0], d[1])
    rowsum = np.sum(flagmat, 0)
    colsum = np.sum(flagmat, 1)
    yflag = rowsum >= 1
    xflag = colsum >= 1
    xid = np.arange(d[0])
    xid = xid.compress(xflag)
    xcnt = int(xid.size)
    xst = int(xid.min())
    yid = np.arange(d[1])
    yid = yid.compress(yflag)
    ycnt = int(yid.size)
    yst = int(yid.min())
    lon_var = lon.get(start=[xst, yst], count=[xcnt, ycnt])
    lat_var = lat.get(start=[xst, yst], count=[xcnt, ycnt])
    sst = f.select(param)
    attr = sst.attributes()
    slope = attr['slope']
    intercept = attr['intercept']
    flagValue = attr['bad_value_scaled']
    sst_var = sst.get(start=[xst, yst], count=[xcnt, ycnt])
    fg = f.select('qual_' + param)
    fg_var = fg.get(start=[xst, yst], count=[xcnt, ycnt])
    if flagLevel is None:
        mask = sst_var == flagValue
    else:
        mask = (sst_var == flagValue) | (fg_var >= flagLevel)
    sst_var = np.ma.masked_array(sst_var * slope + intercept, mask=mask, type=float)
    return


def modis_date_convert(argin, julian=True, calendar=False, matlab=False, epoch=None, verbose=False):
    if np.size(argin) == 1:
        if type(argin) is not list:
            argin = [argin]
    forward = type(argin[0]) is str
    if calendar is True:
        julian = False
    if julian is True:
        calendar = False
    if epoch is None:
        epoch = datetime.date(1950, 1, 1)
    if forward:
        if len(argin[0]) == 7:
            strptime_fmt = '%Y%j'
        if len(argin[0]) == 11:
            strptime_fmt = '%Y%j%H%M'
        if len(argin[0]) == 13:
            strptime_fmt = '%Y%j%H%M%S'
        moddate = [ datetime.datetime.strptime(x, strptime_fmt) for x in argin ]
        if julian is True:
            return [ x.toordinal() + datetime.timedelta(seconds=x.second, minutes=x.minute, hours=x.hour).seconds / 86400.0 - epoch.toordinal() + 1 for x in moddate
                   ]
        if calendar is True:
            return [ x.strftime('%d/%m/%Y') for x in moddate ]
    else:
        _, dateObj = cnes_convert(argin)
        if type(argin[0]) is float:
            strftime_fmt = '%Y%j%H%M%S'
        else:
            strftime_fmt = '%Y%j'
        return [ O.strftime(strftime_fmt) for O in dateObj ]
    return


def modis_date_from_filename(argin, julian=True, calendar=False, matlab=False, epoch=None):
    if np.size(argin) == 1:
        if type(argin) is not list:
            argin = [argin]
    if calendar is True:
        julian = False
    if julian is True:
        calendar = False
    if epoch is None:
        epoch = datetime.date(1950, 1, 1)
    return modis_date_convert([ x[1:12] for x in argin ], julian=julian, calendar=calendar)


def modis_filename2cnes(modis_fname):
    modis_date = modis_filename2modisdate(modis_fname)
    return modis2cnes(modis_date)


def modis_filename2modisdate(modis_fname):
    """
    #+
    # MODIS_FILENAME2DATE : Convert MODIS file name to MODIS date
    # 
    # @author: Renaud DUSSURGET (LER PAC/IFREMER)
    # @history: Created by RD on 29/10/2012
    #
    #-
    """
    if not isinstance(modis_fname, list):
        modis_fname = [modis_fname]
    return [ os.path.splitext(os.path.basename(m))[0][1:12] for m in modis_fname ]


class image_data:

    def __init__(self, file_pattern, limit=None, current=0, param='sst'):
        if limit is None:
            self.limit = [-90, -180, 90, 180]
        else:
            self.limit = limit
        self.param = param
        ls = glob.glob(file_pattern)
        dirname = [ os.path.dirname(p) for p in ls ]
        filename = [ os.path.basename(i) for i in ls ]
        self.datelist = np.array(modis_date_from_filename(filename, julian=True))
        self.filelist = [ dirname[i] + '/' + filename[i] for i in range(len(filename)) ]
        self.current = current
        self.sst_dev = 1.5
        self.cache_size = 9
        sort_order = np.argsort(self.datelist)
        self.datelist = self.datelist[sort_order]
        filelist = [ self.filelist[i] for i in sort_order ]
        self.filelist = filelist
        self.cache_index = np.ma.masked_array(np.zeros(self.cache_size), mask=np.repeat(True, self.cache_size))
        self.cached = self.cache_index.compressed().size
        self.cached_lon = []
        self.cached_lat = []
        self.cached_sst = []
        return

    def show_image(self, pmap, logscale=False, vmin=None, vmax=None, colorbar=True, title=None, cbar_label=None, cmap=None):
        mnsst = self.sst.mean()
        var_sst = np.std(self.sst)
        if vmin is None:
            vmin = mnsst - self.sst_dev * var_sst
            if np.abs(vmin - mnsst) >= 2:
                vmin = mnsst - 2
        if vmax is None:
            vmax = mnsst + self.sst_dev * var_sst
            if np.abs(vmax - mnsst) >= 2:
                vmax = mnsst + 2
        if title is None:
            title = ''
        title += ('\nSST chosen->{0:%Y/%m/%d}\nshown->{1:%Y/%m/%d - %H:%M} (offset : {2:d} days)\nfile->{3}').format(self.chosen_date, self.datetime, -self.offset.days, os.path.basename(self.filename))
        pmap.pcolormesh(self.lon, self.lat, self.sst, vmin=vmin, vmax=vmax, cmap=cmap)
        if colorbar is True:
            pmap.colorbar(label=cbar_label)
        pmap.title(title)
        return

    def set_current(self, date, **kwargs):
        try:
            if len(date) > 0:
                date = date[0]
        except TypeError:
            date = date

        self.current = nearest(self.datelist, date)
        self.offset = -datetime.timedelta(days=self.datelist[self.current] - date)
        self.filename = self.filelist[self.current]
        self.date = self.datelist[self.current]
        days = divmod(self.date, 1)
        self.datetime = datetime.datetime.fromordinal(int(days[0])) + datetime.timedelta(datetime.datetime(1950, 1, 1).toordinal() + days[1] - 1)
        hours = divmod(datetime.timedelta(days=divmod(self.date, 1)[1]).seconds, 3600)
        minutes = divmod(hours[1], 60)
        self.hours = hours[0]
        self.minutes = minutes[0]
        self.chosen_date = self.datetime + self.offset
        self.chosen_date_modis = modis_date_convert(date)[0]
        self.chosen_date_cal = cnes_convert(date)[0][0]
        self.load(**kwargs)

    def load(self, **kwargs):
        cache_id = np.arange(self.cache_size)
        if self.cache_index.compress(self.cache_index == self.current).size == 1:
            cache_id = cache_id.compress(self.cache_index == self.current)
        else:
            if self.cached == self.cache_size:
                print 'clearing oldest cache element'
                self.cached_lon.pop(0)
                self.cached_lat.pop(0)
                self.cached_sst.pop(0)
                cached = self.cache_index[1:]
                toappend = np.ma.array(0, mask=True)
                self.cache_index = np.append(cached, toappend)
                self.cache_index.mask = np.append(cached.mask, toappend.mask)
                self.cached = self.cache_index.compressed().size
            print 'Loading ' + os.path.basename(self.filename) + ' - modis'
            modis = modis_sst(self.filename, limit=self.limit, param=self.param, **kwargs)
            self.cached_lon += [modis['lon'][:]]
            self.cached_lat += [modis['lat'][:]]
            self.cached_sst += [modis['sst'][:]]
            self.cache_index.mask[self.cached] = False
            self.cache_index[self.cached] = self.current
            self.cached = self.cache_index.compressed().size
            cache_id = cache_id.compress((self.cache_index == self.current).compressed())
        self.lon = self.cached_lon[cache_id]
        self.lat = self.cached_lat[cache_id]
        self.sst = self.cached_sst[cache_id]
        self.date = self.datelist[cache_id]
        print ('Cache size : {0} (shape : {2}) - loading {1}').format(self.cached, cache_id, np.shape(self.cached_lon))