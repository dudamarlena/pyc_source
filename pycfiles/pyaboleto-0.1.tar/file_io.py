# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyabm\file_io.py
# Compiled at: 2013-02-01 18:05:57
__doc__ = '\nContains functions to input and output data to various formats. Also attempts \nto load GDAL to handle geospatial data, logging a warning if GDAL is not \navailable.\n'
import sys, logging
logger = logging.getLogger(__name__)
from pyabm import rc_params
rcParams = rc_params.get_params()
try:
    from .file_io_ogr import *
except ImportError:
    logger.warning('Failed to load GDAL/OGR. Cannot process spatial data.')

def write_point_process(nodes, outputFile):
    """Writes input node instances to a text file in R point-process format."""
    ofile = open(outputFile, 'w')
    xvals = []
    yvals = []
    for node in list(nodes.values()):
        xvals.append(node.getX())
        yvals.append(node.getY())

    xl = min(xvals)
    xu = max(xvals)
    yl = min(yvals)
    yu = max(yvals)
    ofile.write(str(len(nodes)))
    ofile.write('\n***R spatial point process***\n' % vars())
    ofile.write('%(xl).11e %(xu).11e %(yl).11e %(yu).11e 1\n' % vars())
    for x, y in zip(xvals, yvals):
        ofile.write('%(x).11e %(y).11e\n' % vars())

    ofile.close()
    return 0