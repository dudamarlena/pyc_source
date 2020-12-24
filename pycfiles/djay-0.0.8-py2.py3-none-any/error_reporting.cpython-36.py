# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/utils/error_reporting.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 8362 bytes
"""
Error reporting should be safe from encoding/decoding errors.
However, implicit conversions of strings and exceptions like

>>> u'%s world: %s' % ('Hällo', Exception(u'Hällo')

fail in some Python versions:

* In Python <= 2.6, ``unicode(<exception instance>)`` uses
  `__str__` and fails with non-ASCII chars in`unicode` arguments.
  (work around http://bugs.python.org/issue2517):

* In Python 2, unicode(<exception instance>) fails, with non-ASCII
  chars in arguments. (Use case: in some locales, the errstr
  argument of IOError contains non-ASCII chars.)

* In Python 2, str(<exception instance>) fails, with non-ASCII chars
  in `unicode` arguments.

The `SafeString`, `ErrorString` and `ErrorOutput` classes handle
common exceptions.
"""
import sys, codecs
try:
    import locale
except ImportError:
    locale_encoding = None
else:
    try:
        locale_encoding = locale.getlocale()[1] or locale.getdefaultlocale()[1]
    except ValueError as error:
        if 'unknown locale: UTF-8' in error.args:
            locale_encoding = 'UTF-8'
        else:
            locale_encoding = None
    except:
        locale_encoding = None

    try:
        codecs.lookup(locale_encoding or '')
    except LookupError:
        locale_encoding = None

    class SafeString(object):
        __doc__ = '\n    A wrapper providing robust conversion to `str` and `unicode`.\n    '

        def __init__(self, data, encoding=None, encoding_errors='backslashreplace', decoding_errors='replace'):
            self.data = data
            self.encoding = encoding or getattr(data, 'encoding', None) or locale_encoding or 'ascii'
            self.encoding_errors = encoding_errors
            self.decoding_errors = decoding_errors

        def __str__(self):
            try:
                return str(self.data)
            except UnicodeEncodeError:
                if isinstance(self.data, Exception):
                    args = [str(SafeString(arg, self.encoding, self.encoding_errors)) for arg in self.data.args]
                    return ', '.join(args)
                if isinstance(self.data, str):
                    if sys.version_info > (3, 0):
                        return self.data
                    else:
                        return self.data.encode(self.encoding, self.encoding_errors)
                raise

        def __unicode__(self):
            """
        Return unicode representation of `self.data`.

        Try ``unicode(self.data)``, catch `UnicodeError` and

        * if `self.data` is an Exception instance, work around
          http://bugs.python.org/issue2517 with an emulation of
          Exception.__unicode__,

        * else decode with `self.encoding` and `self.decoding_errors`.
        """
            try:
                u = str(self.data)
                if isinstance(self.data, EnvironmentError):
                    u = u.replace(": u'", ": '")
                return u
            except UnicodeError as error:
                if isinstance(self.data, EnvironmentError):
                    return "[Errno %s] %s: '%s'" % (self.data.errno,
                     SafeString(self.data.strerror, self.encoding, self.decoding_errors),
                     SafeString(self.data.filename, self.encoding, self.decoding_errors))
                else:
                    if isinstance(self.data, Exception):
                        args = [str(SafeString(arg, (self.encoding), decoding_errors=(self.decoding_errors))) for arg in self.data.args]
                        return ', '.join(args)
                    if isinstance(error, UnicodeDecodeError):
                        return str(self.data, self.encoding, self.decoding_errors)
                raise


    class ErrorString(SafeString):
        __doc__ = '\n    Safely report exception type and message.\n    '

        def __str__(self):
            return '%s: %s' % (self.data.__class__.__name__,
             super(ErrorString, self).__str__())

        def __unicode__(self):
            return '%s: %s' % (self.data.__class__.__name__,
             super(ErrorString, self).__unicode__())


    class ErrorOutput(object):
        __doc__ = '\n    Wrapper class for file-like error streams with\n    failsave de- and encoding of `str`, `bytes`, `unicode` and\n    `Exception` instances.\n    '

        def __init__(self, stream=None, encoding=None, encoding_errors='backslashreplace', decoding_errors='replace'):
            """
        :Parameters:
            - `stream`: a file-like object,
                        a string (path to a file),
                        `None` (write to `sys.stderr`, default), or
                        evaluating to `False` (write() requests are ignored).
            - `encoding`: `stream` text encoding. Guessed if None.
            - `encoding_errors`: how to treat encoding errors.
        """
            if stream is None:
                stream = sys.stderr
            else:
                if not stream:
                    stream = False
                else:
                    if isinstance(stream, str):
                        stream = open(stream, 'w')
                    else:
                        if isinstance(stream, str):
                            stream = open(stream.encode(sys.getfilesystemencoding()), 'w')
            self.stream = stream
            self.encoding = encoding or getattr(stream, 'encoding', None) or locale_encoding or 'ascii'
            self.encoding_errors = encoding_errors
            self.decoding_errors = decoding_errors

        def write(self, data):
            """
        Write `data` to self.stream. Ignore, if self.stream is False.

        `data` can be a `string`, `unicode`, or `Exception` instance.
        """
            if self.stream is False:
                return
            else:
                if isinstance(data, Exception):
                    data = str(SafeString(data, self.encoding, self.encoding_errors, self.decoding_errors))
                try:
                    self.stream.write(data)
                except UnicodeEncodeError:
                    self.stream.write(data.encode(self.encoding, self.encoding_errors))
                except TypeError:
                    if isinstance(data, str):
                        self.stream.write(data.encode(self.encoding, self.encoding_errors))
                        return
                    else:
                        if self.stream in (sys.stderr, sys.stdout):
                            self.stream.buffer.write(data)
                        else:
                            self.stream.write(str(data, self.encoding, self.decoding_errors))

        def close(self):
            """
        Close the error-output stream.

        Ignored if the stream is` sys.stderr` or `sys.stdout` or has no
        close() method.
        """
            if self.stream in (sys.stdout, sys.stderr):
                return
            try:
                self.stream.close()
            except AttributeError:
                pass