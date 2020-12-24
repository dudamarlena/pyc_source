# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/client/client.py
# Compiled at: 2013-04-22 17:17:25
from optparse import OptionParser, OptionGroup
import util, os, sys, logging, downloader, uploader
from const import Const
logging.basicConfig(level=logging.INFO)

def main():
    """
    Parses command line options, then delegates to various other functions.
    """
    usage_str = '\n%prog OPTION [FILENAME | dir: DIRECTORY | repo] | Download a file from Github\n%prog push OPTION [FILEPATH | DIRPATH]          | Push a file to Github\n\nExamples:\n`grabrc .emacs`  -- Download .emacs from Github.\n`grabrc dir:.emacs.d --outfile .irssiconfig` - Download the .emacs.d directory from Github.\n`grabrc repo --destdir=/tmp/` -- Download and untar the repository in /tmp/.\n`grabrc push /home/user/.vimrc` -- Save ~/.vimrc to Github, overwriting the existing .vimrc.\n'
    parser = OptionParser(usage=usage_str, version='r33')
    download_group = OptionGroup(parser, 'Download: All (files, directories, repositories)')
    download_group.add_option('-o', '-O', '--name', '--outfile', dest='outfile', action='store', metavar='NAME', help='Rename the downloaded item to NAME.')
    download_group.add_option('-d', '--destdir', dest='destdir', action='store', metavar='DIR', help='Place the downloaded item in DIR.                               Default: The current directory.')
    download_group.add_option('--no-backup', dest='nobackup', action='store_true', help="If the file already exists, don't make a backup.                               Default: False. If the item already exists, it will be backed up.")
    dir_group = OptionGroup(parser, 'Download: Repositories')
    dir_group.add_option('-k', '--keep-tar', dest='tar', action='store_true', help='Download the repository as a tar.gz file.                                Default: Untar the repository.')
    dir_group.add_option('-z', '--keep-zip', dest='zip', action='store_true', help='Download the repository as a .zip.')
    filegroup = OptionGroup(parser, 'Download: Files')
    filegroup.add_option('-a', '--append', dest='append', action='store_true', help='If file already exists, append to existing file.                          Default: Back up existing file')
    filegroup.add_option('-r', '--replace', dest='replace', action='store_true', help='If the file already exists, replace it')
    filegroup.add_option('-p', '--print', dest='stdout', action='store_true', help='Print the file to the console instead of saving it.')
    savegroup = OptionGroup(parser, 'Upload')
    savegroup.add_option('-m', '--message', dest='message', help='Specify a commit message for saving a file to Github.')
    map(parser.add_option_group, [
     download_group, filegroup, dir_group])
    opts, args = parser.parse_args()
    logging.debug('Options and arguments: %s / %s' % (opts, args))

    def usage_exit(level, reason):
        parser.print_help()
        print '[%s] %s' % (level.upper(), reason)
        sys.exit(1)

    try_msg = "Try either 'grabrc FILE' to download a file from Github or 'grabrc push FILEPATH' to upload a file."
    if len(args) > 2 or len(args) == 0:
        usage_exit('error', 'Invalid number of arguments. ' + try_msg)
    mode = 'download'
    if len(args) == 1:
        arg = args[0]
        if arg == 'save':
            usage_exit('error', 'Please specify a file to save.')
        elif arg == 'repo':
            mode = 'repo'
        else:
            download_name = arg
    elif 'push' in args:
        mode = 'upload'
        upload_filepath = (n for n in args if n != 'push').next()
    else:
        usage_exit('error', 'Invalid arguments. ' + try_msg)
    if opts.append and opts.replace:
        util.exit_runtime_error('Both --append and --replace were selected. Please select only one.')
    if opts.zip and opts.tar:
        util.exit_runtime_error('Both --keep-zip and --keep-tar were selected. Please select only one.')
    opts.destdir = opts.destdir or os.getcwd()
    opts.destdir = util.sanitize_path(opts.destdir)
    if opts.outfile:
        opts.outfile = util.sanitize_path(opts.outfile)
    configpath = '%s/.grabrc' % os.path.expanduser('~')
    if opts.__dict__.get('github'):
        github_acc = opts.github
    if not os.path.isfile(configpath):
        print '        ========================================================\n        Welcome! This seems to be your first time starting %s.\n        Please enter your Github username.\n        %s will search for files in the repository named %s' % (
         Const.PROG_NAME, Const.PROG_NAME, Const.REPO_NAME)
        github_acc = raw_input('-- Github account: ')
        cfile = open(configpath, 'w+')
        cfile.write(github_acc)
    else:
        cfile = open(configpath, 'r+')
        github_acc = cfile.readline().strip()
    cfile.close()
    opts.github = github_acc
    logging.debug('Github account: %s' % github_acc)
    DIR_PREFIX = 'dir:'
    if mode == 'upload':
        uploader.save(upload_filepath, opts)
    elif mode == 'download':
        if download_name.startswith(DIR_PREFIX):
            downloader.download_subdirectory(download_name[len(DIR_PREFIX):], opts)
        else:
            downloader.download_file(download_name, opts)
    elif mode == 'repo':
        downloader.download_repo_nongit(opts)


if __name__ == '__main__':
    main()