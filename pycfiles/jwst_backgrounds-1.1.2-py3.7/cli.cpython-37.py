# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/jwst_backgrounds/cli.py
# Compiled at: 2019-12-06 14:34:11
# Size of source mod 2**32: 1284 bytes
"""
Usage: 
    jwst_backgrounds [options] <ra> <dec> <wavelength> 

Options:
    --help                        show this help
    --thresh <float>              threshold factor relative to the minimum background [default: 1.1]
    --day <integer>               which day in the year for which to extract the background 
    --showsubbkgs                 show background components in the bathtub plot
    --background_file <string>    output file name for the background [default: background.txt]
    --bathtub_file <string>       output file name for the bathtub curve [default: background_versus_day.txt]

Help:
    For help using this tool, please contact the jwst help desk at jwsthelp.stsci.edu

"""
from jwst_backgrounds import jbt
import jwst_backgrounds.docopt as docopt

def main():
    """Main CLI entrypoint."""
    opt = docopt(__doc__, options_first=True)
    if opt['--day'] is None:
        thisday = None
    else:
        thisday = int(opt['--day'])
    jbt.get_background((float(opt['<ra>'])), (float(opt['<dec>'])), (float(opt['<wavelength>'])), thresh=(float(opt['--thresh'])),
      thisday=thisday,
      showsubbkgs=(opt['--showsubbkgs']),
      background_file=(opt['--background_file']),
      bathtub_file=(opt['--bathtub_file']))