# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/plot/save2file.py
# Compiled at: 2017-09-15 02:12:02
from __future__ import division, print_function, absolute_import
from builtins import range
import sys, scipyplot.log as log, matplotlib.pyplot as plt

def save2file(nameFile, fig=plt.gcf(), fileFormat='pdf', verbosity=1, indent=0, dpi=100):
    """

    :param fig:
    :param nameFile:
    :param fileFormat:
    :param verbosity:
    :param indent:
    :param dpi:
    :return:
    """
    fullNameFile = nameFile + '.' + fileFormat
    log.cnd_msg(verbosity, 0, 'Saving to file: ' + fullNameFile, indent_depth=indent)
    try:
        fig.savefig(fullNameFile, dpi=dpi, bbox_inches='tight', pad_inches=0)
        status = 0
    except:
        log.cnd_warning(verbosity, 1, str(sys.exc_info()[0]))
        status = -1

    log.cnd_status(verbosity, 0, status)