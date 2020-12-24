# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ttws/cli.py
# Compiled at: 2020-01-16 03:54:37
# Size of source mod 2**32: 5406 bytes
import sys, os, getopt, textwrap
from . import BLACKLIST, cleanAnnotation, extstring, detecttype, stripDocString, trimWhitespace, unknownDirectory, unknownOption

def main(args=None):
    if args is None:
        args = sys.argv
    script_name = args.pop(0)
    script_name = os.path.split(script_name)[1]
    try:
        opts, dirnames = getopt.getopt(args, 'hvsbc', ['help', 'version', 'strip', 'blanks', 'clean',
         'eol='])
    except getopt.GetoptError:
        unknownOption(args)
        sys.exit(0)

    if not dirnames:
        usage(args)
        sys.exit(0)
    cleanOpt = False
    stripOpt = False
    eol = os.linesep
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(args)
            sys.exit(0)
        elif opt in ('-v', '--version'):
            os.system('pip show ttws')
            sys.exit(0)
        elif opt in ('-c', '--clean'):
            cleanOpt = True
        elif opt in ('-b', '--blanks'):
            os.system('for fn in `find -name "*.mo"`; do cat -s $fn >$fn.1; mv $fn.1 $fn; done')
            sys.exit(0)
        elif opt in ('-s', '--strip'):
            stripOpt = True
        elif opt in '--eol':
            eol = {'CRLF':'\r\n',  'LF':'\n', 
             'CR':'\r'}
            eol = eol.get(arg, os.linesep)
        else:
            unknownOption(args)
            sys.exit(0)

    for dirname in dirnames:
        if os.path.exists(dirname) is False:
            unknownDirectory(dirname)
        else:
            for path, dirs, files in os.walk(dirname):
                for directory in dirs:
                    if directory in BLACKLIST:
                        print('skipping version control dir: %s ' % directory)
                        dirs.remove(directory)

                for file in files:
                    filepath = os.path.join(path, file)
                    filetype = detecttype(filepath)
                    if filetype is 'mo':
                        if cleanOpt is True:
                            print('trimming and cleaning %s' % filepath)
                            trimWhitespace(filepath, eol)
                            cleanAnnotation(filepath, eol)
                    if filetype is 'mo':
                        if stripOpt is True:
                            print('trimming and stripping %s' % filepath)
                            trimWhitespace(filepath, eol)
                            stripDocString(filepath, eol)
                    if filetype is 'mo' or filetype is 'text':
                        print('trimming %s' % filepath)
                        trimWhitespace(filepath, eol)
                    else:
                        print('skipping file of type %s: %s' % (filetype, filepath))


def usage(script_name):
    """Help message on usage."""
    message = "\n        Usage: ttws [OPTIONS] <directory> [<directory> ...]\n\n         This script will recursively scan all text files in a given list of\n         directories and remove all trailing white space in every line as well\n         as multiple blank lines at the end of the file. Binary files and files\n         residing in '.bzr', '.cvs', '.git', '.hg', '.svn' directories are\n         skipped.\n\n         Since the main application is for Modelica projects it expects all files\n         to be of type ASCII or UTF8. Otherwise it will throw an exception,\n         report the illegal file and terminate.\n\n        Note for Windows users:\n         If you do not have libmagic installed, the script will fall back to\n         only trim files with the following extensions:\n             %s\n\n        Options:\n            -h, --help\n                displays this help message\n\n            -v, --version\n                displays version information\n\n            -s, --strip\n                strips leading or trailing white spaces from info or\n                revision strings that contain HTML documentation\n                (those disturb the proper HTML rendering in 'some' tools)\n\n            --eol=[CRLF|LF|CR]\n                Force the line endings to be of type:\n                 - CRLF = '\\r\\n' Windows\n                 - LF = '\\n' POSIX\n                 - CR = '\\r' Mac (pre OSX)\n                If empty or not specified it is set to the OS default.\n                I.e., on this machine to: %s.\n\n            -c, --clean\n                WARNING: USE THIS OPTION AT YOUR OWN RISK AS\n                         IT *MIGHT* BREAK YOUR CODE!\n                Removes obsolete or superfluous annotation constructs\n                from Modelica files.\n                Only use this if your code is under version control\n                and in combination with a careful code-diff review.\n\n            -b, --blanks\n                suppress repeated empty output lines from *.mo files\n                (This option should not be run in combination with others.)\n\n        " % (extstring, repr(os.linesep))
    print(textwrap.dedent(message))


if __name__ == '__main__':
    sys.exit(main())