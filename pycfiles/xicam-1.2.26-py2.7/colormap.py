# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\colormap.py
# Compiled at: 2018-08-27 17:21:07
import numpy as np
Gray = np.arange(255)
Red = np.round(255.0 * (np.sin(2.0 * Gray * np.pi / 255.0) + 1.0) / 2.0)
Green = np.round(255.0 * (np.sin(2.0 * Gray * np.pi / 255.0 - np.pi / 2.0) + 1.0) / 2.0)
Blue = np.round(255.0 * (np.sin(2.0 * Gray * np.pi / 255.0 - np.pi) + 1.0) / 2.0)
LUT = np.array([Red, Green, Blue]).T