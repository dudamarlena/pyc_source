# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyStatsBatteries/Test.py
# Compiled at: 2020-02-04 11:01:33
# Size of source mod 2**32: 335 bytes
from PyStatsBatteries.Descriptors import *
from PyStatsBatteries.Management import *
import pandas as pd
import matplotlib.pyplot as plt
X = pd.read_csv('/home/marc/Bureau/Capacity_Analysis/Mehdi/Tableau_Moyenne.csv', sep=',')
d = Descriptors()
m = Management()
d.Scatterplot(X, 'CC/solid', 'AM')