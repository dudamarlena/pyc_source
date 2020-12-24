# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_converter.py
# Compiled at: 2018-12-13 08:22:07
import unittest, numpy as np
from tests.utils import load_data, get_index_of_function
from tests.materials import Nickel, Argon
from pystog.utils import RealSpaceHeaders, ReciprocalSpaceHeaders
from pystog.converter import Converter

class TestConverterUtilities(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.converter = Converter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_safe_divide(self):
        self.assertTrue(np.array_equal(self.converter._safe_divide(np.arange(10), np.arange(10)), [
         0, 1, 1, 1, 1, 1, 1, 1, 1, 1]))


class TestConverterRealSpaceBase(unittest.TestCase):
    rtol = 1e-05
    atol = 1e-08

    def initialize_material(self):
        self.kwargs = self.material.kwargs
        self.first = self.material.real_space_first
        self.last = self.material.real_space_last
        data = load_data(self.material.real_space_filename)
        self.r = data[:, get_index_of_function('r', RealSpaceHeaders)]
        self.gofr = data[:, get_index_of_function('g(r)', RealSpaceHeaders)]
        self.GofR = data[:, get_index_of_function('G(r)', RealSpaceHeaders)]
        self.GKofR = data[:, get_index_of_function('GK(r)', RealSpaceHeaders)]
        self.gofr_target = self.material.gofr_target
        self.GofR_target = self.material.GofR_target
        self.GKofR_target = self.material.GKofR_target

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.converter = Converter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def g_to_G(self):
        GofR = self.converter.g_to_G(self.r, self.gofr, **self.kwargs)
        self.assertTrue(np.allclose(GofR[self.first:self.last], self.GofR_target, rtol=self.rtol, atol=self.atol))

    def g_to_GK(self):
        GKofR = self.converter.g_to_GK(self.r, self.gofr, **self.kwargs)
        self.assertTrue(np.allclose(GKofR[self.first:self.last], self.GKofR_target, rtol=self.rtol, atol=self.atol))

    def G_to_g(self):
        gofr = self.converter.G_to_g(self.r, self.GofR, **self.kwargs)
        self.assertTrue(np.allclose(gofr[self.first:self.last], self.gofr_target, rtol=self.rtol, atol=self.atol))

    def G_to_GK(self):
        GKofR = self.converter.G_to_GK(self.r, self.GofR, **self.kwargs)
        self.assertTrue(np.allclose(GKofR[self.first:self.last], self.GKofR_target, rtol=self.rtol, atol=self.atol))

    def GK_to_g(self):
        gofr = self.converter.GK_to_g(self.r, self.GKofR, **self.kwargs)
        self.assertTrue(np.allclose(gofr[self.first:self.last], self.gofr_target, rtol=self.rtol, atol=self.atol))

    def GK_to_G(self):
        GofR = self.converter.GK_to_G(self.r, self.GKofR, **self.kwargs)
        self.assertTrue(np.allclose(GofR[self.first:self.last], self.GofR_target, rtol=self.rtol, atol=self.atol))


class TestConverterRealSpaceNickel(TestConverterRealSpaceBase):

    def setUp(self):
        super(TestConverterRealSpaceNickel, self).setUp()
        self.material = Nickel()
        self.initialize_material()

    def test_g_to_G(self):
        self.g_to_G()

    def test_g_to_GK(self):
        self.g_to_GK()

    def test_G_to_g(self):
        self.G_to_g()

    def test_G_to_GK(self):
        self.G_to_GK()

    def test_GK_to_g(self):
        self.GK_to_g()

    def test_GK_to_G(self):
        self.GK_to_G()


class TestConverterRealSpaceArgon(TestConverterRealSpaceBase):

    def setUp(self):
        super(TestConverterRealSpaceArgon, self).setUp()
        self.material = Argon()
        self.initialize_material()

    def test_g_to_G(self):
        self.g_to_G()

    def test_g_to_GK(self):
        self.g_to_GK()

    def test_G_to_g(self):
        self.G_to_g()

    def test_G_to_GK(self):
        self.G_to_GK()

    def test_GK_to_g(self):
        self.GK_to_g()

    def test_GK_to_G(self):
        self.GK_to_G()


class TestConverterReciprocalSpaceBase(unittest.TestCase):
    rtol = 1e-05
    atol = 1e-08

    def initialize_material(self):
        self.kwargs = self.material.kwargs
        self.first = self.material.reciprocal_space_first
        self.last = self.material.reciprocal_space_last
        data = load_data(self.material.reciprocal_space_filename)
        self.q = data[:, get_index_of_function('Q', ReciprocalSpaceHeaders)]
        self.sq = data[:,
         get_index_of_function('S(Q)', ReciprocalSpaceHeaders)]
        self.fq = data[:,
         get_index_of_function('Q[S(Q)-1]', ReciprocalSpaceHeaders)]
        self.fq_keen = data[:,
         get_index_of_function('FK(Q)', ReciprocalSpaceHeaders)]
        self.dcs = data[:,
         get_index_of_function('DCS(Q)', ReciprocalSpaceHeaders)]
        self.sq_target = self.material.sq_target
        self.fq_target = self.material.fq_target
        self.fq_keen_target = self.material.fq_keen_target
        self.dcs_target = self.material.dcs_target

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.converter = Converter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def S_to_F(self):
        fq = self.converter.S_to_F(self.q, self.sq, **self.kwargs)
        self.assertTrue(np.allclose(fq[self.first:self.last], self.fq_target, rtol=self.rtol, atol=self.atol))

    def S_to_FK(self):
        fq_keen = self.converter.S_to_FK(self.q, self.sq, **self.kwargs)
        self.assertTrue(np.allclose(fq_keen[self.first:self.last], self.fq_keen_target, rtol=self.rtol, atol=self.atol))

    def S_to_DCS(self):
        dcs = self.converter.S_to_DCS(self.q, self.sq, **self.kwargs)
        self.assertTrue(np.allclose(dcs[self.first:self.last], self.dcs_target, rtol=self.rtol, atol=self.atol))

    def F_to_S(self):
        sq = self.converter.F_to_S(self.q, self.fq, **self.kwargs)
        self.assertTrue(np.allclose(sq[self.first:self.last], self.sq_target, rtol=self.rtol, atol=self.atol))

    def F_to_FK(self):
        fq_keen = self.converter.F_to_FK(self.q, self.fq, **self.kwargs)
        self.assertTrue(np.allclose(fq_keen[self.first:self.last], self.fq_keen_target, rtol=self.rtol, atol=self.atol))

    def F_to_DCS(self):
        dcs = self.converter.F_to_DCS(self.q, self.fq, **self.kwargs)
        self.assertTrue(np.allclose(dcs[self.first:self.last], self.dcs_target, rtol=self.rtol, atol=self.atol))

    def FK_to_S(self):
        sq = self.converter.FK_to_S(self.q, self.fq_keen, **self.kwargs)
        self.assertTrue(np.allclose(sq[self.first:self.last], self.sq_target, rtol=self.rtol, atol=self.atol))

    def FK_to_F(self):
        fq = self.converter.FK_to_F(self.q, self.fq_keen, **self.kwargs)
        self.assertTrue(np.allclose(fq[self.first:self.last], self.fq_target, rtol=self.rtol, atol=self.atol))

    def FK_to_DCS(self):
        dcs = self.converter.FK_to_DCS(self.q, self.fq_keen, **self.kwargs)
        self.assertTrue(np.allclose(dcs[self.first:self.last], self.dcs_target, rtol=self.rtol, atol=self.atol))

    def DCS_to_S(self):
        sq = self.converter.DCS_to_S(self.q, self.dcs, **self.kwargs)
        self.assertTrue(np.allclose(sq[self.first:self.last], self.sq_target, rtol=self.rtol, atol=self.atol))

    def DCS_to_F(self):
        fq = self.converter.DCS_to_F(self.q, self.dcs, **self.kwargs)
        self.assertTrue(np.allclose(fq[self.first:self.last], self.fq_target, rtol=self.rtol, atol=self.atol))

    def DCS_to_FK(self):
        fq_keen = self.converter.DCS_to_FK(self.q, self.dcs, **self.kwargs)
        self.assertTrue(np.allclose(fq_keen[self.first:self.last], self.fq_keen_target, rtol=self.rtol, atol=self.atol))


class TestConverterReciprocalSpaceNickel(TestConverterReciprocalSpaceBase):

    def setUp(self):
        super(TestConverterReciprocalSpaceNickel, self).setUp()
        self.material = Nickel()
        self.initialize_material()

    def test_S_to_F(self):
        self.S_to_F()

    def test_S_to_FK(self):
        self.S_to_FK()

    def test_S_to_DCS(self):
        self.S_to_DCS()

    def test_F_to_S(self):
        self.F_to_S()

    def test_F_to_FK(self):
        self.F_to_FK()

    def test_F_to_DCS(self):
        self.F_to_DCS()

    def test_FK_to_S(self):
        self.FK_to_S()

    def test_FK_to_F(self):
        self.FK_to_F()

    def test_FK_to_DCS(self):
        self.FK_to_DCS()

    def test_DCS_to_S(self):
        self.DCS_to_S()

    def test_DCS_to_F(self):
        self.DCS_to_F()

    def test_DCS_to_FK(self):
        self.DCS_to_FK()


class TestConverterReciprocalSpaceArgon(TestConverterReciprocalSpaceBase):

    def setUp(self):
        super(TestConverterReciprocalSpaceArgon, self).setUp()
        self.material = Argon()
        self.initialize_material()

    def test_S_to_F(self):
        self.S_to_F()

    def test_S_to_FK(self):
        self.S_to_FK()

    def test_S_to_DCS(self):
        self.S_to_DCS()

    def test_F_to_S(self):
        self.F_to_S()

    def test_F_to_FK(self):
        self.F_to_FK()

    def test_F_to_DCS(self):
        self.F_to_DCS()

    def test_FK_to_S(self):
        self.FK_to_S()

    def test_FK_to_F(self):
        self.FK_to_F()

    def test_FK_to_DCS(self):
        self.FK_to_DCS()

    def test_DCS_to_S(self):
        self.DCS_to_S()

    def test_DCS_to_F(self):
        self.DCS_to_F()

    def test_DCS_to_FK(self):
        self.DCS_to_FK()


if __name__ == '__main__':
    unittest.main()