# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/v2/test.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 56234 bytes
"""
This a test suite for NPK.
  
Note that all functionalities  are not tested yet !
"""
from __future__ import print_function
import unittest, tempfile, math
from v1.Kore import *
error = 0

class TextNPKv1(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print('\n========', self.shortDescription(), '===============')

    def test_benchmark(self):
        """
     benchmark for gifa
     verbose 1    # check what you're doing
     benchmark for NPK
       run on a 512 x 2k real data set.
       Processing performed is :
       - Exponen. Broading in F2
       - Real FT, phasing, in F22
       - 5 points Spline base-line correction in F2
       - cosine apodization in F1, zero-filling in F1
       - Real FT and phasing in F1.
     The displayed spectrum at the end is 512 by 1k real points
     results are (some figures date from version 1.0 !) :
        """
        import time
        dim(2)
        chsize(128, 128)
        one()
        sin(0.0, 'f12')
        revf('f1')
        revf('f2')
        chsize(512, 2048)
        itype(0)
        put('data')
        t = time.clock()
        for i in range(10):
            get('data')
            em(0.0, 1.0)
            revf('f2')
            rft('f2')
            phase(20.0, 20.0, 'f2')
            real('f2')
            bcorr(2, 2, 'f2', [10, 100, 300, 600, 900])
            sin(0.0, 'f1')
            chsize(get_si1_2d() * 2, get_si2_2d())
            rft('f1')
            phase(20.0, 20.0, 'f1')

        print('Total TIME:', time.clock() - t)
        print(' ')
        print('Typical results are :')
        print('=====================')
        print(' 7.00"   - G4 1.68 MHz - Mac Os 10.4 (PowerBook)')
        print(' 3.00"   - macintel mono core - Mac Os 10.4 (MacMini)')
        print(' 2.80"   - PIV 2.8 GHz hyperthreading - Linux')
        print(' 2.45"   - AMD 64  Opteron 2.2 GHz - Linux')
        print(' 1.52"   - Core 2 duo 2.8 GHz - Mac Os 10.5 (powerbook)')
        print(' 0.81"   - Xeon 5570 2.66GHz - Mac Os 10.6 (MacPro)')

    def test_basic(self):
        """test the basic NPK mechanisms
        """
        dim(2)
        ok = get_dim() == 2
        dim(1)
        ok = ok and get_dim() == 1
        self.report_result(ok, 'Basic context settings')

    def test_cache(self):
        """test the cache sub-system
        """
        self.report_result(1, 'dedans')
        t11 = 1000
        t12 = 248
        t22 = 1000
        t13 = 40
        t23 = 120
        t33 = 80
        total = 8 * pow(t11 - 1, 2) + 4096
        total = total + 16 * pow(t12 - 1, 2) * pow(t22 - 1, 2) + 4096
        total = total + 32 * pow(t13 - 1, 2) * pow(t23 - 1, 2) * pow(t33 - 1, 2) + 4096
        total = total + 4 * pow(t13 - 1, 2) * pow(t23 - 1, 2) * pow(t33 - 1, 2) + 4096
        total = total / 1024
        file1 = tempfile.mktemp('.gifatemp')
        file2 = tempfile.mktemp('.gifatemp')
        file3 = tempfile.mktemp('.gifatemp')
        file4 = tempfile.mktemp('.gifatemp')
        file5 = tempfile.mktemp('.gifatemp')
        file6 = tempfile.mktemp('.gifatemp')
        file7 = tempfile.mktemp('.gifatemp')
        file8 = tempfile.mktemp('.gifatemp')
        dim(1)
        chsize(t11)
        one()
        mult(100)
        sin(0)
        writec(file1)
        dim(2)
        chsize(t12, t22)
        one()
        mult(1000)
        sin(0, 'f12')
        writec(file2)
        dim(3)
        chsize(t13, t23, t33)
        one()
        mult(10000)
        sin(0, 'f123')
        writec(file3)
        self.report_result(1, 'Write')
        dim(1)
        chsize(512)
        zero()
        read(file1)
        com_max()
        ok = get_si1_1d() == t11 and math.fabs(geta_max(1) - 100) < 1 and math.fabs(geta_max(2)) < 1
        print(ok)
        dim(2)
        chsize(100, 100)
        zero()
        read(file2)
        com_max()
        ok = ok and get_si1_2d() * get_si2_2d() == t12 * t22 and math.fabs(geta_max(1)) - 1000 < 1 and math.fabs(geta_max(2)) < 1
        print(ok)
        dim(3)
        chsize(10, 10, 10)
        zero()
        read(file3)
        com_max()
        ok = ok and get_si1_3d() * get_si2_3d() * get_si3_3d() == t13 * t23 * t33
        print(ok)
        ok = ok and math.fabs(geta_max(1) - 10000) < 1 and math.fabs(geta_max(2)) < 1
        print(geta_max(1))
        print(geta_max(2))
        self.report_result(ok, 'Read')
        join(file3)
        join(file1)
        join(file2)
        print('listfilec() yet to be done')
        pi_2 = 2 * math.atan(1)
        join(file1)
        td = 2 * int(t11 / 4) + 1
        tf = t11 - 10
        test = 100 * math.cos(pi_2 * tf / t11)
        dim(1)
        getc(td, tf)
        ok = get_si1_1d() == tf - td + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 70.71) < 1 and math.fabs(geta_max(2) - test) < 1
        self.report_result(ok, 'Getc 1d - 1d')
        okok = ok
        join(file2)
        td = 1
        tf = t12
        test = 1000 * math.cos(pi_2 * tf / t12)
        dim(1)
        getc('f1', 1, td, tf)
        ok = get_si1_1d() == tf - td + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 1000) < 1 and math.fabs(geta_max(2) - test) < 1
        td = 2 * int(t22 / 4) + 1
        tf = t22 - 10
        test = 707.1 * math.cos(pi_2 * tf / t22)
        getc('f2', t12 / 2, td, tf)
        ok = ok and get_si1_1d() == tf - td + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 500) < 10 and math.fabs(geta_max(2) - test) < 10
        report_result(ok, 'Getc 2d - 1d')
        okok = okok and ok
        join(file3)
        td = 1
        tf = t13
        test = 10000 * math.cos(pi_2 * tf / t13)
        dim(1)
        getc('f1', 1, 1, td, tf)
        ok = get_si1_1d() == tf - td + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 10000) < 1 and math.fabs(geta_max(2) - test) < 1
        td = 2 * int(t23 / 4) + 1
        tf = t23 - 10
        test = 7071 * math.cos(pi_2 * tf / t23)
        getc('f2', t13 / 2, 1, td, tf)
        ok = ok and get_si1_1d() == tf - td + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 5000) < 100 and math.fabs(geta_max(2) - test) < 100
        td = 2 * int(t33 / 4) + 1
        tf = t33 - 10
        test = 5000 * math.cos(pi_2 * tf / t33)
        getc('f3', t13 / 2, t23 / 2, td, tf)
        ok = ok and get_si1_1d() == tf - td + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 3535.4999999999995) < 100 and math.fabs(geta_max(2) - test) < 100
        self.report_result(ok, 'Getc 3d - 1d')
        okok = okok and ok
        join(file2)
        td1 = 2 * int(t12 / 4) + 1
        tf1 = t12 - 10
        td2 = 2 * int(t22 / 4) + 1
        tf2 = t22 - 10
        test = 1000 * math.cos(pi_2 * tf1 / t12) * math.cos(pi_2 * tf2 / t22)
        dim(2)
        getc(td1, td2, tf1, tf2)
        ok = get_si1_2d() == tf1 - td1 + 1 and get_si2_2d() == tf2 - td2 + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 500) < 10 and math.fabs(geta_max(2) - test) < 10
        self.report_result(ok, 'Getc 2d - 2d')
        okok = okok and ok
        join(file3)
        td1 = 1
        tf1 = t23
        td2 = 1
        tf2 = t33
        test = 10000 * math.cos(pi_2 * tf1 / t23) * math.cos(pi_2 * tf2 / t33)
        dim(2)
        getc('f1', 1, td1, td2, tf1, tf2)
        ok = get_si1_2d() == tf1 - td1 + 1 and get_si2_2d() == tf2 - td2 + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 10000) < 1 and math.fabs(geta_max(2) - test) < 1
        td1 = 2 * int(t13 / 4) + 1
        tf1 = t13 - 10
        td2 = 2 * int(t33 / 4) + 1
        tf2 = t33 - 10
        test = 10000 * math.cos(pi_2 * tf1 / t13) * math.cos(pi_2 * tf2 / t33)
        dim(2)
        getc('f2', 1, td1, td2, tf1, tf2)
        ok = ok and get_si1_2d() == tf1 - td1 + 1 and get_si2_2d() == tf2 - td2 + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 5000) < 200 and math.fabs(geta_max(2) - test) < 100
        td1 = 2 * int(t13 / 4) + 1
        tf1 = t13 - 10
        td2 = 2 * int(t23 / 4) + 1
        tf2 = t23 - 10
        test = 7071 * math.cos(pi_2 * tf1 / t13) * math.cos(pi_2 * tf2 / t23)
        dim(2)
        getc('f3', t33 / 2, td1, td2, tf1, tf2)
        ok = ok and get_si1_2d() == tf1 - td1 + 1 and get_si2_2d() == tf2 - td2 + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 3535.4999999999995) < 100 and math.fabs(geta_max(2) - test) < 100
        self.report_result(ok, 'Getc 3d - 2d')
        okok = okok and ok
        join(file3)
        td1 = 2 * int(t13 / 4) + 1
        tf1 = t13 - 10
        td2 = 2 * int(t23 / 4) + 1
        tf2 = t23 - 10
        td3 = 2 * int(t33 / 4) + 1
        tf3 = t33 - 10
        test = 10000 * math.cos(pi_2 * tf1 / t13) * math.cos(pi_2 * tf2 / t23) * math.cos(pi_2 * tf3 / t33)
        dim(3)
        getc(td1, td2, td3, tf1, tf2, tf3)
        ok = get_si1_3d() == tf1 - td1 + 1 and get_si2_3d() == tf2 - td2 + 1 and get_si3_3d() == tf3 - td3 + 1
        com_max()
        ok = ok and math.fabs(geta_max(1) - 3535.4999999999995) < 200 and math.fabs(geta_max(2) - test) < 100
        report_result(ok, 'Getc 3d - 3d')
        okok = okok and ok
        self.report_result(okok, 'Getc')
        dim(1)
        chsize(t11)
        zero()
        writec(file4)
        dim(2)
        chsize(t12, t22)
        zero()
        writec(file5)
        dim(3)
        chsize(t13, t23, t33)
        zero()
        writec(file6)
        join(file4)
        td = 1
        tf = t11 / 2
        dim(1)
        chsize(tf)
        one()
        putc(td, tf)
        zero()
        getc(td, t11)
        com_max()
        ok = geta_max(1) == 1.0 and math.fabs(geta_max(2)) < 1e-06
        getc(tf + 1, t11)
        com_max()
        ok = ok and math.fabs(geta_max(1)) < 1e-06 and math.fabs(geta_max(2)) < 1e-06
        self.report_result(ok, 'Putc 1d - 1d')
        okok = ok
        join(file5)
        td = 1
        tf = t12 / 2
        dim(1)
        chsize(tf)
        one()
        putc('f1', 1, td, tf)
        zero()
        getc('f1', 1, td, t12)
        com_max()
        ok = geta_max(1) == 1.0 and math.fabs(geta_max(2) < 1e-06)
        getc('f1', 1, tf + 1, t12)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        td = 1
        tf = t22 / 2
        dim(1)
        chsize(tf)
        one()
        putc('f2', t12 / 2 + 1, td, tf)
        zero()
        getc('f2', t12 / 2 + 1, td, t22)
        com_max()
        ok = ok and geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc('f2', t12 / 2 + 1, tf + 1, t22)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        self.report_result(ok, 'Putc 2d - 1d')
        okok = okok and ok
        join(file6)
        td = 1
        tf = t13 / 2
        dim(1)
        chsize(tf)
        one()
        putc('f1', 1, 1, td, tf)
        zero()
        getc('f1', 1, 1, td, t13)
        com_max()
        ok = geta_max(1) == 1.0 and math.fabs(geta_max(2)) < 1e-06
        getc('f1', 1, 1, tf + 1, t13)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        td = 1
        tf = t23 / 2
        dim(1)
        chsize(tf)
        one()
        putc('f2', 1, t13 / 2 + 1, td, tf)
        zero()
        getc('f2', 1, t13 / 2 + 1, td, t23)
        com_max()
        ok = ok and geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc('f2', 1, t13 / 2 + 1, tf + 1, t23)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        td = 1
        tf = t33 / 2
        dim(1)
        chsize(tf)
        one()
        putc('f3', t13 / 2 + 1, t23 / 2 + 1, td, tf)
        zero()
        getc('f3', t13 / 2 + 1, t23 / 2 + 1, td, t33)
        com_max()
        ok = ok and geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc('f3', t13 / 2 + 1, t23 / 2 + 1, tf + 1, t33)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        self.report_result(ok, 'Putc 3d - 1d')
        okok = okok and ok
        join(file5)
        td1 = 1
        tf1 = t12 / 2
        td2 = 1
        tf2 = t22 / 2
        dim(2)
        chsize(tf1, tf2)
        one()
        putc(td1, td2, tf1, tf2)
        zero()
        getc(td1, td2, t12, t22)
        com_max()
        ok = geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc(tf1 + 1, tf2 + 1, t12, t22)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        self.report_result(ok, 'Putc 2d - 2d')
        okok = okok and ok
        join(file6)
        td1 = 1
        tf1 = t23 / 2
        td2 = 1
        tf2 = t33 / 2
        dim(2)
        chsize(tf1, tf2)
        one()
        putc('f1', 1, td1, td2, tf1, tf2)
        zero()
        getc('f1', 1, td1, td2, t23, t33)
        com_max()
        ok = geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc('f1', 1, tf1 + 1, tf2 + 1, t23, t33)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        td1 = 1
        tf1 = t13 / 2
        td2 = 1
        tf2 = t33 / 2
        dim(2)
        chsize(tf1, tf2)
        one()
        putc('f2', t23 / 2 + 1, td1, td2, tf1, tf2)
        zero()
        getc('f2', t23 / 2 + 1, td1, td2, t13, t33)
        com_max()
        ok = ok and geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc('f2', t23 / 2 + 1, tf1 + 1, tf2 + 1, t13, t33)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        td1 = 1
        tf1 = t13 / 2
        td2 = 1
        tf2 = t23 / 2
        dim(2)
        chsize(tf1, tf2)
        one()
        putc('f3', t33 / 2 + 1, td1, td2, tf1, tf2)
        zero()
        getc('f3', t33 / 2 + 1, td1, td2, t13, t23)
        com_max()
        ok = ok and geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc('f3', t33 / 2 + 1, tf1 + 1, tf2 + 1, t13, t23)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        self.report_result(ok, 'Putc 3d - 2d')
        okok = okok and ok
        join(file6)
        td1 = 1
        tf1 = t13 / 2
        td2 = 1
        tf2 = t23 / 2
        td3 = 1
        tf3 = t33 / 2
        dim(3)
        chsize(tf1, tf2, tf3)
        one()
        putc(td1, td2, td3, tf1, tf2, tf3)
        zero()
        getc(td1, td2, td3, t13, t23, t33)
        com_max()
        ok = geta_max(1) == 1.0 and geta_max(2) < 1e-06
        getc(tf1 + 1, tf2 + 1, tf3 + 1, t13, t23, t33)
        com_max()
        ok = ok and geta_max(1) < 1e-06 and geta_max(2) < 1e-06
        self.report_result(ok, 'Putc 3d - 3d')
        okok = okok and ok
        report_result(okok, 'Putc')
        newfilec(file7, 10.1, 0, (
         t13 / 4, t23 / 4, t33 / 4), (0.1, 0.2, 0.3), (1.1, 1.2, 1.3), (2.1, 2.2, 2.3))
        disjoin()
        join(file7)
        ok = get_c_dim() == 3 and math.fabs(get_c_offsf1() - 0.1) < 1e-06 and math.fabs(get_c_offsf2() - 0.2) < 1e-06 and math.fabs(get_c_offsf3() - 0.3) < 1e-06
        ok = ok and math.fabs(get_c_specwf1() - 1.1) < 1e-06 and math.fabs(get_c_specwf2() - 1.2) < 1e-06 and math.fabs(get_c_specwf3() - 1.3) < 1e-06
        ok = ok and math.fabs(get_c_freq1() - 2.1) < 1e-06 and math.fabs(get_c_freq2() - 2.2) < 1e-06 and math.fabs(get_c_freq3() - 2.3) < 1e-06
        ok = ok and get_c_sizef1() == t13 / 4 and get_c_sizef2() == t23 / 4 and get_c_sizef3() == t33 / 4
        ok = ok and get_c_type() == 0 and math.fabs(get_c_freq() - 10.1) < 1e-06
        dim(1)
        chsize(t23 / 4)
        for i in range(1, 1 + t13 / 4):
            for j in range(1, 1 + t33 / 4):
                one()
                mult(i + j)
                putc('f2', i, j, 1, t23 / 4)

        disjoin()
        join(file7)
        dim(2)
        getc('f2', t23 / 8, 1, 1, t13 / 4, t33 / 4)
        com_max()
        ok = geta_max(1) == t13 / 4 + t33 / 4 and geta_max(2) == 2
        disjoin()
        self.report_result(ok, 'newfilec')
        join(file4)
        disjoin()
        join(file5)
        disjoin()
        join(file6)
        disjoin()
        join(file1)
        disjoin()
        join(file2)
        disjoin()
        join(file3)
        disjoin()
        self.report_result(not get_c_joined(), 'Disjoin')
        print('proc3d yet to be done')
        proc3d(file7, file8, 'f1', 'chsize(get_si1_2d()/2,get_si2_2d()); mult(-1)', globals())
        join(file8)
        ok = get_c_sizef1() == t13 / 4 and get_c_sizef2() == t23 / 8 and get_c_sizef3() == t33 / 4
        getc('f2', t23 / 8, 1, 1, t13 / 4, t33 / 4)
        com_max()
        ok = ok and geta_max(2) == -(t13 / 4 + t33 / 4) and geta_max(1) == -2
        disjoin()
        self.report_result(ok, 'proc3d')
        join(file6)
        print(file6)
        putheader('Type', repr(12))
        ok = getheader('Dim') == '3'
        getheader('Type')
        ok = ok and getheader('Type') == '12'
        putheader('Coucou', 'You can even put string in there')
        print(getheader('Coucou'))
        ok = ok and getheader('Coucou') == 'You can even put string in there'
        putheader('2nd example', 'Parameters can be anything')
        ok = ok and getheader('2nd example') == 'Parameters can be anything'
        disjoin()
        join(file6)
        ok = ok and getheader('Type') == '12'
        disjoin()
        self.report_result(ok, 'Getheader, Putheader')
        print('addc() yet to be done')

    def test_dataset(self):
        if get_c_joined() == 0:
            print('No currently JOINed file')
        else:
            print('Currently JOINed file :')
            print('Filename       = ' + repr(get_c_name()))
            print('Dim            = ' + repr(get_c_dim()))
            print('Size f1        = ' + repr(get_c_sizef1()))
            print('Size f2        = ' + repr(get_c_sizef2()))
            print('Size F3        = ' + repr(get_c_sizef3()))
            print('1H Frequency   = ' + repr(get_c_freq()))
            print('Freq f1        = ' + repr(get_c_freq1()))
            print('Freq f2        = ' + repr(get_c_freq2()))
            print('Freq F3        = ' + repr(get_c_freq3()))
            print('Specw f1       = ' + repr(get_c_specwf1()))
            print('Specw f2       = ' + repr(get_c_specwf2()))
            print('Specw F3       = ' + repr(get_c_specwf3()))
            print('OffF1          = ' + repr(get_c_offsf1()))
            print('OffF2          = ' + repr(get_c_offsf2()))
            print('OffF3          = ' + repr(get_c_offsf3()))
            print('Max. Abs.      = ' + repr(get_c_absmax()))

    def test_extb(self):
        dim(1)
        order(10)
        simu(1000, 512, 2, 1.0, 200, 1.0, 0.0, 1.0, 600, 1.0, 0.0, 0.0)
        dt2svd(512)
        svd2ar(2)
        ar2rt(2)
        rtclean(2)
        rtlist(2, 1, get_nrt())
        rtinv(2)
        rtlist(1, 1, get_nrt())
        rt2pk(512, 1, 0.0)
        pklist(1, get_npk1d())

    def test_extm(self):
        dim(1)
        order(10)
        simu(1000, 512, 2, 1.0, 200, 1.0, 0.0, 1.0, 600, 1.0, 0.0, 0.0)
        dt2svd(512)
        svd2ar(1)
        ar2rt(1)
        svd2ar(2)
        ar2rt(2)
        rtmatch(3)
        rtlist(3, 1, get_nrt())
        rt2pk(512, 2, 0.0)
        pklist(1, get_npk1d())

    def test_ft_base(self):
        f = 'hsqc_grad'
        try:
            read(f)
        except:
            print('** data/ directory is missing, test will not be executed **')

        com_max()
        self.report_result(get_dim() == 2 and get_si1_2d() == 256 and get_si2_2d() == 2048 and math.fabs(geta_max(1) - 45705) < 10.0, 'Loading of data')
        com_sin(0.2, 'f12')
        ft_sim()
        chsize(2 * get_si1_2d(), get_si2_2d())
        ft_sh_tppi()
        phase(119.2, -80.0, 'f2')
        com_max()
        self.report_result(math.fabs(geta_max(1) - 40154644.0) < 40.0, 'Basic Fourier Transform and phasing')
        real('f12')
        com_max()
        report_result(math.fabs(geta_max(1) - 39193776.0) < 40.0, 'Real')
        row(86)
        dim(1)
        extract(584, 922)
        com_max()
        a = math.fabs(geta_max(1) - 4283381.0) < 10.0
        dim(2)
        col(819)
        dim(1)
        com_max()
        report(math.fabs(geta_max(1) - 7945463.0) < 8.0 and a, 'dim , row, col, extract')
        dim(2)
        proj('f1', 's')
        dim(1)
        evaln(33, 142)
        com_max()
        report(math.fabs(geta_max(2) - 361132.4) < 4.0 and math.fabs(noise - 81255) < 1.0, 'proj evaln')
        writec('fit_test')

    def test_inout(self):
        dim(1)
        readv('data_test/hpf576hpresat2611af.fid/fid')
        com_max()
        self.report_result(geta_max(1) == 219632 and get_si1_1d() == 6848, 'ReadV 1D')
        dim(2)
        readv('data_test/hpf576hnoe1502611af.fid/fid')
        com_max()
        self.report_result(geta_max(1) == 111982 and get_si1_2d() == 768 and si2_2d == 3008, 'ReadV 2D')

    def test_maxentropy(self):
        """
    # This test should be considerably extended.
    # for the moment, only Inverse Laplace/Tabulated is tested
    # the minimum would be to add 2D FT Maxent
        """
        dim(1)
        itype(0)
        dmin(0.001)
        dmax(1)
        chsize(30)
        for i in range(30):
            setval(i + 1, 0.1 * math.exp(i + 0.3333333333333333))

        put('tab')
        ntrial = 4
        seed = 127
        for i in range(ntrial):
            chsize(15)
            one()
            mult(1000)
            tm(1, 1)
            chsize(30)
            reverse()
            chsize(40)
            tlaplace()
            ns = 0.001 * val1d(1)
            addnoise(ns, seed)
            seed = seed + 11
            noise(ns)
            algo(11)
            iter(200)
            miniter(4)
            ndisp(50)
            lambsp(4)
            invtlap(100)
            iter(1000)
            invtlapcont()
            a = get_iterdone() > 10 and get_iterdone() <= 1000 and get_chi2() < 3
            evaln(1, 100)
            a = a and get_shift() < 80.5 and get_noise() < 125 and val1d(68) > 330
            writec('test-r-%d.gs1' % i)

        self.report_result(a, 'Inverse Laplace Transform (tried %i time)' % ntrial)
        if not (a and get_chi2() < 5):
            print('iterdone =', get_iterdone(), '    CHI2 =', get_chi2(), '    SHIFT=', get_shift(), '     NOISE=', get_noise(), '   VAL(68)=', val1d(68))
            print('the Inverse Laplace Transform fails because of a convergence slower than normal')
            print('You can still use this module, but will have not optimal convergence speed')

    def test_memory(self):
        """check for dynamic memory size
        """
        l = (1, 4, 16, 64, 256, 1024, 4096, 16384)
        for i in l:
            dim(1)
            n = i * 1024
            chsize(n)
            self.report_result(1, '1D buffer size: ' + str(n))

        dim(1)
        chsize(1024)
        for i in l:
            dim(2)
            chsize(1024, i)
            self.report_result(1, '2D buffer size: 1024 x ' + str(i))

        dim(2)
        chsize(128, 128)
        for i in l:
            dim(3)
            chsize(32, 32, i)
            self.report_result(1, '3D buffer size: 32 x 32 x ' + str(i))

        dim(3)
        chsize(16, 16, 16)

    def test_pkhandle(self):
        """
    # testing PKSYM in 2D, unit Hertz and PPM (using SIMUN)
        """
        dim(2)
        specw(5283.0, 4230.0)
        freq(600.13, 600.13, 600.0)
        offset(500.0, 500.0)
        chsize(512, 1024)
        zero()
        unit('h')
        simun(1, 1.0, 3461, 999, 2.1, 1.5, 0.0, 0.0)
        simun(1, 1.0, 5000, 601, 2.1, 1.5, 0.0, 0.0)
        sin(0, 'f12')
        ft('f12')
        com_max()
        minimax(5000, geta_max(1) * 2)
        real('f12')
        zoom(0)
        peak(0)
        if get_npk2d() == 2:
            a = math.fabs(geta_pk2d_f1f(1) - 114) < 0.01
            b = math.fabs(geta_pk2d_f1f(2) - 39) < 0.01
            c = math.fabs(geta_pk2d_f2f(1) - 453) < 0.01
            d = math.fabs(geta_pk2d_f2f(2) - 501) < 0.01
            e = math.fabs(geta_pk2d_a(1) - 9228.83) < 1.0
            tt = a and b and c and d and e
        else:
            tt = 1 == 0
        self.report_result(tt, 'PEAK in 2D')
        pksym(1, 1.0)
        a = math.fabs(geta_pk2d_f1f(3) - 232.98) < 0.01
        b = math.fabs(geta_pk2d_f2f(3) - 155.804) < 0.01
        c = math.fabs(geta_pk2d_f1f(4) - 252.196) < 0.01
        d = math.fabs(geta_pk2d_f2f(4) + 31.536) < 0.01
        self.report_result(a and b and c and d, 'PKSYM 2D with option add')
        pkselect(1, 2, 3, 0)
        pksym(0, 1.0)
        a = npk2d == 2
        b = math.fabs(geta_pk2d_f1f(1) - 114) < 0.01
        c = math.fabs(geta_pk2d_f1f(2) - 232.98) < 0.01
        self.report_result(a and b and c, 'PKSELECT - PKSYM 2D with option remove')

    def report_result(self, t, msg):
        """report test message

        used by test suite
        """
        l = len(msg)
        l = max(1, 80 - l)
        if t:
            print('--- ', msg, '.' * (l - 4), ' Ok')
        else:
            print('--- ', msg, '.' * (l - 8), ' FAILED')

    def new_func(x):
        print(x)


if __name__ == '__main__':
    unittest.main()