# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/filehash/filehash_cli.py
# Compiled at: 2019-12-27 22:41:44
# Size of source mod 2**32: 3236 bytes
import argparse, os.path, sys
from filehash import FileHash, SUPPORTED_ALGORITHMS
default_hash_algorithm = 'sha256'

def create_parser():
    parser = argparse.ArgumentParser(description='Tool for calculating the checksum / hash of a file or directory.')
    parser.add_argument('-a',
      '--algorithm',
      help=('Checksum/hash algorithm to use.  Valid values are: {0}.  Defaults to "{1}"'.format(', '.join(['"' + a + '"' for a in SUPPORTED_ALGORITHMS]), default_hash_algorithm)),
      default=default_hash_algorithm)
    parser_group = parser.add_mutually_exclusive_group(required=True)
    parser_group.add_argument('-c',
      '--checksums',
      help='Read the file and verify the checksums/hashes match.')
    parser_group.add_argument('-d',
      '--directory',
      help='Calculate the checksums/hashes for a directory.')
    parser_group.add_argument('-t',
      '--cathash',
      nargs='+',
      help='Process multiple files to yield a single hash value.')
    parser_group.add_argument('filenames',
      default=[], nargs='*',
      help='files to calculate the checksum/hash on')
    return parser


def process_dir(directory, hasher):
    if not os.path.isdir(directory):
        print('ERROR: Unable to read directory: {0}'.format(directory))
        sys.exit(1)
    results = hasher.hash_dir(directory)
    for result in results:
        print('{0} *{1}'.format(result.hash, result.filename))


def process_cathash(filenames, hasher):
    result = hasher.cathash_files(filenames)
    print('{0} *{1}'.format(result, ' '.join(filenames)))


def process_files(filenames, hasher):
    for filename in filenames:
        if not os.path.isfile(filename):
            print('ERROR: Unable to read file: {0}'.format(filename))
            sys.exit(1)
        result = hasher.hash_file(filename)
        print('{0} *{1}'.format(result, filename))


def process_checksum_file(checksum_filename, hasher):
    if not os.path.isfile(checksum_filename):
        print('ERROR: Unable to read checksum file: {0}'.format(checksum_filename))
        sys.exit(1)
    else:
        basename, ext = os.path.splitext(checksum_filename)
        if ext.lower() == '.sfv':
            results = hasher.verify_sfv(checksum_filename)
        else:
            results = hasher.verify_checksums(checksum_filename)
    for result in results:
        print('{0}: {1}'.format(result.filename, 'OK' if result.hashes_match else 'ERROR'))


def main():
    args = create_parser().parse_args()
    if args.algorithm.lower() not in SUPPORTED_ALGORITHMS:
        print('ERROR: Unknown checksum/hash algorithm: {0}'.format(args.algorithm))
        parser.print_help()
        sys.exit(1)
    else:
        hasher = FileHash(args.algorithm.lower())
        if args.checksums:
            process_checksum_file(args.checksums, hasher)
        else:
            if args.directory:
                process_dir(args.directory, hasher)
            else:
                if args.cathash:
                    process_cathash(args.cathash, hasher)
                else:
                    process_files(args.filenames, hasher)


if __name__ == '__main__':
    main()