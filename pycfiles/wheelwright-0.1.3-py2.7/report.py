# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/wheelwright/report.py
# Compiled at: 2012-01-15 21:18:56
"""Report generation methods."""
__author__ = 'Kris Andersen'
__email__ = 'kris@biciworks.com'
__copyright__ = 'Copyright © 2012 Kris Andersen'
__license__ = 'GPLv3'
import numpy as np, datetime, os
from rst2pdf.createpdf import RstToPdf
from ConfigParser import ConfigParser
import wheel, wheelwright, tm1

def pdf(code, tension, accuracy, kgf0, kgf1, figure, filename):
    """
    Write report as PDF file.

    :Parameters:
      - `code`: TM-1 spoke code index
      - `target`: Target tension [kgf]
      - `accuracy`: Target accuracy [0.0, 1.0]
      - `kgf0`: Tension for spoke set 0 [kgf]
      - `kgf1`: Tension for spoke set 1 [kgf]
      - `figure`: Path to spoke tension image filename
      - `filename`: Report output filename
    """
    timestamp = datetime.datetime.now().strftime('%B %d, %Y %I:%M %p')
    try:
        c = ConfigParser(allow_no_value=True)
        c.read(['wheelwright.cfg',
         os.path.expanduser('~') + '/wheelwright.cfg',
         os.path.expanduser('~') + '/.wheelwright'])
        header = c.get('Report', 'header')
    except:
        header = None

    report = '\nWheelwright Report\n==================\n\n.. figure:: %s\n    :align: center\n\n    Spoke tensions: Spokes that have achieved the correct target\n    tension for the rim are within the green region.\n\n    | **Spoke Type**: %s\n    | **Target Tension**: %.1f kgf\n    | **Target Accuracy**: %.0f%%\n\nSpoke Tensions\n--------------\n\n   +------------------------------------------+------------------------------------------+\n   | Left Spokes                              | Right Spokes                             |\n   +-------------------------+----------------+-------------------------+----------------+\n   | Number                  | Tension (kgf)  | Number                  | Tension (kgf)  |\n   +=========================+================+=========================+================+\n' % (figure, tm1.spoke_codes[code], tension, 100.0 * accuracy)
    n = 1
    for x, y in zip(kgf0, kgf1):
        report += '   |%25d|%16.1f|%25d|%16.1f|\n' % (n, x, n + 1, y)
        report += '   +-------------------------+----------------+-------------------------+----------------+\n'
        n += 2

    row = 'Average Tension (kgf)'
    report += '   |%25s|%16.1f|%25s|%16.1f|\n' % (row, np.mean(kgf0), row, np.mean(kgf1))
    report += '   +-------------------------+----------------+-------------------------+----------------+\n'
    row = 'Standard Deviation (kgf)'
    report += '   |%25s|%16.1f|%25s|%16.1f|\n' % (row, np.std(kgf0), row, np.std(kgf1))
    report += '   +-------------------------+----------------+-------------------------+----------------+\n\n'
    report += '.. footer:: Wheelwright %s | http://biciworks.com/wheelwright/ | %s\n' % (
     wheelwright.__version__, timestamp)
    if header:
        report += '.. header:: %s\n' % header
    RstToPdf(breakside='any', splittables=True).createPdf(text=report, output=filename)
    return