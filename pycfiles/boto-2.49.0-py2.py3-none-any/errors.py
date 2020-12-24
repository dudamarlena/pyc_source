# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/errors.py
# Compiled at: 2012-08-16 08:05:32
__doc__ = '\nCustom error handlers\n'
import warnings

class BotneeException(Exception):

    def __init__(self, value, logger=None):
        self.parameter = value
        if logger and value:
            logger.error(value)

    def __str__(self):
        return repr(self.parameter)


class BotneeWarning(object):

    def __init__(self, message, logger=None):
        if message:
            warnings.warn(message)
            if logger:
                logger.warn(message)


class EngineError(BotneeException):
    """Custom error handler for engine class"""


class EngineWarning(BotneeWarning):
    """Custom warning handler for engine class"""


class DocManagerError(BotneeException):
    """Custom error handler for document store"""


class DocStoreError(BotneeException):
    """Custom error handler for document store"""


class DocStoreWarning(BotneeWarning):
    """Custom warning handler for the document store"""


class ProcessError(BotneeException):
    """Custom error handler for the process module"""


class ProcessWarning(BotneeWarning):
    """Custom warning handler for the process module"""


class StandardDocumentError(BotneeException):
    """Custom error handler for standard document io"""


class GetRelatedError(BotneeException):
    """Custom error handler for GetRelated"""


class GetRelatedWarning(BotneeWarning):
    """Custom warning handler for GetRelated"""


class FiltersWarning(BotneeWarning):
    """Custom warning handler for Filters"""


class RssWriterWarnging(BotneeWarning):
    """Custom warning handler for rss_writer"""