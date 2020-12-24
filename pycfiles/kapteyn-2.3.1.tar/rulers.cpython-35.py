# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/jansky/data/users/breddels/src/kapteyn-sky2/kapteyn/rulers.py
# Compiled at: 2016-03-21 10:28:21
# Size of source mod 2**32: 32220 bytes
"""
.. highlight:: python
   :linenothreshold: 10

Module rulers
===============
This module defines a class for drawing rulers.

.. autoclass:: Ruler

"""
import numpy
from kapteyn.positions import str2pos, unitfactor

def isinside(x, y, pxlim, pylim):
    if pxlim[0] <= pxlim[1]:
        if x < pxlim[0] - 0.5 or x > pxlim[1] + 0.5:
            return False
    elif x < pxlim[1] - 0.5 or x > pxlim[0] + 0.5:
        return False
    if pylim[0] <= pylim[1]:
        if y < pylim[0] - 0.5 or y > pylim[1] + 0.5:
            return False
    elif y < pylim[1] - 0.5 or y > pylim[0] + 0.5:
        return False
    return True


def dispcoord(longitude, latitude, disp, direction, angle):
    """
   Find a world coordinate with distance 'disp' w.r.t. given
   long, lat. The angle of the line between the two points
   has angle 'angle' w.r.t. the North.

   Note that this is a copy of a routine in maputils.
   To avoid circular imports, we copied the function here.
   
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


class Ruler(object):
    __doc__ = '\n   Draws a line between two spatial positions\n   from a start point (x1,y1) to an end point (x2,y2)\n   with labels indicating a constant offset in world\n   coordinates. The positions are either in pixels\n   or in world coordinates. The start and end point\n   can also be positions entered as a string which\n   follows the syntax described in method\n   :func:`positions.str2pos`. The ruler can also\n   be given as a start point and a size and angle.\n   These are distance and angle on a sphere.\n\n   The ruler is a straight\n   line but the ticks are usually not equidistant\n   because projection effects make the offsets non linear\n   (e.g. the TAN projection diverges while the CAR projection\n   shows equidistant ticks).\n   By default, the zero point is exactly in the middle of\n   the ruler but this can be changed by setting a\n   value for *lambda0*.  The step size\n   for the ruler ticks in units of the spatial\n   axes is entered in parameter *step*.\n   At least one of the axes in the plot needs to be\n   a spatial axis.\n\n   Size and step size can be entered in units given by\n   a parameter *units*. The default unit is degrees.\n\n   :param projection:    The Projection object which sets the WCS for the ruler.\n   :type projection:     A :class:`wcs.Projection` object\n\n   :param mixpix:        The pixel of the missing spatial axis in a Position-Velocity\n                         image.\n   :type mixpix:         Integer\n\n   :param pxlim:         Limit in pixel coordinates for the x-axis.\n   :type pxlim:          Tuple or list with two integers.\n\n   :param pylim:         Limit in pixel coordinates for the y-axis.\n   :type pylim:          Tuple or list with two integers.\n\n   :param aspectratio:   The aspect ratio is defined as *pixel height / pixel width*.\n                         The value is needed to draw tick mark perpendicular\n                         to the ruler line for images where the pixels are not square\n                         in world coordinates. Its default is 1.0.\n   :type aspectratio:    Float\n\n   :param pos1:          Position information for the start point. This info overrules\n                         the values in x1 and y1.\n   :type pos1:           String\n\n   :param pos2:          Position information for the end point. This info overrules\n                         the values in x2 and y2.\n   :type pos2:           String\n\n   :param rulersize:     Instead of entering a start- and an end point, one can also\n                         enter a start point in *pos1* or in *x1, y1* and specify a\n                         size of the ruler. The size is entered in units given by\n                         parameter *units*. If no units are given, the size is in degrees.\n                         Note that with size we mean the distance on a sphere.\n                         To calculate the end point, we need an angle.\n                         this angle is given in *rulerangle*.\n                         If *rulersize* has a value, then values in *pos2* and *x2,y2*\n                         are ignored.\n   :type rulersize:      Floating point number\n\n   :param rulerangle:    An angel in degrees which, together with *rulersize*, sets the\n                         end point of the ruler. The angle is defined as an angle on\n                         a sphere.  The angle is an astronomical angle (defined\n                         with respect to the direction of the North).\n\n   :type rulerangle:     Floating point number\n\n   :param x1:            X-location of start of ruler either in pixels or world coordinates\n                         Default is lowest pixel coordinate in x.\n   :type x1:             None or Floating point number\n\n   :param y1:            Y-location of start of ruler either in pixels or world coordinates\n                         Default is lowest pixel coordinate in y.\n   :type y1:             None or Floating point number\n\n   :param x2:            X-location of end of ruler either in pixels or world coordinates\n                         Default is highest pixel coordinate in x.\n   :type x2:             None or Floating point number\n\n   :param y2:            Y-location of end of ruler either in pixels or world coordinates\n                         Default is highest pixel coordinate in y.\n   :type y2:             None or Floating point number\n\n   :param lambda0:       Set the position of label which represents offset 0.0.\n                         Default is lambda=0.5 which represents the middle of the ruler.\n                         If you set lambda=0 then offset 0.0 is located at the start\n                         of the ruler. If you set lambda=1 then offset 0.0 is located at the\n                         end of the ruler.\n   :type lambda0:        Floating point number\n\n   :param step:          Step size of world coordinates in degrees or in units\n                         entered in *units*.\n   :type step:           Floating point number\n\n   :param world:         Set ruler mode to world coordinates (default is pixels)\n   :type world:          Boolean\n\n   :param angle:         Set angle of tick marks in degrees. If omitted then a default\n                         is calculated (perpendicular to ruler line) which applies\n                         to all labels.\n   :type angle:          Floating point number\n\n   :param addangle:      Add a constant angle in degrees to *angle*.\n                         Only useful if *angle* has its default\n                         value. This parameter is used to improve layout.\n   :type adangle:        Floating point number\n\n   :param fmt:           Format of the labels. See example.\n   :type fmt:            String\n\n   :param fun:           Format ruler values according to this function (e.g. to convert\n                         degrees into arcminutes). The output is always in degrees.\n   :type fun:            Python function or Lambda expression\n\n   :param units:         Rulers ticks are labeled in a unit that is compatible\n                         with degrees. The units are set by the step size used to\n                         calculate the position of the tick marks. You can\n                         set these units explicitely with this parameter.\n                         Note that values for *fun* and *fmt*\n                         cannot be set because these are set automatically if\n                         *units* has a value. Note that *units* needs only\n                         a part of a complete units string because a\n                         case insensitive minimal match\n                         is applied. Usually one will use something like\n                         *units=arcmin* or *units=Arcsec*.\n\n                         Note: If a value for *units* is entered, then this method\n                         expects the step size is given in the same units.\n   :type units:          String\n\n   :param fliplabelside: Choose other side of ruler to draw labels.\n   :type fliplabelside:  Boolean\n\n   :param mscale:        A scaling factor to create more or less distance between\n                         the ruler and its labels. If *None* then this method calculates\n                         defaults. The values are usually less than 5.0.\n\n   :type mscale:         Floating point number\n\n   :param gridmode:      If True, correct pixel position for CRPIX to\n                         get grid coordinates where the pixel at CRPIX is 0\n   :type gridmode:       Boolean\n\n   :param `**kwargs`:    Set keyword arguments for the labels.\n                         The attributes for the ruler labels are set with these keyword arguments.\n   :type `**kwargs`:     Matplotlib keyword argument(s)\n\n   :Raises:\n      :exc:`Exception`\n         *Rulers only suitable for maps with at least one spatial axis!*\n         These rulers are only for plotting offsets as distances on\n         a sphere for the current projection system. So we need at least\n         one spatial axis and if there is only one spatial axis in the plot,\n         then we need a matching spatial axis.\n      :exc:`Exception`\n         *Cannot make ruler with step size equal to zero!*\n         Either the input of the step size is invalid or a wrong default\n         was calculated (perhaps end point is equal to start point).\n      :exc:`Exception`\n         *Start point of ruler not in pixel limits!*\n      :exc:`Exception`\n         *End point of ruler not in pixel limits!*\n\n   :Returns:      A ruler object of class ruler which is added to the plot container\n                  with Plotversion\'s method :meth:`Plotversion.add`.\n                  This ruler object has two methods to change the properties\n                  of the line and the labels:\n\n                  * `setp_line(**kwargs)` -- Matplotlib keyword arguments for changing\n                     the line properties.\n                  * `setp_labels(**kwargs)` -- Matplotlib keyword arguments for changing\n                     the label properties.\n\n   :Notes:        A bisection is used to find a new marker position so that\n                  the distance to a previous position is *step*..\n                  We use a formula of Thaddeus Vincenty, 1975, for the\n                  calculation of a distance on a sphere accurate over the\n                  entire sphere.\n\n   :Examples:     Create a ruler object and change its properties\n\n                  ::\n\n                     ruler2 = annim.Ruler(x1=x1, y1=y1, x2=x2, y2=y2, lambda0=0.5, step=2.0,\n                                          fmt=\'%3d\', mscale=-1.5, fliplabelside=True)\n                     ruler2.setp_labels(ha=\'left\', va=\'center\', color=\'b\')\n\n                     ruler4 = annim.Ruler(pos1="23h0m 15d0m", pos2="22h0m 30d0m", lambda0=0.0,\n                                          step=1, world=True,\n                                          fmt=r"$%4.0f^\\prime$",\n                                          fun=lambda x: x*60.0, addangle=0)\n                     ruler4.setp_line(color=\'g\')\n                     ruler4.setp_labels(color=\'m\')\n\n                     # Force step size and labeling to be in minutes of arc.\n                     annim.Ruler(pos1=\'0h3m30s 6d30m\', pos2=\'0h3m30s 7d0m\',\n                                 lambda0=0.0, step=5.0,\n                                 units=\'arcmin\', color=\'c\')\n\n   .. automethod:: setp_line\n   .. automethod:: setp_label\n   '

    def __init__(self, projection, mixpix, pxlim, pylim, aspectratio=1.0, pos1=None, pos2=None, rulersize=None, rulerangle=None, x1=None, y1=None, x2=None, y2=None, lambda0=0.5, step=None, world=False, angle=None, addangle=0.0, fmt=None, fun=None, units=None, fliplabelside=False, mscale=None, labelsintex=True, gridmode=False, **kwargs):
        self.ptype = 'Ruler'
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.x = []
        self.y = []
        self.xw = []
        self.yw = []
        self.stepsizeW = None
        self.label = []
        self.offsets = []
        self.angle = None
        self.kwargs = {'clip_on': True}
        self.tickdx = None
        self.tickdy = None
        self.mscale = None
        self.fun = None
        self.fmt = None
        self.linekwargs = {'color': 'k'}
        self.kwargs.update(kwargs)
        self.aspectratio = aspectratio
        self.rulertitle = None
        self.gridmode = gridmode

        def bisect(offset, lambda_s, Xw, Yw, x1, y1, x2, y2):
            """
         We are looking for a value mu so that mu+lambda_s sets a
         pixel which corresponds to world coordinates that are
         'offset' away from the start point set by lambda_s
         If lambda_s == 0 then we are in x1, x2. If lambda_s == 1
         we are in x2, y2
         """
            mes = ''
            if offset >= 0.0:
                a = 0.0
                b = 1.1
            else:
                a = -1.1
                b = 0.0
            f1 = getdistance(a, lambda_s, Xw, Yw, x1, y1, x2, y2) - abs(offset)
            f2 = getdistance(b, lambda_s, Xw, Yw, x1, y1, x2, y2) - abs(offset)
            validconditions = f1 * f2 < 0.0
            if not validconditions:
                mes = 'Found interval without a root for this step size'
                return (
                 None, mes)
            tol = 1e-12
            N0 = 50
            i = 0
            fa = getdistance(a, lambda_s, Xw, Yw, x1, y1, x2, y2) - abs(offset)
            while i <= N0:
                p = a + (b - a) / 2.0
                fp = getdistance(p, lambda_s, Xw, Yw, x1, y1, x2, y2) - abs(offset)
                i += 1
                if fp == 0.0 or (b - a) / 2.0 < tol:
                    break
                if fa * fp > 0:
                    a = p
                    fa = fp
                else:
                    b = p
            else:
                mes = 'Ruler bisection failed after %d iterations!' % N0
                p = None

            return (
             p, mes)

        def DV(l1, b1, l2, b2):
            fac = numpy.pi / 180.0
            l1 *= fac
            b1 *= fac
            l2 *= fac
            b2 *= fac
            dlon = l2 - l1
            a1 = numpy.cos(b2) * numpy.sin(dlon)
            a2 = numpy.cos(b1) * numpy.sin(b2) - numpy.sin(b1) * numpy.cos(b2) * numpy.cos(dlon)
            a = numpy.sqrt(a1 * a1 + a2 * a2)
            b = numpy.sin(b1) * numpy.sin(b2) + numpy.cos(b1) * numpy.cos(b2) * numpy.cos(dlon)
            d = numpy.arctan2(a, b)
            return d * 180.0 / numpy.pi

        def tolonlat(x, y):
            if mixpix == None:
                xw, yw = projection.toworld((x, y))
                xwo = xw
                ywo = yw
            else:
                W = projection.toworld((x, y, mixpix))
                xw = W[(projection.lonaxnum - 1)]
                yw = W[(projection.lataxnum - 1)]
                xwo = xw
                ywo = yw
            if projection.lonaxnum > projection.lataxnum:
                xwo, ywo = ywo, xwo
            return (
             xw, yw, xwo, ywo)

        def topixel2(xw, yw):
            if mixpix == None:
                x, y = projection.topixel((xw, yw))
            else:
                unknown = numpy.nan
                wt = (xw, yw, unknown)
                pixel = (unknown, unknown, mixpix)
                wt, pixel = projection.mixed(wt, pixel)
                x = pixel[0]
                y = pixel[1]
            return (
             x, y)

        def getdistance(mu, lambda_s, Xw, Yw, x1, y1, x2, y2):
            lam = lambda_s + mu
            x = x1 + lam * (x2 - x1)
            y = y1 + lam * (y2 - y1)
            xw, yw, xw1, yw1 = tolonlat(x, y)
            return DV(Xw, Yw, xw, yw)

        def nicestep(x1, y1, x2, y2):
            xw1, yw1, dummyx, dummyy = tolonlat(x1, y1)
            xw2, yw2, dummyx, dummyy = tolonlat(x2, y2)
            step = None
            length = DV(xw1, yw1, xw2, yw2)
            sec = numpy.array([30, 20, 15, 10, 5, 2, 1])
            minut = sec
            deg = numpy.array([60, 30, 20, 15, 10, 5, 2, 1])
            nicenumber = numpy.concatenate((deg * 3600.0, minut * 60.0, sec))
            fact = 3600.0
            d = length * fact
            step2 = 0.9 * d / 3.0
            for p in nicenumber:
                k = int(step2 / p)
                if k >= 1.0:
                    step2 = k * p
                    step = step2
                    break

            if step == None:
                f = int(numpy.log10(d))
                if d < 1.0:
                    f -= 1
                D3 = numpy.round(d / 10.0 ** f, 0)
                if D3 == 3.0:
                    D3 = 2.0
                else:
                    if D3 == 6:
                        D3 = 5.0
                    elif D3 == 7:
                        D3 = 8
            else:
                if D3 == 9:
                    D3 = 10
                if D3 in (2, 4, 8):
                    k = 4
                else:
                    k = 5
                step = D3 * 10.0 ** f / k
            return step / fact

        spatial = projection.types[0] in ('longitude', 'latitude') or projection.types[1] in ('longitude',
                                                                                              'latitude')
        if not spatial:
            raise Exception('Rulers only suitable for maps with at least one spatial axis!')
        uf = None
        if units is not None:
            uf, errmes = unitfactor('degree', units)
            if uf is None:
                raise ValueError(errmes)
            if pos1 is not None:
                poswp = str2pos(pos1, projection, mixpix=mixpix, gridmode=self.gridmode)
                if poswp[3] != '':
                    raise Exception(poswp[3])
                pix = poswp[1][0]
                x1 = pix[0]
                y1 = pix[1]
        elif x1 is None:
            x1 = pxlim[0]
            world = False
        if y1 is None:
            y1 = pylim[0]
            world = False
        if world:
            x1, y1 = topixel2(x1, y1)
        if pos2 is not None:
            poswp = str2pos(pos2, projection, mixpix=mixpix, gridmode=self.gridmode)
            if poswp[3] != '':
                raise Exception(poswp[3])
            pix = poswp[1][0]
            x2 = pix[0]
            y2 = pix[1]
        else:
            if rulersize is not None:
                lon1, lat1, xwo1, ywo1 = tolonlat(x1, y1)
                swapped = lon1 != xwo1
                if rulerangle is None:
                    rulerangle = 270.0
                if uf is not None:
                    rulersize /= uf
                lon2, lat2 = dispcoord(lon1, lat1, rulersize, -1, rulerangle)
                if swapped:
                    x2 = lat2
                    y2 = lon2
                else:
                    x2 = lon2
                    y2 = lat2
                x2, y2 = topixel2(x2, y2)
            else:
                if x2 is None:
                    x2 = pxlim[1]
                    world = False
                if y2 is None:
                    y2 = pylim[1]
                    world = False
                if world:
                    x2, y2 = topixel2(x2, y2)
                if step is None:
                    stepsizeW = nicestep(x1, y1, x2, y2)
                else:
                    stepsizeW = step
                if step == 0.0:
                    raise Exception('Cannot make ruler with step size equal to zero!')
                uf = None
                if units != None:
                    uf, errmes = unitfactor('degree', units)
                    if uf is None:
                        raise ValueError(errmes)
                    if uf != 1.0:
                        fun = lambda x: x * uf
                        if step is not None:
                            stepsizeW /= uf
                        if fmt is None:
                            pass
                if uf == 1.0:
                    if labelsintex:
                        fmt = '%4.0f^{\\circ}'
                    else:
                        fmt = '%4.0f°'
                else:
                    if uf == 60.0:
                        if labelsintex:
                            fmt = '%4.0f^{\\prime}'
                        else:
                            fmt = "%4.0f'"
                    else:
                        if uf == 3600.0:
                            if labelsintex:
                                fmt = '%4.0f^{\\prime\\prime}'
                            else:
                                fmt = "%4.0f''"
                        else:
                            raise ValueError('Only degree, arcmin and arcsec allowed')
            if fun is None and fmt is None:
                if labelsintex:
                    fmt = '%4.0f^{\\circ}'
                else:
                    fmt = '%4.0f°'
        if abs(stepsizeW) < 1.0:
            fun = lambda x: x * 60.0
            if labelsintex:
                fmt = '%4.0f^{\\prime}'
            else:
                fmt = "%4.0f'"
            if abs(stepsizeW) < 0.016666666666666666:
                fun = lambda x: x * 3600.0
                if labelsintex:
                    fmt = '%4.0f^{\\prime\\prime}'
                else:
                    fmt = "%4.0f''"
        else:
            if fmt is None:
                fmt = '%g'
            start_in = isinside(x1, y1, pxlim, pylim)
            if not start_in:
                raise Exception('Start point of ruler not in pixel limits!')
            end_in = isinside(x2, y2, pxlim, pylim)
            if not end_in:
                raise Exception('End point of ruler not in pixel limits!')
            defangle = 180.0 * numpy.arctan2(y2 - y1, (x2 - x1) / aspectratio) / numpy.pi - 90.0
            l1 = pxlim[1] - pxlim[0] + 1.0
            l1 /= 100.0
            l2 = pylim[1] - pylim[0] + 1.0
            l2 /= 100.0
            ll = max(l1, l2)
            dx = ll * numpy.cos(defangle * numpy.pi / 180.0) * aspectratio
            dy = ll * numpy.sin(defangle * numpy.pi / 180.0)
            if fliplabelside:
                dx = -dx
                dy = -dy
            if angle == None:
                phi = defangle
            else:
                phi = angle
        phi += addangle
        defkwargs = {'fontsize': 10, 'rotation': phi}
        if defangle + 90.0 in (270.0, 90.0, -90.0, -270.0):
            if fliplabelside:
                defkwargs.update({'va': 'center', 'ha': 'right'})
            else:
                defkwargs.update({'va': 'center', 'ha': 'left'})
            if mscale == None:
                mscale = 1.5
        else:
            if defangle + 90.0 in (0.0, 180.0, -180.0):
                if fliplabelside:
                    defkwargs.update({'va': 'bottom', 'ha': 'center'})
                else:
                    defkwargs.update({'va': 'top', 'ha': 'center'})
                mscale = 1.5
            else:
                defkwargs.update({'va': 'center', 'ha': 'center'})
        if mscale == None:
            mscale = 2.5
        defkwargs.update(kwargs)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.angle = defangle
        self.tickdx = dx
        self.tickdy = dy
        self.mscale = mscale
        self.kwargs.update(defkwargs)
        self.fmt = fmt
        self.fun = fun
        self.flip = fliplabelside
        lambda_s = lambda0
        x0 = x1 + lambda_s * (x2 - x1)
        y0 = y1 + lambda_s * (y2 - y1)
        Xw, Yw, xw1, yw1 = tolonlat(x0, y0)
        self.append(x0, y0, 0.0, fmt % 0.0)
        self.appendW(xw1, yw1)
        self.stepsizeW = stepsizeW
        for sign in [1.0, -1.0]:
            mu = 0.0
            offset = 0.0
            lamplusmu = lambda_s + mu
            while mu != None and 0.0 <= lamplusmu <= 1.0:
                offset += sign * stepsizeW
                mu, mes = bisect(offset, lambda_s, Xw, Yw, x1, y1, x2, y2)
                if mu != None:
                    lamplusmu = lambda_s + mu
                    if 0.0 <= lamplusmu <= 1.0:
                        x = x1 + lamplusmu * (x2 - x1)
                        y = y1 + lamplusmu * (y2 - y1)
                        if fun != None:
                            off = fun(offset)
                        else:
                            off = abs(offset)
                        self.append(x, y, offset, fmt % off, labelsintex)
                        xw, yw, xw1, yw1 = tolonlat(x, y)
                        self.appendW(xw1, yw1)
                elif sign == -1.0:
                    break

        self.pxlim = pxlim
        self.pylim = pylim

    def set_title(self, rulertitle, **kwargs):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        defangle = 180.0 * numpy.arctan2(y2 - y1, (x2 - x1) / self.aspectratio) / numpy.pi
        xt = x1 + 0.5 * (x2 - x1)
        yt = y1 + 0.5 * (y2 - y1)
        self.xt = xt
        self.yt = yt
        self.titleangle = defangle
        self.rulertitle = rulertitle
        self.titlekwargs = kwargs

    def setp_line(self, **kwargs):
        """
      Set the ruler line properties. The keyword arguments are Matplotlib
      keywords for :class:`Line2D` objects.

      :param kwargs: Keyword argument(s) for changing the default properties
                     of the ruler line. This line is a :class:`Line2D`
                     Matplotlib object with attributes like
                     *linewidth*, *color* etc.
      :type kwargs:  Python keyword arguments
      """
        self.linekwargs.update(kwargs)

    def setp_label(self, **kwargs):
        """
      Set the ruler label properties. The keyword arguments are Matplotlib
      keywords for :class:`Text` objects. Note that the properties
      apply to all labels. It is not possible to address a separate label.

      :param kwargs: Keyword argument(s) for changing the default properties
                     of the ruler labels. This line is a :class:`Text`
                     Matplotlib object with attributes like
                     *fontsize*, *color* etc.
      :type kwargs:  Python keyword arguments
      """
        self.kwargs.update(kwargs)

    def append(self, x, y, offset, label, labelsintex=True):
        self.x.append(x)
        self.y.append(y)
        self.offsets.append(offset)
        if labelsintex:
            label = '$%s$' % label
        self.label.append(label)

    def appendW(self, xw, yw):
        self.xw.append(xw)
        self.yw.append(yw)

    def plot(self, frame):
        """
      Plot one ruler object in the current frame
      """
        frame.plot((self.x1, self.x2), (self.y1, self.y2), '-', **self.linekwargs)
        dx = self.tickdx
        dy = self.tickdy
        for x, y, label in zip(self.x, self.y, self.label):
            frame.plot([x, x + dx], [y, y + dy], '-', color='k')
            frame.text(x + self.mscale * dx, y + self.mscale * dy, label, **self.kwargs)

        if self.rulertitle is not None:
            if self.flip:
                titlekwargs = {'va': 'top', 'ha': 'center', 'rotation_mode': 'anchor'}
            else:
                titlekwargs = {'va': 'bottom', 'ha': 'center', 'rotation_mode': 'anchor'}
            titlekwargs.update(self.titlekwargs)
            titleangle = self.titleangle
            if titleangle > 135.0:
                titleangle -= 180.0
                titlekwargs.update({'va': 'top'})
            if titleangle <= -135.0:
                titleangle += 180.0
                titlekwargs.update({'va': 'top'})
            try:
                frame.text(self.xt - dx, self.yt - dy, self.rulertitle, rotation=titleangle, **titlekwargs)
            except:
                pass