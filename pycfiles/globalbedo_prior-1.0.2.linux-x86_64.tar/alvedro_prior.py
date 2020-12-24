# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda/lib/python2.7/site-packages/globalbedo_prior/alvedro_prior.py
# Compiled at: 2014-03-24 07:56:27
"""alvedro_prior"""
import optparse, sys, os
from .GlobAlbedoPrior import GlobAlbedoPrior
__author__ = 'P Lewis & J Gomez-Dans (NCEO&UCL)'
__copyright__ = '(c) 2014'
__license__ = 'GPL'
__version__ = '1.0.2'
__maintainer__ = 'J Gomez-Dans'
__email__ = 'j.gomez-dans@ucl.ac.uk'
__status__ = 'Development'

def main():
    print '%s, version %s.\nJ Gomez-Dans (NCEO & UCL)' % (
     __doc__, __version__)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'])
    parser.add_option('-t', '--tile', action='store', dest='tile', type=str, help='Tile to process (e.g. h17v04)')
    parser.add_option('-d', '--datadir', action='store', dest='datadir', type=str, help='Root directory where data are stored')
    parser.add_option('-o', '--outputdir', action='store', dest='outdir', type=str, help='Output directory')
    options, args = parser.parse_args()
    ga = GlobAlbedoPrior(options.tile, options.datadir, options.outdir, bands=[1, 2, 3, 4, 5, 6, 7])
    ga.stage1_prior()
    ga.stage2_prior()


if __name__ == '__main__':
    main()