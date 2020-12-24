# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/mapscookiegettercli/mapscookiegettercli/mapscookiegettercli.py
# Compiled at: 2019-03-05 08:16:25
# Size of source mod 2**32: 3333 bytes
"""
Main code for mapscookiegettercli

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging, argparse, coloredlogs
from mapscookiegettercli import CookieGetter
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '04-03-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'mapscookiegettercli'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    parser = argparse.ArgumentParser(description='A tool to retrieve the cookies from a google authentication process\n                                                     towards the google maps service to be used with\n                                                     locationsharinglib.')
    parser.add_argument('--log-level', '-L',
      help='Provide the log level. Defaults to info.',
      dest='log_level',
      action='store',
      type=(str.upper),
      default='INFO',
      choices=[
     'DEBUG',
     'INFO',
     'WARNING',
     'ERROR',
     'CRITICAL'])
    args = parser.parse_args()
    return args


def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    coloredlogs.install(level=(args.log_level))
    getter = CookieGetter()
    getter.run()


if __name__ == '__main__':
    main()