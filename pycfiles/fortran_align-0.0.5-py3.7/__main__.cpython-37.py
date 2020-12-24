# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/falign/__main__.py
# Compiled at: 2020-03-15 08:04:56
# Size of source mod 2**32: 3531 bytes
"""Align comments in Fortran files."""
import argparse, sys, logging
from typing import List
from falign.falign import FAlign

def run():
    """Run FAlign."""
    parser = argparse.ArgumentParser(prog='falign')
    parser.add_argument('--output', default='', metavar='file-name',
      help='Output file')
    parser.add_argument('--inplace', default=False, action='store_true',
      help='Reformat inplace')
    parser.add_argument('--dry-run', default=False, action='store_true',
      help='Just write result to standard error and do not touch output file')
    parser.add_argument('--debug', default=False, action='store_true',
      help='Write debugging information to standard error')
    parser.add_argument('--ignore-offset', type=int, default=None, metavar='ignored-offset',
      help='Ignored offset before aligning a line comment to the right and not with the code')
    parser.add_argument('input', nargs='?', default='', metavar='file-name',
      help='Input file')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(stream=(sys.stderr), level=(logging.DEBUG))
    else:
        logging.basicConfig(stream=(sys.stderr), level=(logging.WARNING))
    if args.inplace:
        if args.output:
            logging.error('Error in Argument: --inplace and --output can not be defined at the same time!')
            sys.exit(1)
    if args.inplace:
        if not args.input:
            logging.error('Error in Argument: --inplace can not be used without input file!')
            sys.exit(1)
    input_lines = []
    output_lines = []
    if args.input:
        logging.debug('open(%s)', args.input)
        input_file = open((args.input), mode='r', encoding='ascii', errors='surrogateescape')
        logging.debug('read(%s)', args.input)
        input_lines.extend(input_file.readlines())
        logging.debug('close(%s)', args.input)
        input_file.close()
    else:
        logging.debug('read(sys.stdin)')
        input_lines.extend(sys.stdin.readlines())
    if args.debug:
        sys.stderr.write(''.join(input_lines))
    logging.debug('falign()')
    falign = FAlign(1, 49, args.ignore_offset)
    output_lines.extend(falign.falign(input_lines))
    if args.inplace and input_lines == output_lines:
        logging.debug('input equals output: no change --> no write.')
    else:
        if args.dry_run:
            logging.debug('dry-run: write(stderr)')
            sys.stderr.write('\n'.join(output_lines))
        else:
            if args.output:
                logging.debug('open(%s)', args.output)
                output_file = open((args.output), mode='w', encoding='ascii', errors='surrogateescape')
                logging.debug('write(%s)', args.output)
                output_file.writelines(output_lines)
                logging.debug('%s.close()', args.output)
                output_file.close()
            else:
                if args.inplace and args.input:
                    logging.debug('open(%s)', args.input)
                    output_file = open((args.input), mode='w', encoding='ascii', errors='surrogateescape')
                    logging.debug('write(%s)', args.input)
                    output_file.writelines(output_lines)
                    logging.debug('%s.close()', args.input)
                    output_file.close()
                else:
                    logging.debug('write(stdout)')
                    sys.stdout.writelines(output_lines)
    logging.debug('done.')


if __name__ == '__main__':
    run()