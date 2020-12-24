# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/static/process_template.py
# Compiled at: 2019-05-17 05:49:30
# Size of source mod 2**32: 565 bytes
"""Mapchete process file template."""

def execute(mp):
    """
    Insert your python code here.

    Access input data specified in the .mapchete file:

    with mp.open("<input_id>") as src:
        data = src.read()

    For vector data a list of features is returned, for raster data a numpy
    array. Data is already reprojected.

    To write the process output simply return a feature list or numpy array:

    return modified_data

    Please note the returned data type has to match the output type specified
    in the .mapchete file.
    """
    pass