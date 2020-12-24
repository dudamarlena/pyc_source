# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/sleep/timeseries_brain_plot.py
# Compiled at: 2018-11-24 16:08:24
# Size of source mod 2**32: 2371 bytes
import numpy as np
from visbrain.gui import Brain
from visbrain.objects import TimeSeries3DObj, SourceObj
from visbrain.io import download_file
from Clumsy import get_sub_tal, TimeSeriesLF, rolling_window
__all__ = []
original = False
if original:
    s_xyz = np.load(download_file('xyz_sample.npz', astype='example_data'))['xyz']
    s_xyz = s_xyz[4::25, ...]
    s_text = [str(k) for k in range(s_xyz.shape[0])]
    s_textsize = 1.5
else:
    mp, bp, tal = get_sub_tal('R1207J', 'FR1', True)
    x = tal['atlases']['ind']['x']
    y = tal['atlases']['ind']['y']
    z = tal['atlases']['ind']['z']
    arr = np.vstack((x, y, z))
    choice = np.random.choice(np.arange(tal.shape[0]), 25)
    s_xyz = arr[choice]
    s_text = [str(k) for k in choice]
    s_textsize = 1.5
s_obj = SourceObj('MySources', s_xyz, symbol='disc', color='green')
sf = 100.0
n_time_points = 700
n_sources = s_xyz.shape[0]
time = np.mgrid[0:n_sources, 0:n_time_points][1] / sf
amp = np.random.randint(2, 20, n_sources).reshape(-1, 1)
pha = np.random.randint(1, 7, n_sources).reshape(-1, 1)
ts_data = amp * np.sin(2 * np.pi * pha * time)
ts_data += np.random.randn(n_sources, n_time_points)
ts_to_mask = [
 5, 7, 11, 3, 14, 17, 22, 23]
ts_select = np.ones((s_xyz.shape[0],), dtype=bool)
ts_select[ts_to_mask] = False
ts_amp = 5.4
ts_width = 15.7
ts_color = 'orange'
ts_dxyz = (1.0, 2.0, 5.0)
ts_lw = 2.2
ts = TimeSeries3DObj('Ts1', ts_data, s_xyz, select=ts_select, ts_amp=ts_amp, ts_width=ts_width,
  line_width=ts_lw,
  translate=ts_dxyz,
  color=ts_color)
vb = Brain(time_series_obj=ts, source_obj=s_obj)
vb.show()