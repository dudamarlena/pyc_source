# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\youtube_batch\main.py
# Compiled at: 2018-01-01 11:01:51
# Size of source mod 2**32: 7166 bytes
r"""
Uploads all videos in the given folders to Youtube.
Usage: youtube-batch [OPTIONS] FOLDER [FOLDER2 ...]
For example with:

    youtube-batch --endings="mp4, mpg, mkv"                  --privacy="private"                  --publish-at="2017-01-14T20:15:00.0+01:00"                  D:\Dateien\Filme\yesterday D:/Dateien/Filme/upload
"""
import os, sys
from pathlib import Path
import optparse, itertools
from pprint import pprint
from youtube_upload import lib

class OptionsError(Exception):
    pass


EXIT_CODES = {OptionsError: 2, 
 NotImplementedError: 5}

def upload_files(file_list, options, args):
    """Upload all files in file_list by using tokland/youtube-upload script."""
    for file in file_list:
        cmd = 'youtube-upload'
        full_cmd = ''
        full_cmd += cmd
        additional_options = {'--chunksize':options.chunksize, 
         '--privacy':'private', 
         '--title':file.stem, 
         '--publish-at':options.publish_at, 
         '--client-secrets':options.client_secrets, 
         '--credentials-file':options.credentials_file}
        for option_name, option_value in additional_options.items():
            if option_value != '' and option_value != None:
                full_cmd += ' ' + option_name + '="' + str(option_value) + '"'

        bool_options = {'--auth-browser': options.auth_browser}
        for option_name, option_bool in bool_options.items():
            if option_bool:
                full_cmd += ' ' + option_name

        full_cmd += ' "' + str(file) + '"'
        if options.dry_run:
            if options.pprint:
                pprint(full_cmd)
            else:
                print(full_cmd)
            if not options.dry_run:
                os.system(full_cmd)


def parse_options_error(parser, options, args):
    """Check errors in options."""
    required_options = []
    missing = [opt for opt in required_options if not getattr(options, opt)]
    if missing:
        parser.print_usage()
        msg = 'Some required option are missing: {0}'.format(', '.join(missing))
        raise OptionsError(msg)


def run_main(parser, options, args, output=sys.stdout):
    """Run the main scripts from the parsed options/args.
       And checks if the given folders exists beforehand."""
    parse_options_error(parser, options, args)
    endings = [str(s.strip()) for s in (options.endings or '').split(',')]
    file_list = []
    for index, path in enumerate(args):
        p = Path(path)
        if not p.exists():
            raise OptionsError('{0} does not exists'.format(path))
        for end in endings:
            if options.recursive:
                files = Path(path).glob('**/*.' + end)
            else:
                files = Path(path).glob('*.' + end)
            file_list = itertools.chain(file_list, files)

    file_list = sorted(file_list)
    if len(file_list) == 0:
        raise OptionsError('No files in the given folders. Maybe try -r or --recursive to search recursively for videos in the given folders. Like \n youtube-batch -r FOLDER [FOLDER2 ...]')
    upload_files(file_list, options, args)


def main(arguments):
    """Define the usage and the options. And then parses the given options/args and give this to run_main()."""
    usage = 'Usage: %prog [OPTIONS] FOLDER [FOLDER2 ...]\n\nUploads all videos in the folders to Youtube.\nFor example with:\n\n    youtube-batch --dry-run --pprint --endings="mp4, mpg, mkv" --privacy="private" --publish-at="2017-01-14T20:15:00.0+01:00" D:\\Dateien\\Filme\\yesterday D:/Dateien/Filme/upload'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-r',
      '--recursive',
      action='store_true',
      dest='recursive',
      help='Search recursively for videos in the given folders.',
      default=False)
    parser.add_option('-e',
      '--endings',
      dest='endings',
      type='string',
      default='mp4, mpg, mkv, avi',
      help='Video File Endings (separated by commas: "mp4, m4v,...") [mp4, mpg, mkv, avi]')
    parser.add_option('',
      '--chunksize',
      dest='chunksize',
      type='int',
      default=262144,
      help='Update file chunksize [262144]')
    parser.add_option('',
      '--privacy',
      dest='privacy',
      metavar='STRING',
      default='public',
      help='Privacy status (public | unlisted | private) [public]')
    parser.add_option('',
      '--publish-at',
      dest='publish_at',
      metavar='datetime',
      default=None,
      help='Publish date (ISO 8601): YYYY-MM-DDThh:mm:ss.sZ')
    parser.add_option('',
      '--client-secrets',
      dest='client_secrets',
      default='./.client_secrets.json',
      type='string',
      help='Client secrets JSON file [./.client_secrets.json]')
    parser.add_option('',
      '--credentials-file',
      dest='credentials_file',
      default='',
      type='string',
      help='Credentials JSON file')
    parser.add_option('',
      '--auth-browser',
      dest='auth_browser',
      default=False,
      action='store_true',
      help='Open a GUI browser to authenticate if required')
    parser.add_option('-d',
      '--dry-run',
      dest='dry_run',
      default=False,
      action='store_true',
      help='Just print the resulting command lines, but do not start uploading')
    parser.add_option('-p',
      '--pprint',
      dest='pprint',
      default=False,
      action='store_true',
      help='Use pretty print (pprint) as print function')
    if len(arguments) == 0:
        parser.print_help()
        return 0
    options, args = parser.parse_args(arguments)
    run_main(parser, options, args)


def run():
    sys.exit(lib.catch_exceptions(EXIT_CODES, main, sys.argv[1:]))


if __name__ == '__main__':
    run()