# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/Peaks.py
# Compiled at: 2020-02-19 13:12:25
# Size of source mod 2**32: 41330 bytes
"""set of function for Peak detections and display - 1D and 2D

Very First functionnal - Not finished !

Peak1D and Peak2D are simple objects
    with attributes like Id, label, intens(ity), pos(ition), or width
    the only added method is report() (returns a string)

Peak1DList and Peak2DList are python list, with a few added methods
    - report (to stdio or to a file)
    - largest sort in decreasing order of intensity
        other sorts can simply done by peaklist.sort(key = lambda p: p.XXX)
            where XXX is any peak attribute  (see largest code)

Example of usage:

# assuming d is a 2D NPKData / 1D will be just as simple
d.pp()          # computes a peak picking over the whole spectrum using 3 x standard_deviation(d)
                # This is just a detection of all local maxima

# We can be more specific:
d.pp(threshold=5E5, zoom=((700,1050),(300,350)) )     # zoom is always in the currently active unit, defined with d.unit

# this attached the peak list to the dataset as d.peaks,
# it is a list of Peaks2D objects, with some added properties
print( "number of detected peaks: %d" % len(d.peaks))

p0 = d.peaks[0]     # peaks have label, intensity and positions attributes

print( p0.report() )        # and a report method
                            # report has an additional format parameter which enables control on the output

# we can call centroid to improve the accuracy and move the position to center of a fitted (2D) parabola
d.centroid()     

# The peak list can be displayed on screen as simple crosses
d.display_peaks()

# The label can be modififed for specific purposes:
for p in d.peaks:
    if 150 < p.posF2 < 1500 :
        p.label = "%.2f x %.f"%(p.posF1,p.posF2)    # for instance changing to the coordinates for a certain zone
    else:
        p.label = ""                                # and removing elsewhere

d.display_peaks(peak_label=True)

# peak lists can also be reported
d.report_peak()

# but also as a formatted stream, and redirected to a file:
output = open("my_peak_list.csv","w")      # open the file
output.write("# LABEL, INTENSITY, F1, Width, F2, width")
d.report_peak(file=output, format="{1}, {4:.2f}, {2:.7f}, {5:.2f}, {3:.7f}, {6:.2f}")
        # arguments order order is   id, label, posF1, posF2, intensity, widthF1, widthF2
output.close()

Sept 2015 M-A Delsuc
"""
from __future__ import print_function
import numpy as np, unittest
from spike import NPKError
from spike.NPKData import NPKData_plugin, _NPKData, flatten, parsezoom
from spike.util.counter import timeit
from scipy.optimize import curve_fit
import warnings
debug = 0
NbMaxDisplayPeaks = 1000

def _identity(x):
    """the null function - used as default function argument"""
    return x


class Peak(object):
    __doc__ = ' a generic class to store peaks\n    defines :\n    Id          a unique integer\n    intens      The intensity (the height of the largest point)\n    area        The area/volume of the peak\n    label       a string \n    intens_err  The uncertainty of the previous values\n    area_err    ..\n    \n    '

    def __init__(self, Id, label, intens):
        self.Id = Id
        self.label = label
        self.intens = float(intens)
        self.area = 0.0
        self.intens_err = 0.0
        self.area_err = 0.0


class Peak1D(Peak):
    __doc__ = 'a class to store a single 1D peak\n    defines in addition to Peak\n    pos         position of the peak in index relative to the typed (real/complex) buffer\n    width       width of the peak in index\n    pos_err     uncertainty of the previous values\n    width_err   ...\n    '
    report_format = '{}, {}, {:.2f}, {:.2f}'
    full_format = '{}, {}, {}, {}, {}, {}, {}, {}, '

    def __init__(self, Id, label, intens, pos):
        super(Peak1D, self).__init__(Id, label, intens)
        self.pos = float(pos)
        self.pos_err = 0.0
        self.width = 0.0
        self.width_err = 0.0

    def report(self, f=_identity, format=None):
        """
        print the peak list
        f is a function used to transform the coordinate
        indentity function is default,
        for instance you can use something like
        peaks.report(f=s.axis1.itop)    to get ppm values on a NMR dataset
        order is "id, label, position, intensity"

        parameters are : 
        Id label positions intens width intens_err pos_err width_err 
        in that order.

        By default returns only the 4 first fields with 2 digits, but the format keyword can change that.
        format values:
        - None or "report", the standard value is used:  "{}, {}, {:.2f}, {:.2f}" 
                  (so only the four first parameters are shown)
        - "full" is all parrameters at full resolution  ( "{}; "*8 )
        - any othe string following the format syta will do.
            you can use any formating syntax. So for instance the following format
            "{1} :   {3:.2f}  F1: {2:.7f} +/- {4:.2f}"
            will remove the Id, show position with 7 digits after the comma, and will show width

        you can change the report and full default values by setting
        pk.__class__.report_format   and   pk.__class__.full_format  which class attributes
        """
        if format is None or format == 'report':
            format = self.report_format
        else:
            if format == 'full':
                format = self.full_format
        return format.format(self.Id, self.label, f(self.pos), self.intens, self.width, self.pos_err, self.intens_err, self.width_err)

    def _report(self, f=_identity):
        """
        full report for 1D Peaks
        list is : Id, label, pos intens, widthF1, width, pos_err, intens_err, width_err
        """
        return self.report(f=f, format=(self.full_format))


class Peak2D(Peak):
    __doc__ = 'a class to store a single 2D peak\n    defines in addition to Peak\n    posF1 posF2         positions in F1 and F2 of the peak in index relative to the typed (real/complex) axis\n    widthF1 ...F2       widthes of the peak in index\n    posF1_err ...       uncertainty of the previous values\n    widthF1_err   ...\n    '
    report_format = '{}, {}, {:.2f}, {:.2f}, {:.2f}'
    full_format = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '

    def __init__(self, Id, label, intens, posF1, posF2):
        super(Peak2D, self).__init__(Id, label, intens)
        self.posF1 = posF1
        self.posF2 = posF2
        self.widthF1 = 0.0
        self.widthF2 = 0.0
        self.posF1_err = 0.0
        self.posF2_err = 0.0
        self.widthF1_err = 0.0
        self.widthF2_err = 0.0

    def report(self, f1=_identity, f2=_identity, format=None):
        """
        print the peak list
        f1, f2 are two functions used to transform respectively the coordinates in F1 and F2
        indentity function is default,
        for instance you can use something like
        peaks.report(f1=s.axis1.itop, f2=s.axis2.itop)    to get ppm values on a NMR dataset
        order is "id, label, posF1, posF2, intensity, widthF1, widthF2"

        printed parameters are : 
        Id label posF1 posF2 intens widthF1 widthF2 posF1_err posF2_err intens_err widthF1_err widthF2_err 

        By default returns only the 5 first fields with 2 digits, but the format keyword can change that.
        format values:
        - None or "report", the standard value is used:  "{}, {}, {:.2f}, {:.2f}, {:.2f}" 
                  (so only the four first parameters are shown)
        - "full" is all parrameters at full resolution  ( "{}; "*12 )
        - any othe string following the format syntxa will do.
            you can use any formating syntax. So for instance the following format
            "{1} :   {4:.2f}  F1: {2:.7f} +/- {5:.2f}  X  F2: {3:.7f} +/- {6:.2f}"
            will remove the Id, show position with 7 digits after the comma, and will show widthes    
        """
        if format is None or format == 'report':
            format = self.report_format
        else:
            if format == 'full':
                format = self.full_format
        return format.format(self.Id, self.label, f1(self.posF1), f2(self.posF2), self.intens, self.widthF1, self.widthF2, self.posF1_err, self.posF2_err, self.intens_err, self.widthF1_err, self.widthF2_err)

    def _report(self, f1=_identity, f2=_identity):
        """
        full report for 2D Peaks
        list is : Id, label, posF1, posF2, intens, widthF1, widthF2, posF1_err, posF2_err, intens_err, widthF1_err, widthF2_err
        """
        return self.report(f1=f1, f2=f2, format=(self.full_format))


class PeakList(list):
    __doc__ = '\n    the class generic to all peak lists\n    '

    def __init__(self, *arg, **kwds):
        (super(PeakList, self).__init__)(*arg)
        if 'threshold' in kwds:
            self.threshold = kwds['threshold']
            del kwds['threshold']
        else:
            self.threshold = None
        if 'source' in kwds:
            self.source = kwds['source']
            del kwds['source']
        else:
            self.source = None
        if kwds:
            keys = kwds.keys()
            keys.sort()
            extras = ', '.join(['%s=%s' % (k, kwds[k]) for k in keys])
            raise ValueError('unrecognized keyword args: %s' % extras)

    @property
    def intens(self):
        """returns a numpy array of the intensities"""
        return np.array([pk.intens for pk in self])

    @property
    def label(self):
        """returns an array of the labels"""
        return [pk.label for pk in self]

    def len(self):
        return len(self)

    def largest(self):
        """sort the peaklist in decresing order of intensities"""
        self.sort(reverse=True, key=(lambda p: p.intens))


def peak_aggreg(pklist, distance):
    """
    aggregates peaks in peaklist if peaks are closer than a given distance in pixel
    distance : if two peaks are less than distance (in points),  they are aggregated
    """
    pkl = sorted(pklist, key=(lambda p: p.pos))
    newlist = Peak1DList()
    prev = pkl[0]
    ipk = 1
    maxgrp = (prev.intens, 0)
    newgrp = [0]
    if ipk < len(pkl):
        current = pkl[ipk]
        if abs(current.pos - prev.pos) <= distance:
            newgrp.append(ipk)
            if current.intens > maxgrp[0]:
                maxgrp = (
                 current.intens, ipk)
            else:
                if len(newgrp) == 1:
                    inewpk = newgrp[0]
                else:
                    inewpk = maxgrp[1]
                newlist.append(pkl[inewpk])
                newgrp = [ipk]
                maxgrp = (current.intens, ipk)
            ipk += 1
            prev = current
        elif len(newgrp) == 1:
            inewpk = newgrp[0]
    else:
        inewpk = maxgrp[1]
    newlist.append(pklist[inewpk])
    return newlist


class Peak1DList(PeakList):
    __doc__ = '\n    store a list of 1D peaks\n    contains the array version of the Peak1D object :\n    self.pos is the numpy array of the position of all the peaks\n    and self[k] is the kth Peak1D object of the list\n    '

    @property
    def pos(self):
        """returns a numpy array of the positions in index"""
        return np.array([pk.pos for pk in self])

    def report(self, f=_identity, file=None, format=None, NbMaxPeaks=NbMaxDisplayPeaks):
        """
        print the peak list
        f is a function used to transform respectively the coordinates
        indentity function is default,
        for instance you can use something like
        d.peaks.report(f=d.axis1.itop)    to get ppm values on a NMR dataset

        check documentation for Peak1D.report() for details on output format
        """
        if NbMaxPeaks < len(self):
            print(('# %d in Peak list - reporting the %d largest' % (len(self), NbMaxPeaks)), file=file)
            indices = list(np.argpartition(self.intens, len(self) - NbMaxPeaks)[-NbMaxPeaks:])
            for i, pk in enumerate(self):
                if i in indices:
                    print(pk.report(f=f, format=format), file=file)

        else:
            print(('# %d in Peak list' % len(self)), file=file)
            for pk in self:
                print(pk.report(f=f, format=format), file=file)

    def _report(self, f=_identity, file=None):
        """return full report for 1D peak list
        list is : Id, label, pos, intens, width,  pos_err, intens_err, width_err
        """
        lst = [pk._report(f=f) for pk in self]
        return '\n'.join(lst)

    def display(self, peak_label=False, peak_mode='marker', zoom=None, show=False, f=_identity, color='red', markersize=None, figure=None, scale=1.0, NbMaxPeaks=NbMaxDisplayPeaks):
        """
        displays 1D peaks
        zoom is in index
        peak_mode is either "marker" or "bar"
        NbMaxPeaks is the maximum number of peaks to displayin the zoom window (show only the largest)
        f() should be a function which converts from points to current display scale - typically npk.axis1.itoc
        """
        if len(self) == 0:
            return
        else:
            from spike.Display import testplot
            plot = testplot.plot()
            if figure is None:
                fig = plot.subplot(111)
            else:
                fig = figure
            if zoom:
                z0 = zoom[0]
                z1 = zoom[1]
                pkl = [i for i, p in enumerate(self) if p.pos >= z0 if p.pos <= z1]
            else:
                pkl = range(len(self))
            if peak_mode == 'marker':
                if len(self) > 0:
                    mmax = max(self.intens) / scale
                    pkl = list(filter(lambda i: self.intens[i] <= mmax, pkl))
            else:
                if len(pkl) > NbMaxPeaks:
                    pkl.sort(reverse=True, key=(lambda i: self[i].intens))
                    pkl = pkl[:NbMaxPeaks]
                if peak_mode == 'marker':
                    fig.plot((f(self.pos[pkl])), (self.intens[pkl]), 'x', color=color)
                else:
                    if peak_mode == 'bar':
                        for i in pkl:
                            p = self[i]
                            fig.plot([f(p.pos), f(p.pos)], [0, p.intens], '-', color=color)

                    else:
                        raise Exception('wrong peak_mode')
        if peak_label:
            for i in pkl:
                p = self[i]
                fig.annotate((p.label), (f(p.pos), p.intens), xycoords='data',
                  xytext=(0, 10),
                  textcoords='offset points',
                  rotation=40,
                  color='red',
                  fontsize=7,
                  arrowprops=dict(arrowstyle='-'),
                  horizontalalignment='left',
                  verticalalignment='bottom')

        if show:
            plot.show()

    def pos2label(self):
        """use pos in current unit, using converion f and set it as label for each peak"""
        f = self.source.axis1.itoc
        for pk in self:
            pk.label = '%.4f' % (f(pk.pos),)


class Peak2DList(PeakList):
    __doc__ = '\n    store a list of 2D peaks\n    contains the array version of the Peak2D object :\n    self.posF1 is the numpy array of the position of all the peaks\n    and self[k] is the kth Peak2D object of the list\n    '

    @property
    def posF1(self):
        """returns a numpy array of the F1 positions in index"""
        return np.array([pk.posF1 for pk in self])

    @property
    def posF2(self):
        """returns a numpy array of the F2 positions in index"""
        return np.array([pk.posF2 for pk in self])

    def report(self, f1=_identity, f2=_identity, file=None, format=None, NbMaxPeaks=NbMaxDisplayPeaks):
        """
        print the peak list
        f1, f2 are two functions used to transform respectively the coordinates in F1 and F2
        indentity function is default,
        for instance you can use something like
        d.peaks.export(f1=s.axis1.itop, f2=s.axis2.itop)    to get ppm values on a NMR dataset
        the file keyword allows to redirect the output to a file object 
        
        check documentation for Peak2D.report() for details on output format
        """
        if NbMaxPeaks < len(self):
            print(('# %d in Peak list - reporting the %d largest' % (len(self), NbMaxPeaks)), file=file)
            indices = list(np.argpartition(self.intens, len(self) - NbMaxPeaks)[-NbMaxPeaks:])
            for i, pk in enumerate(self):
                if i in indices:
                    print(pk.report(f1=f1, f2=f2, format=format), file=file)

        else:
            print(('# %d in Peak list' % len(self)), file=file)
            for pk in self:
                print(pk.report(f1=f1, f2=f2, format=format), file=file)

    def _report(self, f1=_identity, f2=_identity, file=None):
        """return full report for 2D peak list
        list is : Id, label, posF1, posF2, intens, widthF1, widthF2, posF1_err, posF2_err, intens_err, widthF1_err, widthF2_err
        """
        lst = [pk._report(f1=f1, f2=f2) for pk in self]
        return '\n'.join(lst)

    def display(self, axis=None, peak_label=False, zoom=None, show=False, f1=_identity, f2=_identity, color=None, markersize=6, figure=None, NbMaxPeaks=NbMaxDisplayPeaks):
        """
        displays 2D peak list
        zoom is in index
        f1 and f2 should be functions which convert from points to current display scale - typically npk.axis1.itoc npk.axis2.itoc
        """
        import spike.Display.testplot as testplot
        plot = testplot.plot()
        if figure is None:
            fig = plot.subplot(111)
        else:
            fig = figure
        if zoom is not None:
            z1lo, z1up, z2lo, z2up = flatten(zoom)
            pk = []
            for p in range(len(self)):
                plp = self[p]

            if plp.posF1 >= z1lo and plp.posF1 <= z1up and plp.posF2 >= z2lo and plp.posF2 <= z2up:
                pk.append(p)
        else:
            pk = range(len(self))
        if debug > 0:
            print('plotting %d peaks' % len(pk))
        elif axis is None:
            plF1 = self.posF1
            plF2 = self.posF2
            fig.plot((f2(plF2[pk])), (f1(plF1[pk])), 'x', color=color, markersize=markersize)
            if peak_label:
                for p in pk:
                    plp = self[p]
                    fig.text((1.01 * plp.posF2), (1.01 * plp.posF1), (plp.label), color=color, markersize=markersize)

        else:
            raise Exception('to be done')
        if show:
            fig.show()


def _peaks2d(npkd, threshold=0.1, zoom=None, value=False, zones=0):
    """
    Extract peaks from 2d Array dataset
    if value is True, return the magnitude at position (x,y)
    """
    if not zones == 0:
        _peaks2d(npkd, threshold=threshold, zoom=zoom, value=value)
    else:
        print('** assuming no zoom predefined **')
        for z in range(zones):
            print(z)


def peakpick(npkd, threshold=None, zoom=None, autothresh=3.0, verbose=True):
    """
    performs a peak picking of the current experiment
    threshold is the level above which peaks are picked
        None (default) means that autothresh*(noise level of dataset) will be used - using d.robust_stats() as proxy for noise-level
    zoom defines the region on which detection is made
        zoom is in currentunit (same syntax as in display)
        None means the whole data
    """
    if threshold is None:
        mu, sigma = npkd.robust_stats()
        threshold = autothresh * sigma
        if mu > 0:
            threshold += mu
    elif npkd.dim == 1:
        listpkF1, listint = peaks1d(npkd, threshold=threshold, zoom=zoom)
        pkl = Peak1DList((Peak1D(i, str(i), intens, pos) for i, pos, intens in zip(range(len(listint)), list(listpkF1), list(listint))),
          threshold=threshold,
          source=npkd)
        pkl.pos2label()
        npkd.peaks = pkl
    else:
        if npkd.dim == 2:
            listpkF1, listpkF2, listint = peaks2d(npkd, threshold=threshold, zoom=zoom)
            pkl = Peak2DList((Peak2D(i, str(i), intens, posF1, posF2) for i, posF1, posF2, intens in zip(range(len(listpkF1)), listpkF1, listpkF2, listint)),
              threshold=threshold,
              source=npkd)
            npkd.peaks = pkl
        else:
            raise NPKError(('Not implemented of %sD experiment' % npkd.dim), data=npkd)
    if threshold is None:
        if verbose:
            print('PP Threshold:', threshold)
    if verbose:
        print('PP: %d detected' % (len(npkd.peaks),))
    return npkd


def peaks2d(npkd, threshold, zoom):
    """
    math code for NPKData 2D peak picker
    """
    npkd.check2D()
    print('########## in peaks2d ')
    print('zoom ', zoom)
    z1lo, z1up, z2lo, z2up = parsezoom(npkd, zoom)
    print('z1lo, z1up, z2lo, z2up ', z1lo, z1up, z2lo, z2up)
    buff = npkd.get_buffer()[z1lo:z1up, z2lo:z2up]
    if npkd.itype != 0:
        buff = buff.real
    tbuff = buff[1:-1, 1:-1]
    listpk = np.where((tbuff > threshold * np.ones(tbuff.shape)) & (tbuff > buff[:-2, 1:-1]) & (tbuff > buff[2:, 1:-1]) & (tbuff > buff[1:-1, :-2]) & (tbuff > buff[1:-1, 2:]))
    listpkF1 = int(z1lo) + listpk[0] + 1
    listpkF2 = int(z2lo) + listpk[1] + 1
    listint = npkd.buffer[(listpkF1, listpkF2)]
    return (listpkF1, listpkF2, listint)


def peaks1d(npkd, threshold, zoom=None):
    """
    math code for NPKData 1D peak picker
    """
    npkd.check1D()
    z1, z2 = parsezoom(npkd, zoom)
    buff = npkd.get_buffer()[z1:z2]
    if npkd.itype == 1:
        buff = buff.real
    tbuff = buff[1:-1]
    listpk = np.where((tbuff > threshold * np.ones(tbuff.shape)) & (tbuff > buff[:-2]) & (tbuff > buff[2:]))
    listpkF1 = int(z1) + listpk[0] + 1
    listint = npkd.get_buffer()[listpkF1].real
    return (listpkF1, listint)


def center(x, xo, intens, width):
    """
    the centroid definition, used to fit the spectrum
    x can be a nparray
    FWMH is   sqrt(2) x width.
    """
    return intens * (1 - ((x - xo) / width) ** 2)


def center2d(yx, yo, xo, intens, widthy, widthx):
    """
    the 2D centroid, used to fit 2D spectra - si center()
    xy is [x0, y_0, x_1, y_1, ..., x_n-1, y_n-1] - is 2*n long for n points,
    returns [z_0, z_1, ... z_n-1]
    """
    y = yx[::2]
    x = yx[1::2]
    return intens * (1 - ((x - xo) / widthx) ** 2) * (1 - ((y - yo) / widthy) ** 2)


def centroid1d(npkd, npoints=3, reset_label=True):
    """
    from peak lists determined with peak()
    realize a centroid fit of the peak summit and width,
    will use npoints values around center  (npoints has to be odd)
    computes Full width at half maximum
    updates in data peak list
    reset_label when True (default) reset the labels of FTMS datasets
    TODO : update uncertainties
    """
    from scipy import polyfit
    npkd.check1D()
    noff = (int(npoints) - 1) / 2
    if 2 * noff + 1 != npoints or npoints < 3:
        raise NPKError('npoints must odd and >2 ', data=npkd)
    buff = npkd.get_buffer().real
    for pk in npkd.peaks:
        xdata = np.arange(int(round(pk.pos - noff)), int(round(pk.pos + noff + 1)))
        ydata = buff[xdata]
        try:
            popt, pcov = curve_fit(center, xdata, ydata, p0=[pk.pos, pk.intens, 1.0])
        except RuntimeError:
            print('peak %d (id %s) centroid could not be fitted' % (pk.Id, pk.label))
        else:
            pk.pos = popt[0]
            pk.intens = popt[1]
            pk.width = np.sqrt(2.0) * popt[2]
            errors = np.sqrt(np.diag(pcov))
            pk.pos_err = errors[0]
            pk.intens_err = errors[1]
            pk.width_err = np.sqrt(2.0) * errors[2]
    else:
        if reset_label:
            npkd.peaks.pos2label()


def centroid2d--- This code section failed: ---

 L. 623         0  LOAD_CONST               0
                2  LOAD_CONST               ('polyfit',)
                4  IMPORT_NAME              scipy
                6  IMPORT_FROM              polyfit
                8  STORE_FAST               'polyfit'
               10  POP_TOP          

 L. 624        12  LOAD_FAST                'npkd'
               14  LOAD_METHOD              check2D
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 625        20  LOAD_FAST                'npoints_F1'
               22  STORE_FAST               'nF1'

 L. 626        24  LOAD_FAST                'npoints_F2'
               26  STORE_FAST               'nF2'

 L. 627        28  LOAD_GLOBAL              int
               30  LOAD_FAST                'nF1'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               1
               36  BINARY_SUBTRACT  
               38  LOAD_CONST               2
               40  BINARY_TRUE_DIVIDE
               42  STORE_FAST               'noff1'

 L. 628        44  LOAD_GLOBAL              int
               46  LOAD_FAST                'nF2'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               1
               52  BINARY_SUBTRACT  
               54  LOAD_CONST               2
               56  BINARY_TRUE_DIVIDE
               58  STORE_FAST               'noff2'

 L. 629        60  LOAD_CONST               2
               62  LOAD_FAST                'noff1'
               64  BINARY_MULTIPLY  
               66  LOAD_CONST               1
               68  BINARY_ADD       
               70  LOAD_FAST                'nF1'
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_TRUE    108  'to 108'
               76  LOAD_FAST                'nF1'
               78  LOAD_CONST               3
               80  COMPARE_OP               <
               82  POP_JUMP_IF_TRUE    108  'to 108'
               84  LOAD_CONST               2
               86  LOAD_FAST                'noff2'
               88  BINARY_MULTIPLY  
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  LOAD_FAST                'nF2'
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_TRUE    108  'to 108'
              100  LOAD_FAST                'nF2'
              102  LOAD_CONST               3
              104  COMPARE_OP               <
              106  POP_JUMP_IF_FALSE   120  'to 120'
            108_0  COME_FROM            98  '98'
            108_1  COME_FROM            82  '82'
            108_2  COME_FROM            74  '74'

 L. 630       108  LOAD_GLOBAL              NPKError
              110  LOAD_STR                 'npoints must odd and >2 '
              112  LOAD_FAST                'npkd'
              114  LOAD_CONST               ('data',)
              116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           106  '106'

 L. 631       120  LOAD_FAST                'npkd'
              122  LOAD_ATTR                peaks
              124  GET_ITER         
          126_128  FOR_ITER            526  'to 526'
              130  STORE_FAST               'pk'

 L. 632       132  LOAD_GLOBAL              int
              134  LOAD_GLOBAL              round
              136  LOAD_FAST                'pk'
              138  LOAD_ATTR                posF1
              140  LOAD_FAST                'noff1'
              142  BINARY_SUBTRACT  
              144  CALL_FUNCTION_1       1  ''
              146  CALL_FUNCTION_1       1  ''
              148  STORE_FAST               'st1'

 L. 633       150  LOAD_GLOBAL              int
              152  LOAD_GLOBAL              round
              154  LOAD_FAST                'pk'
              156  LOAD_ATTR                posF1
              158  LOAD_FAST                'noff1'
              160  BINARY_ADD       
              162  LOAD_CONST               1
              164  BINARY_ADD       
              166  CALL_FUNCTION_1       1  ''
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'end1'

 L. 634       172  LOAD_GLOBAL              int
              174  LOAD_GLOBAL              round
              176  LOAD_FAST                'pk'
              178  LOAD_ATTR                posF2
              180  LOAD_FAST                'noff2'
              182  BINARY_SUBTRACT  
              184  CALL_FUNCTION_1       1  ''
              186  CALL_FUNCTION_1       1  ''
              188  STORE_DEREF              'st2'

 L. 635       190  LOAD_GLOBAL              int
              192  LOAD_GLOBAL              round
              194  LOAD_FAST                'pk'
              196  LOAD_ATTR                posF2
              198  LOAD_FAST                'noff2'
              200  BINARY_ADD       
              202  LOAD_CONST               1
              204  BINARY_ADD       
              206  CALL_FUNCTION_1       1  ''
              208  CALL_FUNCTION_1       1  ''
              210  STORE_DEREF              'end2'

 L. 636       212  LOAD_GLOBAL              np
              214  LOAD_METHOD              array
              216  LOAD_CLOSURE             'end2'
              218  LOAD_CLOSURE             'st2'
              220  BUILD_TUPLE_2         2 
              222  LOAD_LISTCOMP            '<code_object <listcomp>>'
              224  LOAD_STR                 'centroid2d.<locals>.<listcomp>'
              226  MAKE_FUNCTION_8          'closure'
              228  LOAD_GLOBAL              range
              230  LOAD_FAST                'st1'
              232  LOAD_FAST                'end1'
              234  CALL_FUNCTION_2       2  ''
              236  GET_ITER         
              238  CALL_FUNCTION_1       1  ''
              240  CALL_METHOD_1         1  ''
              242  LOAD_METHOD              ravel
              244  CALL_METHOD_0         0  ''
              246  STORE_FAST               'yxdata'

 L. 639       248  LOAD_FAST                'npkd'
              250  LOAD_METHOD              get_buffer
              252  CALL_METHOD_0         0  ''
              254  LOAD_FAST                'st1'
              256  LOAD_FAST                'end1'
              258  BUILD_SLICE_2         2 
              260  LOAD_DEREF               'st2'
              262  LOAD_DEREF               'end2'
              264  BUILD_SLICE_2         2 
              266  BUILD_TUPLE_2         2 
              268  BINARY_SUBSCR    
              270  LOAD_METHOD              ravel
              272  CALL_METHOD_0         0  ''
              274  STORE_FAST               'zdata'

 L. 640       276  SETUP_FINALLY       318  'to 318'

 L. 642       278  LOAD_GLOBAL              curve_fit
              280  LOAD_GLOBAL              center2d
              282  LOAD_FAST                'yxdata'
              284  LOAD_FAST                'zdata'
              286  LOAD_FAST                'pk'
              288  LOAD_ATTR                posF1
              290  LOAD_FAST                'pk'
              292  LOAD_ATTR                posF2
              294  LOAD_FAST                'pk'
              296  LOAD_ATTR                intens
              298  LOAD_CONST               1.0
              300  LOAD_CONST               1.0
              302  BUILD_LIST_5          5 
              304  LOAD_CONST               ('p0',)
              306  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              308  UNPACK_SEQUENCE_2     2 
              310  STORE_FAST               'popt'
              312  STORE_FAST               'pcov'
              314  POP_BLOCK        
              316  JUMP_FORWARD        360  'to 360'
            318_0  COME_FROM_FINALLY   276  '276'

 L. 643       318  DUP_TOP          
              320  LOAD_GLOBAL              RuntimeError
              322  COMPARE_OP               exception-match
          324_326  POP_JUMP_IF_FALSE   358  'to 358'
              328  POP_TOP          
              330  POP_TOP          
              332  POP_TOP          

 L. 644       334  LOAD_GLOBAL              print
              336  LOAD_STR                 'peak %d (label %s) centroid could not be fitted'
              338  LOAD_FAST                'pk'
              340  LOAD_ATTR                Id
              342  LOAD_FAST                'pk'
              344  LOAD_ATTR                label
              346  BUILD_TUPLE_2         2 
              348  BINARY_MODULO    
              350  CALL_FUNCTION_1       1  ''
              352  POP_TOP          
              354  POP_EXCEPT       
              356  JUMP_FORWARD        360  'to 360'
            358_0  COME_FROM           324  '324'
              358  END_FINALLY      
            360_0  COME_FROM           356  '356'
            360_1  COME_FROM           316  '316'

 L. 645       360  LOAD_FAST                'popt'
              362  LOAD_CONST               0
              364  BINARY_SUBSCR    
              366  LOAD_FAST                'pk'
              368  STORE_ATTR               posF1

 L. 646       370  LOAD_FAST                'popt'
              372  LOAD_CONST               1
              374  BINARY_SUBSCR    
              376  LOAD_FAST                'pk'
              378  STORE_ATTR               posF2

 L. 647       380  LOAD_FAST                'popt'
              382  LOAD_CONST               2
              384  BINARY_SUBSCR    
              386  LOAD_FAST                'pk'
              388  STORE_ATTR               intens

 L. 648       390  LOAD_GLOBAL              np
              392  LOAD_METHOD              sqrt
              394  LOAD_CONST               2.0
              396  CALL_METHOD_1         1  ''
              398  LOAD_FAST                'popt'
              400  LOAD_CONST               3
              402  BINARY_SUBSCR    
              404  BINARY_MULTIPLY  
              406  LOAD_FAST                'pk'
              408  STORE_ATTR               widthF1

 L. 649       410  LOAD_GLOBAL              np
              412  LOAD_METHOD              sqrt
              414  LOAD_CONST               2.0
              416  CALL_METHOD_1         1  ''
              418  LOAD_FAST                'popt'
              420  LOAD_CONST               4
              422  BINARY_SUBSCR    
              424  BINARY_MULTIPLY  
              426  LOAD_FAST                'pk'
              428  STORE_ATTR               widthF2

 L. 650       430  LOAD_GLOBAL              np
              432  LOAD_METHOD              sqrt
              434  LOAD_GLOBAL              np
              436  LOAD_METHOD              diag
              438  LOAD_FAST                'pcov'
              440  CALL_METHOD_1         1  ''
              442  CALL_METHOD_1         1  ''
              444  STORE_FAST               'errors'

 L. 651       446  LOAD_GLOBAL              print
              448  LOAD_FAST                'errors'
              450  CALL_FUNCTION_1       1  ''
              452  POP_TOP          

 L. 652       454  LOAD_FAST                'errors'
              456  LOAD_CONST               0
              458  BINARY_SUBSCR    
              460  LOAD_FAST                'pk'
              462  STORE_ATTR               posF1_err

 L. 653       464  LOAD_FAST                'errors'
              466  LOAD_CONST               1
              468  BINARY_SUBSCR    
              470  LOAD_FAST                'pk'
              472  STORE_ATTR               posF2_err

 L. 654       474  LOAD_FAST                'errors'
              476  LOAD_CONST               2
              478  BINARY_SUBSCR    
              480  LOAD_FAST                'pk'
              482  STORE_ATTR               intens_err

 L. 655       484  LOAD_GLOBAL              np
              486  LOAD_METHOD              sqrt
              488  LOAD_CONST               2.0
              490  CALL_METHOD_1         1  ''
              492  LOAD_FAST                'errors'
              494  LOAD_CONST               3
              496  BINARY_SUBSCR    
              498  BINARY_MULTIPLY  
              500  LOAD_FAST                'pk'
              502  STORE_ATTR               widthF1_err

 L. 656       504  LOAD_GLOBAL              np
              506  LOAD_METHOD              sqrt
              508  LOAD_CONST               2.0
              510  CALL_METHOD_1         1  ''
              512  LOAD_FAST                'errors'
              514  LOAD_CONST               4
              516  BINARY_SUBSCR    
              518  BINARY_MULTIPLY  
              520  LOAD_FAST                'pk'
              522  STORE_ATTR               widthF2_err
              524  JUMP_BACK           126  'to 126'

Parse error at or near `STORE_ATTR' instruction at offset 522


def centroid(npkd, *arg, **kwarg):
    if npkd.dim == 1:
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', message='.*ovariance.*')
            centroid1d(npkd, *arg, **kwarg)
    else:
        if npkd.dim == 2:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', message='.*ovariance.*')
                centroid2d(npkd, *arg, **kwarg)
        else:
            raise Exception('Centroid yet to be done')
    return npkd


def display_peaks(npkd, peak_label=False, peak_mode='marker', zoom=None, show=False, color=None, markersize=6, figure=None, scale=1.0, NbMaxPeaks=NbMaxDisplayPeaks):
    """
    display the content of the peak list, 
    peak_mode is either "marker" (default) or "bar" (1D only)
    zoom is in current unit.
    """
    if npkd.dim == 1:
        z1, z2 = parsezoom(npkd, zoom)
        if npkd.axis1.itype == 0:
            ff1 = npkd.axis1.itoc
        else:
            ff1 = lambda x: npkd.axis1.itoc(2 * x)
        return npkd.peaks.display(peak_label=peak_label, peak_mode=peak_mode, zoom=(z1, z2), show=show, f=ff1, color=color, markersize=markersize, figure=figure, scale=scale, NbMaxPeaks=NbMaxPeaks)
    if npkd.dim == 2:
        z1lo, z1up, z2lo, z2up = parsezoom(npkd, zoom)
        if npkd.axis1.itype == 0:
            ff1 = npkd.axis1.itoc
        else:
            ff1 = lambda x: npkd.axis1.itoc(2 * x)
        if npkd.axis2.itype == 0:
            ff2 = npkd.axis2.itoc
        else:
            ff2 = lambda x: npkd.axis2.itoc(2 * x)
        return npkd.peaks.display(peak_label=peak_label, zoom=((z1lo, z1up), (z2lo, z2up)), show=show, f1=ff1, f2=ff2, color=color, markersize=markersize, figure=figure, NbMaxPeaks=NbMaxPeaks)
    raise Exception('to be done')


def report_peaks(npkd, file=None, format=None, NbMaxPeaks=NbMaxDisplayPeaks):
    """
    print the content of the peak list, using the current unit
    
    if file should be an already opened writable file stream. 
    if None, output will go to stdout
    
    for documentation, check Peak1D.report() and Peak2D.report()
    """
    if npkd.dim == 1:
        if npkd.axis1.itype == 0:
            ff1 = npkd.axis1.itoc
        else:
            ff1 = lambda x: npkd.axis1.itoc(2 * x)
        return npkd.peaks.report(f=ff1, file=file, format=format, NbMaxPeaks=NbMaxPeaks)
    if npkd.dim == 2:
        if npkd.axis1.itype == 0:
            ff1 = npkd.axis1.itoc
        else:
            ff1 = lambda x: npkd.axis1.itoc(2 * x)
        if npkd.axis2.itype == 0:
            ff2 = npkd.axis2.itoc
        else:
            ff2 = lambda x: npkd.axis2.itoc(2 * x)
        return npkd.peaks.report(f1=ff1, f2=ff2, file=file, format=format, NbMaxPeaks=NbMaxPeaks)
    raise Exception('to be done')


def pk2pandas(npkd, full=False):
    """export extract of current peak list to pandas Dataframe - in current unit
    if full is False (default), the uncertainty are not listed
    uses nmr or ms version depending on data_type
    """
    import spike.FTMS
    if isinstance(npkd, spike.FTMS.FTMSData):
        return pk2pandas_ms(npkd, full=full)
    return pk2pandas_nmr(npkd, full=full)


def pk2pandas_ms--- This code section failed: ---

 L. 738         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              pandas
                6  STORE_FAST               'pd'

 L. 739         8  LOAD_FAST                'npkd'
               10  LOAD_ATTR                dim
               12  LOAD_CONST               1
               14  COMPARE_OP               ==
            16_18  POP_JUMP_IF_FALSE   360  'to 360'

 L. 740        20  LOAD_GLOBAL              np
               22  LOAD_METHOD              array
               24  LOAD_LISTCOMP            '<code_object <listcomp>>'
               26  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
               28  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               30  LOAD_FAST                'npkd'
               32  LOAD_ATTR                peaks
               34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'width'

 L. 741        42  LOAD_CONST               0.5
               44  LOAD_GLOBAL              abs
               46  LOAD_FAST                'npkd'
               48  LOAD_ATTR                axis1
               50  LOAD_METHOD              itoc
               52  LOAD_FAST                'npkd'
               54  LOAD_ATTR                peaks
               56  LOAD_ATTR                pos
               58  LOAD_FAST                'width'
               60  BINARY_ADD       
               62  CALL_METHOD_1         1  ''
               64  LOAD_FAST                'npkd'
               66  LOAD_ATTR                axis1
               68  LOAD_METHOD              itoc
               70  LOAD_FAST                'npkd'
               72  LOAD_ATTR                peaks
               74  LOAD_ATTR                pos
               76  LOAD_FAST                'width'
               78  BINARY_SUBTRACT  
               80  CALL_METHOD_1         1  ''
               82  BINARY_SUBTRACT  
               84  CALL_FUNCTION_1       1  ''
               86  BINARY_MULTIPLY  
               88  STORE_FAST               'width_array'

 L. 742        90  LOAD_FAST                'full'
            92_94  POP_JUMP_IF_FALSE   270  'to 270'

 L. 743        96  LOAD_GLOBAL              np
               98  LOAD_METHOD              array
              100  LOAD_LISTCOMP            '<code_object <listcomp>>'
              102  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              104  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              106  LOAD_FAST                'npkd'
              108  LOAD_ATTR                peaks
              110  GET_ITER         
              112  CALL_FUNCTION_1       1  ''
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'err'

 L. 744       118  LOAD_CONST               0.5
              120  LOAD_GLOBAL              abs
              122  LOAD_FAST                'npkd'
              124  LOAD_ATTR                axis1
              126  LOAD_METHOD              itoc
              128  LOAD_FAST                'npkd'
              130  LOAD_ATTR                peaks
              132  LOAD_ATTR                pos
              134  LOAD_FAST                'err'
              136  BINARY_ADD       
              138  CALL_METHOD_1         1  ''
              140  LOAD_FAST                'npkd'
              142  LOAD_ATTR                axis1
              144  LOAD_METHOD              itoc
              146  LOAD_FAST                'npkd'
              148  LOAD_ATTR                peaks
              150  LOAD_ATTR                pos
              152  LOAD_FAST                'err'
              154  BINARY_SUBTRACT  
              156  CALL_METHOD_1         1  ''
              158  BINARY_SUBTRACT  
              160  CALL_FUNCTION_1       1  ''
              162  BINARY_MULTIPLY  
              164  STORE_FAST               'pos_err_array'

 L. 745       166  LOAD_FAST                'pd'
              168  LOAD_METHOD              DataFrame

 L. 746       170  LOAD_LISTCOMP            '<code_object <listcomp>>'
              172  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              174  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              176  LOAD_FAST                'npkd'
              178  LOAD_ATTR                peaks
              180  GET_ITER         
              182  CALL_FUNCTION_1       1  ''

 L. 747       184  LOAD_FAST                'npkd'
              186  LOAD_ATTR                peaks
              188  LOAD_ATTR                label

 L. 748       190  LOAD_FAST                'npkd'
              192  LOAD_ATTR                axis1
              194  LOAD_METHOD              itoc
              196  LOAD_FAST                'npkd'
              198  LOAD_ATTR                peaks
              200  LOAD_ATTR                pos
              202  CALL_METHOD_1         1  ''

 L. 749       204  LOAD_FAST                'width_array'

 L. 750       206  LOAD_GLOBAL              np
              208  LOAD_METHOD              around
              210  LOAD_FAST                'npkd'
              212  LOAD_ATTR                axis1
              214  LOAD_METHOD              itoc
              216  LOAD_FAST                'npkd'
              218  LOAD_ATTR                peaks
              220  LOAD_ATTR                pos
              222  CALL_METHOD_1         1  ''
              224  LOAD_FAST                'width_array'
              226  BINARY_TRUE_DIVIDE
              228  LOAD_CONST               -3
              230  CALL_METHOD_2         2  ''

 L. 751       232  LOAD_FAST                'npkd'
              234  LOAD_ATTR                peaks
              236  LOAD_ATTR                intens

 L. 752       238  LOAD_FAST                'pos_err_array'

 L. 753       240  LOAD_LISTCOMP            '<code_object <listcomp>>'
              242  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              244  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              246  LOAD_FAST                'npkd'
              248  LOAD_ATTR                peaks
              250  GET_ITER         
              252  CALL_FUNCTION_1       1  ''

 L. 745       254  LOAD_CONST               ('Id', 'Label', 'm/z', 'Δm/z', 'R', 'Intensity', 'ε_m/z', 'ε_Intensity')
              256  BUILD_CONST_KEY_MAP_8     8 
              258  CALL_METHOD_1         1  ''
              260  LOAD_METHOD              set_index

 L. 754       262  LOAD_STR                 'Id'

 L. 745       264  CALL_METHOD_1         1  ''
              266  STORE_FAST               'P1'
              268  JUMP_FORWARD        972  'to 972'
            270_0  COME_FROM            92  '92'

 L. 756       270  LOAD_FAST                'pd'
              272  LOAD_METHOD              DataFrame

 L. 757       274  LOAD_LISTCOMP            '<code_object <listcomp>>'
              276  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              278  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              280  LOAD_FAST                'npkd'
              282  LOAD_ATTR                peaks
              284  GET_ITER         
              286  CALL_FUNCTION_1       1  ''

 L. 758       288  LOAD_FAST                'npkd'
              290  LOAD_ATTR                peaks
              292  LOAD_ATTR                label

 L. 759       294  LOAD_FAST                'npkd'
              296  LOAD_ATTR                axis1
              298  LOAD_METHOD              itoc
              300  LOAD_FAST                'npkd'
              302  LOAD_ATTR                peaks
              304  LOAD_ATTR                pos
              306  CALL_METHOD_1         1  ''

 L. 760       308  LOAD_FAST                'width_array'

 L. 761       310  LOAD_GLOBAL              np
              312  LOAD_METHOD              around
              314  LOAD_FAST                'npkd'
              316  LOAD_ATTR                axis1
              318  LOAD_METHOD              itoc
              320  LOAD_FAST                'npkd'
              322  LOAD_ATTR                peaks
              324  LOAD_ATTR                pos
              326  CALL_METHOD_1         1  ''
              328  LOAD_FAST                'width_array'
              330  BINARY_TRUE_DIVIDE
              332  LOAD_CONST               -3
              334  CALL_METHOD_2         2  ''

 L. 762       336  LOAD_FAST                'npkd'
              338  LOAD_ATTR                peaks
              340  LOAD_ATTR                intens

 L. 756       342  LOAD_CONST               ('Id', 'Label', 'm/z', 'Δm/z', 'R', 'Intensity')
              344  BUILD_CONST_KEY_MAP_6     6 
              346  CALL_METHOD_1         1  ''
              348  LOAD_METHOD              set_index

 L. 763       350  LOAD_STR                 'Id'

 L. 756       352  CALL_METHOD_1         1  ''
              354  STORE_FAST               'P1'
          356_358  JUMP_FORWARD        972  'to 972'
            360_0  COME_FROM            16  '16'

 L. 765       360  LOAD_FAST                'npkd'
              362  LOAD_ATTR                dim
              364  LOAD_CONST               2
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   964  'to 964'

 L. 767       372  LOAD_GLOBAL              np
              374  LOAD_METHOD              array
              376  LOAD_LISTCOMP            '<code_object <listcomp>>'
              378  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              380  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              382  LOAD_FAST                'npkd'
              384  LOAD_ATTR                peaks
              386  GET_ITER         
              388  CALL_FUNCTION_1       1  ''
              390  CALL_METHOD_1         1  ''
              392  STORE_FAST               'width1'

 L. 768       394  LOAD_CONST               0.5
              396  LOAD_GLOBAL              abs
              398  LOAD_FAST                'npkd'
              400  LOAD_ATTR                axis1
              402  LOAD_METHOD              itoc
              404  LOAD_FAST                'npkd'
              406  LOAD_ATTR                peaks
              408  LOAD_ATTR                pos
              410  LOAD_FAST                'npkd'
              412  LOAD_ATTR                peaks
              414  LOAD_ATTR                width1
              416  BINARY_ADD       
              418  CALL_METHOD_1         1  ''
              420  LOAD_FAST                'npkd'
              422  LOAD_ATTR                axis1
              424  LOAD_METHOD              itoc
              426  LOAD_FAST                'npkd'
              428  LOAD_ATTR                peaks
              430  LOAD_ATTR                pos
              432  LOAD_FAST                'npkd'
              434  LOAD_ATTR                peaks
              436  LOAD_ATTR                width1
              438  BINARY_SUBTRACT  
              440  CALL_METHOD_1         1  ''
              442  BINARY_SUBTRACT  
              444  CALL_FUNCTION_1       1  ''
              446  BINARY_MULTIPLY  
              448  STORE_FAST               'width1_array'

 L. 769       450  LOAD_GLOBAL              np
              452  LOAD_METHOD              array
              454  LOAD_LISTCOMP            '<code_object <listcomp>>'
              456  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              458  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              460  LOAD_FAST                'npkd'
              462  LOAD_ATTR                peaks
              464  GET_ITER         
              466  CALL_FUNCTION_1       1  ''
              468  CALL_METHOD_1         1  ''
              470  STORE_FAST               'width2'

 L. 770       472  LOAD_CONST               0.5
              474  LOAD_GLOBAL              abs
              476  LOAD_FAST                'npkd'
              478  LOAD_ATTR                axis2
              480  LOAD_METHOD              itoc
              482  LOAD_FAST                'npkd'
              484  LOAD_ATTR                peaks
              486  LOAD_ATTR                pos
              488  LOAD_FAST                'npkd'
              490  LOAD_ATTR                peaks
              492  LOAD_ATTR                width2
              494  BINARY_ADD       
              496  CALL_METHOD_1         1  ''
              498  LOAD_FAST                'npkd'
              500  LOAD_ATTR                axis2
              502  LOAD_METHOD              itoc
              504  LOAD_FAST                'npkd'
              506  LOAD_ATTR                peaks
              508  LOAD_ATTR                pos
              510  LOAD_FAST                'npkd'
              512  LOAD_ATTR                peaks
              514  LOAD_ATTR                width2
              516  BINARY_SUBTRACT  
              518  CALL_METHOD_1         1  ''
              520  BINARY_SUBTRACT  
              522  CALL_FUNCTION_1       1  ''
              524  BINARY_MULTIPLY  
              526  STORE_FAST               'width2_array'

 L. 773       528  LOAD_FAST                'npkd'
              530  LOAD_ATTR                axis1
              532  LOAD_METHOD              itoc
              534  LOAD_FAST                'npkd'
              536  LOAD_ATTR                peaks
              538  LOAD_ATTR                pos
              540  CALL_METHOD_1         1  ''
              542  LOAD_FAST                'width1_array'
              544  BINARY_TRUE_DIVIDE
              546  STORE_FAST               'R1'

 L. 774       548  LOAD_FAST                'npkd'
              550  LOAD_ATTR                axis2
              552  LOAD_METHOD              itoc
              554  LOAD_FAST                'npkd'
              556  LOAD_ATTR                peaks
              558  LOAD_ATTR                pos
              560  CALL_METHOD_1         1  ''
              562  LOAD_FAST                'width2_array'
              564  BINARY_TRUE_DIVIDE
              566  STORE_FAST               'R2'

 L. 775       568  LOAD_FAST                'full'
          570_572  POP_JUMP_IF_FALSE   848  'to 848'

 L. 777       574  LOAD_GLOBAL              np
              576  LOAD_METHOD              array
              578  LOAD_LISTCOMP            '<code_object <listcomp>>'
              580  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              582  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              584  LOAD_FAST                'npkd'
              586  LOAD_ATTR                peaks
              588  GET_ITER         
              590  CALL_FUNCTION_1       1  ''
              592  CALL_METHOD_1         1  ''
              594  STORE_FAST               'err1'

 L. 778       596  LOAD_GLOBAL              np
              598  LOAD_METHOD              array
              600  LOAD_LISTCOMP            '<code_object <listcomp>>'
              602  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              604  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              606  LOAD_FAST                'npkd'
              608  LOAD_ATTR                peaks
              610  GET_ITER         
              612  CALL_FUNCTION_1       1  ''
              614  CALL_METHOD_1         1  ''
              616  STORE_FAST               'err2'

 L. 779       618  LOAD_CONST               0.5
              620  LOAD_GLOBAL              abs
              622  LOAD_FAST                'npkd'
              624  LOAD_ATTR                axis1
              626  LOAD_METHOD              itoc
              628  LOAD_FAST                'npkd'
              630  LOAD_ATTR                peaks
              632  LOAD_ATTR                posF1
              634  LOAD_FAST                'err1'
              636  BINARY_ADD       
              638  CALL_METHOD_1         1  ''
              640  LOAD_FAST                'npkd'
              642  LOAD_ATTR                axis1
              644  LOAD_METHOD              itoc
              646  LOAD_FAST                'npkd'
              648  LOAD_ATTR                peaks
              650  LOAD_ATTR                posF1
              652  LOAD_FAST                'err1'
              654  BINARY_SUBTRACT  
              656  CALL_METHOD_1         1  ''
              658  BINARY_SUBTRACT  
              660  CALL_FUNCTION_1       1  ''
              662  BINARY_MULTIPLY  
              664  STORE_FAST               'pos1_err_array'

 L. 780       666  LOAD_CONST               0.5
              668  LOAD_GLOBAL              abs
              670  LOAD_FAST                'npkd'
              672  LOAD_ATTR                axis2
              674  LOAD_METHOD              itoc
              676  LOAD_FAST                'npkd'
              678  LOAD_ATTR                peaks
              680  LOAD_ATTR                posF2
              682  LOAD_FAST                'err2'
              684  BINARY_ADD       
              686  CALL_METHOD_1         1  ''
              688  LOAD_FAST                'npkd'
              690  LOAD_ATTR                axis2
              692  LOAD_METHOD              itoc
              694  LOAD_FAST                'npkd'
              696  LOAD_ATTR                peaks
              698  LOAD_ATTR                posF2
              700  LOAD_FAST                'err2'
              702  BINARY_SUBTRACT  
              704  CALL_METHOD_1         1  ''
              706  BINARY_SUBTRACT  
              708  CALL_FUNCTION_1       1  ''
              710  BINARY_MULTIPLY  
              712  STORE_FAST               'pos2_err_array'

 L. 781       714  LOAD_FAST                'pd'
              716  LOAD_METHOD              DataFrame

 L. 782       718  LOAD_LISTCOMP            '<code_object <listcomp>>'
              720  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              722  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              724  LOAD_FAST                'npkd'
              726  LOAD_ATTR                peaks
              728  GET_ITER         
              730  CALL_FUNCTION_1       1  ''

 L. 783       732  LOAD_FAST                'npkd'
              734  LOAD_ATTR                peaks
              736  LOAD_ATTR                label

 L. 784       738  LOAD_FAST                'npkd'
              740  LOAD_ATTR                axis1
              742  LOAD_METHOD              itoc
              744  LOAD_FAST                'npkd'
              746  LOAD_ATTR                peaks
              748  LOAD_ATTR                posF1
              750  CALL_METHOD_1         1  ''

 L. 785       752  LOAD_FAST                'npkd'
              754  LOAD_ATTR                axis2
              756  LOAD_METHOD              itoc
              758  LOAD_FAST                'npkd'
              760  LOAD_ATTR                peaks
              762  LOAD_ATTR                posF2
              764  CALL_METHOD_1         1  ''

 L. 786       766  LOAD_FAST                'npkd'
              768  LOAD_ATTR                peaks
              770  LOAD_ATTR                intens

 L. 787       772  LOAD_FAST                'width1_array'

 L. 788       774  LOAD_FAST                'width2_array'

 L. 789       776  LOAD_GLOBAL              np
              778  LOAD_METHOD              around
              780  LOAD_FAST                'R1'
              782  LOAD_CONST               -3
              784  CALL_METHOD_2         2  ''

 L. 790       786  LOAD_GLOBAL              np
              788  LOAD_METHOD              around
              790  LOAD_FAST                'R1'
              792  LOAD_CONST               -3
              794  CALL_METHOD_2         2  ''

 L. 791       796  LOAD_GLOBAL              np
              798  LOAD_METHOD              around
              800  LOAD_FAST                'R1'
              802  LOAD_FAST                'R2'
              804  BINARY_MULTIPLY  
              806  LOAD_CONST               1000000.0
              808  BINARY_TRUE_DIVIDE
              810  LOAD_CONST               -3
              812  CALL_METHOD_2         2  ''

 L. 792       814  LOAD_FAST                'pos1_err_array'

 L. 793       816  LOAD_FAST                'pos2_err_array'

 L. 794       818  LOAD_LISTCOMP            '<code_object <listcomp>>'
              820  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              822  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              824  LOAD_FAST                'npkd'
              826  LOAD_ATTR                peaks
              828  GET_ITER         
              830  CALL_FUNCTION_1       1  ''

 L. 781       832  LOAD_CONST               ('Id', 'Label', 'm/z F1', 'm/z F2', 'Intensity', 'Δm/z F1', 'Δm/z F2', 'R1', 'R2', 'R *1E6', 'ε_m/z F1', 'ε_m/z F2', 'ε_Intensity')
              834  BUILD_CONST_KEY_MAP_13    13 
              836  CALL_METHOD_1         1  ''
              838  LOAD_METHOD              set_index

 L. 795       840  LOAD_STR                 'Id'

 L. 781       842  CALL_METHOD_1         1  ''
              844  STORE_FAST               'P1'
              846  JUMP_FORWARD        962  'to 962'
            848_0  COME_FROM           570  '570'

 L. 797       848  LOAD_FAST                'pd'
              850  LOAD_METHOD              DataFrame

 L. 798       852  LOAD_LISTCOMP            '<code_object <listcomp>>'
              854  LOAD_STR                 'pk2pandas_ms.<locals>.<listcomp>'
              856  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              858  LOAD_FAST                'npkd'
              860  LOAD_ATTR                peaks
              862  GET_ITER         
              864  CALL_FUNCTION_1       1  ''

 L. 799       866  LOAD_FAST                'npkd'
              868  LOAD_ATTR                peaks
              870  LOAD_ATTR                label

 L. 800       872  LOAD_FAST                'npkd'
              874  LOAD_ATTR                axis1
              876  LOAD_METHOD              itoc
              878  LOAD_FAST                'npkd'
              880  LOAD_ATTR                peaks
            882_0  COME_FROM           268  '268'
              882  LOAD_ATTR                posF1
              884  CALL_METHOD_1         1  ''

 L. 801       886  LOAD_FAST                'npkd'
              888  LOAD_ATTR                axis2
              890  LOAD_METHOD              itoc
              892  LOAD_FAST                'npkd'
              894  LOAD_ATTR                peaks
              896  LOAD_ATTR                posF2
              898  CALL_METHOD_1         1  ''

 L. 802       900  LOAD_FAST                'npkd'
              902  LOAD_ATTR                peaks
              904  LOAD_ATTR                intens

 L. 803       906  LOAD_FAST                'width1_array'

 L. 804       908  LOAD_FAST                'width2_array'

 L. 805       910  LOAD_GLOBAL              np
              912  LOAD_METHOD              around
              914  LOAD_FAST                'R1'
              916  LOAD_CONST               -3
              918  CALL_METHOD_2         2  ''

 L. 806       920  LOAD_GLOBAL              np
              922  LOAD_METHOD              around
              924  LOAD_FAST                'R1'
              926  LOAD_CONST               -3
              928  CALL_METHOD_2         2  ''

 L. 807       930  LOAD_GLOBAL              np
              932  LOAD_METHOD              around
              934  LOAD_FAST                'R1'
              936  LOAD_FAST                'R2'
              938  BINARY_MULTIPLY  
              940  LOAD_CONST               1000000.0
              942  BINARY_TRUE_DIVIDE
              944  LOAD_CONST               -3
              946  CALL_METHOD_2         2  ''

 L. 797       948  LOAD_CONST               ('Id', 'Label', 'm/z F1', 'm/z F2', 'Intensity', 'Δm/z F1', 'Δm/z F2', 'R1', 'R2', 'R *1E6')
              950  BUILD_CONST_KEY_MAP_10    10 
              952  CALL_METHOD_1         1  ''
              954  LOAD_METHOD              set_index

 L. 808       956  LOAD_STR                 'Id'

 L. 797       958  CALL_METHOD_1         1  ''
              960  STORE_FAST               'P1'
            962_0  COME_FROM           846  '846'
              962  JUMP_FORWARD        972  'to 972'
            964_0  COME_FROM           368  '368'

 L. 810       964  LOAD_GLOBAL              Exception
              966  LOAD_STR                 'Not implemented in 3D yet'
              968  CALL_FUNCTION_1       1  ''
              970  RAISE_VARARGS_1       1  'exception instance'
            972_0  COME_FROM           962  '962'
            972_1  COME_FROM           356  '356'

 L. 811       972  LOAD_FAST                'P1'
              974  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 882_0


def pk2pandas_nmr--- This code section failed: ---

 L. 814         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              pandas
                6  STORE_FAST               'pd'

 L. 815         8  LOAD_FAST                'npkd'
               10  LOAD_ATTR                dim
               12  LOAD_CONST               1
               14  COMPARE_OP               ==
            16_18  POP_JUMP_IF_FALSE   310  'to 310'

 L. 816        20  LOAD_CONST               2
               22  LOAD_FAST                'npkd'
               24  LOAD_ATTR                axis1
               26  LOAD_ATTR                specwidth
               28  BINARY_MULTIPLY  
               30  LOAD_FAST                'npkd'
               32  LOAD_ATTR                cpxsize1
               34  BINARY_TRUE_DIVIDE
               36  STORE_DEREF              'w_itohz'

 L. 818        38  LOAD_GLOBAL              np
               40  LOAD_METHOD              array
               42  LOAD_LISTCOMP            '<code_object <listcomp>>'
               44  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               48  LOAD_FAST                'npkd'
               50  LOAD_ATTR                peaks
               52  GET_ITER         
               54  CALL_FUNCTION_1       1  ''
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'err'

 L. 819        60  LOAD_FAST                'npkd'
               62  LOAD_ATTR                axis1
               64  LOAD_METHOD              itoc
               66  LOAD_FAST                'npkd'
               68  LOAD_ATTR                peaks
               70  LOAD_ATTR                pos
               72  LOAD_FAST                'err'
               74  BINARY_ADD       
               76  CALL_METHOD_1         1  ''
               78  LOAD_FAST                'npkd'
               80  LOAD_ATTR                axis1
               82  LOAD_METHOD              itoc
               84  LOAD_FAST                'npkd'
               86  LOAD_ATTR                peaks
               88  LOAD_ATTR                pos
               90  LOAD_FAST                'err'
               92  BINARY_SUBTRACT  
               94  CALL_METHOD_1         1  ''
               96  BINARY_SUBTRACT  
               98  STORE_FAST               'pos_err_array'

 L. 820       100  LOAD_CONST               0.5
              102  LOAD_GLOBAL              np
              104  LOAD_METHOD              abs
              106  LOAD_FAST                'pos_err_array'
              108  CALL_METHOD_1         1  ''
              110  BINARY_MULTIPLY  
              112  STORE_FAST               'pos_err_array'

 L. 821       114  LOAD_FAST                'full'
              116  POP_JUMP_IF_FALSE   230  'to 230'

 L. 822       118  LOAD_FAST                'pd'
              120  LOAD_METHOD              DataFrame

 L. 823       122  LOAD_LISTCOMP            '<code_object <listcomp>>'
              124  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              126  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              128  LOAD_FAST                'npkd'
              130  LOAD_ATTR                peaks
              132  GET_ITER         
              134  CALL_FUNCTION_1       1  ''

 L. 824       136  LOAD_FAST                'npkd'
              138  LOAD_ATTR                peaks
              140  LOAD_ATTR                label

 L. 825       142  LOAD_FAST                'npkd'
              144  LOAD_ATTR                axis1
              146  LOAD_METHOD              itoc
              148  LOAD_FAST                'npkd'
              150  LOAD_ATTR                peaks
              152  LOAD_ATTR                pos
              154  CALL_METHOD_1         1  ''

 L. 826       156  LOAD_FAST                'npkd'
              158  LOAD_ATTR                peaks
              160  LOAD_ATTR                intens

 L. 827       162  LOAD_CLOSURE             'w_itohz'
              164  BUILD_TUPLE_1         1 
              166  LOAD_LISTCOMP            '<code_object <listcomp>>'
              168  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              170  MAKE_FUNCTION_8          'closure'
              172  LOAD_FAST                'npkd'
              174  LOAD_ATTR                peaks
              176  GET_ITER         
              178  CALL_FUNCTION_1       1  ''

 L. 828       180  LOAD_FAST                'pos_err_array'

 L. 829       182  LOAD_LISTCOMP            '<code_object <listcomp>>'
              184  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              186  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              188  LOAD_FAST                'npkd'
              190  LOAD_ATTR                peaks
              192  GET_ITER         
              194  CALL_FUNCTION_1       1  ''

 L. 830       196  LOAD_CLOSURE             'w_itohz'
              198  BUILD_TUPLE_1         1 
              200  LOAD_LISTCOMP            '<code_object <listcomp>>'
              202  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              204  MAKE_FUNCTION_8          'closure'
              206  LOAD_FAST                'npkd'
              208  LOAD_ATTR                peaks
              210  GET_ITER         
              212  CALL_FUNCTION_1       1  ''

 L. 822       214  LOAD_CONST               ('Id', 'Label', 'Position', 'Intensity', 'Width', 'Position_err', 'Intensity_err', 'Width_err')
              216  BUILD_CONST_KEY_MAP_8     8 
              218  CALL_METHOD_1         1  ''
              220  LOAD_METHOD              set_index

 L. 831       222  LOAD_STR                 'Id'

 L. 822       224  CALL_METHOD_1         1  ''
              226  STORE_FAST               'P1'
              228  JUMP_FORWARD        798  'to 798'
            230_0  COME_FROM           116  '116'

 L. 833       230  LOAD_FAST                'pd'
              232  LOAD_METHOD              DataFrame

 L. 834       234  LOAD_LISTCOMP            '<code_object <listcomp>>'
              236  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              238  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              240  LOAD_FAST                'npkd'
              242  LOAD_ATTR                peaks
              244  GET_ITER         
              246  CALL_FUNCTION_1       1  ''

 L. 835       248  LOAD_FAST                'npkd'
              250  LOAD_ATTR                peaks
              252  LOAD_ATTR                label

 L. 836       254  LOAD_FAST                'npkd'
              256  LOAD_ATTR                axis1
              258  LOAD_METHOD              itoc
              260  LOAD_FAST                'npkd'
              262  LOAD_ATTR                peaks
              264  LOAD_ATTR                pos
              266  CALL_METHOD_1         1  ''

 L. 837       268  LOAD_FAST                'npkd'
              270  LOAD_ATTR                peaks
              272  LOAD_ATTR                intens

 L. 838       274  LOAD_CLOSURE             'w_itohz'
              276  BUILD_TUPLE_1         1 
              278  LOAD_LISTCOMP            '<code_object <listcomp>>'
              280  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              282  MAKE_FUNCTION_8          'closure'
              284  LOAD_FAST                'npkd'
              286  LOAD_ATTR                peaks
              288  GET_ITER         
              290  CALL_FUNCTION_1       1  ''

 L. 833       292  LOAD_CONST               ('Id', 'Label', 'Position', 'Intensity', 'Width')
              294  BUILD_CONST_KEY_MAP_5     5 
              296  CALL_METHOD_1         1  ''
              298  LOAD_METHOD              set_index

 L. 839       300  LOAD_STR                 'Id'

 L. 833       302  CALL_METHOD_1         1  ''
              304  STORE_FAST               'P1'
          306_308  JUMP_FORWARD        798  'to 798'
            310_0  COME_FROM            16  '16'

 L. 840       310  LOAD_FAST                'npkd'
              312  LOAD_ATTR                dim
              314  LOAD_CONST               2
              316  COMPARE_OP               ==
          318_320  POP_JUMP_IF_FALSE   790  'to 790'

 L. 841       322  LOAD_CONST               2
              324  LOAD_FAST                'npkd'
              326  LOAD_ATTR                axis1
              328  LOAD_ATTR                specwidth
              330  BINARY_MULTIPLY  
              332  LOAD_FAST                'npkd'
              334  LOAD_ATTR                cpxsize1
              336  BINARY_TRUE_DIVIDE
              338  STORE_DEREF              'w_itohz1'

 L. 842       340  LOAD_CONST               2
              342  LOAD_FAST                'npkd'
              344  LOAD_ATTR                axis2
              346  LOAD_ATTR                specwidth
              348  BINARY_MULTIPLY  
              350  LOAD_FAST                'npkd'
              352  LOAD_ATTR                cpxsize2
              354  BINARY_TRUE_DIVIDE
              356  STORE_DEREF              'w_itohz2'

 L. 844       358  LOAD_GLOBAL              np
              360  LOAD_METHOD              array
              362  LOAD_LISTCOMP            '<code_object <listcomp>>'
              364  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              366  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              368  LOAD_FAST                'npkd'
              370  LOAD_ATTR                peaks
              372  GET_ITER         
              374  CALL_FUNCTION_1       1  ''
              376  CALL_METHOD_1         1  ''
              378  STORE_FAST               'err1'

 L. 845       380  LOAD_GLOBAL              np
              382  LOAD_METHOD              array
              384  LOAD_LISTCOMP            '<code_object <listcomp>>'
              386  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              388  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              390  LOAD_FAST                'npkd'
              392  LOAD_ATTR                peaks
              394  GET_ITER         
              396  CALL_FUNCTION_1       1  ''
              398  CALL_METHOD_1         1  ''
              400  STORE_FAST               'err2'

 L. 846       402  LOAD_FAST                'npkd'
              404  LOAD_ATTR                axis1
              406  LOAD_METHOD              itoc
              408  LOAD_FAST                'npkd'
              410  LOAD_ATTR                peaks
              412  LOAD_ATTR                posF1
              414  LOAD_FAST                'err1'
              416  BINARY_ADD       
              418  CALL_METHOD_1         1  ''
              420  LOAD_FAST                'npkd'
              422  LOAD_ATTR                axis1
              424  LOAD_METHOD              itoc
              426  LOAD_FAST                'npkd'
              428  LOAD_ATTR                peaks
              430  LOAD_ATTR                posF1
              432  LOAD_FAST                'err1'
              434  BINARY_SUBTRACT  
              436  CALL_METHOD_1         1  ''
              438  BINARY_SUBTRACT  
              440  STORE_FAST               'pos1_err_array'

 L. 847       442  LOAD_FAST                'npkd'
              444  LOAD_ATTR                axis2
              446  LOAD_METHOD              itoc
              448  LOAD_FAST                'npkd'
              450  LOAD_ATTR                peaks
              452  LOAD_ATTR                posF2
              454  LOAD_FAST                'err2'
              456  BINARY_ADD       
              458  CALL_METHOD_1         1  ''
              460  LOAD_FAST                'npkd'
              462  LOAD_ATTR                axis2
              464  LOAD_METHOD              itoc
              466  LOAD_FAST                'npkd'
              468  LOAD_ATTR                peaks
              470  LOAD_ATTR                posF2
              472  LOAD_FAST                'err2'
              474  BINARY_SUBTRACT  
              476  CALL_METHOD_1         1  ''
              478  BINARY_SUBTRACT  
              480  STORE_FAST               'pos2_err_array'

 L. 848       482  LOAD_CONST               0.5
              484  LOAD_GLOBAL              np
              486  LOAD_METHOD              abs
              488  LOAD_FAST                'pos1_err_array'
              490  CALL_METHOD_1         1  ''
              492  BINARY_MULTIPLY  
              494  STORE_FAST               'pos1_err_array'

 L. 849       496  LOAD_CONST               0.5
              498  LOAD_GLOBAL              np
              500  LOAD_METHOD              abs
              502  LOAD_FAST                'pos2_err_array'
              504  CALL_METHOD_1         1  ''
              506  BINARY_MULTIPLY  
              508  STORE_FAST               'pos2_err_array'

 L. 850       510  LOAD_FAST                'full'
          512_514  POP_JUMP_IF_FALSE   680  'to 680'

 L. 851       516  LOAD_FAST                'pd'
              518  LOAD_METHOD              DataFrame

 L. 852       520  LOAD_LISTCOMP            '<code_object <listcomp>>'
              522  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              524  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              526  LOAD_FAST                'npkd'
              528  LOAD_ATTR                peaks
              530  GET_ITER         
              532  CALL_FUNCTION_1       1  ''

 L. 853       534  LOAD_FAST                'npkd'
              536  LOAD_ATTR                peaks
              538  LOAD_ATTR                label

 L. 854       540  LOAD_FAST                'npkd'
              542  LOAD_ATTR                axis1
              544  LOAD_METHOD              itoc
              546  LOAD_FAST                'npkd'
              548  LOAD_ATTR                peaks
              550  LOAD_ATTR                posF1
              552  CALL_METHOD_1         1  ''

 L. 855       554  LOAD_FAST                'npkd'
              556  LOAD_ATTR                axis2
              558  LOAD_METHOD              itoc
              560  LOAD_FAST                'npkd'
              562  LOAD_ATTR                peaks
              564  LOAD_ATTR                posF2
              566  CALL_METHOD_1         1  ''

 L. 856       568  LOAD_FAST                'npkd'
              570  LOAD_ATTR                peaks
              572  LOAD_ATTR                intens

 L. 857       574  LOAD_CLOSURE             'w_itohz1'
              576  BUILD_TUPLE_1         1 
              578  LOAD_LISTCOMP            '<code_object <listcomp>>'
              580  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              582  MAKE_FUNCTION_8          'closure'
              584  LOAD_FAST                'npkd'
              586  LOAD_ATTR                peaks
              588  GET_ITER         
              590  CALL_FUNCTION_1       1  ''

 L. 858       592  LOAD_CLOSURE             'w_itohz2'
              594  BUILD_TUPLE_1         1 
              596  LOAD_LISTCOMP            '<code_object <listcomp>>'
              598  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              600  MAKE_FUNCTION_8          'closure'
              602  LOAD_FAST                'npkd'
              604  LOAD_ATTR                peaks
              606  GET_ITER         
              608  CALL_FUNCTION_1       1  ''

 L. 859       610  LOAD_FAST                'pos1_err_array'

 L. 860       612  LOAD_FAST                'pos2_err_array'

 L. 861       614  LOAD_LISTCOMP            '<code_object <listcomp>>'
              616  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              618  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              620  LOAD_FAST                'npkd'
              622  LOAD_ATTR                peaks
              624  GET_ITER         
              626  CALL_FUNCTION_1       1  ''

 L. 862       628  LOAD_CLOSURE             'w_itohz1'
              630  BUILD_TUPLE_1         1 
              632  LOAD_LISTCOMP            '<code_object <listcomp>>'
              634  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              636  MAKE_FUNCTION_8          'closure'
              638  LOAD_FAST                'npkd'
              640  LOAD_ATTR                peaks
              642  GET_ITER         
              644  CALL_FUNCTION_1       1  ''

 L. 863       646  LOAD_CLOSURE             'w_itohz1'
              648  BUILD_TUPLE_1         1 
              650  LOAD_LISTCOMP            '<code_object <listcomp>>'
              652  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              654  MAKE_FUNCTION_8          'closure'
              656  LOAD_FAST                'npkd'
              658  LOAD_ATTR                peaks
              660  GET_ITER         
              662  CALL_FUNCTION_1       1  ''

 L. 851       664  LOAD_CONST               ('Id', 'Label', 'Position F1', 'Position F2', 'Intensity', 'Width F1', 'Width F2', 'Position_err F1', 'Position_err F2', 'Intensity_err', 'Width_err F1', 'Width_err F2')
              666  BUILD_CONST_KEY_MAP_12    12 
              668  CALL_METHOD_1         1  ''
              670  LOAD_METHOD              set_index

 L. 864       672  LOAD_STR                 'Id'

 L. 851       674  CALL_METHOD_1         1  ''
              676  STORE_FAST               'P1'
              678  JUMP_FORWARD        788  'to 788'
            680_0  COME_FROM           512  '512'

 L. 866       680  LOAD_FAST                'pd'
              682  LOAD_METHOD              DataFrame

 L. 867       684  LOAD_LISTCOMP            '<code_object <listcomp>>'
              686  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              688  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              690  LOAD_FAST                'npkd'
              692  LOAD_ATTR                peaks
              694  GET_ITER         
              696  CALL_FUNCTION_1       1  ''

 L. 868       698  LOAD_FAST                'npkd'
              700  LOAD_ATTR                peaks
              702  LOAD_ATTR                label

 L. 869       704  LOAD_FAST                'npkd'
              706  LOAD_ATTR                axis1
              708  LOAD_METHOD              itoc
              710  LOAD_FAST                'npkd'
              712  LOAD_ATTR                peaks
              714  LOAD_ATTR                posF1
              716  CALL_METHOD_1         1  ''
            718_0  COME_FROM           228  '228'

 L. 870       718  LOAD_FAST                'npkd'
              720  LOAD_ATTR                axis2
              722  LOAD_METHOD              itoc
              724  LOAD_FAST                'npkd'
              726  LOAD_ATTR                peaks
              728  LOAD_ATTR                posF2
              730  CALL_METHOD_1         1  ''

 L. 871       732  LOAD_FAST                'npkd'
              734  LOAD_ATTR                peaks
              736  LOAD_ATTR                intens

 L. 872       738  LOAD_CLOSURE             'w_itohz1'
              740  BUILD_TUPLE_1         1 
              742  LOAD_LISTCOMP            '<code_object <listcomp>>'
              744  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              746  MAKE_FUNCTION_8          'closure'
              748  LOAD_FAST                'npkd'
              750  LOAD_ATTR                peaks
              752  GET_ITER         
              754  CALL_FUNCTION_1       1  ''

 L. 873       756  LOAD_CLOSURE             'w_itohz2'
              758  BUILD_TUPLE_1         1 
              760  LOAD_LISTCOMP            '<code_object <listcomp>>'
              762  LOAD_STR                 'pk2pandas_nmr.<locals>.<listcomp>'
              764  MAKE_FUNCTION_8          'closure'
              766  LOAD_FAST                'npkd'
              768  LOAD_ATTR                peaks
              770  GET_ITER         
              772  CALL_FUNCTION_1       1  ''

 L. 866       774  LOAD_CONST               ('Id', 'Label', 'Position F1', 'Position F2', 'Intensity', 'Width F1', 'Width F2')
              776  BUILD_CONST_KEY_MAP_7     7 
              778  CALL_METHOD_1         1  ''
              780  LOAD_METHOD              set_index

 L. 874       782  LOAD_STR                 'Id'

 L. 866       784  CALL_METHOD_1         1  ''
              786  STORE_FAST               'P1'
            788_0  COME_FROM           678  '678'
              788  JUMP_FORWARD        798  'to 798'
            790_0  COME_FROM           318  '318'

 L. 876       790  LOAD_GLOBAL              Exception
              792  LOAD_STR                 'Not implemented in 3D yet'
              794  CALL_FUNCTION_1       1  ''
              796  RAISE_VARARGS_1       1  'exception instance'
            798_0  COME_FROM           788  '788'
            798_1  COME_FROM           306  '306'

 L. 877       798  LOAD_FAST                'P1'
              800  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 718_0


class PeakTests(unittest.TestCase):

    def test_peaks2d(self):
        """test 2D peak picker"""
        print(self.test_peaks2d.__doc__)
        M = np.zeros((30, 30))
        M[(5, 7)] = 20
        M[(10, 12)] = 20
        d = _NPKData(buffer=M)
        d.pp(threshold=10)
        self.assertEqual(list(d.peaks.posF1), [5, 10])
        self.assertEqual(list(d.peaks.posF2), [7, 12])
        self.assertEqual(list(d.peaks.intens), [20.0, 20.0])

    def test_peaks1d(self):
        """test 1D peak picker"""
        print(self.test_peaks1d.__doc__)
        M = np.zeros(30)
        M[5] = 20
        M[7] = 8
        M[15] = 11
        M[10] = 20
        d = _NPKData(buffer=M)
        d.pp(threshold=3)
        self.assertEqual(list(d.peaks.pos), [5.0, 7.0, 10.0, 15.0])
        self.assertEqual(list(d.peaks.intens), [20.0, 8.0, 20.0, 11.0])
        d.peaks.report(NbMaxPeaks=2)

    def test_center1d(self):
        x = np.arange(5)
        y = center(x, 2.2, 10.0, 1.2)
        self.assertAlmostEqual(y[2], 9.72222222)
        d = _NPKData(buffer=(np.maximum(y, 0.0)))
        d.peaks = Peak1DList(source=d)
        d.peaks.append(Peak1D(0, '0', 9.7, 2))
        d.peaks[(-1)].width = 1.0
        d.centroid(npoints=3)
        self.assertAlmostEqual(d.peaks[0].pos, 2.2)
        self.assertAlmostEqual(d.peaks[0].intens, 10.0)
        self.assertAlmostEqual(d.peaks[0].width, 1.2 * np.sqrt(2))
        d.peaks.report(NbMaxPeaks=10)

    def test_center2d(self):
        M = np.zeros((20, 20))
        for y in range(1, 10):
            for x in range(6, 11):
                M[(y, x)] = center2d(np.array([y, x]), 5.3, 7.9, 20.0, 5.0, 1.3)
            else:
                self.assertAlmostEqual(M[(2, 7)], 5.87777515)
                d = _NPKData(buffer=(np.maximum(M, 0.0)))
                d.peaks = Peak2DList(source=d)
                d.peaks.append(Peak2D(0, '0', 18.0, 5, 8))
                d.centroid(npoints_F1=5)
                self.assertAlmostEqual(d.peaks[0].posF1, 5.3)
                self.assertAlmostEqual(d.peaks[0].posF2, 7.9)
                self.assertAlmostEqual(d.peaks[0].intens, 20.0)
                self.assertAlmostEqual(d.peaks[0].widthF1, 5.0 * np.sqrt(2))
                self.assertAlmostEqual(d.peaks[0].widthF2, 1.3 * np.sqrt(2))


NPKData_plugin('pp', peakpick)
NPKData_plugin('peakpick', peakpick)
NPKData_plugin('centroid', centroid)
NPKData_plugin('report_peaks', report_peaks)
NPKData_plugin('display_peaks', display_peaks)
NPKData_plugin('peaks2d', peaks2d)
NPKData_plugin('pk2pandas', pk2pandas)