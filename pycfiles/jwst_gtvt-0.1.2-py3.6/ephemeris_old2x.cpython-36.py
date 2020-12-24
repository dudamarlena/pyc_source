# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/jwst_gtvt/ephemeris_old2x.py
# Compiled at: 2020-04-22 16:08:44
# Size of source mod 2**32: 10011 bytes
from __future__ import print_function
import sys
from math import *
from .rotationsx import *
from . import astro_funcx as astro_func
D2R = pi / 180.0
R2D = 180.0 / pi
PI2 = 2.0 * pi
unit_limit = lambda x: min(max(-1.0, x), 1.0)
MIN_SUN_ANGLE = 84.8 * D2R
MAX_SUN_ANGLE = 135.0 * D2R
SUN_ANGLE_PAD = 0.5 * D2R
obliquity_of_the_ecliptic = -23.439291
obliquity_of_the_ecliptic *= D2R
Qecl2eci = QX(obliquity_of_the_ecliptic)

class Ephemeris:

    def __init__(self, afile, cnvrt=False, verbose=True):
        """Eph constructor, cnvrt True converts into Ecliptic frame """
        if cnvrt:
            if verbose:
                print('Using Ecliptic Coordinates')
        else:
            if verbose:
                print('Using Equatorial Coordinates')
            else:
                self.datelist = []
                self.xlist = []
                self.ylist = []
                self.zlist = []
                self.amin = 0.0
                self.amax = 0.0
                aV = Vector(0.0, 0.0, 0.0)
                fin = open(afile, 'r').readlines()
                if afile.find('l2_halo_FDF_060619.trh') > -1:
                    ascale = 0.001
                else:
                    ascale = 1.0
            if afile.find('horizons_EM') > -1:
                not_there = True
                istart = 0
                while fin[istart][:5] != '$$SOE':
                    if fin[istart].find('Center body name:') > -1:
                        if fin[istart].find('Sun') > -1:
                            not_there = False
                        elif verbose:
                            print(fin[istart])
                    istart += 1

                istart += 1
                if not_there:
                    print('This ephemeris does not use the Sun as the center body.  It should not be used.')
                    exit(-1)
                while fin[istart][:5] != '$$EOE':
                    item = fin[istart].strip()
                    item = item.split(',')
                    adate = float(item[0]) - 2400000.5
                    x = float(item[2]) * ascale
                    y = float(item[3]) * ascale
                    z = float(item[4]) * ascale
                    if cnvrt:
                        aV.set_eq(x, y, z)
                        ll = aV.length()
                        aV = aV / ll
                        aV = Qecl2eci.inv_cnvrt(aV)
                        aV = aV * ll
                        x = aV.rx()
                        y = aV.ry()
                        z = aV.rz()
                    self.datelist.append(adate)
                    self.xlist.append(x)
                    self.ylist.append(y)
                    self.zlist.append(z)
                    if self.amin == 0.0:
                        self.amin = adate
                    istart += 1

            else:
                for item in fin[2:]:
                    item = string.strip(item)
                    item = string.split(item)
                    adate = time2.mjd_from_string(item[0])
                    x = float(item[1]) * ascale
                    y = float(item[2]) * ascale
                    z = float(item[3]) * ascale
                    if cnvrt:
                        aV.set_eq(x, y, z)
                        ll = aV.length()
                        aV = aV / ll
                        aV = Qecl2eci.inv_cnvrt(aV)
                        aV = aV * ll
                        x = aV.rx()
                        y = aV.ry()
                        z = aV.rz()
                    self.datelist.append(adate)
                    self.xlist.append(x)
                    self.ylist.append(y)
                    self.zlist.append(z)
                    if self.amin == 0.0:
                        self.amin = adate

        self.amax = adate
        del fin

    def report_ephemeris(self, limit=100000, pathname=None):
        """Prints a formatted report of the ephemeris.
        
        If a limit is specified, no more than the maximum number of records are reported.
        pathname = optional path to a file to hold the report."""
        num_to_report = min(limit, len(self.datelist))
        if pathname:
            dest = open(pathname, 'w')
            print(('#Generated %s\n' % time.ctime()), file=dest)
        else:
            dest = sys.stdout
        print(('%17s  %14s  %14s  %14s\n' % ('DATE      ', 'X (KM)   ', 'Y (KM)   ',
                                             'Z (KM)   ')), file=dest)
        for num in range(num_to_report):
            date = self.datelist[num]
            x = self.xlist[num]
            y = self.ylist[num]
            z = self.zlist[num]
            print(('%17s  %14.3f  %14.3f  %14.3f' % (time2.display_date(date), x, y, z)), file=dest)

        if pathname:
            dest.close()

    def pos(self, adate):
        cal_days = adate - self.datelist[0]
        indx = int(cal_days)
        frac = cal_days - indx
        x = (self.xlist[(indx + 1)] - self.xlist[indx]) * frac + self.xlist[indx]
        y = (self.ylist[(indx + 1)] - self.ylist[indx]) * frac + self.ylist[indx]
        z = (self.zlist[(indx + 1)] - self.zlist[indx]) * frac + self.zlist[indx]
        return Vector(x, y, z)

    def Vsun_pos(self, adate):
        Vsun = -1.0 * self.pos(adate)
        Vsun = Vsun / Vsun.length()
        return Vsun

    def sun_pos(self, adate):
        Vsun = -1.0 * self.pos(adate)
        Vsun = Vsun / Vsun.length()
        coord2 = asin(unit_limit(Vsun.z))
        coord1 = atan2(Vsun.y, Vsun.x)
        if coord1 < 0.0:
            coord1 += PI2
        return (
         coord1, coord2)

    def normal_pa(self, adate, tgt_c1, tgt_c2):
        sun_c1, sun_c2 = self.sun_pos(adate)
        sun_pa = astro_func.pa(tgt_c1, tgt_c2, sun_c1, sun_c2)
        V3_pa = sun_pa + pi
        if V3_pa < 0.0:
            V3_pa += PI2
        if V3_pa >= PI2:
            V3_pa -= PI2
        return V3_pa

    def is_valid(self, date, coord_1, coord_2, V3pa):
        """Indicates whether an attitude is valid at a given date."""
        if date < self.amin or date > self.amax:
            return False
        else:
            sun_1, sun_2 = self.sun_pos(date)
            d = astro_func.dist(coord_1, coord_2, sun_1, sun_2)
            vehicle_pitch = pi / 2 - d
            if d < MIN_SUN_ANGLE or d > MAX_SUN_ANGLE:
                return False
            pa = astro_func.pa(coord_1, coord_2, sun_1, sun_2) + pi
            roll = acos(cos(V3pa - pa))
            sun_roll = asin(sin(roll) * cos(vehicle_pitch))
            if abs(sun_roll) <= 5.2 * D2R:
                sun_pitch = atan2(tan(vehicle_pitch), cos(roll))
                if sun_pitch <= 5.0 * D2R:
                    if sun_pitch >= -44.8 * D2R:
                        return True
            return False

    def in_FOR(self, adate, coord_1, coord_2):
        sun_1, sun_2 = self.sun_pos(adate)
        d = astro_func.dist(coord_1, coord_2, sun_1, sun_2)
        if d < MIN_SUN_ANGLE or d > MAX_SUN_ANGLE:
            return False
        else:
            return True

    def bisect_by_FOR(self, in_date, out_date, coord_1, coord_2):
        delta_days = 200.0
        mid_date = (in_date + out_date) / 2.0
        while delta_days > 1e-06:
            sun_1, sun_2 = self.sun_pos(mid_date)
            d = astro_func.dist(coord_1, coord_2, sun_1, sun_2)
            if d > MAX_SUN_ANGLE or d < MIN_SUN_ANGLE:
                out_date = mid_date
            else:
                in_date = mid_date
            mid_date = (in_date + out_date) / 2.0
            delta_days = abs(in_date - out_date) / 2.0

        if in_date > out_date:
            mid_date = mid_date + 1e-06
        else:
            mid_date = mid_date - 1e-06
        return mid_date

    def bisect_by_attitude(self, in_date, out_date, coord_1, coord_2, pa):
        icount = 0
        delta_days = 200.0
        mid_date = (in_date + out_date) / 2.0
        while delta_days > 1e-06:
            if self.is_valid(mid_date, coord_1, coord_2, pa):
                in_date = mid_date
            else:
                out_date = mid_date
            mid_date = (in_date + out_date) / 2.0
            delta_days = abs(in_date - out_date) / 2.0
            icount = icount + 1

        return mid_date