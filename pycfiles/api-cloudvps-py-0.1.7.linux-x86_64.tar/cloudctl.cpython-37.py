# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grudin/dev/my/api-cloudvps-py/.venv/lib/python3.7/site-packages/cloudvps/cloudctl.py
# Compiled at: 2018-07-17 13:27:11
# Size of source mod 2**32: 1359 bytes
import cloudvps, os, sys, os.path, argparse

def get_token():
    """
    Obtain token from different places
    """
    if 'CLOUD_TOKEN' in os.environ:
        return os.environ['CLOUD_TOKEN']
    return get_from_file()


def get_from_file(file='.cloudvps_token'):
    """
    Try get token from default `file`
    """
    try:
        from pathlib import Path
        token_file = Path(os.path.join(Path.home(), file))
        if token_file.exists():
            with token_file.open() as (f):
                return f.readline()
    except:
        from os.path import expanduser, exists
        token_file = os.path.join(os.path.expanduser('~'), file)
        if exists(token_file):
            with open(token_file) as (f):
                return f.readline()


def serve():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    print('forever')
    print(get_token())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose',
      help='increase output verbosity', action='store_true')
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if args.verbose:
        print('verbosity turned on')
    serve()