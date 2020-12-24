# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/logger.py
# Compiled at: 2014-01-14 18:58:51
"""
Remote logging API.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'Logger']
from .config import Config
from ..messaging.codes import MessageType, MessageCode, MessagePriority

class Logger(object):
    """
    Logging API for plugins.

    Plugins should use this class instead of a simple `print`,
    otherwise messages will not be logged by GoLismero.

    Example:
       >>> Logger.log("My log message with information")
       >>> Logger.log_error("My log with error information")
       >>> Logger.log_verbose("Log message to display only when verbose mode is enabled")
    """
    DISABLED = 0
    STANDARD = 1
    VERBOSE = 2
    MORE_VERBOSE = 3

    def __new__(cls, *args, **kwargs):
        """
        .. warning: This is a static class, do not try to instance it!
        """
        raise NotImplementedError('This is a static class!')

    @classmethod
    def _log(cls, message, level, is_error=False):
        """
        Send a log message with the specified level and error status.

        :param message: Message to write.
        :type message: str
        """
        if not isinstance(message, basestring):
            message = str(message)
        Config._context.send_msg(message_type=MessageType.MSG_TYPE_CONTROL, message_code=MessageCode.MSG_CONTROL_LOG, message_info=(
         message, level, is_error), priority=MessagePriority.MSG_PRIORITY_HIGH)

    @classmethod
    def log(cls, message):
        """
        Send a log message of STANDARD level.

        :param message: Message to write.
        :type message: str
        """
        cls._log(message, cls.STANDARD, is_error=False)

    @classmethod
    def log_verbose(cls, message):
        """
        Send a log message of VERBOSE level.

        :param message: Message to write.
        :type message: str
        """
        cls._log(message, cls.VERBOSE, is_error=False)

    @classmethod
    def log_more_verbose(cls, message):
        """
        Send a log message of MORE_VERBOSE level.

        :param message: Message to write.
        :type message: str
        """
        cls._log(message, cls.MORE_VERBOSE, is_error=False)

    @classmethod
    def log_error(cls, message):
        """
        Send an error log message of STANDARD level.

        :param message: Message to write.
        :type message: str
        """
        cls._log(message, cls.STANDARD, is_error=True)

    @classmethod
    def log_error_verbose(cls, message):
        """
        Send an error log message of VERBOSE level.

        :param message: Message to write.
        :type message: str
        """
        cls._log(message, cls.VERBOSE, is_error=True)

    @classmethod
    def log_error_more_verbose(cls, message):
        """
        Send an error log message of MORE_VERBOSE level.

        :param message: Message to write.
        :type message: str
        """
        cls._log(message, cls.MORE_VERBOSE, is_error=True)