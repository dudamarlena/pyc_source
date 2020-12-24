# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/xim.py
# Compiled at: 2008-01-19 12:07:24
"""Main file for Ximenez.

$Id: xim.py 46 2008-01-19 17:07:27Z damien.baty $
"""
import sys, time, getopt, socket, logging
from ximenez.utils import getPluginInstance
USAGE = 'Standard usage: %s -c <collector> -a <action>\n\n-h, --help\n  Display help and exit.\n\n-v, --version\n  Display version and exit.\n\n-c <collector>\n  Use <collector> plug-in.\n\n--ci <input>\n  Provide input to te collector plug-in.\n\n-a <action>\n  Use <action> plug-in.\n\n--ai <input>\n  Provide input to the action plug-in.\n\n-o <output-file>, --outfile <output-file>\n  Log to <output-file>.\n\nSee the documentation for further details.' % sys.argv[0]
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_TIMEOUT = 3
socket.setdefaulttimeout(DEFAULT_TIMEOUT)
__version__ = '0.9'

def main():
    """Collect informations and execute action."""
    try:
        (options, args) = getopt.getopt(sys.argv[1:], 'hva:c:o:', [
         'help', 'version', 'output=', 'ai=', 'ci='])
    except getopt.GetoptError:
        print USAGE
        sys.exit(1)

    action = None
    collector = None
    action_input = None
    collector_input = None
    output_path = None
    for (option, value) in options:
        if option == '-a':
            action = value
        elif option == '-c':
            collector = value
        elif option == '--ai':
            action_input = value
        elif option == '--ci':
            collector_input = value
        elif option in ('-o', '--output'):
            output_path = value
        elif option in ('-h', '--help'):
            print USAGE
            sys.exit(0)
        elif option in ('-v', '--version'):
            print __version__
            sys.exit(0)

    if not action or not collector:
        print 'Error: wrong arguments.'
        print USAGE
        sys.exit(1)
    log_settings = {'level': LOGGING_LEVEL, 'format': LOGGING_FORMAT, 'datefmt': LOGGING_DATE_FORMAT}
    if output_path is not None:
        log_settings['filename'] = output_path
    logging.basicConfig(**log_settings)
    try:
        collector = getPluginInstance(collector, 'collectors')
    except ImportError:
        logging.critical('Could not import "%s" collector plug-in. Got the following exception:', collector, exc_info=True)
        sys.exit(1)

    try:
        action = getPluginInstance(action, 'actions')
    except ImportError:
        logging.critical('Could not import "%s" action plug-in. Got the following exception:', action, exc_info=True)
        sys.exit(1)

    start_time = time.time()
    logging.info("Started Ximenez session: '%s'." % (' ').join(sys.argv[1:]))
    collector.getInput(collector_input)
    sequence = collector.collect()
    logging.info('Collected %d items.' % len(sequence))
    action.getInput(action_input)
    action.execute(sequence)
    elapsed = time.time() - start_time
    logging.info('Executed action in %d seconds.' % elapsed)
    return


if __name__ == '__main__':
    main()