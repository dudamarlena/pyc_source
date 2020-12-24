# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/sourcecode.py
# Compiled at: 2019-08-19 15:09:29
"""Source code text utilities"""
__all__ = [
 'get_eol_chars', 'get_os_name_from_eol_chars',
 'get_eol_chars_from_os_name', 'has_mixed_eol_chars',
 'fix_indentation']
__docformat__ = 'restructuredtext'
EOL_CHARS = (
 ('\r\n', 'nt'), ('\n', 'posix'), ('\r', 'mac'))

def get_eol_chars(text):
    """Get text EOL characters"""
    for eol_chars, _os_name in EOL_CHARS:
        if text.find(eol_chars) > -1:
            return eol_chars


def get_os_name_from_eol_chars(eol_chars):
    """Return OS name from EOL characters"""
    for chars, os_name in EOL_CHARS:
        if eol_chars == chars:
            return os_name


def get_eol_chars_from_os_name(os_name):
    """Return EOL characters from OS name"""
    for eol_chars, name in EOL_CHARS:
        if name == os_name:
            return eol_chars


def has_mixed_eol_chars(text):
    """Detect if text has mixed EOL characters"""
    eol_chars = get_eol_chars(text)
    if eol_chars is None:
        return False
    else:
        correct_text = eol_chars.join((text + eol_chars).splitlines())
        return repr(correct_text) != repr(text)


def fix_indentation(text):
    """Replace tabs by spaces"""
    return text.replace('\t', '    ')