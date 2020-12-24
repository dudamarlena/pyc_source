# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/utils/arguments_parser.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 3578 bytes
__doc__ = '\nproducti_gestio.utils.arguments_parser\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nIt just parses the given arguments via command line.\n'
import argparse, sys, producti_gestio
long_license = '\nCopyright (c) 2018 The producti-gestio Authors (see AUTHORS)\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'

def parser(args: list=sys.argv) -> object:
    """It tries to parse
    sys.argv and processes
    given parameters.

    Args:
      args: list:  (Default value = sys.argv)

    Returns:
      object: A parse_args object of all the parameters.
    """
    global long_license
    if len(args) <= 1:
        args.append('-h')
    args = args[1:]
    version_pg = 'producti_gestio ' + producti_gestio.__version__
    name_description = 'the name of the project you would like to create'
    desc = 'A simple HTTPServer generator.'
    _parser = argparse.ArgumentParser(description=desc)
    _parser.add_argument('-n', '--name', help=name_description)
    _parser.add_argument('-v', '--version', help='print current version',
      action='version',
      version=version_pg)
    _parser.add_argument('-l', '--license', help='print the license',
      action='version',
      version=long_license)
    return _parser.parse_args(args)