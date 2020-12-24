# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/megdata/tests/test_ctfreaders.py
# Compiled at: 2018-10-24 06:01:48
# Size of source mod 2**32: 2001 bytes
import numpy as np
from os.path import join, abspath
from megdata.test import megdatatestpath, array_assert
from megdata.test.support import MEGDataTestBase
MEGDATATEST = megdatatestpath()
DATADIR = abspath(join(MEGDATATEST, 'naf', 'meg', 'ctfreaders'))

class TestCtfReader(MEGDataTestBase):

    def postSetUp(self):
        import h5py
        h = h5py.File(join(DATADIR, 'soft002data_03.testhdf5'), 'r')
        self.orig_data = h['testdata'][...]
        self.orig_data *= 1e-15
        self.orig_order = h['testdata'].attrs['chanorder']
        h.close()

    def test_ctf_data_load_slice(self):
        """Test that we load CTF data correctly by slice"""
        from megdata import CTFDataset
        c = CTFDataset.from_file(join(MEGDATATEST, 'ctfdata/SOFT002/08104_CrossSite_20101215_03.ds/08104_CrossSite_20101215_03.res4'))
        slices_per_epoch = c.res.no_samples
        scales = []
        for chan in c.res.channels:
            scales.append(1.0 / (chan.gain * chan.q_gain))

        scales = np.array(scales)
        for e in range(self.orig_data.shape[1]):
            start = e * slices_per_epoch
            end = start + 1000
            new_dat = c.read_raw_data(slices=(start, end), indices=c.meg_indices).T
            new_dat = new_dat * scales[(c.meg_indices, np.newaxis)]
            array_assert(new_dat, self.orig_data[:, e, :], decimal=8)