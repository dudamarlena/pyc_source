# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/html_parser.py
# Compiled at: 2019-02-14 00:35:17
from django.utils import six
from django.utils.six.moves import html_parser as _html_parser
try:
    HTMLParseError = _html_parser.HTMLParseError
except AttributeError:

    class HTMLParseError(Exception):
        pass


if six.PY3:

    class HTMLParser(_html_parser.HTMLParser):
        """Explicitly set convert_charrefs to be False.

        This silences a deprecation warning on Python 3.4, but we can't do
        it at call time because Python 2.7 does not have the keyword
        argument.
        """

        def __init__(self, convert_charrefs=False, **kwargs):
            _html_parser.HTMLParser.__init__(self, convert_charrefs=convert_charrefs, **kwargs)


else:
    HTMLParser = _html_parser.HTMLParser