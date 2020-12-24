# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/processes/examples/example_process.py
# Compiled at: 2020-03-23 15:53:29
# Size of source mod 2**32: 567 bytes
"""Example process file."""

def execute(mp):
    """
    Example process for testing.

    Inputs
    ------
    file1
        raster file

    Parameters
    ----------

    Output
    ------
    np.ndarray
    """
    with mp.open('file1') as (raster_file):
        if raster_file.is_empty():
            return 'empty'
        dem = raster_file.read(resampling='bilinear')
    return dem