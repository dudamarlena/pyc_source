# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yamlog/logger.py
# Compiled at: 2010-02-11 09:00:29
"""
logger - return a logging instance already configured.
setup - setup the logging.
teardown - tear down the logging.
"""
__all__ = [
 'logger', 'setup', 'teardown']
from logging import handlers
import logging, os, platform, textwrap

class _LoggerAdapter(logging.LoggerAdapter):
    """Prepend an indentation to the logging message.

    Subclass `LoggerAdapter` and override `process()`.

    """
    SPACE = '  '
    wrapper = textwrap.TextWrapper(initial_indent=SPACE, subsequent_indent=SPACE)

    def process(self, msg, kwargs):
        kwargs['extra'] = self.extra
        return (self.wrapper.fill(msg), kwargs)


class _LoggerExtra(object):
    """The `extra` context information passed to `LoggerAdapter`."""
    host = platform.node()

    def __getitem__(self, name):
        """Allow this instance to look like a dict."""
        if name == 'host':
            result = self.host
        return result

    def __iter__(self):
        """Allow iteration over keys.

        They which will be merged into the `LogRecord` dictionary before
        formatting and output.

        """
        keys = [
         'host']
        keys.extend(self.__dict__.keys())
        return iter(keys)


def logger(name):
    """Return an instance of `LoggerAdapter` with the extra fields."""
    return _LoggerAdapter(logging.getLogger(name), _LoggerExtra())


def setup(filename='/tmp/python.log'):
    """Configure the logging.

    ...

    Parameters
    ----------
    filename : str
        The file name where logs are going to be written.
        Default is */tmp/python.log*.

    See Also
    --------
    teardown

    Notes
    -----
    Use the date and time international format:
        http://www.w3.org/TR/NOTE-datetime

    Could be used the directory */var/log* but there would be to run it
    as an user with permissions to write there.

    """
    if os.path.isdir(os.path.dirname(filename)):
        filename_ = filename
    else:
        filename_ = '/' + os.path.basename(filename)
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    file_handler = handlers.RotatingFileHandler(filename_, maxBytes=131072, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    yaml_formatter = logging.Formatter('---\nDate-Time: %(asctime)s\nHost: %(host)s\nName: %(name)s\n%(levelname)s:\n%(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
    file_handler.setFormatter(yaml_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    simple_formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logging.logProcesses = 0
    logging.logThreads = 0


def teardown():
    """Flush and close all handlers of logging.

    ...

    See Also
    --------
    setup

    """
    logging.shutdown()