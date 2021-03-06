# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/color_matcher/bin/cli.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 4180 bytes
__author__ = 'Christopher Hahne'
__email__ = 'info@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <info@christopherhahne.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
from color_matcher import __version__
from color_matcher.top_level import ColorMatcher, METHODS
from color_matcher.io_handler import *
import getopt, sys, os

def usage():
    print('Usage: color-matcher <options>\n')
    print('Options:')
    print('-s <path>,     --src=<path>       Specify source image file or folder to process')
    print('-r <filepath>, --ref=<filepath>   Specify target image file')
    print('-m <method>,   --method=<method>  Provide color transfer method. Available methods are:')
    print('                                  ' + ', '.join(['"' + m + '"' for m in METHODS]))
    print('-w ,           --win              Select files from window')
    print('-h,            --help             Print this help message')
    print('')


def parse_options(argv):
    try:
        opts, args = getopt.getopt(argv, 'hs:r:m:w', ['help', 'src=', 'ref=', 'method=', 'win'])
    except getopt.GetoptError as e:
        try:
            print(e)
            sys.exit(2)
        finally:
            e = None
            del e

    else:
        cfg = dict()
        cfg['src_path'] = ''
        cfg['ref_path'] = ''
        cfg['method'] = None
        cfg['win'] = None
        if opts:
            for opt, arg in opts:
                if opt in ('-h', '--help'):
                    usage()
                    sys.exit()
                if opt in ('-s', '--src'):
                    cfg['src_path'] = arg.strip(' "\'')
                if opt in ('-r', '--ref'):
                    cfg['ref_path'] = arg.strip(' "\'')
                if opt in ('-m', '--method'):
                    cfg['method'] = arg.strip(' "\'')
                if opt in ('-w', '--win'):
                    cfg['win'] = True

        else:
            return cfg


def main():
    print('\ncolor-matcher v%s \n' % __version__)
    cfg = parse_options(sys.argv[1:])
    if cfg['win']:
        cfg['src_path'] = select_file('.', 'Select source image')
        cfg['ref_path'] = select_file(cfg['src_path'], 'Select reference image')
    else:
        if not (cfg['src_path'] and cfg['ref_path']):
            usage()
            print('Canceled due to missing image file path\n')
            sys.exit()
        if os.path.isdir(cfg['src_path']):
            filenames = [f for f in os.listdir(cfg['src_path']) if f.lower().endswith(FILE_EXTS)]
        else:
            if os.path.isfile(cfg['src_path']):
                if not os.path.isfile(cfg['ref_path']):
                    print('File(s) not found \n')
                    sys.exit()
            else:
                filenames = [
                 cfg['src_path']]
    cfg['method'] = cfg['method'] if cfg['method'] in METHODS else 'mvgd'
    ref = load_img_file(cfg['ref_path'])
    output_path = os.path.dirname(cfg['src_path'])
    for f in filenames:
        src = load_img_file(f)
        res = ColorMatcher(src=src, ref=ref, method=(cfg['method'])).main()
        filename = os.path.splitext(os.path.basename(cfg['src_path']))[0] + '_' + cfg['method']
        file_ext = os.path.splitext(cfg['src_path'])[(-1)]
        save_img_file(res, file_path=(os.path.join(output_path, filename)), file_type=(file_ext[1:]))
    else:
        return True


if __name__ == '__main__':
    sys.exit(main())