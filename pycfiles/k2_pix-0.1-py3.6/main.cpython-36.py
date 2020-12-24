# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/k2-pix/main.py
# Compiled at: 2017-12-13 13:34:59
# Size of source mod 2**32: 3596 bytes
""" Plot a K2 TPF and overlay a sky survey image."""
from __future__ import division, print_function, absolute_import
import argparse
from tpf import TargetPixelFile
from figure import K2Fig

def k2pix():
    """ Script to plot a K2 TPF and overlay a sky survey image."""
    parser = argparse.ArgumentParser(description="Plots a co-added Target Pixel File (TPF) from NASA's Kepler/K2/TESS with a survey image overlaid.")
    parser.add_argument('-v', '--verbose', action='store_true', help='')
    parser.add_argument('--output', metavar='FILENAME', type=str,
      default=None,
      help='.gif or .mp4 output filename (default: gif with the same name as the input file)')
    parser.add_argument('--survey', metavar='SURVEY', type=str,
      default=None,
      help='survey (available in skyview) to overlay on the K2 image.')
    parser.add_argument('--stretch', type=str, default='log', help='type of contrast stretching: "linear", "sqrt", "power", "log", or "asinh" (default is "log")')
    parser.add_argument('--min_percent', metavar='%', type=float, default=1.0, help='minimum cut percentile (default: 1.0)')
    parser.add_argument('--max_percent', metavar='%', type=float, default=95.0, help='maximum cut percentile (default: 95)')
    parser.add_argument('--cmap', type=str, default='gray',
      help='matplotlib color map name (default: gray)')
    parser.add_argument('--contour_color', type=str, default='red',
      help='matplotlib color name (default: red)')
    parser.add_argument('tpf_filename', nargs='+', help='path to one or more Target Pixel Files (TPF)')
    args = parser.parse_args(args)
    for fn in args.tpf_filename:
        try:
            tpf = TargetPixelFile(fn, verbose=(args.verbose))
            fig = K2Fig(tpf)
            fig.create_figure(output_filename=(args.output), stretch=(args.stretch),
              min_percent=(args.min_percent),
              max_percent=(args.max_percent),
              cmap=(args.cmap),
              contour_color=(args.contour_color))
        except Exception as e:
            if args.verbose:
                raise e
            else:
                print('ERROR: {}'.format(e))


if __name__ == '__main__':
    fn = 'https://archive.stsci.edu/missions/k2/target_pixel_files/c5/211900000/72000/ktwo211972478-c05_lpd-targ.fits.gz'
    tpf = TargetPixelFile(fn)
    fig = K2Fig(tpf)
    fig.create_figure('overplot.png', '2MASS-K')