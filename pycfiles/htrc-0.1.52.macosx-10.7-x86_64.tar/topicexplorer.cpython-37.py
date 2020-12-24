# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/htrc/tools/topicexplorer.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 3576 bytes
from builtins import map
import os.path, subprocess
from tempfile import NamedTemporaryFile
from htrc.volumes import download_volumes
from htrc.workset import path_to_volumes

def main(path, topics, iterations, output_dir='/media/secure_volume/workset'):
    if os.path.exists('/media/secure_volume'):
        try:
            volumes = path_to_volumes(path)
        except ValueError as e:
            try:
                print('Could not process workset. {}'.format(str(e)))
                sys.exit(1)
            finally:
                e = None
                del e

        try:
            download_volumes(volumes, output_dir)
        except OSError as e:
            try:
                if not os.path.exists('/media/secure_volume/'):
                    print('Secure volume not mounted. Could not download volumes')
                    sys.exit(1)
                else:
                    print('Could not download volumes. {} {}'.format(e.strerror, e.filename))
                    sys.exit(1)
            finally:
                e = None
                del e

        except RuntimeError as e:
            try:
                if not args.debug:
                    print('Could not download volumes. {}'.format(str(e)))
                    sys.exit(1)
                else:
                    raise e
            finally:
                e = None
                del e

        path = output_dir
    else:
        if not os.path.exists(path):
            try:
                volumes = path_to_volumes(path)
                volfile = NamedTemporaryFile(prefix='htrc-workset', delete=False)
                volfile.write(bytes('\n'.join(volumes), 'ascii'))
                path = volfile.name
                volfile.close()
            except ValueError as e:
                try:
                    print('Could not process workset. {}'.format(str(e)))
                    sys.exit(1)
                finally:
                    e = None
                    del e

        if path.endswith('/'):
            path = path[:-1]
        subprocess.check_call([
         'topicexplorer', 'init', path,
         '--name', '"HathiTrust Workset"',
         '--rebuild', '--htrc', '-q'])
        subprocess.check_call([
         'topicexplorer', 'prep', path,
         '-q', '--min-word-len', '3', '--lang', 'en',
         '--high', '30', '--low', '10'])
        subprocess.check_call([
         'topicexplorer', 'train', path, '-k'] + list(map(str, topics)) + [
         '--iter', str(iterations),
         '--context-type', 'book',
         '-q'])
        subprocess.check_call([
         'topicexplorer', 'launch', path])


def populate_parser(parser=None):
    if parser is None:
        from argparse import ArgumentParser
        parser = ArgumentParser()
    parser.add_argument('-k', type=int, nargs='+', required=True, help='number of topics')
    parser.add_argument('--iter', help='number of iterations', default=200)
    parser.add_argument('path', default='/media/secure_volume/workset', nargs='?')
    parser.add_argument('--workset-path', help='Location to store workset download.', default='/media/secure_volume/workset')
    return parser


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Topic Explorer tools for the HTRC')
    populate_parser(parser)
    args = parser.parse_args()
    main(args.path, args.k, args.iter, args.workset_path)