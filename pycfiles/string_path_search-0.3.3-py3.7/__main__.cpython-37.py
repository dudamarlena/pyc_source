# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\string_path_search\__main__.py
# Compiled at: 2019-08-13 14:31:37
# Size of source mod 2**32: 10459 bytes
"""
For a directory and a list of strings, find the files that match any string.

Usage:
    python __main__.py [OPTIONS] <scan-root> [<search-string> [...]]
    where:
        -a, --unpack-archives = Unpack and scan within archives
            (Default: Arhives will NOT be uncompressed and will be scanned
            as a single file). LIMITATIONS: Only zip and tar archives will be
            unpacked. Only gzip and bzip2 tar compression methods are supported.
        -B, --branding-text=<branding-text> = A string of text containing
            company or other information to add above the column headers in
            scan reports (Default: no text).
        -b, --branding-logo=<branding-logo> = (MS Excel only) An image
            file containing a corporate logo or other graphic to add above the
            column headers in scan reports (Default: no logo).
        -h, --help = Print usage information and exit.
        -e, --excel-output = Generate Microsoft Excel 2007 (.xlsx) output
            (Default: Generate comma-separated-value (CSV) text output)
        -i  --ingore-case = Ignore UPPER/lowercase differences when matching strings
            (Default: case differences are significant).
        -o, --output-dir=<output-dir> = Location for output (Default:
            <current working directory>).
        -s, --search-strings=<search-strings> = A file containing strings to
        search for, one per line (No Default).
        -q, --quiet = Decrease logging verbosity (may repeat). -vvvv will suppress all logging.
        -t, --temp-dir=<temp-dir> = Location for unpacking archives
            (Default: <output_dir>/temp).
        -v, --verbose = Increase logging verbosity.
    <scan-root> = Directory to scan (No Default).

Limitations:
    Requires Python 3.4 or later.
    Only handles jar, tar, and zip archives.
    Only handles bzip2, gzip, and xz tar compression.
    Only handles compression in archives, not single files.
    Maximum file size and results array length limited by available system RAM.
    Maximum archive size limited by available Scanner.temp_dir disk space.
"""
import getopt, logging, os, sys, time
from string_path_search import Scanner, eprint, LOGGER, make_dir_safe, Output

def print_usage():
    """Print the program usage."""
    usage = '\n        $ python -m string_path_search [OPTIONS] <scan-root> [<search-string> [...]]\n        or (if the .exe was installed from pypi):\n        $ string_path_search.exe [OPTIONS] <scan-root> [<search-string> [...]]\n        where:\n            -a, --unpack-archives = Unpack and scan within archives\n                (Default: Arhives will NOT be uncompressed and will be scanned\n                as a single file). Only jar, tar, and zip archives will be\n                unpacked. Tar bzip2, gzip, and xz compression is supported.\n            -B, --branding-text=<branding-text> = A string of text containing\n                company or other information to add above the column headers in\n                scan reports (Default: no text).\n            -b, --branding-logo=<branding-logo> = (MS Excel only) An image\n                file containing a corporate logo or other graphic to add above the\n                column headers in scan reports (Default: no logo).\n            -h, --help = Print usage information and exit.\n            -e, --excel-output = Generate Microsoft Excel 2007 (.xlsx) output\n                (Default: Generate comma-separated-value (CSV) text output)\n            -i  --ingore-case = Ignore UPPER/lowercase differences when matching strings\n                (Default: case differences are significant).\n            -o, --output-dir=<output-dir> = Location for output (Default:\n                <current working directory>).\n            -s, --search-strings-file=<search-strings> = A file containing strings\n                to search for, one per line (No Default).\n            -q, --quiet = Decrease logging verbosity (may repeat). -qqqq will suppress all logging.\n            -t, --temp-dir=<temp-dir> = Location for unpacking archives\n                (Default: <output_dir>/temp).\n            -v, --verbose = Increase logging verbosity.\n            -x, --exclusions-file=<exclusion-file> = A file containing (base) filenames to\n                exclude from the search results.\n        <scan-root> = Directory to scan (No Default).\n        <search-string> ... = One or more terms to search for in <scan-root>.\n        '
    eprint(usage)


def parse_args():
    """Populate the config structure from the command line."""
    config = {'branding_text':None, 
     'branding_logo':None, 
     'excel_output':False, 
     'ignore_case':False, 
     'log_level':logging.INFO, 
     'output_dir':os.getcwd(), 
     'search_strings_file':None, 
     'temp_dir':os.path.join(os.getcwd(), 'temp'), 
     'scan_archives':False, 
     'exclusions_file':None, 
     'search_strings':set(), 
     'exclusions':set()}
    sys_args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(sys_args, 'aB:b:ehio:qs:t:vx:', [
         'scan_archives',
         'branding_text',
         'branding_logo',
         'excel_output',
         'help',
         'ignore_case',
         'output_dir',
         'quiet',
         'search-strings-filetemp_dir',
         'verbose',
         'exclusions-file'])
    except getopt.GetoptError as err:
        try:
            eprint(err.msg)
            print_usage()
            sys.exit(2)
        finally:
            err = None
            del err

    if '-v' in opts:
        if '-q' in opts:
            eprint('Improper usage: Use -v or -q, not both.')
            print_usage()
            sys.exit(2)
    for opt, arg in opts:
        if opt in ('-B', '--branding-text'):
            config['branding_text'] = arg.strip()
        elif opt in ('-b', '--branding-logo'):
            config['branding_logo'] = arg.strip()
        elif opt in ('-a', '--unpack-archives'):
            config['scan_archives'] = True
        elif opt in ('-e', '--excel-output'):
            config['excel_output'] = True
        elif opt in ('-h', '--help'):
            print_usage()
            sys.exit(0)
        elif opt in ('-i', '--ignore-case'):
            config['ignore_case'] = True
        elif opt in ('-o', '--output-dir'):
            config['output_dir'] = arg.strip()
        elif opt in ('-q', '--quiet'):
            if config['log_level'] == logging.CRITICAL:
                config['log_level'] = logging.NOTSET
            else:
                if config['log_level'] == logging.ERROR:
                    config['log_level'] = logging.CRITICAL
                else:
                    if config['log_level'] == logging.WARNING:
                        config['log_level'] = logging.ERROR
                    else:
                        config['log_level'] = logging.WARNING
        elif opt in ('-s', '--search-string-file'):
            config['search_strings_file'] = arg.strip()
        elif opt in ('-t', '--temp-dir'):
            config['temp_dir'] = arg.strip()
        else:
            if opt in ('-v', '--verbose'):
                config['log_level'] = logging.DEBUG

    if not args:
        eprint('Insufficient arguments on command line')
        print_usage()
        sys.exit(2)
    config['scan_root'] = args[0].strip()
    if len(args) > 1:
        for _ in args[1:]:
            config['search_strings'].add(_.strip())

    if not config['search_strings']:
        eprint('You must specify at least one search string, either via the -s <search-strings-file> option or as positional commandline argument.')
        print_usage()
        sys.exit(2)
    return config


def main():
    """Instantiate a Scanner and initiate a scan."""
    configs = parse_args()
    if configs['branding_logo']:
        if not os.path.exists(configs['branding_logo']):
            eprint("The <branding-logo> , {0}, doesn't exist.".format(configs['branding_logo']))
            sys.exit(2)
    if not (os.path.exists(configs['output_dir']) and os.path.isdir(configs['output_dir'])):
        eprint("The <output-dir> , {0}, doesn't exist or isn't a directory.".format(configs['output_dir']))
        sys.exit(2)
    make_dir_safe(configs['temp_dir'], True)
    if configs['search_strings_file']:
        if not os.path.exists(configs['search_strings_file']):
            eprint("-s <search-strings-file> argument, {0}, doesn't exist".format(configs['search_strings_file']))
            sys.exit(2)
        with open((configs['search_strings_file']), 'rt', encoding='utf-8') as (fid):
            for line in fid:
                configs['search_strings'].add(line.strip())

    if configs['exclusions_file']:
        if not os.path.exists(configs['exclusions_file']):
            eprint("-s <exclusions_file> argument, {0}, doesn't exist".format(configs['exclusions_file']))
            sys.exit(2)
        with open((configs['exclusions_file']), 'rt', encoding='utf-8') as (fid):
            for line in fid:
                configs['exclusions'].add(line.strip().casefold())

    if not os.path.exists(configs['scan_root']):
        eprint("The <scan-root> , {0}, doesn't exist.".format(configs['scan_root']))
        sys.exit(2)
    LOGGER.setLevel(configs['log_level'])
    LOGGER.info('Startup')
    scanner = Scanner(configs)
    scanner.scan()
    output = Output.get_output(scanner.HEADERS, scanner.get_results(), configs)
    output.output()


if __name__ == '__main__':
    main()