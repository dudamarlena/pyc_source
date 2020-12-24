# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/safelog.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = 'Filters for log sanitisation.\n\n.. inheritance-diagram:: BaseSafelogFilter SafelogEmailFilter SafelogIPv4Filter SafelogIPv6Filter\n    :parts: 1\n\nThe ``Safelog*Filter`` classes within this module can be instantiated and\nadding to any :class:`logging.Handler`, in order to transparently filter\nsubstrings within log messages which match the given ``pattern``. Matching\nsubstrings may be optionally additionally validated by implementing the\n:meth:`~BaseSafelogFilter.doubleCheck` method before they are finally replaced\nwith the ``replacement`` string. For example::\n\n    >>> import io\n    >>> import logging\n    >>> from bridgedb import safelog\n    >>> handler = logging.StreamHandler(io.BytesIO())\n    >>> logger = logging.getLogger()\n    >>> logger.addHandler(handler)\n    >>> logger.addFilter(safelog.SafelogEmailFilter())\n    >>> logger.info("Sent response email to: blackhole@torproject.org")\n\n..\n\n**Module Overview:**\n\n::\n\n bridgedb.safelog\n  |\n  |_ setSafeLogging - Enable or disable safelogging globally.\n  |_ logSafely - Utility for manually sanitising a portion of a log message\n  |\n  \\_ BaseSafelogFilter - Base class for log message sanitisation filters\n     |   |_ doubleCheck - Optional stricter validation on matching substrings\n     |   \\_ filter - Determine if some part of a log message should be filtered\n     |\n     |_ SafelogEmailFilter - Filter for removing email addresses from logs\n     |_ SafelogIPv4Filter - Filter for removing IPv4 addresses from logs\n     |_ SafelogIPv6Filter - Filter for removing IPv6 addresses from logs\n\n..\n'
import functools, logging, re
from bridgedb.parse import addr
safe_logging = True

def setSafeLogging(safe):
    """Enable or disable automatic filtering of log messages.

    :param bool safe: If ``True``, filter email and IP addresses from log
        messages automagically.
    """
    global safe_logging
    safe_logging = safe


def logSafely(string):
    """Utility for manually sanitising a portion of a log message.

    :param str string: If ``SAFELOGGING`` is enabled, sanitise this **string**
        by replacing it with ``"[scrubbed]"``. Otherwise, return the
        **string** unchanged.
    :rtype: str
    :returns: ``"[scrubbed]"`` or the original string.
    """
    if safe_logging:
        return '[scrubbed]'
    return string


class BaseSafelogFilter(logging.Filter):
    u"""Base class for creating log message sanitisation filters.

    A :class:`BaseSafelogFilter` uses a compiled regex :attr:`pattern` to
    match particular items of data in log messages which should be sanitised
    (if ``SAFELOGGING`` is enabled in :file:`bridgedb.conf`).

    .. note::
        The :attr:`pattern` is used only for string *matching* purposes, and
        *not* for validation. In other words, a :attr:`pattern` which matches
        email addresses should simply match something which appears to be an
        email address, even though that matching string might not technically
        be a valid email address vis-á-vis :rfc:`5321`.

    In addition, a ``BaseSafelogFilter`` uses a :attr:`easyFind`, which is
    simply a string or character to search for before running checking against
    the regular expression, to attempt to avoid regexing *everything* which
    passes through the logger.

    :cvar pattern: A compiled regular expression, whose matches will be
        scrubbed from log messages and replaced with :attr:`replacement`.
    :vartype easyFind: str
    :cvar easyFind: A simpler string to search for before to match by regex.
    :vartype replacement: str
    :cvar replacement: The string to replace ``pattern`` matches
        with. (default: ``"[scrubbed]"``)
    """
    pattern = re.compile('FILTERME')
    easyFind = 'FILTERME'
    replacement = '[scrubbed]'

    def doubleCheck(self, match):
        """Subclasses should override this function to implement any additional
        substring filtering to decrease the false positive rate, i.e. any
        additional filtering or validation which is *more* costly than
        checking against the regular expression, :attr:`pattern`.

        To use only the :attr:`pattern` matching in :meth:`filter`, and not
        use this method, simply do::

            return True

        :param str match: Some portion of the :ivar:`logging.LogRecord.msg`
            string which has already passed the checks in :meth:`filter`, for
            which additional validation/checking is required.
        :rtype: bool
        :returns: ``True`` if the additional validation passes (in other
            words, the **match** *should* be filtered), and ``None`` or
            ``False`` otherwise.
        """
        return True

    def filter(self, record):
        """Filter a log record.

        The log **record** is filtered, and thus sanitised by replacing
        matching substrings with the :attr:`replacement` string, if the
        following checks pass:

        1. ``SAFELOGGING`` is currently enabled.
        2. The ``record.msg`` string contains :attr:`easyFind`.
        3. The ``record.msg`` matches the regular expression, :attr:`pattern`.

        :type record: :class:`logging.LogRecord`
        :param record: Basically, anything passed to :func:`logging.log`.
        """
        if safe_logging:
            msg = str(record.msg)
            if msg.find(self.easyFind) > 0:
                matches = self.pattern.findall(msg)
                for match in matches:
                    if self.doubleCheck(match):
                        msg = msg.replace(match, self.replacement)

            record.msg = msg
        return record


class SafelogEmailFilter(BaseSafelogFilter):
    """A log filter which removes email addresses from log messages."""
    pattern = re.compile('([a-zA-Z0-9]+[.+a-zA-Z0-9]*[@]{1}[a-zA-Z0-9]+[.-a-zA-Z0-9]*[.]{1}[a-zA-Z]+)')
    easyFind = '@'

    @functools.wraps(BaseSafelogFilter.filter)
    def filter(self, record):
        return BaseSafelogFilter.filter(self, record)


class SafelogIPv4Filter(BaseSafelogFilter):
    """A log filter which removes IPv4 addresses from log messages."""
    pattern = re.compile('(?:\\d{1,3}\\.?){4}')
    easyFind = '.'

    def doubleCheck(self, match):
        """Additional check to ensure that **match** is an IPv4 address."""
        if addr.isIPv4(match):
            return True

    @functools.wraps(BaseSafelogFilter.filter)
    def filter(self, record):
        return BaseSafelogFilter.filter(self, record)


class SafelogIPv6Filter(BaseSafelogFilter):
    """A log filter which removes IPv6 addresses from log messages."""
    pattern = re.compile('([:]?[a-fA-F0-9:]+[:]+[a-fA-F0-9:]+){1,8}')
    easyFind = ':'

    def doubleCheck(self, match):
        """Additional check to ensure that **match** is an IPv6 address."""
        if addr.isIPv6(match):
            return True

    @functools.wraps(BaseSafelogFilter.filter)
    def filter(self, record):
        return BaseSafelogFilter.filter(self, record)