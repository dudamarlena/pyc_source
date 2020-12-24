# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/Algo/CS_transformations.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 6686 bytes
"""
Authors: Marc-André
Last modified: 2011/11/18.

adapted by Lionel on 2013-3-6.
Copyright (c) 2011 IGBMC. All rights reserved.
"""
from __future__ import print_function
import numpy as np
import numpy.fft as fft

class transformations(object):
    __doc__ = '\n    this class contains methods which are tools to generate transform and ttransform.\n    ttrans form data to image\n    trans from image to data.\n    '

    def __init__(self, size_image, size_mesure, sampling=None, debug=0):
        """
        size_image and size_mesure are sizes of x and s space
        all other fields are meant to be overloaded after creation
        
        direct transform refers to S => X  // image => Data transform
        """
        self.size_image = size_image
        self.size_mesure = size_mesure
        self.pre_ft = self.Id
        self.tpre_ft = self.Id
        self.post_ft = self.Id
        self.tpost_ft = self.Id
        self.ft = fft.ifft
        self.tft = fft.fft
        self.sampling = sampling
        self.debug = debug

    def report(self):
        """dumps content"""
        for i in dir(self):
            if not i.startswith('_'):
                print(i, getattr(self, i))

    def Id(self, x):
        return x

    def check(self):
        if self.debug:
            print('\nsize_image: %d - size_mesure: %d\nsampling %s\n' % (self.size_image, self.size_mesure, str(self.sampling)))
        if self.sampling is not None:
            assert len(self.sampling) == self.size_mesure
            assert max(self.sampling) <= self.size_image

    def zerofilling(self, x):
        xx = np.zeros((self.size_image), dtype=(x.dtype))
        xx[:len(x)] = x[:]
        x = xx
        return x

    def sample(self, x):
        """
        apply a sampling function - using self.sampling
        """
        return x[self.sampling]

    def tsample(self, x):
        """
        transpose of the sampling function
        """
        xx = np.zeros((self.size_image), dtype=(x.dtype))
        xx[self.sampling] = x
        return xx

    def transform(self, s):
        """
        transform to data.
        Passing from s (image) to x (data)
        pre_ft() : s->s
        ft()     : s->x - fft.ifft by default - should not change size
        post_ft() : x->x - typically : broadening, sampling, truncating, etc...
        """
        if self.debug:
            print('entering trans', s.shape, s.dtype)
        else:
            if self.pre_ft != self.Id:
                s = self.pre_ft(s)
                if self.debug:
                    print('trans pre_ft', s.shape, s.dtype)
            else:
                x = self.ft(s)
                if self.post_ft != self.Id:
                    x = self.post_ft(x)
                    if self.debug:
                        print('trans post_ft', x.shape, x.dtype)
                if self.sampling is not None:
                    x = self.sample(x)
                    if self.debug:
                        print('trans sample', x.shape, x.dtype)
            if self.size_mesure != len(x):
                x = x[0:self.size_mesure]
                if self.debug:
                    print('trans trunc', x.shape, x.dtype)
        if self.debug:
            print('exiting trans', x.shape, x.dtype)
        return x

    def ttransform(self, x):
        """
        the transpose of transform
        Passing from x to s (data to image)
        """
        if self.debug:
            print('entering ttrans', x.shape, x.dtype)
        elif self.sampling is not None:
            if self.debug:
                print('ttrans sample')
            x = self.tsample(x)
        else:
            if self.size_image != len(x):
                if self.debug:
                    print('ttrans zerofill', len(x), self.size_image)
                x = self.zerofilling(x)
        if self.tpost_ft != self.Id:
            if self.debug:
                print('ttrans tpost_ft')
            x = self.tpost_ft(x)
        s = self.tft(x)
        if self.tpre_ft != self.Id:
            if self.debug:
                print('ttrans tpre_ft')
            s = self.tpre_ft(s)
        if self.debug:
            print('exiting ttrans', s.shape, s.dtype)
        return s


def sampling_load(addr_sampling_file):
    """
    Loads a sampling protocole from a list of indices stored in a file named addr_sampling_file
    returns an nparray with the sampling scheme.
    
    i.e. if b is a full dataset, b[sampling] is the sampled one
    """
    with open(addr_sampling_file, 'r') as (F):
        param = read_param(F)
        F.seek(0)
        sampling = read_data(F)
    return (sampling, param)


def read_data(F):
    """
    Reads data from the sampling file, used by sampling_load()
    """
    data = []
    for l in F:
        if not l.startswith('#'):
            if l.strip() == '':
                continue
            data.append(int(l))

    return np.array(data)


def read_param(F):
    """
    Reads the sampling parameters. used by sampling_load()
    """
    dic = {}
    for l in F:
        if not l.startswith('#'):
            break
        v = l.rstrip().split(':')
        if len(v) < 2:
            continue
        entry = v[0][1:].strip()
        dic[entry] = v[1].lstrip()

    return dic


if __name__ == '__main__':
    tr = transformations(2000, 1000)
    tr.report()