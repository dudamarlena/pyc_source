# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/common/logging/verbosity.py
# Compiled at: 2016-10-20 13:56:51
# Size of source mod 2**32: 1914 bytes
"""
Basic console logging based on verbosity
"""
import logging, logging.handlers
from ZConfig.matcher import SectionValue
from dhcpkit.common.server.logging import DEBUG_HANDLING, DEBUG_PACKETS
from dhcpkit.common.server.logging.config_datatypes import logging_level

def set_verbosity_logger(logger: logging.Logger, verbosity: int, existing_console: logging.Handler=None):
    """
    Install a console based logger based based on the given verbosity.

    :param logger: The logger to add the handlers to
    :param verbosity: The verbosity level given as command line argument
    :param existing_console: The existing console handler
    """
    logger.setLevel(logging.NOTSET)
    if existing_console:
        console = existing_console
    else:
        from dhcpkit.common.server.logging.config_elements import ConsoleHandlerFactory
        fake_section = SectionValue(name='', values={'level': logging_level('error'),  'color': None}, matcher=None)
        console_factory = ConsoleHandlerFactory(fake_section)
        console = console_factory()
        logger.addHandler(console)
    if verbosity >= 5:
        if console.level > DEBUG_PACKETS:
            console.setLevel(DEBUG_PACKETS)
    if verbosity >= 4:
        if console.level > DEBUG_HANDLING:
            console.setLevel(DEBUG_HANDLING)
    if verbosity >= 3 and console.level > logging.DEBUG:
        console.setLevel(logging.DEBUG)
    else:
        if verbosity == 2 and console.level > logging.INFO:
            console.setLevel(logging.INFO)
        else:
            if verbosity >= 1 and console.level > logging.WARNING:
                console.setLevel(logging.WARNING)
            elif console.level > logging.CRITICAL:
                console.setLevel(logging.CRITICAL)