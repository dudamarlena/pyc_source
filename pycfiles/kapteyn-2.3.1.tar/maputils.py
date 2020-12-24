# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/jansky/data/users/breddels/src/kapteyn-sky2/kapteyn/maputils.py
# Compiled at: 2016-03-21 11:25:25
"""
.. highlight:: python
   :linenothreshold: 5

Module maputils 
===============

In the maputils tutorial we show many examples with Python code and 
figures to illustrate the functionality and flexibility of this module.
The documentation below is restricted to the module's classes and methods.

Introduction
------------

One of the goals of the Kapteyn Package is to provide a user/programmer basic
tools to make plots (with WCS annotation) of image data from FITS files.
These tools are based on the functionality of PyFITS and Matplotlib.
The methods from these packages are modified in *maputils* for an optimal
support of inspection and presentation of astronomical image data with
easy to write and usually very short Python scripts. To illustrate
what can be done with this module, we list some steps you need
in the process to create a hard copy of an image from a FITS file:

* Open FITS file on disk or from a remote location (URL)
* Specify in which header data unit the image data is stored
* Specify the data slice for data sets with dimensions > 2
* Specify the order of the image axes
* Set the limits in pixels of both image axes
* Set the sky system in which you want to plot wcs information.

Then for the display:

* Plot the image or a mosaic of images in the correct aspect ratio
* Plot (labeled) contours
* Plot world coordinate labels along the image axes  (basic routines in :mod:`wcsgrat`)
* Plot coordinate graticules (basic routines in :mod:`wcsgrat`)
* Interactively change color map and color limits
* Read the position of features in a map and write these positions in your terminal.
* Resize your plot canvas to get an optimal layout while preserving the aspect ratio.
* Write the result to *png* or *pdf* (or another format from a list)

Of course there are many programs that can do this job some way or the other.
But most probably no program does it exactly the way you want or the program
does too much. Also many applications cannot be extended, at least not as simple
as with the building blocks in :mod:`maputils`.

Module :mod:`maputils` is also very useful as a tool to extract and plot
data slices from data sets with more than two axes. For example it can plot
so called *Position-Velocity* maps from a radio interferometer data cube
with channel maps. It can annotate these plots with the correct WCS annotation using
information about the 'missing' spatial axis.

To facilitate the input of the correct data to open a FITS image,
to specify the right data slice or to set the pixel limits for the
image axes, we implemented also some helper functions.
These functions are primitive (terminal based) but effective. You can
replace them by enhanced versions, perhaps with a graphical user interface.

Here is an example of what you can expect. We have a three dimensional data set
on disk called *ngc6946.fits* with axes RA, DEC and VELO.
The program prompts the user to enter
image properties like data limits, axes and axes order.
The image below is a data slice in RA, DEC at VELO=50.
We changed interactively the color map (keys *page-up/page-down*)
and the color limits (pressing right mouse button while moving the mouse) and saved
a hard copy on disk.

In the next code we use keyword parameter *promptfie* a number of times.
Abbreviation 'fie' stands for *Function Interactive Environment*.

.. literalinclude:: EXAMPLES/mu_introduction.py
   
.. image:: EXAMPLES/mu_introduction.png
   :width: 700
   :align: center
   
   
.. centered:: Image from FITS file with graticules and WCS labels

Module level data
-----------------

:data:`cmlist`
   Object from class Colmaplist which has attribute *colormaps* which
   is a sorted list with names of colormaps. It has attributes:

      * **colormaps** -- List with names of color lookup tables
      
      * **cmap_default** -- Color map set by default to 'jet'

   :Example:

      >>> from kapteyn import maputils
      >>> print maputils.cmlist.colormaps
      >>> cmap = raw_input("Enter name of a colormap: ")
      ['Accent', 'Blues', 'BrBG', 'BuGn', 'BuPu', 'Dark2',
      'GnBu', 'Greens', 'Greys', 'OrRd', 'Oranges', 'PRGn',
      'Paired', 'Pastel1', 'Pastel2', 'PiYG', 'PuBu', 'PuBuGn',
      'PuOr', 'PuRd', 'Purples', 'RdBu', 'RdGy', 'RdPu',
      'RdYlBu', 'RdYlGn', 'Reds', 'Set1', 'Set2', 'Set3',
      'Spectral', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd',
      'autumn', 'binary', 'bone', 'cool', 'copper', 'flag',
      'gist_earth', 'gist_gray', 'gist_heat', 'gist_ncar',
      'gist_rainbow', 'gist_stern', 'gist_yarg', 'gray',
      'hot', 'hsv', 'jet', 'pink', 'prism', 'spectral',
      'spring', 'summer', 'winter']

Prompt functions
----------------

.. index:: Open a FITS file
.. autofunction:: prompt_fitsfile
.. index:: Set axis numbers of FITS image
.. autofunction:: prompt_imageaxes
.. index:: Set pixel limits in FITS image
.. autofunction:: prompt_box
.. index:: Set spectral translation from list
.. autofunction:: prompt_spectrans
.. index:: Set sky system for output
.. autofunction:: prompt_skyout
.. index:: Get clip values for image data
.. autofunction:: prompt_dataminmax

Utility functions
-----------------

.. index:: Convert PyFITS header to Python dictionary
.. autofunction:: fitsheader2dict

.. index:: Calculate distance on sphere
.. autofunction:: dist_on_sphere

.. autofunction:: showall

Class FITSimage
---------------

.. index:: Extract image data from FITS file
.. autoclass:: FITSimage

Class Annotatedimage
---------------------

.. index:: Plot FITS image data with Matplotlib
.. autoclass:: Annotatedimage

Class Image
-----------

.. autoclass:: Image

Class Contours
--------------

.. autoclass:: Contours

Class Colorbar
--------------

.. autoclass:: Colorbar

Class Beam
----------

.. autoclass:: Beam

Class Skypolygon
-----------------

.. autoclass:: Skypolygon

Class Marker
------------

.. autoclass:: Marker

Class Pixellabels
-----------------

.. autoclass:: Pixellabels

Class Colmaplist
----------------

.. autoclass:: Colmaplist

Class FITSaxis
--------------

.. autoclass:: FITSaxis

Class Positionmessage
---------------------

.. autoclass:: Positionmessage

Class MovieContainer
--------------------

.. autoclass:: MovieContainer

Class Cubeatts
---------------

.. autoclass:: Cubeatts

Class Cubes
-----------

.. autoclass:: Cubes

   
"""
__version__ = '1.20'
import locale
locale.setlocale(locale.LC_NUMERIC, 'C')
from matplotlib import rcParams
backend = rcParams['backend'].upper()
try:
    rcParams['savefig.format'] = 'pdf'
except:
    pass

from sys import stdout
from matplotlib import __version__ as mplversion
mploldversion = mplversion < '1.2.0'
from matplotlib.pyplot import setp as plt_setp
from matplotlib.pyplot import figure, show
from matplotlib import cm
from matplotlib.colors import Colormap, Normalize
from matplotlib.colorbar import make_axes, Colorbar, ColorbarBase
from matplotlib.patches import Polygon, Rectangle, Ellipse
from matplotlib.ticker import MultipleLocator, ScalarFormatter, FormatStrFormatter
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.image import AxesImage
from matplotlib.cbook import report_memory
from matplotlib.widgets import Cursor
import matplotlib.axes as axesclass
if mploldversion:
    import matplotlib.nxutils as nxutils
else:
    import matplotlib.path as path
try:
    import pyfits
    pyfitsversion = pyfits.__version__
    pyfitsoldversion = pyfitsversion < '3.1.0'
except:
    from astropy import __version__ as astropyversion
    import astropy.io.fits as pyfits
    pyfitsoldversion = False
    pyfitsversion = 'Astropy %s' % astropyversion

import numpy
from kapteyn import wcs, wcsgrat
from kapteyn.celestial import skyrefsystems, epochs, skyparser, lon2hms, lat2dms, lon2dms
from kapteyn.tabarray import tabarray, readColumns
from kapteyn.mplutil import AxesCallback, CanvasCallback, VariableColormap, TimeCallback, KeyPressFilter
from kapteyn.positions import str2pos, mysplit, unitfactor
from kapteyn.interpolation import map_coordinates
from kapteyn.filters import gaussian_filter
from kapteyn import rulers
import readline
from gc import collect as garbagecollect
import six
from string import ascii_letters as letters
from random import choice
from re import split as re_split
from datetime import datetime
import warnings, time
from os import getpid as os_getpid
from os import remove, getcwd
from os.path import basename as os_basename
from subprocess import Popen, PIPE, check_call, CalledProcessError
from platform import system as os_system
try:
    from gipsy import anyout, typecli
    gipsymod = True
except:
    gipsymod = False

KeyPressFilter.allowed = [
 'f', 'g']
left, bottom, right, top = (
 wcsgrat.left, wcsgrat.bottom, wcsgrat.right, wcsgrat.top)
native, notnative, bothticks, noticks = (wcsgrat.native, wcsgrat.notnative, wcsgrat.bothticks, wcsgrat.noticks)
annotatedimage_list = []
nonefunc = lambda x: None
backgroundchanged = False
MINBOUND = 0.005
MAXBOUND = 0.995
from matplotlib.backend_bases import NavigationToolbar2
NavigationToolbar2.ext_callback = None
NavigationToolbar2.ext_callback2 = None

def resetframe(self, event):
    if self.ext_callback2:
        self.ext_callback2()
    if self.ext_callback:
        self.ext_callback()


oldzoom = NavigationToolbar2.release_zoom

def newzoom(self, event):
    oldzoom(self, event)
    resetframe(self, event)


NavigationToolbar2.release_zoom = newzoom
oldpan = NavigationToolbar2.release_pan

def newpan(self, event):
    oldpan(self, event)
    resetframe(self, event)


NavigationToolbar2.release_pan = newpan
old_update_view = NavigationToolbar2._update_view

def new_update_view(self):
    try:
        old_update_view(self)
    except:
        pass

    resetframe(self, None)
    return


NavigationToolbar2._update_view = new_update_view
from matplotlib.figure import Figure
Figure.ext_callback = None
old_subplots_adjust = Figure.subplots_adjust

def new_subplots_adjust(self, *args, **kwargs):
    old_subplots_adjust(self, *args, **kwargs)
    if self.ext_callback:
        self.ext_callback()


Figure.subplots_adjust = new_subplots_adjust

def getmemory():
    pid = os_getpid()
    system = os_system()
    garbagecollect()
    if system.lower().startswith('linux'):
        a = Popen('ps -p %d -o sz,rss' % pid, shell=True, stdout=PIPE).stdout.readlines()
        mem = int(a[1].split()[1])
        mem /= 1024
        mem = 'Resident mem.: ' + str(mem) + ' MB '
    else:
        mem = report_memory()
        mem = 'Mem. pages: ' + str(mem)
    return mem


def nint(x):
    return numpy.floor(x + 0.5)


def flushprint(s):
    print s
    stdout.flush()


def showall():
    """
   Usually in a script with only one object of class
   :class:`maputils.Annotatedimage` one plots this object,
   and its derived objects, with method :meth:`maputils.Annotatedimage.plot`.
   Matplotlib must be instructed to do the real plotting with
   pyplot's function *show()*. This function does this all.

   :Examples:

   
      >>> im1 = f1.Annotatedimage(frame1)
      >>> im1.Image()
      >>> im1.Graticule()
      >>> im2 = f2.Annotatedimage(frame2)
      >>> im2.Image()
      >>> maputils.showall()
      
   """
    for ai in annotatedimage_list:
        ai.plot()

    show()


def issequence(obj):
    return isinstance(obj, (list, tuple, numpy.ndarray))


def getfilename(pre='mu', post='fits'):
    d = datetime.now()
    stamp = d.strftime('%Y%m%d_%Hh%Mm%Ss')
    filename = '%s%s%d.%s' % (pre, stamp, d.microsecond, post)
    return filename


def randomlabel(base=''):
    chars = letters
    label = base
    for i in range(8):
        label = label + choice(chars)

    return label


def get_splitlon(projection):
    """
   Assumed is a two dimensional map with two spatial axes.
   The projection is extracted from the ctype of the first axis.
   Then a decision is made whether we have a border in an all sky plot in
   longitude or not.
   """
    if projection.category not in ('undefined', 'zenithal'):
        splitlon = projection.crval[0] + 180.0
        if splitlon >= 360.0:
            splitlon -= 360.0
        if splitlon <= -360.0:
            splitlon += 360.0
    else:
        splitlon = None
    return splitlon


def getnumbers(prompt):
    """
   Given a series of expressions all representing numbers, return a list
   with the evaluated numbers. An expression that could not be evaluated
   is skipped without a warning. Mathematical functions can be used
   from NumPy and should be entered e.g. as *numpy.sin(numpy.pi)*
   """
    xstr = input(prompt)
    xsplit = mysplit(xstr)
    X = []
    for x in xsplit:
        try:
            xlist = eval(x)
            if issequence(xlist):
                for xx in xlist:
                    X.append(xx)

            else:
                X.append(eval(x))
        except:
            pass

    return X


def getscale(hdr):
    bscale = None
    bzero = None
    blank = None
    bitpix = None
    if 'BITPIX' in hdr:
        bitpix = hdr['BITPIX']
    if 'BSCALE' in hdr:
        bscale = hdr['BSCALE']
    if 'BZERO' in hdr:
        bzero = hdr['BZERO']
    if 'BLANK' in hdr:
        blank = hdr['BLANK']
    return (
     bitpix, bzero, bscale, blank)


def dist_on_sphere(l1, b1, l2, b2):
    """
Formula for distance on sphere accurate over entire sphere
(Vincenty, Thaddeus, 1975). Input and output are in degrees.

:param l1:
   Longitude of first location on sphere
:type l1:
   float
:param b1:
   Latitude of first location on sphere
:type b1:
   float
:param l2:
   Longitude of second location on sphere
:type l2:
   float
:param b2:
   Latitude of second location on sphere
:type b2:
   float

:Examples:

   >>> from kapteyn.maputils import dist_on_sphere
   >>> print dist_on_sphere(0,0, 20,0)
       20.0

   >>> print dist_on_sphere(0,30, 20,30)
       17.2983302106

   """
    fac = numpy.pi / 180.0
    l1 *= fac
    b1 *= fac
    l2 *= fac
    b2 *= fac
    dlon = l2 - l1
    aa1 = numpy.cos(b2) * numpy.sin(dlon)
    aa2 = numpy.cos(b1) * numpy.sin(b2) - numpy.sin(b1) * numpy.cos(b2) * numpy.cos(dlon)
    a = numpy.sqrt(aa1 * aa1 + aa2 * aa2)
    b = numpy.sin(b1) * numpy.sin(b2) + numpy.cos(b1) * numpy.cos(b2) * numpy.cos(dlon)
    d = numpy.arctan2(a, b)
    return d * 180.0 / numpy.pi


def dispcoord(longitude, latitude, disp, direction, angle):
    """
   INPUT:   longitude: numpy array, enter in degrees.
            latitude:  numpy array, enter in degrees.
            disp:      the displacement in the sky entered
                       in degrees. The value can also be
                       negative to indicate the opposite
                       direction
            angle:     the angle wrt. a great circle of
                       constant declination entered in
                       degrees.
            direction: If the longitude increases in the -X
                       direction (e.q. RA-DEC) then direction
                       is -1. else direction = +1

   Assume a triangle on a sphere with side b(=disp) connec-
   ting two positions along a great circle and sides 90-d1,
   and 90-d2 (d1, d2 are the declinations of the input and
   output positions) that connect the input and output
   position to the pole P of the sphere. Then the distance
   between the two points Q1=(a1,d1) and Q2=(a2,d2) is:
   cos(b)=cos(90-d1)cos(90-d2)+sin(90-d1)sin(90-d2)cos(a2-a1)
   Q2 is situated to the left of Q1.
   If the angle PQ1Q2 is alpha then we have another cosine
   rule:
   cos(90-d2) = cos(b)cos(90-d1)+sin(b)sin(90-d1)cos(alpha)
   or:
   sin(d2) = cos(b)sin(d1)+sin(b)cos(d1)cos(alpha)
   which gives d2. Angle Q1PQ2 is equal to a2-a1. For this
   angle we have the sine formula:
   sin(b)/sin(a2-a1) = sin(90-d2)/sin(alpha) so that:
   sin(a2-a1) = sin(b)sin(alpha)/cos(d2).
   b,alpha and d2 are known -> a2.
   """
    Pi = numpy.pi
    b = abs(disp * Pi / 180.0)
    a1 = longitude * Pi / 180.0
    d1 = latitude * Pi / 180.0
    alpha = angle * Pi / 180.0
    d2 = numpy.arcsin(numpy.cos(b) * numpy.sin(d1) + numpy.cos(d1) * numpy.sin(b) * numpy.cos(alpha))
    cosa2a1 = (numpy.cos(b) - numpy.sin(d1) * numpy.sin(d2)) / (numpy.cos(d1) * numpy.cos(d2))
    sina2a1 = numpy.sin(b) * numpy.sin(alpha) / numpy.cos(d2)
    dH = numpy.arctan2(direction * sina2a1, cosa2a1)
    a2 = a1 - dH
    lonout = a2 * 180.0 / Pi
    latout = d2 * 180.0 / Pi
    return (
     lonout, latout)


def split_polygons(plons, plats, splitlon):
    """
   Given a set coordinates which form a polygon,
   we need to return a list of polygons. The polygons
   that should be distinghuised are those on one side
   of a split meridian (splitlon) and those on the other side.

   We need this if polygons are plotted near the edges
   (in longitudes) of allsky plots with cylindrical
   (at least: non-zenithal) projections.
   Then we need to split up the polygon. But this polygon
   can be complicated. For example it is possible that
   the polygon must be splitted in more than two parts.

   This algorith works only for those polygons that, when
   sliced by 'splitlon' fall apart in two pieces.

   Returns:

   lon1, lat1, lon2, lat2
   The longitudes and latitudes of first and second object.
   The lists could be empty if the polygon is contained in the
   range splitlon+epsilon to splitlon-epsilon

   Intersections:
   
   Line through: (a1,d1), (a2,d2). At which d3 is a3?
   lambda = (a3-a1)/(a2-a1). Then when a = a3 -->
   d3 = d1 + lambda *(d2-d1) 
   """
    epsilon = 1e-08
    ilons = []
    ilats = []
    prevlon = None
    prevlat = None
    lons = list(plons)
    lons.append(lons[0])
    lats = list(plats)
    lats.append(lats[0])
    lon1 = []
    lat1 = []
    lon2 = []
    lat2 = []
    right2left = False
    left2right = False
    lastlat = None
    changedborder = 0
    intersectlon = [None, None]
    intersectlat = [None, None]
    for lon, lat in zip(lons, lats):
        if prevlon is not None:
            crossed = False
            if prevlon < splitlon:
                lon1.append(prevlon)
                lat1.append(prevlat)
                eps = -epsilon
                if lon > splitlon:
                    crossed = True
            else:
                lon2.append(prevlon)
                lat2.append(prevlat)
                eps = epsilon
                if lon <= splitlon:
                    crossed = True
            if crossed:
                if prevlon == lon:
                    d3 = prevlat
                else:
                    Lambda = (splitlon - prevlon) / (lon - prevlon)
                    d3 = prevlat + Lambda * (lat - prevlat)
                    intersectlon[changedborder] = splitlon + eps
                    intersectlat[changedborder] = d3
                    changedborder += 1
            if changedborder == 2:
                dlats = numpy.linspace(0, 1, 20)
                for dlat in dlats:
                    if eps > 0.0:
                        ds = intersectlat[0]
                        de = intersectlat[1]
                    else:
                        ds = intersectlat[1]
                        de = intersectlat[0]
                    d = ds + dlat * (de - ds)
                    lon1.append(splitlon - epsilon)
                    lat1.append(d)
                    d = de + dlat * (ds - de)
                    lon2.append(splitlon + epsilon)
                    lat2.append(d)

                changedborder = 0
        prevlon = lon
        prevlat = lat

    return (
     lon1, lat1, lon2, lat2)


def change_header(hdr, **kwargs):
    """
   Given header 'hdr', change/add or delete all keys
   given in **kwargs. Input 'hdr' is either a Python
   dictionary or a PyFITS header object.
   """
    if type(hdr) == 'dict':
        dicttype = True
    else:
        dicttype = False
    for name in list(kwargs.keys()):
        value = kwargs[name]
        fitsname = name.upper()
        if value is None:
            try:
                del hdr[fitsname]
            except KeyError:
                pass

        elif dicttype:
            hdr[fitsname] = value
        else:
            hdr.update(fitsname, value)

    return


def colornavigation_info():
    """
   This function compiles and returns a help text for
   color map interaction.
   """
    helptext = 'pgUp and pgDown: browse through colour maps -- MB right: Change slope and offset\n'
    helptext += 'Colour scales: 0=reset 1=linear 2=logarithmic'
    helptext += '3=exponential 4=square-root 5=square 9=inverse\n'
    helptext += 'h: Toggle histogram equalization & raw image -- '
    helptext += 'z: Toggle smooth & raw image -- x: Increase smooth factor\n'
    helptext += 'm: Save current colour map to disk -- '
    helptext += 'b: Change colour of bad pixels -- '
    helptext += 'Shift MB left: Write pos. to term.'
    return helptext


class Positionmessage(object):
    """
This class creates an object with attributes that are needed to
set a proper message with information about a position
in a map and its corresponding image value.
The world coordinates are calculated in the sky system
of the image. This system could have been changed by the user.

The input parameters are usually set after initialization of
an object from class :class:`Annotatedimage`.
For users/programmers the atributes are more important.
With the attributes of objects of this class we can change
the format of the numbers in the informative message.

Note that the methods of this class return separate strings
for the pixel coordinates, the world coordinates and the image
values. The final string is composed in the calling environment.

:param skysys:
   The sky definition of the current image
:type skysys:
   A single parameter or tuple with integers or string
:param skyout:
   The sky definition of the current image as defined by
   a user/programmer
:type skyout:
   A single parameter or tuple with integers or string
:param skysys:
   The sky definition of the current image
:type axtype:
   tuple with strings

:Attributes:

   .. attribute:: pixfmt

         Python number format to set formatting of pixel
         coordinates in position message in toolbar.

   .. attribute:: wcsfmt

         Python number format to set formatting of world
         coordinates in position message in toolbar.
         If the map has a valid sky system then the
         values will be formatted in hms/dms, unless
         attribute *hmsdms* is set to *False*.

   .. attribute:: zfmt

         Python number format to set formatting of image
         value(s) in position message in toolbar.

   .. attribute:: hmsdms

         If True, spatial coordinates are formatted in hms/dms.

   .. attribute:: dmsprec

         Precision in (dms) seconds if coordinate is
         formatted in dms. The precision in seconds of a
         longitude axis in an equatorial system is
         automatically copied from this number and increased
         with 1.
   """

    def __init__(self, skysys, skyout, axtype):
        self.pixfmt = '%.1f'
        self.wcsfmt = '%.3g'
        self.wcsuffmt = '%.7f'
        self.zfmt = '%.3e'
        self.hmsdms = True
        self.dmsprec = 1
        sys = None
        if skyout is None:
            if skysys is not None:
                sys, ref, equinox, epoch = skyparser(skysys)
        else:
            sys, ref, equinox, epoch = skyparser(skyout)
        self.sys = sys
        self.axtype = axtype
        return

    def z2str(self, z):
        if self.zfmt is None:
            return
        else:
            if issequence(z):
                if len(z) != 3:
                    raise Exception('z2str: Toolbar Message expects 1 or 3 image values')
                else:
                    s = ''
                    for number in z:
                        if numpy.isnan(number):
                            s += 'NaN'
                        else:
                            s += self.zfmt % number + ' '

                    return s.rstrip()
            else:
                if numpy.isnan(z):
                    s = 'NaN'
                else:
                    s = self.zfmt % z
                return s
            return

    def pix2str(self, x, y):
        if self.pixfmt is None:
            return
        else:
            s = self.pixfmt % x + ' ' + self.pixfmt % y
            return s

    def wcs2str(self, xw, yw, missingspatial, returnlist=False, unformatted=False):
        if not self.wcsfmt and not unformatted:
            return
        else:
            if unformatted and self.wcsuffmt is None:
                return
            vals = (
             xw, yw)
            if missingspatial is not None:
                vals += (missingspatial,)
            if returnlist:
                s = []
            else:
                s = ''
            if unformatted:
                wcsfmt = self.wcsuffmt
            else:
                wcsfmt = self.wcsfmt
            for atyp, val in zip(self.axtype, vals):
                if val is None:
                    coord = 'NaN'
                elif self.hmsdms and not unformatted:
                    if atyp == 'longitude':
                        if self.sys == wcs.equatorial:
                            coord = lon2hms(val, prec=self.dmsprec + 1)
                        else:
                            coord = lon2dms(val, prec=self.dmsprec)
                    elif atyp == 'latitude':
                        coord = lat2dms(val, prec=self.dmsprec)
                    else:
                        coord = wcsfmt % val
                else:
                    coord = wcsfmt % val
                if returnlist:
                    s.append(coord)
                else:
                    s += coord + ' '

            return s


class Colmaplist(object):
    """
   This class provides an object which stores
   the names of all available colormaps.
   The method *add()* adds external colormaps to
   this list. The class is used in the context of
   other classes but its attribute *colormaps*
   can be useful.

   :param -: No parameters
   
   :Attributes:
   
      .. attribute:: colormaps

         List with names of colormaps as used in combination
         with keyword parameter *cmap* in the constructor
         of :class:`Annotatedimage`.
         Note that currently we use a module level object
         ``cmlist`` which has all the information, so we
         don't use class variable ``colormaps``.
         Only when we created a list with color maps with object ``cmlist``, this 
         variable has a value. Then both of the next statements are equivalent:
         
         >>> print maputils.Colmaplist.colormaps
         >>> print maputils.cmlist.colormaps
            
   """
    colormaps = []

    def compare_key(self, a):
        return a.lower()

    def __init__(self):
        self.colormaps = [ m for m in list(cm.datad.keys()) if not m.endswith('_r') ]
        self.colormaps.sort(key=self.compare_key)
        Colmaplist.colormaps = self.colormaps
        self.cmap_default = 'jet'

    def add(self, clist):
        if not issequence(clist):
            clist = [
             clist]
        self.colormaps += clist
        self.colormaps.sort(key=self.compare_key)

    def addfavorites(self, flist):
        if not issequence(flist):
            flist = [
             flist]
        newlist = flist + self.colormaps
        self.colormaps = flist + self.colormaps


cmlist = Colmaplist()
cmlist.add(VariableColormap.luts())

def cmp_to_key(mycmp):
    """Convert a cmp= function into a key= function"""

    class K:

        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


def fitsheader2dict(header, comment=True, history=True):
    """
Transform a FITS header (read with PyFITS) into a Python
dictionary.
This is useful if one wants to iterate over all keys in the
header. The PyFITS header is not iterable.
   """

    class fitsdict(dict):
        pass

    result = fitsdict()
    result.comment = {}
    if isinstance(header, dict):
        for key in header:
            result[key] = header[key]
            try:
                result.comment[key] = header.comment[key]
            except:
                result.comment[key] = ''

    else:
        if pyfitsoldversion:
            cardset = header.ascard
        else:
            cardset = header.cards
        for card in cardset:
            try:
                if pyfitsoldversion:
                    key = card.key
                else:
                    key = card.keyword
                if history and key == 'HISTORY' or comment and key == 'COMMENT':
                    try:
                        result[key].append(card.value)
                    except KeyError:
                        result[key] = [
                         card.value]

                else:
                    result[key] = header[key]
                    result.comment[key] = card.comment
            except:
                card.verify()

    return result


def prompt_box(pxlim, pylim, axnameX, axnameY):
    """
External helper function which returns the
limits in pixels of the x- and y-axis.
The input syntax is: xlo,xhi, ylo,yhi. For *x* and *y*
the names of the image axes are substituted.
Numbers can be separated by comma's and or
spaces. A number can also be specified
with an expression e.g. ``0, 10,  10/3, 100*numpy.pi``.
All these numbers are converted to integers.

:param pxlim:
   Sequence of two numbers representing limits
   in pixels along the x axis as defined in the FITS file.
:type pxlim:
   tuple with two integers
:param pylim:
   Sequence of two numbers representing limits
   in pixels along the y axis as defined in the FITS file.
:type pylim:
   tuple with two integers
:param axnameX:
   Name of image X-axis
:type axnameX:
   String
:param axnameY:
   Name of image Y-axis
:type axnameY:
   String

:Prompts:
   *Enter pixel limits in Xlo,Xhi,  Ylo,Yhi ..... [xlo,xhi, ylo,yhi]:*

   The default should be the axis limits as defined in the FITS header
   in keywords *NAXISn*.
   In a real case this could look like:
   
   *Enter pixel limits in RAlo,RAhi,  DEClo,DEChi ..... [1, 100, 1, 100]:*

:Returns:
   Tuple with two elements
   pxlim, pylim (see parameter description)

:Notes:
   This function does not check if the limits are
   within the index range of the (FITS)image.
   This check is done in the :meth:`FITSimage.set_limits` method
   of the :class:`FITSimage` class.

:Examples:
   Use of this function as prompt function in the
   :meth:`FITSimage.set_limits` method::
   
      fitsobject = maputils.FITSimage('rense.fits')
      fitsobject.set_imageaxes(1,2, slicepos=30) # Define image in cube
      fitsobject.set_limits(promptfie=maputils.prompt_box)
   
   This 'box' prompt needs four numbers. The first is the range in 
   x and the second is the range in y. The input are pixel coordinates,
   e.g.::
   
       >>>  0, 10   10/3, 100*numpy.pi

   Note the mixed use of spaces and comma's to
   separate the numbers. Note also the use of
   NumPy for mathematical functions. The numbers are truncated to integers.
   """
    boxtxt = '%slo,%shi,  %slo,%shi' % (axnameX, axnameX, axnameY, axnameY)
    while True:
        try:
            s = 'Enter pixel limits in %s ..... [%d, %d, %d, %d]: ' % (boxtxt, pxlim[0], pxlim[1], pylim[0], pylim[1])
            box = input(s)
            if box != '':
                lims = re_split('[, ]+', box.strip())
                xlo = int(eval(lims[0]))
                xhi = int(eval(lims[1]))
                ylo = int(eval(lims[2]))
                yhi = int(eval(lims[3]))
                readline.add_history(box)
                ok = pxlim[0] <= xlo <= pxlim[1] and pxlim[0] <= xhi <= pxlim[1] and pylim[0] <= ylo <= pylim[1] and pylim[0] <= ylo <= pylim[1]
                if not ok:
                    print 'One of the values is outside the pixel limits'
                else:
                    break
            else:
                return (
                 pxlim, pylim)
        except KeyboardInterrupt:
            raise
        except:
            print 'Wrong box'

    return (
     (
      xlo, xhi), (ylo, yhi))


def prompt_fitsfile(defaultfile=None, prompt=True, hnr=None, alter=None, memmap=None):
    """
An external helper function for the FITSimage class to
prompt a user to open the right Header and Data Unit (hdu)
of a FITS file.
A programmer can supply his/her own function
of which the return value is a sequence containing 
the hdu list, the header unit number, the filename and a character for 
the alternate header.
   
:param defaultfile:
   Name of FITS file on disk or url of FITS file on the internet.
   The syntax follows the standard described in the PyFITS documentation.
   See also the examples.
:type defaultfile:
   String
:param prompt:
   If False and a default file exists, then do not prompt for a file name.
   Open file and start checking HDU's
:type prompt:
   Boolean
:param hnr:
   The number of the FITS header that you want to use.
   This function lists the hdu information and when
   hnr is not given, you will be prompted.
:type hnr:
   Integer
:param alter:
   Selects an alternate header. Default is the standard header.
   Keywords in alternate headers end on a character A..Z
:type alter:
   Empty or a single character. Input is case insensitive.
:param memmap:
   Set PyFITS memory mapping on/off. Let PyFITS set the default.
:type memmap:
   Boolean

:Prompts:
   1. *Enter name of fits file ...... [a default]:*

      Enter name of file on disk of valid url.
   2. *Enter number of Header Data Unit ...... [0]:*

      If a FITS file has more than one HDU, one must decide
      which HDU contains the required image data.
      
:Returns:

   * *hdulist* - The HDU list and the user selected index of the wanted 
     hdu from that list. The HDU list is returned so that it
     can be closed in the calling environment.
   * *hnr* - FITS header number. Usually the first header, i.e. *hnr=0*
   * *fitsname* - Name of the FITS file.
   * *alter* - A character that corresponds to an alternate header
     (with alternate WCS information e.g. a spectral translation).
     
:Notes:
   --
   
:Examples:  
   Besides file names of files on disk, PyFITS allows url's and gzipped 
   files to retrieve FITS files e.g.::
   
      http://www.atnf.csiro.au/people/mcalabre/data/WCS/1904-66_ZPN.fits.gz
      
   """
    while True:
        try:
            if defaultfile is None:
                filename = ''
                s = 'Enter name of FITS file: '
            else:
                filename = defaultfile
                s = 'Enter name of FITS file ...... [%s]: ' % filename
            if defaultfile is None or prompt:
                fn = input(s)
            else:
                fn = filename
            if fn != '':
                filename = fn
            hdulist = pyfits.open(filename, memmap=memmap)
            break
        except IOError as xxx_todo_changeme1:
            errno, strerror = xxx_todo_changeme1.args
            print 'I/O error(%s): %s opening [%s]' % (errno, strerror, filename)
            prompt = True
        except KeyboardInterrupt:
            raise
        except:
            defaultfile = None
            print 'Cannot open file, unknown error.'
            con = input('Abort? ........... [Y]/N:')
            if con == '' or con.upper() == 'Y':
                raise Exception('Loop aborted by user')

    hdulist.info()
    if hnr is None:
        n = len(hdulist)
        if n > 1:
            while True:
                p = input('Enter number of Header Data Unit ... [0]:')
                if p == '':
                    hnr = 0
                    break
                else:
                    try:
                        p = int(p)
                    except:
                        pass

                    try:
                        k = hdulist[p]
                        hnr = p
                        break
                    except:
                        pass

        else:
            hnr = 0
    if alter == '':
        alternates = []
        hdr = hdulist[hnr].header
        for a in letters[:26]:
            k = 'CRPIX1%c' % a.upper()
            if k in hdr:
                print (
                 'Found alternate header:', a.upper())
                alternates.append(a)

        if len(alternates):
            while True:
                p = input('Enter char. for alternate header ... [No alt. header]:')
                if p == '':
                    alter = ''
                    break
                elif p.upper() in alternates:
                    alter = p.upper()
                    break
                else:
                    print 'Character not in list with allowed alternates!'

    return (
     hdulist, hnr, filename, alter)


def prompt_imageaxes(fitsobj, axnum1=None, axnum2=None, slicepos=None):
    """
Helper function for FITSimage class. It is a function that requires
interaction with a user. Therefore we left it out of any class
definition. so that it can be replaced by any other function that
returns the position of the data slice in a FITS file.

It prompts the user
for the names of the axes of the wanted image. For a
2D FITS data set there is nothing to ask, but for
dimensions > 2, we should prompt the user to enter two
image axes. Then also a list with pixel positions should
be returned. These positions set the position of the data
slice on the axes that do not belong to the image.
Only with this information the right slice can be extracted.

The user is prompted in a loop until a correct input is given.
If a spectral axis is part of the selected image then
a second prompt is prepared for the input of the required spectral
translation.

:param fitsobj:
   An object from class FITSimage. This prompt function derives useful
   attributes from this object such as the allowed spectral
   translations.
:type fitsobj:
   Instance of class FITSimage
:param axnum1:
   The axis number of the first (horizontal in terms of plot software)
   axis of the selected image which should be used as the default
   in the prompt. If *None* then the default is set to 1.
:type axnum1:
   Integer [1, NAXIS]
:param axnum2:
   The axis number of the first (horizontal in terms of plot software)
   axis of the selected image which should be used as the default
   in the prompt. If *None* then the default is set to 1.
   If both *axnum1* and *axnum2* are specified then the image
   axis input prompt is skipped.
:type axnum2:
   Integer [1, NAXIS]

:Prompts:
      Name of the image axes:
        *Enter 2 axes from (list with allowed axis names) .... [default]:*

        e.g.: ``Enter 2 axes from (RA,DEC,VELO) .... [RA,DEC]:``

        The axis names can be abbreviated. A minimal match is applied.

   
:Returns:
   Tuple with three elements:
   
   * *axnum1*:
     Axis number of first image axis. Default or entered by a user.
   * *axnum2*:
     Axis number of second image axis. Default or entered by a user.
   * *slicepos*:
     A list with pixel positions. One pixel for each axis
     outside the image in the same order as the axes in the FITS
     header. These pixel positions are necessary
     to extract the right 2D data from FITS data with dimensions > 2.

:Example:
   Interactively set the axes of an image using a prompt function::
   
      # Create a maputils FITSimage object from a FITS file on disk
      fitsobject = maputils.FITSimage('rense.fits')
      fitsobject.set_imageaxes(promptfie=maputils.prompt_imageaxes)
   
   """
    n = fitsobj.naxis
    if axnum1 is None or axnum2 is None:
        a1 = axnum1
        a2 = axnum2
        ax1 = a1
        ax2 = a2
        unvalid = True
        axnamelist = '('
        for i in range(1, n + 1):
            axnamelist += fitsobj.axisinfo[i].axname
            if i < n:
                axnamelist += ','

        axnamelist += ')'
        while unvalid:
            if axnum1 is None:
                a1 = 1
                ax1 = -1
            if axnum2 is None:
                a2 = 2
                ax2 = -1
            deflt = '%s,%s' % (fitsobj.axisinfo[a1].axname, fitsobj.axisinfo[a2].axname)
            mes = 'Enter 2 axes from %s .... [%s]: ' % (axnamelist, deflt)
            str1 = input(mes)
            if str1 == '':
                str1 = deflt
            axes = re_split('[, ]+', str1.strip())
            if len(axes) == 2:
                for i in range(n):
                    ax = i + 1
                    str2 = fitsobj.axisinfo[ax].axname
                    if str2.find(axes[0].upper(), 0, len(axes[0])) > -1:
                        ax1 = ax
                    if str2.find(axes[1].upper(), 0, len(axes[1])) > -1:
                        ax2 = ax

                unvalid = not (ax1 >= 1 and ax1 <= n and ax2 >= 1 and ax2 <= n and ax1 != ax2)
                if unvalid:
                    print 'Incorrect input of image axes!'
                if ax1 == ax2 and ax1 != -1:
                    print 'axis 1 == axis 2'
            else:
                print 'Number of images axes must be 2. You entered %d' % (len(axes),)

        print (
         'You selected: ', fitsobj.axisinfo[ax1].axname, fitsobj.axisinfo[ax2].axname)
        axnum1 = ax1
        axnum2 = ax2
    axperm = [
     axnum1, axnum2]
    if slicepos is None:
        slicepos = []
        if n > 2:
            for i in range(n):
                axnr = i + 1
                maxn = fitsobj.axisinfo[axnr].axlen
                if axnr not in [axnum1, axnum2]:
                    unvalid = True
                    while unvalid:
                        crpix = fitsobj.axisinfo[axnr].crpix
                        if crpix < 1 or crpix > fitsobj.axisinfo[axnr].axlen:
                            crpix = 1
                        prompt = 'Enter pixel position between 1 and %d on %s ..... [%d]: ' % (maxn, fitsobj.axisinfo[axnr].axname, crpix)
                        x = input(prompt)
                        if x == '':
                            x = int(crpix)
                        else:
                            x = int(eval(x))
                        unvalid = not (x >= 1 and x <= maxn)
                        if unvalid:
                            print 'Pixel position not in range 1 to %d! Try again.' % maxn

                    slicepos.append(x)

    return (
     axnum1, axnum2, slicepos)


def prompt_spectrans(fitsobj):
    """
Ask user to enter spectral translation if one of the axes is spectral.

:param fitsobj:
   An object from class FITSimage. From this object we derive the allowed spectral
   translations.
:type fitsobj:
   Instance of class FITSimage

:Prompts:

      The spectral translation if one of the image axes is a spectral axis.
   
         *Enter number between 0 and N of spectral translation .... [native]:*

         *N* is the number of allowed translations  minus 1.
         The default *Native* in this context implies that no translation is applied.
         All calculations are done in the spectral type given by FITS header
         item *CTYPEn* where *n* is the number of the spectral axis.

:Returns: 
   * *spectrans* - The selected spectral translation from a list with spectral
     translations that are allowed for the input object of class FITSimage.
     A spectral translation translates for example frequencies to velocities.

:Example:

   >>> fitsobject = maputils.FITSimage(promptfie=maputils.prompt_fitsfile)
   >>> print fitsobject.str_spectrans()    # Print a list with options first
   >>> fitsobject.set_spectrans(promptfie=maputils.prompt_spectrans)
   """
    asktrans = False
    for ax in fitsobj.axperm:
        if fitsobj.axisinfo[ax].wcstype == 'spectral':
            asktrans = True

    spectrans = None
    nt = len(fitsobj.allowedtrans)
    if nt > 0 and asktrans:
        s = ''
        for i, tr in enumerate(fitsobj.allowedtrans):
            s += '%d:%s (%s) ' % (i, tr[0], tr[1])

        print s
        unvalid = True
        while unvalid:
            try:
                prompt = 'Enter number between 0 and %d of spectral translation .... [native]: ' % (nt - 1)
                st = input(prompt)
                if st != '':
                    st = int(st)
                    unvalid = st < 0 or st > nt - 1
                    if unvalid:
                        print 'Not a valid number!'
                    else:
                        spectrans = fitsobj.allowedtrans[st][0]
                else:
                    unvalid = False
            except KeyboardInterrupt:
                raise
            except:
                unvalid = True

    return spectrans


def prompt_skyout(fitsobj):
    """
Ask user to enter the output sky system if the data is a spatial map.

:param fitsobj:
   An object from class FITSimage. This prompt function uses this object to
   get information about the axis numbers of the spatial axes in a
   data structure.
:type fitsobj:
   Instance of class FITSimage

:Returns:
   * *skyout* - The sky definition to which positions in the native system
      will be transformed.

:Example:

   >>> fitsobject = maputils.FITSimage(promptfie=maputils.prompt_fitsfile)
   >>> fitsobject.set_skyout(promptfie=maputils.prompt_skyout)
   """
    spatials = [
     fitsobj.proj.lonaxnum, fitsobj.proj.lataxnum]
    spatialmap = fitsobj.axperm[0] in spatials and fitsobj.axperm[1] in spatials
    if not spatialmap:
        return
    else:
        skyout = skysys = refsys = equinox = epoch = None
        unvalid = True
        maxskysys = 4
        while unvalid:
            try:
                prompt = 'Sky system 0=eq, 1=ecl, 2=gal, 3=sup.gal .... [native]: '
                st = input(prompt)
                if st != '':
                    st = int(st)
                    unvalid = st < 0 or st >= maxskysys
                    if unvalid:
                        print 'Not a valid number!'
                    else:
                        skysys = st
                else:
                    unvalid = False
            except KeyboardInterrupt:
                raise
            except:
                unvalid = True

        if skysys in [wcs.equatorial, wcs.ecliptic]:
            unvalid = True
            maxrefsys = 5
            prompt = 'Ref.sys 0=fk4, 1=fk4_no_e, 2=fk5, 3=icrs, 4=dynj2000 ... [native]: '
            while unvalid:
                try:
                    st = input(prompt)
                    if st != '':
                        st = int(st)
                        unvalid = st < 0 or st >= maxrefsys
                        if unvalid:
                            print 'Not a valid number!'
                        else:
                            refsys = st + maxskysys
                    else:
                        unvalid = False
                except KeyboardInterrupt:
                    raise
                except:
                    unvalid = True

            if refsys in [wcs.fk4, wcs.fk4_no_e, wcs.fk5]:
                prompt = 'Enter equinox (e.g. J2000 or B1983.5) .... [native]: '
                unvalid = True
                while unvalid:
                    try:
                        st = input(prompt)
                        if st != '':
                            B, J, JD = epochs(st)
                            equinox = st
                        unvalid = False
                    except KeyboardInterrupt:
                        raise
                    except:
                        unvalid = True

            if refsys in [wcs.fk4, wcs.fk4_no_e]:
                prompt = 'Enter date of observation (e.g. MJD24034) .... [native]: '
                unvalid = True
                while unvalid:
                    try:
                        st = input(prompt)
                        if st != '':
                            B, J, JD = epochs(st)
                            epoch = st
                        unvalid = False
                    except KeyboardInterrupt:
                        raise
                    except:
                        unvalid = True

        if skysys is None:
            skyout = None
        else:
            skyout = []
            skyout.append(skysys)
            if equinox is not None:
                skyout.append(equinox)
            if refsys is not None:
                skyout.append(refsys)
            if epoch is not None:
                skyout.append(epoch)
            skyout = tuple(skyout)
        return skyout


def prompt_dataminmax(fitsobj):
    """
    Ask user to enter one or two clip values.
    If one clip level is entered then in display routines
    the data below this value will be clipped. If a second level is
    entered, then all data values above this level
    will also be filtered.

   :param fitsobj:
      An object from class FITSimage.
   :type fitsobj:
      Instance of class FITSimage

   :Returns:
      * *clipmin*, *clipmax* - Two values to set limits on the image value
        e.g. for color editing.

   :Example:

      >>> fitsobject = maputils.FITSimage(promptfie=maputils.prompt_fitsfile)
      >>> clipmin, clipmax = maputils.prompt_dataminmax(fitsobject)
      >>> annim = fitsobject.Annotatedimage(frame, clipmin=clipmin, clipmax=clipmax)
   """
    mi, ma = fitsobj.get_dataminmax(box=True)
    mes = 'Enter clip levels      [%g %g]: ' % (mi, ma)
    clips = input(mes)
    if clips:
        clips = re_split('[, ]+', clips.strip())
        if len(clips) == 1:
            clipmin = eval(clips[0])
            clipmax = ma
        else:
            clipmin = eval(clips[0])
            clipmax = eval(clips[1])
    else:
        clipmin = mi
        clipmax = ma
    return (
     clipmin, clipmax)


class Image(object):
    """
   Prepare the FITS- or external image data to be plotted in Matplotlib.
   All parameters are set by method :meth:`Annotatedimage.Image`.
   The keyword arguments are those for Matplotlib's method *imshow()*.
   Two of them are useful in the context of this class. These parameters
   are *visible*, a boolean to set the visibility of the image to on or off,
   and *alpha*, a number between 0 and 1 which sets the transparency of
   the image.

   See also: :meth:`Annotatedimage.Image`

   :Methods:

   .. automethod:: plot
   """

    def __init__(self, imdata, box, cmap, norm, **kwargs):
        self.ptype = 'Image'
        self.box = box
        newkwargs = {'origin': 'lower', 'extent': self.box, 'interpolation': 'nearest'}
        newkwargs.update(kwargs)
        self.kwargs = newkwargs
        self.data = imdata
        self.frame = None
        self.im = None
        self.xyn_mouse = [0.5, 0.5]
        self.cmap = cmap
        self.norm = norm
        return

    def plot(self, frame):
        """
      Plot image object. Usually this is done by method
      :meth:`Annotatedimage.plot` but it can also be used separately.

      """
        if self.data is None:
            raise Exception('Cannot plot image because image data is not available!')
        self.frame = frame
        t = self.frame.figure.transFigure.transform([(0, 0), (1, 1)])
        pixX = abs(t[(0, 0)] - t[(1, 0)])
        zoom = pixX / self.data.shape[1]
        dummy = self.data
        self.im = self.frame.imshow(dummy, cmap=self.cmap, norm=self.norm, aspect=frame.get_aspect(), **self.kwargs)
        self.frame.set_xlim((self.box[0], self.box[1]))
        self.frame.set_ylim((self.box[2], self.box[3]))
        return


class Contours(object):
    """
   Objects from this class calculate and plot contour lines.
   Most of the parameters are set by method
   :meth:`Annotatedimage.Contours`. The others are:

   
   :param filled:
      If True, then first create filled contours and draw
      the contour lines upon these filled contours
   :type filled:
      Boolean
   :param negative:
      Set the line style of the contours that represent negative
      image numbers. The line styles are Matplotlib line styles e.g.:
      [None | 'solid' | 'dashed' | 'dashdot' | 'dotted']
   :type negative:
      String
   :param kwargs:
      Parameters for properties of all contours (e.g. *linewidths*).
      

   :Notes:
      If the line widths of contours are given in the constructor
      (parameter *linewidths*) then these linewidths are copied to the
      line widths in the colorbar (if requested).

   :Methods:

   .. automethod:: plot
   .. automethod:: setp_contour
   .. automethod:: setp_label
   """

    def __init__(self, imdata, box, levels=None, cmap=None, norm=None, filled=False, negative='dashed', **kwargs):
        self.ptype = 'Contour'
        self.box = box
        self.cmap = cmap
        self.norm = norm
        newkwargs = {'origin': 'lower', 'extent': box}
        newkwargs.update(kwargs)
        self.kwargs = newkwargs
        self.data = imdata
        self.clevels = levels
        self.commoncontourkwargs = None
        self.ckwargslist = None
        if self.clevels is not None:
            self.ckwargslist = [
             None] * len(self.clevels)
        self.commonlabelkwargs = None
        self.lkwargslist = None
        if self.clevels is not None:
            self.lkwargslist = [
             None] * len(self.clevels)
        self.labs = None
        self.filled = filled
        if 'colors' in self.kwargs:
            if self.kwargs['colors'] is not None:
                self.cmap = None
        self.negative = negative
        return

    def plot(self, frame):
        """
      Plot contours object. Usually this is done by method
      :meth:`Annotatedimage.plot` but it can also be used separately.
      """
        if self.data is None:
            raise Exception('Cannot plot image because image data is not available!')
        self.frame = frame
        if self.clevels is None:
            if self.filled:
                self.frame.contourf(self.data, cmap=self.cmap, norm=self.norm, **self.kwargs)
            self.CS = self.frame.contour(self.data, cmap=self.cmap, norm=self.norm, **self.kwargs)
            self.clevels = self.CS.levels
        else:
            if not issequence(self.clevels):
                self.clevels = [
                 self.clevels]
            if self.filled:
                self.frame.contourf(self.data, self.clevels, cmap=self.cmap, norm=self.norm, **self.kwargs)
            self.CS = self.frame.contour(self.data, self.clevels, cmap=self.cmap, norm=self.norm, **self.kwargs)
            self.clevels = self.CS.levels
        self.frame.set_xlim((self.box[0], self.box[1]))
        self.frame.set_ylim((self.box[2], self.box[3]))
        if self.commoncontourkwargs is not None:
            for c in self.CS.collections:
                plt_setp(c, **self.commoncontourkwargs)

        if self.ckwargslist is not None:
            for i, kws in enumerate(self.ckwargslist):
                if kws is not None:
                    plt_setp(self.CS.collections[i], **kws)

        if self.negative is not None:
            for i, lev in enumerate(self.CS.levels):
                if lev < 0:
                    plt_setp(self.CS.collections[i], linestyle=self.negative)

        if self.commonlabelkwargs is not None:
            self.labs = self.frame.clabel(self.CS, **self.commonlabelkwargs)
        if self.lkwargslist is not None:
            for i, kws in enumerate(self.lkwargslist):
                if kws is not None:
                    lab = self.frame.clabel(self.CS, [self.clevels[i]], **kws)

        return

    def setp_contour(self, levels=None, **kwargs):
        """
      Set properties for contours either for all contours if *levels*
      is omitted or for specific levels if keyword *levels*
      is set to one or more levels.

      :param levels:
         None or one or more levels from the set of given contour levels
      :type levels:
         None or one or a sequence of numbers

      :Examples:
      
         >>> cont = annim.Contours(levels=range(10000,16000,1000))
         >>> cont.setp_contour(linewidth=1)
         >>> cont.setp_contour(levels=11000, color='g', linewidth=3)
      """
        if levels is None:
            self.commoncontourkwargs = kwargs
        else:
            if self.clevels is None:
                raise Exception('Contour levels not set so I cannot identify contours')
            if not issequence(levels):
                levels = [
                 levels]
            for lev in levels:
                try:
                    i = list(self.clevels).index(lev)
                except ValueError:
                    i = -1

                if i != -1:
                    self.ckwargslist[i] = kwargs

        return

    def setp_label(self, levels=None, tex=True, **kwargs):
        r"""
      Set properties for the labels along the contours.
      The properties are Matplotlib properties (fontsize, colors,
      inline, fmt).

      :param levels:
            None or one or more levels from the set of given contour levels
      :type levels:
            None or one or a sequence of numbers

      :param tex:
         Print the labels in TeX if a format is entered.
         If set to True, add '$' characters
         so that Matplotlib knows that it has to format the label
         in TeX. The default is *True*. 
      :type tex:
         Boolean
      :param xxx:
         Other parameters are Matplotlib parameters for method
         :meth:`clabel` in Matplotlib :class:`ContourLabeler`
         (fontsize, colors, inline, fmt).

      :Examples:

         >>> cont2 = annim.Contours(levels=(8000,9000,10000,11000))
         >>> cont2.setp_label(11000, colors='b', fontsize=14, fmt="%.3f")
         >>> cont2.setp_label(fontsize=10, fmt="%g \lambda")
      """
        if tex and 'fmt' in kwargs:
            kwargs['fmt'] = '$' + kwargs['fmt'] + '$'
        if levels is None:
            self.commonlabelkwargs = kwargs
        else:
            if self.clevels is None:
                raise Exception('Contour levels not set so I cannot identify contours')
            if not issequence(levels):
                levels = [
                 levels]
            for lev in levels:
                try:
                    i = list(self.clevels).index(lev)
                except ValueError:
                    i = -1

                if i != -1:
                    self.lkwargslist[i] = kwargs

        return


class Colorbar(object):
    """
   Colorbar class. Usually the parameters will be provided by method
   :meth:`Annotatedimage.Colorbar`

   Useful keyword parameters:

   :param frame:
      If a frame is given then this frame will be the colorbar frame.
      If None, the frame is calculated by taking space from its parent
      frame.
   :type frame:
      Matplotlib Axes instance

   :Methods:
   
   .. automethod:: plot
   .. automethod:: set_label
   """

    def __init__(self, cmap, frame=None, norm=None, contourset=None, clines=False, fontsize=9, label=None, linewidths=None, visible=True, **kwargs):
        """
      cmap: Was usuable in versions <= 0.99.8. Now we cannot use
            colorbaseBase anymore (changing color map did not update
            the colorbar) and have to use the colorbar method instead.
            Then in fact, either an image or a contourset should be
            supplied and the cmap is not necessary. For now we leave the code
            unaltered. TODO: Address the use of cmap.
      frame: If a frame is entered it will be stored here and used as
            Axes object. However when None, the calling environment
            must call plot() with a valid frame (usually this frame
            will be 'stolen' from a mother frame.
            clines: Draw contour lines in colorbar also. Does not matter
            if this comes from an image or contour set.
      linewidhts: One number to set the line width of all the contour
            lines in the colorbar. Note that linewidths set for a
            contour level will be copied for the line width of the
            line in the colorbar. However if parameter *linewidths*
            is set, it will be applied to all lines in the contour colorbar.
      """
        self.ptype = 'Colorbar'
        self.cmap = cmap
        self.norm = norm
        self.contourset = contourset
        self.plotcontourlines = clines
        self.cbfontsize = fontsize
        self.linewidths = linewidths
        self.frame = frame
        self.label = label
        self.labelkwargs = None
        newkwargs = {'orientation': 'vertical'}
        if not visible:
            alpha = {'alpha': 0.0}
            newkwargs.update(alpha)
        newkwargs.update(kwargs)
        self.kwargs = newkwargs
        return

    def colorbarticks(self):
        """
      Usually used within the context of this class, but can also be used
      if one needs to resize the colorbar tick labels in the calling
      environment.
      """
        for t in self.cb.ax.get_xticklabels():
            t.set_fontsize(self.cbfontsize)

        for t in self.cb.ax.get_yticklabels():
            t.set_fontsize(self.cbfontsize)

    def plot(self, cbframe, mappable=None):
        """
      Plot image object. Usually this is done by method
      :meth:`Annotatedimage.plot` but it can also be used separately.

      Note:
      We changed the default formatter for the colorbar. This can be done with
      the 'format' parameter. We changed the formatter to a fixed format string.
      This prevents that MPL uses an offset and a scaling for the labels.
      If MPL does this, it adds an extra label, showing the offset and scale
      in scientific notation. We do not want this extra label because we don't
      have enough control over it (e.g. it can appear outside your viewport
      or in a black background with a black font). With the new formatter
      we are sure to get the real value in our labels.
      """
        self.frame = cbframe
        fig = cbframe.figure
        majorFormatter = FormatStrFormatter('%g')
        self.cb = fig.colorbar(mappable, cax=self.frame, norm=self.norm, format=majorFormatter, **self.kwargs)
        if self.plotcontourlines and self.contourset is not None:
            CS = self.contourset.CS
            if 'ticks' not in self.kwargs:
                self.kwargs['ticks'] = CS.levels
            lws = []
            if self.linewidths is not None:
                for lw in CS.tlinewidths:
                    lws.append((self.linewidths,))

                CS.tlinewidths = lws
            self.cb.add_lines(CS)
        else:
            CS = None
        self.colorbarticks()
        if self.label is not None:
            if self.labelkwargs is None:
                self.cb.set_label(self.label)
            else:
                self.cb.set_label(self.label, **self.labelkwargs)
        return

    def set_label(self, label, **kwargs):
        """
      Set a text label along the long side of the color bar.
      It is a convenience routine for Matplotlib's *set_label()*
      but this one needs a plotted colorbar while we postpone plotting.
      """
        self.label = label
        self.labelkwargs = kwargs


class Beam(object):
    """
   Beam class. Usually the parameters will be provided by method
   :meth:`Annotatedimage.Beam`
   
   Objects from class Beam are graphical representations of the resolution
   of an instrument. The beam is centered at a position xc, yc.
   The major axis of the beam is the FWHM of longest distance between
   two opposite points on the ellipse. The angle between the major axis
   and the North is the position angle.

   Note that it is not correct to calculate the ellipse that represents
   the beam by applying distance 'r' (see code) as a function of
   angle, to get the new world coordinates. The reason is that the
   fwhm's are given as sizes on a sphere and therefore a correction for
   the declination is required. With method *dispcoord()* (see source code
   of class Beam)
   we sample the
   ellipse on a sphere with a correct position angle and with the correct
   sizes.

   Note that a beam can also be specified in 'pixel'/'grid' units.
   Then the ellipse axes and center are in pixel coordinates, while the
   position angle is defined with respect to the positive X axis (i.e. not the
   astronomical position angle).
   """

    def __init__(self, xc, yc, fwhm_major, fwhm_minor, pa, projection=None, units=None, **kwargs):
        self.ptype = 'Beam'
        if units:
            grids = units.upper().startswith('PIX')
        else:
            grids = False
        if not grids:
            if units is not None:
                uf, errmes = unitfactor('degree', units)
                if uf is None:
                    raise ValueError(errmes)
                else:
                    fwhm_major /= uf
                    fwhm_minor /= uf
            semimajor = fwhm_major / 2.0
            semiminor = fwhm_minor / 2.0
            Pi = numpy.pi
            startang, endang, delta = (0.0, 360.0, 1.0)
            sinP = numpy.sin(pa * Pi / 180.0)
            cosP = numpy.cos(pa * Pi / 180.0)
            phi = numpy.arange(startang, endang + delta, delta, dtype='f')
            cosA = numpy.cos(phi * Pi / 180.0)
            sinA = numpy.sin(phi * Pi / 180.0)
            d = semiminor * cosA * (semiminor * cosA) + semimajor * sinA * (semimajor * sinA)
            r = numpy.sqrt(semimajor * semimajor * semiminor * semiminor / d)
            self.p1 = None
            self.p2 = None
            lon_new, lat_new = dispcoord(xc, yc, r, -1, phi + pa)
            splitlon = get_splitlon(projection)
            if splitlon is None:
                lon1, lat1 = lon_new, lat_new
                lon2 = lat2 = []
            else:
                lon1, lat1, lon2, lat2 = split_polygons(lon_new, lat_new, splitlon)
            if len(lon1):
                xp, yp = projection.topixel((lon1, lat1))
                self.p1 = Polygon(list(zip(xp, yp)), **kwargs)
            if len(lon2):
                xp, yp = projection.topixel((lon2, lat2))
                self.p2 = Polygon(list(zip(xp, yp)), **kwargs)
        else:
            self.p1 = Ellipse((xc, yc), fwhm_major, fwhm_minor, angle=pa, **kwargs)
            self.p2 = None
        return

    def plot(self, frame):
        if self.p1 is not None:
            frame.add_patch(self.p1)
        if self.p2 is not None:
            frame.add_patch(self.p2)
        return


class Skypolygon(object):
    """
   This class defines objects that can only be plotted onto
   spatial maps.
   Usually the parameters will be provided by method
   :meth:`Annotatedimage.Skypolygon`
   
   """

    def __init__(self, projection, prescription=None, xc=None, yc=None, major=None, minor=None, nangles=6, pa=0.0, units=None, lons=None, lats=None, stepsize=1.0, **kwargs):
        self.ptype = 'Skypolygon'
        self.p1 = self.p2 = None
        self.patch = None
        splitlon = get_splitlon(projection)
        if prescription is None:
            if lons is None and lats is None:
                raise ValueError('No prescription entered nor longitudes and latitudes')
            elif lons is None or lats is None:
                raise ValueError('No prescription entered and missing longitudes or latitudes')
        else:
            if xc is None or yc is None:
                raise ValueError('Missing value for center xc or yc!')
            if major is None and minor is None:
                raise ValueError('Both major and minor axes are not specified!')
            if major is None:
                major = minor
            if minor is None:
                minor = major
            if units is not None:
                uf, errmes = unitfactor('degree', units)
                if uf is None:
                    raise ValueError(errmes)
                else:
                    major /= uf
                    minor /= uf
            Pi = numpy.pi
            if prescription[0].upper() == 'E':
                semimajor = major / 2.0
                semiminor = minor / 2.0
                startang, endang, delta = 0.0, 360.0, abs(stepsize)
                sinP = numpy.sin(pa * Pi / 180.0)
                cosP = numpy.cos(pa * Pi / 180.0)
                phi = numpy.arange(startang, endang + delta, delta, dtype='f')
                cosA = numpy.cos(phi * Pi / 180.0)
                sinA = numpy.sin(phi * Pi / 180.0)
                d = semiminor * cosA * (semiminor * cosA) + semimajor * sinA * (semimajor * sinA)
                r = numpy.sqrt(semimajor * semimajor * semiminor * semiminor / d)
                lons, lats = dispcoord(xc, yc, r, -1, phi + pa)
            elif prescription[0].upper() == 'R':
                xs = minor / 2.0
                ys = -major / 2.0
                samples = 100
                deltax = minor / float(samples)
                deltay = major / float(samples)
                x = numpy.zeros(samples)
                y = numpy.zeros(samples)
                for i in range(samples):
                    x[i] = xs
                    y[i] = ys + i * deltay

                phi1 = numpy.arctan2(y, x)
                r1 = numpy.hypot(x, y)
                xs = minor / 2.0
                ys = major / 2.0
                for i in range(samples):
                    x[i] = xs - i * deltax
                    y[i] = ys

                phi2 = numpy.arctan2(y, x)
                r2 = numpy.hypot(x, y)
                xs = -minor / 2.0
                ys = major / 2.0
                for i in range(samples):
                    x[i] = xs
                    y[i] = ys - i * deltay

                phi3 = numpy.arctan2(y, x)
                r3 = numpy.hypot(x, y)
                xs = -minor / 2.0
                ys = -major / 2.0
                for i in range(samples):
                    x[i] = xs + i * deltax
                    y[i] = ys

                phi4 = numpy.arctan2(y, x)
                r4 = numpy.hypot(x, y)
                phi = numpy.concatenate((phi1, phi2, phi3, phi4)) * 180 / Pi + 90
                r = numpy.concatenate((r1, r2, r3, r4))
                lons, lats = dispcoord(xc, yc, r, -1, phi + pa)
            elif prescription[0].upper() == 'N':
                if nangles < 3:
                    raise ValueError('Number of angles in regular polygon must be > 2!')
                nsamples = 360.0 / nangles
                psi = numpy.linspace(0, 360, nangles + 1)
                radius = major / 2.0
                xs = radius
                ys = 0.0
                first = True
                for ang in psi[1:]:
                    xe = radius * numpy.cos(ang * Pi / 180)
                    ye = radius * numpy.sin(ang * Pi / 180)
                    lambd = numpy.arange(0.0, 1.0, 1.0 / nsamples)
                    x = xs + lambd * (xe - xs)
                    y = ys + lambd * (ye - ys)
                    Phi = numpy.arctan2(y, x) * 180.0 / Pi
                    R = numpy.hypot(x, y)
                    xs = xe
                    ys = ye
                    if first:
                        phi = Phi.copy()
                        r = R.copy()
                        first = False
                    else:
                        phi = numpy.concatenate((phi, Phi))
                        r = numpy.concatenate((r, R))

                lons, lats = dispcoord(xc, yc, r, -1, phi + pa)
        if lons is None or lats is None:
            raise ValueError('Unknown prescription')
        if splitlon is None:
            lon1, lat1 = lons, lats
            lon2 = lat2 = []
        else:
            lon1, lat1, lon2, lat2 = split_polygons(lons, lats, splitlon)
        if len(lon1):
            xp, yp = projection.topixel((lon1, lat1))
            self.p1 = Polygon(list(zip(xp, yp)), closed=True, **kwargs)
            self.lon1 = lon1
            self.lat1 = lat1
        if len(lon2):
            xp, yp = projection.topixel((lon2, lat2))
            self.p2 = Polygon(list(zip(xp, yp)), closed=True, **kwargs)
            self.lon2 = lon2
            self.lat2 = lat2
        return

    def plot(self, frame):
        if self.p1 is not None:
            frame.add_patch(self.p1)
            self.patch = self.p1
        if self.p2 is not None:
            frame.add_patch(self.p2)
            self.patch = self.p2
        return


class Marker(object):
    """
   Marker class. Usually the parameters will be provided by method
   :meth:`Annotatedimage.Marker`

   Mark features in your map with a marker symbol. Properties of the
   marker are set with Matplotlib's keyword arguments.
   """

    def __init__(self, xp=None, yp=None, **kwargs):
        self.ptype = 'Marker'
        self.xp = xp
        self.yp = yp
        self.kwargs = kwargs
        self.patch = None
        return

    def plot(self, frame):
        if self.xp is None or self.yp is None:
            return
        if not issequence(self.xp):
            self.xp = [
             self.xp]
        if not issequence(self.yp):
            self.yp = [
             self.yp]
        self.patch = frame.plot(self.xp, self.yp, 'o', **self.kwargs)
        self.patch = self.patch[0]
        return


class Gridframe(object):
    """
   -------------------------------------------------------------------------------
   Helper class which defines objects with properties which are read
   when pixel coordinates need to be plotted.
   -------------------------------------------------------------------------------
   """

    def __init__(self, pxlim, pylim, plotaxis, gridlines, major, minor, inside=False, **kwargs):
        self.ptype = 'Gridframe'
        self.pxlim = pxlim
        self.pylim = pylim
        self.plotaxis = plotaxis
        self.markerkwargs = {}
        self.kwargs = kwargs
        self.gridlines = gridlines
        self.major = major
        self.minor = minor
        self.inside = inside


class Pixellabels(object):
    """
   Draw positions in pixels along one or more
   plot axes. Nice numbers and step size are
   calculated by Matplotlib's own plot methods.
   
   
   :param plotaxis:     The axis number of one or two of the axes of the
                        plot rectangle:
   
                        * wcsgrat.left
                        * wcsgrat.bottom
                        * wcsgrat.right
                        * wcsgrat.top

                        or 'left', 'bottom', 'right', 'top'
                        
   :type  plotaxis:     Integer
   
   :param markersize:   Set size of ticks at pixel positions.
                        The size can be negative to get tick
                        marks that point outwards.
   :type  markersize:   Integer
   
   :param gridlines:    Set plotting of grid lines (connected tick marks)
                        on or off (True/False). The default is off.
   :type gridlines:     Boolean

   :param major:        This number overrules the default positions
                        for the major tick marks. The tick marks and labels
                        are plotted at a multiple number of *major*.
   :type major:         Float or Integer (usually the input will be an integer).

   :param minor:        This number sets the plotting of minor tick marks on.
                        The markers are plotted at a multiple value of
                        *minor*.
   :type minor:         Float or Integer (usually the input will be an integer).
   
   :param offset:       The pixels can have an integer offset.
                        If you want the reference pixel to be pixel
                        0 then supply offset=(crpixX, crpixY).
                        These crpix values are usually read from then
                        header. In this routine the nearest integer of
                        the input is calculated to ensure that the
                        offset is an integer value.
   :type offset:        *None* or a floating point number
   
   :param kwargs:       Keyword arguments to set attributes for
                        the labels (e.g. color='g', fontsize=8)
   :type kwargs:        Matplotlib keyword argument(s)
   
   :Returns:            An object from class *Gridframe* which
                        is added to the plot container with Plotversion's
                        method :meth:`Plotversion.add`.
   
   :Notes:              Graticules and Pixellabels are plotted in their own
                        plot frame. If you want to be able to toggle grid lines
                        in a frame labeled with pixel coordinates, then you have to make sure
                        that the Pixellabels frame is plotted last. So always define
                        Pixellabels objects before Graticule objects. 
   
   :Examples:           Annotate the pixels in a plot along the right and top axis
                        of a plot. Change the color of the labels to red::
   
                           mplim = f.Annotatedimage(frame)
                           mplim.Pixellabels(plotaxis=("bottom", "right"), color="r")

                           or with separate axes:
   
                           mplim.Pixellabels(plotaxis="bottom", color="r")

                           mplim.Pixellabels(plotaxis="right", color="b", markersize=10)
                           mplim.Pixellabels(plotaxis="top", color="g", markersize=-10, gridlines=True)

   :Methods:

   .. automethod:: setp_marker
   .. automethod:: setp_label
   """

    def __init__(self, pxlim, pylim, plotaxis=None, markersize=None, gridlines=False, ticks=None, major=None, minor=None, offset=None, inside=False, **kwargs):

        def nint(x):
            return numpy.floor(x + 0.5)

        self.ptype = 'Pixellabels'
        defkwargs = {'fontsize': 7}
        defkwargs.update(kwargs)
        if plotaxis is None:
            plotaxis = [
             2, 3]
        px = [0, 0]
        py = [0, 0]
        px[0] = pxlim[0]
        py[0] = pylim[0]
        px[1] = pxlim[1]
        py[1] = pylim[1]
        if offset is not None:
            offX = nint(offset[0])
            offY = nint(offset[1])
            px[0] -= offX
            px[1] -= offX
            py[0] -= offY
            py[1] -= offY
        gridlabs = Gridframe(px, py, plotaxis, gridlines, major, minor, inside, **defkwargs)
        self.gridlabs = gridlabs
        self.frame = None
        return

    def setp_marker(self, **kwargs):
        """
      Set properties of the pixel label tick markers
       
      :param kwargs:  keyword arguments to change properties of
                      the tick marks. A tick mark is a Matploltlib
                      :class:`Line2D` object with attributes like
                      *markeredgewidth* etc.
      :type kwargs:   Python keyword arguments.
      """
        self.gridlabs.markerkwargs.update(kwargs)

    def setp_label(self, **kwargs):
        """
      Set properties of the pixel label tick markers
       
      :param kwargs:  keyword arguments to change properties of
                      (all) the tick labels. A tick mark is a Matploltlib
                      :class:`Text` object with attributes like
                      *fontsize*, *fontstyle* etc.
      :type kwargs:   Python keyword arguments.
      """
        self.gridlabs.kwargs.update(kwargs)

    def plot(self, frame):
        """
      -----------------------------------------------------------
      Purpose:         Plot labels that annotate the pixels
                       (or another system if an offset is given)
      Parameters:
         pixellabels - Object from class Gridframe made with 
                       method Graticule.Pixellabels
      Returns:         --
      Notes:           This method can only plot the grid labels along
                       two axes. If you need to label the other axes 
                       too, then add another grid with method Pixellabels().

      -----------------------------------------------------------
      """
        fig = frame.figure
        pixellabels = self.gridlabs
        plotaxes = wcsgrat.parseplotaxes(pixellabels.plotaxis)
        if len(plotaxes) > 2:
            raise Exception('Can plot labels for a maximum of 2 axes. Please split up!')
        if 0 in plotaxes and 2 in plotaxes or 1 in plotaxes and 3 in plotaxes:
            raise Exception('Cannot plot labels for this combination. Please split up!')
        aspect = frame.get_aspect()
        adjust = frame.get_adjustable()
        kwargs = pixellabels.kwargs
        markerkwargs = pixellabels.markerkwargs
        xlo = pixellabels.pxlim[0] - 0.5
        ylo = pixellabels.pylim[0] - 0.5
        xhi = pixellabels.pxlim[1] + 0.5
        yhi = pixellabels.pylim[1] + 0.5
        framelabel = randomlabel('fr_')
        try:
            r, c, n = frame.get_geometry()
            gframe = fig.add_subplot(r, c, n, aspect=aspect, adjustable=adjust, autoscale_on=False, frameon=False, label=framelabel)
            gframe.set_position(frame.get_position())
        except:
            gframe = fig.add_axes(frame.get_position(), aspect=aspect, adjustable=adjust, autoscale_on=False, frameon=False, label=framelabel)

        gframe.set_xlim((xlo, xhi))
        gframe.set_ylim((ylo, yhi))
        self.frame = gframe
        if 3 in plotaxes or 1 in plotaxes:
            if pixellabels.major is not None:
                majorLocator = MultipleLocator(pixellabels.major)
                gframe.xaxis.set_major_locator(majorLocator)
            if pixellabels.minor:
                minorLocator = MultipleLocator(pixellabels.minor)
                gframe.xaxis.set_minor_locator(minorLocator)
        if 3 in plotaxes:
            gframe.xaxis.set_label_position('top')
            gframe.xaxis.tick_top()
        else:
            if 1 in plotaxes:
                gframe.xaxis.set_label_position('bottom')
                gframe.xaxis.tick_bottom()
            else:
                for tick in gframe.xaxis.get_major_ticks():
                    tick.label2.set(visible=False)
                    tick.label1.set(visible=False)
                    tick.tick1On = False
                    tick.tick2On = False

                setmarker = pixellabels.markerkwargs > 0
                for tick in gframe.xaxis.get_major_ticks():
                    if 3 in plotaxes:
                        tick.label2.set(**kwargs)
                        if setmarker:
                            tick.tick2line.set(**markerkwargs)
                        tick.tick1On = False
                        tick.gridOn = pixellabels.gridlines
                    elif 1 in plotaxes:
                        tick.label1.set(**kwargs)
                        if setmarker:
                            tick.tick1line.set(**markerkwargs)
                        tick.tick2On = False
                        tick.gridOn = pixellabels.gridlines

                if 2 in plotaxes or 0 in plotaxes:
                    if pixellabels.major is not None:
                        majorLocator = MultipleLocator(pixellabels.major)
                        gframe.yaxis.set_major_locator(majorLocator)
                    if pixellabels.minor:
                        minorLocator = MultipleLocator(pixellabels.minor)
                        gframe.yaxis.set_minor_locator(minorLocator)
                if 2 in plotaxes:
                    gframe.yaxis.set_label_position('right')
                    gframe.yaxis.tick_right()
                elif 0 in plotaxes:
                    gframe.yaxis.set_label_position('left')
                    gframe.yaxis.tick_left()
                else:
                    for tick in gframe.yaxis.get_major_ticks():
                        tick.label2.set(visible=False)
                        tick.label1.set(visible=False)
                        tick.tick1On = False
                        tick.tick2On = False

            for tick in gframe.yaxis.get_major_ticks():
                if 2 in plotaxes:
                    tick.label2.set(**kwargs)
                    if setmarker:
                        tick.tick2line.set(**markerkwargs)
                    tick.tick1line.set_visible(False)
                    tick.gridOn = pixellabels.gridlines
                elif 0 in plotaxes:
                    tick.label1.set(**kwargs)
                    if setmarker:
                        tick.tick1line.set(**markerkwargs)
                    tick.tick2line.set_visible(False)
                    tick.gridOn = pixellabels.gridlines

        if self.gridlabs.inside:
            if 0 in plotaxes:
                for tick in gframe.yaxis.get_major_ticks():
                    tick.set_pad(-10.0)
                    tick.label1.set_horizontalalignment('left')

            if 2 in plotaxes:
                for tick in gframe.yaxis.get_major_ticks():
                    tick.set_pad(-10.0)
                    tick.label2.set_horizontalalignment('right')

            if 1 in plotaxes:
                for tick in gframe.xaxis.get_major_ticks():
                    tick.set_pad(-10.0)
                    tick.label1.set_verticalalignment('top')

            if 3 in plotaxes:
                for tick in gframe.xaxis.get_major_ticks():
                    tick.set_pad(-10.0)
                    tick.label2.set_verticalalignment('bottom')

        fig.sca(frame)
        return


class Annotatedimage(object):
    """
This is one of the core classes of this module. It sets the connection
between the FITS data (created or read from file) and the routines that
do the actual plotting with Matplotlib.
The class is usually used in the context of class :class:`FITSimage` which
has a method that prepares the parameters for the constructor of
this class.

:param frame:
   This is the frame where image and or contours will be plotted.
   If omitted then a default frame will be set
:type frame:
   Matplotlib Axes instance
:param header:
   The header data for this file. Either from a FITS header or a
   dictionary with header data.
:type header:
   Python dictionary or pyfits.NP_pyfits.Header instance
:param pxlim:
   Two integer numbers which should not be smaller than 1 and not
   bigger than the header value *NAXISn*, where n represents the
   x axis.
:type pxlim:
   Tuple with two integers
:param pylim:
   Two integer numbers which should not be smaller than 1 and not
   bigger than the header value *NAXISn*, where n represents the
   y axis.
:type pylim:
   Tuple with two integers
:param imdata:
   Image data. This data must represent the area defined by
   *pxlim* and *pylim*.
:type imdata:
   2D NumPy array
:param projection:
   The current projection object which provides this class
   with conversion methods from :mod:`wcs` like
   :meth:`wcs.Projection.toworld` and :meth:`wcs.Projection.topixel`
   needed for conversions between pixel- and world coordinates.
:type projection:
   Instance of Projection class from module :mod:`wcs`
:param axperm:
   Tuple or list with the FITS axis number of the two image axes,
   e.g. axperm=(1,2)
:type axperm:
   Tuple with two integers
:param wcstypes:
   In some modules we need to know what the type of an axis in the image is
   so that for example we can find out whether two different images have swapped axes.
   The order of this list is the same as the order in the original FITS file.
   'lo' is longitude axis, 'la' is latitude axis,
   'sp' is spectral axis, 'li' is a linear axis. Appended to 'li' is an
   underscore and the ctype of that axis (e.g. 'li_stokes').
   If the original data has axes (RA, DEC, FREQ, STOKES), then FITSimage.wcstypes
   = ['lo','la', 'sp', 'li_STOKES'] and when we have an Annotatedimage
   object with axes (FREQ, DEC) then the axis permutation array is (3, 2) and
   the wcsypes list is ['sp', 'la'].
:type wcstypes:
   List of strings.
:param skyout:
   A so called sky definition (sky system, reference system, equinox)
   which is used to annotate the world coordinates and to draw
   graticule lines.
:type skyout:
   String
:param spectrans:
   The spectral translation. It sets the output system for spectral axes.
   E.g. a frequency axis can be labeled with velocities.
:type spectrans:
   String
:param alter:
   The alternative description of a world coordinate system. In a FITS header
   there is an alternative description of the world coordinate system if
   for each wcs related keyword, there is an alternative keyword which has
   a character appended to it (e.g. CRVAL1a, CDELT1a). The character that
   is appended is the one that need to be entered if one wants to use the
   alternate system. Note that this is only relevant to axis labeling and
   the plotting of graticules.
:type alter:
   Character (case insensitive)
:param mixpix:
   The axis number (FITS standard i.e. starts with 1) of the missing spatial axis for
   images with only one spatial axis (e.q. Position-Velocity plots).
:type mixpix:
   *None* or an integer
:param aspect:
   The aspect ratio. This value is used to correct the scale of the plot so
   that equal sizes in world coordinates (degrees) represent equal sizes
   in a plot. This aspect ratio is only useful for spatial maps. Its default
   value is 1.0. The aspect ratio is defined as:
   :math:`abs(cdelty/cdeltx)`. This value is automatically set in objects
   from :class:`FITSimage`
:param slicepos:
   Pixel coordinates used to slice the data
   in a data set with more than two axes. The pixel coordinates represent
   positions on the axes that do not belong to the image.
:type slicepos:
   Single value or tuple with integers
:param sliceaxnames:
   List with names of the axes outside the map. Assume we have a map of a RA-DEC
   map from a RA-DEC-FREQ cube, then *sliceaxnames* = ['FREQ']. Currently these
   names are not used.
:type sliceaxnames:
   List with strings
:param basename:
   Base name for new files on disk, for example to store a color map
   on disk. The default is supplied by method :meth:`FITSimage.Annotatedimage`.
:type basename:
   string
:param cmap:
   A colormap from class :class:`mplutil.VariableColormap` or a string
   that represents a colormap (e.g. 'jet', 'spectral' etc.).
:type cmap:
   mplutil.VariableColormap instance or string
:param blankcolor:
   Color of the undefined pixels (NaN's, blanks). It is a matplotlib color
   e.g. blankcolor='g'. In the display the color of the blanks can
   be changed with key 'B'. It loops throug a small set with predefined
   colors. Changing the colors of bad pixels helps to make them more visible.
:type blankcolor:
   Matplotlib color (e.g. 'c', '#aabb12')
:param clipmin:
   A value which sets the lower value of the interval between which the colors
   in the colormap are distributed. If omitted, the minimum data value will
   be *clipmin*.
:type clipmin:
   Float
:param clipmax:
   A value which sets the upper value of the interval between which the colors
   in the colormap are distributed. If omitted, the maximum data value will
   be *clipmin*.
:type clipmax:
   Float
:param boxdat:
   An 2dim. array with the same shape as the *boxdat* attribute of the
   input FITSimage object. 
:type boxdat:
   NumPy array
:param sourcename:
   Name of origin of data. By default set to 'unknownsource'
:type sourcename:
   String
:param gridmode:
   By default this value is set to False. Positions are written
   as pixel coordinates and input of coordinates as strings will
   parse numbers as pixel coordinates. If one sets this to True, then
   a system of grids is used. The relation between a pixel and a grid
   for axis *n* is:
   
   ``grid = pixel - NINT(CRPIXn)``

   Some (legacy) astronomy software packages use this system.
   Toolbar position information is written in grid coordinates and also numbers
   in the (string) input of positions are processed as grids.
   This option is useful when an interface is needed between the
   Kapteyn Package and another software package (e.g. GIPSY).
   Note that with positions as strings, we mean positions parsed
   with method :meth:`positions.str2pos`. These are not the
   positions which are described as **pixel** positions.
:type gridmode:
   Boolean
:param adjustable:
   todo
:type adjustable:
   todo
:param anchor:
   todo
:type anchor:
   todo
:param newaspect:
   todo
:type newaspect:
   todo
:param clipmode:
   todo
:type clipmode:
   Integer
:param clipmn:
   todo
:type clipmn:
   tuple with 2 integers
:param cubemanager:
   todo
:type cubemanager:
   maputils.figure.canvas.manager object or None
:param callbackslist:
   todo
:type callbackslist:
   Python dictionary
   
:Attributes:

    .. attribute:: alter

          Character that sets an alternate world coordinate system.

    .. attribute:: aspect

          Aspect ratio of a pixel according to the FITS header.
          For spatial maps this value is used to set and keep an
          image in the correct aspect ratio.

    .. attribute:: axperm

          Axis numbers of the two axis in this map. Axis numbers
          start with 1.

    .. attribute:: basename

          Name of data origin.

    .. attribute:: blankcolor

          Color of 'bad' pixels as a Matplotlib color.
          
    .. attribute:: box

          Coordinates of the plot box. In order to keep the entire pixel in the
          corners in the plot, one has to extend the values of *pxlim* and
          *pylim* with 0.5 pixel.

    .. attribute:: clipmin

          Value either entered or calculated, which scales the image data to the
          available colors. Clipmin is the minimum value.

    .. attribute:: clipmax

          Value either entered or calculated, which scales the image data to the
          available colors. Clipmax is the maximum value.

    .. attribute:: cmap

          The color map. This is an object from class :class:`mplutil.VariableColormap`.
          which is inherited from the Matplotlib color map class.

    .. attribute:: cmapinverse

          Boolean which store the status of the current colormap, standard or inverted.

    .. attribute:: data

          Image data. Other data containers are attibutes 'data_blur', 'data_hist',
          and 'data_orig'.

    .. attribute:: fluxfie

          Function or Lambda expression which can be used to scale the flux found with
          method *getflux()*. There must be two parameters in this function or

          expression: *a* for the area and *s* for the sum of the pixel values.
          E.g. ``Annotatedimage.fluxfie = lambda s, a: s/a``
          Note that there is no method to set this attribute.
          The attribute is used in the shapes module.

    .. attribute:: frame

          Matplotlib Axes instance where image and contours are plotted

    .. attribute:: gridmode

          Boolean that indicates when we work in pixel- or in grid coordinates.

    .. attribute:: hdr

          Header which is used to derive the world coordinate system for axis labels
          and graticule lines. The header is either a Python dictionary or a PyFITS
          header.

    .. attribute:: mixpix

          The pixel of the missing spatial axis in a Position-Velocity
          image.

    .. attribute:: objlist

          List with all plot objects for the current *Annotatedimage* object derived from classes:
          'Beam', 'Colorbar', 'Contours', 'Graticule', 'Image', 'Marker', 'Minortickmarks',
          'Pixellabels', 'RGBimage', 'Ruler', 'Skypolygon'

    .. attribute:: pixelstep

          The step size in pixels or fraction of pixels. This size is used to sample
          the area of an object. Used in the context of the shapes module.
          E.g. ``annim.pixelstep = 0.5;``

    .. attribute:: pixoffset

          Tuple with two offsets in pixels used to distinguish a pixel coordinate system
          from a grid coordinate system.

    .. attribute:: projection

          An object from the Projection class as defined in module :mod:`wcs`

    .. attribute:: ptype

          Each object in the object list has an attribute which describes the (plot) type
          of the object. The ptype of an Annotatedimage is *Annotatedimage*.

    .. attribute:: pxlim

          Pixel limits in x = (xlo, xhi)

    .. attribute:: pylim

          Pixel limits in y = (ylo, yhi)

    .. attribute:: rgbs

          Boolean which is set to True if the current image is composed of three images
          each representing one color.
          
    .. attribute:: sliceaxnames

          A list with axis names that are not part of the current image, but
          are part of the data structure from which the current Annotated image data
          is extracted.

    .. attribute:: skyout

          The sky definition for which graticule lines are plotted
          and axis annotation is made (e.g. "Equatorial FK4")

    .. attribute:: spectrans

          The translation code to transform native spectral coordinates
          to another system (e.g. frequencies to velocities)

    .. attribute:: slicepos

          Single value or tuple with more than one value representing
          the pixel coordinates on axes in the original data structure
          that do not belong to the image. It defines how the data slice
          is ectracted from the original.
          The order of these 'outside' axes is copied from the (FITS) header.

    .. attribute:: wcstypes
    
          Type of the axes in this data. The order is the same as of the axes.
          The types ara strings and are derived from attribute wcstype of the
          Projection object. The types are:
          'lo' is longitude axis. 'la' is latitude axis,
          'sp' is spectral axis. 'li' is a linear axis. Appended to 'li' is an
          underscore and the ctype of that axis (e.g. 'li_stokes').
  

    .. attribute:: lutscales
    
          Class variable. A list with possible color mapping scales:
          ['linear', 'log', 'exp', 'sqrt', 'square']
     
    .. attribute:: blankcols
    
          Class variable. A list with Matplotlib colors:
          ['c', 'w', 'k', 'y', 'm', 'r', 'g', 'b']
                    
    .. attribute:: blanknames
     
          Class variable. A list with strings, representing the colors in 
          :attr:`maputils.Annotatedimage.blankcols`:
          ['Cyan', 'White', 'Black', 'Yellow', 'Magenta', 'Red', 'Green', 'Blue']
          
    .. attribute:: slopetrans
    
          Pixel values between [a,b] are mapped to colors with index between
          [A,B]. The mapping is a straight line with a slope and an offset
          Scale horizontal mouse position between [0,1] into a
          value between 0 and ``slopetrans`` degrees to scale the mapping of 
          pixel values to colors.
          Current value is set to 89 degrees. 
           
    .. attribute:: shifttrans
    
          Translate vertical mouse position from [0,1] to [-``shifttrans``, ``shifttrans``]
          to scale the mapping of pixel values to colors.
          Currently ``shifttrans`` is set to 0.5.
          
          
:Methods:

.. automethod:: set_norm
.. automethod:: set_colormap
.. automethod:: write_colormap
.. automethod:: set_blankcolor
.. automethod:: set_aspectratio
.. automethod:: get_colornavigation_info
.. automethod:: Image
.. automethod:: RGBimage
.. automethod:: Contours
.. automethod:: Colorbar
.. automethod:: Graticule
.. automethod:: Pixellabels
.. automethod:: Minortickmarks
.. automethod:: Beam
.. automethod:: Marker
.. automethod:: Ruler
.. automethod:: Skypolygon
.. automethod:: plot
.. automethod:: toworld
.. automethod:: topixel
.. automethod:: inside
.. automethod:: histeq
.. automethod:: blur
.. automethod:: interact_toolbarinfo
.. automethod:: interact_imagecolors
.. automethod:: interact_writepos
.. automethod:: positionsfromfile

   """
    lutscales = [
     'linear', 'log', 'exp', 'sqrt', 'square']
    scalekeys = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4}
    scales_default = 0
    blankcols = ['c', 'w', 'k', 'y', 'm', 'r', 'g', 'b']
    blanknames = ['Cyan', 'White', 'Black', 'Yellow', 'Magenta', 'Red', 'Green', 'Blue']
    blankcols_default = 0
    slopetrans = 89.0
    shifttrans = 0.5

    def __init__(self, frame, header, pxlim, pylim, imdata, projection, axperm, wcstypes, skyout, spectrans, alter='', mixpix=None, aspect=1, slicepos=None, sliceaxnames=None, basename=None, cmap=None, blankcolor=blankcols[blankcols_default], clipmin=None, clipmax=None, boxdat=None, sourcename='unknownsource', gridmode=False, adjustable='box', anchor='C', newaspect=None, clipmode=0, clipmn=(4, 5), callbackslist={}):
        """
      """
        self.ptype = 'Annotatedimage'
        self.sourcename = sourcename
        self.hdr = header
        self.projection = projection
        self.pxlim = pxlim
        self.pylim = pylim
        if boxdat is not None:
            self.data = boxdat
        else:
            self.data = imdata
        self.mixpix = mixpix
        self.axperm = axperm
        self.wcstypes = wcstypes
        self.skyout = skyout
        self.spectrans = spectrans
        self.alter = alter
        if self.pxlim[0] <= self.pxlim[1]:
            deltax = 0.5
        else:
            deltax = -0.5
        if self.pylim[0] <= self.pylim[1]:
            deltay = 0.5
        else:
            deltay = -0.5
        self.box = (
         self.pxlim[0] - deltax, self.pxlim[1] + deltax, self.pylim[0] - deltay, self.pylim[1] + deltay)
        self.image = None
        self.aspect = aspect
        if newaspect is not None:
            self.aspect = newaspect
        self.adjustable = adjustable
        self.anchor = anchor
        self.slicepos = slicepos
        self.gridmode = gridmode
        self.sliceaxnames = sliceaxnames
        self.contours = None
        self.colorbar = None
        self.contourset = None
        if cmap is None:
            cmap = cmlist.cmap_default
        self.objlist = []
        self.frame = self.adjustframe(frame, adjustable)
        self.messenger = None
        self.toolbarkey = None
        self.callbackslist = callbackslist
        try:
            self.figmanager = self.frame.figure.canvas.manager
            if self.figmanager.toolbar.set_message is not nonefunc:
                self.figmanager.toolbar.globalmessenger = self.figmanager.toolbar.set_message
                self.figmanager.toolbar.set_message = nonefunc
        except:
            self.figmanager = None

        if 'exmes' in callbackslist:
            self.messenger = callbackslist['exmes']
            self.canvasmessenger = False
        else:
            try:
                self.messenger = self.figmanager.toolbar.globalmessenger
                self.canvasmessenger = True
            except:
                self.messenger = nonefunc
                self.canvasmessenger = False

            self.autostate = None
            try:
                self.autostate = cmap.auto
                cmap.auto = False
            except:
                pass

        self.set_colormap(cmap)
        self.set_blankcolor(blankcolor)
        needstats = False
        datmin = datmax = mean = rms = None
        if clipmode == 0:
            if None in [clipmin, clipmax]:
                needstats = True
        else:
            needstats = True
        if needstats:
            datmin, datmax, mean, rms = self.get_stats()
        if clipmin is None:
            if clipmode in (0, 1):
                clipmin = datmin
            elif None in [mean, rms]:
                clipmin = None
            else:
                clipmin = mean - rms * clipmn[0]
        if clipmax is None:
            if clipmode in (0, 1):
                clipmax = datmax
            elif None in [mean, rms]:
                clipmax = None
            else:
                clipmax = mean + rms * clipmn[1]
        self.clipmin = clipmin
        self.clipmax = clipmax
        self.datmin = datmin
        self.datmax = datmax
        self.mean = mean
        self.rms = rms
        if self.clipmin is None or not numpy.isfinite(self.clipmin):
            self.clipmin = 0.0
        if self.clipmax is None or not numpy.isfinite(self.clipmax):
            self.clipmax = self.clipmin + 1.0
        if self.clipmin > self.clipmax:
            self.clipmin, self.clipmax = self.clipmax, self.clipmin
        self.AxesCallback_ids = []
        self.norm = Normalize(vmin=self.clipmin, vmax=self.clipmax, clip=True)
        self.histogram = False
        self.data_hist = None
        self.blurred = False
        self.data_blur = None
        self.blurfac = (self.pxlim[1] - self.pxlim[0] + 1) / 200.0
        self.blurindx = 0
        self.X_lastvisited = None
        self.Y_lastvisited = None
        self.data_orig = self.data
        if basename is None:
            self.basename = 'Unknown'
        else:
            self.basename = basename
        self.pixelstep = 1.0
        self.fluxfie = lambda s, a: s / a
        annotatedimage_list.append(self)
        self.pixoffset = [0.0, 0.0]
        if self.gridmode:
            self.set_pixoffset(nint(self.projection.crpix[0]), nint(self.projection.crpix[1]))
        self.rgbs = None
        if self.autostate is not None:
            cmap.auto = self.autostate
            self.cmap.auto = self.autostate
        self.regcb = None
        self.infoobj = None
        self.linepieces = []
        self.textlabels = []
        self.splitcb = None
        self.cbframe = None
        self.composed_slicemessage = ''
        self.grat = None
        self.clevels = None
        self.contourSet = None
        self.contours_on = False
        self.contours_changed = False
        self.contours_cmap = None
        self.contours_colour = 'r'
        self.backgroundImageNr = None
        self.alpha = 1.0
        return

    def callback(self, cbid, *arg):
        """
      Helper function for registered callbacks
      """
        if cbid in self.callbackslist:
            self.callbackslist[cbid](*arg)

    def get_stats(self):
        """
      Get necessary statistics e.g. to set clip levels
      """
        if self.data is None:
            return (None, None, None, None)
        else:
            datmin = datmax = mean = rms = mask = None
            validmask = False
            datmin = numpy.nanmin(self.data)
            if not numpy.isfinite(datmin):
                mask = numpy.isfinite(self.data)
                validmask = numpy.any(mask)
                if validmask:
                    datmin = float(self.data[mask].min())
                else:
                    datmin = None
            if validmask:
                if numpy.any(mask):
                    datmax = float(self.data[mask].max())
                else:
                    datmax = None
            else:
                datmax = numpy.nanmax(self.data)
                if not numpy.isfinite(datmax):
                    datmax = None
            if validmask:
                mean = float(self.data[mask].mean())
                rms = float(self.data[mask].std())
            else:
                mean = float(self.data.mean())
                rms = float(self.data.std())
                if not (numpy.isfinite(rms) and numpy.isfinite(mean)):
                    mask = numpy.isfinite(self.data)
                    if numpy.any(mask):
                        mean = float(self.data[mask].mean())
                        rms = float(self.data[mask].std())
            return (
             datmin, datmax, mean, rms)

    def set_pixoffset(self, xoff=0.0, yoff=0.0):
        """
      For conversions from FITS to other pixel based coordinate systems.
      """
        self.pixoffset[0] = xoff
        self.pixoffset[1] = yoff

    def set_norm(self, clipmin=None, clipmax=None):
        """
      Matplotlib scales image values between 0 and 1 for its distribution
      of colors from the color map. With this method we set the image values
      which we want to scale between 0 and 1. The default image values
      are the minimum and maximum of the data in :attr:`Annotatedimage.data`.
      If you want to inspect a certain range of data values you need more
      colors in a smaller intensity range, then use different *clipmin*
      and *clipmax* in the constructor of :class:`Annotatedimage` or
      in this method.

      :param clipmin:
         Image data below this threshold will get the same color
         Value None will be replaced by 'clipmin'.
      :type clipmin:
         Float
      :param clipmax:
         Image data above this threshold will get the same color
         Value None will be replaced by 'clipmax'.
      :type clipmax:
         Float

      :Examples:

         >>> fitsobj = maputils.FITSimage("m101.fits")
         >>> annim = fitsobj.Annotatedimage(frame, cmap="spectral")
         >>> annim.Image(interpolation='spline36')
         >>> annim.set_norm(10000, 15500)

         or:

         >>> fitsobj = maputils.FITSimage("m101.fits")
         >>> annim = fitsobj.Annotatedimage(frame, cmap="spectral", clipmin=10000, clipmax=15500)

      :notes:
      
         It is also possible to change the norm after an image has been displayed.
         This enables a programmer to setup key interaction for
         changing the clip levels in an image for example when the default clip levels
         are not suitable to inspect a certain data range.
         Usually the color editing (with :meth:`Annotatedimage.interact_imagecolors`)
         can do this job very well so we think there is not much demand in a scripting
         environment. With GUI's it will be different.
      """
        if clipmin is None:
            clipmin = self.clipmin
        if clipmax is None:
            clipmax = self.clipmax
        if clipmin > clipmax:
            clipmin, clipmax = clipmax, clipmin
        self.norm = Normalize(vmin=clipmin, vmax=clipmax, clip=True)
        if self.cmap is not None:
            self.cmap.update()
        if self.image is not None:
            self.image.norm = self.norm
            if self.image.im is not None:
                self.image.im.set_clim(clipmin, clipmax)
        if self.colorbar is not None:
            self.colorbar.cb.set_clim(clipmin, clipmax)
        return

    def set_colormap(self, cmap, blankcolor=None):
        """
      Method to set the initial color map for images, contours and colorbars.
      These color maps are either strings (e.g. 'jet' or 'spectral')
      from a list with Matplotlib color maps or it is a path to
      a color map on disk (e.g. cmap="/home/user/luts/mousse.lut").
      If the color map is not found in the list with known color maps
      then it is added to the list, which is a global variable called
      *cmlist*. (see: :data:`maputils.cmlist`)

      The Kapteyn Package has also a list with useful color maps. See
      example below or example 'mu_luttest.py' in the
      :doc:`maputilstutorial`.
      
      If you add the event handler *interact_imagecolors()* it is
      possible to change colormaps with keyboard keys and mouse.

      :param cmap:
         The color map to be used for image, contours and colorbar
      :type cmap:
         String or instance of VariableColormap
      :param blankcolor:
         Color of the bad pixels in your image.
      :type blankcolor:
          Matplotlib color

      :Examples:

         >>> fitsobj = maputils.FITSimage("m101.fits")
         >>> annim = fitsobj.Annotatedimage(frame, clipmin=10000, clipmax=15500)
         >>> annim.set_colormap("spectral")

         or use the constructor as in:

         >>> annim = fitsobj.Annotatedimage(frame, cmap="spectral", clipmin=10000, clipmax=15500)

         Get extra lookup tables from Kapteyn Package (by default, these
         luts are appended at creation time of cmlist, see :data:`maputils.cmlist`)
      
         >>> extralist = mplutil.VariableColormap.luts()
         >>> maputils.cmlist.add(extralist)

      """
        if cmap is None:
            cmap = cmlist.cmap_default
        if isinstance(cmap, Colormap):
            self.cmap = cmap
            self.cmindx = 0
        else:
            if isinstance(cmap, six.string_types):
                try:
                    self.cmindx = cmlist.colormaps.index(cmap)
                except:
                    cmlist.add(cmap)
                    self.cmindx = cmlist.colormaps.index(cmap)

                self.cmap = VariableColormap(cmap)
            else:
                raise Exception('Color map is not of type Colormap or string')
            if self.image is not None:
                self.cmap.set_source(cmap)
            self.startcmap = self.cmap
            self.startcmindx = cmlist.colormaps.index(cmlist.cmap_default)
            self.cmapinverse = False
            if blankcolor is not None:
                self.set_blankcolor(blankcolor)
            try:
                self.cmap.auto = False
            except:
                pass

        return

    def write_colormap(self, filename):
        """
      Method to write current colormap rgb values to file on disk.
      If you add the event handler *interact_imagecolors()*, this
      method is automatically invoked if you press key 'm'.

      This method is only useful if the colormap changes i.e.
      in an interactive environment.
      
      :param filename:  
         Name of file to which the current (modified) color look up table
         (lut) is written. This lut can be imported as a new lut in another session.
      :type filename: 
         Python stringz
       
      """
        a = tabarray(self.cmap._lut[0:-3, 0:3])
        a.writeto(filename)

    def set_blankcolor(self, blankcolor, alpha=1.0):
        """
      Set the color of bad pixels.
      If you add the event handler *interact_imagecolors()*, this
      method steps through a list of colors for the bad pixels in an
      image.

      :param blankcolor:
         The color of the bad pixels (blanks) in your map
      :type blankcolor:
         Matplotlib color
      :param alpha:
         Make the color of bad pixels transparent with *alpha < 1*
      :type alpha:
         Float in interval [0,1]
         
      :Example:

         >>> annim.set_blankcolor('c')
      """
        self.cmap.set_bad(blankcolor, alpha)
        self.blankcol = blankcolor

    def set_aspectratio(self, aspect):
        """
      Set the aspect ratio. Overrule the default aspect ratio which corrects
      pixels that are not square in world coordinates. Can be useful if you
      want to stretch images for which the aspect ratio doesn't matter
      (e.g. XV maps).

      :param aspect:
         The aspect ratio is defined as *pixel height / pixel width*.
         With this value one can stretch an image in x- or y direction.
         The default is such that 1 arcmin in x has the same length
         in cm as 1 arcmin in y.
      :type aspect:
         Float
         
      :Example:

         >>> annim = fitsobj.Annotatedimage(frame)
         >>> annim.set_aspectratio(1.2)
      """
        if aspect <= 0.0:
            raise ValueError('Only aspect ratios > 0 are allowed')
        self.aspect = abs(aspect)
        self.frame.set_aspect(aspect=self.aspect, adjustable=self.adjustable, anchor=self.anchor)

    def adjustframe(self, frame, adjustable='box'):
        """
      Method to change the frame for the right aspect ratio and
      how to react on a resize of the plot window.
      """
        frame.set_aspect(aspect=self.aspect, adjustable=adjustable, anchor=self.anchor)
        frame.set_autoscale_on(False)
        frame.xaxis.set_visible(False)
        frame.yaxis.set_visible(False)
        frame.set_xlim((self.box[0], self.box[1]))
        frame.set_ylim((self.box[2], self.box[3]))
        return frame

    def get_colornavigation_info(self):
        """
      This method compiles and returns a help text for
      color map interaction.
      """
        helptext = colornavigation_info()
        return helptext

    def blur(self, nx, ny=None):
        """
      Blur the image by convolving with a gaussian kernel of typical
      size nx (pixels). The optional keyword argument ny allows for a different
      size in the y direction.
      nx, ny are the sigma's for the gaussian kernel.
      """
        if ny is None:
            ny = nx
        if self.data is None:
            raise Exception('Cannot plot image because image data is not available!')
        if self.data_blur is None:
            self.data_blur = numpy.zeros(self.data.shape)
        gaussian_filter(self.data_orig, sigma=(nx, ny), order=0, output=self.data_blur, mode='reflect', cval=numpy.nan)
        self.data_blur = self.data_orig - self.data_orig + self.data_blur
        return

    def histeq(self, nbr_bins=256):
        """
      Create a histogram equalized version of the data.
      The histogram equalized data is stored in attribute *data_hist*.
      """
        if self.data is None:
            raise Exception('Cannot plot image because image data is not available!')
        im = self.data
        ix = numpy.isfinite(im)
        imhist, bins = numpy.histogram(im[ix].flatten(), nbr_bins, normed=True, range=(
         self.clipmin, self.clipmax))
        cdf = imhist.cumsum()
        cdf = cdf / cdf[(-1)]
        im2 = numpy.interp(im.flatten(), bins[:-1], cdf)
        m = (self.clipmax - self.clipmin) / (cdf[(-1)] - cdf[0])
        im2 = m * (im2 - cdf[0]) + self.clipmin
        self.data_hist = im - im + im2.reshape(im.shape)
        return

    def Image(self, **kwargs):
        """
      Setup of an image.
      This method is a call to the constructor of class :class:`Image` with
      a default value for most of the keyword parameters.
      This created object has an attribute *im* which is
      an instance of Matplotlib's *imshow()* method.
      This object has a plot method. This method is used by the
      more general :meth:`Annotatedimage.plot` method.

      :param kwargs:
         From the documentation
         of Matplotlib we learn that for method *imshow()* (used in the plot method
         if an Image) a few interesting keyword arguments remain:

         * *interpolation* - From Matplotlib's documentation: Acceptable values are
           None, 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning',
           'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel',
           'mitchell', 'sinc', 'lanczos'
         * *visible* - Switch the visibility of the image
         * *alpha* - Value between 0 and 1 which sets the transparency of the image.

      :type kwargs:
         Python keyword parameters

      :Attributes:

         .. attribute:: im

         The object generated after a call to Matplotlib's *imshow()*.

      :Example:

         >>> fitsobject = maputils.FITSimage(promptfie=maputils.prompt_fitsfile)
         >>> annim = fitsobject.Annotatedimage()
         >>> annim.Image(interpolation="spline36")

         or create an image but make it invisible:

         >>> annim.Image(visible=False)
      """
        if self.image is not None:
            raise Exception('Only 1 image allowed per Annotatedimage object')
        image = Image(self.data, self.box, self.cmap, self.norm, **kwargs)
        self.objlist.append(image)
        self.image = image
        return image

    def RGBimage(self, f_red, f_green, f_blue, fun=None, **kwargs):
        """
      Matplotlib's method imshow() is able to produce RGB images.
      To create a real RGB image, we need three arrays with identical
      shape representing the red, green and blue components.
      Method imshow() requires data scaled between 0 and 1.

      This utility method prepares a composed and scaled data array
      derived from three FITSimage objects.
      It scales the composed array and not the individual image arrays.
      The method allows for a function or lambda expression to
      be entered to process the scaled data.
      The world coordinate system (e.g. to plot graticules) is copied
      from the current :class:`Annotatedimage` object. Note that for the
      three images only the shape of the array must be equal to the
      shape of the data of the current :class:`Annotatedimage` object.

      :param f_red:
         This object describes a two dimensional data structure which represents
         the red part of the composed image.
      :type f_red:
         Object from class :class:`FITSimage`
      :param f_green:
         This object describes a two dimensional data structure which represents
         the green part of the composed image.
      :type f_green:
         Object from class :class:`FITSimage`
      :param f_blue:
         This object describes a two dimensional data structure which represents
         the blue part of the composed image.
      :type f_blue:
         Object from class :class:`FITSimage`
      :param fun:
         A function or a Lambda expression to process the scaled data.
      :type fun:
         Function or Lambda expression
      :param kwargs:
         See description method :meth:`Annotatedimage.Image`.
      :type kwargs:
         Python keyword parameters

      :Note:
         A RGB image does not interact with a colormap. Interacting with a colormap
         (e.g. after adding annim.interact_imagecolors() in the example below)
         is not forbidden but it gives weird results. To rescale the data, for
         instance for a better view of interesting data, you need to enter a
         function or Lambda expression with parameter *fun*.

      :Example:

       ::
      
         from kapteyn import maputils
         from numpy import sqrt
         from matplotlib import pyplot as plt
         
         f_red = maputils.FITSimage('m101_red.fits')
         f_green = maputils.FITSimage('m101_green.fits')
         f_blue = maputils.FITSimage('m101_blue.fits')
         
         fig = plt.figure()
         frame = fig.add_subplot(1,1,1)
         annim = f_red.Annotatedimage(frame)
         annim.RGBimage(f_red, f_green, f_blue, fun=lambda x:sqrt(x), alpha=0.5)
         
         grat = annim.Graticule()
         annim.interact_toolbarinfo()
         
         maputils.showall()

      """
        if self.image is not None:
            raise Exception('Only 1 image allowed per Annotatedimage object')
        if f_red.boxdat.shape != self.data.shape:
            raise Exception('Shape of red image is not equal to shape of Annotatedimage object!')
        if f_green.boxdat.shape != self.data.shape:
            raise Exception('Shape of green image is not equal to shape of Annotatedimage object!')
        if f_blue.boxdat.shape != self.data.shape:
            raise Exception('Shape of blue image is not equal to shape of Annotatedimage object!')
        rgbim = numpy.zeros(self.data.shape + (3, ))
        rgbim[:, :, 0] = f_red.boxdat
        rgbim[:, :, 1] = f_green.boxdat
        rgbim[:, :, 2] = f_blue.boxdat
        dmin = rgbim.min()
        dx = rgbim.max() - dmin
        if dx == 0.0:
            dx = 1.0
        rgbim = (rgbim - dmin) / dx
        if fun is not None:
            rgbim = fun(rgbim)
        image = Image(rgbim, self.box, self.cmap, self.norm, **kwargs)
        self.objlist.append(image)
        self.image = image
        self.rgbs = (
         f_red.boxdat, f_green.boxdat, f_blue.boxdat)
        return image

    def Contours(self, levels=None, cmap=None, colors=None, **kwargs):
        r"""
      Setup of contour lines.
      This method is a call to the constructor of class :class:`Contours`
      with a number of default parameters.
      Either it plots single contour lines or a combination
      of contour lines and filled regions between the contours.
      The colors are taken from the current colormap.

      :param levels:
         Image values for which contours must be plotted. The default
         is *None* which results in a list with values calculated
         by the Contour constructor.
      :type levels:
         None or a list with floating point numbers
      :param cmap:
         A colormap from class :class:`mplutil.VariableColormap` or a string
         that represents a colormap (e.g. 'jet', 'spectral' etc.).
         It sets the contour colours.
      :type cmap:
         mplutil.VariableColormap instance or string
      :param colors:
         A sequence with Matplotlib colors, e.g. ['r','g','y']
      :type colors:
         Sequence with strings
      :param kwargs:
         There are a number of keyword arguments that
         are useful:
       
         * *filled* - if set to True the area between two contours will
           get a color (close to the color of the contour.
         * negative - one of Matplotlib's line styles
           'solid', 'dashed', 'dashdot', 'dotted' in which contours are
           plotted which represent negative image values.
         * *colors* - If None, the current colormap will be used.
           If a character or string, all levels will be plotted in this color.
           If a tuple of matplotlib colors then different levels will be
           plotted in different colors in the order specified.
         * *linewidths* - If a number, all levels will be plotted with this linewidth.
           If a tuple, different levels will be plotted with different
           linewidths in the order specified
         * *linestyles* - One of 'solid', 'dashed', 'dashdot', 'dotted', which
           sets the style of the contour. It can also be given in a list. See the
           Matplotlib documentation for its behaviour.
      :type kwargs:
         Python keyword parameters

      :Methods:

         * :meth:`Contours.setp_contour` - Set properties for individual contours
         * :meth:`Contours.setp_label` - Plot labels for individual contours

      :Examples:

         >>> fitsobj = maputils.FITSimage("m101.fits")
         >>> annim = fitsobj.Annotatedimage()
         >>> annim.Image(alpha=0.5)
         >>> cont = annim.Contours()
         >>> print "Levels=", cont.clevels
         Levels= [  4000.   6000.   8000.  10000.  12000.  14000.]

         >>> annim.Contours(filled=True)

         In the next example note the plural form of the standard Matplotlib
         keywords. They apply to all contours:
         
         >>> annim.Contours(colors='w', linewidths=2)

         Set levels and the line style for negative contours:
      
         >>> annim.Contours(levels=[-500,-300, 0, 300, 500], negative="dotted")

         A combination of keyword parameters with less elements than
         the number of contour levels:
      
         >>> cont = annim.Contours(linestyles=('solid', 'dashed', 'dashdot', 'dotted'),
                                   linewidths=(2,3,4), colors=('r','g','b','m'))

         Example of setting of properties for all and 1 contour with
         *setp_contour()*:
      
         >>> cont = annim.Contours(levels=range(10000,16000,1000))
         >>> cont.setp_contour(linewidth=1)
         >>> cont.setp_contour(levels=11000, color='g', linewidth=3)

         Plot a (formatted) label near a contour with *setp_label()*:
      
         >>> cont2 = annim.Contours(levels=(8000,9000,10000,11000))
         >>> cont2.setp_label(11000, colors='b', fontsize=14, fmt="%.3f")
         >>> cont2.setp_label(fontsize=10, fmt="$%g \lambda$")
      """
        if cmap is None and colors is None:
            colors = [
             'r']
        if cmap and colors:
            cmap = None
        contourset = Contours(self.data, self.box, levels, cmap=cmap, norm=self.norm, colors=colors, **kwargs)
        self.objlist.append(contourset)
        self.contourset = contourset
        return contourset

    def writecontours_file(self, filename=None):
        """
      Get info about the contours that are plotted
      and write their vertices to a text file on disk.
      The contours in the contour set are processed in order of the
      given contour levels. Per level, all the closed contours are processed
      in unknown order. For each contour the vertices are written to
      the file given by keyword parameter filename=
      There are various situations where it is useful to have this data.
      For example, it can be used to contruct masks or to analyze
      the shape of a contour or to calculate the flux if you know the size
      of a pixel.
      The contents of the file on disk is something similar to this:

      ! Level: 10000, contour number 0 area=20 sum=234302
      -132.000000   -72.255098
      -131.043290   -72.000000
      ....
      ! Level: 10000, contour number 1 area=141 sum=1.87093e+06      
      -142.000000   -68.235209
      -141.000000   -68.235209
      ....

      :param filename:
         Name of file on disk where the vertices of all contours are
         written. By default the name is set to: contour_info_xxxxx.txt
         where xxxxx contains data and time of creation.
      :type filename:
         String
         
      :returns:
         None, or a tuple with filename and current directory
      
      """
        if not self.contourSet:
            return
        if not filename:
            stamp = datetime.now().strftime('%d%m%Y_%H%M%S')
            filename = 'visions_contour_info' + '_' + stamp + '.txt'
        contourSet = self.contourSet
        gridmode = self.gridmode
        fp = open(filename, 'w')
        allcollections = contourSet.collections
        alllevels = contourSet.levels
        for levnr, collection in enumerate(allcollections):
            allpaths = collection.get_paths()
            cnr = 0
            for path in allpaths:
                verts = path.vertices
                flux = self.getflux(verts)
                fp.write('! Level: %g, contour number %d area=%g sum=%g\n' % (alllevels[levnr], cnr, flux[0], flux[1]))
                if gridmode:
                    xygrid = self.projection.pixel2grid(verts)
                else:
                    xygrid = verts
                for xco, yco in xygrid:
                    s = '%12f %12f\n' % (xco, yco)
                    fp.write(s)

                cnr += 1

        fp.close()
        return (filename, getcwd())

    def Colorbar(self, frame=None, clines=False, **kwargs):
        """
      This method is a call to the constructor of class :class:`Colorbar`
      with a number of default parameters.
      A color bar is an image which represents the current color scheme.
      It annotates the colors with image values so that it is possible
      to get an idea of the distribution of the values in your image.

      :param frame:
         By default a colorbar will 'steal' some space from its parent frame
         but this behaviour can be overruled by setting an explicit frame (Matplotlib Axes object).
      :type frame:
         Matplotlib Axes object
      :param clines:
          If set to true AND a contour set (an :meth:`Annotatedimage.Contours` object)
          is available, then lines will be plotted in the colorbar
          at positions that correspond to the contour levels
      :type clines:
          Boolean
      :param kwargs:
          Specific keyword arguments and Keyword arguments for Matplotlib's method *ColorbarBase()*

          * *label* - A text that will be plotted along the long axis of the colorbar.
          * *linewidths* - One number that sets the line width of all the contour lines
            in the colorbar.

          From Matplotlib:
             
          * *orientation* - 'horizontal' or 'vertical'
          * *fontsize* - Size of numbers along the colorbar
          * *ticks* - Levels which are annotated along the colorbar
          * *visible* - Make image in colorbar invisible
           
      :type kwargs:
          Python keyword arguments

      :methods:
          :meth:`Colorbar.set_label` - Plot a title along the long side of the colorbar.

      :Examples:

          A basic example were the font size for the ticks are set:
             
          >>> fitsobj = maputils.FITSimage("m101.fits")
          >>> annim = fitsobj.Annotatedimage(cmap="spectral")
          >>> annim.Image()
          >>> colbar = annim.Colorbar(fontsize=8)
          >>> annim.plot()
          >>> plt.show()

          Set frames for Image and Colorbar:

          >>> frame = fig.add_axes((0.1, 0.2, 0.8, 0.8))
          >>> cbframe = fig.add_axes((0.1, 0.1, 0.8, 0.1))
          >>> annim = fitsobj.Annotatedimage(cmap="Accent", clipmin=8000, frame=frame)
          >>> colbar = annim.Colorbar(fontsize=8, orientation='horizontal', frame=cbframe)

          Create a title for the colorbar and change its font size:

          >>> units = r'$ergs/(sec.cm^2)$'
          >>> colbar.set_label(label=units, fontsize=24)
      """
        if self.colorbar is not None:
            raise Exception('Only 1 colorbar allowed per Annotatedimage object')
        colorbar = Colorbar(self.cmap, frame=frame, norm=self.norm, contourset=self.contourset, clines=clines, **kwargs)
        self.objlist.append(colorbar)
        self.colorbar = colorbar
        return colorbar

    def Graticule(self, visible=True, pxlim=None, pylim=None, **kwargs):
        r"""
      This method is a call to the constructor of class :class:`wcsgrat.Graticule`
      with a number of default parameters.
      
      It calculates and plots graticule lines of constant longitude or constant
      latitude. The description of the parameters is found in
      :class:`wcsgrat.Graticule`. An extra parameter is *visible*.
      If visible is set to False than we can plot objects derived from this
      class such as 'Rulers' and 'Insidelabels' without plotting unwanted
      graticule lines and labels.

      :Methods:

         * :meth:`wcsgrat.Graticule.Ruler`
         * :meth:`wcsgrat.Graticule.Insidelabels`

      Other parameters such as *hdr*, *axperm*, *pxlim*, *pylim*, *mixpix*,
      *skyout* and *spectrans* are set to defaults in the context of this method
      and should not be overwritten.

      :Examples:

         >>> fitsobj = maputils.FITSimage('m101.fits')
         >>> annim = fitsobj.Annotatedimage()
         >>> grat = annim.Graticule()
         >>> annim.plot()
         >>> plt.show()

         Set the range in world coordinates and set the positions for
         the labels with (X, Y):
         
         >>> X = arange(0,360.0,15.0)
         >>> Y = [20, 30,45, 60, 75, 90]
         >>> grat = annim.Graticule(wylim=(20.0,90.0), wxlim=(0,360), 
                                    startx=X, starty=Y)

         Add a ruler, based on the current Annotatedimage object:
         
         >>> ruler3 = annim.Ruler(23*15,30,22*15,15, 0.5, 1, world=True,
                                 fmt=r"$%4.0f^\prime$",
                                 fun=lambda x: x*60.0, addangle=0)
         >>> ruler3.setp_labels(color='r')

         Add world coordinate labels inside the plot. Note that these are
         derived from the current Graticule object.
         
         >>> grat.Insidelabels(wcsaxis=0, constval=-51, rotation=90, fontsize=10,
                               color='r', ha='right')

      """

        class Gratdata(object):

            def __init__(self, hdr, axperm, wcstypes, pxlim, pylim, mixpix, skyout, spectrans, alter):
                self.hdr = hdr
                self.axperm = axperm
                self.pxlim = pxlim
                self.pylim = pylim
                self.mixpix = mixpix
                self.skyout = skyout
                self.spectrans = spectrans
                self.alter = alter
                self.wcstypes = wcstypes

        if pxlim is None:
            pxlim = self.pxlim
        if pylim is None:
            pylim = self.pylim
        gratdata = Gratdata(self.hdr, self.axperm, self.wcstypes, pxlim, pylim, self.mixpix, self.skyout, self.spectrans, self.alter)
        graticule = wcsgrat.Graticule(graticuledata=gratdata, **kwargs)
        graticule.visible = visible
        self.objlist.append(graticule)
        return graticule

    def Minortickmarks(self, graticule, partsx=10, partsy=10, **kwargs):
        """
      Drawing minor tick marks is as easy or as difficult as finding
      the positions of major tick marks. Therefore we decided that
      the best way to draw minor tick marks is to calculate a new
      (but invisible) graticule object. Only the tick marks are visible.

      :param graticule:
         Graticule object from which we change the step size
         between tick marks to create a new Graticule object for which
         most components (graticule lines, labels, ...) are made invisible.
      :type graticule:
         Object from class :class:`wcsgrat.Graticule`
      :param partsx:
         Divide major tick marks in this number of parts.
         This method forces this number to be an integer between 2 and 20
         If the input is None then nothing is plotted. For example for maps with
         only one spatial axis, one can decide to plot tick marks for only
         one of the axes.
      :type partsx:
         Integer or None
      :param partsx:
         See description for parameter *partsx*
      :type partsx:
         Integer or None
      :param kwargs:
         Parameters for changing the attributes of the tick mark symbols.
         Useful keywords are *color*, *markersize* and *markeredgewidth*.
      :type kwargs:
         Matplotlib keyword arguments related to a Line2D object.
   
      :Notes:
   
         Minor tick marks are also plotted at the positions of major tick marks.
         By default this will not be visible. It is visible if you user
         a longer marker size, a different color or a marker with increased
         width.
         The default marker size is set to 2.
   
      :Returns:
   
         This method returns a graticule object. Its properties can be
         changed in the calling environment with the appropriate methods
         (e.g. :meth:`wcsgrat.Graticule.setp_tickmark`).
   
      :Examples:
   
         ::
   
            from kapteyn import maputils
            from matplotlib import pyplot as plt
            fitsobj = maputils.FITSimage("m101.fits")
            mplim = fitsobj.Annotatedimage()
            grat = mplim.Graticule()
            grat2 = grat.minortickmarks()
            mplim.plot()
            plt.show()
   
         Adding parameters to change attributes:

         >>> grat2 = grat.minortickmarks(3, 5, color="#aa44dd", markersize=3, markeredgewidth=2)

         Minor tick marks only along x axis:

         >>> grat2 = minortickmarks(grat, 3, None)
      """
        startx = graticule.xstarts[0]
        starty = graticule.ystarts[1]
        skyout = graticule.skyout
        spectrans = graticule.spectrans
        wxlim = graticule.wxlim
        wylim = graticule.wylim
        if 'markersize' not in kwargs:
            kwargs.update(markersize=2)
        kwargs1 = kwargs.copy()
        kwargs2 = kwargs.copy()
        deltax = graticule.delta[0]
        deltay = graticule.delta[1]
        if partsx is None:
            deltax = None
            kwargs1.update(visible=False)
        else:
            deltax /= float(max(2, min(20, int(abs(partsx)))))
        if partsy is None:
            deltay = None
            kwargs2.update(visible=False)
        else:
            deltay /= float(max(2, min(20, int(abs(partsy)))))
        minorgrat = self.Graticule(startx=startx, starty=starty, deltax=deltax, deltay=deltay, wxlim=wxlim, wylim=wylim, skyout=skyout, spectrans=spectrans)
        minorgrat.setp_gratline(wcsaxis=[0, 1], visible=False)
        minorgrat.setp_ticklabel(wcsaxis=[0, 1], visible=False)
        minorgrat.setp_axislabel(plotaxis=[0, 1, 2, 3], visible=False)
        minorgrat.setp_tickmark(wcsaxis=0, **kwargs1)
        minorgrat.setp_tickmark(wcsaxis=1, **kwargs2)
        return minorgrat

    def Pixellabels(self, **kwargs):
        """
      This method is a call to the constructor of class
      :class:`Pixellabels`
      with a number of default parameters.
      It sets the annotation along a plot axis to pixel coordinates.

      :param plotaxis:     
         The axis name of one or two of the axes of the
         plot rectangle: or 'left', 'bottom', 'right', 'top'
         Combinations are always between 'left' and 'bottom' and 'right' and 'top'.
      :type  plotaxis:     
         String
      :param markersize:   
         Set size of ticks at pixel positions.
         The size can be negative to get tick marks that point outwards.
      :type  markersize:   
         Integer
      :param gridlines:    
         Set plotting of grid lines (connected tick marks)
         on or off (True/False). The default is off.
      :type gridlines:     
         Boolean
      :param offset:       
         The pixels can have an integer offset.
         If you want the reference pixel to be pixel
         0 then supply offset=(crpixX, crpixY).
         These crpix values are usually read from then
         header (e.g. as CRPIX1 and CRPIX2).
         In this routine the nearest integer of
         the input is calculated to ensure that the
         offset is an integer value.
      :type offset:        
         *None* or floating point numbers
      :param xxx:          
         Other parameters are related to Matplotlib label attributes.

      :Examples:

         >>> fitsobject = maputils.FITSimage("m101.fits")
         >>> annim = fitsobject.Annotatedimage()
         >>> annim.Pixellabels(plotaxis=("top","right"), color="b", markersize=10)

         or separate the labeling so that you can give different properties
         for different axes. In this case we shift the labels along the
         top axis towards the axis line with *va='top'*:
            
         >>> annim.Pixellabels(plotaxis='top', va='top')
         >>> annim.Pixellabels(plotaxis='right')

      :Notes:

         If a pixel offset is given for this Annimated object, then plot
         the pixel labels with this offset.

      """
        pixlabels = Pixellabels(self.pxlim, self.pylim, offset=self.pixoffset, **kwargs)
        self.objlist.append(pixlabels)
        return pixlabels

    def Beam(self, major, minor, pa=0.0, pos=None, xc=None, yc=None, units=None, **kwargs):
        r"""
      Objects from class Beam are graphical representations of the resolution
      of an instrument. The beam is centered at a position xc, yc.
      The major axis of the beam is the FWHM of the longest distance between
      two opposite points on the ellipse. The angle between the major axis
      and the North is the position angle.

      A beam is an ellipse in world coordinates.
      To draw a beam given the input parameters, points are calculated in world
      coordinates so that angle and required distance of sample points on the
      ellipse are correct on a sphere.
       
      
      :param major: Full width at half maximum of major axis of beam in degrees.
      :type major:  Float
      :param minor: Full width at half maximum of minor axis of beam in degrees.
      :type minor:  Float
      :param pa:    Position angle in degrees. This is the angle between
                    the positive y-axis and the major axis of the beam.
                    The default value is 0.0.
      :type pa:     Float
      :param pos:   A string that represents the position of the center
                    of the beam. If two numbers are available then
                    one can also use parameters *xc* and *yc*.
                    The value in parameter *pos* supersedes the values
                    in *xc* and *yc*.
      :type pos:    String
      :param xc:    X value in **world** coordinates of the center position
                    of the beam.
      :type xc:     Float
      :param yc:    Y value in **world** coordinates of the center position
                    of the beam.
      :type yc:     Float

      :Examples:
      
       ::
      
         fwhm_maj = 0.08
         fwhm_min = 0.06
         lat = 54.347395233845
         lon = 210.80254413455
         beam = annim.Beam(fwhm_maj, fwhm_min, 90, xc=lon, yc=lat,
                           fc='g', fill=True, alpha=0.6)
         pos = '210.80254413455 deg, 54.347395233845 deg'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='m', fill=True, alpha=0.6)
         pos = '14h03m12.6105s 54d20m50.622s'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='y', fill=True, alpha=0.6)
         pos = 'ga 102.0354152 {} 59.7725125'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='g', fill=True, alpha=0.6)
         pos = 'ga 102d02m07.494s {} 59.7725125'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='b', fill=True, alpha=0.6)
         pos = '{ecliptic,fk4, j2000} 174.3674627 {} 59.7961737'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='r', fill=True, alpha=0.6)
         pos = '{eq, fk4-no-e, B1950} 14h01m26.4501s {} 54d35m13.480s'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='c', fill=True, alpha=0.6)
         pos = '{eq, fk4-no-e, B1950, F24/04/55} 14h01m26.4482s {} 54d35m13.460s'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='c', fill=True, alpha=0.6)
         pos = '{ecl} 174.367764 {} 59.79623457'
         beam = annim.Beam(fwhm_maj, fwhm_min, pos=pos, fc='c', fill=True, alpha=0.6)
         pos = '53 58'     # Pixels
         beam = annim.Beam(0.04, 0.02, pa=30, pos=pos, fc='y', fill=True, alpha=0.4)
         pos = '14h03m12.6105s 58' # World coordinate and a pixel coordinate
         beam = annim.Beam(0.04, 0.02, pa=-30, pos=pos, fc='y', fill=True, alpha=0.4)

         # Using system of pixels/grids: use units='pixels'
         # Note that for the use of pos= nothing changes. Only ellipse axes are
         # in pixels and the position angle is wrt. the X axis.
         beam(9, 3, pos='10 10', pa=0, units='pixels', fc='y', hatch='/', alpha=0.4)

         # Make hatching more dense:
         beam(9, 3, pos='10 10', pa=0, units='pixels', fc='y', hatch='////', alpha=0.4)

         # Note the use of an escape character for the hatch symbol
         beam(9, 3, pos='pc pc', pa=0, units='PIX', fc='m', hatch='\', alpha=0.4)

         # Note that the center of the ellipse can also be entered with xc and yc
         # which prevents parsing by str2pos(). 
         beam(9, 3, xc=10, yc=10, pa=40, units='pix', fc='c', hatch='x', alpha=0.4)
         
      :Properties:

         A selection of keyword arguments for the beam (which is a
         Matplotlib :class:`Polygon` object) are:

         * alpha - float (0.0 transparent through 1.0 opaque)
         * color - Matplotlib color arg or sequence of rgba tuples
         * edgecolor or ec - Matplotlib color spec, or None for default, or 'none' for no color
         * facecolor or fc - Matplotlib color spec, or None for default, or 'none' for no color
         * linestyle  or ls - ['solid' | 'dashed' | 'dashdot' | 'dotted']
         * linewidth or lw - float or None for default
         * hatch - ['/' | '' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*']

      """
        if units:
            grids = units.upper().startswith('PIX')
        else:
            grids = False
        if pos is not None:
            poswp = str2pos(pos, self.projection, mixpix=self.mixpix, gridmode=self.gridmode)
            if poswp[3] != '':
                raise Exception(poswp[3])
            if grids:
                world = poswp[1][0]
            else:
                world = poswp[0][0]
        else:
            world = (
             xc, yc)
            if grids:
                world = self.projection.grid2pixel(world)
        spatials = [
         self.projection.lonaxnum, self.projection.lataxnum]
        spatialmap = self.axperm[0] in spatials and self.axperm[1] in spatials
        if not spatialmap:
            raise Exception('Can only plot a beam in a spatial map')
        beam = Beam(world[0], world[1], major, minor, pa, projection=self.projection, units=units, **kwargs)
        self.objlist.append(beam)
        return beam

    def Skypolygon(self, prescription=None, xc=None, yc=None, cpos=None, major=None, minor=None, nangles=6, pa=0.0, units=None, lons=None, lats=None, stepsize=1.0, **kwargs):
        """
      Construct an object that represents an area in the sky.
      Usually this is an ellipse, rectangle or regular polygon with
      given center and other parameters to define its size or number
      of angles and the position angle. The object is plotted in a
      way that the sizes and angles, as defined on a sphere, are
      preserved.
      The objects need a 'prescription'. This is a recipe to calculate
      a distance to a center point (0,0) as function of an angle
      in a linear and flat system. Then the object perimeter is
      re-calculated for a given center (xc,yc) and for corresponding
      angles and distances on a sphere.

      If *prescription=None*, then this method expects two arrays
      *lons* and *lats*.  These are copied unaltered as vertices for
      an irregular polygon.

      For cylindrical projections it is possible that a polygon in a
      all sky plot
      crosses a boundary (e.g. 180 degrees longitude if the projection
      center is at 0 degrees). Then the object is splitted into two parts
      one for the region 180-phi and one for the region 180+phi where phi
      is an arbitrary positive angle.
      This splitting is done for objects with and without a prescription.

      :param prescription:
         How should the polygon be created? The prescriptions are
         "ellipse", "rectangle", "npolygon" or None.
         This method only checks the first character of the string.
      :type prescription:
         String or None
      :param xc:
         Coordinate in degrees to set the center of the shape in X
      :type xc:
         Floating point number
      :param yc:
         Coordinate in degrees to set the center of the shape in Y
      :type yc:
         Floating point number
      :param cpos:
         Instead of a position in world coordinates (xc, yc),
         supply a string with a position. The syntax is described
         in the positions module. For example:
         ``cpos='20h30m10s -10d10m20.23s`` or ``cpos=ga 110.3 ga 33.4``
      :type cpos:
         String
      :param major:
         Major axis of ellipse in degrees. This parameter is also used as
         height for rectangles and as radius for regular polygons.
      :type major:
         Floating point number
      :param minor:
        Minor axis of ellipse in degrees. This parameter is also used as
         width for rectangles. If the prescription is an ellipse then
         a circle is defined if *major*=*minor*
      :type minor:
         Floating point number
      :param nangles:
         The number of angles in a regular polygon. The radius of this
         shape is copied from parameter *major*.
      :type nangles:
         Integer
      :param pa:
         Position angle. This is an astronomical angle i.e. with respect
         to the north in the direction of the east. For an ellipse the angle is
         between the north and the major axis. For a rectangle it is the
         angle between the north and the parameter that represents the height.
         For a regular polygon, it is the angle between the north and the line that
         connects the center with the first angle in the polygon.
      :type pa:
         Floating point number
      :param units:
         A case insensitive minimal matched string that sets the units for the
         values in *major* and *minor* (e.g. arcmin, arcsec).
      :type units:
         String
      :param lons:
         Sequence with longitudes in degrees that (together with matching
         latitudes) are used to define the vertices of a polygon.
         If nothing is entered for *prescription* or *prescription=None*
         then these positions are used unaltered.
      :type lons:
         Sequence of floating point numbers.
      :param lats:
         See description at *lons*.
      :type lats:
         Sequence of floating point numbers.
      :param stepsize:
         Step in degrees to calculate samples (applies to ellipse only)
      :type stepsize:
         Floating point number
      :param kwargs:
         Plot parameters
      :type kwargs:
         Matplotlib keyword arguments
      """
        if cpos is not None:
            poswp = str2pos(cpos, self.projection, mixpix=self.mixpix, gridmode=self.gridmode)
            if poswp[3] != '':
                raise Exception(poswp[3])
            world = poswp[0][0]
        else:
            world = (
             xc, yc)
        spatials = [
         self.projection.lonaxnum, self.projection.lataxnum]
        spatialmap = self.axperm[0] in spatials and self.axperm[1] in spatials
        if not spatialmap:
            raise Exception('Can only plot a sky polygon in a spatial map')
        spoly = Skypolygon(projection=self.projection, prescription=prescription, xc=world[0], yc=world[1], major=major, minor=minor, nangles=nangles, pa=pa, units=units, lons=lons, lats=lats, stepsize=stepsize, **kwargs)
        self.objlist.append(spoly)
        return spoly

    def Marker(self, pos=None, x=None, y=None, mode='', **kwargs):
        """
      Plot marker symbols at given positions. This method creates
      objects from class Marker. The constructor of that class needs
      positions in pixel coordinates. Here we allow positions to
      be defined in a string which can contain either world- or pixel
      coordinates (or a mix of both). If x and y coordinates are
      known, or read from file, one can also enter this data without
      parsing. The keyword arguments *x* and *y* can be used to enter
      pixel coordinates or world coordinates.

      :param pos:
         A definition of one or more positions for the current
         image. The string is parsed by :mod:`positions`.
      :type pos:
         String
      :param x:
         If keyword argument *pos* is not used, then this method
         expects numbers in parameters *x* and *y*. Advantage of
         using this parameter, is that it skips the position
         parser and therefore it is much faster.
      :type x:
         Float or a sequence of floating point numbers
      :param y:
         If keyword argument *pos* is not used, then this method
         expects numbers in parameters *x* and *y*
      :type y:
         Float or a sequence of floating point numbers
      :param mode:
         Flag to set the conversion mode. If the input string starts
         with 'w'  od 'W' then the numbers
         in *x* and *y* are world coordinates. Else, if the string starts
         with 'p' or 'P', they are processed as pixel coordinates.
      :type mode:
         String
                  
      :Returns:

         Object from class :class:`Marker`

      :Examples:
         In the first example we show 4 markers plotted in the
         projection center (given by header values CRPIX)::
      
            f = maputils.FITSimage("m101.fits")
            fig = plt.figure()
            frame = fig.add_subplot(1,1,1)
            annim = f.Annotatedimage(frame, cmap="binary")
            annim.Image()
            grat = annim.Graticule()
            annim.Marker(pos="pc", marker='o', markersize=10, color='r')
            annim.Marker(pos="ga 102.035415152 ga 59.772512522", marker='+',
                        markersize=20, markeredgewidth=2, color='m')
            annim.Marker(pos="{ecl,fk4,J2000} 174.367462651 {} 59.796173724",
                        marker='x', markersize=20, markeredgewidth=2, color='g')
            annim.Marker(pos="{eq,fk4-no-e,B1950,F24/04/55} 210.360200881 {} 54.587072397",
                        marker='o', markersize=25, markeredgewidth=2, color='c',
                        alpha=0.4)

         In the second example we show how to plot a sequence of markers.
         Note the use of the different keyword arguments and the role
         of flag *world* to force the given values to be processed in pixel
         coordinates::
       
            # Use pos= keyword argument to enter sequence of
            # positions in pixel coordinates
            pos = "[200+20*sin(x/20) for x in range(100,200)], range(100,200)"
            annim.Marker(pos=pos, marker='o', color='r')
            
            # Use x= and y= keyword arguments to enter sequence of
            # positions in pixel coordinates
            xp = [400+20*numpy.sin(x/20.0) for x in range(100,200)]
            yp = range(100,200)
            annim.Marker(x=xp, y=yp, mode='pixels', marker='o', color='g')

            # Single position in pixel coordinates
            annim.Marker(x=150, y=150, mode='pixels', marker='+', color='b')
            
         In the next example we show how to use method :meth:`positionsfromfile`
         in combination with this Marker method to read positions
         from a file and to plot them. The positions in the file
         are world coordinates. Method :meth:`positionsfromfile`
         returns pixel coordinates::
      
            fn = 'smallworld.txt'
            xp, yp = annim.positionsfromfile(fn, 's', cols=[0,1])
            annim.Marker(x=xp, y=yp, mode='pixels', marker=',', color='b')

      """
        if x is None and y is None and pos is None:
            return
        else:
            if pos is None:
                p = mode.upper().startswith('P')
                if p:
                    w = False
                else:
                    w = mode.upper().startswith('W')
                if not p and not w:
                    raise Exception('Marker(): Mode not or incorrectly specified!')
                else:
                    world = w
            if x is None and y is not None or x is not None and y is None:
                raise Exception('Marker(): One of the arrays is None and the other is not!')
            if pos is not None and (x is not None or y is not None):
                raise Exception('Marker(): You cannot enter values for both pos= and x= and/or y=')
            if pos is not None:
                poswp = str2pos(pos, self.projection, mixpix=self.mixpix, gridmode=self.gridmode)
                if poswp[3] != '':
                    raise Exception(poswp[3])
                xp = poswp[1][:, 0]
                yp = poswp[1][:, 1]
            elif world:
                xp, yp = self.topixel(x, y)
            else:
                xp, yp = x, y
            markers = Marker(xp, yp, **kwargs)
            self.objlist.append(markers)
            return markers

    def Ruler(self, pos1=None, pos2=None, x1=None, y1=None, x2=None, y2=None, lambda0=0.5, step=None, world=False, angle=None, addangle=0.0, fmt=None, fun=None, fliplabelside=False, mscale=None, labelsintex=True, **kwargs):
        """
      This method prepares arguments for a call to function
      :func:`rulers.Ruler` in module :mod:`rulers`

      Note that this method sets a number of parameters which
      cannot be changed like *projection*, *mixpix*, *pxlim*, *pylim*
      and *aspectratio*, which are all derived from the properties of the current
      :class:`maputils.Annotatedimage` object.
      """
        ruler = rulers.Ruler(self.projection, self.mixpix, self.pxlim, self.pylim, aspectratio=self.aspect, pos1=pos1, pos2=pos2, x1=x1, y1=y1, x2=x2, y2=y2, lambda0=lambda0, step=step, world=world, angle=angle, addangle=addangle, fmt=fmt, fun=fun, fliplabelside=fliplabelside, mscale=mscale, labelsintex=labelsintex, gridmode=self.gridmode, **kwargs)
        self.objlist.append(ruler)
        return ruler

    def plot(self):
        """
      Plot all objects stored in the objects list for this Annotated image.

      :Example:

         >>> fitsobj = maputils.FITSimage('m101.fits')
         >>> annim = fitsobj.Annotatedimage()
         >>> grat = annim.Graticule()
         >>> annim.plot()
         >>> plt.show()

      """
        needresize = False
        for obj in self.objlist:
            try:
                pt = obj.ptype
                if pt == 'Colorbar':
                    if obj.frame is None:
                        needresize = True
                        orientation = obj.kwargs['orientation']
                    else:
                        self.cbframe = obj.frame
            except:
                raise Exception('Unknown object. Cannot plot this!')

        if needresize:
            self.cbframe = make_axes(self.frame, orientation=orientation)[0]
            self.frame = self.adjustframe(self.frame)
        for obj in self.objlist:
            try:
                pt = obj.ptype
            except:
                raise Exception('Unknown object. Cannot plot this!')

            if pt in ('Image', 'Contour', 'Graticule', 'Insidelabels', 'Pixellabels',
                      'Beam', 'Marker', 'Ruler', 'Skypolygon'):
                try:
                    visible = obj.visible
                except:
                    visible = True

                obj.plot(self.frame)

        for obj in self.objlist:
            pt = obj.ptype
            if pt == 'Colorbar':
                if self.image is not None:
                    obj.plot(self.cbframe, self.image.im)
                elif self.contourset is not None:
                    obj.plot(self.cbframe, self.contourset.CS)
                else:
                    raise Exception('A color bar could not find an image or contour set!')

        self.cmap.add_frame(self.frame)
        return

    def toworld(self, xp, yp, matchspatial=False):
        """
      This is a helper method for method :meth:`wcs.Projection.toworld`.
      It converts pixel positions from a map to world coordinates.
      The difference with that method is that this method has its focus
      on maps, i.e. two dimensional structures.
      It knows about the missing spatial axis if your data slice has only one
      spatial axis.
      Note that pixels in FITS run from 1 to *NAXISn* and that the pixel
      coordinate equal to *CRPIXn* corresponds to the world coordinate
      in *CRVALn*.
   
      :param xp:
         Pixel value(s) corresponding to the x coordinate of a position.
      :type xp:
         Single Floating point number or sequence
      :param yp:
         A pixel value corresponding to the y coordinate of a position.
      :type yp:
         Single Floating point number or sequence
      :param matchspatial:
         If True then also return the world coordinate of the matching spatial
         axis. Usually this is an issue when the map is a slice with only
         one spatial axis (XV- or Position-Velocity map)
      :type matchspatial:
         Boolean

      :Note:
         If somewhere in the process an error occurs,
         then the return values of the world
         coordinates are all *None*.

      :Returns:
         Three world coordinates: *xw* which is the world coordinate for
         the x-axis, *yw* which is the world coordinate for
         the y-axis and (if *matchspatial=True*) *missingspatial* which
         is the world coordinate
         that belongs to the missing spatial axis.
         If there is not a missing spatial axis, then the value of this
         output parameter is *None*. So you don't need to know the structure
         of the map beforehand. You can test whether the last value
         is *None* or not *None* in the calling environment.
   
      :Examples:
         We have a test set with:
         
         * RA:   crpix1=51  - crval1=-51,28208479590
         * DEC:  crpix2=51  - crval2=+60.15388802060
         * VELO: crpix3=-20 - crval3=-243000 (m/s)
   
         Now let us try to find the world coordinates
         of a RA-VELO map at (crpix1, crpix3) at slice position DEC=51.
         We should get three numbers which are all equal
         to the value of *CRVALn*
   
         >>> from kapteyn import maputils
         >>> fig = figure()
         >>> fitsobject = maputils.FITSimage('ngc6946.fits')
         >>> fitsobject.set_imageaxes(1,3, slicepos=51)
         >>> annim = fitsobject.Annotatedimage()
         >>> annim.toworld(51,-20)
         (-51.282084795899998, -243000.0, 60.1538880206)
         >>> annim.topixel(-51.282084795899998, -243000.0)
         (51.0, -20.0)

         Or work with a sequence of numbers (list, tuple of NumPy ndarray
         object) as in this example::

            from kapteyn import maputils

            f = maputils.FITSimage("ngc6946.fits")
            # Get an XV slice at DEC=51
            f.set_imageaxes(1, 3, slicepos=51)
            annim = f.Annotatedimage()
            
            x = [10, 50, 300, 399]
            y = [1, 44, 88, 100]
            
            # Convert these to world coordinates
            lon, velo, lat = annim.toworld(x, y, matchspatial=True)
            print "lon, velo lat=", lon, velo, lat

            # We are not interested in the pixel coordinate of the slice
            # because we know it is 51. Therefore we omit 'matchspatial'
            x, y = annim.topixel(lon, velo)
            print "Back to pixel coordinates: x, y =", x, y

            #Output:
            #lon, velo lat= [-50.691745281033555,
            #                -51.267685761904154,
            #                -54.862775451370837,
            #                -56.280231731192607]
            #               [-154800.00401099998,
            #                 25799.987775999994,
            #                 210599.97937199997,
            #                 260999.97707999998]
            #               [ 60.152142940138205,
            #                 60.153886982461088,
            #                 60.089564526325667,
            #                 60.028325686860846]

            #Back to pixel coordinates: x, y = [  10.   50.  300.  399.]
            #                                  [   1.   44.   88.  100.]
      """
        xw = yw = None
        missingspatial = None
        try:
            if self.mixpix is None:
                xw, yw = self.projection.toworld((xp, yp))
            else:
                if issequence(xp):
                    mixpix = numpy.zeros(len(xp)) + self.mixpix
                else:
                    mixpix = self.mixpix
                xw, yw, missingspatial = self.projection.toworld((xp, yp, mixpix))
        except:
            pass

        if matchspatial:
            return (xw, yw, missingspatial)
        else:
            return (
             xw, yw)
            return

    def topixel(self, xw, yw, matchspatial=False):
        """
      This is a helper method for method :meth:`wcs.Projection.topixel`.
      It knows about the missing spatial axis if a data slice has only one
      spatial axis. It converts world coordinates in units (given by the
      FITS header, or the spectral translation) from a map to pixel coordinates.
      Note that pixels in FITS run from 1 to *NAXISn*.
   
      :param xw:
         A world coordinate corresponding to the x coordinate of a position.
      :type xw:
         Floating point number
      :param yw:
         A world coordinate corresponding to the y coordinate of a position.
      :type yw:
         Floating point number
      :param matchspatial:
         If set to *True* then return the pixel coordinates and the value of the
         pixel on the missing spatial axis.
      :type matchspatial:
         Boolean

      :Returns:
         Two pixel coordinates: *x* which is the world coordinate for
         the x-axis and *y* which is the world coordinate for
         the y-axis.

         If somewhere in the proces an error occurs, then the return values of the pixel
         coordinates are all *None*.
   
      :Notes:
         This method knows about the pixel on the missing spatial axis
         (if there is one). This pixel is usually the pixel coordinate of
         the slice if the dimension of the data is > 2.

      :Examples:
         See example at :meth:`toworld`
      """
        x = y = None
        try:
            if self.mixpix is None:
                x, y = self.projection.topixel((xw, yw))
            else:
                if issequence(xw):
                    mixpix = numpy.zeros(len(xw)) + self.mixpix
                    unknown = numpy.zeros(len(xw)) + numpy.nan
                else:
                    mixpix = self.mixpix
                    unknown = numpy.nan
                wt = (
                 xw, yw, unknown)
                pixel = (unknown, unknown, mixpix)
                wt, pixel = self.projection.mixed(wt, pixel)
                x = pixel[0]
                y = pixel[1]
        except:
            pass

        if matchspatial:
            return (x, y, self.mixpix)
        else:
            return (
             x, y)
            return

    def inside(self, x=None, y=None, pos=None, mode=''):
        """
      This convenience method belongs to class :class:`Annotatedimage` which
      represents a two dimensional map which could be a slice
      (*slicepos*) from a
      bigger data structure and/or could be limited by limits on the
      pixel ranges of the image axes (*pxlim*, *pylim*).
      Then, for a sequence of coordinates in x and y, return a sequence with
      Booleans with *True* for a coordinate within the boundaries of this
      map and *False* when it is outside the boundaries of this
      map. This method can work with either sequences of coordinates
      (parameters *x* and *y*)
      or a string with a position (parameter *pos*).
      If parameters *x* and *y* are used then parameter *world* sets
      these coordinates to world- or pixel coordinates.

      :param x:
         Single number of a sequence representing the x coordinates
         of your input positions. These coordinates are world coordinates
         if *mode='world'* (or *mode='w'*) and pixel
         coordinates if *mode='pixels* (or *mode='p'*).
      :type x:
         Floating point number or sequence of floating point numbers.
      :param y:
         Single number of a sequence representing the x coordinates
         of your input positions. See description for parameter *x*
      :type y:
         Floating point number or sequence of floating point numbers.
      :param mode:
         Input in *x* and*y* represent either pixel coordinates or
         world coordinates. Is the first character is 'p' or 'P' then
         the mode is set to pixels. If it starts with 'w' or 'W' the input
         in *x* and *y* are world coordinates.
      :param pos:
         A description of one or a number of positions entered as a string.
         The syntax is described in module :mod:`positions`.
         The value of parameter *mode* is ignored.
      :type pos:
         String
      :param world:
         If parameters *x* and *y* are used then the step of coordinate
         interpretation as with *pos* is skipped. These coordinates can be either
         pixel- or world coordinates depending on the value of *world*.
         By default this value is *True*.
      :type world:
         Boolean

      :Raises:
         :exc:`Exception`
            *One of the arrays is None and the other is not!*

         :exc:`Exception`
            *You cannot enter values for both pos= and x= and/or y=*

      :Returns:

         * None -- there was nothing to do
         * Single Boolean -- Input was a single position
         * NumPy array of Booleans -- Input was a sequence of positions

      :Note:
         
         For programmers: note the similarity to method :meth:`Marker`
         with respect to the use of method :meth:`positions.str2pos`.

         This method is tested with script *mu_insidetest.py* which
         is part of the examples tar file.

      :Examples:

         >>> fitsobj = maputils.FITSimage("m101.fits")
         >>> fitsobj.set_limits((180,344), (100,200))
         >>> annim = fitsobj.Annotatedimage()

         >>> pos="{} 210.870170 {} 54.269001"
         >>> print annim.inside(pos=pos)
         >>> pos="ga 101.973853, ga 59.816461"
         >>> print annim.inside(pos=pos)

         >>> x = range(180,400,40)
         >>> y = range(100,330,40)
         >>> print annim.inside(x=x, y=y, mode='pixels')

         >>> print annim.inside(x=crval1, y=crval2, mode='w')

      """
        if x is None and y is None and pos is None:
            return
        else:
            if pos is None:
                p = mode.upper().startswith('P')
                if p:
                    w = False
                else:
                    w = mode.upper().startswith('W')
                if not p and not w:
                    raise Exception('Inside(): Mode not or incorrectly specified!')
                else:
                    world = w
            if x is None and y is not None or x is not None and y is None:
                raise Exception('Inside(): One of the arrays is None and the other is not!')
            if pos is not None and (x is not None or y is not None):
                raise Exception('Inside(): You cannot enter values for both pos= and x= and/or y=')
            if pos is not None:
                world, pixels, units, errmes = str2pos(pos, self.projection, mixpix=self.mixpix, gridmode=self.gridmode)
                if errmes != '':
                    raise Exception(errmes)
                else:
                    xp = pixels[:, 0]
                    yp = pixels[:, 1]
            elif world:
                xp, yp = self.topixel(x, y)
                if not issequence(x):
                    x = [
                     x]
                if not issequence(y):
                    y = [
                     y]
                if xp is None:
                    xp = numpy.array([None] * len(x))
                if yp is None:
                    yp = numpy.array([None] * len(y))
            else:
                if not isinstance(x, numpy.ndarray):
                    xp = numpy.array(x)
                else:
                    xp = x
                if not isinstance(y, numpy.ndarray):
                    yp = numpy.array(y)
                else:
                    yp = y
            b = numpy.where((xp > self.pxlim[0] - 0.5) & (xp < self.pxlim[1] + 0.5) & (yp > self.pylim[0] - 0.5) & (yp < self.pylim[1] + 0.5), True, False)
            if b.shape != () and len(b) == 1:
                b = b[0]
            return b

    def positionmessage(self, x, y, posobj, parts=False):
        """
      Display cursor position in pixels and world coordinates together
      with the image value in the message area of a Matplotlib window.
      This function is used internally by :meth:`on_move` and
      :meth:`on_click`.

      :param x:
         The x coordinate of a position in the image
      :type x:
         Floating point number
      :param y:
         The y coordinate of a position in the image
      :type y:
         Floating point number
      :param posobj:
         A description of how the string should be formatted is
         stored in this object.
      :type posobj:
         An object from class :class:`Positionmessage`

      :Returns:
         A formatted string with position information and
         the image value of the corresponding pixel. E.g.
         ``x,y= 56.91, 25.81  wcs=-51.366665, 59.973195  Z=-4.45e-04``

         The WCS coordinates are not formatted in hms/dms. They are
         printed in the units of the FITS header.

      :Notes:
         This method knows about the object's missing axis if
         only one spatial axis was part of the image.
         It takes also care of NaNs in your map.
      """
        s = ''
        if self.pxlim[0] - 0.5 < x < self.pxlim[1] + 0.5:
            if self.pylim[0] - 0.5 < y < self.pylim[1] + 0.5:
                xw, yw, missingspatial = self.toworld(x, y, matchspatial=True)
                xi = int(numpy.round(x - (self.pxlim[0] - 1)))
                yi = int(numpy.round(y - (self.pylim[0] - 1)))
                x -= self.pixoffset[0]
                y -= self.pixoffset[1]
                spix = posobj.pix2str(x, y)
                swcs = posobj.wcs2str(xw, yw, missingspatial)
                swcsuf = posobj.wcs2str(xw, yw, missingspatial, unformatted=True)
                if self.rgbs is None:
                    if self.data is None:
                        z = numpy.nan
                    else:
                        z = self.data[(yi - 1, xi - 1)]
                else:
                    z = (
                     self.rgbs[0][(yi - 1, xi - 1)], self.rgbs[1][(yi - 1, xi - 1)], self.rgbs[2][(yi - 1, xi - 1)])
                s = ''
                if spix is not None:
                    s = 'x,y=%s' % spix
                if swcs is not None:
                    s += '  wcs=%s' % swcs
                sz = None
                sz = self.rgbs is None and self.data is None or posobj.z2str(z)
                s += '  z=%s' % sz
        if parts:
            return (spix, swcs, swcsuf, sz)
        else:
            return s.strip()
            return

    def mouse_toolbarinfo(self, axesevent):
        """
      *Display position information:*

      Note that the events (motion_notify_event) are blocked from the
      moment you changed mode in the toolbar to zoom or pan mode.
      So we display a message in our modified Matplotlib routines
      that deal with callbacks for zoom- and pan actions.
      """
        s = ''
        x, y = axesevent.xdata, axesevent.ydata
        self.X_lastvisited = x
        self.Y_lastvisited = y
        try:
            mode = self.figmanager.toolbar.mode
        except:
            return

        if mode != '':
            return
        s = self.positionmessage(x, y, axesevent.posobj)
        if s != '':
            if self.canvasmessenger and not backend.startswith('QT'):
                charw = 0.12
                xsize = self.frame.figure.get_figwidth()
                messagemax = xsize - 2.5
                if len(s) * charw > messagemax:
                    l = int(messagemax / charw)
                    s = s[:l]
            self.messenger(s)

    def interact_toolbarinfo(self, pixfmt='%.1f', wcsfmt='%.3e', zfmt='%+.3e', hmsdms=True, dmsprec=1):
        """
      Allow this :class:`Annotatedimage` object to interact with the user.
      It reacts to mouse movements. A message is prepared with position information
      in both pixel coordinates and world coordinates. The world coordinates
      are in the units given by the (FITS) header.

      :param pixfmt:
         Python number format for pixel coordinates
      :type pixfmt:
         String
      :param wcsfmt:
         Python number format for wcs coordinates if the coordinates
         are not spatial or if parameter *hmsdms* is False.
      :type wcsfmt:
         String
      :param zfmt:
         Python number format for image value(s)
      :type pixfmt:
         String
      :param hmsdms:
         If True (default) then spatial coordinates will be formatted
         in hours/degrees, minutes and seconds according to the current sky system.
         The precision in seconds is entered with parameter *dmsprec*.
      :type hmsdms:
         Boolean
      :param dmsprec:
         Number of decimal digits in seconds for coordinates formatted in
         in HMS/DMS
      :type dmsprec:
         Integer
         
      :Notes:

         If a format is set to *None*, its corresponding number(s) will
         not appear in the informative message.

         If a message does not fit in the toolbar then only a part is
         displayed. We don't have control over the maximum size of that message
         because it depends on the backend that is used (GTK, QT,...).
         If nothing appears, then a manual resize of the window will suffice.

      :Example: 

         Attach to an object from class :class:`Annotatedimage`:
      
         >>> annim = f.Annotatedimage(frame)
         >>> annim.interact_toolbarinfo()

         or:

         >>> annim.interact_toolbarinfo(wcsfmt=None, zfmt="%g")
         
         A more complete example::

            from kapteyn import maputils
            from matplotlib import pyplot as plt

            f = maputils.FITSimage("m101.fits")
            
            fig = plt.figure(figsize=(9,7))
            frame = fig.add_subplot(1,1,1)
            
            annim = f.Annotatedimage(frame)
            ima = annim.Image()
            annim.Pixellabels()
            annim.plot()
            annim.interact_toolbarinfo()
            
            plt.show()

      """
        posobj = Positionmessage(self.projection.skysys, self.skyout, self.projection.types)
        posobj.pixfmt = pixfmt
        posobj.wcsfmt = wcsfmt
        posobj.zfmt = zfmt
        posobj.hmsdms = hmsdms
        posobj.dmsprec = dmsprec
        self.toolbarkey = AxesCallback(self.mouse_toolbarinfo, self.frame, 'motion_notify_event', posobj=posobj)
        self.AxesCallback_ids.append(self.toolbarkey)

    def disconnectCallbacks(self):
        """
      Disconnect callbacks made with AxecCallback()
      The id's are stored in a list 'AxesCallback_ids'
      """
        for acid in self.AxesCallback_ids:
            acid.deschedule()
            del acid

        self.AxesCallback_ids = []

    def mouse_imagecolors(self, axesevent):
        """
      *Reset color limits:*
   
      If you move the mouse in this image and press the **right mouse button**
      at the same time, then the color limits for image and colorbar are
      set to a new value.
      
      :param axesevent:
         AxesCallback event object with pixel position information.
      :type axesevent:
         AxesCallback instance
   
      :Example:
         Given an object from class :class:`Annotatedimage` called *annim*,
         register this callback function for the position information with:
   
         >>> annim.interact_imagecolors()
   
      :Notes:
         See *interact_imagecolors()* for more info.
      """
        if axesevent.event.button == 3 and axesevent.event.key in ('', None):
            x, y = axesevent.xdata, axesevent.ydata
            if self.image is None or self.image.im is None:
                return
            xy = self.frame.transData.transform((x, y))
            self.image.xyn_mouse = self.frame.transAxes.inverted().transform(xy)
            x, y = self.image.xyn_mouse
            slope = Annotatedimage.slopetrans * x
            sloperads = numpy.tan(numpy.radians(slope))
            offset = y - Annotatedimage.shifttrans
            self.cmap.modify(sloperads, offset)
            self.callback('slope', slope)
            self.callback('offset', offset)
        return

    def key_imagecolors(self, axesevent, externalkey=None):
        """
   This method catches keys which change the color setting of an image.
   See also documentation at *interact_imagecolors()*.

   :param axesevent:
      AxesCallback event object with pixel position information.
   :type axesevent:
      AxesCallback instance

   :Examples:
      If *image* is an object from :class:`Annotatedimage` then register
      this function with:

      >>> annim = f.Annotatedimage(frame)
      >>> annim.interact_imagecolors()
      """
        if externalkey is not None:
            eventkey = externalkey
        else:
            eventkey = axesevent.event.key
        if eventkey is None:
            return
        else:
            scales = Annotatedimage.lutscales
            scalekeys = Annotatedimage.scalekeys
            scales_default = Annotatedimage.scales_default
            if eventkey in ('pageup', 'pagedown'):
                lm = len(cmlist.colormaps)
                if eventkey == 'pagedown':
                    self.cmindx += 1
                    if self.cmindx >= lm:
                        self.cmindx = 0
                if eventkey == 'pageup':
                    self.cmindx -= 1
                    if self.cmindx < 0:
                        self.cmindx = lm - 1
                newcolormapstr = cmlist.colormaps[self.cmindx]
                self.messenger(newcolormapstr)
                self.cmap.set_source(newcolormapstr)
                self.callback('lut', self.cmindx)
            elif eventkey in scalekeys:
                key = eventkey
                s_indx = scalekeys[key]
                self.cmap.set_scale(scales[s_indx])
                mes = "Color map scale set to '%s'" % scales[s_indx]
                self.messenger(mes)
                self.callback('scale', s_indx)
            elif eventkey == '9':
                if self.cmap.invrt == -1.0:
                    self.cmap.set_inverse(False)
                    self.cmapinverse = False
                    mes = 'Color map not inverted'
                else:
                    self.cmap.set_inverse(True)
                    self.cmapinverse = True
                    mes = 'Color map inverted!'
                self.messenger(mes)
                self.callback('inverse', self.cmapinverse)
            elif eventkey == '0':
                self.cmap.auto = False
                self.messenger('Reset color map to default')
                self.cmap.set_source(cmlist.colormaps[self.startcmindx])
                self.cmap.modify(1.0, 0.0)
                if self.cmap.invrt == -1.0:
                    self.cmap.set_inverse(False)
                    self.cmapinverse = False
                self.cmindx = self.startcmindx
                self.cmap.set_scale(scales[0])
                self.blankcol = Annotatedimage.blankcols[0]
                self.cmap.set_bad(self.blankcol)
                self.cmap.auto = True
                self.cmap.update()
                self.callback('lut', self.cmindx)
                self.callback('inverse', False)
                self.callback('scale', scales_default)
                self.callback('slope', 45.0)
                self.callback('offset', 0.0)
                self.callback('blankcol', 0)
            elif eventkey.upper() == 'B':
                blankcols = Annotatedimage.blankcols
                try:
                    indx = blankcols.index(self.blankcol)
                except:
                    indx = 0

                if indx + 1 == len(blankcols):
                    indx = 0
                else:
                    indx += 1
                self.blankcol = blankcols[indx]
                self.cmap.set_bad(self.blankcol)
                mes = "Color of bad pixels changed to '%s'" % Annotatedimage.blanknames[indx]
                self.messenger(mes)
                self.callback('blankcol', indx)
            elif eventkey.upper() == 'M':
                stamp = datetime.now().strftime('%d%m%Y_%H%M%S')
                filename = self.basename + '_' + stamp + '.lut'
                self.write_colormap(filename)
                mes = 'Save color map to file [%s]' % filename
                self.messenger(mes)
                self.callback('savelut', filename)
            elif eventkey.upper() == 'H':
                if self.histogram:
                    self.set_histogrameq(False)
                    self.messenger('Original image displayed')
                    self.callback('histeq', False)
                else:
                    if self.data_hist is None:
                        self.messenger('Calculating histogram')
                    self.set_histogrameq()
                    self.messenger('Histogram eq. image displayed')
                    self.callback('histeq', True)
            elif eventkey.upper() == 'X':
                self.blurindx += 1
                if self.blurindx >= 10:
                    self.blurindx = 1
                self.blurfac = self.blurindx * 0.5
                mes = 'Blur index: %d blur sigma: %g' % (self.blurindx, self.blurfac)
                self.messenger(mes)
                self.set_blur(nx=self.blurfac, new=True)
                self.callback('blurfac', self.blurfac)
            elif eventkey.upper() == 'Z':
                if self.blurred:
                    self.set_blur(False)
                    self.messenger('Original image displayed')
                    self.callback('blurred', False)
                else:
                    if self.data_blur is None:
                        self.messenger('Calculating smoothed version')
                    self.set_blur(nx=self.blurfac)
                    self.messenger('Smoothed eq. image displayed')
                    self.callback('blurred', True)
            return

    def set_histogrameq(self, on=True):
        if not on:
            self.data = self.data_orig
            self.histogram = False
        else:
            if self.data_hist is None:
                self.histeq()
            self.data = self.data_hist
            self.histogram = True
        if self.image.im is not None:
            self.image.im.set_data(self.data)
        else:
            self.image.data = self.data
        self.cmap.update()
        return

    def set_blur(self, on=True, nx=10, ny=None, new=False):
        if not on:
            self.data = self.data_orig
            self.blurred = False
        else:
            if self.data_blur is None or new:
                self.blur(nx, ny)
            self.data = self.data_blur
            self.blurred = True
        if self.image.im is not None:
            self.image.im.set_data(self.data)
        else:
            self.image.data = self.data
        self.cmap.update()
        return

    def interact_imagecolors(self):
        """
      Add mouse interaction (right mouse button) and keyboard interaction
      to change the colors in an image.

      **MOUSE**

      If you move the mouse in the image for which you did register this
      callback function and press the **right mouse button**
      at the same time, then the color limits for image and colorbar are
      set to a new value.

      The new color setting is calculated as follows: first the position
      of the mouse (x, y) is transformed into normalized coordinates
      (i.e. between 0 and 1) called (xn, yn).
      These values are used to set the slope and offset for a function that
      sets an color for an image value according to the relations:
      ``slope = tan(89 * xn); offset = yn - 0.5``.
      The minimum and maximum values of the image are set by parameters
      *clipmin* and *clipmax*. For a mouse position exactly in the center
      (xn,yn) = (0.5,0.5) the slope is 1.0 and the offset is 0.0 and the
      colors will be divided equally between *clipmin* and *clipmax*.

      **KEYBOARD**

         * **page-down** move forwards through a list with known color maps.
         * **page-up** move backwards through a list with known color maps.
         * **0** resets the colors to the original colormap and scaling.
           The default color map is 'jet'.
         * **i** (or 'I') toggles between **inverse** and normal scaling.
         * **1** sets the colormap scaling to **linear**
         * **2** sets the colormap scaling to **logarithmic**
         * **3** sets the colormap scaling to **exponential**
         * **4** sets the colormap scaling to **square root**
         * **5** sets the colormap scaling to **square**
         * **b** (or 'B') changes color of **bad** pixels.
         * **h** (or 'H') replaces the current data by a **histogram equalized**
           version of this data. This key toggles between the original
           data and the equalized data.
         * **z** (or 'Z') replaces the current data by a **smoothed**
           version of this data. This key is a toggle between
           the original data and the blurred version, smoothed
           with a value of sigma set by key 'x'. Pressing 'x' repeatedly
           increases the smoothing factor. Note that Not a Number (NaN) values
           are smoothed to 0.0.
         * **x** (or 'X") increases the smoothing factor. The number of steps is
           10. Then is starts again with step 1.
         * **m** (or 'M') saves current colormap look up data to a file.
           The default name of the file is the name of file from which the data
           was extracted or the name given in the constructor. The name is
           appended with '.lut'. This data is written in the
           right format so that it can be be (re)used as input colormap.
           This way you can fix a color setting and reproduce the same setting
           in another run of
           a program that allows one to enter a colormap from file.

      If *annim* is an object from class :class:`Annotatedimage` then activate
      color editing with:

      >>> fits = maputils.FITSimage("m101.fits")
      >>> fig = plt.figure()
      >>> frame = fig.add_subplot(1,1,1)
      >>> annim = fits.Annotatedimage(frame)
      >>> annim.Image()
      >>> annim.interact_imagecolors()
      >>> annim.plot()
      """
        self.imagecolorsmouse = AxesCallback(self.mouse_imagecolors, self.frame, 'motion_notify_event')
        self.imagecolorskey = AxesCallback(self.key_imagecolors, self.frame, 'key_press_event')
        self.cmap.auto = True
        self.AxesCallback_ids.append(self.imagecolorskey)
        self.AxesCallback_ids.append(self.imagecolorsmouse)

    def mouse_writepos(self, axesevent):
        """
      Print position information of the position where
      you clicked with the right mouse button while pressing
      the SHIFT key. Print the info on the command line or
      GIPSY command line cq. Log file.
      Register this function with an event handler,
      see example.
   
      :param axesevent:
         AxesCallback event object with pixel position information.
      :type axesevent:
         AxesCallback instance
   
      :Example:
         Register this callback function for object *annim* with:
   
         >>> annim.interact_writepos()
      """
        condition = axesevent.event.button == 1 and axesevent.event.key == 'shift'
        if not condition:
            return
        if self.figmanager.toolbar.mode == '':
            x, y = axesevent.xdata, axesevent.ydata
            spix, swcs, swcsuf, sz = self.positionmessage(x, y, axesevent.posobj, parts=True)
            s = ' '
            if spix:
                s += spix
            if swcs:
                if s:
                    s += ' '
                s += swcs
            if swcsuf:
                if s:
                    s += ' '
                s += swcsuf
            if sz:
                if s:
                    s += ' '
                s += sz
            if s == ' ':
                return
            if axesevent.gipsy and gipsymod:
                if axesevent.g_appendcr:
                    s += '\r'
                if axesevent.g_typecli:
                    typecli(s)
                if axesevent.g_tolog:
                    anyout(s)
            else:
                print s

    def interact_writepos(self, pixfmt='%.1f', dmsprec=1, wcsfmt='%.3g', zfmt='%.3e', hmsdms=True, grids=True, world=True, worlduf=False, imval=True, gipsy=False, g_typecli=False, g_tolog=False, g_appendcr=False):
        """
      Add mouse interaction (left mouse button) to write the position
      of the mouse to screen. The position is written both in pixel
      coordinates and world coordinates.

      
      :param pixfmt:
         Python number format for pixel coordinates
      :type pixfmt:
         String
      :param wcsfmt:
         Python number format for wcs coordinates if the coordinates
         are not spatial or if parameter *hmsdms* is False.
      :type wcsfmt:
         String
      :param zfmt:
         Python number format for image value(s)
      :type pixfmt:
         String
      :param hmsdms:
         If True (default) then spatial coordinates will be formatted
         in hours/degrees, minutes and seconds according to the current sky system.
         The precision in seconds is entered with parameter *dmsprec*.
      :type hmsdms:
         Boolean
      :param dmsprec:
         Number of decimal digits in seconds for coordinates formatted in
         in HMS/DMS
      :type dmsprec:
         Integer
      :param gipsy:
         If set to True, the output is written with GIPSY function anyout() to
         screen and a log file.
      :type gipsy:
         Boolean
      :param typecli:
         If True then write the positions on the Hermes command line instead of the
         log file and screen.
      :type typecli:
         Boolean
      
      :Example:

         >>> fits = maputils.FITSimage("m101.fits")
         >>> fig = plt.figure()
         >>> frame = fig.add_subplot(1,1,1)
         >>> annim = fits.Annotatedimage(frame)
         >>> annim.Image()
         >>> annim.interact_writepos()
         >>> annim.plot()

         For a formatted output one could add parameters to *interact_writepos()*.
         The next line writes no pixel coordinates, writes spatial coordinates
         in degrees (not in HMS/DMS format) and adds a format for
         the world coordinates and the image value(s).

         >>> annim.interact_writepos(pixfmt=None, wcsfmt="%.12f", zfmt="%.3e",
                                    hmsdms=False)
      """
        posobj = Positionmessage(self.projection.skysys, self.skyout, self.projection.types)
        posobj.pixfmt = posobj.wcsfmt = posobj.wcsuffmt = posobj.zfmt = None
        if grids:
            posobj.pixfmt = pixfmt
        if world:
            posobj.wcsfmt = wcsfmt
        if worlduf:
            if wcsfmt:
                posobj.wcsuffmt = wcsfmt
        if imval:
            posobj.zfmt = zfmt
        posobj.hmsdms = hmsdms
        posobj.dmsprec = dmsprec
        if not gipsy:
            g_typecli = False
        self.writeposmouse = AxesCallback(self.mouse_writepos, self.frame, 'button_press_event', gipsy=gipsy, g_typecli=g_typecli, g_tolog=g_tolog, g_appendcr=g_appendcr, posobj=posobj)
        self.AxesCallback_ids.append(self.writeposmouse)
        return

    def motion_events(self):
        """
      Allow this :class:`Annotatedimage` object to interact with the user.
      It reacts on mouse movements. During these movements, a message
      with information about the position of the cursor in pixels
      and world coordinates is displayed on the toolbar.
      """
        self.cidmove = AxesCallback(self.on_move, self.frame, 'motion_notify_event')
        self.AxesCallback_ids.append(self.cidmove)

    def key_events(self):
        """
      Allow this :class:`Annotatedimage` object to interact with the user.
      using keys.
      """
        self.cidkey = AxesCallback(self.key_pressed, self.frame, 'key_press_event')
        self.AxesCallback_ids.append(self.cidkey)

    def click_events(self):
        """
      Allow this :class:`Annotatedimage` object to interact with the user.
      It reacts on pressing the left mouse button and prints a message
      to stdout with information about the position of the cursor in pixels
      and world coordinates.
      """
        self.cidclick = AxesCallback(self.on_click, self.frame, 'button_press_event')
        self.AxesCallback_ids.append(self.cidclick)

    def positionsfromfile(self, filename, comment, skyout=None, **kwargs):
        """
      Read positions from a file with world coordinates and convert them to
      pixel coordinates. The interface is exactly the same as from method
      :meth:`tabarray.readColumns()`

      It expects that the first column you specify contains the longitudes and
      the second column that is specified the latitudes.

      :param filename:
         Name (and pahth if necessary) of the file which contains longitudes
         and latitudes.
      :type filename:
         String
      :param comment:
         Comment characters. If a line starts with a comment character,
         it will be skipped.
      :type comment:
         String
      :param skyout:
         Tell the system in what sky system your longitudes and latitudes are.
      :type skyout:
         Sky definition
      :param kwargs:
         Keywords for Tabarray's method readColumns.
      :type kwargs:
         Python keyword arguments

      :Examples:
      
         >>> fn = 'smallworld.txt'
         >>> xp, yp = annim.positionsfromfile(fn, 's', cols=[0,1])
         >>> frame.plot(xp, yp, ',', color='#FFDAAA')

         Or: your graticule is equatorial but the coordinates in the file are
         galactic:
         
         >>> xp, yp = annim.positionsfromfile(fn, 's', skyout='ga', cols=[0,1])
      """
        ainv = self.projection.allow_invalid
        if skyout is not None:
            skyout_old = self.projection.skyout
            self.projection.skyout = skyout
        self.projection.allow_invalid = True
        lon, lat = readColumns(filename, comment, **kwargs)
        xp, yp = self.projection.topixel((lon, lat))
        xp = numpy.ma.masked_where(numpy.isnan(xp) | (xp > self.pxlim[1]) | (xp < self.pxlim[0]), xp)
        yp = numpy.ma.masked_where(numpy.isnan(yp) | (yp > self.pylim[1]) | (yp < self.pylim[0]), yp)
        self.projection.allow_invalid = ainv
        if skyout is not None:
            self.projection.skyout = skyout_old
        return (
         xp, yp)

    def getflux(self, xy, pixelstep=None):
        if pixelstep is None:
            pixelstep = self.pixelstep
        poly = numpy.asarray(xy)
        mm = poly.min(0)
        xmin = mm[0]
        ymin = mm[1]
        mm = poly.max(0)
        xmax = mm[0]
        ymax = mm[1]
        xmin = numpy.floor(xmin)
        xmax = numpy.ceil(xmax)
        ymin = numpy.floor(ymin)
        ymax = numpy.ceil(ymax)
        Y = numpy.arange(ymin, ymax + 1, pixelstep)
        X = numpy.arange(xmin, xmax + 1, pixelstep)
        l = int(xmax - xmin + 1)
        b = int(ymax - ymin + 1)
        numpoints = len(X) * len(Y)
        x, y = numpy.meshgrid(X, Y)
        pos = list(zip(x.flatten(), y.flatten()))
        pos = numpy.asarray(pos)
        if mploldversion:
            mask = nxutils.points_inside_poly(pos, poly)
        else:
            polypath = path.Path(xy)
            mask = polypath.contains_points(pos)
        i = numpy.arange(len(pos), dtype='int')
        posm = pos[i[numpy.where(mask)]]
        xy = posm.T
        x = xy[0]
        y = xy[1]
        xcor = self.pxlim[0] - 0.5
        ycor = self.pylim[0] - 0.5
        x = numpy.asarray(x - xcor, dtype='int')
        y = numpy.asarray(y - ycor, dtype='int')
        z = self.data[(y, x)]
        area = len(posm) * pixelstep * pixelstep
        sum = z.sum() * (pixelstep * pixelstep)
        return (
         area, sum)


class FITSaxis(object):
    """
This class defines objects which store WCS information from a FITS
header. It includes axis number and alternate header information
in a FITS keyword.
    
:param axisnr:
   FITS axis number. For this number the relevant keys in the header
   are read.
:type axisnr:
   Integer
:param hdr:
   FITS header
:type hdr:
   pyfits.NP_pyfits.Header instance

   
:Methods:

.. automethod:: printattr
.. automethod:: printinfo

   """

    def __init__(self, axisnr, hdr, alter):

        def makekey(key, alternate=True):
            s = '%s%d' % (key, axisnr)
            if alter != '' and alternate:
                s += alter
            return s

        ax = makekey('CTYPE')
        self.ctype = 'Unknown'
        self.axname = 'Unknown'
        self.axext = ''
        if ax in hdr:
            self.ctype = hdr[ax].upper()
            info = hdr[ax].split('-')
            self.axname = info[0].upper()
            if len(info) > 1:
                ext = info[(-1)].upper()
                extlist = {'ARC': 'Zenithal equidistant projection', 'AIR': 'Airy projection', 
                   'AZP': 'Slant zenithal (azimuthal) perspective projection', 
                   'AIT': 'Hammer Aitoff projection', 
                   'BON': "Bonne's equal area projection", 
                   'CAR': 'Plate Carree', 
                   'CEA': "Lambert's equal area projection", 
                   'COD': 'Conic equidistant projection', 
                   'COE': 'Conic equal area projection', 
                   'COO': 'Conic orthomorfic projection', 
                   'COP': 'Conic perspective projection', 
                   'CSC': 'COBE quadrilateralized spherical cube projection', 
                   'CYP': "Gall's stereographic projection", 
                   'MER': "Mercator's projection", 
                   'MOL': "Mollweide's projection", 
                   'NCP': 'Northern celestial pole projection', 
                   'PAR': 'Parabolic projection', 
                   'PCO': 'Polyconic', 
                   'POL': 'Polyconic projection', 
                   'QSC': 'Quadrilateralized spherical cube projection', 
                   'SIN': 'Slant orthograpic projection', 
                   'SFL': 'Sanson-Flamsteed projection', 
                   'STG': 'Stereographic projection', 
                   'SZP': 'Slant zenithal perspective', 
                   'TAN': 'Gnomonic projection', 
                   'TSC': 'Tangential spherical cube projection', 
                   'ZEA': 'Zenith equal area projection', 
                   'ZPN': 'Zenithal polynomial projection'}
                self.axext = ext
                if ext in extlist:
                    self.axext += ' (' + extlist[ext] + ')'
        else:
            self.ctype = 'X%d' % axisnr
            self.axname = self.ctype
        ai = makekey('NAXIS', alternate=False)
        self.axlen = hdr[ai]
        self.axisnr = axisnr
        self.axstart = 1
        self.axend = self.axlen
        ai = makekey('CDELT')
        if ai in hdr:
            self.cdelt = hdr[ai]
        else:
            self.cdelt = 1.0
        ai = makekey('CRVAL')
        if ai in hdr:
            self.crval = hdr[ai]
        else:
            self.crval = 1.0
        ai = makekey('CUNIT')
        if ai in hdr:
            self.cunit = hdr[ai]
        else:
            self.unit = '?'
        ai = makekey('CRPIX')
        if ai in hdr:
            self.crpix = hdr[ai]
        else:
            self.crpix = self.axlen / 2
        ai = makekey('CROTA')
        self.crota = 0
        if ai in hdr:
            self.crota = hdr[ai]
        self.wcstype = None
        self.wcsunits = None
        self.outsidepix = None
        return

    def printattr(self):
        """
   Print formatted information for this axis.
   
   :Examples:
      
   >>> from kapteyn import maputils
   >>> fitsobject = maputils.FITSimage('rense.fits')
   >>> fitsobject.hdr
   <pyfits.NP_pyfits.Header instance at 0x1cae3170>
   >>> ax1 = maputils.FITSaxis(1, fitsobject.hdr)
   >>> ax1.printattr()
   axisnr     - Axis number:  1
   axlen      - Length of axis in pixels (NAXIS):  100
   ctype      - Type of axis (CTYPE):  RA---NCP
   axname     - Short axis name:  RA
   cdelt      - Pixel size:  -0.007165998823
   crpix      - Reference pixel:  51.0
   crval      - World coordinate at reference pixel:  -51.2820847959
   cunit      - Unit of world coordinate:  DEGREE
   wcstype    - Axis type according to WCSLIB:  None
   wcsunits   - Axis units according to WCSLIB:  None
   outsidepix - A position on an axis that does not belong to an image:  None
   
   If we set the image axes in *fitsobject* then the WCS attributes
   will get a value also. This object stores its FITSaxis objects in a list
   called *axisinfo[]*. The index is the required FITS axis number.
   
   >>> fitsobject.set_imageaxes(1, 2, 30)
   >>> fitsobject.axisinfo[1].printattr()
   ..........
   wcstype    - Axis type according to WCSLIB:  longitude
   wcsunits   - Axis units according to WCSLIB:  deg
   outsidepix - A position on an axis that does not belong to an image:  None

      """
        s = 'axisnr     - Axis number: %s\n' % self.axisnr + 'axlen      - Length of axis in pixels (NAXIS): %s\n' % self.axlen + 'axstart    - First pixel coordinate: %s\n' % self.axstart + 'axend      - Last pixel coordinate: %s\n' % self.axend + 'ctype      - Type of axis (CTYPE): %s\n' % self.ctype + 'axname     - Short axis name: %s\n' % self.axname + 'axext      - Axis extension: : %s\n' % self.axext + 'cdelt      - Pixel size: %s\n' % self.cdelt + 'crpix      - Reference pixel: %s\n' % self.crpix + 'crval      - World coordinate at reference pixel: %s\n' % self.crval + 'cunit      - Unit of world coordinate: %s\n' % self.cunit + 'crota      - Rotation of axis: %s\n' % self.crota + 'wcstype    - Axis type according to WCSLIB: %s\n' % self.wcstype + 'wcsunits   - Axis units according to WCSLIB: %s\n' % self.wcsunits + 'outsidepix - A position on an axis that does not belong to an image: %s\n' % self.outsidepix
        return s

    def printinfo(self):
        """
   Print formatted information for this axis.
   
   :Examples:
   
      >>> from kapteyn import maputils
      >>> fitsobject = maputils.FITSimage('rense.fits')
      >>> ax1 = maputils.FITSaxis(1, fitsobject.hdr)
      >>> ax1.printinfo()
      Axis 1: RA---NCP  from pixel 1 to   512
      {crpix=257 crval=178.779 cdelt=-0.0012 (DEGREE)}
      {wcs type=longitude, wcs unit=deg}
      Axis 2: DEC--NCP  from pixel 1 to   512
      {crpix=257 crval=53.655 cdelt=0.00149716 (DEGREE)}
      {wcs type=latitude, wcs unit=deg}
      

   :Notes:
      if attributes for a :class:`maputils.FITSimage` object are changed
      then the relevant axis properties are updated.
      So this method can return different results depending
      on when it is used.
      """
        a = self
        s = 'Axis %d: %-9s from pixel %5d to %5d\n  {crpix=%d crval=%G cdelt=%g (%s)}\n  {wcs type=%s, wcs unit=%s}' % (
         a.axisnr,
         a.ctype,
         a.axstart,
         a.axend,
         a.crpix,
         a.crval,
         a.cdelt,
         a.cunit,
         a.wcstype,
         a.wcsunits)
        return s


class FITSimage(object):
    """
This class extracts 2D image data from FITS files. It allows for
external functions to prompt users for relevant input like the
name of the FITS file, which header in that file should be used,
the axis numbers of the image axes, the pixel
limits and a spectral translation if one of the selected axes
is a spectral axis.
All the methods in this class that allow these external functions
for prompting can also be used without these functions. Then one needs
to know the properties of the FITS data beforehand.
   
:param filespec:
   A default file either to open directly
   or to be used in a prompt as default file. This variable
   should have a value if no external function is used to prompt a user.
:type filespec:
   String
:param promptfie:
   A user supplied function which should prompt a
   user for some data, opens the FITS file and returns the hdu
   list and a user selected index for the header from this hdu
   list. An example of a function supplied by
   :mod:`maputils` is function :func:`prompt_fitsfile`
:type promptfie:
   Python function
:param hdunr:
   A preset of the index of the header from the hdu list.
   If this variable is set then it should not prompted for in the
   user supplied function *promptfie*.
:type hdunr:
   Integer
:param alter:
   Selects an alternate header for the world coordinate system.
   Default is the standard header.
   Keywords in alternate headers end on a character A..Z
:type alter:
   Empty or a single character. Input is case insensitive.
:param memmap:
   Set the memory mapping for PyFITS. The default is copied from the
   default in your version of PyFITS. If you want to be sure it is on
   then specify *memmap=1*
:type memmap:
   Boolean
:param externalheader:
   If defined, then it is a header from an external source e.g. a user
   defined header.
:type externalheader:
   Python dictionary
:param externaldata:
   If defined, then it is data from an external source e.g. user
   defined data or processed data in a numpy array. A user/programmer
   should check if the shape of the numpy array fits the sizes given
   in FITS keywords *NAXISn*.
:type externaldata:
   Numpy array
:param parms:
   Extra parameters for PyFITS's *open()* method, such as
   *uint16*, *ignore_missing_end*, *checksum*, see PyFITS documentation
   for their meaning.
:type parms:
   keyword arguments

:Attributes:
   
    .. attribute:: filename

       Name of the FITS file (read-only).
       
    .. attribute:: hdr

       Header as read from the header (read-only).
       
    .. attribute:: naxis

       Number of axes (read-only).
       
    .. attribute:: dat

       The raw image data (not sliced, swapped or limited in range).
       The required sliced image data is stored in attribute :attr:`boxdat`.
       This is a read-only attribute. 
       
    .. attribute:: axperm

       Axis permutation array. These are the (FITS) axis numbers of your
       image x & y axis.

    .. attribute:: wcstypes

       Type of the axes in this data. The order is the same as of the axes.
       The types ara strings and are derived from attribute wcstype of the
       Projection object. The types are:
       'lo' is longitude axis. 'la' is latitude axis,
       'sp' is spectral axis. 'li' is a linear axis. Appended to 'li' is an
       underscore and the ctype of that axis (e.g. 'li_stokes').
       
    .. attribute:: mixpix

       The missing pixel if the image has only one spatial axis. The other
       world coordinate could be calculated with a so called *mixed* method
       which allows for one world coordinate and one pixel.
       
    .. attribute:: axisinfo

       A list with :class:`FITSaxis` objects. One for each axis. The index is
       an axis number (starting at 1).
       
    .. attribute:: slicepos

       A list with positions on axes in the FITS file which do not belong to
       the required image.
       
    .. attribute:: pxlim

       Axis limit in pixels. This is a tuple or list (xlo, xhi).
       
    .. attribute:: pylim

       Axis limit in pixels. This is a tuple or list (xlo, xhi).
       
    .. attribute:: boxdat

       The image data. Possibly sliced, axis swapped and limited in axis range.
       
    .. attribute:: imshape

       Sizes of the 2D array in :attr:`boxdat`.
       
    .. attribute:: spectrans

       A string that sets the spectra translation. If one uses the prompt function
       for the image axes, then you will get a list of possible translations for the
       spectral axis in your image.

    .. attribute:: proj

       An object from :class:`wcs.Projection`. This object is the result of the call:
       ``proj = wcs.Projection(self.hdr)``, so it is the Projection object that involves all
       the axes in the FITS header.
    
    .. attribute:: convproj

       An object from :class:`wcs.Projection`. This object is needed to
       be able to use methods *toworld()* and *topixel()* for the
       current image.
       
    .. attribute:: figsize

       A suggested figure size (inches) in X and Y directions.
       
    .. attribute:: aspectratio

       Plot a circle in **world coordinates** as a circle. That is, if the
       pixel size in the FITS header differs in X and Y, then correct
       the (plot) size of the pixels with value *aspectratio*
       so that features in an image have the correct sizes in longitude and
       latitude in degrees.
      
:Notes:
   The object is initialized with a default position for a data slice if
   the dimension of the FITS data is > 2. This position is either the value
   of CRPIX from the header or 1 if CRPIX is outside the range [1, NAXIS].

   Values -inf and +inf in a dataset are replaced by NaN's (not a number number).
   We know that Matplotlib's methods have problems with these values, but these
   methods can deal with NaN's.

:Examples:
   PyFITS allows URL's to retrieve FITS files. It can also read gzipped files e.g.:
   
      >>> f = 'http://www.atnf.csiro.au/people/mcalabre/data/WCS/1904-66_ZPN.fits.gz'
      >>> fitsobject = maputils.FITSimage(f)
      >>> print fitsobject.str_axisinfo()
      Axis 1: RA---ZPN  from pixel 1 to   192
        {crpix=-183 crval=0 cdelt=-0.0666667 (Unknown)}
        {wcs type=longitude, wcs unit=deg}
      Axis 2: DEC--ZPN  from pixel 1 to   192
        {crpix=22 crval=-90 cdelt=0.0666667 (Unknown)}
        {wcs type=latitude, wcs unit=deg}

   Use Maputil's prompt function :func:`prompt_fitsfile` to get
   user interaction for the FITS file specification.
   
      >>> fitsobject = maputils.FITSimage(promptfie=maputils.prompt_fitsfile)

:Methods:

.. index:: Select image data from FITS file
.. automethod:: set_imageaxes
.. index:: Set pixel limits of image axes
.. automethod:: set_limits
.. index:: Set spectral translation
.. automethod:: set_spectrans
.. index:: Set output sky
.. automethod:: set_skyout
.. index:: A class for plotting FITS data
.. automethod:: Annotatedimage
.. index:: Aspect ratio from FITS header data
.. automethod:: get_pixelaspectratio
.. index:: Set default figure size for Matplotlib
.. automethod:: get_figsize
.. index:: Print information from FITS header
.. automethod:: str_header
.. automethod:: str_axisinfo
.. automethod:: str_wcsinfo
.. automethod:: str_spectrans
.. automethod:: get_dataminmax
.. automethod:: slice2world
.. automethod:: header2classic
.. automethod:: reproject_to
.. automethod:: writetofits

   """

    def __init__(self, filespec=None, promptfie=None, prompt=True, hdunr=None, alter='', memmap=None, externalheader=None, externaldata=None, externalname='artificial', **parms):
        if externalheader is not None:
            self.hdr = externalheader
            self.bitpix, self.bzero, self.bscale, self.blank = getscale(self.hdr)
            self.filename = externalname
            if externaldata is not None:
                if 'int' in externaldata.dtype.name:
                    self.dat = externaldata.astype(numpy.float32)
                else:
                    self.dat = externaldata
            else:
                self.dat = None
        else:
            if promptfie:
                if memmap is None:
                    hdulist, hdunr, filename, alter = promptfie(filespec, prompt, hdunr, alter)
                else:
                    hdulist, hdunr, filename, alter = promptfie(filespec, prompt, hdunr, alter, memmap)
            else:
                try:
                    if memmap is None:
                        hdulist = pyfits.open(filespec, **parms)
                    else:
                        hdulist = pyfits.open(filespec, memmap=memmap, **parms)
                    filename = filespec
                except IOError as xxx_todo_changeme:
                    errno, strerror = xxx_todo_changeme.args
                    print 'Cannot open FITS file: I/O error(%s): %s' % (errno, strerror)
                    raise
                except:
                    print 'Cannot open file, unknown error!'
                    raise

                if hdunr is None:
                    hdunr = 0
                self.hdunr = hdunr
                hdu = hdulist[hdunr]
                self.filename = filename
                self.hdr = hdu.header
                self.bitpix, self.bzero, self.bscale, self.blank = getscale(self.hdr)
                if externaldata is None:
                    if 'int' in hdu.data.dtype.name:
                        self.dat = hdu.data.astype(numpy.float32)
                    else:
                        self.dat = hdu.data
                else:
                    self.dat = externaldata
                hdulist.close()
            self.alter = alter.upper()
            self.naxis = self.hdr['NAXIS']
            if self.naxis < 2:
                print 'You need at least two axes in your FITS file to extract a 2D image.'
                print 'Number of axes in your FITS file is %d' % (self.naxis,)
                hdulist.close()
                raise Exception('Number of data axes must be >= 2.')
            self.axperm = [
             1, 2]
            self.mixpix = None
            axinf = {}
            for i in range(self.naxis):
                axisnr = i + 1
                axinf[axisnr] = FITSaxis(axisnr, self.hdr, self.alter)

            self.axisinfo = axinf
            slicepos = []
            sliceaxnames = []
            sliceaxnums = []
            n = self.naxis
            if n > 2:
                for i in range(n):
                    axnr = i + 1
                    if axnr not in self.axperm:
                        crpix = self.axisinfo[axnr].crpix
                        if crpix < 1 or crpix > self.axisinfo[axnr].axlen:
                            crpix = 1
                        slicepos.append(crpix)
                        sliceaxnames.append(self.axisinfo[axnr].axname)
                        sliceaxnums.append(axnr)

            self.slicepos = slicepos
            self.sliceaxnames = sliceaxnames
            self.sliceaxnums = sliceaxnums
            n1 = self.axisinfo[self.axperm[0]].axlen
            n2 = self.axisinfo[self.axperm[1]].axlen
            self.pxlim = [1, n1]
            self.pylim = [1, n2]
            self.proj = wcs.Projection(self.hdr, alter=self.alter)
            for i in range(n):
                ax = i + 1
                self.axisinfo[ax].wcstype = self.proj.types[i]
                self.axisinfo[ax].wcsunits = self.proj.units[i]
                self.axisinfo[ax].cdelt = self.proj.cdelt[i]
                self.axisinfo[ax].crval = self.proj.crval[i]
                self.axisinfo[ax].ctype = self.proj.ctype[i]
                self.axisinfo[ax].cunit = self.proj.cunit[i]
                self.axisinfo[ax].crpix = self.proj.crpix[i]

            wcstypes = []
            for i in range(n):
                ax = i + 1
                if self.proj.lonaxnum is not None and ax == self.proj.lonaxnum:
                    wcstypes.append('lo')
                elif self.proj.lataxnum is not None and ax == self.proj.lataxnum:
                    wcstypes.append('la')
                elif self.proj.specaxnum is not None and ax == self.proj.specaxnum:
                    wcstypes.append('sp')
                else:
                    wcstypes.append('li_' + str(self.proj.ctype[i]))

        self.wcstypes = wcstypes
        self.spectrans = None
        self.skyout = None
        self.boxdat = self.dat
        self.set_imageaxes(self.axperm[0], self.axperm[1], self.slicepos)
        self.aspectratio = None
        self.pixelaspectratio = self.get_pixelaspectratio()
        self.figsize = None
        return

    def slice2world(self, skyout=None, spectra=None, userunits=None):
        """
      Given the pixel coordinates of a slice, return the world
      coordinates of these pixel positions and their units.
      For example in a 3-D radio cube with axes RA-DEC-FREQ one can have
      several RA-DEC images as function of FREQ. This FREQ is given
      in pixels coordinates in attribute *slicepos*. The world coordinates
      are calculated using the Projection object which is
      also an attribute.

      :param skyout:
         Set current projection object in new output sky mode
      :type skyout:
         String or tuple representing sky definition

      :param spectra:
         Use this spectral translation for the output world coordinates
      :type spectra:
         String

      :param userunits:
         A sequence of units as the user wants to have it appear
         in the slice info string. The order of these units must
         be equal to the order of the axes outside the slice/subset.
         Both the world coordinates and the units are adjusted. 
      :type userunits:
         String
          
      :Returns:
         A tuple with two elements: *world* and *units*.
         Element *world* is either an empty list or a list with
         one or more world coordinates. The number of coordinates is
         equal to the number of axes in a data set that do not
         belong to the extracted data which can be a slice.
         For each world coordinate there is a unit in element *units*.

      :Note:
         This method first calculates a complete set of world coordinates.
         Where it did not define a slice position, it takes the header
         value *CRPIXn*. So if a map is defined with only one spatial axes and
         the missing spatial axis is found in *slicepos* than we have two
         matching pixel coordinates for which we can calculate world coordinates.
         So by definition, if a slice is a function of a spatial
         coordinate, then its world coordinate is found by using the matching
         pixel coordinate which, in case of a spatial map, corresponds to the
         projection center.

      :Example:
      
         >>> vel, uni = fitsobj.slice2world(spectra="VOPT-???")
         >>> velinfo = "ch%d = %.1f km/s" % (ch, vel[0]/1000.0)

         or:
         >>> vel, uni = fitsobj.slice2world(spectra="VOPT-???", userunits="km/s")
      """
        if self.slicepos is None:
            return (None, None)
        else:
            pix = []
            units = []
            world = []
            j = 0
            skyout_old = self.proj.skyout
            if skyout is not None:
                self.proj.skyout = skyout
            if spectra is not None:
                newproj = self.proj.spectra(spectra)
            else:
                newproj = self.proj
            for i in range(self.naxis):
                if i + 1 in self.axperm:
                    pix.append(self.proj.crpix[i])
                else:
                    pix.append(self.slicepos[j])
                    j += 1

            wor = newproj.toworld(tuple(pix))
            for i in range(self.naxis):
                if i + 1 not in self.axperm:
                    world.append(wor[i])
                    units.append(newproj.cunit[i])

            if skyout is not None:
                self.proj.skyout = skyout_old
            if userunits is not None:
                sworld = []
                sunits = []
                if not issequence(userunits):
                    userunits = [
                     userunits]
                for w, u, uu in zip(world, units, userunits):
                    if uu is not None:
                        uf, errmes = unitfactor(u, uu)
                        if uf is None:
                            raise ValueError(errmes)
                        else:
                            w *= uf
                            u = uu
                    sworld.append(w)
                    sunits.append(u)

            else:
                sworld = world
                sunits = units
            return (
             sworld, sunits)

    def get_dataminmax(self, box=False):
        """
      Get minimum and maximum value of data in entire data structure
      defined by the current FITS header or in a slice. 
      These values can be important if
      you want to compare different images from the same source
      (e.g. channel maps in a radio data cube).

      :param box:
         Find min, max in data or if set to True in data slice (with limits).
      :type box:
         Boolean
         
      :Returns:
         min, max, two floating point numbers representing the minimum
         and maximum data value in data units of the header (*BUNIT*).

      :Note:
         We assume here that the data is read when a FITSobject was created.
         Then the data is filtered and the -inf, inf values are replaced 
         by NaN's.
         
      :Example:
         Note the difference between the min, max of the entire data or the
         min, max of the slice (limited by a box)::
   
            fitsobj = maputils.FITSimage('ngc6946.fits')
            vmin, vmax = fitsobj.get_dataminmax()
            for i, ch in enumerate(channels):
               fitsobj.set_imageaxes(lonaxnum, lataxnum, slicepos=ch)
               print "Min, max in this channel: ", fitsobj.get_dataminmax(box=True)

      """
        if box:
            if self.boxdat is None:
                return (0, 1)
            mask = numpy.isfinite(self.boxdat)
            mi = numpy.min(self.boxdat[mask])
            ma = numpy.max(self.boxdat[mask])
        else:
            mask = numpy.isfinite(self.dat)
            mi = numpy.min(self.dat[mask])
            ma = numpy.max(self.dat[mask])
        return (
         mi, ma)

    def str_header(self):
        """
      Print the meta information from the selected header.
      Omit items of type *HISTORY*. It prints both real FITS headers
      and headers given by a dictionary.

      :Returns:
         A string with the header keywords

      :Examples:
         If you think a user needs more information from the header than
         can be provided with method :meth:`str_axisinfo` it can be useful to
         display the contents of the selected FITS header.
         This is the entire header and not a selected alternate header.

         >>> from kapteyn import maputils
         >>> fitsobject = maputils.FITSimage('rense.fits')
         >>> print fitsobject.str_header()
         SIMPLE  =                    T / SIMPLE FITS FORMAT
         BITPIX  =                  -32 / NUMBER OF BITS PER PIXEL
         NAXIS   =                    3 / NUMBER OF AXES
         NAXIS1  =                  100 / LENGTH OF AXIS
         NAXIS2  =                  100 / LENGTH OF AXIS
         NAXIS3  =                  101 / LENGTH OF AXIS
         BLOCKED =                    T / TAPE MAY BE BLOCKED
         CDELT1  =  -7.165998823000E-03 / PRIMARY PIXEL SEPARATION
         CRPIX1  =   5.100000000000E+01 / PRIMARY REFERENCE PIXEL
         CRVAL1  =  -5.128208479590E+01 / PRIMARY REFERENCE VALUE
         CTYPE1  = 'RA---NCP          ' / PRIMARY AXIS NAME
         CUNIT1  = 'DEGREE            ' / PRIMARY AXIS UNITS
         etc. etc.

      """
        st = ''
        if isinstance(self.hdr, dict):
            keylist = list(self.hdr.keys())
            keylist.sort()
            for k in keylist:
                s = self.hdr[k]
                if not str(s).startswith('HISTORY'):
                    if isinstance(s, six.string_types):
                        val = "'" + '%-18s' % s + "'"
                    else:
                        val = '%+20s' % str(s)
                    st += '%-8s' % k + '= ' + val + ' /\n'

        else:
            for s in self.hdr.ascardlist():
                if not str(s).startswith('HISTORY'):
                    st += '%s\n' % s

        return st

    def str_axisinfo(self, axnum=None, long=False):
        """
      For each axis in the FITS header, return a string with the data related
      to the World Coordinate System (WCS).

      :param axnum:
         A list with axis numbers for which one wants to print information.
         These axis numbers are FITS numbers i.e. in range [1,NAXIS].
         To display information about the two image axes one should use
         attribute :attr:`maputils.FITSimage.axperm` as in the second example
         below.
      :type axnum:
         None, Integer or list with Integers
      :param long:
         If *True* then more verbose information is printed.
      :type long:
         Boolean

      :Returns:
         A string with WCS information for each axis in *axnum*.

      :Examples:
         Print useful header information after the input of the FITS file
         and just before the specification of the image axes:

         >>> from kapteyn import maputils
         >>> fitsobject = maputils.FITSimage('rense.fits')
         >>> print fitsobject.str_axisinfo()
         Axis 1: RA---NCP  from pixel 1 to   100
           {crpix=51 crval=-51.2821 cdelt=-0.007166 (DEGREE)}
           {wcs type=longitude, wcs unit=deg}
         Axis 2: DEC--NCP  from pixel 1 to   100
           {crpix=51 crval=60.1539 cdelt=0.007166 (DEGREE)}
           {wcs type=latitude, wcs unit=deg}
         Axis 3: VELO-HEL  from pixel 1 to   101
           {crpix=-20 crval=-243 cdelt=4200 (km/s)}
           {wcs type=spectral, wcs unit=m/s}

         Print extended information for the two image axes only:
      
         >>> print str_axisinfo(axnum=fitsobject.axperm, long=True)

        
      :Notes:
         For axis numbers outside the range of existing axes
         in the FITS file, nothing will be printed. No exception
         will be raised.
      """
        if axnum is None:
            axnum = list(range(1, self.naxis + 1))
        if not issequence(axnum):
            axnum = [
             axnum]
        s = ''
        l = len(axnum)
        for i, ax in enumerate(axnum):
            if ax >= 1 and ax <= self.naxis:
                a = self.axisinfo[ax]
                if int:
                    s += a.printattr()
                else:
                    s += a.printinfo()
                if i < l - 1:
                    s += '\n'

        return s

    def str_wcsinfo(self):
        """
      Compose a string with information about
      the data related to the current World Coordinate System (WCS)
      (e.g. which axes are
      longitude, latitude or spectral axes)

      :Returns:
         String with WCS information for the current Projection
         object.

      :Examples: Print information related to the world coordinate system:

         >>> print fitsobject.str_wcsinfo()
         Current sky system:                 Equatorial
         reference system:                   ICRS
         Output sky system:                  Equatorial
         Output reference system:            ICRS
         projection's epoch:                 J2000.0
         Date of observation from DATE-OBS:  2002-04-04T09:42:42.1
         Date of observation from MJD-OBS:   None
         Axis number longitude axis:         1
         Axis number latitude axis:          2
         Axis number spectral axis:          None
         Allowed spectral translations:      None

      """
        s = ''
        sys, ref, equinox, epoch = skyparser(self.convproj.skysys)
        if sys is not None:
            s += 'Native sky system:                 %s\n' % skyrefsystems.id2fullname(sys)
        if ref is not None:
            s += 'Native reference system:           %s\n' % skyrefsystems.id2fullname(ref)
        if equinox is not None:
            s += 'Native Equinox:                    %s\n' % equinox
        if epoch is not None:
            s += 'Native date of observation:        %s\n' % epoch
        sys, ref, equinox, epoch = skyparser(self.convproj.skyout)
        if sys is not None:
            s += 'Output sky system:                 %s\n' % skyrefsystems.id2fullname(sys)
        if ref is not None:
            s += 'Output reference system:           %s\n' % skyrefsystems.id2fullname(ref)
        if equinox is not None:
            s += 'Output Equinox:                    %s\n' % equinox
        if epoch is not None:
            s += 'Output date of observation:        %s\n' % epoch
        s += "Projection's epoch:                %s\n" % self.convproj.epoch
        s += 'Date of observation from DATE-OBS: %s\n' % self.convproj.dateobs
        s += 'Date of observation from MJD-OBS:  %s\n' % self.convproj.mjdobs
        s += 'Axis number longitude axis:        %s\n' % self.convproj.lonaxnum
        s += 'Axis number latitude axis:         %s\n' % self.convproj.lataxnum
        s += 'Axis number spectral axis:         %s\n' % self.convproj.specaxnum
        s += 'Selected spectral translation:     %s\n' % self.spectrans
        return s

    def str_spectrans(self):
        """
      Compose a string with the possible spectral translations for this data.

      :Returns:
         String with information about the allowed spectral
         translations for the current Projection object.

      :Examples: Print allowed spectral translations:

         >>> print fitsobject.str_spectrans()
      
      """
        s = ''
        isspectral = False
        for ax in self.axperm:
            if self.axisinfo[ax].wcstype == 'spectral':
                isspectral = True

        if not isspectral:
            return
        i = 0
        for st, un in self.convproj.altspec:
            s += '%d   %s (%s)\n' % (i, st, un)
            i += 1

        return s

    def getaxnumberbyname(self, axname):
        """
      Given an axis specification,  
      convert to the corresponding axis number. If the input was a number,
      then return this number. Note that there is no check on
      multiple matches of the minimal matched string.
      The string matching is case insensitive.

      :param axname:   The name of one of the axis in the header of this
                       object.
      :type axname:    String or Integer
      """
        if not isinstance(axname, six.string_types):
            return axname
        else:
            n = self.naxis
            axnumber = None
            for i in range(n):
                ax = i + 1
                str2 = self.axisinfo[ax].axname
                if str2.find(string_upper(axname), 0, len(axname)) > -1:
                    axnumber = ax
                    break

            if axnumber is None:
                raise ValueError('Axis name [%s] is not found in the header' % axname)
            return axnumber

    def set_imageaxes(self, axnr1=None, axnr2=None, slicepos=None, promptfie=None):
        """
      A FITS file can contain a data set of dimension n.
      If n < 2 we cannot display the data without more information.
      If n == 2 the data axes are those in the FITS file, Their numbers are 1 and 2.
      If n > 2 then we have to know the numbers of those axes that
      are part of the image. For the other axes we need to know a
      pixel position so that we are able to extract a data slice.

      Attribute :attr:`dat` is then always a 2D array.

      :param axnr1:
         Axis number of first image axis (X-axis). If it is a string, then
         the number of the first axis which matches is returned. The string match
         is minimal and case insensitive. 
      :type axnr1:
         Integer or String
      :param axnr2:
         Axis number of second image axis (Y-axis). If it is a string, then
         the number of the first axis which matches is returned. The string match
         is minimal and case insensitive.
      :type axnr2:
         Integer or String
      :param slicepos:
         list with pixel positions on axes outside the image at which
         an image is extracted from the data set. Applies only to data sets with
         dimensions > 2. The length of the list must be equal to the number
         of axes in the data set that are not part of the image.
      :type slicepos:
         Integer or sequence of integers
      :param spectrans:
         The spectral translation to convert between different spectral types
         if one of the image axes has spectral type.
      :type spectrans:
         Integer
      :param promptfie:
         A Function that for in an Interactive Environment (fie),
         supplied by the user, that can
         prompt a user to enter the values for axnr1, axnr2
         and slicepos. An example of a function supplied by
         :mod:`maputils` is function :func:`prompt_imageaxes`

      :Raises:
         :exc:`Exception`
            *One axis number is missing and no prompt function is given!*

         :exc:`Exception`
            *Missing positions on axes outside image!* -- Somehow there are not
            enough elements in parameter *slicepos*. One should supply
            as many pixel positions as there are axes in the FITS data
            that do not belong to the selected image.

         :exc:`Exception`
            *Cannot find a matching axis for the spatial axis!* -- The matching
            spatial axis for one of the image axes could not be found
            in the FITS header. It will not be possible to get
            useful world coordinates for the spatial axis in your image.

      **Modifies attributes:**
          .. attribute:: axisinfo
          
                A dictionary with objects from class :class:`FITSaxis`. One object
                for each axis. The dictionary keys are the axis numbers.
                See also second example at method :meth:`FITSaxis.printattr`.
              
          .. attribute:: allowedtrans

                A list with strings representing the spectral translations
                that are possible for the current image axis selection.

           .. attribute:: spectrans

                The selected spectral translation

          .. attribute:: slicepos

                One or a list with integers that represent pixel positions on
                axes in the data set that do not belong to the image.
                At these position, a slice with image data is extracted.

          .. attribute:: map

                Image data from the selected FITS file. It is always a
                2D data slice and its size can be found in attribute
                :attr:`imshape`.

          .. attribute:: imshape

                The shape of the array :attr:`map`.

          .. attribute:: mixpix

                Images with only one spatial axis, need another spatial axis
                to produces useful world coordinates. This attribute is
                extracted from the relevant axis in attribute :attr:`slicepos`.

          .. attribute:: convproj

                An object from class Projection as defined in :mod:`wcs`.

          .. attribute:: axperm

                The axis numbers corresponding with the X-axis and Y-axis in
                the image.

      :Note:
         The aspect ratio is reset (to *None*) after each call to this method.

      :Examples:
         Set the image axes explicitly:

         >>> fitsobject = maputils.FITSimage('rense.fits')
         >>> fitsobject.set_imageaxes(1,2, slicepos=30)

         Set the images axes in interaction with the user using
         a prompt function:

         >>> fitsobject = maputils.FITSimage('rense.fits')
         >>> fitsobject.set_imageaxes(promptfie=maputils.prompt_imageaxes)

         Enter (part of) the axis names. Note the minimal matching and
         case insensitivity.
                   
         >>> fitsobject = maputils.FITSimage('rense.fits')
         >>> fitsobject.set_imageaxes('ra','d', slicepos=30)
      """
        axnr1 = self.getaxnumberbyname(axnr1)
        axnr2 = self.getaxnumberbyname(axnr2)
        n = self.naxis
        if n >= 2:
            if (axnr1 is None or axnr2 is None) and promptfie is None:
                if axnr1 is None and axnr2 is None:
                    axnr1 = self.axperm[0]
                    axnr2 = self.axperm[1]
                else:
                    raise Exception('One axis number is missing and no prompt function is given!')
            if slicepos is None and promptfie is None:
                slicepos = self.slicepos
        self.allowedtrans = self.proj.altspec
        if promptfie is not None:
            axnr1, axnr2, self.slicepos = promptfie(self, axnr1, axnr2)
        elif slicepos is not None and n > 2:
            if issequence(slicepos):
                self.slicepos = slicepos
            else:
                self.slicepos = [
                 slicepos]
            k = 0
            for i in range(n):
                axnr = i + 1
                if axnr not in [axnr1, axnr2]:
                    self.sliceaxnames[k] = self.axisinfo[axnr].axname
                    k += 1

        axperm = [
         axnr1, axnr2]
        wcsaxperm = [axnr1, axnr2]
        axperm.sort()
        if n > 2:
            if len(self.slicepos) != n - 2:
                raise Exception('Missing positions on axes outside image!')
            j = 0
            for i in range(n):
                axnr = i + 1
                if axnr != axnr1 and axnr != axnr2:
                    axperm.append(axnr)
                    self.axisinfo[axnr].outsidepix = self.slicepos[j]
                    j += 1

        if n > 2:
            sl = []
            for ax in range(n, 0, -1):
                if ax == axnr1 or ax == axnr2:
                    sl.append(slice(None))
                else:
                    g = self.axisinfo[ax].outsidepix
                    sl.append(slice(g - 1, g))

            if self.dat is not None:
                axlen1 = int(self.axisinfo[axnr1].axlen)
                axlen2 = int(self.axisinfo[axnr2].axlen)
                if axperm[0] != wcsaxperm[0]:
                    self.boxdat = self.dat[sl].reshape((axlen1, axlen2))
                else:
                    self.boxdat = self.dat[sl].reshape((axlen2, axlen1))
        else:
            self.boxdat = self.dat
        if self.boxdat is not None:
            self.imshape = self.boxdat.shape
            if axperm[0] != wcsaxperm[0]:
                self.boxdat = numpy.swapaxes(self.boxdat, 0, 1)
                self.imshape = self.boxdat.shape
        if axperm[0] != wcsaxperm[0]:
            axperm[0] = wcsaxperm[0]
            axperm[1] = wcsaxperm[1]
        n1 = self.axisinfo[axperm[0]].axlen
        n2 = self.axisinfo[axperm[1]].axlen
        self.pxlim = [1, n1]
        self.pylim = [1, n2]
        self.mixpix = None
        ap = wcsaxperm
        mix = False
        matchingaxnum = None
        if n > 2:
            ax1 = wcsaxperm[0]
            ax2 = wcsaxperm[1]
            if ax1 == self.proj.lonaxnum and ax2 != self.proj.lataxnum:
                matchingaxnum = self.proj.lataxnum
                mix = True
            elif ax1 == self.proj.lataxnum and ax2 != self.proj.lonaxnum:
                matchingaxnum = self.proj.lonaxnum
                mix = True
            if ax2 == self.proj.lonaxnum and ax1 != self.proj.lataxnum:
                matchingaxnum = self.proj.lataxnum
                mix = True
            elif ax2 == self.proj.lataxnum and ax1 != self.proj.lonaxnum:
                matchingaxnum = self.proj.lonaxnum
                mix = True
        if mix:
            if matchingaxnum is not None:
                self.mixpix = self.axisinfo[matchingaxnum].outsidepix
                ap = (axperm[0], axperm[1], matchingaxnum)
            else:
                raise Exception('Cannot find a matching axis for the spatial axis!')
        else:
            ap = (
             axperm[0], axperm[1])
        if self.spectrans is not None:
            self.proj.spectra(self.spectrans)
        self.convproj = self.proj.sub(ap)
        if self.skyout is not None:
            self.convproj.skyout = self.skyout
        self.axperm = wcsaxperm
        self.aspectratio = None
        return

    def set_spectrans(self, spectrans=None, promptfie=None):
        """
      Set spectral translation or ask user to enter a spectral
      translation if one of the axes in the current FITSimage
      is spectral.

      :param spectrans:
         A spectral translation e.g. to convert frequencies
         to optical velocities.
      :type spectrans:
         String
      :param promptfie:
         A function, supplied by the user, that can
         prompt a user to enter a sky definition.
      :type promptfie:
         A Python function without parameters. It returns
         a string with the spectral translation.
         An example of a function supplied by
         :mod:`maputils` is function :func:`prompt_spectrans`
      
      :Examples:
         Set a spectral translation using 1) a prompt function,
         2) a spectral translation for which we don't know the code
         for the conversion algorithm and 3) set the translation explicitly:

         >>> fitsobject.set_spectrans(promptfie=maputils.prompt_spectrans)
         >>> fitsobject.set_spectrans(spectrans="VOPT-???")
         >>> fitsobject.set_spectrans(spectrans="VOPT-V2W")

      """
        isspectral = False
        for ax in range(1, self.naxis + 1):
            if self.axisinfo[ax].wcstype == 'spectral':
                isspectral = True

        if not isspectral:
            return
        else:
            if promptfie is None:
                self.spectrans = spectrans
            else:
                self.spectrans = promptfie(self)
            if self.spectrans is not None:
                self.convproj = self.convproj.spectra(self.spectrans)
            return

    def set_skyout(self, skyout=None, promptfie=None):
        """
      Set the output sky definition. Mouse positions and
      coordinate labels will correspond to the selected
      definition. The method will only work if both axes are
      spatial axes.

      :param skyout:
         The output sky definition for sky system, reference system,
         equinox and date of observation.
         For the syntax of a sky definition see the description
         at :meth:`celestial.skymatrix`
      :type skyout:
         A single value or tuple.
      :param promptfie:
         A function, supplied by the user, that can
         prompt a user to enter a sky definition.
      :type promptfie:
         A Python function without parameters. It returns
         the sky definition.
         An example of a function supplied by
         :mod:`maputils` is function :func:`prompt_skyout`
         
      :Notes:
          The method sets an output system only for data with
          two spatial axes. For XV maps the output sky system is
          always the same as the native system.

      """
        spatials = [
         self.proj.lonaxnum, self.proj.lataxnum]
        spatialmap = self.axperm[0] in spatials and self.axperm[1] in spatials
        if not spatialmap:
            return
        else:
            if promptfie is None:
                if skyout is None:
                    raise Exception('No definition for the output sky is given!')
                else:
                    self.skyout = skyout
            else:
                self.skyout = promptfie(self)
            if self.skyout is not None:
                self.convproj.skyout = self.skyout
            return

    def set_limits(self, pxlim=None, pylim=None, promptfie=None):
        """
      This method sets the image box. That is, it sets the limits
      of the image axes in pixels. This can be a useful feature if
      one knows which part of an image contains the interesting data.
      
      :param pxlim:
         Two integer numbers which should not be smaller than 1 and not
         bigger than the header value *NAXISn*, where n represents the
         x axis.
      :type pxlim:
         Tuple with two integers
      :param pylim:
         Two integer numbers which should not be smaller than 1 and not
         bigger than the header value *NAXISn*, where n represents the
         y axis.
      :type pylim:
         Tuple with two integers
      :param promptfie:
         An external function with parameters *pxlim*, *pylim*, *axnameX*,
         and *axnameY* which are used to compose a prompt.
         If a function is given then there is no need to enter *pxlim* and *pylim*.
         The prompt function must return (new) values for *pxlim* and *pylim*.
         An example of a function supplied by
         :mod:`maputils` is function :func:`prompt_box`
      :type promptfie:
         Python function

      :Examples: Ask user to enter limits with prompt function :func:`prompt_box`
         
         >>> fitsobject = maputils.FITSimage('rense.fits')
         >>> fitsobject.set_imageaxes(1,2, slicepos=30) # Define image in cube
         >>> fitsobject.set_limits(promptfie=maputils.prompt_box)
      """
        n1 = int(self.axisinfo[self.axperm[0]].axlen)
        n2 = int(self.axisinfo[self.axperm[1]].axlen)
        npxlim = [None, None]
        npylim = [None, None]
        if pxlim is None:
            npxlim = [
             1, n1]
        else:
            if not issequence(pxlim):
                raise Exception('pxlim must be tuple or list!')
            npxlim[0] = int(nint(pxlim[0]))
            npxlim[1] = int(nint(pxlim[1]))
        if pylim is None:
            npylim = [
             1, n2]
        else:
            if not issequence(pylim):
                raise Exception('pylim must be tuple or list!')
            npylim[0] = int(nint(pylim[0]))
            npylim[1] = int(nint(pylim[1]))
        if promptfie is not None:
            axname1 = self.axisinfo[self.axperm[0]].axname
            axname2 = self.axisinfo[self.axperm[1]].axname
            npxlim, npylim = promptfie(self.pxlim, self.pylim, axname1, axname2)
        if npxlim[0] < 1:
            npxlim[0] = 1
        if npxlim[1] > n1:
            npxlim[1] = n1
        if npylim[0] < 1:
            npylim[0] = 1
        if npylim[1] > n2:
            npylim[1] = n2
        if self.boxdat is not None:
            self.boxdat = self.boxdat[npylim[0] - 1:npylim[1], npxlim[0] - 1:npxlim[1]]
            self.imshape = self.boxdat.shape
        self.pxlim = npxlim
        self.pylim = npylim
        self.axisinfo[self.axperm[0]].axstart = npxlim[0]
        self.axisinfo[self.axperm[0]].axend = npxlim[1]
        self.axisinfo[self.axperm[1]].axstart = npylim[0]
        self.axisinfo[self.axperm[1]].axend = npylim[1]
        return

    def get_pixelaspectratio(self):
        """
      Return the aspect ratio of the pixels in the current
      data structure defined by the two selected axes.
      The aspect ratio is defined as *pixel height / pixel width*.

      :Example:

         >>> fitsobject = maputils.FITSimage('m101.fits')
         >>> print fitsobject.get_pixelaspectratio()
         1.0002571958

      :Note:

         If a header has only a cd matrix and no values for CDELT,
         then these values are set to 1. This gives an aspect ratio
         of 1.
      """
        a1 = self.axperm[0]
        a2 = self.axperm[1]
        cdeltx = self.axisinfo[a1].cdelt
        cdelty = self.axisinfo[a2].cdelt
        nx = float(self.pxlim[1] - self.pxlim[0] + 1)
        ny = float(self.pylim[1] - self.pylim[0] + 1)
        if self.proj.lonaxnum in self.axperm and self.proj.lataxnum in self.axperm:
            aspectratio = abs(cdelty / cdeltx)
        else:
            aspectratio = nx / ny
        self.pixelaspectratio = aspectratio
        return aspectratio

    def get_figsize(self, xsize=None, ysize=None, cm=False):
        """
      Usually a user will set the figure size manually
      with Matplotlib's figure(figsize=...) construction.
      For many plots this is a waste of white space around the plot.
      This can be improved by taking the aspect ratio into account
      and adding some extra space for labels and titles.
      For aspect ratios far from 1.0 the number of pixels in x and y
      are taken into account.

      A handy feature is that you can enter the two values in centimeters
      if you set the flag *cm* to True.

      If you have a plot which is higher than its width and you want to
      fit in on a A4 page then use:

      >>> f = maputils.FITSimage(externalheader=header)
      >>> figsize = f.get_figsize(ysize=21, cm=True)
      >>> fig = plt.figure(figsize=figsize)
      >>> frame = fig.add_subplot(1,1,1)
      
      """
        if xsize is not None and not cm:
            xsize *= 2.54
        if ysize is not None and not cm:
            ysize *= 2.54
        if xsize is not None and ysize is not None:
            return (xsize / 2.54, ysize / 2.54)
        else:
            a1 = self.axperm[0]
            a2 = self.axperm[1]
            cdeltx = self.axisinfo[a1].cdelt
            cdelty = self.axisinfo[a2].cdelt
            nx = float(self.pxlim[1] - self.pxlim[0] + 1)
            ny = float(self.pylim[1] - self.pylim[0] + 1)
            aspectratio = abs(cdelty / cdeltx)
            if aspectratio > 10.0 or aspectratio < 0.1:
                aspectratio = nx / ny
            extraspace = 3.0
            if xsize is None and ysize is None:
                if abs(nx * cdeltx) >= abs(ny * cdelty):
                    xsize = 21.0
                else:
                    ysize = 21.0
            if xsize is not None:
                xcm = xsize
                ycm = xcm * (ny / nx) * aspectratio + extraspace
            else:
                ycm = ysize
                xcm = ycm * (nx / ny) / aspectratio + extraspace
            return (
             xcm / 2.54, ycm / 2.54)

    def header2classic(self):
        r"""
      If a header contains PC or CD elements, and not all the 'classic'
      elements for a WCS then  a number of FITS readers could have a
      problem if they don't recognize a PC and CD matrix. What can be done
      is to derive the missing header items, CDELTn and CROTA from
      these headers and add them to the header.

      What is a 'classic' FITS header?
      
      (See also http://fits.gsfc.nasa.gov/fits_standard.html)
      For the transformation between pixel coordinates and world
      coordinates, FITS supports three conventions.
      First some definitions:

      An intermediate pixel coordinate :math:`q_i`  is calculated from a
      pixel coordinates :math:`p` with:

      .. math::
      
         q_i = \sum_{j=1}^N m_{ij}(p_j-r_j)

      Rj are the pixel coordinate elements of a reference point
      (FITS header item CRPIXj), j is an index for the pixel axis
      and i for the world axis
      The matrix :math:`m_{ij}` must be non-singular and its dimension is
      NxN where N is the number of world coordinate axes (given
      by FITS header item NAXIS).

      The conversion of :math:`q_i` to intermediate world coordinate :math:`x_i` is
      a scale :math:`s_i`:

      .. math::
      
         x_i = s_i q_i

      **Formalism 1 (PC keywords)**

      Formalism 1 encodes :math:`m_{ij}` in so called PCi_j keywords
      and scale factor :math:`s_i` are the values of the CDELTi keywords
      from the FITS header.

      It is obvious that the value of CDELT should not be 0.0.

      **Formalism 2 (CD keywords)**

      If the matrix and scaling are combined we get for the
      intermediate WORLD COORDINATE :math:`x_i`:

      .. math::

         x_i = \sum_{j=1}^N (s_i m_{ij})(p_j-r_j)

      FITS keywords CDi_j encodes the product :math:`s_i m_{ij}`.
      The units of :math:`x_i` are given by FITS keyword CTYPEi.

      **Formalism 3 (Classic)**
      
      This is the oldest but now deprecated formalism. It uses CDELTi
      for the scaling and CROTAn for a rotation of the image plane.
      n is associated with the latitude axis so often one sees
      CROTA2 in the header if the latitude axis is the second axis
      in the dataset

      Following the FITS standard, a number of rules is set:
      
         1. CDELT and CROTA may co-exist with the CDi_j keywords
            but must be ignored if an application supports the CD
            formalism.
         2. CROTAn must not occur with PCi_j keywords
         3. CRPIXj defaults to 0.0
         4. CDELT defaults to 1.0
         5. CROTA defaults to 0.0
         6. PCi_j defaults to 1 if i==j and to 0 otherwise. The matrix
            must not be singular
         7. CDi_j defaults to 0.0. The matrix must not be singular.
         8. CDi_j and PCi_j must not appear together in a header.

      **Alternate WCS axis descriptions**

      A World Coordinate System (WCS) can be described by an
      alternative set of keywords.
      For this keywords a character in the range [A..Z] is appended.
      In our software we made the assumption that the primary
      description contains all the necessary information
      to derive a 'classic' header and therefore we will ignore
      alternate header descriptions.

      **Conversion to a formalism 3 ('classic') header**

      Many FITS readers from the past are not upgraded to process
      FITS files with headers written using formalism 1 or 2.
      The purpose of this application is to convert a FITS file
      to a file that can be read and interpreted by old FITS readers.
      For GIPSY we require FITS headers to be written using formalism
      3. If keywords are missing, they will be derived and a
      comment will be inserted about the keyword not being an
      original keyword.

      The method that converts the header, tries to process it
      first with WCSLIB (tools to interpret the world coordinate
      system as described in a FITS header). If this fails, then we
      are sure that the header is incorrect and we cannot proceed.
      One should use a FITS tool like 'fv' (the Interactive FITS
      File Editor from Nasa) to repair the header.

      The conversion process starts with exploring the spatial part
      of the header.
      It knows which axes are spatial and it reads the corresponding
      keywords (CDELTi, CROTAn, CDi_j, PCi_j and PC00i_00j (old
      format for PC elements).
      If there is no CD or PC matrix, then the conversion routine
      returns the unaltered original header.
      If it finds a PC matrix and no CD matrix then the header should
      contain CDELT keywords. With the values of these keywords we
      create a CD matrix:

      .. math::
      
         \begin{bmatrix}cd_{11} & cd_{12}\\ cd_{21} & cd_{22}\end{bmatrix} =
         \begin{bmatrix}cdelt_1 & 0\\ 0 & cdelt_2 \end{bmatrix}
         \begin{bmatrix}pc_{11} & pc_{12}\\ pc_{21} & pc_{22}\end{bmatrix}

      Notes:
      
         *  We replaced notation i_j by ij so cd11 == CD1_1
         *  For the moment we restricted the problem to the 2 dim.
            spatial case because that is what we need to retrieve
            a value for CROTA, the rotation of the image.)
         *  We assumed that the PC matrix did not represent
            transposed axes as in:

      .. math::

         PC = \begin{bmatrix}0 & 1 & 0\\ 0 & 0 & 1\\ 1 & 0 & 0 \end{bmatrix}
         

      If cd12 == 0.0 and cd12 == 0.0 then CROTA is obviously 0.
      There is no rotation and CDELT1 = cd11, CDELT2 = cd22

      If one or both values of cd12, cd21 is not zero then we
      expect a value for CROTA unequal to zero and/or skew.

      We calculate the scaling parameters CDELT with::

                     CDELT1 = sqrt(cd11*cd11+cd21*cd21)
                     CDELT2 = sqrt(cd12*cd12+cd22*cd22)

      The determinant of the matrix is::

                     det = cd11*cd22 - cd12*cd21

      This value cannot be 0 because we required that the matrix is
      non-singular.
      Further we distinguish two situations: a determinant < 0 and
      a determinant > 0 (zero was already excluded).
      Then we derive two rotations. If these are equal,
      the image is not skewed.
      If they are not equal, we derive the rotation from the
      average of the two calculated angles. As a measure of skew,
      we calculated the difference between the two rotation angles.
      Here is a piece of the actual code::

                     sign = 1.0
                     if det < 0.0:
                        cdeltlon_cd = -cdeltlon_cd
                        sign = -1.0
                     rot1_cd = atan2(-cd21, sign*cd11)
                     rot2_cd = atan2(sign*cd12, cd22)
                     rot_av = (rot1_cd+rot2_cd)/2.0
                     crota_cd = degrees(rot_av)
                     skew = degrees(abs(rot1_cd-rot2_cd))

      New values of CDELT and CROTA will be inserted in the new
      'classic' header only if they were not part of the original
      header.

      The process continues with non spatial axes. For these axes
      we cannot derive a rotation. We only need to find a CDELTi
      if for axis i no value could be found in the header.
      If this value cannot be derived from the a CD matrix (usually
      with diagonal element CDi_i) then the default 1.0 is assumed.
      Note that there will be a warning about this in the comment
      string for the corresponding keyword in the new 'classic' FITS
      header.

      Finally there is some cleaning up. First all CD/PC elements are
      removed for all the axes in the data set. Second, some unwanted
      keywords are removed. The current list is:
      ["XTENSION", "EXTNAME", "EXTEND"]

      
      See also: Calabretta & Greisen: 'Representations of celestial coordinates
      in FITS', section 6

      :param -: No parameters
      
      :Returns:
         A tuple with three elements:

         * *hdr* - A modified copy of the current header.
           The CD and PC elements are removed.
         * *skew* - Difference between the two calculated rotation angles
           If this number is bigger then say 0.001 then there is considerable
           skew in the data. One should reproject the data so that it fits
           a non skewed version with only a CROTA in the header
         * *hdrchanged* - A list with keywords the are changed when a
           'classic' header is required.

      :Notes:

         This method is tested with FITS files:

         * With classic header
         * With only CD matrix
         * With only PC matrix
         * With PC and CD matrix
         * With CD matrix and NAXIS > 2
         * With sample files with skew

         
      :Example:
       ::   
       
            from kapteyn import maputils, wcs
            import pyfits
                     
            Basefits = maputils.FITSimage(promptfie=maputils.prompt_fitsfile)
            newheader, skew, hdrchanged = Basefits.header2classic()
            if len(hdrchanged):
               print newheader
            if skew != 0.0:
               print "found skew:", skew
      """
        skew = 0.0
        hdrchanged = []
        hdr = self.hdr.copy()
        if type(hdr) == 'dict':
            dicttype = True
        else:
            dicttype = False
        comment = 'Appended by Kapteyn Package module Maputils %s' % datetime.now().strftime('%dd%mm%Yy%Hh%Mm%Ss')
        lonaxnum = self.proj.lonaxnum
        lataxnum = self.proj.lataxnum
        spatial = lonaxnum is not None and lataxnum is not None
        if spatial:
            cdeltlon = None
            cdeltlat = None
            crota = None
            key = 'CDELT%d' % lonaxnum
            if key in hdr:
                cdeltlon = hdr[key]
            key = 'CDELT%d' % lataxnum
            if key in hdr:
                cdeltlat = hdr[key]
            key = 'CROTA%d' % lataxnum
            if key in hdr:
                crota = hdr[key]
            cd11 = cd12 = cd21 = cd22 = None
            CD = [0.0] * 4
            k = 0
            cdmatrix = False
            for i in [lonaxnum, lataxnum]:
                for j in [lonaxnum, lataxnum]:
                    key = 'CD%d_%d' % (i, j)
                    if key in hdr:
                        CD[k] = hdr[key]
                        del hdr[key]
                        hdrchanged.append(key)
                        cdmatrix = True
                    k += 1

            cd11, cd12, cd21, cd22 = CD
            key = 'CROTA%d' % lonaxnum
            if key in hdr:
                del hdr[key]
            pcmatrix = False
            PC = [None] * 4
            k = 0
            for i in [lonaxnum, lataxnum]:
                for j in [lonaxnum, lataxnum]:
                    if i == j:
                        PC[k] = 1.0
                    else:
                        PC[k] = 0.0
                    key = 'PC%d_%d' % (i, j)
                    if key in hdr:
                        PC[k] = hdr[key]
                        del hdr[key]
                        hdrchanged.append(key)
                        pcmatrix = True
                    k += 1

            pc11, pc12, pc21, pc22 = PC
            pcoldmatrix = False
            if not pcmatrix:
                PCold = [
                 None] * 4
                k = 0
                for i in [lonaxnum, lataxnum]:
                    for j in [lonaxnum, lataxnum]:
                        if i == j:
                            PCold[k] = 1.0
                        else:
                            PCold[k] = 0.0
                        key = 'PC%03d%03d' % (i, j)
                        if key in hdr:
                            PCold[k] = hdr[key]
                            del hdr[key]
                            hdrchanged.append(key)
                            pcoldmatrix = True
                        k += 1

                pco11, pco12, pco21, pco22 = PCold
            if not pcmatrix and pcoldmatrix:
                PC = PCold
                pc11, pc12, pc21, pc22 = PC
                pcmatrix = True
            if not cdmatrix:
                if pcmatrix and None in [cdeltlon, cdeltlat]:
                    raise ValueError("Header does not contain necessary CDELT's!")
                if pcmatrix:
                    cd11 = cdeltlon * pc11
                    cd12 = cdeltlon * pc12
                    cd21 = cdeltlat * pc21
                    cd22 = cdeltlat * pc22
                    CD = [cd11, cd12, cd21, cd22]
                    cdmatrix = True
            if not cdmatrix:
                return (hdr, 0, [])
            from math import sqrt
            from math import atan2
            from math import degrees, radians
            from math import cos, sin, acos
            if cd12 == 0.0 and cd21 == 0.0:
                crota_cd = 0.0
                cdeltlon_cd = cd11
                cdeltlat_cd = cd22
            else:
                cdeltlon_cd = sqrt(cd11 * cd11 + cd21 * cd21)
                cdeltlat_cd = sqrt(cd12 * cd12 + cd22 * cd22)
                det = cd11 * cd22 - cd12 * cd21
                if det == 0.0:
                    raise ValueError('Determinant of CD matrix == 0')
                sign = 1.0
                if det < 0.0:
                    cdeltlon_cd = -cdeltlon_cd
                    sign = -1.0
                rot1_cd = atan2(-cd21, sign * cd11)
                rot2_cd = atan2(sign * cd12, cd22)
                rot_av = (rot1_cd + rot2_cd) / 2.0
                crota_cd = degrees(rot_av)
                skew = degrees(abs(rot1_cd - rot2_cd))
            if cdeltlon is None:
                cdeltlon = cdeltlon_cd
                key = 'CDELT%d' % lonaxnum
                if dicttype:
                    hdr.update(key=cdeltlon)
                else:
                    hdr.update(key, cdeltlon, comment)
                hdrchanged.append(key)
            if cdeltlat is None:
                cdeltlat = cdeltlat_cd
                key = 'CDELT%d' % lataxnum
                if dicttype:
                    hdr.update(key=cdeltlat)
                else:
                    hdr.update(key, cdeltlat, comment)
                hdrchanged.append(key)
            if crota is None:
                crota = crota_cd
                key = 'CROTA%d' % lataxnum
                if dicttype:
                    hdr.update(key=crota)
                else:
                    hdr.update(key, crota, comment)
                hdrchanged.append(key)
        wasdefault = False
        naxis = hdr['NAXIS']
        if spatial and naxis > 2 or not spatial:
            for k in range(naxis):
                axnum = k + 1
                key = 'CDELT%d' % axnum
                if not spatial or spatial and axnum != lonaxnum and axnum != lataxnum:
                    if key not in hdr:
                        key_cd = 'CD%d_%d' % (axnum, axnum)
                        if key_cd in hdr:
                            newval = hdr[key_cd]
                        else:
                            newval = 1.0
                            wasdefault = True
                        if dicttype:
                            hdr[key] = newval
                        else:
                            if wasdefault:
                                s = 'Inserted default 1.0! ' + comment
                            else:
                                s = comment
                            hdr.update(key, newval, s)
                        hdrchanged.append(key)

        for i in range(naxis):
            for j in range(naxis):
                axi = i + 1
                axj = j + 1
                keys = [
                 'CD%d_%d' % (axi, axj), 'PC%d_%d' % (axi, axj), 'PC%03d%03d' % (axi, axj)]
                for key in keys:
                    if key in hdr:
                        del hdr[key]
                        hdrchanged.append(key)

        ekeys = [
         'XTENSION', 'EXTNAME', 'EXTEND']
        for key in ekeys:
            if key in hdr:
                del hdr[key]

        return (
         hdr, skew, hdrchanged)

    def reproject_to(self, reprojobj=None, pxlim_dst=None, pylim_dst=None, plimlo=None, plimhi=None, interpol_dict=None, rotation=None, insertspatial=None, **fitskeys):
        """
      The current FITSimage object must contain a number of spatial maps.
      This method then reprojects these maps so that they conform to
      the input header.

      Imagine an image and a second image of which you want to overlay contours
      on the first one. Then this method uses the current data to reproject
      to the input header and you will end up with a new FITSimage object
      which has the spatial properties of the input header and the reprojected
      data of the current FITSimage object.

      Also more complicated data structures can be used. Assume you have a
      data cube with axes RA, Dec and Freq. Then this method will reproject
      all its spatial subsets to the spatial properties of the input header.

      The current FITSimage object tries to keep as much of its original
      FITS keywords. Only those related to spatial data are copied from the
      input header. The size of the spatial map can be limited or extended.
      The axes that are not spatial are unaltered.

      The spatial information for both data structures are extracted from
      the headers so there is no need to specify the spatial parts of the
      data structures.

      The image that is reprojected can be limited in size with parameters
      pxlim_dst and pylim_dst.
      If the input is a FITSimage object, then these parameters (pxlim_dst
      and pylim_dst) are copied
      from the axes lengths set with method :meth:`set_limits()` for that
      FITSimage object.

      :param reprojobj:
          *  The header which provides the new information to reproject to.
             The size of the reprojected map is either copied from
             the NAXIS keywords in the header or entered with parameters
             *pxlim_dst* and *pylim_dst*. The reprojections are done for all
             spatial maps in the current FITSimage object or for a selection
             entered with parameters *plimlo* and *plimhi* (see examples).
          *  The FITSimage object from which relevant information is
             extracted like the header and the new sizes of the spatial axes
             which otherwise should have been provided in parameters
             *pxlim_dst* and *pylim_dst*. The reprojection is restricted to
             one spatial map and its slice information is copied
             from the current FITSimage. This option is selected if you
             want to overlay e.g. contours from the current FITSimage
             data onto data from another WCS.
          *  If None, then the current header is used. Modifications to this header
             are done with keyword arguments.
      :type reprojobj:
          Python dictionary or PyFITS header. Or a :class:`maputils.FITSimage`
          object
      :param pxlim_dst:
          Limits in pixels for the reprojected box.
      :type pxlim_dst:
          Tuple of integers
      :param plimlo:
          One or more pixel coordinates corresponding to axes outside
          the spatial map in order as found in the header 'reprojobj'.
          The values set the lower limits of the axes.
          There is no need to specify all limits but the order is important.
      :type plimlo:
          Integer or tuple of integers
      :param plimhi:
          The same as plimhi, but now for the upper limits.
      :type plimhi:
          Integer or tuple of integers
      :param interpol_dict:
          This parameter is a dictionary with parameters for the interpolation routine
          which is used to reproject data. The interpolation routine
          is based on SciPy's *map_coordinates*. The most important parameters with
          the maputils defaults are:

          .. tabularcolumns:: |p{10mm}|p{100mm}|

          =========  ===============================================================        
            order :  Integer, optional

                     The order of the spline interpolation, default is 1.
                     The order has to be in the range 0-5.
            mode :   String, optional

                     Points outside the boundaries of the input are filled according
                     to the given mode ('constant', 'nearest', 'reflect' or 'wrap').
                     Default is 'constant'.
            cval :   scalar, optional

                     Value used for points outside the boundaries of the input if
                     mode='constant'. Default is numpy.NaN
          =========  ===============================================================
          
      :type interpol_dict:
         Python dictionary
      :param rotation:
         Sets a rotation angle. If this method encounters this keyword, it will
         create a so called 'classic' header. That is a header without
         CD or PC elements. Then the rotation angle of the current spatial
         map is only given by FITS keyword *CROTAn*. The value of *rotation* is added
         to *CROTAn* to create a new value which is inserted in the new header.
         Note that values for *CROTAn* in the *fitskeys* parameter list
         overwrite this calculated value.
      :type rotation:
         Floating point number or *None*
      :param insertspatial:
         If True, then replace spatial part of current header by spatial part
         of new (destination) header.
         Assume you start with a data cube with a number of spatial maps
         as function of frequency (the third axis in the data set). If
         you use the header of another FITS file as the definition of
         a new world coordinate system, then it could be that this header
         represents a two dimensional data set. This is not an incompatible
         set because we only require a description of the spatial part.
         To keep the description of the original three dimensional
         structure we insert the new spatial(only) information into the
         current header. The default then is *insertspatial=True*.
         In other cases where we use the original header as the base
         header, one just inserts new values and there is no need to
         set insert something, so then the default is *insertspatial=False*.
         A user can change the default. This can be useful. For example
         in the maputils tutorial we have a script mu_reproj2classic.py where
         we use the header of a FITS file to make some changes and use the
         changed header as an external header to re-project to. The default
         then is *insertspatial=True*, but the external header is already
         a complete header, so there is no need to insert something.
      :type insertspatial:
         Boolean
      :param fitskeys:
         Parameters containing FITS keywords and values which are written
         in the reprojection header. 
      :type fitskeys:
         Python keyword arguments.

      :Examples:

            -Set limits for axes outside the spatial map. Assume a data structure
            with axes RA-DEC-FREQ-STOKES for which the RA-DEC part is reprojected to
            a set RA'-DEC'-FREQ-STOKES. The ranges for FREQ and STOKES set the
            number of spatial maps in this data structure. One can limit these
            ranges with *plimlo* and *plimhi*.
            
            * *plimlo=(20,2)*, *plimhi=(40,2)*

              we restrict the reprojections for spatial maps
              at frequencies 20 to 40 at one position on the STOKES axis
              (at pixel coordinate 2).
   
            * *plimlo=(None,2)*, *plimhi=(None,2)*
            
              If one wants to reproject all the maps at all frequencies
              but only for STOKES=2 and 3 then use:
              *plimlo=(None,2)* and *plimhi=(None,2)* where None implies no limits.
   
            * *plimlo=40*
              
              No *plimhi* is entered. Then there are no upper limits. Only one value
              (40) is entered so this must represent the FREQ axis at pixel
              coordinate 40. It represents all spatial maps from FREQ pixel
              coordinate 40 to the end of the FREQ range, repeated for all
              pixels on the STOKES axis.
   
            * *plimlo=(55,1)*, *plimhi=(55,1)*
            
              This reprojects just one map at FREQ pixel coordinate 55
              and STOKES pixel coordinate 1. This enables a user/programmer
              to extract one spatial map, reproject it and write it as a single
              map to a FITS file while no information about the FREQ and STOKES
              axes is lost. The dimensionality of the new data remains 4 but
              the length of the 'repeat axes' is 1.
   
            Note that if the data structure was represented by axes
            FREQ-RA-STOKES-DEC then the examples above are still valid because
            these set the limits on the repeat axes FREQ and POL whatever the
            position of these axes in the data structure.

            -Use and modify the current header to change the data.
            The example shows how to rotate an image and display the result.

            ::

               Basefits = maputils.FITSimage("m101.fits")
               Rotfits = Basefits.reproject_to(rotation=40.0,
                                             naxis1=800, naxis2=800,
                                             crpix1=400, crpix2=400)
   
               # If copy on disk required:
               # Rotfits.writetofits("m10rot.fits", clobber=True, append=False)
   
               annim = Rotfits.Annotatedimage()
               annim.Image()
               annim.Graticule()
               annim.interact_toolbarinfo()
               maputils.showall()

            -Use an external header and change keywords in that header
            before the re-projection:
       
            >>> Rotfits = Basefits.reproject_to(externalheader,
                                                naxis1=800, naxis2=800,
                                                crpix1=400, crpix2=400)

            -Use the FITS file's own header. Change it and use it as an
            external header

            ::

               from kapteyn import maputils, wcs

               Basefits = maputils.FITSimage("m101.fits")
               classicheader, skew, hdrchanged = Basefits.header2classic()

               lat = Basefits.proj.lataxnum
               key = "CROTA%d"%lat
               classicheader[key] = 0.0 # New value for CROTA
               Basefits.reproject_to(classicheader, insertspatial=False)
               fnew = maputils.FITSimage(externalheader=classicheader,
                                         externaldata=Basefits.dat)
               fnew.writetofits("classic.fits", clobber=True, append=False)

            
      
      :Tests:

         1) The first test was a reprojection of data of *map1* to the
            spatial header of *map2*. One should observe that the result
            of the reprojection (*reproj*) has its spatial structure from
            *map2* and its non spatial structure (i.e. the repeat axes)
            from *map1*. Note that the order of longitude, latitude
            in *map1* is swapped in *map2*.
   
            map1:
            CTYPE:  RA - POL - FREQ - DEC
            NAXIS   35   5     16     41
   
            map2:
            CTYPE:  DEC - POL - FREQ - RA
            NAXIS   36    4     17     30
   
            reproj = map1.reproject_to(map2)
   
            reproj:
            CTYPE:  RA - POL - FREQ - DEC
            NAXIS   36   5     16     30

         2) Tested with values for the repeat axes
         3) Tested with values for the output box
         4) Tested with a new CTYPE (GLON-TAN, GLAT-TAN)
            and new CRVAL
      
      .. note::

            If you want to align an image with the direction of the north,
            then the value of *CROTAn* (e.g. CROTA2) should be set to zero.
            To ensure that the data will be rotated, use parameter
            *rotation* with a dummy value so that the header used for
            the re-projection is a 'classic' header:

            e.g.:

            >>> Rotfits = Basefits.reproject_to(rotation=0.0, crota2=0.0)

            Todo: If CTYPE's change, then also LONPOLE and LATPOLE
                  should change
         

      
      .. warning::

            Values for *CROTAn* in parameter *fitskeys* overwrite
            values previously set with keyword *rotation*.

      .. warning::

            Changing values of *CROTAn* will not always result in
            a rotated image. If the world coordinate system was defined using
            CD or PC elements, then changing *CROTAn* will only add the keyword
            but it is never read because CD & PC transformations have precedence.
      """

        def flatten(seq):
            res = []
            for item in seq:
                if isinstance(item, (tuple, list)):
                    res.extend(flatten(item))
                else:
                    res.append(item)

            return res

        plimLO = plimHI = None
        fromheader = True
        if isinstance(reprojobj, FITSimage):
            pxlim_dst = reprojobj.pxlim
            pylim_dst = reprojobj.pylim
            slicepos = self.slicepos
            plimLO = plimHI = slicepos
            repheader = reprojobj.hdr.copy()
            fromheader = False
            if insertspatial is None:
                insertspatial = True
        elif reprojobj is None:
            repheader = self.hdr.copy()
            if insertspatial is None:
                insertspatial = False
        else:
            repheader = reprojobj.copy()
            if insertspatial is None:
                insertspatial = True
            if reprojobj is None and not rotation is None:
                repheader, skew, hdrchanged = self.header2classic()
                key = 'CROTA%d' % self.proj.lataxnum
                if key in repheader:
                    crotanew = repheader[key] + rotation
                    repheader[key] = crotanew
                else:
                    crotanew = rotation
                    if type(repheader) == 'dict':
                        repheader[key] = crotanew
                    else:
                        repheader.update(key, crotanew)
            if len(fitskeys) > 0:
                change_header(repheader, **fitskeys)
            p1 = wcs.Projection(self.hdr)
            naxis = len(p1.naxis)
            axnum = []
            axnum_out = []
            for i in range(1, naxis + 1):
                if i in [p1.lonaxnum, p1.lataxnum]:
                    axnum.append(i)
                else:
                    axnum_out.append(i)

            if len(axnum) != 2:
                raise Exception('No spatial maps to reproject in this data structure!')
            naxisout = len(axnum_out)
            len1 = p1.naxis[(axnum[0] - 1)]
            len2 = p1.naxis[(axnum[1] - 1)]
            p1_spat = p1.sub(axnum)
            p2 = wcs.Projection(repheader)
            naxis_2 = len(p2.naxis)
            axnum2 = []
            for i in range(1, naxis_2 + 1):
                if i in [p2.lonaxnum, p2.lataxnum]:
                    axnum2.append(i)

            if len(axnum2) != 2:
                raise Exception('The input header does not contain a spatial data structure!')
            p2_spat = p2.sub(axnum2)
            lenXnew = p2.naxis[(axnum2[0] - 1)]
            lenYnew = p2.naxis[(axnum2[1] - 1)]
            lonaxnum2 = p2.lonaxnum
            lataxnum2 = p2.lataxnum
            shapenew = [
             0] * naxis
            if pxlim_dst is None:
                pxlim_dst = [
                 1] * 2
                pxlim_dst[1] = lenXnew
            if pylim_dst is None:
                pylim_dst = [
                 1] * 2
                pylim_dst[1] = lenYnew
            nx = pxlim_dst[1] - pxlim_dst[0] + 1
            ny = pylim_dst[1] - pylim_dst[0] + 1
            N = nx * ny
            if naxisout > 0:
                if plimLO is None or plimHI is None:
                    plimLO = [
                     0] * (naxis - 2)
                    plimHI = [0] * (naxis - 2)
                    for i, axnr in enumerate(axnum_out):
                        plimLO[i] = 1
                        plimHI[i] = p1.naxis[(axnr - 1)]

                    if plimlo is not None:
                        if not issequence(plimlo):
                            plimlo = [
                             plimlo]
                        if len(plimlo) > naxisout:
                            raise ValueError('To many values in plimlo, max=%d' % naxisout)
                        for i, p in enumerate(plimlo):
                            plimLO[i] = p

                    if plimhi is not None:
                        if not issequence(plimhi):
                            plimhi = [
                             plimhi]
                        if len(plimhi) > naxisout:
                            raise ValueError('To many values in plimhi, max=%d' % naxisout)
                        for i, p in enumerate(plimhi):
                            plimHI[i] = p

                for axnr, lo, hi in zip(axnum_out, plimLO, plimHI):
                    n = hi - lo + 1
                    shapenew[axnr - 1] = n
                    N *= n

            shapenew[axnum[0] - 1] = nx
            shapenew[axnum[1] - 1] = ny
            shapenew = shapenew[::-1]
            newdata = numpy.zeros(N, dtype=self.dat.dtype)
            newdata.shape = shapenew
            if insertspatial:
                newheader = self.insertspatialfrom(repheader, axnum, axnum2)
            else:
                newheader = repheader
            if nx != lenXnew:
                ax = axnum2[0]
                newheader['NAXIS%d' % ax] = nx
                newheader[('CRPIX%d' % ax)] += -pxlim_dst[0] + 1
            if ny != lenYnew:
                ax = axnum2[1]
                newheader['NAXIS%d' % ax] = ny
                newheader[('CRPIX%d' % ax)] += -pylim_dst[0] + 1
            if naxisout > 0:
                for axnr, lo, hi in zip(axnum_out, plimLO, plimHI):
                    n = hi - lo + 1
                    newheader['NAXIS%d' % axnr] = n
                    newheader[('CRPIX%d' % axnr)] += -lo + 1

                key1 = 'CD%d_%d' % (p1.lonaxnum, p1.lonaxnum)
                key2 = 'CD%d_%d' % (axnum_out[0], axnum_out[0])
                if key1 in newheader and not key2 in newheader:
                    for axnr in axnum_out:
                        key2 = 'CD%d_%d' % (axnr, axnr)
                        newheader[key2] = newheader[('CDELT%d' % axnr)]

            if interpol_dict is not None:
                if not 'order' in interpol_dict:
                    interpol_dict['order'] = 1
                if not 'cval' in interpol_dict:
                    interpol_dict['cval'] = numpy.NaN
            else:
                interpol_dict = {}
                interpol_dict['order'] = 1
                interpol_dict['cval'] = numpy.NaN
            dst_offset = (
             pylim_dst[0] - 1, pxlim_dst[0] - 1)
            src_offset = (
             0, 0)
            coords = numpy.around(wcs.coordmap(p1_spat, p2_spat, dst_shape=(ny, nx), dst_offset=dst_offset, src_offset=src_offset) * 512.0) / 512.0
            if naxisout == 0:
                boxdat = self.dat
                newdata = map_coordinates(boxdat, coords, **interpol_dict)
            else:
                perms = []
                for lo, hi in zip(plimLO, plimHI):
                    pixellist = list(range(lo, hi + 1))
                    perms.append(pixellist)

                z = perms[0]
                for i in range(1, len(perms)):
                    z = [ [x, y] for y in perms[i] for x in z ]
                    Z = []
                    for l in z:
                        Z.append(flatten(l))

                    z = Z

            for tup in z:
                sl = []
                slnew = []
                nout = len(axnum_out) - 1
                for ax in range(naxis, 0, -1):
                    if ax in [p1.lonaxnum, p1.lataxnum]:
                        sl.append(slice(None))
                        slnew.append(slice(None))
                    else:
                        if issequence(tup):
                            g = tup[nout]
                        else:
                            g = tup
                        sl.append(slice(g - 1, g))
                        g2 = g - plimLO[nout] + 1
                        slnew.append(slice(g2 - 1, g2))
                        nout -= 1

                boxdat = self.dat[sl].squeeze()
                boxdatnew = newdata[slnew].squeeze()
                reprojecteddata = map_coordinates(boxdat, coords, **interpol_dict)
                boxdatnew[:] = reprojecteddata

        fi = FITSimage(externalheader=newheader, externaldata=newdata)
        if not fromheader:
            slicepos = [ 1 for x in slicepos ]
            fi.set_imageaxes(reprojobj.axperm[0], reprojobj.axperm[1], slicepos)
        return fi

    def insertspatialfrom(self, header, axnum1, axnum2):
        """
      Utility function, used in the context of method
      *reproject_to()*, which returns a new header based on the
      current header, but where its spatial information
      is replaced by the spatial information of the input
      header *header*. The axis numbers of the spatial axes in
      *header* must be entered in *lon2* and *lat2*.

      :param header:
         The header from which the spatial axis information must be
         copied into the current structure.
      :type header:
         PyFITS header object or Python dictionary
      :param axnum1:
         The axis numbers of the spatial axes in the input header
      :type axnum2:
         Tuple of two integers
      :param axnum2:
         The axis numbers of the spatial axes in the destination
         header
      :type axnum2:
         Tuple of two integers

      :Notes:

         For reprojections we use only the primary header. The alternate
         header is NOT removed from the header.

         If the input header has a CD matrix for its spatial axes, and
         the current data structure has not a CD matrix, then we 
         add missing elements in the current header. If the CDELT's
         are missing for the construction of CD elements, the
         value 1 is assumed for diagonal elements.
      """
        comment = True
        history = True
        newheader = fitsheader2dict(self.hdr, comment, history)
        repheader = fitsheader2dict(header, comment, history)
        lon1 = axnum1[0]
        lat1 = axnum1[1]
        lon2 = axnum2[0]
        lat2 = axnum2[1]
        naxis = len(self.proj.naxis)
        axnum_out = []
        for i in range(1, naxis + 1):
            if i not in [self.proj.lonaxnum, self.proj.lataxnum]:
                axnum_out.append(i)

        wcskeys = [
         'NAXIS', 'CRPIX', 'CRVAL', 'CTYPE', 'CUNIT', 'CDELT', 'CROTA']
        for k in wcskeys:
            for ax in (lon1, lat1):
                key1 = '%s%d' % (k, ax)
                if key1 in newheader:
                    del newheader[key1]

        for k in wcskeys:
            for ax in ((lon1, lon2), (lat1, lat2)):
                key1 = '%s%d' % (k, ax[0])
                key2 = '%s%d' % (k, ax[1])
                if key2 in repheader:
                    newheader[key1] = repheader[key2]

        wcskeys = [
         'LONPOLE', 'LATPOLE', 'EQUINOX', 'EPOCH', 'RADESYS', 'MJD-OBS', 'DATE-OBS']
        for key in wcskeys:
            if key in repheader:
                newheader[key] = repheader[key]
            elif key in newheader:
                del newheader[key]

        wcskeys = [
         'PC', 'CD', 'PV', 'PS']
        for key in list(newheader.keys()):
            for wk in wcskeys:
                if key.startswith(wk) and key.find('_') != -1:
                    try:
                        i, j = key[2:].split('_')
                        i = int(i)
                        j = int(j)
                        for ax in (lon2, lat2):
                            if i == ax:
                                del newheader[key]

                    except:
                        pass

        cdmatrix = False
        pcmatrix = False
        for key in list(repheader.keys()):
            for wk in wcskeys:
                if key.startswith(wk) and key.find('_'):
                    try:
                        i, j = key[2:].split('_')
                        i = int(i)
                        j = int(j)
                        ii = jj = None
                        if i == lon2:
                            ii = lon1
                        if i == lat2:
                            ii = lat1
                        if j == lon2:
                            jj = lon1
                        if j == lat2:
                            jj = lat1
                        if ii is not None and jj is not None:
                            newkey = '%s%d_%d' % (wk, ii, jj)
                            newheader[newkey] = repheader[key]
                            if wk == 'CD':
                                cdmatrix = True
                            if wk == 'PC':
                                pcmatrix = True
                    except:
                        pass

        if cdmatrix:
            for i in axnum_out:
                newkey = 'CD%d_%d' % (i, i)
                if newkey not in newheader:
                    cdeltkey = 'CDELT%d' % i
                    if cdeltkey in newheader:
                        cdelt = newheader[cdeltkey]
                    else:
                        cdelt = 1.0
                    newheader[newkey] = cdelt

        else:
            if pcmatrix:
                for i in axnum_out:
                    newkey = 'PC%d_%d' % (i, i)
                    if newkey not in newheader:
                        newheader[newkey] = 1.0

            for i in [1, naxis]:
                for j in [1, naxis]:
                    key = 'PC%03d%03d' % (i, j)
                    if key in newheader:
                        del newheader[key]

        return newheader

    def writetofits(self, filename=None, comment=True, history=True, bitpix=None, bzero=None, bscale=None, blank=None, clobber=False, append=False, extname=''):
        """
      This method copies current data and current header to a FITS file
      on disk. This is useful if either header or data comes from an
      external source. If no file name is entered then a file name
      will be composed using current date and time of writing.
      The name then start with 'FITS'.

      :param filename:
         Name of new file on disk. If omitted the default name is
         'FITS' followed by a date and a time (in hours, minutes seconds).
      :type filename:
         String
      :param comment: 
         If you do not want to copy comments, set parameter to False
      :type comment:
         Boolean
      :param history: 
         If you do not want to copy history, set parameter to False
      :type history:
         Boolean
      :param bitpix:
         Write FITS data in another format (8, 16, 32, -32, -64).
         If no *bitpix* is entered then -32 is assumed. Parameters
         *bzero*, *bscale* and *blank* are ignored then.
      :type bitpix:
         Integer
      :param bzero:
         Offset in scaled data. If bitpix is not equal to -32 and the values
         for bscale and bzero are None, then the data is scaled between the 
         minimum and maximum data values. For this scaling the method scale() from
         PyFITS is used with ``option='minmax'``. However PyFITS 1.3 generates an
         error due to a bug. 
      :type bzero:
         Float
      :param bscale:
         Scale factor for scaled data. If bitpix is not equal to -32 and the values
         for bscale and bzero are None, then the data is scaled between the 
         minimum and maximum data values. For this scaling the method scale() from
         PyFITS is used with ``option='minmax'``. However PyFITS 1.3 generates an
         error due to a bug. 
      :type bscale:
         Float
      :param blank:
         Value that represents a blank. Usually only for scaled data.
      :type blank:
         Float/Integer
      :param clobber:
         If a file on disk already exists then an exception is raised.
         With *clobber=True* an existing file will be overwritten.
         We don't attempt to suppres PyFITS warnings because its warning
         mechanism depends on the Python version.
      :type clobber:
         Boolean
      :param append:
         Append image data in new HDU to existing FITS file
      :type append:
         Boolean
      :param extname:
         Name of image extension if append=True. Default is empty string.
      :type  extname:
         String

      :Raises:
         :exc:`ValueError`
             You will get an exception if the shape of your external data in parameter 'boxdat'
             is not equal to the current sliced data with limits.

      :Examples: Artificial header and data:

        ::
      
            # Example 1. From a Python dictionary header
            
            header = {'NAXIS' : 2, 'NAXIS1': 800, 'NAXIS2': 800,
                      'CTYPE1' : 'RA---TAN',
                      'CRVAL1' :0.0, 'CRPIX1' : 1, 'CUNIT1' : 'deg', 'CDELT1' : -0.05,
                      'CTYPE2' : 'DEC--TAN',
                      'CRVAL2' : 0.0, 'CRPIX2' : 1, 'CUNIT2' : 'deg', 'CDELT2' : 0.05,
                     }
            x, y = numpy.mgrid[-sizex1:sizex2, -sizey1:sizey2]
            edata = numpy.exp(-(x**2/float(sizex1*10)+y**2/float(sizey1*10)))
            f = maputils.FITSimage(externalheader=header, externaldata=edata)
            f.writetofits()

            # Example 2. From an external header and dataset.
            # In this example we try to copy the data format from the input file.
            # PyFITS removes header items BZERO and BSCALE because it reads its
            # data in a NumPy array that is compatible with BITPIX=-32.
            # The original values for *bitpix*, *bzero*, *bscale* and *blank*
            # are retrieved from the object attributes with the same name.
            
            from kapteyn import maputils

            fitsobject = maputils.FITSimage(promptfie=maputils.prompt_fitsfile)
            header = fitsobject.hdr 
            edata = fitsobject.dat
            f = maputils.FITSimage(externalheader=header, externaldata=edata)
            
            f.writetofits(history=True, comment=True, 
                          bitpix=fitsobject.bitpix,
                          bzero=fitsobject.bzero,
                          bscale=fitsobject.bscale,
                          blank=fitsobject.blank,
                          clobber=True)
                          
            # Example 3. Write a FITS file in the default format, BITPIX=-32
            # and don't bother about FITS history and comment cards.
            
            f.writetofits(history=False, comment=False)
      """
        if filename is None:
            filename = getfilename('mu', 'fits')
            append = False
        if append:
            try:
                f = pyfits.open(filename)
                f.close()
            except:
                append = False

        hdu = pyfits.PrimaryHDU(self.dat)
        pythondict = fitsheader2dict(self.hdr, comment, history)
        for key, val in pythondict.items():
            if key == 'HISTORY' or key == 'COMMENT':
                if history and key == 'HISTORY':
                    for v in val:
                        hdu.header.add_history(v)

                elif comment and key == 'COMMENT':
                    for v in val:
                        hdu.header.add_comment(v)

            else:
                try:
                    if pyfitsoldversion:
                        hdu.header.update(key, val, pythondict.comment[key])
                    else:
                        hdu.header[key] = (
                         val, pythondict.comment[key])
                except:
                    pass

        if bitpix is not None:
            code = hdu.NumCode[bitpix]
            if bzero is None and bscale is None:
                hdu.scale(code, option='minmax')
            else:
                if bzero is None:
                    bzero = 0.0
                if bscale is None:
                    bscale = 1.0
                hdu.scale(code, bzero=bzero, bscale=bscale)
            if blank is not None:
                hdu.header['BLANK'] = self.blank
        elif 'BLANK' in hdu.header:
            del hdu.header['BLANK']
        if append:
            hdu.header.update('EXTNAME', extname)
            pyfits.append(filename, self.dat, header=hdu.header)
        else:
            hdulist = pyfits.HDUList([hdu])
            hdulist.writeto(filename, clobber=clobber, output_verify='silentfix')
            hdulist.close()
        return

    def Annotatedimage(self, frame=None, **kwargs):
        """
      This method couples the data slice that represents an image to
      a Matplotlib Axes object (parameter *frame*). It returns an object
      from class :class:`Annotatedimage` which has only attributes relevant for
      Matplotlib.

      :param frame:
         Plot the current image in this Matplotlib Axes object.
         If omitted, a default frame will be set using
         Matplotlib's method *add_subplot()*
      :type frame:
         A Matplotlib Axes instance

      :param kwargs:
         These parameters are keyword arguments for the constructor of
         :class:`Annotatedimage`. All of them get a default value in this
         routine. The ones for which it can be useful to change are:

         * skyout: The sky definition for graticule and world coordinates
         * spectrans: The spectral translation for the spectral axis
         * aspect: The aspect ratio of the pixels
         * basename: A name for a file on disk e.g. to store a color lut
         * cmap: A color map
         * blankcolor: The color of bad pixels,
         * clipmin: Scale colors between image values clipmin and clipmax
         * clipmax: Scale colors between image values clipmin and clipmax
         * gridmode: Set modus of str2pos() to pixels or grids

      :type kwargs:
         Python keyword arguments

      :Attributes:
         See documentation at :class:`Annotatedimage`
      
      :Returns:
         An object from class :class:`Annotatedimage`

      :Examples:
         >>> f = maputils.FITSimage("ngc6946.fits")
         >>> f.set_imageaxes(1, 3, slicepos=51)
         >>> annim = f.Annotatedimage()

         or::

            from kapteyn import maputils
            from matplotlib import pyplot as plt
   
            f = maputils.FITSimage("m101.fits")
            fig = plt.figure()
            frame = fig.add_subplot(1,1,1)
            annim = f.Annotatedimage(frame)
            annim.Image()
            annim.Graticule()
            annim.plot()
            plt.show()

      """
        ar = self.get_pixelaspectratio()
        if 'basename' not in kwargs:
            basename = self.filename.rsplit('.')[0]
            kwargs['basename'] = basename
        else:
            basename = kwargs['basename']
        if frame is None:
            fig = figure()
            frame = fig.add_subplot(1, 1, 1, frameon=False)
        wcstypes = [self.wcstypes[(self.axperm[0] - 1)], self.wcstypes[(self.axperm[1] - 1)]]
        mplimage = Annotatedimage(frame, self.hdr, self.pxlim, self.pylim, self.boxdat, self.convproj, self.axperm, wcstypes, skyout=self.skyout, spectrans=self.spectrans, alter=self.alter, mixpix=self.mixpix, aspect=ar, slicepos=self.slicepos, sliceaxnames=self.sliceaxnames, sourcename=self.filename, **kwargs)
        return mplimage


class MovieContainer(object):
    """
This class is a container for objects from class :class:`maputils.Annotatedimage`.
For this container there are methods to alter the visibility
of the stored objects to get the effect of a movie loop.
The objects are appended to a list with method :meth:`maputils.MovieContainer.append`.
With method :meth:`MovieContainer.movie_events` the movie is started
and keys 'P', '<', '>', '+' and '-' are available to control the movie.

* 'P' : Pause/resume movie loop
* '<' : Step 1 image back in the sequence of images. Key ',' and arrow down has the same effect.
* '>' : Step 1 image forward in the sequence of images. Key '.' and arrow up has the same effect.
* '+' : Increase the speed of the loop. The speed is limited by the size of the image and
        the hardware in use.
* '-' : Decrease the speed of the movie loop

One can also control the movie with method :meth:`MovieContainer.controlpanel`

Usually one creates a movie container with class class:`Cubes`

:param helptext:
   Allow or disallow methods to set an informative text about the keys in use.
:type helptext:
   Boolean
:param imageinfo:
   Allow or disallow methods to set an informative text about which image
   is displayed and, if available, it prints information about the pixel
   coordinate(s) of the slice if the image was extracted from a data cube.
:type imageinfo:
   Boolean
:param slicemessages:
   A list with messages, associated with the frames in your movie.
   Usually one uses this option to gain some efficiency because there
   is no need to construct a message each time a frame is changed.
:type slicemessages:
   List with strings.

:Attributes:
   
    .. attribute:: annimagelist

       List with objects from class :class:`maputils.Annotatedimage`.
       
    .. attribute:: indx
    
       Index in list with objects of object which represents the current image.

    .. attribute:: framespersec

       A value in seconds, representing the interval of refreshing an image
       in the movie loop.

    .. attribute:: info

       An object of class infoObject which has an attribute for the index
       of the current frame ('indx') and an attribute with an informative message
       about the current displayed slice.

    
:Examples:
   Use of this class as a container for images in a movie loop:

   .. literalinclude:: EXAMPLES/mu_movie.py

   Skip informative text on the display:
   
   >>> movieimages = maputils.MovieContainer(helptext=False, imageinfo=False)

:Methods:

.. automethod:: append
.. automethod:: movie_events
.. automethod:: controlpanel
.. automethod:: setmessages
.. automethod:: setimage
.. automethod:: imageloop
.. automethod:: toggle_images
   """

    class infoObject(object):
        """
      Object which is a parameter of a registered callback function
      It returns the index of the current frame in attribute 'indx' and
      a message with physical coordinates of the slice position in attribute
      'mes'
      """

        def __init__(self):
            self.indx = 0
            self.mes = ''
            self.cubenr = None
            self.slicemessage = ''
            return

    record_fps = 15
    record_frameformat = 'png'
    record_bitrate = 1800
    record_outfile = 'visionsmovie.mp4'
    record_fnameformatstr = '%s%%07d.%s'
    record_basename = '_tmp_visions'
    record_removetmpfiles = True
    recdefs = dict(outfile=record_outfile, bitrate=record_bitrate, tmpprefix=record_basename, removetmp=record_removetmpfiles, fps=record_fps)

    def __init__(self, fig, helptext=True, imageinfo=True, slicemessages=[], toolbarinfo=False, sliceinfoobj=None, callbackslist={}):
        self.annimagelist = []
        self.indx = 0
        self.fig = fig
        self.textid = None
        self.helptext = helptext
        self.imageinfo = imageinfo
        self.slicemessages = slicemessages
        self.numimages = 0
        self.callbackinfo = self.infoObject()
        self.pause = True
        self.forward = True
        self.toolbarinfo = toolbarinfo
        self.sliceinfoobj = None
        self.currentcubenr = None
        self.movieframelist = []
        self.movielistindx = 0
        self.oldim = None
        self.compareim = None
        self.callbackslist = callbackslist
        self.framespersec = 20
        self.flushcounter = 0
        self.recording = False
        self.record_counter = 0
        self.set_recorddefaults()
        if self.helptext:
            delta = 0.01
            self.helptextbase = "Use keys 'p' to Pause/Resume. '+','-' to increase/decrease movie speed.  '<', '>' to step in Pause mode."
            speedtext = ' Speed=%d im/s' % self.framespersec
            self.helptext_id = self.fig.text(0.5, delta, self.helptextbase + speedtext + '\n' + colornavigation_info(), color='g', fontsize=8, ha='center')
        else:
            self.helptextbase = ''
            speedtext = ''
            self.helptext_id = None
        self.canvas = self.fig.canvas
        self.framespersec = 20
        self.cidkey = None
        self.cidscroll = None
        self.movieloop = TimeCallback(self.imageloop, 1.0 / self.framespersec)
        self.movieloop.deschedule()
        self.movieloop.once = False
        return

    def addcallbacks(self, cbs):
        """
      Helper function for to add one or more callbacks to
      the dictionary with registered callbacks. Parameter cbs should
      also be a dictionary.
      """
        self.callbackslist.update(cbs)

    def callback(self, cbid, *arg):
        """
      Helper function for registered callbacks
      """
        if cbid in self.callbackslist:
            self.callbackslist[cbid](*arg)

    def append(self, annimage, visible=True, cubenr=0, slicemessage=None):
        """
      Append object from class :class:`Annotatedimage`.
      First there is a check for the class
      of the incoming object. If it is the first object that is appended then
      from this object the Matplotlib figure instance is copied.
      
      :param annimage:
         Add an image to the list.
      :type annimage:
         An object from class :class:`Annotatedimage`.

      :param visible:
         Set the data in this object to visible or invisible. Usually one sets
         the first image in a movie to visible and the others to invisible.

      :Raises:
         'Container object not of class maputils.Annotatedimage!'
         An object was not recognized as a valid object to append.

      """
        if not isinstance(annimage, Annotatedimage):
            raise TypeError('Container object not of class maputils.Annotatedimage!')
        annimage.origdata = None
        annimage.image.im.set_visible(visible)
        self.annimagelist.append(annimage)
        self.numimages = len(self.annimagelist)
        if slicemessage is None:
            s = 'im #%d=slice:%s' % (self.numimages - 1, annimage.slicepos)
            annimage.slicemessage = s
        else:
            annimage.slicemessage = slicemessage
        annimage.cubenr = cubenr
        return

    def setmessages(self, slicemessages):
        """
      Set a list with messages that will be used to display information
      when a frame is changed. This message is either printed on the image
      or returned, using a callback function, to the calling environment.
      List may be smaller than the number of images in the movie.
      A message should correspond to the movie index number.
      """
        self.slicemessages = slicemessages

    def set_movieframes(self, framelist):
        """
      For INTERACTIVE use.
      Set the movie frame numbers that you want to display
      in a movie loop. If the list is None or empty, all images are
      part of the movieloop. The order of the numbers is arbitrary so
      many settings are possible (e.g. reverse order (100:0:-1) or skip
      images (0:100:2).

      Note:
      We don't perfrom any checking here. The only check is in the toggle_image
      method where we check whether the frame number in this list is a valid
      index.
      The entered list is associated to the movie container not
      to specific cubes.
      """
        self.movieframelist = framelist

    def movie_events(self, allow=True):
        """
      Connect keys for movie control and start the movie.
      Note that we defined the callbacks to trigger on the entire canvas.
      We don't need to connect it to a frame (AxesCallback). We have to
      disconnect the callbacks explicitly.

      """
        if len(self.annimagelist) == 0:
            return
        else:
            if allow:
                if self.cidkey:
                    self.fig.canvas.mpl_disconnect(self.cidkey)
                if self.cidscroll:
                    self.fig.canvas.mpl_disconnect(self.cidscroll)
                self.cidkey = self.fig.canvas.mpl_connect('key_press_event', self.controlpanel)
                self.cidscroll = self.fig.canvas.mpl_connect('scroll_event', self.controlpanel)
            else:
                if self.cidkey:
                    self.fig.canvas.mpl_disconnect(self.cidkey)
                if self.cidscroll:
                    self.fig.canvas.mpl_disconnect(self.cidscroll)
                self.cidkey = self.cidscroll = None
            return

    def controlpanel(self, event, externalkey=''):
        """
      Process the key and scroll events for the movie container.
      An external process (i.e. not the Matplotlib canvas) can access
      the control panel. It uses parameter 'externalkey'.
      In the calling environment one needs to set 'event' to None.
      """
        self.movieloop.once = False
        if event is None and externalkey == '':
            return
        else:
            if event is not None:
                try:
                    key = event.key.upper()
                    if key == 'UP':
                        key = '.'
                    if key == 'DOWN':
                        key = ','
                except AttributeError:
                    if event.button == 'up':
                        key = '.'
                    if event.button == 'down':
                        key = ','
                except:
                    return

            else:
                key = externalkey.upper()
            if key == 'P':
                if self.pause:
                    self.movieloop.schedule()
                    self.pause = False
                else:
                    self.movieloop.deschedule()
                    self.fig.canvas.draw()
                    self.pause = True
                self.callback('moviepause', self.pause, self.forward)
            elif key == 'START':
                if not self.pause:
                    self.movieloop.deschedule()
                    if not self.forward:
                        self.forward = True
                        self.movieloop.schedule()
                    else:
                        self.pause = True
                else:
                    self.forward = True
                    self.movieloop.schedule()
                    self.pause = False
            elif key == 'STARTBACK':
                if not self.pause:
                    self.movieloop.deschedule()
                    if self.forward:
                        self.forward = False
                        self.movieloop.schedule()
                    else:
                        self.pause = True
                else:
                    self.forward = False
                    self.movieloop.schedule()
                    self.pause = False
            elif key == 'STOP' and not self.pause:
                self.movieloop.deschedule()
                self.fig.canvas.draw()
                self.pause = True
            elif key == 'ONCE':
                self.forward = True
                self.movieloop.once = True
                self.movieloop.counter = 0
                if self.movieframelist:
                    self.movieloop.maxcount = len(self.movieframelist)
                else:
                    self.movieloop.maxcount = len(self.annimagelist)
                self.movieloop.schedule()
                self.pause = False
            elif key in ('+', '='):
                self.framespersec = min(self.framespersec + 1, 200)
                self.movieloop.set_interval(1.0 / self.framespersec)
                if self.helptext:
                    speedtxt = ' Speed=%d im/s' % self.framespersec
                    self.helptext_id.set_text(self.helptextbase + speedtxt)
                self.callback('speedchanged', self.framespersec)
            elif key in ('-', '_'):
                self.framespersec = max(self.framespersec - 1, 1)
                self.movieloop.set_interval(1.0 / self.framespersec)
                if self.helptext:
                    speedtxt = ' Speed=%d im/s' % self.framespersec
                    self.helptext_id.set_text(self.helptextbase + speedtxt)
                self.callback('speedchanged', self.framespersec)
            elif key in (',', '<', 'PREV'):
                if not self.pause:
                    self.movieloop.deschedule()
                    self.pause = True
                self.toggle_images(next=False)
            elif key in ('.', '>', 'NEXT'):
                if not self.pause:
                    self.movieloop.deschedule()
                    self.pause = True
                self.toggle_images(next=True)
            return

    def set_recorddefaults(self, outfile=None, fps=None, bitrate=None, removetmpfiles=None):
        """
      This method sets or overwrites the default parameters used to make a
      movie on disk of the recorded images (saved with savefig())
      Notes: The values cannot be expressions
      """
        if fps is None:
            self.record_fps = MovieContainer.record_fps
        else:
            mes = ''
            try:
                fps = int(fps)
                if fps < 0:
                    mes = 'Frames per second must be positive'
                    raise
                else:
                    self.record_fps = fps
            except:
                if not mes:
                    mes = 'Invalid expression for frames per second'
                raise Exception(mes)

            self.record_frameformat = MovieContainer.record_frameformat
            if bitrate is None:
                self.record_bitrate = MovieContainer.record_bitrate
            else:
                mes = ''
                try:
                    bitrate = int(bitrate)
                    if bitrate < 0:
                        mes = 'Bitrate must be a positive integer'
                        raise
                    else:
                        self.record_bitrate = bitrate
                except:
                    if not mes:
                        mes = 'Invalid expression for bitrate in kbit/s'
                    raise Exception(mes)

                if outfile is None:
                    self.record_outfile = MovieContainer.record_outfile
                else:
                    try:
                        self.record_outfile = str(outfile)
                        f = file(self.record_outfile, 'w+')
                        f.close()
                    except:
                        raise Exception('Cannot write this movie on disk (invalid directory?)')

            self.record_fnameformatstr = MovieContainer.record_fnameformatstr
            self.record_basename = MovieContainer.record_basename
            if removetmpfiles is None:
                self.record_removetmpfiles = MovieContainer.record_removetmpfiles
            else:
                try:
                    self.record_removetmpfiles = bool(removetmpfiles)
                except:
                    raise Exception('Invalid value for remove tmp file option')

        return

    @staticmethod
    def get_recorddefaults():
        """
      Return a dictionary with defaults for recording a movue on disk. The method
      is a static method so that the calling environment is able to obtain these
      defaults before any MovieContainer object is created i.e. in a GUI where
      we present the defaults before any image is recorded.
      """
        return MovieContainer.recdefs

    def set_recording(self, recording):
        """
      Method to set a flag to start or stop recording what is on screen using
      savefig(). Currently figures are recorded only if images are toggled.
      """
        if recording:
            self.recording = True
        else:
            self.recording = False

    def create_recording(self):
        """
      Method creates a movie from screendumps on disk. The utility needed to
      create a movie is 'ffmpeg'.
      NOTE: ffmpeg is deprecated. Use 'avconv' in the near future
      ffmpeg:   -f fmt -> Force format
                -vcodec -> Force video codec to codec
                -s -> '-s', '%dx%d' % self.frame_size # Frame seize. Default is same as source
                -pix_fmt -> Set pixel format
                -r fps-> Set frame rate (Hz value, fraction or abbreviation), (default = 25)
                -b brt -> Video bitrate of the output file
                -y -> Overwrite existing filenam
      """
        from glob import glob
        if self.record_counter == 0:
            raise Exception('No images available to create a movie!<br> Start recording first.')
        cmd = 'ffmpeg'
        basename = self.record_fnameformatstr % (self.record_basename, self.record_frameformat)
        args = [cmd, '-vframes', str(self.record_counter),
         '-r', str(self.record_fps), '-i', basename]
        if self.record_bitrate > 0:
            args.extend(['-b', '%dk' % self.record_bitrate])
        args.extend(['-y', self.record_outfile])
        try:
            proc = check_call(args, shell=False, stdout=PIPE, stderr=PIPE)
        except OSError:
            raise Exception('Cannot find ffmpeg to create movie')
        except CalledProcessError as message:
            raise Exception('Something wrong in parameters for command ffmpeg')
        except:
            raise Exception('Unknown error creating a movie with ffmpeg')

        if self.record_removetmpfiles:
            files = glob('%s*.%s' % (self.record_basename, self.record_frameformat))
            for f in files:
                remove(f)

        pics = self.record_counter
        self.record_counter = 0
        return (pics, (' ').join(args))

    def imageloop(self, cb):
        """
      Helper method to get movie loop

      :param cb:
          Mouse event object with pixel position information.
      :type cb:
          Callback object based on matplotlib.backend_bases.MouseEvent instance
      """
        self.toggle_images(self.forward)

    def setspeed(self, framespersec):
        """
      Change movie speed by changing timer interval.
      Note that speed can be < 1.0
      """
        self.framespersec = max(framespersec, 0)
        self.framespersec = min(self.framespersec, 200)
        self.movieloop.set_interval(1.0 / self.framespersec)
        if self.helptext:
            speedtxt = ' Speed=%d im/s' % self.framespersec
            self.helptext_id.set_text(self.helptextbase + speedtxt)

    def setimage(self, i, force_redraw=False):
        """
      Set a movie frame by index number. If the index is invalid, then do
      nothing.

      :param i:
          Index of movie frame which is any number between 0 and the
          number of loaded images.
      """
        if i is None:
            return
        else:
            if 0 <= i < self.numimages:
                self.toggle_images(indx=i, force_redraw=force_redraw)
            return

    def toggle_images(self, next=True, indx=None, force_redraw=False):
        """
      Toggle the visible state of images either by a timed callback
      function or by keys.
      This toggle works if one stacks multiple images in one frame
      with method :meth:`MovieContainer.append`.
      Only one image gets status visible=True. The others
      are set to visible=False. This toggle changes this visibility
      for images and the effect, is a movie.
      
      :param next:
         Step forward through list if next=True. Else step backwards.
      :type next:
         Boolean
      :param indx:
         Set image with this index
      :type indx:
         Integer
      :param force_redraw:
         Boolean flag to force everything to be repainted, which would
         otherwise only occur if there is a change of cubes
      """
        if self.movieloop.once:
            if self.movieloop.counter == self.movieloop.maxcount:
                self.oldim.once = False
                self.movieloop.once = False
                self.movieloop.deschedule()
                self.fig.canvas.draw()
                self.pause = True
                return
            self.movieloop.counter += 1
        cubechanged = False
        xd = None
        yd = None
        if indx is not None:
            newmovieframeindx = indx
            self.indx = newmovieframeindx
        else:
            if not self.annimagelist:
                return
            fromlist = self.movieframelist
            if fromlist:
                movielistindx = self.movielistindx
                if next:
                    if movielistindx + 1 >= len(self.movieframelist):
                        movielistindx = 0
                    else:
                        movielistindx += 1
                else:
                    if movielistindx - 1 < 0:
                        movielistindx = len(self.movieframelist) - 1
                    else:
                        movielistindx -= 1
                    newmovieframeindx = self.movieframelist[movielistindx]
                    self.movielistindx = movielistindx
                    if newmovieframeindx >= len(self.annimagelist) or newmovieframeindx < 0:
                        return
            else:
                currindx = self.indx
                if next:
                    if currindx + 1 >= len(self.annimagelist):
                        currindx = 0
                    else:
                        currindx += 1
                else:
                    if currindx - 1 < 0:
                        currindx = len(self.annimagelist) - 1
                    else:
                        currindx -= 1
                    newmovieframeindx = currindx
                    self.indx = newmovieframeindx
                oldim = self.oldim
                resets = 0
                if self.compareim:
                    self.compareim.image.im.set_alpha(1.0)
                    self.compareim.image.im.set_visible(False)
                    self.compareim = None
                    if oldim:
                        resets += 1
                if oldim is not None:
                    if oldim.origdata is not None:
                        oldim.data[:] = oldim.origdata[:]
                        oldim.origdata = None
                        oldim.image.im.set_data(oldim.data)
                        oldim.set_blankcolor(oldim.old_blankcolor[0], oldim.old_blankcolor[1])
                        splitimage = self.annimagelist[oldim.splitmovieframe]
                        splitimage.image.im.set_visible(False)
                        resets += 1
                    if oldim.blurred:
                        oldim.set_blur(False)
                        resets += 1
                    if oldim.histogram:
                        oldim.set_histogrameq(False)
                        resets += 1
                    if resets:
                        self.callback('imagereset')
                    oldim.image.im.set_visible(False)
                    oldim.disconnectCallbacks()
                    if self.toolbarinfo:
                        x = oldim.X_lastvisited
                        y = oldim.Y_lastvisited
                        if None not in [x, y]:
                            xd, yd = oldim.frame.transData.transform((x, y))
                newim = self.annimagelist[newmovieframeindx]
                if newim.backgroundImageNr:
                    backgroundimage = self.annimagelist[newim.backgroundImageNr]
                    newim.image.im.set_visible(False)
                    backgroundimage.image.im.set_visible(True)
                else:
                    newim.image.im.set_visible(True)
                info = newim.infoobj
                if info:
                    info.set_text(newim.slicemessage)
                oldcubenr = -1
                if newim.cubenr != self.currentcubenr or force_redraw:
                    oldcubenr = self.currentcubenr
                    cubechanged = True
                    self.currentcubenr = newim.cubenr
                    if oldim is not None:
                        for li in oldim.linepieces:
                            li.set_visible(False)

                        for tl in oldim.textlabels:
                            tl.set_visible(False)

                        if oldim.infoobj:
                            oldim.infoobj.set_visible(False)
                        if oldim.hascolbar and oldim.cbframe:
                            oldim.cbframe.set_visible(False)
                        if oldim.splitcb:
                            oldim.splitcb.deschedule()
                        if oldim.contourSet:
                            for col in oldim.contourSet.collections:
                                col.set_visible(False)

                    for li in newim.linepieces:
                        li.set_visible(True)

                    for tl in newim.textlabels:
                        tl.set_visible(True)

                    if newim.contours_on and newim.contourSet:
                        for col in newim.contourSet.collections:
                            col.set_visible(True)

                    if newim.infoobj:
                        newim.infoobj.set_visible(True)
                    if newim.splitcb:
                        newim.splitcb.schedule()
                    if newim.cbframe:
                        if newim.hascolbar:
                            newim.cbframe.set_visible(True)
                        else:
                            newim.cbframe.set_visible(False)
                    self.canvas.draw()
                    doflush = True
                    self.callback('cubechanged', newim)
                else:
                    if oldim and oldim.contourSet:
                        for col in oldim.contourSet.collections:
                            col.set_visible(False)

                    doflush = False
                    if newim.backgroundImageNr:
                        newim.frame.draw_artist(backgroundimage.image.im)
                    else:
                        newim.frame.draw_artist(newim.image.im)
                    if info:
                        newim.frame.draw_artist(info)
                    for li in newim.linepieces:
                        newim.grat.frame.draw_artist(li)

                for tl in newim.textlabels:
                    newim.frame.draw_artist(tl)

            if newim.contours_on:
                if not newim.contourSet or newim.contours_changed:
                    if newim.contours_cmap:
                        cs = newim.Contours(newim.clevels, cmap=cm.get_cmap(newim.contours_cmap))
                    else:
                        if not newim.contours_colour:
                            newim.contours_colour = 'r'
                        cs = newim.Contours(newim.clevels, colors=newim.contours_colour)
                    cs.plot(newim.frame)
                    newim.contourSet = cs.CS
                    newim.contours_changed = False
                for col in newim.contourSet.collections:
                    col.set_visible(True)
                    newim.frame.draw_artist(col)

            self.canvas.blit(newim.frame.bbox)
        newX = newY = None
        newim.interact_imagecolors()
        if self.toolbarinfo:
            newim.interact_toolbarinfo()
            newim.interact_writepos(pixfmt=newim.coord_pixfmt, dmsprec=newim.coord_dmsprec, wcsfmt=newim.coord_wcsfmt, zfmt=newim.coord_zfmt, gipsy=True, grids=newim.coord_grids, world=newim.coord_world, worlduf=newim.coord_worlduf, imval=newim.coord_imval, g_typecli=newim.coord_tocli, g_tolog=newim.coord_tolog, g_appendcr=newim.coord_appendcr)
            cb = newim.toolbarkey
            if None not in [xd, yd]:
                cb.xdata, cb.ydata = newim.frame.transData.inverted().transform((xd, yd))
                newim.mouse_toolbarinfo(cb)
                newX, newY = cb.xdata, cb.ydata
        self.oldim = newim
        self.callbackinfo.mes = newim.slicemessage
        self.callbackinfo.indx = newmovieframeindx
        self.callbackinfo.cubenr = newim.cubenr
        self.callbackinfo.slicemessage = newim.composed_slicemessage
        self.callback('movchanged', self.callbackinfo)
        if doflush:
            self.canvas.flush_events()
        self.callback('crosshair', self.indx, cubechanged, oldcubenr)
        if cubechanged:
            self.callback('zprofile', None, newX, newY, newim.cubenr)
        if self.recording:
            filenam = '%s%07d.%s' % (self.record_basename, self.record_counter, self.record_frameformat)
            self.record_counter += 1
            self.fig.savefig(filenam)
        return


class Cubeatts(object):
    """
   Class that sets cube attributes. The constructor is called by the :meth:`maputils.Cubes.append`
   method of class :class:`maputils.Cubes` and should not be used otherwise.
   We document the class because it has some useful attributes.
   
   The attributes should only be used as a read-only attribute.
   
   :param xxx:
      All parameters are set by the :class:`maputils.Cubes` class.
   
   :Attributes:
       
    .. attribute:: frame
    
       Matplotlib Axes object used to display the current image. The attribute should 
       only be used as a read-only attribute.
       
    .. attribute:: pxlim, pylim
    
       The axes limits in pixels. The attribute should 
       only be used as a read-only attribute.
       
    .. attribute:: slicepos
    
       Attribute ``slicepos`` is documented in :meth:`maputils.Cubes.append`.
       It is a sequence with numbers or tuples with numbers.
       The attribute should only be used as a read-only attribute.
       
    .. attribute:: fitsobj
    
       Object from class :class:`maputils.FITSimage`
       
    .. attribute:: pixelaspectratio
    
       This attribute stores the aspect ratio of the pixels in the images of this cube.
       
    .. attribute:: nummovieframes
    
       This attribute stores the number of images in this cube.
       
    .. attribute:: hasgraticule
    
       Boolean which flags whether one requested to plot a graticule
       
    .. attribute:: gridmode
    
       Boolean which flags wheter one requested positions in grids or in pixels.
       Pixels follow the FITS syntax. That is, the first pixel along an axis
       is pixel 1. The last pixel is pixel NAXISn. NAXIS is a header item and n
       is the axis number (starting with 1). FITS headers also contain an key
       CRPIXn. This is the number (may be non-integer) of the pixel where 
       the projection center is located. If ``gridmode==True``, the position
       of CRPIX is labeled 0. The mode applies to the output of positions.
       
    .. attribute:: cmap
    
       The current color lookup table (color mapping). 
       
    .. attribute:: hascolbar
    
       Boolean which flag whether one requested to draw a color bar.
       
    .. attribute:: vmin, vmax
    
       Attributes which store the minimum and maximum clip values to display the data.
       
    .. attribute:: datmin, datmax
    
       Attributes which stores the minimum and maximum data values.
       They are used to set the default clip levels.
       
    .. attribute:: mean
    
       Mean of all the data values in this cube. It gets its value for certain values
       of attribute ``clipmode``.
       
    .. attribute:: rms
    
       Root mean square of all the data values in this cube.
       It gets its value for certain values
       of attribute ``clipmode``.
       
    .. attribute:: clipmode
    
       Stores the requested mode which sets the clip values.
       The modes are documented in method :meth:`maputils.Cubes.append`.
       
    .. attribute:: clipmn
    
       Stores the requested number of times (m, n) the value of the rms
       is used to set the clip values around the mean.
       The modes are documented in method :meth:`maputils.Cubes.append`.
   """

    def __init__(self, frame, fitsobj, axnums, slicepos=[], pxlim=None, pylim=None, vmin=None, vmax=None, hasgraticule=False, gridmode=False, hascolbar=True, pixelaspectratio=None, clipmode=0, clipmn=(4, 5), callbackslist={}):
        self.frame = frame
        self.pxlim = pxlim
        self.pylim = pylim
        if pxlim is None:
            self.pxlim = (
             1, fitsobj.axisinfo[axnums[0]].axlen)
        if pylim is None:
            self.pylim = (
             1, fitsobj.axisinfo[axnums[1]].axlen)
        self.slicepos = slicepos
        self.fitsobj = fitsobj
        self.pixelaspectratio = pixelaspectratio
        if slicepos:
            self.nummovieframes = len(slicepos)
        else:
            self.nummovieframes = 1
        self.hasgraticule = hasgraticule
        self.gridmode = gridmode
        self.xold = None
        self.yold = None
        self.framep1 = None
        self.framep2 = None
        self.annimp1 = None
        self.annimp2 = None
        self.linepieces = set()
        self.textlabels = set()
        self.grat = None
        anums = [
         axnums[0], axnums[1]]
        n = fitsobj.naxis
        if n > 2:
            for i in range(n):
                axnr = i + 1
                if axnr not in anums:
                    anums.append(axnr)

        self.axnums = anums
        self.movieframeoffset = None
        self.lastimagenr = 0
        self.panelXframes = []
        self.panelYframes = []
        self.cmap = None
        self.panelscb = None
        self.splitcb = None
        self.origdata = None
        self.set_xvprojections()
        self.preparefirst = True
        self.cnr = None
        self.hascolbar = hascolbar
        self.cbframe = None
        self.imagesinthiscube = []
        self.shortfilename = os_basename(self.fitsobj.filename)
        self.callbackslist = callbackslist
        lineprops = {'animated': False, 'linewidth': 1}
        self.lineh = self.frame.axhline(xmin=MINBOUND, xmax=MAXBOUND, visible=False, **lineprops)
        self.linev = self.frame.axvline(ymin=MINBOUND, ymax=MAXBOUND, visible=False, **lineprops)
        self.panelxline = None
        self.panelyline = None
        self.needclear = False
        self.background = None
        self.panelXback = None
        self.panelYback = None
        self.vmin = vmin
        self.vmax = vmax
        self.zmin = vmin
        self.zmax = vmax
        self.vmin_def = None
        self.vmax_def = None
        self.datmin = None
        self.datmax = None
        self.mean = None
        self.rms = None
        self.clipmode = clipmode
        self.clipmn = clipmn
        self.scalefac = None
        self.limitsinfo = None
        self.setlimits = []
        return

    def callback(self, cbid, *arg):
        """
      Helper function for registered callbacks
      """
        if cbid in self.callbackslist:
            self.callbackslist[cbid](*arg)

    def cubestats(self):
        """
      Given the datmin, datmax, mean and rms attributes of all the images in
      this cube, calculate the same attributes for the entire cube

      Formulas are explained in article on:
      http://en.wikipedia.org/wiki/Standard_deviation
      Section: Population-based statistics
      """
        if not self.imagesinthiscube:
            return
        else:
            alldatmin = []
            alldatmax = []
            allmean = []
            allrms = []
            for aim in self.imagesinthiscube:
                if aim.datmin is not None and numpy.isfinite(aim.datmin):
                    alldatmin.append(aim.datmin)
                if aim.datmax is not None and numpy.isfinite(aim.datmax):
                    alldatmax.append(aim.datmax)
                if aim.mean is not None and numpy.isfinite(aim.mean):
                    allmean.append(aim.mean)
                if aim.rms is not None and numpy.isfinite(aim.rms):
                    allrms.append(aim.rms)

            if len(alldatmin):
                self.datmin = min(list(alldatmin))
            if len(alldatmax):
                self.datmax = max(list(alldatmax))
            n = 0
            mean_t = 0.0
            rms_t = 0.0
            for mean, rms in zip(allmean, allrms):
                if rms and mean:
                    n += 1
                    mean_t += mean
                    rms_t += rms * rms + mean * mean

            if n:
                self.mean = mean_t / n
                self.rms = numpy.sqrt(rms_t / n - self.mean * self.mean)
            else:
                self.mean = self.rms = None
            return

    def imagestats(self):
        """
      For each image in this cube, calculate the values for the
      data min., data max., mean and rms.
      """
        if not self.imagesinthiscube:
            return
        for aim in self.imagesinthiscube:
            aim.datmin, aim.datmax, aim.mean, aim.rms = aim.get_stats()

        self.cubestats()

    def setcubeclips(self, clipmin=None, clipmax=None, clipmode=0, clipmn=(4, 5)):
        if not self.imagesinthiscube:
            return
        else:
            if None in (clipmin, clipmax) or clipmode in (1, 2):
                if None in [self.datmin, self.datmax, self.mean, self.rms]:
                    self.cubestats()
            if clipmode == 0:
                if clipmin is None:
                    clipmin = self.datmin
                if clipmax is None:
                    clipmax = self.datmax
            if clipmode == 1:
                clipmin = self.datmin
                clipmax = self.datmax
            if clipmode == 2:
                if self.mean and self.rms:
                    clipmin = self.mean - clipmn[0] * self.rms
                    clipmax = self.mean + clipmn[1] * self.rms
            if clipmin is None:
                if clipmax is not None:
                    clipmin = clipmax - 1.0
                else:
                    clipmin = 0.0
            if clipmax is None:
                if clipmin is not None:
                    clipmax = clipmin + 1.0
                else:
                    clipmax = 1.0
            self.vmin = clipmin
            self.vmax = clipmax
            for aim in self.imagesinthiscube:
                aim.image.im.set_clim(min(clipmin, clipmax), max(clipmin, clipmax))

            canvas = aim.frame.figure.canvas
            canvas.draw()
            return

    def set_slicemessages(self, spectrans):
        """
      Change slice messages to comply with this spectral translation.
      Apply message change to all Annotatedimage objects in this cube.

      :param spectrans:
         A coded spectral translation e.g. FREQ, WAVE or VRAD
         with translation code (e.g. V2F) or questionmarks as
         wildcard (e.g. VRAD-???)
      :type spectrans:
         String

      :Notes:

         After the slice messages are set, we have to refresh the image
         if a message was required on the image. After loading this is done
         by setting the image to the first loaded image (for this cube).
         If this method is called externally, the caller is responsible for
         refreshing the current image.
      """
        if not self.imagesinthiscube:
            return
        else:
            axnames = []
            crpix = []
            for an in self.axnums[2:]:
                axi = self.fitsobj.axisinfo[an]
                if axi.wcstype == 'spectral' and spectrans:
                    axnames.append(spectrans.split('-')[0])
                else:
                    axnames.append(axi.axname)
                crpix.append(axi.crpix)

            for i, aim in enumerate(self.imagesinthiscube):
                j = i + self.movieframeoffset
                s = ''
                sc = 'im%3d: %s ' % (j, os_basename(self.fitsobj.filename))
                if self.slicepos:
                    if not issequence(self.slicepos[i]):
                        splist = [
                         self.slicepos[i]]
                    else:
                        splist = self.slicepos[i]
                    self.fitsobj.slicepos = splist
                    vlist, ulist = self.fitsobj.slice2world(skyout=None, spectra=spectrans, userunits=None)
                    if self.gridmode:
                        splist = [ splist[k] - crpix[k] for k in range(len(splist)) ]
                    for v, u, aname, sp in zip(vlist, ulist, axnames, splist):
                        s += '%s(%d)=%+-g' % (aname, sp, v)
                        if u:
                            s += ' (%s)' % u
                        s += '  '

                    s = s.strip()
                aim.slicemessage = s
                aim.composed_slicemessage = sc + ' ' + s
                aim.imnr = j
                aim.spectrans = spectrans

            return

    def set_panelXframes(self, framelist):
        """
      For the current cube, build a list with indices which all represent a
      slice in the panel that is parallel to the X axis.
      Prepare a data array for this slice panel.
      Remember that you have set up a 'movie cube' (which can be composed out
      of more than one data source). In this movie cube one can imagine a third
      axis perpendicular to the image axes. Along this axis, one can take a
      slice through the data. The sliced data can be represented in an image
      (e.g. a position-velocity diagram). The positions on the third axis
      are indices of the movie frame array and need not to be contiguous or
      ordered.
      """
        self.panelXframes = framelist
        if self.panelXframes:
            lx = int(self.pxlim[1] - self.pxlim[0] + 1)
            ly = int(len(self.panelXframes))
            self.Mx = numpy.zeros((ly, lx))

    def set_panelYframes(self, framelist):
        """
      For the current cube, build a list with indices which all represent a
      slice in the panel that is parallel to the Y axis.
      Prepare a data array for this slice panel.
      See also text at set_panelXframes().
      """
        self.panelYframes = framelist
        if self.panelYframes:
            ly = int(self.pylim[1] - self.pylim[0] + 1)
            lx = int(len(self.panelYframes))
            self.My = numpy.zeros((ly, lx))

    def set_xvprojections(self):
        """
      Is there an axis in the set that is not part of the image?
      We may need this axis later if we need a 'missing' spatial axis
      """
        ap = set(range(1, self.fitsobj.naxis + 1))
        apsub = set(self.axnums[:2])
        apdiff = list(ap.difference(apsub))
        if apdiff:
            dummyax = apdiff[0]
        else:
            dummyax = None
        fo = self.fitsobj
        if dummyax:
            spatials = [
             fo.proj.lataxnum, fo.proj.lonaxnum]
            if self.axnums[0] in spatials and dummyax in spatials:
                convproj = fo.proj.sub((self.axnums[0], dummyax))
            elif not (self.axnums[0] in spatials or dummyax in spatials):
                axperm = (
                 self.axnums[0], dummyax)
                convproj = fo.proj.sub(axperm)
            elif fo.proj.lonaxnum in [dummyax, self.axnums[0]]:
                axperm = (
                 self.axnums[0], dummyax, fo.proj.lataxnum)
                convproj = fo.proj.sub(axperm)
            else:
                axperm = (
                 self.axnums[0], dummyax, fo.proj.lonaxnum)
                convproj = fo.proj.sub(axperm)
            self.panelx_axperm = (
             self.axnums[0], dummyax)
        else:
            convproj = fo.convproj
            self.panelx_axperm = (self.axnums[0], self.axnums[1])
        self.panelx_proj = convproj
        if dummyax:
            spatials = [fo.proj.lataxnum, fo.proj.lonaxnum]
            if self.axnums[1] in spatials and dummyax in spatials:
                convproj = fo.proj.sub((dummyax, self.axnums[1]))
            elif not (self.axnums[1] in spatials or dummyax in spatials):
                axperm = (
                 self.axnums[1], dummyax)
                convproj = fo.proj.sub(axperm)
            elif fo.proj.lonaxnum in [dummyax, self.axnums[1]]:
                axperm = (
                 dummyax, self.axnums[1], fo.proj.lataxnum)
                convproj = fo.proj.sub(axperm)
            else:
                axperm = (
                 dummyax, self.axnums[1], fo.proj.lonaxnum)
                convproj = fo.proj.sub(axperm)
            self.panely_axperm = (
             dummyax, self.axnums[1])
        else:
            convproj = fo.convproj
            self.panely_axperm = (self.axnums[0], self.axnums[1])
        self.panely_proj = convproj
        return


class Cubes(object):
    """
A container with Cubeatts objects. With this class we build the movie container
which can store images from different data cubes.

:param toolbarinfo:
   This flag sets an informative message in the toolbar. For the QT backend
   the message is printed on a separate line at the bottom of the plot.
   The message contains information about the position of the cursor and
   when possible, it will show the corresponding world coordinates. Also the
   pixel value is printed.
   If you display a slice panel, then the information about the mouse position
   is different. For example the y direction of the horizontal slice panel is
   not a function of a world coordinate, but a function of movie frame number.
   This number can be used to find a world coordinate.
:type toolbarinfo:
   Boolean

:param imageinfo:
   If set to True, a label will be plotted in the upper left corner of
   your plot. The label contains information about the current image, such as
   the name of the repeat axis and the value on the repeat axis in physical
   coordinates.
:type imageinfo:
   Boolean

:param printload:
   If True, print a message on the terminal about the image that is loading.
:type printload:
   Boolean

:param helptext:
   Print a message at the bottom of the figure with information about the
   navigation.
:type helptext:
   Boolean

:param callbackslist:
   To be able to interfere or interact with the cube viewer we need to
   know the status of processes in maputils, like when is the loading of images finished
   or when does the image viewer switches between two images from a different cube.
   These events are sometimes related to the container with cubes, sometimes they
   are specific for a cube, see also :meth:`maputils.Cubes.append`. 
   To handle these events, one must connect it to a function
   or an object with methods. For a :class:`maputils.Cubes` container we have defined two events:

   *  'progressbar' -- The progress bar is an
      object from a class that (somehow) displays the progress. It should have at
      least four methods:  
         
         1) ``setMinimum()``
         2) ``setMaximum()``
         3) ``setValue()`` 
         4) ``reset()``
         
      For example in a PyQt4 gui we can define `progressbar` with an object from class 
      ``QProgressBar()``. This class provides already the necessary methods.
      The PyQt4 progress bar displays percentages. Maputils sets its range between
      zero and the number of movie frames (images) contained in the new cube.
      Usually, loading 1 image is too fast for a useful progress bar, but
      with numerous images in a cube, it is convenient to know the progress of the loading
      process. 
      
   *  'memory' --  Every time Maputils calls a function associated with trigger 'memory', a 
      string is generated with a 'used memory' report. The function should have only one argument
      and this argument is set by Maputils to the requested string with memory information.
      
   *  'cubechanged' -- If images are loaded from different data cubes and a user
      changes the viewer to display an image from a different cube, then the handler 
      for this trigger is executed.
      The trigger must be handled by a
      function with at least one parameter and this parameter (the first) is returned as object from 
      class :class:`maputils.Annotatedimage`
      
   *  'imagereset' --
      Actions like transparency setting, splitting, blurring and histogram
      equalization are restricted to the current image and are
      undone after changing to another image in the movie container.
      This trigger can update a GUI with this information (e.g. reset a transparency slider).
      The trigger must be handled by a function that does not need to have any
      parameter because nothing will be returned. 
      
   *  'movchanged' -- The function that handles the event has a parameter which is an object
      with four attributes:

         * ``mes`` -- A string which contains information about the slicemessage
         * ``indx`` -- The index of the image in the movie container with all images
         * ``cubenr`` -- The index of the cube to which the current image belongs. The
           index is for the list :attr:`maputils.Cubes.cubelist`
         * ``slicemessage`` -- A string with information about the image (name and axis names)      
      
   *  'speedchanged' -- User changed frame rate. The function has at least one parameter (the first)
      which stores the new frame rate in frames per second.
      
   *  'moviepaused' -- User pressed keyboard key 'P' to start or stop a movie. 
      The function has at least two parameters (the first and second)
      which stores the the pause status as a Boolean and the forward/backward status as a Boolean.
      
   *  'finished' -- All images are loaded and mouse- and keyboard interaction with
      the canvas is enabled. A similar callback is found in method :meth:`maputils.Cubes.append`         
      but the difference is that 'finished' is triggered only after all stacked append actions are 
      finished, while 'cubeloaded` is triggered as soon images from a cube are loaded.
                  
:type callbackslist:
   Python dictionary with function names and function pointers
   
:Example: Example 1 (Use callback functions in the constructor of a Cubes object)
      
   ::   
   
      from matplotlib.pyplot import figure, show
      from kapteyn import maputils

      def writeMemory(mem):
         print mem

      class ProgressBar(object):
         def __init__(self):
            self.value = 0
         def setMinimum(self, x):
            self.minimum = x
         def setMaximum(self, x):
            self.maximum = x
         def setValue(self, x):
            self.value = x
            print "Progress: %d %%"%(100.0*self.value/(self.maximum-self.minimum))
         def reset(self):
            self.value = self.minimum

      def cubeChanged(newim, x=10):
         print "Viewer changed cube with image", newim, x

      def imageChange(imageinfo):
         print "New image with movie container index:", imageinfo.indx
         print "Image belongs to cube number:", imageinfo.cubenr
         print "Short info:", imageinfo.mes
         print "Long info:", imageinfo.slicemessage 

      def imageReset():
         print "User changed images, but the previous was changed by temporary settings (e.g. splitting)"

      def printFinish():
         print "Loading finished and user interaction has been started"

      def speedChanged(framerate):
         print "User changes speed of movie loop to %d fr/s"%framerate

      fig = figure()
      frame = fig.add_subplot(1,1,1)
      progressBar = ProgressBar()
      myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False, 
                        callbackslist={'memory'       : writeMemory,
                                       'progressbar'  : progressBar,
                                       'cubechanged'  : cubeChanged,
                                       'imagereset'   : imageReset,
                                       'speedchanged' : speedChanged,
                                       'movchanged'   : imageChange,
                                       'finished'     : printFinish})
      fitsobject = maputils.FITSimage('ngc6946.fits')
      myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=range(1,101))

      frame = fig.add_subplot(1,1,1, label='m101')
      fitsobject2 = maputils.FITSimage('m101.fits')
      myCubes.append(frame, fitsobject2, axnums=(1,2))

:Example: Use two different cube containers connected to two different figures

   ::
   
      from matplotlib.pyplot import figure, show
      from kapteyn import maputils

      def externalMes(pos):
         print "Position cube 1:", pos

      def externalMes2(pos):
         print "Position cube 2:", pos

      def postLoading(cubecontainer, splitfr, slicepos):
         print "Set frame to compare with to:", splitfr
         cubecontainer.set_splitimagenr(splitfr)
         cubecontainer.set_panelframes(range(len(slicepos)), panel='XY')

      fig = figure()
      myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)

      frame = fig.add_subplot(1,1,1, label='ngc6946')
      fitsobject = maputils.FITSimage('ngc6946.fits')
      splitfr = 30
      slicepos = range(1,102)

      # Create a lambda function, but make sure it uses the current values
      # for the cube container (Cubes() object)
      cubeLoaded = lambda A=myCubes, B=splitfr, C=slicepos: postLoading(A,B,C)
      myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=slicepos,
                     callbackslist={'exmes'      : externalMes,                              
                                    'cubeloaded' : cubeLoaded})

      fig2 = figure(2)
      myCubes = maputils.Cubes(fig2, toolbarinfo=True, printload=False)

      frame2 = fig2.add_subplot(1,1,1, label='m101')
      fitsobject2 = maputils.FITSimage('ngc6946.fits')
      myCubes.append(frame2, fitsobject2, axnums=(1,3), slicepos=range(1,101),
                     callbackslist={'exmes' : externalMes2})

      show()
         

:Attributes:
   
    .. attribute:: calbackslist
    
       List with strings which correspond to the triggers in parameter `maputils.Cubes.callbackslist`
       The list is filtered and contains only known triggers. Triggers for the 
       MovieContainer object are filtered and passed to the constructor of this object.
    
    .. attribute:: colbwpixels
    
       Class attribute which sets a fixed width for the color bar in pixels.
       e.g.:: 
       
          myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)
          myCubes.colbwpixels = 100

    .. attribute:: crosshair
    
       Boolean which flags whether a cross hair cursor has been set or not.
 
    .. attribute:: cubelist
       
       Python list with cubes appended to this list by method :meth:`maputils.Cubes.append`.

    .. attribute:: currentcube
    
       This cube containers can store multiple cubes. Each cube (object of class :class:`maputils.Cubeatts`)
       is stored in the list :attr:`maputils.Cubes.cubelist`. The current cube is the cube to which
       the image on display belongs. This current cube is also an object of
       :class:`maputils.Cubeatts`.

    .. attribute:: fig
    
       The Matplotlib Figure used to display the images in the cubes container

    .. attribute:: imageinfo
    
       The status of Boolean parameter ``imageinfo``

    .. attribute:: numcubes
    
       The number of cubes with images stored in this container
       
    .. attribute:: movieimages
    
       The container of class :class:`maputils.MovieContainer`
    
    .. attribute:: printload
    
       The status of Boolean parameter ``printload``
   
    .. attribute:: splitmovieframe

       Number of movie frame which contains the image which we want to
       use together with the current image to split. The attribute is
       set with :meth:`maputils.Cubes.set_splitimagenr`.
       
    .. attribute:: toolbarinfo
    
       The status of Boolean parameter ``toolbarinfo``
 
    .. attribute:: zprofileheight
                
       Class attribute to set the height of the plot with the z-profile.
       The height is given in normalized device coordinates [0,1]. The height is 
       set to 0.1 by default.
       The other plots on your canvas will adjust to fit the new height. You can set the 
       new height immediately after you created a cubes container, e.g.::
       
          myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)
          myCubes.zprofileheight = 0.3       
   
   

    .. attribute:: zprofileOn
       
       Boolean which flags whether a z-profile plot has been requested or not.
   
   
:Methods:

.. automethod:: append
.. automethod:: set_aspectratio
.. automethod:: set_colbar_on
.. automethod:: set_coordinate_mode
.. automethod:: set_crosshair
.. automethod:: set_graticule_on
.. automethod:: set_panelframes
.. automethod:: set_skyout
.. automethod:: set_spectrans
.. automethod:: set_splitimagenr
.. automethod:: set_zprofile
.. automethod:: zprofileLimits

   """
    colbwidth = 0.06
    colbwpixels = 40
    zprofileheight = 0.1

    def __init__(self, fig, toolbarinfo=False, imageinfo=True, printload=False, helptext=True, callbackslist={}):
        keysM = [
         'cubechanged', 'movchanged', 'imagereset', 'speedchanged', 'moviepause']
        dictM = {'crosshair': self.drawCrosshair, 'zprofile': self.plotZprofile}
        keysC = ['progressbar', 'memory', 'finished']
        dictC = {}
        for k in keysM:
            if k in callbackslist:
                dictM[k] = callbackslist[k]

        for k in keysC:
            if k in callbackslist:
                dictC[k] = callbackslist[k]

        self.numcubes = 0
        self.movieimages = MovieContainer(fig, helptext=helptext, toolbarinfo=toolbarinfo, imageinfo=imageinfo, callbackslist=dictM)
        self.fig = fig
        self.timerlist = []
        self.movieimages.cidkey = None
        self.movieimages.cidscroll = None
        self.toolbarinfo = toolbarinfo
        self.imageinfo = imageinfo
        self.imageloadnr = 0
        self.movieframecounter = 0
        self.currentcube = 0
        self.cubelist = []
        self.maxframe = [None] * 4
        self.movieframeoffset = 0
        self.cubeindx = 0
        self.loadcb = None
        self.printload = printload
        self.splitmovieframe = 0
        self.panelmode = 0
        self.infoobj = None
        self.lastimage = None
        self.figadjust = False
        self.resizecb = CanvasCallback(self.reposition, fig.canvas, 'resize_event')
        NavigationToolbar2.ext_callback = self.reposition
        NavigationToolbar2.ext_callback2 = self.set_graticules
        Figure.ext_callback = self.reposition
        self.callbackslist = dictC
        if 'progressbar' in self.callbackslist:
            self.progressbar = self.callbackslist['progressbar']
        else:
            self.progressbar = None
        if 'memory' in self.callbackslist:
            self.memorystatus = self.callbackslist['memory']
        else:
            self.memorystatus = None
        self.numXpanels = 0
        self.numYpanels = 0
        self.previous_subpars = (
         fig.subplotpars.hspace, fig.subplotpars.wspace)
        self.crosshair = False
        self.zprofileOn = False
        self.zprofileframe = None
        self.zprofileXdata = None
        self.zprofileYdata = None
        return

    def callback(self, cbid, *arg):
        """
      Helper function for registered callbacks
      """
        if cbid in self.callbackslist:
            self.callbackslist[cbid](*arg)

    def plotZprofile(self, cube, x, y, cubenr=None, pos=None):
        """
      Purpose: This method plots a Z-profile for the current cube at the
               current position.

               The method can be called either with the current cube or
               with the (index) number of the current cube. For the
               cursor position in x and y, the image value is extracted
               from all the images in the cube. This way we build a so
               called Z-profile. The profile is updated
               if you move the mouse (event causes execution of method
               self.updatepanels). But it is also triggered with a callback
               in toggle_images if the cube changed.
               We use blitting to speed up the plotting of the profile.
      """
        if not self.zprofileOn:
            return
        else:
            if cube is None:
                if cubenr is None:
                    return
                cube = self.cubelist[cubenr]
            if pos is not None:
                im = cube.imagesinthiscube[0]
                world, pixels, units, errmes = str2pos(pos, im.projection, mixpix=im.mixpix, gridmode=im.gridmode)
                if errmes != '':
                    return errmes
                x = float(pixels[:, 0])
                y = float(pixels[:, 1])
            if x is None:
                x = cube.xold
            if y is None:
                y = cube.yold
            if None in [x, y]:
                return
            if self.zprofileframe.changed:
                framechanged = True
                self.zprofileframe.changed = False
            else:
                framechanged = False
            if cube.zmin is None:
                cube.zmin = cube.vmin
            if cube.zmax is None:
                cube.zmax = cube.vmax
            clipchanged = False
            if cube.zmin != self.zprofileframe.clipmin:
                clipchanged = True
            if cube.zmax != self.zprofileframe.clipmax:
                clipchanged = True
            yyy = []
            xi = numpy.round(x - (cube.pxlim[0] - 1))
            yi = numpy.round(y - (cube.pylim[0] - 1))
            if xi < 1 or xi > cube.pxlim[1] - cube.pxlim[0] + 1:
                return
            if yi < 1 or yi > cube.pylim[1] - cube.pylim[0] + 1:
                return
            yyy = [ aim.data[(yi - 1, xi - 1)] for aim in cube.imagesinthiscube ]
            start = cube.movieframeoffset
            xxx = numpy.arange(start, start + len(yyy))
            xxx1 = numpy.zeros(2 * len(xxx))
            yyy1 = numpy.zeros(2 * len(xxx))
            j = 0
            for i in range(len(xxx)):
                xxx1[j] = xxx[i] - 0.5
                xxx1[j + 1] = xxx[i] + 0.5
                yyy1[j] = yyy[i]
                yyy1[j + 1] = yyy[i]
                j += 2

            xxx = xxx1
            yyy = yyy1
            offset = cube.imagesinthiscube[0].pixoffset
            v = '%+3d %+3d' % (round(x - int(offset[0])), round(y - int(offset[1])))
            s = ('Z-profile at: x,y=').ljust(22) + v.rjust(10)
            self.zprofileframe.XYinfo.set_text(s)
            canvas = self.zprofileframe.figure.canvas
            if not self.zprofileYdata or self.zprofileframe.cubeindx != cube.cnr or framechanged or clipchanged:
                self.zprofileframe.XYinfo.set_text('')
                self.zprofileframe.set_xlim(xxx.min(), xxx.max())
                self.zprofileframe.set_ylim(cube.zmin, cube.zmax)
                if self.zprofileYdata:
                    self.zprofileYdata.set_xdata([])
                    self.zprofileYdata.set_ydata([])
                canvas.draw()
                self.zprofileframe.background = canvas.copy_from_bbox(self.zprofileframe.bbox)
                self.zprofileYdata, = self.zprofileframe.plot(xxx, yyy, 'g', animated=False)
                self.zprofileframe.cubeindx = cube.cnr
            else:
                canvas.restore_region(self.zprofileframe.background)
                self.zprofileYdata.set_ydata(yyy)
                self.zprofileframe.draw_artist(self.zprofileYdata)
                self.zprofileframe.draw_artist(self.zprofileframe.XYinfo)
                canvas.blit(self.zprofileframe.bbox)
            self.zprofileframe.clipmin = cube.zmin
            self.zprofileframe.clipmax = cube.zmax
            cube.ZprofileXold = x
            cube.ZprofileYold = y
            return

    def zprofileLimits(self, cubenr, zmin=None, zmax=None):
        """
      Set limits of plot with Z_profile for the current cube.

      :param cubenr:
         Index of the cube in Cubes.cubelist for which we want to adjust
         the range in image values in the z-profile
      :type cubenr:
         Integer
      :param zmin:
         Clip Y range (image values) in z-profile. ``zmin`` is the minimum value.
         If set to None, the minimum data value in the corresponding cube is
         used.
      :type zmin:
         Float
      :param zmax:
         Clip Y range (image values) in z-profile. ``zmax`` is the maximum value.
         If set to None, the maximum data value in the corresponding cube is
         used.
      :type zmax:
         Float

      :Notes:
         See example at :meth:`maputils.Cubes.set_zprofile`
      """
        cube = self.cubelist[cubenr]
        if not self.zprofileOn:
            return
        else:
            if zmin is None:
                zmin = cube.vmin
            if zmax is None:
                zmax = cube.vmax
            self.zprofileframe.set_ylim(zmin, zmax)
            self.zprofileframe.figure.canvas.draw()
            cube.zmin = zmin
            cube.zmax = zmax
            return

    def drawCrosshair(self, framenr, cubechanged=False, oldcubenr=-1):
        """
      Another image appeared on screen. If there are panels and you have
      a crosshair cursor, then they should be re-drawn. In the panels, the
      positions of the cursor line should change because another image in
      the cube is displayed.
      """
        if not self.crosshair:
            return
        else:
            currentimage = self.movieimages.annimagelist[framenr]
            cnr = currentimage.cubenr
            cube = self.cubelist[cnr]
            if cubechanged:
                oldcube = self.cubelist[oldcubenr]
                oldcube.linev.set_visible(False)
                oldcube.lineh.set_visible(False)
                oldcube.frame.draw_artist(oldcube.linev)
                oldcube.frame.draw_artist(oldcube.linev)
                if oldcube.panelXframes:
                    oldcube.panelxline.set_visible(False)
                    oldcube.framep1.draw_artist(oldcube.panelxline)
                if oldcube.panelYframes:
                    oldcube.panelyline.set_visible(False)
                    oldcube.framep2.draw_artist(oldcube.panelyline)
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
            cube.background = self.fig.canvas.copy_from_bbox(cube.frame.bbox)
            if not cube.panelXback and cube.panelXframes:
                cube.panelXback = self.fig.canvas.copy_from_bbox(cube.framep1.bbox)
            if not cube.panelYback and cube.panelYframes:
                cube.panelYback = self.fig.canvas.copy_from_bbox(cube.framep2.bbox)
            if cube.xold is None:
                cube.xold = (currentimage.box[1] + currentimage.box[0]) / 2.0
            if cube.yold is None:
                cube.yold = (currentimage.box[3] + currentimage.box[2]) / 2.0
            x = cube.xold
            y = cube.yold
            cube.linev.set_xdata((x, x))
            cube.lineh.set_ydata((y, y))
            cube.linev.set_visible(True)
            cube.lineh.set_visible(True)
            cube.frame.draw_artist(cube.linev)
            cube.frame.draw_artist(cube.lineh)
            self.fig.canvas.blit(cube.frame.bbox)
            currentindx = framenr
            offset = cube.movieframeoffset
            if cube.panelXframes:
                yp = currentindx - offset
                try:
                    i = cube.panelXframes.index(yp)
                    cube.framep1.draw_artist(cube.annimp1.image.im)
                    cube.panelxline.set_ydata((i, i))
                    cube.panelxline.set_visible(True)
                    cube.framep1.draw_artist(cube.panelxline)
                    self.fig.canvas.blit(cube.framep1.bbox)
                except:
                    pass

            if cube.panelYframes:
                xp = currentindx - offset
                try:
                    i = cube.panelYframes.index(xp)
                    cube.framep2.draw_artist(cube.annimp2.image.im)
                    cube.panelyline.set_xdata((i, i))
                    cube.panelyline.set_visible(True)
                    cube.framep2.draw_artist(cube.panelyline)
                    self.fig.canvas.blit(cube.framep2.bbox)
                except:
                    pass

            return

    def cleanupall(self):
        """
      Cleanup the contents of this object (destructor). We need a separate function
      to cleanup because our class contains circular references so it will not
      be touched by Python's garbage collector. Implementing a __del__ method
      also does not work because that decreases the reference counter with one,
      but it was bigger than 1 to begin with. See also:
      http://www.electricmonk.nl/log/2008/07/07/python-destructor-and-garbage-collection-notes/
      
      """
        cidkey = self.movieimages.cidkey
        if cidkey:
            self.canvas.mpl_disconnect(cidkey)
        cidscroll = self.movieimages.cidscroll
        if cidscroll:
            self.canvas.mpl_disconnect(cidscroll)

    def append(self, frame, fitsobj, axnums, slicepos=[], pxlim=None, pylim=None, vmin=None, vmax=None, hasgraticule=False, gridmode=False, hascolbar=True, pixelaspectratio=None, clipmode=0, clipmn=(4, 5), callbackslist={}):
        """
      Add a new cube to the container with cubes. Let's introduce some definitions first:

         1) A **data cube** is a FITS file with more than two data axes.
            Examples are a sequence of channel maps in a radio cube where
            the spatial maps are a function of the observing freequency.
         2) **Image axes** are the two axes of a map we want to display
            Usually these maps have two spatial axes (e.g. R.A. and Dec.),
            but this class can also handle images which are slices with
            axes of mixed types (e.g. R.A. and velocity, a so called position
            velocity diagram).
         3) **Repeat axes** are all the axes that do not belong to the
            set of image axes. Along these repeat axes, one can define
            a sequence of images, for example a set of R.A., Dec. images as function
            of velocity or Stokes parameter.

      :param frame:
          Each series of movie images that is appended needs its own frame.
          Frames can be defined with either Matplotlib's figure.add_subplot() or
          figure.add_axes(). Note that any frame is always resized to fit
          the canvas (with some room for a color bar and using the aspect
          ratio of the pixels in the current image).

          .. only:: latex

             To prevent that Matplotlib
             thinks that two frames are the same, you need to give each frame a unique
             label.  
    
          .. only:: html

             To prevent that Matplotlib
             thinks that two frames are the same, you need to give each frame a unique
             label::

               frame1 = fig.add_subplot(1,1,1, label='label1', frameon=False)
               cube = myCubes.append(frame1, ....)
               frame2 = fig.add_subplot(1,1,1, label='label2', frameon=False)
               cube = myCubes.append(frame2, ....)
             
      :type frame:
         Matplotlib Axes object.
      :param fitsobj:
         A FITSimage object as in: ``fitsobject = maputils.FITSimage('ngc6946.fits')``.
      :type fitsobj:
         Instance of :class:`maputils.FITSimage`
      :param axnums:
         A sequence (tuple or list) with axis numbers. The numbers start with 1.
         For an image you need to specify two axes. The numbers can be in any order.
         So, for instance, you can swap R.A. and Dec. axes, or you can make slices
         with one spatial and a spectral axis. For a cube with CTYPE's (RA,DEC,FREQ)
         you should enter then ``axnums=(1,3)`` or ``axnums=(3,2)`` etc.

         .. only:: html

            If we want RA, FREQ images for all DEC slices, we should write:: 
         
               fitsobject = maputils.FITSimage('ngc6946.fits')
               
               n1, n2, n3 = [fitsobject.axisinfo[i].axlen for i in (1,2,3)]
               print "Range axis 1:", 1, n1
               print "Range axis 2:", 1, n2
               print "Range axis 3:", 1, n3
         
               # Note that slice positions follow FITS standard, i.e. first pixel is 1
               slicepos = range(1, n2+1)  # all DEC slices
               cube = myCubes.append(frame1, fitsobject, axnums=(1,3), slicepos=slicepos)                                  
         
      :type axnums:
         Tuple or list with integers
      :param slicepos:
         A sequence with integers which set the slices that are stored as images. If we call 
         axes outside an image *repeat axes*, then the slice positions are pixel positions
         (following the FITS syntax, so they start with 1 and end with NAXISn (e.g. NAXIS3 from the 
         header). By default, the value of ``slicepos`` is None. This value is
         interpreted as follows:

         1) If a data structure is 2-dimensional, ``slicepos`` is not used
         2) If a data structure has n repeat axes, then for each repeat axis, the value
         
         of CRPIX of the corresponding axis is used, unless the this value is
         negative or greater than the axis length. In that case it is set to 1.
         Note that ``slicepos=None`` always defines only one image!.

         .. only:: latex

            Slice positions can be given in any order.
            (See example in HTML-version of this documentation)

         .. only:: html

            Slice positions can be given in any order::
         

               fitsobject = maputils.FITSimage('ngc6946.fits')
               naxis3 = fitsobject.hdr['NAXIS3']
               slicepos = range(naxis3, 0, -1)
               cube = myCubes.append(frame1, fitsobject, axnums=(1,2), slicepos=slicepos)
           
         Assume you have two repeat axes. One has CTYPE *VELO* and the other has CTYPE *STOKES*.
         Then we need to define a list ``slicepos`` with elements that are tuples with two integers.
         The first for the VELO axis and the second for the STOKES axis, e.g.:
         ``slicepos=[(1,1), (1,2), (1,3), ... ]``
         
         .. only:: latex

            (See example in HTML-version of this documentation)

         .. only:: html

            In the lines below, we load images from a set with axes (RA, DEC, VELO, STOKES).
            We want RA, DEC as image axes (``axnums=(1,2)``) and VELO and STOKES as the repeat axes.
         
            Assume we want a movie loop where we want to loop over all STOKES slices for each 
            slice on the VELO axis. 
            One can define the slice positions as follows::
         
               fitsobject3 = maputils.FITSimage('aurora.fits')
               n3 = fitsobject3.axisinfo[3].axlen
               n4 = fitsobject3.axisinfo[4].axlen

               a = range(1,n3+1)
               b = range(1,n4+1)
               A = [x for x in a for i in range(n4)]
               B = b*n3
               slicepos = zip(A, B)
 
               cube = myCubes.append(frame3, fitsobject3, axnums=(1,2), slicepos=slicepos)
         
            If we want to see all the VELO slices per STOKES slice, then use::

               A = a*n4
               B = [x for x in b for i in range(n3)]
               slicepos = zip(A, B)

      :type slicepos:
         None or a list, tuple or NumPy array with integers
      :param pxlim:
         Two values which set the range on the X axis. The numbers follow the FITS 
         standard, i.e. the first pixel is 1 and the last pixel is given by header item NAXISn.
      :type pxlim:
         Tuple with two integers
      :param pylim:
         Two values which set the range on the Y axis. The numbers follow the FITS 
         standard, i.e. the first pixel is 1 and the last pixel is given by header item NAXISn.

         .. only:: latex

            (See example in HTML-version of this documentation)

         .. only:: html

            Example::
         
               fitsobject = maputils.FITSimage('ngc6946.fits')
                                 
               n1, n2, n3 = [fitsobject.axisinfo[i].axlen for i in (1,2,3)]
               print "Range axis 1:", 1, n1
               print "Range axis 2:", 1, n2
               print "Range axis 3:", 1, n3
               pxlim = (5, n1-5)
               pylim = (5, n2-5)

               cube = myCubes.append(frame1, fitsobject, axnum(1,2), slicepos=range(1, n3+1),
                                     pxlim=pxlim, pylim=pylim)

         
         
      :type pylim:
         Tuple with two integers
      :param vmin:
         Colors are assigned to pixels in a range between vmin and vmax. The values are
         pixel values in units given by BUNIT in the header of the data set.
         By default, the value of *vmin* is set to None. After loading all images,
         the value of *vmin* will be set to the minumum value of all the loaded data.
         One can use *vmin* to enhance features in the data.
         Note that the distribution of colors can be so unbalanced that nothing can be seen
         in the data (e.g. with one pixel which has a much higher value than all the others).
         In this case, one can press key ``h`` to get histogram equalization.
      :type vmin:
         Floating point number
      :param vmax:
         Colors are assigned to pixels in a range between *vmin* and *vmax*.
         The values are
         pixel values in units given by BUNIT in the header of the data set.
         By default, the value of *vmax* is set to None. After loading all images,
         the value of *vmax* will be set to the minimum value of all the loaded data.
         One can use *vmax* to visually extract features in the data.
         Note that the distribution of colors can be so unbalanced that almost no details
         can be seen (e.g. for data with one pixel which has a much higher value
         than all the others).
         In this case, one can press key ``h`` to get histogram equalization.

         .. only:: latex

            (See example in HTML-version of this documentation)

         .. only:: html

            Example::
         
               fitsobject = maputils.FITSimage('ngc6946.fits')
            
               vmin, vmax = fitsobject.get_dataminmax()
               n3 = fitsobject.axisinfo[3].axlen 
               slicepos = range(1, n3+1)
               cube = myCubes.append(frame1, fitsobject, axnums=(1,2), slicepos=slicepos,
                                     vmin=1.1*vmin, vmax=0.9*vmax)

         
      :type vmax:
         Floating point number
      :param hasgraticule:
         If set to True, a system of grid lines will be plotted. The grid lines represent
         the world coordinate system. The system of grid lines is also called a *graticule*.
      :type hasgraticule:
         Boolean
      :param gridmode:
         If set to True, positions are no longer given in the pixel system of the FITS
         standard, but are given in *grids*. In a grid system we call the pixel that 
         corresponds to the projection center, pixel 0. In this system you don't need to
         know the header values of CRPIXn to find the projection center in a map.
      :type gridmode:
         Boolean
      :param hascolbar:
         If set to True (is set by default), a color bar is plotted at the left of the 
         images. The color bar has a fixed with and its height is always the same as the height of 
         the canvas. The color bar can also be plotted with a separate method.
      :type hascolbar:
         Boolean
      :param pixelaspectratio:
         Set the ratio between the height of a pixel and its width. For images with spatial axes, 
         the default should be fine. For other images, the aspect ratio is adjust so that
         a square image will be plotted. In this situation it is often convenient to be able 
         to change the size of a plot with the pixel aspect ratio.
      :type pixelaspectratio:
         Floating point
      :param clipmode:
         * ``clipmode=0`` (default):
           distribute all available image colors equally between *vmin* and *vmax*.
           If these values are not specified, then calculate *vmin* and *vmax*
           from the minimum and maximum
           data value (of all the loaded images in the current cube).
         * ``clipmode=1``: Calculate clip values from the minimum and maximum
           data value (of all the loaded images in the current cube) unless
           values are entered in *vmin* or *vmax* which overrule the calculated
           values.
         * ``clipmode=2``: First calculate the mean and standard deviation (std)
           of all the data (of all the loaded images in the current cube).
           Then calculate ``vmin=mean-clipmn[0]*std`` and ``vmax=mean+clipmn[1]*std``
           and use these values unless a preset value for either *vmin* or
           *vmax* was found. For *clipmn*, see next parameter.

           .. only:: latex

              (See example in HTML-version of this documentation)

           .. only:: html

              The next example illustrates this clip mode::
           
                  fig = figure(figsize=(10,10))
                  myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False,
                                                helptext=False, imageinfo=True)

                  # Create a maputils FITS object from a FITS file on disk
                  fitsobject = maputils.FITSimage('m101.fits')

                  frame1 = fig.add_subplot(1,1,1, label='label1', frameon=False)

                  cube = myCubes.append(frame1, fitsobject, axnums=(1,2), slicepos=None,
                                       clipmode=2, clipmn=(4,4), hascolbar=False)
                  show()
           
      :type clipmode:
         Integer
      :param clipmn:
         Set the scale factors for the standard deviation as described at the
         previous parameter *clipmode*.
         By default, the value is set to (4,5) 
      :type clipmn:
         Tuple with two floats
      :param callbackslist:
            To be able to interfere or interact with the cube viewer we need to
            know the status of processes in Maputils, like when is the color
            mapping in an image has been changed.
            The events handlers that we define with this method are specific
            to one cube.
            To handle these events, one must connect it to a function
            or an object with methods. With method :meth:``maputils.Cubes.append``
            we can handle the following events:
                                    
               *  'waitcursor' --
                  The process of loading images starts and one could change the
                  cursor to another shape to indicate the loading process
               *  'resetcursor'  --
                  The process of loading images has been finished and one could
                  change the cursor to its original shape               
               *  'exmes' -- This event is triggered when the string with information about
                  the cursor position is send to the canvas or to an external function.
               *  'cubeloaded' -- This event is triggerd after all images of the current cube
                  (for which you apply this append method) are loaded. It differs from 
                  the 'finished' event because that event is triggered after loading **all**
                  the cubes in a queue of cubes.
                           
            Some triggers are included to report changes in the color mapping of an image:

               *  'blankcol'  -- Must be handled by a function with one parameter. It returns the
                  index value of the new color that represents blank pixels in the image.
                  
                  .. only:: latex

                     The index can be used to retrieve the Matplotlib short
                     and long name of the color.
                     (Example in the HTML-version of this documentation)

                  .. only:: html

                     The index can be used to retrieve the Matplotlib short and long name of the color
                     as in::
                  
                        print maputils.Annotatedimage.blankcols[bcol]
                        print maputils.Annotatedimage.blanknames[bcol]
               
               *  'blurfac' -- User pressed *x* on the keyboard to change the smoothing factor
                  The callback function must have at least one parameter. The first
                  parameter stores the smoothing (blur) factor in pixels (floating point number).
               *  'blurred' -- User pressed *z* on the keyboard to toggle between smoothed and original image
                  The callback function must have at least one parameter. The first
                  parameter stores the current status (Boolean)
               *  'savelut' -- User pressed *m* on the keyboard to write the current color lookup table
                  to file on disk. The callback function must have at least one parameter. The first
                  parameter stores the file name (string).
               *  'histeq' -- A user pressed key *h* on the keyboard and requested a histogram
                  equalization (or a reset of a previous equalization). The trigger must be handled by a
                  function with one parameter and this parameter is returned as True or False.
               *  'inverse' -- A user changed the current color map to its inverse.
                  The trigger must be handled by a
                  function with one parameter and this parameter is returned as True or False.
               *  'lut' -- A user changed the color lookup table. These so called luts are stored
                  in :data:`maputils.cmlist`.
                  The trigger must be handled by a
                  function with one parameter and this parameter is returned as a index for the list with
                  color maps.
               *  'offset' -- A user changed the relation between pixel values and color mapping.
                  The trigger must be handled by a
                  function with one parameter and this parameter is returned as the current offset which
                  is a floating point value between -0.5 and 0.5
               *  'scale' -- A user changed the color map scaling 
                  1='linear', 2='log', 3='exp', 4='sqrt', 5='square'
                  Key '9' triggers the 'inverse' callback. Key '0' triggers all other callbacks in this
                  list.
                  The trigger must be handled by a
                  function with (at least) one parameter (i.e. the first) and this parameter is returned as a index for the list with
                  scales :attr:`maputils.Annotatedimage.lutscales`.
               *  'slope' -- A user changed the relation between pixel values and color mapping.
                  The trigger must be handled by a
                  function with one parameter and this parameter is returned as the current slope which
                  is a floating point value between 0 and 89 degrees
              
            
      :type callbackslist:
          A dictionary with functions that will be executed after the loading of the images
          has been completed (for the current cube)
          
      
      :Examples:
         1) Simple example with a 3D data FITS file. The cube has axes RA, DEC and VELO. 
         We show how to initialize a Cubes container and how to add objects of type
         :class:`maputils.FITSimage` to this container::

            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=True)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            axnums = (1,2)
            myCubes.append(frame, fitsobject, axnums, slicepos=slicepos)
            show()
 
         2) List with callbacks. In this example we demonstrate how triggers for callbacks
         can be used. The use of Lambda expressions is demonstrated for functions that need
         extra parameters.
         If you run this example you will soon discover how these callbacks work:
         
         .. code-block:: python
            :linenos:

            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def printSlope(slope, cubenr=0):
               # Right mouse button in horizontal direction
               print "Color mapping slope for cube %d = %f"%(cubenr, slope)

            def printOffset(offs):
               # Right mouse button in vertical direction
               print "Shift in color mapping:", offs

            def printLut(indx):
               # User pressed PgUp or PgDn key
               print "User changed lut to: ", maputils.Colmaplist.colormaps[indx]

            def printBlankcol(bcol):
               # User presswed key 'b'
               print "Blank color set to: ", bcol, maputils.Annotatedimage.blankcols[bcol],
                     maputils.Annotatedimage.blanknames[bcol]

            def printHistog(hist):
               # User pressed key 'h' to toggle between a histogram equalized version
               # and the original
               print "Histogram equalized?", hist

            def printScale(scale):
               # User pressed a number from the list [1,2,3,4,5] on the keyboard to set a scale
               print "Scale:", scale, maputils.Annotatedimage.lutscales[scale]

            def printInverse(inv):
               # User pressed key '9' on the keyboard to get an inverse color mapping
               print "Inverse color mapping?", inv
           
            def printBlurfac(blurfac):
               # User pressed 'x' on the keyboard to change the smoothing factor
               print "Smoothing factor:", blurfac

            def writeLut(filename):
               # User pressed 'm' on the keyboard to write the current color lookup table to file
               print "Write lut to file:", filename

            def printSmooth(smooth):
               # User pressed 'z' on the keyboard to toggle between smoothed and original image
               print "Image smoothed?", smooth

            def externalMes(pos):
               print "Position:", pos

            def externalMes2(pos):
               print "Position 2:", pos

            def waitCursor():
               print "Wait cursor on"

            def resetCursor():
               print "Wait cursor off"

            def postLoading(splitfr, slicepos):
               print "Set frame to compare with to:", splitfr
               myCubes.set_splitimagenr(splitfr)
               myCubes.set_panelframes(range(len(slicepos)), panel='XY')

            def printFinish():
               print "Loading finished and user interaction has been started"

            fig = figure()
            myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False,
                                     callbackslist={'finished':printFinish} )

            frame = fig.add_subplot(1,1,1, label='ngc6946')
            fitsobject = maputils.FITSimage('ngc6946.fits')
            splitfr = 30
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=slicepos,
               callbackslist={'slope'    : lambda slope, cubenr=0 : printSlope(slope, cubenr),
                              'offset'   : printOffset,
                              'lut'      : printLut,
                              'scale'    : printScale,
                              'inverse'  : printInverse,
                              'blankcol' : printBlankcol,
                              'blurfac'  : printBlurfac,
                              'blurred'  : printSmooth,
                              'savelut'  : writeLut,
                              'exmes'    : externalMes,
                              'waitcursor'  : waitCursor,
                              'resetcursor' : resetCursor,
                              'cubeloaded'  : lambda: postLoading(splitfr, slicepos)})

            frame = fig.add_subplot(1,1,1, label='m101')
            fitsobject2 = maputils.FITSimage('m101.fits')
            myCubes.append(frame, fitsobject2, axnums=(1,2),
               callbackslist={'slope'       : lambda slope, cubenr=1 : printSlope(slope, cubenr),
                              'histeq'      : printHistog,
                              'waitcursor'  : waitCursor,
                              'exmes'       : externalMes2
                              'resetcursor' : resetCursor})

            show()
          
      """
        C = Cubeatts(frame, fitsobj, axnums, slicepos, pxlim, pylim, vmin, vmax, hasgraticule, gridmode, hascolbar, pixelaspectratio, clipmode, clipmn, callbackslist)
        C.movieframeoffset = self.movieframeoffset
        C.cnr = self.cubeindx
        self.cubelist.append(C)
        self.numcubes += 1
        self.movieframeoffset += C.nummovieframes
        frame.axis('off')
        if self.cubelist[0].panelscb is not None:
            self.end_interactionMovieToPanels()
        self.cubeindx += 1
        timer = TimeCallback(self.loadimages, 1e-05, False, count=0, cube=C, zprofileOn=self.zprofileOn)
        self.timerlist.append(timer)
        if len(self.timerlist) == 1:
            self.timerlist[0].schedule()
        C.previous_bbox = None
        return C

    def cmapcallback(self):
        """
      Module mplutil has an update() method which is triggered after a color map
      change. A callback can be added. This callback is executed at the end of the
      update() method. The callback is added as an attribute as in:
      cube.cmap.callback = self.cmapcallback. We need the callback to register
      when a background has been changed and a crosshair cursor needs to be
      redrawn (background is blitted).
      """
        global backgroundchanged
        backgroundchanged = True

    def set_aspectratio(self, cube, aspectratio):
        """
      Change aspect ratio of frame of 'cube'. 

      :param cube:
         An entry from the list ``Cubes.cubelist``. For example: ``cube=myCubes.cubelist[0]``
      :type cube:
         An object from class :class:`maputils.Cubeatts`.
      :param aspectratio:
         Set aspect ratio of pixels for the images in the cube ``cube``.
      :type aspectratio:
         Floating point number
      
      :Examples:
         Load a cube with images and set the pixel aspect ratio::
         
            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():               
               cube = myCubes.cubelist[0]
               print "Original aspect ratio current cube: %f"%(cube.pixelaspectratio)
               myCubes.set_aspectratio(cube, 2.1)

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, helptext=False,
                                     printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=slicepos,
                           callbackslist={'cubeloaded':postloading})

            show()

      :notes:
         Note for programmers: We need a call to method :meth:`maputils.Cubes.reposition` to adjust
         the graticule frames
      """
        if aspectratio is None or aspectratio == 0.0:
            aspectratio = cube.fitsobj.get_pixelaspectratio()
        else:
            aspectratio = abs(aspectratio)
        cube.pixelaspectratio = abs(aspectratio)
        cube.frame.set_aspect(aspectratio)
        currentindx = cube.lastimagenr + cube.movieframeoffset
        if cube.hasgraticule:
            self.new_graticule(cube, visible=True)
            self.reposition(force=True)
        self.movieimages.setimage(currentindx, force_redraw=True)
        return

    def compose_movieframelist(self):
        """
      Each cube can have a series of images set as images for the movie loop.
      This method composes a list for all cubes.
      """
        newlist = []
        for C in self.cubelist:
            newlist += [ j + C.movieframeoffset for j in C.movieframelist ]

        self.movieimages.set_movieframes(newlist)

    def set_movieframes(self, framelist):
        """
      For INTERACTIVE use.
      Set the images that you want to include in a movieloop. The numbers are
      indices of the array with all the collected images in the moviecontainer.
      The index numbers are not related to a cube.
      """
        self.movieimages.set_movieframes(framelist)

    def set_panelframes(self, framelist, panel='X'):
        """
      Set a list with movie frame index numbers to show up in one of the
      side panels. The panels appear when the list is not empty.
      
      Imagine a 3D data structure. The axes of such a structure could be 
      RA, DEC and FREQ. When we appended images, we specified the axis numbers
      in *axnums*. Assume these numbers are (1,2) which corresponds to images 
      with axes RA and DEC. We can show a movie loop of the images as function 
      of positions in axis FREQ. A side panel is a new image that shares 
      either the RA or the DEC axis with the cube, but the other axis is a FREQ 
      axis. This way we extracted a slice from the cube. ``panel='X'`` gives
      a horizontal RA-FREQ slice and ``panel='Y'`` gives
      a vertical DEC-FREQ slice and the data is extracted at the position of 
      the cursor in the current image and when you move the mouse while pressing
      the left mouse button, you will see that the side panels are updated with
      new data extracted from the new mouse cursor position. It is also possible
      use the mouse in the side panels. If you move the mouse in the FREQ direction,
      you will see that the current image is replaced by the one that matches the
      new slice position in FREQ. If you move in a side panel in the RA or DEC direction,
      then you will see that the opposite side panel is updated because the
      position where the slice was extracted (DEC or RA) has been changed.
      This functionality has been used often for the inspection of radio data because
      it allows you to discover features in the data in a simple and straightforward way.
      
      
      
      :param framelist:
         List with numbers which represent the movie frames from which
         data is extracted to compose a side panel with slice data. Movie frame 
         numbers start with index 0 and range to the number of stored images.
         These images need not to be extracted from the same cube. Therefore 
         there is no clear correspondence between slice positions and movie frame
         numbers.
      :type framelist:
         Iterable sequence with integers
      :param panel:
         Default is to draw a panel along the horizontal image axis (X axis).
         The panel along the Y axis needs to be specified with ``panel='Y'``.
         Both panels are plotted with: ``panel='XY'``
      :type panel:
         One or two characters from the list 'X', 'Y', 'x', 'y'

      
      :Examples:
         Set both side panels to inspect orthogonal slices::

            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
               myCubes.set_panelframes(range(len(slicepos)), panel='XY')

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=slicepos,
                           callbackslist={'cubeloaded':postloading})

            show()
         
      """
        self.numXpanels = self.numYpanels = 0
        for C in self.cubelist:
            frlo = C.movieframeoffset
            frhi = C.movieframeoffset + C.nummovieframes
            panelframes = [ d - frlo for d in framelist if frlo <= d < frhi ]
            if 'X' in panel.upper():
                C.set_panelXframes(panelframes)
            if 'Y' in panel.upper():
                C.set_panelYframes(panelframes)
            if C.panelXframes:
                self.numXpanels += 1
            if C.panelYframes:
                self.numYpanels += 1

        for C in self.cubelist:
            if 'X' in panel.upper():
                self.create_panel('x', C)
            if 'Y' in panel.upper():
                self.create_panel('y', C)

    def create_panel(self, panid, cube):
        """
      Plot (or clean up) one of the panels or both. This method is invoked either
      at the start of the program after loading all images, or when there are 
      triggers for the side panels.
      """
        panx = pany = False
        if panid == 'x':
            panx = True
        else:
            if panid == 'y':
                pany = True
            elif panid == 'r':
                pany = True
                panx = True
            else:
                return
            cubeindx = cube.cnr
            xold = cube.xold
            yold = cube.yold
            frame = cube.frame
            fig = frame.figure
            framep1 = cube.framep1
            framep2 = cube.framep2
            cmap = cube.cmap
            mplimp1 = cube.annimp1
            mplimp2 = cube.annimp2
            slicepos = cube.slicepos
            fitsobject = cube.fitsobj
            pxlim = cube.pxlim
            pylim = cube.pylim
            vmin = cube.vmin
            vmax = cube.vmax
            offset = cube.movieframeoffset
            delta = 1e-06
            j = 0
            panelindx = j
            for C in self.cubelist:
                if C.cnr == cubeindx:
                    panelindx = j
                if C.panelXframes or C.panelYframes:
                    j += 1

        cube.frame = frame
        panbox = [
         0, 0, 0.01, 0.01]
        if panx or pany:
            if panx and framep1:
                if mplimp1:
                    mplimp1.disconnectCallbacks()
                    mplimp1.regcb.deschedule()
                framep1.clear()
                fig.delaxes(framep1)
                if mplimp1.grat:
                    fig.delaxes(mplimp1.grat.frame)
                    fig.delaxes(mplimp1.grat.frame2)
                framep1 = cube.framep1 = None
                mplimp1 = None
            if pany and framep2:
                if mplimp2:
                    mplimp2.disconnectCallbacks()
                    mplimp2.regcb.deschedule()
                framep2.clear()
                fig.delaxes(framep2)
                if mplimp2.grat:
                    fig.delaxes(mplimp2.grat.frame)
                    fig.delaxes(mplimp2.grat.frame2)
                framep2 = cube.framep2 = None
                mplimp2 = None
        xi = xold
        yi = yold
        if None in [xi, yi]:
            xi = pxlim[0]
            yi = pylim[0]
            cube.xold = xi
            cube.yold = yi
        makeXline = False
        if panx and cube.panelXframes:
            label = 'x_' + str(id(cube))
            framep1 = fig.add_axes(panbox, sharex=frame, label=label)
            framep1.set_aspect('auto')
            framep1.set_adjustable('box-forced')
            framep1.axis('off')
            M = cube.Mx
            ly = M.shape[0]
            j = 0
            for indx in cube.panelXframes:
                I = self.movieimages.annimagelist[(offset + indx)]
                if I.origdata is not None:
                    N = I.origdata
                else:
                    N = I.data
                M[ly - j - 1] = N[int(yi - pylim[0])]
                j += 1

            mixpix = pylim[0]
            fo = cube.fitsobj
            wcstypes = [fo.wcstypes[(cube.panelx_axperm[0] - 1)],
             fo.wcstypes[(cube.panelx_axperm[1] - 1)]]
            mplimp1 = Annotatedimage(framep1, header=fo.hdr, pxlim=pxlim, pylim=[ly - 1 - delta, 0], imdata=M, projection=cube.panelx_proj, axperm=cube.panelx_axperm, wcstypes=wcstypes, skyout=fo.skyout, spectrans=fo.spectrans, alter=fo.alter, mixpix=fo.mixpix, aspect='auto', slicepos=mixpix, sliceaxnames=fo.sliceaxnames, sourcename=fo.filename, cmap=cmap, adjustable='box-forced', clipmin=vmin, clipmax=vmax)
            posobj1 = Positionmessage(cube.panelx_proj.skysys, fo.skyout, cube.panelx_proj.types)
            mplimp1.regcb = AxesCallback(self.eventfrompanel1, framep1, 'motion_notify_event', cubenr=cubeindx, posobj=posobj1)
            mplimp1.AxesCallback_ids.append(mplimp1.regcb)
            mplimp1.Image(animated=False)
            mplimp1.plot()
            im = cube.imagesinthiscube[0]
            if im.contours_on:
                cmap, colors, norm, levels = (
                 im.contours_cmap, im.contours_colour, im.norm, im.clevels)
                if cmap is None and colors is None:
                    colors = 'r'
                if cmap is not None:
                    cmap = cm.get_cmap(cmap)
                    colors = None
                mplimp1.contourSet = framep1.contour(mplimp1.image.im.get_array(), levels=levels, extent=mplimp1.box, cmap=cmap, norm=norm, colors=colors)
            cube.annimp1 = mplimp1
            cube.framep1 = framep1
            if cube.panelxline:
                del cube.panelxline
            lineprops = {'animated': False, 'linewidth': 1}
            cube.panelxline = framep1.axhline(xmin=MINBOUND, xmax=MAXBOUND, visible=False, **lineprops)
        makeYline = False
        if pany and cube.panelYframes:
            label = 'y_' + str(id(cube))
            framep2 = fig.add_axes(panbox, sharey=frame, label=label)
            framep2.set_aspect('auto')
            framep2.set_adjustable('box-forced')
            framep2.axis('off')
            M = cube.My
            lx = M.shape[1]
            j = 0
            for indx in cube.panelYframes:
                I = self.movieimages.annimagelist[(offset + indx)]
                if I.origdata is not None:
                    N = I.origdata
                else:
                    N = I.data
                M[:, j] = N[:, int(xi - pxlim[0])]
                j += 1

            fo = cube.fitsobj
            mixpix = pxlim[0]
            wcstypes = [fo.wcstypes[(cube.panely_axperm[0] - 1)],
             fo.wcstypes[(cube.panely_axperm[1] - 1)]]
            mplimp2 = Annotatedimage(framep2, header=fo.hdr, pxlim=[
             0, lx - 1 - delta], pylim=pylim, imdata=M, projection=cube.panely_proj, axperm=cube.panely_axperm, wcstypes=wcstypes, skyout=fo.skyout, spectrans=fo.spectrans, alter=fo.alter, mixpix=mixpix, aspect='auto', slicepos=fo.slicepos, sliceaxnames=fo.sliceaxnames, sourcename=fo.filename, cmap=cmap, adjustable='box-forced', clipmin=vmin, clipmax=vmax)
            posobj2 = Positionmessage(cube.panely_proj.skysys, fo.skyout, cube.panely_proj.types)
            mplimp2.regcb = AxesCallback(self.eventfrompanel2, framep2, 'motion_notify_event', cubenr=cubeindx, posobj=posobj2)
            mplimp2.AxesCallback_ids.append(mplimp2.regcb)
            mplimp2.Image(animated=False)
            mplimp2.plot()
            im = cube.imagesinthiscube[0]
            if im.contours_on:
                cmap, colors, norm, levels = (
                 im.contours_cmap, im.contours_colour, im.norm, im.clevels)
                if cmap is None and colors is None:
                    colors = 'r'
                if cmap is not None:
                    cmap = cm.get_cmap(cmap)
                    colors = None
                mplimp2.contourSet = framep2.contour(mplimp2.image.im.get_array(), levels=levels, extent=mplimp2.box, cmap=cmap, norm=norm, colors=colors)
            cube.annimp2 = mplimp2
            mplimp2.grat = None
            cube.framep2 = framep2
            if cube.panelyline:
                del cube.panelyline
            lineprops = {'animated': False, 'linewidth': 1}
            cube.panelyline = framep2.axvline(ymin=MINBOUND, ymax=MAXBOUND, visible=False, **lineprops)
        self.reposition(force=True)
        return

    def updatemovieframe(self, cb, frompanel1=False, frompanel2=False):
        """
      This method changes an image in the movie container. It is called
      after a mouse move in one of the slice panels. That's why either
      'frompanel1' or 'frompanel2' must be true.
      But this mouse move can also imply a move in a (e.g. spatial) direction
      in a panel comparable to a move in the main window.
      This updates the other panel(s).
      """
        cbx = cb.xdata
        cby = cb.ydata
        cubenr = cb.cubenr
        currentcube = self.cubelist[cubenr]
        if frompanel1:
            yi = int(numpy.round(cb.ydata))
            framenr = currentcube.panelXframes[yi] + currentcube.movieframeoffset
            if framenr >= 0 and framenr < self.movieimages.numimages and framenr != self.movieimages.indx:
                self.movieimages.setimage(framenr)
            self.updatepanels(None, frompanel1, frompanel2, cubenr=cubenr, xpos=cb.xdata, ypos=cb.ydata)
        if frompanel2:
            xi = int(numpy.round(cb.xdata))
            framenr = currentcube.panelYframes[xi] + currentcube.movieframeoffset
            if framenr >= 0 and framenr < self.movieimages.numimages and framenr != self.movieimages.indx:
                self.movieimages.setimage(framenr)
            self.updatepanels(None, frompanel1, frompanel2, cubenr=cubenr, xpos=cb.xdata, ypos=cb.ydata)
        if frompanel1 or frompanel2:
            xd, yd = currentcube.frame.transData.transform((cbx, cby))
            for i in range(0, self.numcubes):
                if i != cubenr:
                    xpos, ypos = self.cubelist[i].frame.transData.inverted().transform((xd, yd))
                    cb.cubenr = i
                    self.updatepanels(None, frompanel1, frompanel2, cubenr=i, xpos=xpos, ypos=ypos)

            cb.cubenr = cubenr
        return

    def eventfrompanel1(self, cb):
        yi = int(numpy.round(cb.ydata))
        cubenr = cb.cubenr
        currentcube = self.cubelist[cubenr]
        if yi < 0 or yi >= len(currentcube.panelXframes):
            return
        framenr = currentcube.panelXframes[yi] + currentcube.movieframeoffset
        currentim = self.movieimages.annimagelist[framenr]
        oim = self.movieimages.annimagelist[self.movieimages.indx]
        oim.X_lastvisited = oim.Y_lastvisited = None
        if self.toolbarinfo:
            yinfo = currentim.slicemessage
            ypos = currentcube.pylim[0]
            xw, yw, missingspatial = currentim.toworld(cb.xdata, ypos, matchspatial=True)
            sl = cb.posobj.wcs2str(xw, yw, missingspatial, returnlist=True)
            s = sl[0] + ' ' + yinfo
            currentim.messenger(s)
        if cb.event.button == 1:
            self.updatemovieframe(cb, frompanel1=True)
        return

    def eventfrompanel2(self, cb):
        xi = int(numpy.round(cb.xdata))
        cubenr = cb.cubenr
        currentcube = self.cubelist[cubenr]
        if xi < 0 or xi >= len(currentcube.panelYframes):
            return
        framenr = currentcube.panelYframes[xi] + currentcube.movieframeoffset
        currentim = self.movieimages.annimagelist[framenr]
        oim = self.movieimages.annimagelist[self.movieimages.indx]
        oim.X_lastvisited = oim.Y_lastvisited = None
        if self.toolbarinfo:
            xinfo = currentim.slicemessage
            xpos = currentcube.pxlim[0]
            xw, yw, missingspatial = currentim.toworld(xpos, cb.ydata, matchspatial=True)
            sl = cb.posobj.wcs2str(xw, yw, missingspatial, returnlist=True)
            s = sl[1] + ' ' + xinfo
            currentim.messenger(s)
        if cb.event.button == 1:
            self.updatemovieframe(cb, frompanel2=True)
        return

    def getpanelboxes(self, frame, numXpanels, numYpanels, numXframesList, numYframesList, Xpanelindx=None, Ypanelindx=None):
        """
      This method calculates the positions of the side panels. It locates these
      panels to the bottom and right of an existing frame. The images are anchored
      to the top left corner and are made smaller if there are side panels.
      The space that is available to the panels is divided in a way that pixels from
      different panels are equal in size. So the ratios of frames between panels
      sets the width or height.The width of the gaps between panels
      is fixed in pixels.

      Note that numXframesList/numYframesList set the number of pixels in a panel
      for each panel. We need this list because for each panel we need the positions
      of the previous panels.
      """
        fig = frame.figure
        xf0, yf0 = fig.transFigure.inverted().transform((0, 0))
        xf1, yf1 = fig.transFigure.inverted().transform((4, 4))
        dx = xf1 - xf0
        dy = yf1 - yf0
        frame.apply_aspect()
        bbox = frame.get_position()
        xlo, ylo, xhi, yhi = (bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax)
        xmin, ymin, xmax, ymax = self.getbiggestbox()
        boxX = boxY = None
        if Xpanelindx is not None and numXframesList is not None:
            totalXframes = 0
            for nf in numXframesList:
                totalXframes += nf

            if not totalXframes:
                return (boxX, boxY)
            dys = (len(numXframesList) + 1) * dy
            H = ymin - dys
            bymin = []
            bymax = []
            for i, nf in enumerate(numXframesList):
                if i == 0:
                    y = ymin - dy
                else:
                    y = bymin[(i - 1)] - dy
                bymax.append(y)
                h = H * float(nf) / totalXframes
                if h <= 0.0:
                    h = 0.1
                bymin.append(y - h)

            bxmin = xlo
            bxmax = xhi
            w = bxmax - bxmin
            h = bymax[Xpanelindx] - bymin[Xpanelindx]
            boxX = (bxmin, bymin[Xpanelindx], w, h)
        if Ypanelindx is not None and numYframesList is not None:
            totalYframes = 0
            for nf in numYframesList:
                totalYframes += nf

            if not totalYframes:
                return (boxX, boxY)
            dxs = (len(numYframesList) + 1) * dx
            W = 1.0 - xmax - dxs
            bxmin = []
            bxmax = []
            for i, nf in enumerate(numYframesList):
                if i == 0:
                    x = xmax + dx
                else:
                    x = bxmax[(i - 1)] + dx
                bxmin.append(x)
                w = W * float(nf) / totalYframes
                if w <= 0.0:
                    w = 0.1
                bxmax.append(x + w)

            bymin = ylo
            bymax = yhi
            h = bymax - bymin
            w = bxmax[Ypanelindx] - bxmin[Ypanelindx]
            boxY = (bxmin[Ypanelindx], bymin, w, h)
        return (
         boxX, boxY)

    def set_crosshair(self, status):
        """
      This method prepares a crosshair cursor, which can be moved with the mouse
      while pressing the left mouse button.

      Usually we want a crosshair cursor, to find the location of features. The
      crosshair cursor extends also to the side panels where the indicate
      at which slice we are looking.

      Note that the situation
      with blitted images and multiple frames (Axes objects) prevents the use
      of class:`matplolib.widgets.Cursor` so an alternative is implemented.

      :param status:
         If set to `True`, a crosshair cursor will be plotted. If `False`, an
         existing crosshair will be removed.
      :type status:
         Boolean

      :Examples:
         Draw a crosshair on the canvas which can be moved with the mouse
         while pressing the left mouse button. Extend the cursor in two side panels::
         
            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
               myCubes.set_panelframes(range(len(slicepos)), panel='XY')
               myCubes.set_crosshair(True)

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=slicepos,
                           callbackslist={'cubeloaded':postloading})

            show()

      """
        self.crosshair = status
        currentindx = self.movieimages.indx
        if self.crosshair:
            self.movieimages.setimage(currentindx, force_redraw=True)
        else:
            currentimage = self.movieimages.annimagelist[currentindx]
            cnr = currentimage.cubenr
            cube = self.cubelist[cnr]
            cube.linev.set_visible(False)
            cube.lineh.set_visible(False)
            if cube.panelXframes:
                cube.panelxline.set_visible(False)
                cube.framep1.draw_artist(cube.panelxline)
            if cube.panelYframes:
                cube.panelyline.set_visible(False)
                cube.framep2.draw_artist(cube.panelyline)
            self.fig.canvas.draw()

    def set_zprofile(self, status):
        """
      This method plots (or removes) a so called z-profile as a (non-filled)
      histogram as function of cursor position in an image.

      The data is extracted from a data set, with at least three axes,
      at the cursor position in the current
      image and this is repeated for all the images in all the cubes that
      were entered. This is also repeated for all the repeat axex that
      you specified for a given cube.
      So the X axis of the z-profile is the movie frame number and not a
      slice number.
      The z-profile is shown per cube. If you change to an image that
      belongs to another cube, the z-profile will change accordingly, but
      the X axis still represents the movie frame number.

      You can update the z-profile by moving the mouse while pressing the left
      mouse button.
      Change the limits in the Y direction (image values) with
      method :meth:`maputils.Cubes.zprofileLimits()`.

      :param status:
         Plot z-profile if ``status=True``. If there is already a z-profile
         plotted, then remove it with ``status=False``
      :type status:
         Boolean

      :Examples:
         Load a cube and plot its z-profile. Set the range of image values
         for the z-profile::

            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
               myCubes.set_zprofile(True)
               myCubes.zprofileLimits(0, 0.0, 0.1)

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)
            myCubes.zprofileheight = 0.3  # Change the height of the z-profile in normalized device coordinates

            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=slicepos,
                           callbackslist={'cubeloaded':postloading})

            show()
         
      """
        self.zprofileOn = status
        if self.zprofileOn:
            left = 0
            width = 1.0
            bottom = 1.0 - self.zprofileheight
            height = self.zprofileheight
            self.zprofileframe = self.fig.add_axes([left, bottom, width, height], label='zprofile', autoscale_on=False, axisbg='#D2D2D2')
            bbox = dict(edgecolor='w', facecolor='w', alpha=0.4, boxstyle='square,pad=0.1')
            ml = MultipleLocator(5)
            self.zprofileframe.xaxis.set_minor_locator(ml)
            for tick in self.zprofileframe.xaxis.get_major_ticks():
                tick.set_pad(-10.0)
                tick.tick1line.set_color('r')

            for tick in self.zprofileframe.yaxis.get_major_ticks():
                tick.set_pad(-10.0)
                tick.tick1line.set_color('r')
                tick.label1.set_horizontalalignment('left')

            for t in self.zprofileframe.get_xticklabels():
                t.set_fontsize(8)

            for t in self.zprofileframe.get_yticklabels():
                t.set_fontsize(8)

            self.zprofileframe.grid(True)
            self.zprofileframe.clipmin = None
            self.zprofileframe.clipmax = None
            self.zprofileframe.cubeindx = -1
            self.zprofileframe.changed = False
            info = self.zprofileframe.text(0.99, 0.8, 'Z-profile at: x,y=', horizontalalignment='right', verticalalignment='top', transform=self.zprofileframe.transAxes, fontsize=8, color='w', animated=False, family='monospace', bbox=dict(facecolor='red', alpha=0.5))
            self.zprofileframe.XYinfo = info
        else:
            fr = self.zprofileframe
            if fr:
                fr.clear()
                self.fig.delaxes(fr)
                del fr
            self.zprofileframe = None
            self.zprofileXdata = None
            self.zprofileYdata = None
        self.reposition(force=True)
        return

    def set_colbar_on(self, cube, mode):
        """
      This method draws or removes a colorbar. Each cube is associated with a
      color bar.

      A color bar will always be plotted to the left side of your plot and it
      have the same height as the canvas.
      The color bar will change its colours if you move the mouse while pressing
      the right mouse button. It will also change if you use color navigation
      with keyboard keys:

      * pgUp and pgDown: browse through colour maps
      * Right mouse button: Change slope and offset
      * Colour scales: 
         * 0=reset 
         * 1=linear 
         * 2=logarithmic
         * 3=exponential 
         * 4=square-root 
         * 5=square 
         * 9=inverse

      * h: Toggle histogram equalization & raw image 

      :param cube:
         An entry from the list ``Cubes.cubelist``. For example: ``cube=myCubes.cubelist[0]``
      :type cube:
         An object from class :class:`maputils.Cubeatts`.
      :param mode:
         If set to ``True``, a color bar will be plotted. If set to ``False``, an
         existing color bar will be removed.
      :type mode:
         Boolean

      :Examples:
         Plot a color bar::

            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
               myCubes.colbwpixels = 100    # Change width of color bar in pixels
               cube = myCubes.cubelist[0]
               myCubes.set_colbar_on(cube, mode=True)

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,2),
                           slicepos=slicepos, hascolbar=False,
                           callbackslist={'cubeloaded':postloading})

            show()

      """
        if not cube or not len(cube.imagesinthiscube):
            return
        cube.hascolbar = mode
        currentindx = cube.lastimagenr + cube.movieframeoffset
        for im in cube.imagesinthiscube:
            im.hascolbar = cube.hascolbar

        self.movieimages.setimage(currentindx, force_redraw=True)
        self.reposition()

    def get_colbar_position(self):
        """
      Purpose: Get position of the colorbar. This position can change if a line
               graph is added. It will be adjusted then in method reposition()
      """
        left = bottom = 0.0
        width = self.colbwidth
        if self.zprofileOn:
            height = 1.0 - self.zprofileheight
        else:
            height = 1.0
        return (
         left, bottom, width, height)

    def new_colorbar(self, cube):
        """
      Purpose: This method creates a frame for a new colorbar.
      """
        label = 'CB_' + str(id(cube))
        left = bottom = 0.0
        width = self.colbwidth
        if self.zprofileOn:
            height = 1.0 - self.zprofileheight
        else:
            height = 1.0
        cube.cbframe = self.fig.add_axes(self.get_colbar_position(), label=label, frameon=False, autoscale_on=False)
        dummyim = cube.imagesinthiscube[0]
        cube.colorbar = dummyim.Colorbar(frame=cube.cbframe, orientation='vertical')
        if 'BUNIT' in cube.fitsobj.hdr:
            dataunits = cube.fitsobj.hdr['BUNIT']
        else:
            dataunits = 'units unknown'
        cube.colorbar.plot(cube.cbframe, dummyim.image.im)
        bbox = dict(edgecolor='w', facecolor='w', alpha=0.4, boxstyle='square,pad=0.1')
        for tick in cube.cbframe.yaxis.get_major_ticks():
            tick.set_pad(-5.0)
            tick.tick2line.set_color('w')
            tick.tick2line.set_markeredgewidth(2)
            tick.label2.set_horizontalalignment('right')
            tick.label2.set_bbox(bbox)

        for t in cube.cbframe.get_yticklabels():
            t.set_fontsize(8)
            t.set_rotation(90)

        cube.cbframe.text(0.2, 0.98, dataunits, fontsize=7, fontweight='bold', color='w', rotation=90, horizontalalignment='left', verticalalignment='top', bbox=dict(color='w', facecolor='red', alpha=0.5))
        for im in cube.imagesinthiscube:
            im.cbframe = cube.cbframe
            im.hascolbar = cube.hascolbar

    def set_skyout(self, cube, skyout):
        """
      This method changes the celestial system. It redraws the graticule so that 
      its labels represent the new celestial system.
            
      :param cube:
         An entry from the list ``Cubes.cubelist``. For example: ``cube=myCubes.cubelist[0]``
      :type cube:
         An object from class :class:`maputils.Cubeatts`.
      :param skyout:
         See :ref:`celestial-skysystems`
      :type skyout:
         String or tuple
      
      
      :Examples:
         Change the sky system from the native system to Galactic and draw a graticule
         showing the world coordinate system::
      
            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
               cube = myCubes.cubelist[0]
               myCubes.set_skyout(cube, "galactic")
               myCubes.set_graticule_on(cube, True)

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, helptext=False,
                                     printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=slicepos,
                           callbackslist={'cubeloaded':postloading})

            show()

      """
        if not cube or not len(cube.imagesinthiscube):
            return
        for im in cube.imagesinthiscube:
            im.skyout = im.projection.skyout = skyout

        if cube.hasgraticule:
            self.new_graticule(cube, visible=True)
        currentindx = cube.lastimagenr + cube.movieframeoffset
        self.movieimages.setimage(currentindx, force_redraw=True)

    def set_spectrans(self, cube, spectrans):
        """
      This method changes the spectral system. If a valid system is defined,
      you will notice that spectral coordinates are printed in the new
      system. If a graticule has a spectral axis, you will see that the labels
      will change so that they represent the new spectral system.

      :param cube:
         An entry from the list ``Cubes.cubelist``. For example: ``cube=myCubes.cubelist[0]``
      :type cube:
         An object from class :class:`maputils.Cubeatts`.
      :param spectrans:
         See :ref:`Alternate headers for a spectral line example <spectralbackground-alt>`
      :type spectrans:
         String

      :Examples:
         Change the sky system from the native spectral system to wavelengths (in m)
         and draw a graticule showing the world coordinate system. Note that we
         loaded images with one spatial and one spectral axis (the cube has a RA, DEC
         and VELO axis) with axnums=(1,3). To get a list with valid spectral
         translations, we printed ``fitsobject.allowedtrans``::
         
            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
               cube = myCubes.cubelist[0]
               myCubes.set_spectrans(cube, "WAVE")
               myCubes.set_graticule_on(cube, True)

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, helptext=False,
                                     printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            print "Possible spectral translations:", fitsobject.allowedtrans
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,3), slicepos=slicepos,
                           callbackslist={'cubeloaded':postloading})

            show()

      """
        if not cube or not len(cube.imagesinthiscube):
            return
        im0 = cube.imagesinthiscube[0]
        if im0.projection.specaxnum:
            if not hasattr(cube, 'nativeproj'):
                cube.nativeproj = im0.projection
            for im in cube.imagesinthiscube:
                if spectrans:
                    im.projection = im.projection.spectra(spectrans)
                    im.spectrans = spectrans
                else:
                    im.projection = cube.nativeproj

            if cube.hasgraticule:
                self.new_graticule(cube, visible=True)
        else:
            cube.set_slicemessages(spectrans)
        currentindx = cube.lastimagenr + cube.movieframeoffset
        self.movieimages.setimage(currentindx, force_redraw=True)

    def set_graticule_on(self, cube, mode):
        """
      This method creates the WCS overlay and refreshes the current image or
      the relevant image if the current image does not belong to the cube
      for which a graticule is requested. The method can be used if the 
      *hasgraticule* parameter in :meth:`maputils.Cubes.append` has not been set.
      
      :param cube:
         An object from the list Cubes.cubelist. For example: ``cube = myCubes.cubelist[0]``
      :type cube:
         An object from class :class:`Cubeatts`.
      :param mode:
         If set to True, a graticule will be plotted. If set to False, an existing
         graticule will be removed.
      :type mode:
         Boolean
      
      :Examples:
         Define a callback which is triggered after loading all the images in 
         a data cube. The callback function extracts the first (and only)
         cube of a list of cubes and plots the graticules::
                  
            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
              cube = myCubes.cubelist[0]
              myCubes.set_graticule_on(cube, True)

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            slicepos = range(1,101)
            axnums = (1,2)
            myCubes.append(frame, fitsobject, axnums=(1,2), slicepos=range(1,101),
                          callbackslist={'cubeloaded':postloading})

            show()
        
        
      """
        if not cube or not len(cube.imagesinthiscube):
            return
        cube.hasgraticule = mode
        currentindx = cube.lastimagenr + cube.movieframeoffset
        if not mode:
            if cube.grat:
                for li in cube.linepieces:
                    li.set_visible(False)

                for tl in cube.textlabels:
                    tl.set_visible(False)

                cube.grat.frame.lines = []
                cube.grat.frame2.lines = []
                cube.grat.frame.texts = []
                cube.grat.frame2.texts = []
                cube.linepieces = []
                cube.textlabels = []
                for im in cube.imagesinthiscube:
                    im.grat = cube.grat
                    im.linepieces = cube.linepieces
                    im.textlabels = cube.textlabels

        else:
            self.new_graticule(cube, visible=True)
        self.movieimages.setimage(currentindx, force_redraw=True)

    def set_graticules(self):
        """
      This method should be called after zoom/pan actions where we want to
      update the graticule on an image. Then one should update this for
      all cubes because a zoom is a zoom in all images in the movie
      container because each frame is zoomed to the same area on display.
      This is a feature of Matplotlib.
      """
        if not len(self.movieimages.annimagelist):
            return
        currentindx = self.movieimages.indx
        currentimage = self.movieimages.annimagelist[currentindx]
        cnr = currentimage.cubenr
        cube = self.cubelist[cnr]
        for cnr, cube in enumerate(self.cubelist):
            if cnr == currentimage.cubenr:
                visible = True
            else:
                visible = False
            self.new_graticule(cube, visible)

    def new_graticule(self, cube, visible):
        """
      Note:
      For images with one spatial axis and one axis that is not spatial
      (for instance spectral or Stokes axis), the spatial
      axis is labeled with offsets. These offsets are a function of the missing
      spatial axis. This implies that in fact, each image in a movie of the same
      cube, could have a different labeling. We chose the alternative, which is
      that for each image the offsets are calculated at the same position on
      the missing axis. This position is the associated value of CRPIX.
      """
        if not cube.hasgraticule:
            return
        else:
            if not len(cube.imagesinthiscube):
                return
            currentimage = cube.imagesinthiscube[0]
            if cube.grat:
                cube.grat.frame.lines = []
                cube.grat.frame2.lines = []
                cube.grat.frame.texts = []
                cube.grat.frame2.texts = []
                cube.frame.texts = []
                frame1 = cube.grat.frame
                frame2 = cube.grat.frame2
            else:
                frame1 = frame2 = None
            pxlim = cube.frame.get_xlim()
            pxlim = (pxlim[0] + 0.5, pxlim[1] - 0.5)
            pylim = cube.frame.get_ylim()
            pylim = (pylim[0] + 0.5, pylim[1] - 0.5)
            cube.grat = currentimage.Graticule(pxlim=pxlim, pylim=pylim)
            cube.grat.setp_ticklabel(wcsaxis=1, rotation=90)
            cube.grat.setp_tick(wcsaxis=(0, 1), visible=False)
            cube.grat.set_tickmode(plotaxis=('left', 'bottom'), mode='NO_TICKS')
            cube.grat.setp_axislabel(plotaxis='left', visible=False)
            cube.grat.setp_axislabel(plotaxis='bottom', visible=False)
            cube.grat.setp_gratline(wcsaxis=(0, 1), lw=0.5, color='k')
            bbox = dict(edgecolor='w', facecolor='w', alpha=0.4, boxstyle='square,pad=0.')
            cube.insideX = cube.grat.Insidelabels(wcsaxis=0, aspect=cube.frame.get_aspect(), fontsize=10, ha='right', va='bottom', rotation_mode='anchor', bbox=bbox)
            bbox = dict(edgecolor='w', facecolor='w', alpha=0.4, boxstyle='square,pad=0.')
            cube.insideY = cube.grat.Insidelabels(wcsaxis=1, aspect=cube.frame.get_aspect(), fontsize=10, ha='right', va='bottom', rotation_mode='anchor', bbox=bbox)
            cube.grat.plot(cube.frame, frame1, frame2)
            cube.linepieces = set(l for l in cube.grat.frame.findobj(Line2D) if l.get_visible())
            cube.textlabels = set(t for t in cube.grat.frame2.findobj(Text) if t.get_text() != '' and t.get_visible())
            if not visible:
                for l in cube.linepieces:
                    l.set_visible(False)

                for t in cube.textlabels:
                    t.set_visible(False)

            for im in cube.imagesinthiscube:
                im.grat = cube.grat
                im.linepieces = cube.linepieces
                im.textlabels = cube.textlabels

            return

    def set_coordinate_mode(self, grids=True, world=False, worlduf=False, imval=False, pixfmt='%.1f', dmsprec=1, wcsfmt='%.7f', zfmt='%.3e', appendcr=False, tocli=False, tolog=True, resetim=True):
        """
      Set modes for the formatting of coordinate information.
      The output is generated by :meth:`Annotatedimage.interact_writepos`.
      Coordinates are written to the terminal (by default)
      if the left mouse button is pressed
      simultaneously with the Shift button. The position corresponds to
      the position of the mouse cursor. For maps with one spatial axis, the
      coordinate of the matching spatial axis is also written.
      
      There are several options to format the output. World coordinates follow
      the syntax of the system set by :meth:`maputils.Cubes.set_skyout` and :meth:`maputils.Cubes.set_spectrans`.

      Note that the settings in this method, only applies to the coordinates that are
      written to terminal (or log file). The labels on the graticule are not changed.

      :param grids:
         Write cursor position in pixels or grids if ``gridmode=True`` in 
         :meth:`maputils.Cubes.append`.
         (the name ``grids`` is a bit misleading). 
      :type grids:
         Boolean
      :param world:
         Write cursor position in world coordinates for the current
         celestial and spectral system
      :type grids:
         Boolean
      :param worlduf:
         Write cursor position in unformatted world coordinates for the current
         celestial and spectral system. This implies that equatorial coordinates
         are written in degrees, not in hms/dms format.
      :type grids:
         Boolean
      :param imval:
         Write the image value at the cursor position in units of the (FITS)
         header.         
      :type imval:
         Boolean
      :param pixfmt:
         Set the precision of the pixels/grids with a Python number format string.
         (default: pixfmt="%.1f")
      :type pixfmt:
         Number format string
      :param dmsprec:
         Number of digits after comma for seconds in latitude. If the longitude
         is equatorial, one extra digit is used.
      :type dmsprec:
         Integer
      :param wcsfmt:
         Set the precision of the un-formatted world coordinates with a Python
         number format string. (Default: wcsfmt="%.7f")
      :type wcsfmt:
         Number format string
      :param zfmt:
         Set the precision of the image values with a Python number format string
         (default: zfmt='%.3e')
      :type zfmt:
         Number format string
      :param appendcr:
         After composing the string with coordinate transformation, add a carriage return
         character. This can be useful when the output is written to a prompt
         which expects a carriage return to process the input.
      :type appendcr:
         Boolean
      :param tocli:
         Only available in the context of GIPSY. This selects the input area of
         Hermes. Often used together with ``appendcr``.
      :type tocli:
         Boolean         
      :param tolog:
         Only available in the context of GIPSY. This selects the log file of
         Hermes.
      :type tolog:
         Boolean
      :param resetim:
         Redraw the current image. The value is set to True by default. The value
         is set to False in the loading process. After loading, one can set
         parameters but you need a trigger to make them current. Note for programmers:
         the parameters in this method are set in :meth:`MovieContainer.toggle_images`.
      :type resetim:
         Boolean

      :Examples: 
         Modify the output of coordinates. We want a position written to
         a terminal in pixels, formatted and unformatted world coordinates
         and we also want the image value at the current cursor location::
                     
            from matplotlib.pyplot import figure, show
            from kapteyn import maputils

            def postloading():
               myCubes.set_coordinate_mode(grids=True, world=True, worlduf=True,
                                          wcsfmt='%.2f', imval=True, pixfmt='%.2f', 
                                          dmsprec=2)
               cube = myCubes.cubelist[0]               

            fig = figure()
            frame = fig.add_subplot(1,1,1)
            myCubes = maputils.Cubes(fig, toolbarinfo=True, helptext=False,
                                    printload=False)
            fitsobject = maputils.FITSimage('ngc6946.fits')
            print "Possible spectral translations:", fitsobject.allowedtrans
            slicepos = range(1,101)
            myCubes.append(frame, fitsobject, axnums=(1,3), slicepos=slicepos,
                           callbackslist={'cubeloaded':postloading})
            show()
         
      """
        for im in self.movieimages.annimagelist:
            im.coord_grids = grids
            im.coord_world = world
            im.coord_worlduf = worlduf
            im.coord_imval = imval
            im.coord_appendcr = appendcr
            im.coord_tocli = tocli
            im.coord_tolog = tolog
            im.coord_pixfmt = pixfmt
            im.coord_wcsfmt = wcsfmt
            im.coord_zfmt = zfmt
            im.coord_dmsprec = dmsprec

        currentindx = self.movieimages.indx
        if resetim:
            self.movieimages.setimage(currentindx, force_redraw=True)

    def reposition(self, cb=None, force=False):
        global backgroundchanged
        backgroundchanged = True
        if self.zprofileOn:
            self.zprofileframe.changed = True
        action = True
        has_panels = self.numXpanels or self.numYpanels
        for cube in self.cubelist:
            if cube.scalefac:
                self.scaleframe(cube, cube.scalefac, reposition=False)
            else:
                self.scaleframe(cube, cube.scalefac, tofit=True, reposition=False)

        if has_panels:
            numXframesList = []
            numYframesList = []
            for cube in self.cubelist:
                numXframesList.append(len(cube.panelXframes))
                numYframesList.append(len(cube.panelYframes))

            pnrX = pnrY = 0
            for cube in self.cubelist:
                frame = cube.frame
                framep1 = cube.framep1
                framep2 = cube.framep2
                if framep1 and self.numXpanels:
                    boxX, boxY = self.getpanelboxes(frame, self.numXpanels, self.numYpanels, numXframesList, numYframesList, pnrX, None)
                    framep1.set_position(boxX)
                    framep1.set_aspect('auto')
                    pnrX += 1
                    cube.framep1 = framep1
                if framep2 and self.numYpanels:
                    boxX, boxY = self.getpanelboxes(frame, self.numXpanels, self.numYpanels, numXframesList, numYframesList, None, pnrY)
                    framep2.set_position(boxY)
                    framep2.set_aspect('auto')
                    pnrY += 1
                    cube.framep2 = framep2

        for cube in self.cubelist:
            if cube.hasgraticule:
                if hasattr(cube, 'grat'):
                    if cube.grat:
                        action = True
                        cube.frame.apply_aspect()
                        gratframe = cube.grat.frame
                        gratframe.set_position(cube.frame.get_position())
                        gratframe = cube.grat.frame2
                        gratframe.set_position(cube.frame.get_position())

        for cube in self.cubelist:
            if cube.cbframe:
                cube.cbframe.set_position(self.get_colbar_position())

        if action:
            self.fig.canvas.draw()
        return

    def redopanels(self):
        """
      Draw the slice panels for the first time or update them
      (the create_panel() method
      checks whether something needs to be plotted). The check is done for
      every cube in the cube list.
      """
        return
        for cnr in range(0, self.numcubes):
            self.create_panel('r', self.cubelist[cnr])

    def set_splitimagenr(self, nr):
        """
      Set image (by its number) which is used to split the current screen.
      
      :param nr:
         Number of the movie frame that corresponds to the image you want
         to use together with the current image to split and compare.
         Note that these movieframe numbers start with 0 and run to the 
         number of loaded frames. The numbering continues after loading 
         more than 1 data cube.

      :type nr:
         Integer
      """
        num = len(self.movieimages.annimagelist)
        if nr < 0 or nr >= num:
            raise ValueError('Image nr %d does not exist (%d<nr<%d)!' % (nr, 0, num))
        else:
            if self.movieimages.compareim:
                currentimage = self.movieimages.annimagelist[self.movieimages.indx]
                currentimage.image.im.set_alpha(1.0)
                self.movieimages.compareim.image.im.set_alpha(1.0)
                self.movieimages.compareim.image.im.set_visible(False)
                self.movieimages.compareim = None
            self.splitmovieframe = nr
        return

    def show_transparent(self, cube, alpha):
        """-----------------------------------------------------------------------
      Make current image transparent with alpha factor
      -----------------------------------------------------------------------"""
        splitmovieframe = self.splitmovieframe
        currentindx = self.movieimages.indx
        if splitmovieframe == currentindx:
            return
        currentimage = self.movieimages.annimagelist[currentindx]
        secondimage = self.movieimages.annimagelist[splitmovieframe]
        secondimage.image.im.set_visible(True)
        if splitmovieframe > currentindx:
            secondimage.image.im.set_alpha(1.0 - alpha)
            currentimage.image.im.set_alpha(1.0)
        else:
            currentimage.image.im.set_alpha(alpha)
            secondimage.image.im.set_alpha(1.0)
        self.fig.canvas.draw()
        self.movieimages.compareim = secondimage

    def splitscreen(self, cb):
        """-----------------------------------------------------------------------
      With Shift and the mouse buttons 1, 2 or 3 while moving the mouse,
      one can split the screen to make another image visible.
      It makes the upper (=current image) transparent and shows the image
      which has index 'splitmovieframe'. 
      -----------------------------------------------------------------------"""
        if cb is None or cb.event is None:
            return
        if cb.event.button is None or cb.event.key is None:
            return
        if cb.event.key != 'control':
            return
        else:
            mb = cb.event.button
            if mb not in (1, 2, 3):
                return
            try:
                currentindx = self.movieimages.indx
            except:
                return

            splitmovieframe = self.splitmovieframe
            if splitmovieframe == currentindx:
                return
            cube = self.cubelist[cb.cubenr]
            currentimage = self.movieimages.annimagelist[currentindx]
            if currentimage.cubenr != cb.cubenr:
                return
            splitimage = self.movieimages.annimagelist[splitmovieframe]
            if currentimage.origdata is None:
                cube.origdata = currentimage.data.copy()
                currentimage.origdata = cube.origdata
                currentimage.splitmovieframe = splitmovieframe
                currentimage.split_xold = currentimage.split_yold = 0
                currentimage.split_mb = mb
            xi = int(nint(cb.xdata + 0.5) - cube.pxlim[0])
            yi = int(nint(cb.ydata + 0.5) - cube.pylim[0])
            xo = int(currentimage.split_xold)
            yo = int(currentimage.split_yold)
            if mb != currentimage.split_mb:
                currentimage.data[:] = cube.origdata[:]
                currentimage.split_xold = currentimage.split_yold = 0
            if mb == 1:
                if yi > currentimage.split_yold:
                    currentimage.data[0:yi] = numpy.nan
                elif yi < currentimage.split_yold:
                    currentimage.data[yi:yo] = cube.origdata[yi:yo]
            else:
                if mb == 2:
                    if xi > currentimage.split_xold:
                        currentimage.data[:, 0:xi] = numpy.nan
                    elif xi < currentimage.split_xold:
                        currentimage.data[:, xi:xo] = cube.origdata[:, xi:xo]
                else:
                    if mb == 3:
                        if xi > currentimage.split_xold:
                            currentimage.data[0:yo:, 0:xi] = numpy.nan
                        elif xi < xo:
                            currentimage.data[0:yo:, xi:xo] = cube.origdata[0:yo, xi:xo]
                        if yi > yo:
                            currentimage.data[yo:yi, 0:xi] = numpy.nan
                        elif yi < yo:
                            currentimage.data[yi:yo, 0:xi] = cube.origdata[yi:yo, 0:xi]
                    currentimage.split_xold = xi
                    currentimage.split_yold = yi
                    currentimage.split_mb = mb
                    splitimage.image.im.set_visible(True)
                    currentimage.image.im.set_visible(True)
                    currentimage.old_blankcolor = currentimage.cmap.bad_val
                    currentimage.set_blankcolor('w', alpha=0.0)
                    currentimage.frame.draw_artist(currentimage.image.im)
                    if self.imageinfo:
                        currentimage.frame.draw_artist(currentimage.info)
                    for li in currentimage.linepieces:
                        currentimage.frame.draw_artist(li)

                for tl in currentimage.textlabels:
                    currentimage.frame.draw_artist(tl)

            return

    def updatepanels(self, cb, frompanel1=False, frompanel2=False, cubenr=None, xpos=None, ypos=None, force=False):
        global backgroundchanged
        skipupdatep1 = skipupdatep2 = False
        if frompanel1:
            skipupdatep1 = True
        if frompanel2:
            skipupdatep2 = True
        if cb is None:
            x = xpos
            y = ypos
            cubeindx = cubenr
            if x is None or y is None:
                return
        else:
            if not hasattr(cb, 'cubenr'):
                return
            x = cb.xdata
            y = cb.ydata
            cubeindx = cb.cubenr
        cube = self.cubelist[cubeindx]
        canvas = cube.frame.figure.canvas
        currentimage = self.movieimages.annimagelist[self.movieimages.indx]
        cnr = currentimage.cubenr
        currentcube = self.cubelist[cnr]
        if cb and cb.event.button != 1:
            return
        else:
            xold = cube.xold
            yold = cube.yold
            framep1 = cube.framep1
            framep2 = cube.framep2
            mplimp1 = cube.annimp1
            mplimp2 = cube.annimp2
            pxlim = cube.pxlim
            pylim = cube.pylim
            offset = cube.movieframeoffset
            xi = int(numpy.round(x))
            yi = int(numpy.round(y))
            if skipupdatep1 and xi == xold and not force:
                return
            if skipupdatep2 and yi == yold and not force:
                return
            if skipupdatep1 and (xi > pxlim[1] or xi < pxlim[0]):
                return
            if skipupdatep2 and (yi > pylim[1] or yi < pylim[0]):
                return
            if not (skipupdatep1 or skipupdatep2):
                if xi > pxlim[1] or xi < pxlim[0] or yi > pylim[1] or yi < pylim[0]:
                    return
            if cube is currentcube and self.zprofileOn:
                if not (frompanel1 or frompanel2):
                    self.plotZprofile(cube, x, y)
                else:
                    if frompanel1:
                        self.plotZprofile(cube, x, None)
                    if frompanel2:
                        self.plotZprofile(cube, None, y)
            if self.crosshair:
                for C in self.cubelist:
                    if not C.background or backgroundchanged:
                        if C is currentcube:
                            if C.background:
                                C.linev.set_visible(False)
                                C.lineh.set_visible(False)
                                C.frame.draw_artist(C.linev)
                                C.frame.draw_artist(C.lineh)
                                self.fig.canvas.draw()
                        C.background = self.fig.canvas.copy_from_bbox(C.frame.bbox)

                if cube is currentcube:
                    if not (frompanel1 or frompanel2):
                        cube.linev.set_xdata((x, x))
                        cube.lineh.set_ydata((y, y))
                    else:
                        if frompanel1:
                            cube.linev.set_xdata((x, x))
                        if frompanel2:
                            cube.lineh.set_ydata((y, y))
                    cube.linev.set_visible(True)
                    cube.lineh.set_visible(True)
                    self.fig.canvas.restore_region(cube.background)
                    cube.frame.draw_artist(cube.linev)
                    cube.frame.draw_artist(cube.lineh)
                    self.fig.canvas.blit(cube.frame.bbox)
            else:
                cube.linev.set_visible(False)
                cube.lineh.set_visible(False)
            if cube.panelXframes and (yi != yold and not skipupdatep1 or force):
                M = cube.Mx
                ly = M.shape[0]
                j = 0
                for indx in cube.panelXframes:
                    I = self.movieimages.annimagelist[(offset + indx)]
                    if I.origdata is not None:
                        N = I.origdata
                    else:
                        N = I.data
                    M[ly - j - 1] = N[int(yi - pylim[0])]
                    j += 1

                mplimp1.image.im.set_data(M)
                framep1.draw_artist(mplimp1.image.im)
                if self.crosshair and cube is currentcube:
                    framep1.draw_artist(cube.panelxline)
                if mplimp1.contourSet:
                    for col in mplimp1.contourSet.collections:
                        framep1.collections.remove(col)

                mplimp1.contourSet = None
                im = cube.imagesinthiscube[0]
                if im.contours_on:
                    cmap, colors, norm, levels = (
                     im.contours_cmap, im.contours_colour, im.norm, im.clevels)
                    if cmap is None and colors is None:
                        colors = 'r'
                    if cmap is not None:
                        cmap = cm.get_cmap(cmap)
                        colors = None
                    mplimp1.contourSet = framep1.contour(mplimp1.image.im.get_array(), levels=levels, extent=mplimp1.box, cmap=cmap, norm=norm, colors=colors)
                    for col in mplimp1.contourSet.collections:
                        col.set_visible(True)
                        mplimp1.frame.draw_artist(col)

                framep1.figure.canvas.blit(framep1.bbox)
            if cube.panelYframes and (xi != xold and not skipupdatep2 or force):
                M = cube.My
                lx = M.shape[1]
                j = 0
                for indx in cube.panelYframes:
                    I = self.movieimages.annimagelist[(offset + indx)]
                    if I.origdata is not None:
                        N = I.origdata
                    else:
                        N = I.data
                    M[:, j] = N[:, int(xi - pxlim[0])]
                    j += 1

                mplimp2.image.im.set_data(M)
                framep2.draw_artist(mplimp2.image.im)
                if self.crosshair and cube is currentcube:
                    framep2.draw_artist(cube.panelyline)
                if mplimp2.contourSet:
                    for col in mplimp2.contourSet.collections:
                        framep2.collections.remove(col)

                mplimp2.contourSet = None
                im = cube.imagesinthiscube[0]
                if im.contours_on:
                    cmap, colors, norm, levels = (
                     im.contours_cmap, im.contours_colour, im.norm, im.clevels)
                    if cmap is None and colors is None:
                        colors = 'r'
                    if cmap is not None:
                        cmap = cm.get_cmap(cmap)
                        colors = None
                    mplimp2.contourSet = framep2.contour(mplimp2.image.im.get_array(), levels=levels, extent=mplimp2.box, cmap=cmap, norm=norm, colors=colors)
                    for col in mplimp2.contourSet.collections:
                        col.set_visible(True)
                        mplimp2.frame.draw_artist(col)

                framep2.figure.canvas.blit(framep2.bbox)
            backgroundchanged = False
            if skipupdatep1:
                cube.xold = xi
            elif skipupdatep2:
                cube.yold = yi
            else:
                cube.xold = xi
                cube.yold = yi
            return

    def getbiggestbox(self):
        """
      This method finds (e.g. after a resize action) the biggest frame
      in the list of cubes. That frame sets the positions of the
      slice panels (usually the position velocity slices).
      """
        self.biggestbox = None
        for c in self.cubelist:
            if c.panelXframes or c.panelYframes:
                c.frame.apply_aspect()
                bbox = c.frame.get_position()
                box = [
                 bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax]
                if self.biggestbox is None:
                    self.biggestbox = box
                else:
                    if box[0] < self.biggestbox[0]:
                        self.biggestbox[0] = box[0]
                    if box[1] < self.biggestbox[1]:
                        self.biggestbox[1] = box[1]
                    if box[2] > self.biggestbox[2]:
                        self.biggestbox[2] = box[2]
                    if box[3] > self.biggestbox[3]:
                        self.biggestbox[3] = box[3]

        return self.biggestbox

    def clearimage(self, im):
        for li in im.linepieces:
            li.set_visible(False)

        for tl in im.textlabels:
            tl.set_visible(False)

        if im.infoobj:
            im.infoobj.set_visible(False)
        im.image.im.set_visible(False)
        if im.cbframe is not None:
            im.cbframe.set_visible(False)
        return

    def scaleframe(self, cube, scalefac, tofit=False, reposition=True):
        """
      Scale the current frame. We position the frame in the upper left corner.
      This gives the best results if panels are added. A user can resize the window
      to get an optimal view.
      """
        fig = cube.frame.figure
        xf0, yf0 = fig.transFigure.inverted().transform((0, 0))
        xf1, yf1 = fig.transFigure.inverted().transform((self.colbwpixels, 0))
        dx = xf1 - xf0
        self.colbwidth = dx
        if tofit:
            if cube.hascolbar:
                left = self.colbwidth
            else:
                left = 0.0
            if self.zprofileOn:
                top = 1.0 - self.zprofileheight
            else:
                top = 1.0
            if self.numXpanels or self.numYpanels:
                figaspect = fig.get_figwidth() / fig.get_figheight()
                if self.numXpanels:
                    H_vert = 0.2
                else:
                    H_vert = 0.0
                H_horz = H_vert / figaspect
                if self.numYpanels:
                    right = 1.0 - 0.2 / figaspect
                else:
                    right = 1.0
                bottom = 0.0 + H_vert
            else:
                right = 1.0
                bottom = 0.0
            cube.scalefac = None
        else:
            cube.scalefac = scalefac
            x0, x1 = cube.pxlim
            y0, y1 = cube.pylim
            lx = x1 - x0 + 1
            ly = y1 - y0 + 1
            fig = cube.frame.figure
            xf0, yf0 = fig.transFigure.inverted().transform((0, 0))
            xf1, yf1 = fig.transFigure.inverted().transform((lx * scalefac, ly * scalefac))
            xf = xf1 - xf0
            yf = yf1 - yf0
            if cube.hascolbar:
                left = self.colbwidth
            else:
                left = 0.0
            right = left + xf
            top = 1.0
            bottom = top - yf
        cube.frame.set_position([left, bottom, right - left, top - bottom])
        if reposition:
            self.reposition(force=True)
        return

    def loadimages(self, cb):
        """
      Loading image(s) into a movie cube is done with a timer callback. This
      callback makes it possible to show the images that you load immediately,
      which is more user friendly then when you have to wait until all images
      are loaded to see something happening on screen.
      Also it makes the gui more responsive.
      """
        cube = cb.cube
        cnr = cube.cnr
        fig = cube.frame.figure
        zprofileOn = cb.zprofileOn
        oldim = self.lastimage
        i = cb.count
        if i == 0:
            if self.progressbar:
                self.progressbar.setMinimum(0)
                self.progressbar.setMaximum(cube.nummovieframes)
            cube.callback('waitcursor')
            if oldim:
                self.clearimage(oldim)
            xf0, yf0 = fig.transFigure.inverted().transform((0, 0))
            xf1, yf1 = fig.transFigure.inverted().transform((self.colbwpixels, 0))
            dx = xf1 - xf0
            self.colbwidth = dx
            if zprofileOn:
                top = 1.0 - self.zprofileheight
            else:
                top = 1.0
            fig.subplots_adjust(left=self.colbwidth, right=1.0, bottom=0.0, top=top)
        if self.printload and cube.slicepos:
            s = '\nLoading image at slice position (in pixels)=%s' % str(cube.slicepos[i])
            flushprint(s)
        if cube.slicepos:
            cube.fitsobj.set_imageaxes(cube.axnums[0], cube.axnums[1], slicepos=cube.slicepos[i])
        cube.fitsobj.set_limits(cube.pxlim, cube.pylim)
        if cube.pixelaspectratio is None:
            cube.pixelaspectratio = cube.fitsobj.get_pixelaspectratio()
        mplim = cube.fitsobj.Annotatedimage(cube.frame, cmap=cube.cmap, clipmin=cube.vmin, clipmax=cube.vmax, gridmode=cube.gridmode, adjustable='box-forced', anchor='NW', newaspect=cube.pixelaspectratio, clipmode=cube.clipmode, clipmn=cube.clipmn, callbackslist=cube.callbackslist)
        mplim.Image(animated=False, alpha=1.0)
        mplim.plot()
        mplim.linepieces = []
        mplim.textlabels = []
        mplim.cubenr = cnr
        if cube.cmap is None:
            cube.cmap = mplim.cmap
        if not (i == 0 and cnr == 0):
            oldim.image.im.set_visible(False)
        s = 'image number %d: ' % self.movieframecounter
        mplim.info = None
        if self.imageinfo:
            mplim.info = mplim.frame.text(0.01, 0.98, s, horizontalalignment='left', verticalalignment='top', transform=mplim.frame.transAxes, fontsize=8, color='w', animated=True, family='monospace', bbox=dict(facecolor='red', alpha=0.5))
            if i == 0:
                mplim.infoobj = mplim.info
                mplim.infoobj.set_animated(False)
            else:
                mplim.infoobj = oldim.infoobj
                mplim.infoobj.set_text(str(i))
        else:
            mplim.infoobj = None
        self.lastimage = mplim
        self.movieimages.append(mplim, visible=True, cubenr=cnr, slicemessage=s)
        self.movieframecounter += 1
        cube.imagesinthiscube.append(mplim)
        if cb.count + 1 == cube.nummovieframes:
            if cube.hasgraticule:
                self.new_graticule(cube, visible=False)
            self.new_colorbar(cube)
            cube.set_slicemessages(cube.fitsobj.spectrans)
            cube.setcubeclips(cube.vmin, cube.vmax, cube.clipmode, cube.clipmn)
            cube.vmin_def = cube.vmin
            cube.vmax_def = cube.vmax
            self.reposition()
        else:
            fig.canvas.draw()
        cb.count += 1
        if self.progressbar:
            self.progressbar.setValue(cb.count)
        if cb.count == cube.nummovieframes:
            cb.deschedule()
            self.set_coordinate_mode(resetim=False)
            self.timerlist.pop(0)
            if self.timerlist:
                self.timerlist[0].schedule()
            else:
                self.lastimage.image.im.set_visible(False)
                self.callback('memory', getmemory())
                if self.cubelist[0].panelscb is None:
                    self.set_interactionMovieToPanels()
                else:
                    self.update_interactionMovieToPanels()
                self.movieimages.setimage(cube.movieframeoffset)
                self.movieimages.movie_events(allow=True)
                self.callback('finished')
            if self.progressbar:
                self.progressbar.reset()
            cube.callback('resetcursor')
            cube.callback('cubeloaded')
            cube.cmap.auto = True
            cube.cmap.callback = self.cmapcallback
        return

    def set_interactionMovieToPanels(self):
        """
      The movie frames for the current cube are all stored in the movie.
      Register a callback for interaction in the movie. Each cube is
      associated with a matplotlib frame (Axes object). So a change in
      mouse position will update the slice panels that belong to each cube
      """
        for cube in self.cubelist:
            if cube.nummovieframes >= 1:
                cube.panelscb = AxesCallback(self.updatepanels, cube.frame, 'motion_notify_event', cubenr=cube.cnr)
            cube.splitcb = AxesCallback(self.splitscreen, cube.frame, 'motion_notify_event', cubenr=cube.cnr)
            cube.splitcb.deschedule()
            for aim in cube.imagesinthiscube:
                aim.splitcb = cube.splitcb

    def update_interactionMovieToPanels(self):
        """-----------------------------------------------------------------------
      Update interaction in movie container. This implies that we add a new
      callback, because this method is called only when we added a new cube.
      -----------------------------------------------------------------------"""
        for cube in self.cubelist:
            if cube.panelscb is not None:
                cube.panelscb.schedule()
            elif cube.nummovieframes >= 1:
                cube.panelscb = AxesCallback(self.updatepanels, cube.frame, 'motion_notify_event', cubenr=cube.cnr)
            if cube.splitcb is None:
                cube.splitcb = AxesCallback(self.splitscreen, cube.frame, 'motion_notify_event', cubenr=cube.cnr)
                for aim in cube.imagesinthiscube:
                    aim.splitcb = cube.splitcb

            cube.splitcb.deschedule()

        return

    def end_interactionMovieToPanels(self):
        """-----------------------------------------------------------------------
      End interaction in side panels.
      Note that this method is called in the append() method where the
      timer is scheduled for the loadimages() method. There we append
      a cube which does not have any callbacks set, but in a loop
      over all the cubes we check whether attribute 'panelscb' is set.
      -----------------------------------------------------------------------"""
        for cube in self.cubelist:
            if cube.panelscb is not None:
                cube.panelscb.deschedule()
            if cube.splitcb is not None:
                cube.splitcb.deschedule()

        return