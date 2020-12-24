# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/shared/messages.py
# Compiled at: 2019-11-21 11:07:35
# Size of source mod 2**32: 2812 bytes
from colorama import Fore
import sys, os, logging

def get_header():
    import circus
    version = circus.__version__
    if len(version) == 3:
        title = '#####            Welcome to the SpyKING CIRCUS (%s)         #####' % version
    else:
        if len(version) == 5:
            title = '#####           Welcome to the SpyKING CIRCUS (%s)        #####' % version
    header = '\n##################################################################\n%s\n#####                                                        #####\n#####              Written by P.Yger and O.Marre             #####\n##################################################################\n\n' % title
    return header


class InfoFilter(logging.Filter):

    def filter(self, rec):
        return rec.levelno == logging.DEBUG


def init_logging(logfile, debug=True, level=None):
    """
    Simple configuration of logging.
    """
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    if level:
        log_level = level
    logger = logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)-8s [%(name)s] %(message)s',
      filename=logfile,
      filemode='a')
    return logger


def write_to_logger(logger, to_write, level='info'):
    for line in to_write:
        if level == 'info':
            logger.info(line)
        else:
            if level in ('debug', 'default'):
                logger.debug(line)
            else:
                if level == 'warning':
                    logger.warning(line)


def print_and_log(to_print, level='info', logger=None, display=True):
    if display:
        if level == 'default':
            for line in to_print:
                print(Fore.WHITE + line + '\r')

        if level == 'info':
            print_info(to_print)
        elif level == 'error':
            print_error(to_print)
    if logger is not None:
        write_to_logger(logger, to_print, level)
    sys.stdout.flush()


def print_info(lines):
    """Prints informations messages, enhanced graphical aspects."""
    print(Fore.YELLOW + '-------------------------  Informations  -------------------------\r')
    for line in lines:
        print(Fore.YELLOW + '| ' + line + '\r')

    print(Fore.YELLOW + '------------------------------------------------------------------\r' + Fore.WHITE)


def print_error(lines):
    """Prints errors messages, enhanced graphical aspects."""
    print(Fore.RED + '----------------------------  Error  -----------------------------\r')
    for line in lines:
        print(Fore.RED + '| ' + line + '\r')

    print(Fore.RED + '------------------------------------------------------------------\r' + Fore.WHITE)


def get_colored_header():
    return Fore.GREEN + get_header() + Fore.RESET