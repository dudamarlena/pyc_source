# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/tools/dates.py
# Compiled at: 2016-03-23 12:35:00
import numpy as np, datetime, matplotlib.pyplot as plt

def cnes_convert(argin, julian=True, calendar=False, matlab=False, epoch=None, fromReference=None, verbose=False):
    try:
        isVector = len(argin) >= 1
    except TypeError:
        isVector = False

    if isVector and type(argin[0]) == str and np.size(argin) != len(argin):
        isVector = False
    if not isVector:
        argin = [argin]
    if isinstance(argin, np.ma.masked_array):
        maskin = argin.mask
    elif type(argin[0]) == str:
        maskin = np.zeros(np.shape(argin), dtype=bool)
    else:
        maskin = ~np.isfinite(argin)
    if isinstance(argin, np.ma.masked_array):
        argin = argin.tolist(0)
    elif isinstance(argin, np.ndarray):
        argin = argin.tolist()
    elif isinstance(argin, list):
        pass
    else:
        raise Exception('Undefined type')
    if type(argin[0]) == str:
        julian = True
    else:
        calendar = True
    if calendar is True:
        julian = False
    if julian is True:
        calendar = False
    if epoch is None:
        epoch = datetime.datetime(1950, 1, 1)
    if matlab is True:
        epoch = datetime.datetime(1, 1, 1)
    if julian is True:
        if verbose is True:
            print 'julian is true'
        narg = np.size(argin)
        strlist = [ x.split('-') for x in argin ]
        datelist = []
        for x in strlist:
            if len(x) == 1:
                datelist.append(datetime.datetime.strptime(x[0].strip(), '%d/%m/%Y'))
            else:
                datelist.append(datetime.datetime.strptime(('{0}-{1}').format(x[0].strip(), x[1].strip()), '%d/%m/%Y-%H:%M'))

        argout = np.array([ (datelist[x] - epoch).days for x in np.arange(narg) ], dtype=float)
        argout[maskin] = (isinstance(argout, np.ma.masked_array) or np).NaN if 1 else np.ma.array(argout.fill_value, mask=True)
        return (
         argout, datelist)
    else:
        if calendar is True:
            if verbose is True:
                print 'caldendar is true'
            datelist = [ epoch.toordinal() + x for x in argin ]
            if verbose is True:
                print datelist
            a = datetime.datetime.fromordinal(int(datelist[0]))
            dateObjList = np.array([ datetime.datetime.fromordinal(int(y)) + datetime.timedelta(seconds=(y - np.floor(y)) * 86400.0) for y in datelist ])
            dateStr = np.array([ Obj.strftime('%d/%m/%Y') for Obj in dateObjList ])
            dateStr[maskin] = None if not isinstance(dateStr, np.ma.masked_array) else np.ma.array(dateStr.fill_value, mask=True)
            dateObjList[maskin] = None if not isinstance(dateStr, np.ma.masked_array) else np.ma.array(dateStr.fill_value, mask=True)
            return (
             dateStr.tolist(), dateObjList.tolist())
        return


def date2seas(date, seas=[
 'DJF', 'MAM', 'JJA', 'SON'], shift=1):
    """
    #===============================================================================
    # ;+
    # ;
    # ; CDO_date2seas : provides the equivalent CDO season to a julian date array
    # ;
    # ; @param date {in}{required}{type=NUMERIC} julian date (CNES days)
    # ; @keyword seas {in}{optional}{type=STRING} seasons vector !! CAUTION !! This <br />
    # ;   must be accompanied by the SHIFT variable
    # ; @keyword shift {in}{optional}{type=NUMERIC} Backward in time offset of the 
    # ;   first element of SEAS vector in number of months from January <br />
    # ;   (e.g. Decembre -> 1, Novembre -> 2, etc... )
    # ; 
    # ;
    # ;-
    #===============================================================================
    """
    corr_months = np.roll(np.arange(12).reshape((4, 3)) + 1, shift)
    nt = len(date)
    outvec = cnes_convert(date)[1]
    month = np.array([ d.month for d in outvec ])
    outseas_ind = -np.ones(nt)
    for i, m in enumerate(month):
        outseas_ind[i] = int(np.where(m == corr_months)[0])

    outseas = [ seas[int(i)] for i in outseas_ind ]
    return (
     outseas, outseas_ind)


def cnes2modis(cnes_date, YYYYDDDHHMM=None, YYYYDDD=True):
    """
    #+
    # CNES2MODIS : Convert CNES julian days to MODIS data format (YYYYDDD)
    # 
    # @author: Renaud DUSSURGET (LEGOS/CTOH)
    # @history: Created by RD on 2/12/2011
    #           Adapted to Python on 29/10/2012 by RD (now at LER PAC/IFREMER)
    #
    #-
    """
    if YYYYDDDHHMM is None:
        YYYYDDDHHMM = False
    if YYYYDDD:
        YYYYDDDHHMM = False
    if YYYYDDDHHMM:
        YYYYDDD = False
    str, obj = cnes_convert(cnes_date)
    dat = [ o.strftime('%Y%j%H%M') for o in obj ]
    return dat


def modis2cnes(modis_date):
    """
    #+
    # MODIS2CNES : Convert MODIS date format to CNES JULIAN DAYS (YYYYDDD or YYYYDDDHHMM)
    # 
    # @author: Renaud DUSSURGET (LER PAC/IFREMER)
    # @history: Created by RD on 29/10/2012
    #
    #-
    """
    if not isinstance(modis_date, list):
        modis_date = [modis_date]
    if len(modis_date[0]) == 7:
        obj = [ datetime.datetime.strptime(d, '%Y%j') for d in modis_date ]
    else:
        obj = [ datetime.datetime.strptime(d, '%Y%j%H%M') for d in modis_date ]
    dat = [ o.strftime('%d/%m/%Y-%H:%M') for o in obj ]
    return cnes_convert(dat)