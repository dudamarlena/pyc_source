# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/contrib/quick_plot.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 145 bytes
import pandas as pd
import matplotlib.pyplot as plt

def quick_plot(fname):
    df = pd.read_csv(fname)
    plt.plot(df.objective)
    plt.show()