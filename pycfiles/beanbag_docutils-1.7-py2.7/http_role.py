# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/beanbag_docutils/sphinx/ext/http_role.py
# Compiled at: 2018-06-14 23:50:40
"""Sphinx extension to add a :rst:role:`http` role for docs.

This extension makes it easy to reference HTTP status codes.

Setup
=====

To use this, you just need to add the extension in :file:`conf.py`::

    extensions = [
        ...
        'beanbag_docutils.sphinx.ext.http_role',
        ...
    ]

Roles
=====

.. rst:directive:: http-status-codes-format

   Specifies a new format to use by default for any :rst:role:`http` roles.
   This should include ``%(code)s`` for the numeric code and ``%(name)s``
   for the name of the HTTP status code.

   Call this again without an argument to use the default format.

.. rst:role:: http

   References an HTTP status code, expanding to the full status name and
   linking to documentation on the status in the process.

Configuration
=============

``http_status_codes_format``:
    The format string used for the titles for HTTP status codes. This
    defaults to ``HTTP %(code)s %(format)s`` and can be temporarily
    overridden using :rst:directive:`http-status-codes-format`.

``http_status_codes_url``:
    The location of the docs for the status codes. This expects a string with a
    ``%s``, which will be replaced by the numeric HTTP status code.
"""
from __future__ import unicode_literals
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.nodes import split_explicit_title
DEFAULT_HTTP_STATUS_CODES_URL = b'http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#%s'
DEFAULT_HTTP_STATUS_CODES_FORMAT = b'HTTP %(code)s %(name)s'
HTTP_STATUS_CODES = {100: b'Continue', 
   101: b'Switching Protocols', 
   102: b'Processing', 
   200: b'OK', 
   201: b'Created', 
   202: b'Accepted', 
   203: b'Non-Authoritative Information', 
   204: b'No Content', 
   205: b'Reset Content', 
   206: b'Partial Content', 
   207: b'Multi-Status', 
   208: b'Already Reported', 
   300: b'Multiple Choices', 
   301: b'Moved Permanently', 
   302: b'Found', 
   303: b'See Other', 
   304: b'Not Modified', 
   305: b'Use Proxy', 
   306: b'Switch Proxy', 
   307: b'Temporary Redirect', 
   308: b'Permanent Redirect', 
   400: b'Bad Request', 
   401: b'Unauthorized', 
   402: b'Payment Required', 
   403: b'Forbidden', 
   404: b'Not Found', 
   405: b'Method Not Allowed', 
   406: b'Not Acceptable', 
   407: b'Proxy Authentication Required', 
   408: b'Request Timeout', 
   409: b'Conflict', 
   410: b'Gone', 
   411: b'Length Required', 
   412: b'Precondition Failed', 
   413: b'Request Entity Too Large', 
   414: b'Request-URI Too Long', 
   415: b'Unsupported Media Type', 
   416: b'Requested Range Not Satisfiable', 
   417: b'Expectation Failed', 
   418: b'I\\m a teapot', 
   422: b'Unprocessable Entity', 
   423: b'Locked', 
   424: b'Failed Dependency', 
   425: b'Unordered Collection', 
   426: b'Upgrade Required', 
   428: b'Precondition Required', 
   429: b'Too Many Requests', 
   431: b'Request Header Fields Too Large', 
   444: b'No Response', 
   449: b'Retry With', 
   450: b'Blocked by Windows Parental Controls', 
   451: b'Unavailable For Legal Reasons', 
   499: b'Client Closed Request', 
   500: b'Internal Server Error', 
   501: b'Not Implemented', 
   502: b'Bad Gateway', 
   503: b'Service Unavailable', 
   504: b'Gateway Timeout', 
   505: b'HTTP Version Not Supported', 
   506: b'Variant Also Negotiates', 
   507: b'Insufficient Storage', 
   508: b'Loop Detected', 
   509: b'Bandwidth Limit Exceeded', 
   510: b'Not Extended', 
   511: b'Network Authentication Required', 
   598: b'Network Read Timeout Error', 
   599: b'Network Connect Timeout Error'}

class SetStatusCodesFormatDirective(Directive):
    """Specifies the format to use for the ``:http:`` role's text."""
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self):
        """Run the directive.

        Returns:
            list:
            An empty list, always.
        """
        temp_data = self.state.document.settings.env.temp_data
        if len(self.arguments):
            temp_data[b'http-status-codes-format'] = self.arguments[0]
        else:
            temp_data.pop(b'http-status-codes-format', None)
        return []


def http_role(role, rawtext, text, linenum, inliner, options={}, content=[]):
    """Implementation of the :rst:role:`http` role.

    This is responsible for converting a HTTP status code to link pointing to
    the status documentation, with the full text for the status name.

    Args:
        rawtext (unicode):
            The raw text for the entire role.

        text (unicode):
            The interpreted text content.

        linenum (int):
            The current line number.

        inliner (docutils.parsers.rst.states.Inliner):
            The inliner used for error reporting and document tree access.

        options (dict):
            Options passed for the role. This is unused.

        content (list of unicode):
            The list of strings containing content for the role directive.
            This is unused.

    Returns:
        tuple:
        The result of the role. It's a tuple containing two items:

        1) A single-item list with the resulting node.
        2) A single-item list with the error message (if any).
    """
    has_explicit_title, title, target = split_explicit_title(text)
    try:
        status_code = int(target)
        if status_code not in HTTP_STATUS_CODES:
            raise ValueError
    except ValueError:
        msg = inliner.reporter.error(b'HTTP status code must be a valid HTTP status; "%s" is invalid.' % target, line=linenum)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return ([prb], [msg])

    env = inliner.document.settings.env
    http_status_codes_url = env.config.http_status_codes_url
    if not http_status_codes_url or b'%s' not in http_status_codes_url:
        msg = inliner.reporter.error(b'http_status_codes_url must be configured.', line=linenum)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return (
         [
          prb], [msg])
    ref = http_status_codes_url % status_code
    if has_explicit_title:
        status_code_text = title
    else:
        http_status_codes_format = env.temp_data.get(b'http-status-codes-format') or env.config.http_status_codes_format
        status_code_text = http_status_codes_format % {b'code': status_code, 
           b'name': HTTP_STATUS_CODES[status_code]}
    node = nodes.reference(rawtext, status_code_text, refuri=ref, **options)
    return (
     [
      node], [])


def setup(app):
    """Set up the Sphinx extension.

    This registers the :rst:role:`http` role,
    :rst:directive:`http-status-codes-format` directive, and the configuration
    settings for specifying the format and URL for linking to HTTP status
    codes.

    Args:
        app (sphinx.application.Sphinx):
            The Sphinx application to register roles and configuration on.
    """
    app.add_config_value(b'http_status_codes_format', DEFAULT_HTTP_STATUS_CODES_FORMAT, True)
    app.add_config_value(b'http_status_codes_url', DEFAULT_HTTP_STATUS_CODES_URL, True)
    app.add_directive(b'http-status-codes-format', SetStatusCodesFormatDirective)
    app.add_role(b'http', http_role)