# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\hdl.py
# Compiled at: 2015-05-16 02:38:44
# Size of source mod 2**32: 1455 bytes
import argparse, sys, subprocess, logging, autohdl.structure as structure, autohdl.pkg_info as pkg_info, autohdl.documentation as documentation, autohdl.configuration as configuration
alog = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Helper to create designs')
    parser.add_argument('-doc', action='store_true', help='extended documentation in browser')
    parser.add_argument('-name', default='', help='set design name and create structure [default - current directory name]')
    parser.add_argument('-version', action='store_true', help='display package version')
    parser.add_argument('-edit', choices=['default_build', 'toolchain'], help='edit default build.yaml file')
    args = parser.parse_args()
    if args.version:
        print('AutoHDL version: ' + pkg_info.version())
    else:
        if args.doc:
            documentation.handler('index')
        else:
            if args.edit:
                if args.edit == 'default_build':
                    subprocess.Popen('notepad {}/Lib/site-packages/autohdl/data/build.yaml'.format(sys.prefix))
                elif args.edit == 'toolchain':
                    subprocess.Popen('notepad {}/Lib/site-packages/autohdl_cfg/toolchain.yaml'.format(sys.prefix))
            else:
                dsn = structure.generate(path=args.name)
                print(dsn)


if __name__ == '__main__':
    configuration.copy()
    main()