# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/payno/.local/share/virtualenvs/tomwer_venv/lib/python3.7/site-packages/nxtomomill/app/tomoh52nx.py
# Compiled at: 2020-04-08 06:55:54
# Size of source mod 2**32: 3457 bytes
"""
This module provides global definitions and methods to transform
a tomo dataset written in edf into and hdf5/nexus file
"""
__authors__ = [
 'C. Nemoz', 'H. Payno', 'A.Sole']
__license__ = 'MIT'
__date__ = '16/01/2020'
import logging
from nxtomomill import utils
from nxtomomill.converter import h5_to_nx
logging.basicConfig(level=(logging.INFO))
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def main(argv):
    """
    """
    import argparse
    parser = argparse.ArgumentParser(description='convert data acquired as hdf5 from bliss to nexus `NXtomo` classes')
    parser.add_argument('input_file_path', help='master file of the acquisition')
    parser.add_argument('output_file', help='output .nx or .h5 file')
    parser.add_argument('--file_extension', action='store_true',
      default='.nx',
      help=('extension of the output file. Valid values are ' + '/'.join(utils.FileExtension.values())))
    parser.add_argument('--single-file', help='merge all scan sequence to the same output file. By default create one file per sequence and group all sequence in the output file',
      dest='single_file',
      action='store_true',
      default=False)
    parser.add_argument('--no-input', help='Do not ask for any',
      dest='request_input',
      action='store_true',
      default=False)
    options = parser.parse_args(argv[1:])
    h5_to_nx(input_file_path=(options.input_file_path), output_file=(options.output_file),
      single_file=(options.single_file),
      file_extension=(options.file_extension),
      request_input=(options.request_input))
    exit(0)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])