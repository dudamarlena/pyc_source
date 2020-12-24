# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alonso/Science/Codes/ReformCodes/NaMaster/test/test_nmt_utils.py
# Compiled at: 2019-12-25 17:21:57
# Size of source mod 2**32: 16424 bytes
import unittest, numpy as np, pymaster as nmt, healpy as hp

class TestUtilsSynfastFsk(unittest.TestCase):

    def setUp(self):
        self.nx = 141
        self.ny = 311
        self.lx = np.radians(1.0)
        self.ly = np.radians(1.0)
        self.nbpw = 30
        self.lmax = np.sqrt((self.nx * np.pi / self.lx) ** 2 + (self.ny * np.pi / self.ly) ** 2)
        self.lpivot = self.lmax / 6.0
        self.alpha_pivot = 1.0
        self.larr = np.arange(int(self.lmax) + 1)
        self.cltt = (2 * self.lpivot / (self.larr + self.lpivot)) ** self.alpha_pivot
        self.clee = self.cltt.copy()
        self.clbb = self.cltt.copy()
        self.clte = np.zeros_like(self.cltt)
        self.cleb = np.zeros_like(self.cltt)
        self.cltb = np.zeros_like(self.cltt)
        self.cl1 = np.array([self.cltt])
        self.cl2 = np.array([self.clee, self.cleb,
         self.clbb])
        self.cl12 = np.array([self.cltt, self.clte, self.cltb,
         self.clee, self.cleb,
         self.clbb])
        self.cl22 = np.array([self.clee, self.cleb, self.cleb, self.cleb,
         self.clbb, self.cleb, self.cleb,
         self.clee, self.cleb,
         self.clbb])
        self.beam = np.ones_like(self.cltt)

    def anafast(self, mps):
        if mps.ndim == 2:
            scalar_input = True
        else:
            scalar_input = False
        k_x = np.fft.rfftfreq(self.nx, self.lx / (2 * np.pi * self.nx))
        k_y = np.fft.fftfreq(self.ny, self.ly / (2 * np.pi * self.ny))
        k_mod = np.sqrt(k_x[None, :] ** 2 + k_y[:, None] ** 2)
        dkvol = (2 * np.pi) ** 2 / (self.lx * self.ly)
        fft_norm = self.lx * self.ly / (2 * np.pi * self.nx * self.ny)
        krange = [
         0, np.amax(k_mod)]
        kbins = max(self.nx, self.ny) // 8
        nk, bk = np.histogram((k_mod.flatten()), range=krange, bins=kbins)
        kk, bk = np.histogram((k_mod.flatten()), range=krange, bins=kbins,
          weights=(k_mod.flatten()))
        kmean = kk / nk

        def compute_cl_single(alm1, alm2):
            almabs2 = (np.real(alm1) * np.real(alm2) + np.imag(alm1) * np.imag(alm2)).flatten()
            pk, bk = np.histogram((k_mod.flatten()), range=krange, bins=kbins,
              weights=almabs2)
            return pk / nk

        if scalar_input:
            alms = np.fft.rfftn(mps) * fft_norm
            cls = compute_cl_single(alms, alms)
        else:
            alms_tqu = np.array([np.fft.rfftn(m) * fft_norm for m in mps])
            k_mod[(0, 0)] = 1e-16
            cosk = k_x[None, :] / k_mod
            cosk[(0, 0)] = 1.0
            sink = k_y[:, None] / k_mod
            sink[(0, 0)] = 0.0
            k_mod[(0, 0)] = 0
            cos2k = cosk ** 2 - sink ** 2
            sin2k = 2 * sink * cosk
            a_t = alms_tqu[0, :, :]
            a_e = cos2k * alms_tqu[1, :, :] - sin2k * alms_tqu[2, :, :]
            a_b = sin2k * alms_tqu[1, :, :] + cos2k * alms_tqu[2, :, :]
            cls = []
            cls.append(compute_cl_single(a_t, a_t))
            cls.append(compute_cl_single(a_e, a_e))
            cls.append(compute_cl_single(a_b, a_b))
            cls.append(compute_cl_single(a_t, a_e))
            cls.append(compute_cl_single(a_e, a_b))
            cls.append(compute_cl_single(a_t, a_b))
            cls = np.array(cls)
        return (kmean, nk, cls * dkvol)

    def test_synfast_flat_errors(self):
        with self.assertRaises(ValueError):
            nmt.synfast_flat((self.nx), (self.ny), (self.lx), (self.ly), (self.cl1),
              [1], beam=(self.beam), seed=1234)
        with self.assertRaises(ValueError):
            nmt.synfast_flat((self.nx), (self.ny), (self.lx), (self.ly), (self.cl2),
              [0, 2], beam=(np.array([self.beam, self.beam])),
              seed=1234)
        with self.assertRaises(ValueError):
            nmt.synfast_flat((self.nx), (self.ny), (self.lx), (self.ly), (self.cl12),
              [0, 2], beam=(np.array([self.beam])),
              seed=1234)
        with self.assertRaises(ValueError):
            nmt.synfast_flat((self.nx), (self.ny), (self.lx), (self.ly), (self.cl12),
              [0, 2], beam=(np.array([self.beam[:15],
             self.beam[:15]])),
              seed=1234)
        with self.assertRaises(RuntimeError):
            nmt.synfast_flat((self.nx), (self.ny), (-self.lx), (self.ly), (self.cl2),
              [2], beam=(np.array([self.beam])),
              seed=1234)
        m = nmt.synfast_flat((self.nx), (self.ny), (self.lx), (self.ly), (self.cl12),
          [0, 2], beam=(np.array([self.beam, self.beam])),
          seed=1234)
        self.assertEqual(m.shape, (3, self.ny, self.nx))

    def test_synfast_flat_stats(self):
        m_t = nmt.synfast_flat((self.nx), (self.ny), (self.lx), (self.ly), (self.cl1),
          [0], beam=(np.array([self.beam])), seed=1234)[0]
        m_p1 = nmt.synfast_flat((self.nx), (self.ny), (self.lx), (self.ly), (self.cl12),
          [0, 2], beam=(np.array([self.beam, self.beam])),
          seed=1234)
        km, nk, ctt1 = self.anafast(m_t)
        km, nk, (ctt2, cee2, cbb2, cte2, ceb2, ctb2) = self.anafast(m_p1)
        lint = km.astype(int)

        def get_diff(c_d, c_t, c11, c22, c12, nmodes, facsig=5):
            diff = np.fabs(c_d - c_t[lint])
            sig = np.sqrt((c11[lint] * c22[lint] + c12[lint] ** 2) / nmodes)
            return diff < facsig * sig

        self.assertTrue(get_diff(ctt1, self.cltt, self.cltt, self.cltt, self.cltt, nk).all())
        self.assertTrue(get_diff(ctt2, self.cltt, self.cltt, self.cltt, self.cltt, nk).all())
        self.assertTrue(get_diff(cee2, self.clee, self.clee, self.clee, self.clee, nk).all())
        self.assertTrue(get_diff(cbb2, self.clbb, self.clbb, self.clbb, self.clbb, nk).all())
        self.assertTrue(get_diff(cte2, self.clte, self.cltt, self.clee, self.clte, nk).all())
        self.assertTrue(get_diff(ceb2, self.cleb, self.clbb, self.clee, self.cleb, nk).all())
        self.assertTrue(get_diff(ctb2, self.cltb, self.cltt, self.clbb, self.cltb, nk).all())


class TestUtilsSynfastSph(unittest.TestCase):

    def setUp(self):
        self.nside = 128
        self.lmax = 3 * self.nside - 1
        self.larr = np.arange(int(self.lmax + 1))
        self.lpivot = self.nside * 0.5
        self.alpha_pivot = 1.0
        self.cltt = (2 * self.lpivot / (self.larr + self.lpivot)) ** self.alpha_pivot
        self.clee = self.cltt.copy()
        self.clbb = self.cltt.copy()
        self.clte = np.zeros_like(self.cltt)
        self.cleb = np.zeros_like(self.cltt)
        self.cltb = np.zeros_like(self.cltt)
        self.cl1 = np.array([self.cltt])
        self.cl2 = np.array([self.clee, self.cleb,
         self.clbb])
        self.cl12 = np.array([self.cltt, self.clte, self.cltb,
         self.clee, self.cleb,
         self.clbb])
        self.cl22 = np.array([self.clee, self.cleb, self.cleb, self.cleb,
         self.clbb, self.cleb, self.cleb,
         self.clee, self.cleb,
         self.clbb])
        self.beam = np.ones_like(self.cltt)

    def anafast(self, mps):
        return hp.anafast(mps)

    def test_synfast_errors(self):
        with self.assertRaises(ValueError):
            nmt.synfast_spherical((self.nside), (self.cl1), [1], seed=1234)
        with self.assertRaises(ValueError):
            nmt.synfast_spherical((self.nside), (self.cl2), [0, 2], seed=1234)
        with self.assertRaises(ValueError):
            nmt.synfast_spherical((self.nside), (self.cl12), [0, 2], beam=(np.array([self.beam])),
              seed=1234)
        with self.assertRaises(ValueError):
            nmt.synfast_spherical((self.nside), (self.cl12), [0, 2], beam=(np.array([self.beam[:15],
             self.beam[:15]])),
              seed=1234)
        m = nmt.synfast_spherical((self.nside), (self.cl12), [0, 2], beam=(np.array([self.beam, self.beam])),
          seed=1234)
        self.assertEqual(m.shape, (3, hp.nside2npix(self.nside)))

    def test_synfast_stats(self):
        m_t = nmt.synfast_spherical((self.nside), (self.cl1), [0], beam=(np.array([self.beam])),
          seed=1234)
        m_p1 = nmt.synfast_spherical((self.nside), (self.cl12), [0, 2], beam=(np.array([self.beam, self.beam])),
          seed=1234)
        ctt1 = self.anafast(m_t)
        ctt2, cee2, cbb2, cte2, ceb2, ctb2 = self.anafast(m_p1)

        def get_diff(c_d, c_t, c11, c22, c12, facsig=5):
            diff = np.fabs(c_d - c_t)
            sig = np.sqrt((c11 * c22 + c12 ** 2) / (2 * self.larr + 1.0))
            return diff < facsig * sig

        self.assertTrue(get_diff(ctt1, self.cltt, self.cltt, self.cltt, self.cltt).all())
        self.assertTrue(get_diff(ctt2, self.cltt, self.cltt, self.cltt, self.cltt).all())
        self.assertTrue(get_diff(cee2, self.clee, self.clee, self.clee, self.clee).all())
        self.assertTrue(get_diff(cbb2, self.clbb, self.clbb, self.clbb, self.clbb).all())
        self.assertTrue(get_diff(cte2, self.clte, self.cltt, self.clee, self.clte).all())
        self.assertTrue(get_diff(ceb2, self.cleb, self.clbb, self.clee, self.cleb).all())
        self.assertTrue(get_diff(ctb2, self.cltb, self.clbb, self.cltt, self.cltb).all())


class TestUtilsMaskSph(unittest.TestCase):

    def setUp(self):
        self.nside = 256
        self.th0 = np.pi / 4
        self.msk = np.zeros((hp.nside2npix(self.nside)), dtype=float)
        self.th, ph = hp.pix2ang(self.nside, np.arange((hp.nside2npix(self.nside)), dtype=int))
        self.msk[self.th < self.th0] = 1.0
        self.aposize = 2.0
        self.inv_x2thr = 1.0 / (1 - np.cos(np.radians(self.aposize)))

    def test_mask_errors(self):
        with self.assertRaises(RuntimeError):
            nmt.mask_apodization((self.msk[:13]), (self.aposize), apotype='C1')
        with self.assertRaises(RuntimeError):
            nmt.mask_apodization((self.msk), (-self.aposize), apotype='C1')
        with self.assertRaises(RuntimeError):
            nmt.mask_apodization((self.msk), (self.aposize), apotype='C3')

    def test_mask_c1(self):
        msk_apo = nmt.mask_apodization((self.msk), (self.aposize), apotype='C1')
        self.assertTrue((msk_apo[(self.th > self.th0)] < 1e-10).all())
        self.assertTrue((np.fabs(msk_apo[(self.th < self.th0 - np.radians(self.aposize))] - 1.0) < 1e-10).all())
        x = np.sqrt((1 - np.cos(self.th - self.th0)) * self.inv_x2thr)
        f = x - np.sin(x * 2 * np.pi) / (2 * np.pi)
        ind_transition = (self.th < self.th0) & (self.th > self.th0 - np.radians(self.aposize))
        self.assertTrue((np.fabs(msk_apo[ind_transition] - f[ind_transition]) < 0.02).all())

    def test_mask_c2(self):
        msk_apo = nmt.mask_apodization((self.msk), (self.aposize), apotype='C2')
        self.assertTrue((msk_apo[(self.th > self.th0)] < 1e-10).all())
        self.assertTrue((np.fabs(msk_apo[(self.th < self.th0 - np.radians(self.aposize))] - 1.0) < 1e-10).all())
        x = np.sqrt((1 - np.cos(self.th - self.th0)) * self.inv_x2thr)
        f = 0.5 * (1 - np.cos(x * np.pi))
        ind_transition = (self.th < self.th0) & (self.th > self.th0 - np.radians(self.aposize))
        self.assertTrue((np.fabs(msk_apo[ind_transition] - f[ind_transition]) < 0.02).all())


class TestUtilsMaskFsk(unittest.TestCase):

    def setUp(self):
        self.nx = self.ny = 200
        self.lx = self.ly = np.radians(10.0)
        self.msk = np.zeros([self.ny, self.nx])
        self.msk[:self.ny // 2, :] = 1.0
        self.aposize = 1.0
        self.inv_xthr = 1.0 / np.radians(self.aposize)
        self.ioff = self.ny // 2 - int(np.radians(self.aposize) / (self.ly / self.ny))

    def test_mask_flat_errors(self):
        with self.assertRaises(ValueError):
            nmt.mask_apodization_flat((self.msk[0]), (self.lx), (self.ly),
              (self.aposize), apotype='C1')
        with self.assertRaises(RuntimeError):
            nmt.mask_apodization_flat((self.msk), (self.lx), (self.ly), (-self.aposize),
              apotype='C1')
        with self.assertRaises(RuntimeError):
            nmt.mask_apodization_flat((self.msk), (self.lx), (self.ly), (self.aposize),
              apotype='C3')

    def test_mask_flat_c1(self):
        msk_apo = nmt.mask_apodization_flat((self.msk), (self.lx), (self.ly), (self.aposize),
          apotype='C1')
        self.assertTrue((msk_apo[self.ny // 2:, :] < 1e-10).all())
        self.assertTrue((np.fabs(msk_apo[:self.ioff, :] - 1.0) < 1e-10).all())
        ind_transition = np.arange((self.ioff), (self.ny // 2), dtype=int)
        x = self.inv_xthr * np.fabs((self.ny / 2.0 - ind_transition) * self.ly / self.ny)
        f = x - np.sin(x * 2 * np.pi) / (2 * np.pi)
        self.assertTrue((np.fabs(msk_apo[ind_transition, :] - f[:, None]) < 1e-10).all())

    def test_mask_flat_c2(self):
        msk_apo = nmt.mask_apodization_flat((self.msk), (self.lx), (self.ly),
          (self.aposize), apotype='C2')
        self.assertTrue((msk_apo[self.ny // 2:, :] < 1e-10).all())
        self.assertTrue((np.fabs(msk_apo[:self.ioff, :] - 1.0) < 1e-10).all())
        ind_transition = np.arange((self.ioff), (self.ny // 2), dtype=int)
        x = self.inv_xthr * np.fabs((self.ny / 2.0 - ind_transition) * self.ly / self.ny)
        f = 0.5 * (1 - np.cos(x * np.pi))
        self.assertTrue((np.fabs(msk_apo[ind_transition, :] - f[:, None]) < 1e-10).all())


if __name__ == '__main__':
    unittest.main()