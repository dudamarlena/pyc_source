# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\deprecations.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1327 bytes
from warnings import warn
from chatette_qiu.utils import print_warn
_SEMICOLON_COMMENTS_DEPRECATION_WARNED = False

def warn_semicolon_comments():
    """
    Warns the user on stdout that one of their files contains semicolons
    comments (which are a deprecated way of making comments).
    Rather use '//' comments instead of ';' comments.
    """
    global _SEMICOLON_COMMENTS_DEPRECATION_WARNED
    if not _SEMICOLON_COMMENTS_DEPRECATION_WARNED:
        print_warn("Comments starting with a semi-colon ';' are " + "now deprecated. Rather use the new double slash '//'" + ' syntax. This syntax allows to have a syntax closer to ' + 'Chatito v2.1.x.')
        warn("Comments starting with a semi-colon ';' are now deprecated. " + "Rather use the new double slash '//' syntax. This " + 'syntax allows to have a syntax closer to Chatito v2.1.x.', DeprecationWarning)
        _SEMICOLON_COMMENTS_DEPRECATION_WARNED = True