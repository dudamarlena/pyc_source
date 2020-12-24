# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/data/alti_data.py
# Compiled at: 2016-03-23 12:35:00
import numpy as np
from netCDF4 import Dataset as ncfile
import operator, glob, os, hydro as htools
from altimetry.externals import esutils_stat as es
from altimetry.tools import cnes_convert, histogram_indices, recale, in_limits, cumulative_distance, nctools
from collections import OrderedDict
from altimetry.tools.nctools import varStr
import matplotlib.pyplot as plt

class alti_data(htools.hydro_data):
    """
    An :class:`altimetry.data.hydro_data` object dedicated to handling along-track altimetry data.
    
    :example: To load different sets of data, try these :
    
      * Concatenate a set of **AVISO's MFSTEP NRT along-track data** and plot a 2D hovmoller matrix:
      
      .. code-block:: python
         
         #Define parameters 
         trange_str = ['24/09/2012','05/09/2013']
         trange,tdatetime=AT.cnes_convert(trange_str) #convert time range
         alti_pattern = '/path/to/nrt/mfstep/nrt_mfstep_j2_sla_vfec_*.nc'
         
         #Load data
         alti=alti_data(alti_pattern,verbose=verbose,datatype='DT',time_range=trange,slaext=True) #Load data
         
         #2D reordering of the data
         alti.reorder()
         
         #Plot results
         pcolormesh(data.lat,data.cycle,data.sla); show() #plot the hovmoller
    
      * Loads a set of **PISTACH L3 5Hz** files and create a new SLA variable and slice the object using a given time range :
      .. code-block:: python
      
         #Load data
         alti_pattern = '/path/to/data/PISTACH_L3_Product_NWMED_MLE4_tr*_5hz.nc'
         alti=alti_data(alti_pattern,limit=limit,verbose=verbose)
          
         alti.create_Variable('sla',                             #new variable name
                              alti.ssh_mss_filtree_21pts,        #data
                              {'time':alti._dimensions['time']}, #set dimensions
                              extend=False)                      #extend option
         
         #get daily updates of the object
         for date in xrange(21300,21320):
            
             #get a deep copy of the object, not to erase the whole dataset
             subset=alti.copy(deep=True)
                
             #update the object with the proper slice
             fg=subset.slice('date', [date,date+1])
             subset.update(fg)
             
             do_something(subset)
    
      * Loads a set of **PISTACH hydro** files :
      
      .. code-block:: python
       
         data=AD.alti_data('%s/*_2PTP*_*.nc' % RepData,verbose=opts.verbose,datatype='RAW',remove_existing=False)
      
      * Load any **NetCDF file** using :class:`altimetry.tools.nctools.nc` :
    
      .. code-block:: python
       
         data=AD.alti_data(fout,verbose=opts.verbose,datatype='RAW',transpose=False)
         
       
       
    """

    def __init__(self, file_pattern, time_range=None, output_is_dict=True, **kwargs):
        """
        returns a dataset from a single file or multiple concatenated files. cf. :class:`altimetry.data.hydro_data` for further informations
        
        :keyword time_range: get start dates from file names (cf. notes on file names when using this option)
        :keyword kwargs: additionnal keywords to be passed to :meth:`altimetry.data.hydro_data.__init__`
        
        .. note:: Naming convetion should respect AVISO formatting 
        
           * start dates should be the 3rd field from the end
           * satellite name should be the 3rd from the start 
           * eg. my_file_sat_20010101_20010108_20010109.nc
           
        """
        self.datatype = None
        self.sat = []
        if time_range is not None:
            ls = np.array(glob.glob(file_pattern))
            if len(ls) == 0:
                raise Exception(('File not found : {0}').format(file_pattern))
            filelist = [ os.path.basename(p) for p in ls ]
            st = [ f.split('_')[(-3)] for f in filelist ]
            jst = np.array([ cnes_convert(('{0}/{1}/{2}').format(s[-2:], s[-4:-2], s[0:4]))[0][0] for s in st ])
            order = np.argsort(jst)
            jst = jst[order]
            ls = ls[order]
            dft = jst[1:] - jst[:-1]
            dt = np.fix(np.median(dft[(dft != 0)]))
            hist, R = es.histogram(jst, binsize=dt, use_weave=False, rev=True, min=time_range[0] - dt / 2.0, max=time_range[1] + dt / 2.0)
            dumind = histogram_indices(hist, R)
            ind = np.array([])
            for i in dumind:
                ind = np.append(ind, i)

            ind = ind.tolist()
            file_pattern = ls[ind]
        htools.hydro_data.__init__(self, file_pattern, output_is_dict=output_is_dict, **kwargs)
        self.set_sats()
        return

    def set_sats(self):
        """
        set satellite name using (cf. notes on file names in `altimetry.data.alti_data.__init__`)
        """
        if self.count == 0:
            return
        for enum in enumerate(self.filelist):
            if hasattr(self, 'id'):
                sat = self.id
            elif (self.datatype == 'DT') | (self.datatype == 'NRT') | (self.datatype == 'PISTACH'):
                sat = [enum[1].split('_')[2]]
            elif self.datatype == 'CTOH':
                sat = [enum[1].split('.')[(-4)]]
            else:
                sat = 'N/A'
            if len(sat) == 1:
                sat * self.filelist_count[enum[0]]
            self.sat = np.append(self.sat, sat)

        self.sat = np.ma.array(self.sat, mask=False)

    def read(self, filename, datatype=None, slaext=False, **kwargs):
        """
        reader method.
        
        :parameter filename: name of the file to load.
        :keyword datatype: choose between DT/NRT/PISTACH/CTOH or other formats to call the corresponding reader. If datatype is :
        
           * DT or NRT or PISTACH : calls :func:`altimetry.data.alti_data.read_sla` or :func:`altimetry.data.alti_data.read_slaext`
           * CTOH : calls :func:`altimetry.data.alti_data.read_CTOH`
           * else : calls :func:`altimetry.data.alti_data.read_nc`, based on :class:`altimetry.tools.nctools.nc` object.
        
        :keyword slaext: force using :func:`altimetry.data.alti_data.read_slaext`
        
        .. note:: This method is call from :meth:`altimetry.data.hydro_data.__init__` and returns a data structure to be handled by :meth:`altimetry.data.hydro_data.update_dataset`
        
        """
        fname, extension = os.path.splitext(filename)
        if os.path.basename(filename).count('.') > os.path.basename(filename).count('_'):
            delim = '.'
        else:
            delim = '_'
        if datatype is None:
            if os.path.basename(filename).split(delim)[0] == 'ctoh':
                datatype = 'CTOH'
            if os.path.basename(filename).split(delim)[0] == 'PISTACH':
                datatype = 'PISTACH'
            if os.path.basename(filename).split(delim)[0] == 'nrt':
                datatype = 'NRT'
            if os.path.basename(filename).split(delim)[0] == 'dt':
                datatype = 'DT'
        self.datatype = datatype
        if (datatype == 'DT') | (datatype == 'NRT') | (datatype == 'PISTACH'):
            if slaext:
                outStr = self.read_slaext(filename, datatype=datatype, **kwargs)
            else:
                outStr = self.read_sla(filename, datatype=datatype, **kwargs)
            if outStr.has_key('_dimensions'):
                self.update_fid_list(os.path.basename(filename), outStr['_dimensions']['time'])
        elif datatype == 'CTOH':
            outStr = self.read_CTOH(filename, **kwargs)
            if outStr.has_key('_dimensions'):
                self.update_fid_list(os.path.basename(filename), outStr['_dimensions']['time'])
        else:
            outStr = self.read_nc(filename, **kwargs)
            if outStr.has_key('_dimensions'):
                self.update_fid_list(os.path.basename(filename), outStr['_dimensions'][outStr['_dimensions'].keys()[1]])
        return outStr

    def read_sla(self, filename, params=None, force=False, timerange=None, datatype=None, **kwargs):
        """
        Read AVISO Along-Track products
        
        :return outStr: Output data structure containing all recorded parameters as specificied by NetCDF file PARAMETER list.
        :author: Renaud Dussurget
        """
        from time import time
        from datetime import timedelta
        self.message(2, ('Reading AVISO DT data ({0})').format(datatype))
        self._filename = filename
        try:
            self._ncfile = ncfile(self._filename, 'r')
        except Exception as e:
            self.warning(1, repr(e))
            return {}

        if os.path.basename(filename).count('.') > os.path.basename(filename).count('_'):
            delim = '.'
        else:
            delim = '_'
        splitted = os.path.basename(filename).split(delim)
        if len(splitted) > 3:
            if (datatype == 'DT') | (datatype == 'NRT'):
                sat_name = splitted[2] if splitted[0] == 'nrt' else splitted[3]
            elif datatype == 'PISTACH':
                sat_name = 'J2'
            else:
                sat_name = 'J2'
        else:
            sat_name = 'N/A'
        par_list = [ i.encode() for i in self._ncfile.variables.keys() ]
        for i in ['BeginDates', 'Longitudes', 'Latitudes']:
            par_list.pop(par_list.index(i))

        nparam = len(par_list)
        self.message(2, 'Recorded parameters : ' + str(nparam) + ' -> ' + str(par_list))
        lon = self.load_ncVar('Longitudes', **kwargs)
        lon['data'] = recale(lon['data'], degrees=True, zero_2pi=True)
        lat = self.load_ncVar('Latitudes', **kwargs)
        ind, flag = in_limits(lon['data'], lat['data'], limit=self.limit)
        dim_lon = lon['_dimensions']
        lat = lat['data'].compress(flag)
        lon = lon['data'].compress(flag)
        sz = np.shape(lon)
        ndims = np.size(sz)
        stDate = self.load_ncVar('BeginDates', **kwargs)['data']
        dumVar = self.load_ncVar('Cycles', **kwargs)
        nbCyc = dumVar['data']
        Ncycs = dumVar['_dimensions']['Cycles']
        Ntra = dumVar['_dimensions']['Tracks']
        nbTra = self.load_ncVar('Tracks', **kwargs)['data']
        DeltaT = self._ncfile.variables['DeltaT'][:] / 86400.0
        npts = self.load_ncVar('NbPoints', **kwargs)['data']
        dumind = np.cumsum(npts)
        date = ()
        cycles = ()
        tracks = ()
        indcopy = ind.copy()
        npts[npts.mask] = 0
        dumind[dumind.mask] = 0
        nbTra_copy = nbTra.copy()
        toto = npts.copy()
        concat_npts = not nbCyc.shape[(-1)] > 1
        for i in np.arange(1, Ncycs, 1.0, dtype=int):
            nbTra = np.ma.concatenate((nbTra, nbTra_copy))
            if concat_npts:
                npts = np.ma.concatenate((npts, tuple(~nbCyc.T[i].mask * 1 * npts)))

        if concat_npts:
            npts = npts.reshape(nbCyc.shape[::-1]).T
        else:
            npts = nbCyc
        nbTra = nbTra.reshape(nbCyc.shape[::-1]).T
        nbTra.mask = nbCyc.mask
        npts = npts.flatten()
        nbTra = nbTra.flatten()
        nbCyc_flatten = nbCyc.flatten()
        nbTra_flatten = nbTra.flatten()
        stDate_flatten = stDate.flatten()
        outInd = []
        for i, nc in enumerate(nbCyc.data.flatten()):
            N = npts[i]
            Nprev = npts[(i - Ncycs)] if i >= Ncycs and np.remainder(float(i), Ncycs) == 0 else 0
            indcopy -= Nprev
            curInd = tuple(sorted(set(xrange(N) if N > 0 else []).intersection(indcopy)))
            ncur = len(curInd)
            outInd += map(operator.sub, curInd, ((curInd[0] if len(curInd) > 0 else 0) - (outInd[(-1)] + 1 if len(outInd) > 0 else 0) - len(ind) * np.remainder(float(i), Ncycs),) * ncur)
            curInd = tuple(map(operator.mul, curInd, (DeltaT,) * ncur))
            date += tuple(map(operator.add, curInd, (stDate_flatten[i],) * ncur))
            cycles += (nbCyc_flatten[i],) * ncur
            tracks += (nbTra_flatten[i],) * ncur

        date = np.ma.masked_array(date, mask=False)
        cycles = np.ma.masked_array(cycles, mask=False)
        tracks = np.ma.masked_array(tracks, mask=False)
        outInd = np.array(outInd, dtype=int)
        nt = len(date)
        date.mask = (False,) * nt
        cycles.mask = date.mask
        tracks.mask = date.mask
        dimStr = dim_lon
        dimStr.pop('Data')
        nrec = len(date)
        dimStr.update({'time': nrec})
        for i in ['DeltaT', 'NbPoints', 'Cycles', 'Tracks', 'DataIndexes']:
            par_list.pop(par_list.index(i))

        outStr = {'_dimensions': dimStr, 'lon': lon, 'lat': lat, 
           'date': date, 
           'cycle': cycles, 
           'track': tracks}
        for param in par_list:
            a = time()
            dumVar = self.load_ncVar(param, Data=ind, **kwargs)
            runtime = time() - a
            dimStr = dumVar['_dimensions']
            dimStr.pop('Cycles')
            dimStr.pop('Data')
            dimStr['time'] = nrec
            dimStr['_ndims'] = len(dimStr.keys()) - 1
            curDim = [ str(dimname) for dimname in dimStr.keys()[1:] ]
            curDimval = [ dimStr[dim] for dim in curDim ]
            flag = [ (np.array(dimname) == outStr['_dimensions'].keys()).sum() == 0 for dimname in curDim ]
            dimUpdate = np.array(curDim).compress(flag)
            for enum in enumerate(dimUpdate):
                self.message(3, ('Appending dimensions {0}:{1} to dataStructure').format(enum[1], np.array(curDimval).compress(flag)[enum[0]]))
                outStr['_dimensions'].update({enum[1]: np.array(curDimval).compress(flag)[enum[0]]})
                outStr['_dimensions']['_ndims'] += 1

            dumStr = {param.lower(): dumVar['data'].flatten()[outInd]}
            outStr.update(dumStr)

        id = np.repeat(sat_name, outStr['_dimensions']['time'])
        outStr.update({'id': id})
        self._ncfile.close()
        return outStr

    def read_slaext(self, filename, params=None, force=False, timerange=None, datatype=None, **kwargs):
        """
        Read AVISO Along-Track SLAEXT regional products
        
        :return outStr: Output data structure containing all recorded parameters as specificied by NetCDF file PARAMETER list.
        :author: Renaud Dussurget
        """
        self.message(2, ('Reading SLAext data ({0})').format(datatype))
        self.message(2, 'Loading %s' % filename)
        self._filename = filename
        try:
            self._ncfile = ncfile(self._filename, 'r')
        except Exception as e:
            self.warning(1, repr(e))
            return {}

        if os.path.basename(filename).count('.') > os.path.basename(filename).count('_'):
            delim = '.'
        else:
            delim = '_'
        splitted = os.path.basename(filename).split(delim)
        if (datatype == 'DT') | (datatype == 'NRT'):
            sat_name = splitted[2] if splitted[0] == 'nrt' else splitted[3]
        if datatype == 'PISTACH':
            sat_name = 'J2'
        par_list = [ i.encode() for i in self._ncfile.variables.keys() ]
        for i in ['time', 'longitude', 'latitude']:
            par_list.pop(par_list.index(i))

        nparam = len(par_list)
        self.message(2, 'Recorded parameters : ' + str(nparam) + ' -> ' + str(par_list))
        lon = self.load_ncVar('longitude', **kwargs)
        lon['data'] = recale(lon['data'], degrees=True, zero_2pi=True)
        lat = self.load_ncVar('latitude', **kwargs)
        ind, flag = in_limits(lon['data'], lat['data'], limit=self.limit)
        dim_lon = lon['_dimensions']
        lat = lat['data'].compress(flag)
        lon = lon['data'].compress(flag)
        dist = cumulative_distance(lat, lon)
        sz = np.shape(lon)
        ndims = np.size(sz)
        id = np.repeat(sat_name, sz)
        date = self.load_ncVar('time', time=ind, **kwargs)
        dimStr = date['_dimensions']
        date = date['data']
        outStr = varStr(dimensions=dimStr)
        outStr.update({'lon': lon})
        outStr.update({'lat': lat})
        outStr.update({'date': date})
        outStr.update({'id': id})
        for param in par_list:
            dumVar = self.load_ncVar(param, time=ind, **kwargs)
            dimStr = dumVar['_dimensions']
            curDim = [ str(dimname) for dimname in dimStr.keys()[1:] ]
            curDimval = [ dimStr[dim] for dim in curDim ]
            flag = [ (np.array(dimname) == outStr['_dimensions'].keys()).sum() == 0 for dimname in curDim ]
            dimUpdate = np.array(curDim).compress(flag)
            for enum in enumerate(dimUpdate):
                self.message(3, ('Appending dimensions {0}:{1} to dataStructure').format(enum[1], np.array(curDimval).compress(flag)[enum[0]]))
                outStr['_dimensions'].update({enum[1]: np.array(curDimval).compress(flag)[enum[0]]})
                if not isinstance(outStr['_dimensions'], dimStr):
                    outStr['_dimensions']['_ndims'] += 1

            cmd = "dumStr = {'" + param.lower() + "':dumVar['data']}"
            self.message(4, 'exec : ' + cmd)
            exec cmd
            outStr.update(dumStr)

        self._ncfile.close()
        return outStr

    def read_CTOH(self, filename, params=None, force=False, timerange=None, datatype=None, **kwargs):
        """
        Read AVISO Along-Track SLA regional products
        
        :return outStr: Output data structure containing all recorded parameters as specificied by NetCDF file PARAMETER list.
        :author: Renaud Dussurget
        """
        self._filename = filename
        try:
            self._ncfile = ncfile(self._filename, 'r')
        except Exception as e:
            self.warning(1, repr(e))
            return {}

        delim = '.'
        splitted = os.path.basename(filename).split(delim)
        sat_name = splitted[3]
        track = np.ma.masked_array(int(splitted[(-2)]))
        ntracks = 1
        par_list = [ i.encode() for i in self._ncfile.variables.keys() ]
        for i in ['cycle', 'lon', 'lat']:
            par_list.pop(par_list.index(i))

        nparam = len(par_list)
        self.message(2, 'Recorded parameters : ' + str(nparam) + ' -> ' + str(par_list))
        lon = self.load_ncVar('lon', **kwargs)
        lon['data'] = recale(lon['data'], degrees=True, zero_2pi=True)
        lat = self.load_ncVar('lat', **kwargs)
        ind, flag = in_limits(lon['data'], lat['data'], limit=self.limit)
        latout = lat.pop('data').compress(flag)
        lonout = lon.pop('data').compress(flag)
        nlon = len(lonout)
        cycle = self.load_ncVar('cycle', time=ind, **kwargs)
        cycleout = cycle.pop('data')
        ncycles = len(cycleout)
        N = ncycles * nlon
        mask = np.repeat(lonout.mask, ncycles) & np.repeat(latout.mask, ncycles) & np.repeat(cycleout.mask, nlon)
        ind = np.repeat(ind, ncycles)
        lon = {'_dimensions': {'_ndims': 1, 'time': N}, '_attributes': lon['_attributes'], 
           'data': np.ma.masked_array(np.repeat(lonout.data, ncycles), mask=mask), 
           'long_name': 'longitude'}
        lat = {'_dimensions': {'_ndims': 1, 'time': N}, '_attributes': lat['_attributes'], 
           'data': np.ma.masked_array(np.repeat(latout.data, ncycles), mask=mask), 
           'long_name': 'latitude'}
        cycle = {'_dimensions': {'_ndims': 1, 'time': N}, '_attributes': cycle['_attributes'], 
           'data': np.ma.masked_array(np.repeat(cycleout.data, nlon).reshape((ncycles, nlon)).T.flatten(), mask=mask), 
           'long_name': 'cycle_number'}
        track = {'_dimensions': {'_ndims': 1, 'time': N}, 'data': np.ma.masked_array(np.repeat(track, N), mask=mask), 
           'long_name': 'track_number'}
        outStr = {'_dimensions': {'_ndims': 1, 'time': N}, 'lon': lon, 
           'lat': lat, 
           'track': track, 
           'cycle': cycle}
        for param in par_list:
            dumVar = self.load_ncVar(param, time=ind, **kwargs)
            dimStr = dumVar.pop('_dimensions')
            attrStr = dumVar.pop('_attributes')
            if dimStr['_ndims'] == 1:
                dumVar = {'data': np.ma.repeat(dumVar.pop('data'), N / dimStr[dimStr.keys()[dimStr['_ndims']]])}
            else:
                dumVar = {'data': dumVar.pop('data').flatten()}
            dumVar['_dimensions'] = outStr['_dimensions'].copy()
            dumVar['_attributes'] = attrStr
            cmd = "dumStr = {'" + param.lower() + "':dumVar}"
            self.message(4, 'exec : ' + cmd)
            exec cmd
            outStr.update(dumStr)

        self._ncfile.close()
        return outStr

    def read_nc(self, filename, **kwargs):
        """
        data reader based on :class:`altimetry.tools.nctools.nc` object.
        
        .. note:: THIS can be VERY powerful!
        """
        self._filename = filename
        remove_existing = kwargs.get('remove_existing', True)
        obj = nctools.nc(verbose=self.verbose, limit=self.limit, use_local_dims=True)
        outStr = obj.read(filename, **kwargs)
        for a in self.__dict__.keys():
            if outStr.has_key(a) and not a.startswith('_'):
                if remove_existing:
                    outStr.pop(a)
                    self.message(2, ('Attribute {0} already exists - removing it (set remove_existing to False instead)').format(a))

        return outStr

    def track_list(self, *args):
        """
        return the list of tracks contained if the dataset
        """
        noargs = len(args) == 0
        if noargs:
            return np.unique(self.track)
        return np.unique(self.track.compress(args[0]))

    def cycle_list(self, *args):
        """
        return the list of cycles contained if the dataset
        """
        noargs = len(args) == 0
        if noargs:
            return np.unique(self.cycle)
        return np.unique(self.cycle.compress(args[0]))

    def reorder(self, *args, **kwargs):
        """
        Reorders data vectors in 2D (ie. with dimensions (CYCLE,RECORD)). This is useful to get a hovmoller-type matrix of each variable.
        
        :example: To plot a hovmoller for a given variable, do ::
           
           .. code-block:: pyhton
              
              data=alti_data('/my/dir/my_files_pattern*.nc') #concatenate the files
              data.reorder() #reorder data
              pcolormesh(data.lat,data.cycle,data.sla); show() #plot the hovmoller
           
        .. note:: This only works for data reprojected along a nominal track.
        """
        trange_str = self.time_range()[0]
        cycle_list = self.cycle_list()
        track_list = self.track_list()
        precision = np.finfo(self.lon.dtype).precision - 2
        self.lon = self.lon.round(decimals=precision)
        self.lat = self.lat.round(decimals=precision)
        self.message(2, 'Detect recurrent lon/lat/track triplets')
        triplets = np.unique(zip(*(self.lon, self.lat, self.track)))
        triplets = np.ma.array(sorted(triplets, key=operator.itemgetter(2)))
        lon = triplets[:, 0]
        lat = triplets[:, 1]
        tracknb = triplets[:, 2]
        track = track_list
        cycle = cycle_list
        N = len(lon)
        ntracks = len(track_list)
        ncycles = len(cycle_list)
        ind = np.arange(N)
        self.message(2, 'Computing space and time indices')
        xid = np.array([ np.where((ln == lon) & (self.lat[i] == lat))[0][0] for i, ln in enumerate(self.lon) ])
        tid = np.array([ np.where(c == cycle_list)[0][0] for c in self.cycle ])
        varSize = np.array([ np.size(self.__dict__[k]) for k in self.__dict__.keys() ])
        par_list = np.array(self.__dict__.keys())[(varSize == self._dimensions['time'])].tolist()
        for par in ['lon', 'lat', 'track', 'cycle']:
            par_list.pop(par_list.index(par))
            self.__setattr__(par, locals()[par])

        self._dimensions = OrderedDict({'_ndims': 3, 'cycle': ncycles, 'record': N, 'track': ntracks})
        record = np.ma.array(ind, mask=np.zeros(N, dtype=bool))
        lon.mask = np.zeros(N, dtype=bool)
        lat.mask = np.zeros(N, dtype=bool)
        tracknb.mask = np.zeros(N, dtype=bool)
        track.mask = np.zeros(ntracks, dtype=bool)
        cycle.mask = np.zeros(ncycles, dtype=bool)
        lon.__setattr__('_dimensions', {'_ndims': 1, 'record': N})
        lon.__setattr__('long_name', 'longitude')
        lat.__setattr__('_dimensions', {'_ndims': 1, 'record': N})
        lat.__setattr__('long_name', 'latitude')
        tracknb.__setattr__('_dimensions', {'_ndims': 1, 'record': ntracks})
        track.__setattr__('long_name', 'track_number')
        track.__setattr__('_dimensions', {'_ndims': 1, 'track': ntracks})
        track.__setattr__('long_name', 'track_list')
        cycle.__setattr__('_dimensions', {'_ndims': 1, 'cycle': ncycles})
        cycle.__setattr__('long_name', 'cycle_number')
        record.__setattr__('_dimensions', {'_ndims': 1, 'record': N})
        record.__setattr__('long_name', 'record_index')
        self.lon = lon
        self.lat = lat
        self.tracknb = tracknb
        self.track = track
        self.cycle = cycle
        self.record = record
        for par in par_list:
            self.message(2, ('Reforming {0}').format(par))
            locals()[par] = np.ma.array(np.zeros((ncycles, N)), mask=np.ones((ncycles, N), dtype=bool), dtype=self.__getattribute__(par).dtype)
            locals()[par][(tid, xid)] = self.__getattribute__(par)
            locals()[par].__setattr__('_dimensions', {'_ndims': 2, 'cycle': ncycles, 'record': N})
            if hasattr(self.__dict__[par], '__dict__'):
                attrStr = OrderedDict()
                null = [ attrStr.update({a: self.__dict__[par].__dict__[a]}) for a in self.__dict__[par].__dict__.keys() if not locals()[par].__dict__.has_key(a) ]
                locals()[par].__dict__.update(attrStr)
            self.__setattr__(par, locals()[par])

        par_list = np.append(par_list, ['lon', 'lat', 'tracknb', 'track', 'cycle', 'record'])
        self.par_list = par_list

    def pass_time(self):
        """
        Compute the central time for each passes.
        
        .. note:: this must be called AFTER having called :meth:`altimetry.data.alti_data.reorder` as it looks for the CYCLE and RECORD dimensions.
        .. note:: The methodology to compute the central time is to interpolate the time along the track at missing points, and then reading the value at point N/2.
        """
        date = self.date
        nt = self._dimensions['cycle']
        N = self._dimensions['record']
        for t in np.arange(nt):
            poly = np.polyfit(np.arange(N)[(~date.mask[t, :])], date[t, :][(~date.mask[t, :])], 1)
            date[t, :][date.mask[t, :]] = poly[0] * np.arange(N)[date.mask[t, :]] + poly[1]

        date.mask = False
        return date[:, N / 2]