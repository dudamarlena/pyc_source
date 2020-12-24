# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/terraformlintingcli/terraformlintingcli.py
# Compiled at: 2018-05-24 11:01:40
"""
Main code for terraformlintingcli

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging, logging.config, json, argparse, os
from terraformtestinglib import Stack, InvalidPositioning, InvalidNaming
from colored import fore, style
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-24'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'terraformlintingcli'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class ReadableDirectory(argparse.Action):
    """Argparse action for a directory that is readable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError(('{} is not a valid path.').format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(('No read access to {}.').format(values))


class ReadableFile(argparse.Action):
    """Argparse action for a file that is readable"""

    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.exists(values):
            raise argparse.ArgumentTypeError(('{} is not a valid file.').format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(('No read access to {}.').format(values))


def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    parser = argparse.ArgumentParser(description='Cli to lint naming conventions of terraform plans based on a provided rule set')
    parser.add_argument('--log-config', '-l', action='store', dest='logger_config', help='The location of the logging config json file', default='')
    parser.add_argument('--log-level', '-L', help='Provide the log level. Defaults to INFO.', dest='log_level', action='store', default='info', choices=[
     'debug',
     'info',
     'warning',
     'error',
     'critical'])
    parser.add_argument('-n', '--naming', metavar='naming.yaml', dest='naming', action=ReadableFile, required=True)
    parser.add_argument('-p', '--positioning', metavar='positioning.yaml', dest='positioning', action=ReadableFile, required=True)
    parser.add_argument('-s', '--stack', dest='stack', metavar='tf_plans_dir', action=ReadableDirectory, required=True)
    args = parser.parse_args()
    return args


def setup_logging(args):
    """
    Sets up the logging.

    Needs the args to get the log level supplied

    Args:
        args: The arguments returned gathered from argparse
    """
    if args.logger_config:
        configuration = json.loads(open(args.logger_config).read())
        logging.config.dictConfig(configuration)
    else:
        handler = logging.StreamHandler()
        handler.setLevel(args.log_level.upper())
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        LOGGER.addHandler(handler)
        LOGGER.setLevel(args.log_level.upper())


def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    try:
        args = get_arguments()
    except argparse.ArgumentTypeError as exc:
        raise SystemExit(exc.message)

    setup_logging(args)
    try:
        stack = Stack(args.stack, args.naming, args.positioning)
    except (InvalidNaming, InvalidPositioning):
        print fore.RED + style.BOLD + 'Invalid file provided as argument' + style.RESET
        raise SystemExit(1)

    stack.validate()
    if stack.errors:
        for error in stack.errors:
            print error

        raise SystemExit(1)
    else:
        message = 'No naming convention or file positioning errors found!'
        print fore.GREEN_3A + style.BOLD + message + style.RESET
        raise SystemExit(0)


if __name__ == '__main__':
    main()