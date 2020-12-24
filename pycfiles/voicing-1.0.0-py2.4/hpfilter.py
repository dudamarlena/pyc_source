# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/voicing/hpfilter.py
# Compiled at: 2008-02-23 19:39:13
import gpkimgclass, sys, os
sys.path.insert(0, os.environ['OXIVOICE'])
import voice_misc
if __name__ == '__main__':
    cutoff_freq = float(sys.argv[1])
    assert cutoff_freq > 0
    d = gpkimgclass.read(sys.argv[2])
    print 'shape=', d.d.shape
    filtered = voice_misc.hipass_sym_butterworth(d.d[:, 0], cutoff_freq * d.dt(), order=4)
    gpkimgclass.gpk_img(d.hdr, filtered).write(sys.argv[3])