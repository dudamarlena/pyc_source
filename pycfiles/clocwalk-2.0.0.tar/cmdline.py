# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/cmdline.py
# Compiled at: 2019-12-11 03:21:38
import os, sys, clocwalk
from optparse import OptionParser
from clocwalk.libs.core.data import logger
from clocwalk.libs.core.data import conf
from clocwalk.libs.core.settings import IS_WIN

def cmdLineParser():
    """
    This function parses the command line parameters and arguments
    """
    _ = os.path.basename(sys.argv[0])
    usage = 'clocwalk [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('--config', '-c', dest='config', help='Print out the version')
    parser.add_option('--verbose', dest='verbose', type='int', default=1, help='Verbosity level: 0-3 (default 1)')
    parser.add_option('--version', dest='version', action='store_true', default=False, help='Print out the version')
    try:
        general = parser.add_option_group('General')
        general.add_option('--upgrade', '-u', dest='upgrade', action='store_true', default=False, help='')
        general.add_option('--force-update', '-f', dest='force_update', action='store_true', default=False, help='')
        general.add_option('--exclude-ext', dest='exclude_ext', help='Does not include file extensions')
        general.add_option('--exclude-dir', dest='exclude_dir', help='Does not contain directories')
        analysis = parser.add_option_group('Analysis')
        analysis.add_option('--path', '-p', dest='code_dir', help='Code path or directory')
        analysis.add_option('--timeout', dest='timeout', type='int', default=5, help='Http request timeout (default 5)')
        analysis.add_option('--vuln-scan', dest='vuln_scan', action='store_true', default=False, help='Http request timeout (default 5)')
        analysis.add_option('--search', dest='search', help='Http request timeout (default 5)')
        try:
            args, _ = parser.parse_args()
            if not any((args.version, args.code_dir, args.upgrade, args.force_update, args.search)):
                err = 'missing a mandatory option (-p, --version, --upgrade/--force-update, --search) use -h for help'
                raise SystemExit(err)
            if args.version:
                print 'clocwalk v%s' % clocwalk.__version__
                raise SystemExit
            conf.update(args.__dict__)
        except UnicodeEncodeError as ex:
            print '\n[!] %s' % ex
            raise SystemExit
        except SystemExit:
            raise

    except Exception as ex:
        print ex

    logger.debug('parsing command line')