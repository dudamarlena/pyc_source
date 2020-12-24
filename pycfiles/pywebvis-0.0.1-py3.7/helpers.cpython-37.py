# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webvis/helpers.py
# Compiled at: 2019-11-05 21:15:15
# Size of source mod 2**32: 523 bytes
import multiprocessing.dummy as thr
try:
    import matplotlib.pyplot as plt
    import mpld3
except Exception as e:
    try:
        print(e)
    finally:
        e = None
        del e

try:
    import seaborn as sns
    sns.set()
except Exception as e:
    try:
        print(e)
    finally:
        e = None
        del e

def threaded(f, *args):
    p = thr.Process(target=f, args=args)
    p.start()
    return p


def get_mpl_html(value, config=None):
    fig, ax = plt.subplots()
    try:
        ax.plot(value)
    except Exception as e:
        try:
            return str(e)
        finally:
            e = None
            del e

    s = mpld3.fig_to_html(fig)
    plt.close(fig)
    return s