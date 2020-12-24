# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/flake8/flake8/statistics.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 4695 bytes
"""Statistic collection logic for Flake8."""
import collections
from typing import Dict, Generator, List, Optional

class Statistics(object):
    __doc__ = 'Manager of aggregated statistics for a run of Flake8.'

    def __init__(self):
        """Initialize the underlying dictionary for our statistics."""
        self._store = {}

    def error_codes(self):
        """Return all unique error codes stored.

        :returns:
            Sorted list of error codes.
        :rtype:
            list(str)
        """
        return sorted({key.code for key in self._store})

    def record(self, error):
        """Add the fact that the error was seen in the file.

        :param error:
            The Violation instance containing the information about the
            violation.
        :type error:
            flake8.style_guide.Violation
        """
        key = Key.create_from(error)
        if key not in self._store:
            self._store[key] = Statistic.create_from(error)
        self._store[key].increment()

    def statistics_for(self, prefix, filename=None):
        """Generate statistics for the prefix and filename.

        If you have a :class:`Statistics` object that has recorded errors,
        you can generate the statistics for a prefix (e.g., ``E``, ``E1``,
        ``W50``, ``W503``) with the optional filter of a filename as well.

        .. code-block:: python

            >>> stats = Statistics()
            >>> stats.statistics_for('E12',
                                     filename='src/flake8/statistics.py')
            <generator ...>
            >>> stats.statistics_for('W')
            <generator ...>

        :param str prefix:
            The error class or specific error code to find statistics for.
        :param str filename:
            (Optional) The filename to further filter results by.
        :returns:
            Generator of instances of :class:`Statistic`
        """
        matching_errors = sorted(key for key in self._store if key.matches(prefix, filename))
        for error_code in matching_errors:
            yield self._store[error_code]


class Key(collections.namedtuple('Key', ['filename', 'code'])):
    __doc__ = 'Simple key structure for the Statistics dictionary.\n\n    To make things clearer, easier to read, and more understandable, we use a\n    namedtuple here for all Keys in the underlying dictionary for the\n    Statistics object.\n    '
    __slots__ = ()

    @classmethod
    def create_from(cls, error):
        """Create a Key from :class:`flake8.style_guide.Violation`."""
        return cls(filename=(error.filename), code=(error.code))

    def matches(self, prefix, filename):
        """Determine if this key matches some constraints.

        :param str prefix:
            The error code prefix that this key's error code should start with.
        :param str filename:
            The filename that we potentially want to match on. This can be
            None to only match on error prefix.
        :returns:
            True if the Key's code starts with the prefix and either filename
            is None, or the Key's filename matches the value passed in.
        :rtype:
            bool
        """
        return self.code.startswith(prefix) and (filename is None or self.filename == filename)


class Statistic(object):
    __doc__ = 'Simple wrapper around the logic of each statistic.\n\n    Instead of maintaining a simple but potentially hard to reason about\n    tuple, we create a namedtuple which has attributes and a couple\n    convenience methods on it.\n    '

    def __init__(self, error_code, filename, message, count):
        """Initialize our Statistic."""
        self.error_code = error_code
        self.filename = filename
        self.message = message
        self.count = count

    @classmethod
    def create_from(cls, error):
        """Create a Statistic from a :class:`flake8.style_guide.Violation`."""
        return cls(error_code=(error.code),
          filename=(error.filename),
          message=(error.text),
          count=0)

    def increment(self):
        """Increment the number of times we've seen this error in this file."""
        self.count += 1