# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/grid/structured_quad/faces.py
# Compiled at: 2015-02-11 19:25:27
from . import links

def number_of_faces(shape):
    """Number of faces in a structured quad grid.

    Parameters
    ----------
    shape : tuple of int
        Shape of grid of nodes.

    Returns
    -------
    int :
        Number of faces in grid.

    Examples
    --------
    >>> from landlab.grid.structured_quad.faces import number_of_faces
    >>> number_of_faces((3, 4))
    17
    """
    return links.number_of_links(shape)