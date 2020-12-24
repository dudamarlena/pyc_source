# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Newville/Codes/wxmplot/examples/simple.py
# Compiled at: 2019-08-25 10:26:58
# Size of source mod 2**32: 200 bytes
import numpy as np
from wxmplot.interactive import plot, wxloop, autoloop
autoloop()
x = np.linspace(0.0, 20.0, 201)
plot(x, (np.sin(x) / (x + 1)), ylabel='response', xlabel='T (sec)')