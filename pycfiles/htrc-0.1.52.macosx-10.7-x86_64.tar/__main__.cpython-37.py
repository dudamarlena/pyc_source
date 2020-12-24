# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/htrc/__main__.py
# Compiled at: 2019-07-30 14:13:50
# Size of source mod 2**32: 7571 bytes
"""
Master script for HTRC Workset Toolkit.
"""
from __future__ import absolute_import, division, print_function
from future import standard_library
standard_library.install_aliases()
import json, os, os.path, shutil, sys
from tempfile import NamedTemporaryFile
from htrc.metadata import get_metadata, get_volume_metadata
import htrc.volumes, htrc.workset, htrc.tools.mallet
from argparse import ArgumentParser
import htrc.tools.topicexplorer
from htrc.lib.cli import bool_prompt
from htrc.util.resolve import *

def download_parser(parser=None):
    if parser is None:
        parser = ArgumentParser()
    parser.add_argument('-u', '--username', help='HTRC username')
    parser.add_argument('-p', '--password', help='HTRC password')
    parser.add_argument('file', nargs='?', default=(sys.stdin), help='workset path[s]')
    parser.add_argument('-f', '--force', action='store_true', help='remove folder if exists')
    parser.add_argument('-o', '--output', help='output directory', default='/media/secure_volume/workset/')
    parser.add_argument('-c', '--concat', action='store_true', help="concatenate a volume's pages in to a single file")
    parser.add_argument('-m', '--mets', action='store_true', help="add volume's METS file")
    parser.add_argument('-pg', '--pages', action='store_true', help='Download given page numbers of a volumes.')
    parser.add_argument('-t', '--token', help='JWT for volumes download.')
    parser.add_argument('-dh', '--datahost', help='Data API host.')
    parser.add_argument('-dp', '--dataport', help='Data API port.')
    parser.add_argument('-de', '--dataepr', help='Data API EPR.')
    parser.add_argument('-dc', '--datacert', help='Client certificate file for mutual TLS with Data API.')
    parser.add_argument('-dk', '--datakey', help='Client key file for mutual TLS with Data API.')
    return parser


def add_workset_path(parser=None):
    if parser is None:
        parser = ArgumentParser()
    parser.add_argument('path', nargs='+', help='workset path[s]')
    return parser


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', help='print long debug messages', action='store_true')
    parsers = parser.add_subparsers(help='select a command')
    parser_getmd = parsers.add_parser('metadata', help='Get metadata for a folder of HathiTrust volumes')
    add_workset_path(parser_getmd)
    parser_getmd.set_defaults(func='metadata')
    parser_export = parsers.add_parser('export', help='Export the list of HathiTrust volumes')
    add_workset_path(parser_export)
    parser_export.set_defaults(func='export')
    parser_download = parsers.add_parser('download', help='Download HathiTrust volumes to disk [requires auth]')
    download_parser(parser_download)
    parser_download.set_defaults(func='download')
    parser_run = parsers.add_parser('run', help='Run a built-in algorithm.')
    run_parsers = parser_run.add_subparsers(help='select a command')
    parser_mallet = run_parsers.add_parser('mallet')
    htrc.tools.mallet.populate_parser(parser_mallet)
    parser_mallet.set_defaults(run='mallet')
    parser_topicexplorer = run_parsers.add_parser('topicexplorer')
    htrc.tools.topicexplorer.populate_parser(parser_topicexplorer)
    parser_topicexplorer.set_defaults(run='topicexplorer')
    parser_run.set_defaults(func='run')
    args = parser.parse_args()
    if args.func in ('metadata', 'export'):
        volumes = []
        if not args.path:
            for line in sys.stdin:
                volumes.append(line)

    else:
        for path in args.path:
            try:
                volumes.extend(htrc.workset.path_to_volumes(path))
            except ValueError:
                volumes.append(path)

    if args.func == 'export':
        for volume in volumes:
            print(volume)

    if args.func == 'metadata':
        metadata = get_metadata(volumes)
        print(json.dumps(metadata))
    else:
        if args.func == 'run':
            if args.run == 'mallet':
                htrc.tools.mallet.main(args.path, args.k, args.iter)
            if args.run == 'topicexplorer':
                htrc.tools.topicexplorer.main(args.path, args.k, args.iter)
        else:
            if args.func == 'download':
                if os.path.exists(args.output):
                    if args.force or bool_prompt(('Folder {} exists. Delete?'.format(args.output)), default=False):
                        shutil.rmtree(args.output)
                        os.makedirs(args.output)
            else:
                print('Please choose another output folder and try again.')
                sys.exit(1)
            if args.pages:
                if args.mets:
                    if args.concat:
                        print('Cannot set both concat and mets with pages')
                        sys.exit(1)
            try:
                resolve_and_download(args)
            except ValueError:
                print('Invalid identifier:', args.file)
                sys.exit(1)


def resolve_and_download--- This code section failed: ---

 L. 141         0  LOAD_FAST                'args'
                2  LOAD_ATTR                file
                4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                stdin
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    28  'to 28'

 L. 143        12  LOAD_GLOBAL              download_with_tempfile
               14  LOAD_FAST                'args'
               16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                stdin
               20  CALL_FUNCTION_2       2  '2 positional arguments'
               22  POP_TOP          

 L. 144        24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            10  '10'

 L. 146        28  LOAD_GLOBAL              os
               30  LOAD_ATTR                path
               32  LOAD_METHOD              exists
               34  LOAD_FAST                'args'
               36  LOAD_ATTR                file
               38  CALL_METHOD_1         1  '1 positional argument'
               40  POP_JUMP_IF_FALSE    54  'to 54'

 L. 148        42  LOAD_GLOBAL              download
               44  LOAD_FAST                'args'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  POP_TOP          

 L. 149        50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'

 L. 151        54  LOAD_FAST                'args'
               56  LOAD_ATTR                file
               58  LOAD_METHOD              endswith
               60  LOAD_STR                 'json'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_JUMP_IF_TRUE    102  'to 102'

 L. 152        66  LOAD_FAST                'args'
               68  LOAD_ATTR                file
               70  LOAD_METHOD              endswith
               72  LOAD_STR                 'jsonld'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_JUMP_IF_TRUE    102  'to 102'

 L. 153        78  LOAD_FAST                'args'
               80  LOAD_ATTR                file
               82  LOAD_METHOD              startswith
               84  LOAD_STR                 'http://'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  POP_JUMP_IF_TRUE    102  'to 102'

 L. 154        90  LOAD_FAST                'args'
               92  LOAD_ATTR                file
               94  LOAD_METHOD              startswith
               96  LOAD_STR                 'https://'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  POP_JUMP_IF_FALSE   152  'to 152'
            102_0  COME_FROM            88  '88'
            102_1  COME_FROM            76  '76'
            102_2  COME_FROM            64  '64'

 L. 156       102  SETUP_EXCEPT        132  'to 132'

 L. 157       104  LOAD_GLOBAL              htrc
              106  LOAD_ATTR                workset
              108  LOAD_METHOD              load
              110  LOAD_FAST                'args'
              112  LOAD_ATTR                file
              114  CALL_METHOD_1         1  '1 positional argument'
              116  STORE_FAST               'volumes'

 L. 158       118  LOAD_GLOBAL              download_with_tempfile
              120  LOAD_FAST                'args'
              122  LOAD_FAST                'volumes'
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_TOP          

 L. 159       128  LOAD_CONST               None
              130  RETURN_VALUE     
            132_0  COME_FROM_EXCEPT    102  '102'

 L. 160       132  DUP_TOP          
              134  LOAD_GLOBAL              ValueError
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   150  'to 150'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 162       146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           138  '138'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           100  '100'

 L. 165       152  SETUP_EXCEPT        202  'to 202'

 L. 166       154  LOAD_GLOBAL              parse_volume_id
              156  LOAD_FAST                'args'
              158  LOAD_ATTR                file
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  POP_JUMP_IF_FALSE   190  'to 190'

 L. 167       164  LOAD_GLOBAL              parse_volume_id
              166  LOAD_FAST                'args'
              168  LOAD_ATTR                file
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  BUILD_LIST_1          1 
              174  STORE_FAST               'volumes'

 L. 168       176  LOAD_GLOBAL              download_with_tempfile
              178  LOAD_FAST                'args'
              180  LOAD_FAST                'volumes'
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  POP_TOP          

 L. 169       186  LOAD_CONST               None
              188  RETURN_VALUE     
            190_0  COME_FROM           162  '162'

 L. 171       190  LOAD_GLOBAL              ValueError
              192  LOAD_STR                 'No Volume ID found'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  RAISE_VARARGS_1       1  'exception instance'
              198  POP_BLOCK        
              200  JUMP_FORWARD        222  'to 222'
            202_0  COME_FROM_EXCEPT    152  '152'

 L. 172       202  DUP_TOP          
              204  LOAD_GLOBAL              ValueError
              206  COMPARE_OP               exception-match
              208  POP_JUMP_IF_FALSE   220  'to 220'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          

 L. 173       216  POP_EXCEPT       
              218  JUMP_FORWARD        222  'to 222'
            220_0  COME_FROM           208  '208'
              220  END_FINALLY      
            222_0  COME_FROM           218  '218'
            222_1  COME_FROM           200  '200'

 L. 176       222  LOAD_GLOBAL              parse_record_id
              224  LOAD_FAST                'args'
              226  LOAD_ATTR                file
              228  CALL_FUNCTION_1       1  '1 positional argument'
          230_232  POP_JUMP_IF_FALSE   266  'to 266'

 L. 177       234  LOAD_GLOBAL              parse_record_id
              236  LOAD_FAST                'args'
              238  LOAD_ATTR                file
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  STORE_FAST               'record_id'

 L. 178       244  LOAD_GLOBAL              record_id_to_volume_ids
              246  LOAD_FAST                'record_id'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  STORE_FAST               'volumes'

 L. 179       252  LOAD_GLOBAL              download_with_tempfile
              254  LOAD_FAST                'args'
              256  LOAD_FAST                'volumes'
              258  CALL_FUNCTION_2       2  '2 positional arguments'
              260  POP_TOP          

 L. 180       262  LOAD_CONST               None
              264  RETURN_VALUE     
            266_0  COME_FROM           230  '230'

 L. 183       266  LOAD_GLOBAL              ValueError
              268  LOAD_STR                 'Not a valid ID file or workset identifier: {}'
              270  LOAD_METHOD              format

 L. 184       272  LOAD_FAST                'args'
              274  LOAD_ATTR                file
              276  CALL_METHOD_1         1  '1 positional argument'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `CALL_FUNCTION_1' instruction at offset 278


def download(args):
    try:
        htrc.volumes.download(args)
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


def download_with_tempfile(args, volumes):
    f = NamedTemporaryFile()
    for volume in volumes:
        f.write((volume + '\n').encode('utf-8'))

    f.flush()
    args.file = f.name
    try:
        download(args)
    finally:
        print('Closing temporary file: ' + f.name)
        f.close()


if __name__ == '__main__':
    main()