# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/test.py
# Compiled at: 2016-11-29 20:56:28
import h5py
from data_provider import VolumeDataProvider
import time
from vector import Vec3d
if __name__ == '__main__':
    dspec_path = 'test_spec/pinky.spec'
    net_spec = dict(input=(1, 208, 208), label=(1, 100, 100))
    params = dict()
    params['drange'] = [0, 1, 2, 3, 4]
    params['dprior'] = None
    params['border'] = None
    params['augment'] = [dict(type='flip')]
    dp = VolumeDataProvider(dspec_path, net_spec, params)
    sample = dp.random_sample()
    print 'Save as file...'
    f = h5py.File('sample.h5')
    for name, data in sample.iteritems():
        f.create_dataset('/' + name, data=data)

    f.close()