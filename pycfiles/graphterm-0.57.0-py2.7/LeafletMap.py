# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/notebooks/LeafletMap.py
# Compiled at: 2014-06-15 00:23:47
"""
LeafletMap.py
"""
import numpy as np
lon = np.arange(240, 360.0, 10.0)
lat = 40 + 10 * np.sin(lon / 10)
plot(lon, lat)
import mplleaflet
html = mplleaflet.fig_to_html()
import gterm
iframe_html = gterm.iframe_html(html=html, width='80%')
gterm.write_pagelet(iframe_html)