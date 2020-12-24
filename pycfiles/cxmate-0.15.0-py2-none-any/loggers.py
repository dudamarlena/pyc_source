# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/loggers.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Loggers is a set of Logging classes used to capture output.\n\nThe most commonly used loggers are StandardOutLogger and FileLogger.\nAdditionally, these loggers can be combined to write output to more than one\ntarget.\n\n'
import os, pprint, datetime, traceback
LL_DEBUG = 4
LL_INFO = 3
LL_WARN = 2
LL_ERROR = 1
LL_NONE = 0
DEFAULT_LL = LL_INFO

class Logger(object):
    """Base class for all loggers.

    To create a custom logger, inherit from this class, and implement
    the write() method so that it writes message in the appropriate manner.

    >>> # To use this class for inheritance ...
    >>> from cxmanage_api.loggers import Logger
    >>>

    :param log_level: Verbosity level of logging for this logger.
    :type log_level: integer
    :param time_stamp: Flag to determine toggle time_stamping each log entry.
    :type time_stamp: boolean
    :param component: Component tag for the log entry.
    :type component: string

    .. note::
        * This class is not intended to be used as a logger itself.
        * Only the **write()** method needs to be implemeneted for your custom
          logger.
        * Log Levels: DEBUG=4, INFO=3, WARN=2, ERROR=1, NONE=0
        * You can turn OFF entry time_stamping by initializing a logger with:
          **time_stamp=False**

    """

    def __init__(self, log_level=DEFAULT_LL, time_stamp=True, component=None):
        """Default constructor for the Logger class."""
        self.log_level = log_level
        self.time_stamp = time_stamp
        if component:
            self.component = '| ' + component
        else:
            self.component = ''

    def _get_log(self, msg, level_tag):
        """Used internally to create an appropriate log message string.

        :param msg: The message to write.
        :type msg: string
        :param level_tag: The log level string, e.g. INFO, DEBUG, WARN, etc.
        :type level_tag: string

        """
        lines = pprint.pformat(msg).splitlines()
        if len(lines) == 1:
            lines = str(msg).splitlines()
        result = []
        for line in lines:
            if self.time_stamp:
                ts_now = str(datetime.datetime.now())
                result.append('%s %s | %s : %s' % (
                 ts_now, self.component, level_tag, line))
            else:
                result.append('%s %s : %s' % (
                 self.component, level_tag, line))

        return ('\n').join(result)

    def write(self, message):
        """Writes a log message.

        .. warning::
            * This method is to be intentionally overridden.
            * Implemented by subclasses.

        :param message: The message to write..
        :type message: string

        :raises NotImplementedError: If write() is not overridden.

        """
        del message
        raise NotImplementedError

    def debug(self, message):
        """Log a message at DEBUG level. LL_DEBUG = 4

        >>> logger.debug('This is debug.')
        2012-12-19 11:13:04.329046  | DEBUG | This is debug.

        :param message: The message to write.
        :type message: string

        """
        if self.log_level >= LL_DEBUG:
            self.write(self._get_log(message, 'DEBUG'))

    def info(self, message):
        """Log a message at the INFO level. LL_INFO = 3

        >>> logger.info('This is informational.')
        2012-12-19 11:11:47.225859  | INFO | This is informational.

        :param message: The message to write.
        :type message: string

        """
        if self.log_level >= LL_INFO:
            self.write(self._get_log(msg=message, level_tag='INFO'))

    def warn(self, message):
        """Log a message at WARN level. LL_WARN = 2

        >>> logger.warn('This is a warning')
        2012-12-19 11:11:12.257814  | WARN | This is a warning

        :param message: The message to write.
        :type message: string

        """
        if self.log_level >= LL_WARN:
            self.write(self._get_log(msg=message, level_tag='WARN'))

    def error(self, message):
        """Log a message at ERROR level. LL_ERROR = 1

        >>> logger.error('This is an error.')
        2012-12-19 11:14:11.352735  | ERROR | This is an error.

        :param message: The message to write.
        :type message: string

        """
        if self.log_level >= LL_ERROR:
            self.write(self._get_log(msg=message, level_tag='ERROR'))


class StandardOutLogger(Logger):
    """A Logger class that writes to Standard Out (stdout).

    Only the write method has to be implemented.

    >>> # Typical instantiation ...
    >>> from cxmanage_api.loggers import StandardOutLogger
    >>> logger = StandardOutLogger()

    :param log_level: Level of logging for this logger.
    :type log_level: integer
    :param time_stamp: Flag to determine toggle time_stamping each log entry.
    :type time_stamp: boolean

    """

    def __init__(self, log_level=DEFAULT_LL, time_stamp=True, component=None):
        """Default constructor for a StandardOutLogger."""
        self.log_level = log_level
        self.time_stamp = time_stamp
        self.component = component
        super(StandardOutLogger, self).__init__(log_level=self.log_level, time_stamp=self.time_stamp, component=self.component)

    def write(self, message):
        """Writes a log message to standard out.

        >>> # It simply prints ...
        >>> logger.write('This function is called by the Base Class')
        This function is called by the Base Class
        >>>

        :param message: The message to write.
        :type message: string

        """
        print message


class FileLogger(Logger):
    """A logger that writes to a file.

    >>> # Typical instantiation ...
    >>> flogger = FileLogger(abs_path='/home/logfile.out')

    :param log_level: Level of logging for this logger.
    :type log_level: integer
    :param time_stamp: Flag to determine toggle time_stamping each log entry.
    :type time_stamp: boolean
    :param name: Name of this logger.
    :type name: string

    """

    def __init__(self, abs_path, time_stamp=True, component=None, log_level=DEFAULT_LL):
        """Default constructor for the FileLogger class."""
        super(FileLogger, self).__init__(log_level=log_level, time_stamp=time_stamp, component=component)
        self.path = abs_path
        try:
            if not os.path.exists(self.path):
                file(self.path, 'w').close()
        except Exception:
            raise

    def write(self, message):
        """Writes a log message to a log file.

        :param message: The message to write.
        :type message: string

        """
        try:
            try:
                old_umask = os.umask(0)
                with open(self.path, 'a') as (file_d):
                    file_d.write(message + '\n')
                    file_d.close()
            except Exception:
                self.error(traceback.format_exc())
                raise

        finally:
            os.umask(old_umask)
            if file_d:
                file_d.close()


class CompositeLogger(object):
    """Takes a list of loggers and writes the same output to them all.

    >>> from cxmanage_api.loggers import StandardOutLogger, FileLogger
    >>> # Let's say you want to log to a file while also seeing the output.
    >>> # Create a StandardOutLogger to 'see' output.
    >>> slogger = StandarOutLogger(...)
    >>> # Create a FileLogger to log to a file.
    >>> flogger = FileLogger(...)
    >>> from cxmanage_api.loggers import CompositeLogger
    >>> # Create a composite logger and you can log to both simultaneously!
    >>> logger = CompositeLogger(loggers=[slogger, flogger])

    :param loggers: A list of loggers to output to
    :type loggers: list
    :param log_level: The level to log at. DEFAULT: LL_INFO
    :type log_level: integer

    """

    def __init__(self, loggers, log_level=DEFAULT_LL):
        """Default constructor for the CompositeLogger class."""
        self.loggers = loggers
        self._log_level = log_level
        for logger in self.loggers:
            logger.log_level = log_level

    @property
    def log_level(self):
        """Returns the log_level for ALL loggers.

        >>> logger.log_level
        >>> 3

        :returns: The log_level for ALL loggers.
        :rtype: integer

        """
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        """Sets the log_level for ALL loggers.

        :param value: The value to set the log_level to.
        :type value: integer

        """
        self._log_level = value
        if not self._log_level:
            return
        for logger in self.loggers:
            logger.log_level = value

    def info(self, message):
        """Loga a message at the INFO level: LL_INFO = 3 for all loggers.

        >>> logger.info('This is informational.')
        2012-12-19 11:37:17.462879  | INFO | This is informational.

        :param message: The message to write.
        :type message: string

        """
        for logger in self.loggers:
            logger.info(message)

    def warn(self, message):
        """Log a message at WARN level: LL_WARN = 2 for all loggers.

        >>> logger.warn('This is a warning.')
        2012-12-19 11:37:50.614862  | WARN | This is a warning.

        :param message: The message to write.
        :type message: string

        """
        for logger in self.loggers:
            logger.warn(message)

    def error(self, message):
        """Log a message at ERROR level. LL_ERROR = 1 for all loggers.

        >>> logger.error('This is an ERROR!')
        2012-12-19 11:41:18.181123  | ERROR | This is an ERROR!

        :param message: The message to write.
        :type message: string

        """
        for logger in self.loggers:
            logger.error(message)

    def debug(self, message):
        """
        Log a message at DEBUG level. LL_DEBUG = 4 for all loggers.

        >>> logger.debug('This is a DEBUG log entry. Message goes here')

        :param message: The message to write.
        :type message: string

        """
        for logger in self.loggers:
            logger.debug(message)