# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/OpenDiscovery/__init__.py
# Compiled at: 2016-03-23 21:44:42
__author__ = 'Gareth Price'
__email__ = 'gareth.price@warwick.ac.uk'
__version__ = '2.5'
__url__ = 'http://opendiscovery.co.uk'
OD_VERSION = __version__
import sys, os, errno
from helpers import *
from helpers.log import *

def log(message='', verbose=True, colour=None, background=None, bold=False, underline=False, inverted=False, run=False, ret=False):
    """ log() prints a message that is formatted properly.

        Using ANSI colour and formatting strings, log() prints out a formatted
        string. If run=True, the following print command (or log())
        will appear on the same line.
    """
    if 'linux' in sys.platform:
        if ret:
            return message
        if run:
            print message,
        else:
            print message
    elif 'darwin' in sys.platform:
        if verbose:
            colours = {'black': '90', 
               'red': '91', 
               'green': '92', 
               'yellow': '93', 
               'blue': '94', 
               'magenta': '95', 
               'cyan': '96', 
               'white': '97'}
            backgrounds = {'default': '49', 
               'black': '100', 
               'red': '101', 
               'green': '102', 
               'yellow': '103', 
               'blue': '104', 
               'magenta': '105', 
               'cyan': '106', 
               'white': '107'}
            if bold:
                message = '\x1b[1m' + message + '\x1b[21m'
            if underline:
                message = '\x1b[4m' + message + '\x1b[24m'
            if background is not None:
                message = '\x1b[' + backgrounds[background] + 'm' + message + '\x1b[49m'
            if colour is not None:
                message = '\x1b[' + colours[colour] + 'm' + message + '\x1b[0m'
            if inverted:
                message = '\x1b[7m' + message + '\x1b[27m'
            if ret:
                return message
            if run:
                print message,
            else:
                print message
    return


def logHeader(message):
    """logHeader() prints out a formatted message which is used for heading sections."""
    message = ('\n{message}').format(message=message)
    print message


def printHeader(message):
    if 'linux' in sys.platform:
        print ('\r{message:<20} ').format(message=message)
    elif 'darwin' in sys.platform:
        print ('\r   \x1b[38;5;204m{message:<20}\x1b[0m ').format(message=message)


class ProgressBar(object):
    """A Simple class for showing a progress bar to the user"""

    def __init__(self, progress, total, message, newline=True):
        if 'linux' in sys.platform:
            message = ('{message:<20}').format(message=message)
        elif 'darwin' in sys.platform:
            message = ('  \x1b[38;5;204m{message:<20}\x1b[0m ').format(message=message)
        import time
        time.sleep(0.01)
        progress += 1
        percentage = progress * 10 / total
        percentage_left = 10 - percentage
        bar = '['
        bar += percentage * log('*', colour='white', ret=True)
        bar += percentage_left * log('*', colour='black', ret=True)
        bar += ']'
        bar += (' {}').format(progress)
        string = ''
        if progress != total:
            if progress == 1 and newline == True:
                string = ('\n\r {message} {bar}').format(message=message, bar=bar)
            else:
                string = ('\r {message} {bar}').format(message=message, bar=bar)
        else:
            string = ('\r {message} {bar}').format(message=message, bar=bar)
        sys.stdout.write(string)
        sys.stdout.flush()


def makeFolder(path):
    """Attempts folder creation

        Tries to create a folder. Raises an exception if one exists already/
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def tryForKeyInDict(needle, haystack, fallback):
    try:
        return haystack[needle]
    except Exception as e:
        return fallback