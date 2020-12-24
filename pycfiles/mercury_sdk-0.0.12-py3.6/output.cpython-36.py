# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_sdk/mcli/output.py
# Compiled at: 2018-11-06 13:31:04
# Size of source mod 2**32: 1015 bytes
import logging, pkg_resources, sys, colorama
FORMAT = '%(message)s'
program_version = pkg_resources.get_distribution('mercury-sdk').version
LOG = logging.getLogger(__name__)

def setup_logging(verbosity):
    verbosity_map = {0:logging.ERROR, 
     1:logging.WARNING, 
     2:logging.INFO, 
     3:logging.DEBUG}
    logging.basicConfig(format=FORMAT, level=(verbosity_map.get(verbosity, logging.DEBUG)))


def print_basic_info(configuration):
    LOG.warning(f"{format_version()}\nConfiguration file: {colorama.Fore.MAGENTA}{configuration.get('config_file')}{colorama.Style.RESET_ALL}\nMercury URL: {configuration.get('mercury_url')}")


def format_version():
    return f"SDK Version: {colorama.Fore.GREEN}{program_version}{colorama.Style.RESET_ALL}"


def print_and_exit(message, code=0):
    print(message)
    sys.exit(code)