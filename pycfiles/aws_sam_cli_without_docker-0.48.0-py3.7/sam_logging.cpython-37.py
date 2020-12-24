# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/sam_logging.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1195 bytes
"""
Configures a logger
"""
import logging

class SamCliLogger:

    @staticmethod
    def configure_logger(logger, formatter, level):
        """
        Configure a Logger with the formatter provided.

        Parameters
        ----------
        logger logging.getLogger
            Logger to configure
        formatter logging.formatter
            Formatter for the logger

        Returns
        -------
        None
        """
        log_stream_handler = logging.StreamHandler()
        log_stream_handler.setLevel(logging.DEBUG)
        log_stream_handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.propagate = False
        logger.addHandler(log_stream_handler)

    @staticmethod
    def configure_null_logger(logger):
        """
        Configure a Logger with a NullHandler

        Useful for libraries that do not follow: https://docs.python.org/3.6/howto/logging.html#configuring-logging-for-a-library

        Parameters
        ----------
        logger logging.getLogger
            Logger to configure

        Returns
        -------
        None
        """
        logger.propagate = False
        logger.addHandler(logging.NullHandler())