# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/examples/stats0d/ex_hotellings_paired.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 350 bytes
import spm1d
dataset = spm1d.data.mv0d.hotellings_paired.NCSSBeforeAfter()
dataset = spm1d.data.mv0d.hotellings_paired.RSXLHotellingsPaired()
yA, yB = dataset.get_data()
print(dataset)
T2 = spm1d.stats.hotellings_paired(yA, yB)
T2i = T2.inference(alpha=0.05)
print(T2i)