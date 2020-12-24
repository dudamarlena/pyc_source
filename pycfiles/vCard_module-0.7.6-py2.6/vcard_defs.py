# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/vcard/vcard_defs.py
# Compiled at: 2010-07-19 03:17:46
"""vCards v3.0 (RFC 2426) definitions and message strings"""
ALPHA_CHARS = 'A-Za-z'
CHAR_CHARS = '\x01-\x7f'
CR_CHAR = '\r'
LF_CHAR = '\n'
CRLF_CHARS = CR_CHAR + LF_CHAR
CTL_CHARS = '\x00-\x1f\x7f'
DIGIT_CHARS = '0-9'
DQUOTE_CHAR = '"'
HTAB_CHAR = '\t'
SP_CHAR = ' '
VCHAR_CHARS = '!-~'
WSP_CHARS = SP_CHAR + HTAB_CHAR
NON_ASCII_CHARS = '\x80-ÿ'
QSAFE_CHARS = WSP_CHARS + '!' + '#-~' + NON_ASCII_CHARS
SAFE_CHARS = WSP_CHARS + '!' + '#-+' + '--9' + '<-~' + NON_ASCII_CHARS
VALUE_CHARS = WSP_CHARS + VCHAR_CHARS + NON_ASCII_CHARS
ESCAPED_CHARS = '\\;,nN'
MANDATORY_PROPERTIES = [
 'BEGIN', 'END', 'FN', 'N', 'VERSION']
PREDEFINED_PROPERTIES = ['BEGIN', 'END', 'NAME', 'PROFILE', 'SOURCE']
OTHER_PROPERTIES = [
 'ADR', 'AGENT', 'BDAY', 'CATEGORIES', 'CLASS', 'EMAIL', 'GEO', 'KEY',
 'LABEL', 'LOGO', 'MAILER', 'NICKNAME', 'NOTE', 'ORG', 'PHOTO', 'PRODID',
 'REV', 'ROLE', 'SORT-STRING', 'SOUND', 'TEL', 'TITLE', 'TZ', 'UID', 'URL']
ALL_PROPERTIES = list(set(MANDATORY_PROPERTIES + PREDEFINED_PROPERTIES + OTHER_PROPERTIES))
ID_CHARS = ALPHA_CHARS + DIGIT_CHARS + '-'
VCARD_LINE_MAX_LENGTH = 75
VCARD_LINE_MAX_LENGTH_RAW = VCARD_LINE_MAX_LENGTH + len(CRLF_CHARS)
MSG_CONTINUATION_AT_START = 'Continuation line at start of vCard (See RFC 2425 section 5.8.1 for line folding details)'
MSG_DOT_AT_LINE_START = 'Dot at start of line without group name (See RFC 2426 section 4 for group syntax)'
MSG_EMPTY_VCARD = 'vCard is empty'
MSG_INVALID_DATE = 'Invalid date (See RFC 2425 section 5.8.4 for date syntax)'
MSG_INVALID_LANGUAGE_VALUE = 'Invalid language (See RFC 1766 section 2 for details)'
MSG_INVALID_LINE_SEPARATOR = 'Invalid line ending; should be \\r\\n (See RFC 2426 section 2.4.2 for details)'
MSG_INVALID_PARAM_NAME = 'Invalid parameter name (See RFC 2426 section 4 for param-name syntax)'
MSG_INVALID_PARAM_VALUE = 'Invalid parameter value (See RFC 2426 section 4 for param-value syntax)'
MSG_INVALID_PROPERTY_NAME = 'Invalid property name (See RFC 2426 section 4 for name syntax)'
MSG_INVALID_SUBVALUE = 'Invalid subvalue (See RFC 2426 section 3 for details)'
MSG_INVALID_SUBVALUE_COUNT = 'Invalid subvalue count (See RFC 2426 section 3 for details)'
MSG_INVALID_TEXT_VALUE = 'Invalid text value (See RFC 2426 section 4 for details)'
MSG_INVALID_TIME = 'Invalid time (See RFC 2425 section 5.8.4 for time syntax)'
MSG_INVALID_TIME_ZONE = 'Invalid time zone (See RFC 2426 section 3.4.1 for time-zone syntax)'
MSG_INVALID_URI = 'Invalid URI (See RFC 1738 section 5 for genericurl syntax)'
MSG_INVALID_VALUE = 'Invalid value (See RFC 2426 section 3 for details)'
MSG_INVALID_VALUE_COUNT = 'Invalid value count (See RFC 2426 section 3 for details)'
MSG_INVALID_X_NAME = 'Invalid X-name (See RFC 2426 section 4 for x-name syntax)'
MSG_MISMATCH_GROUP = 'Group mismatch (See RFC 2426 section 4 for contentline syntax)'
MSG_MISMATCH_PARAM = 'Parameter mismatch (See RFC 2426 section 3 for details)'
MSG_MISSING_GROUP = 'Missing group (See RFC 2426 section 4 for contentline syntax)'
MSG_MISSING_PARAM = 'Parameter missing (See RFC 2426 section 3 for details)'
MSG_MISSING_PARAM_VALUE = 'Parameter value missing (See RFC 2426 section 3 for details)'
MSG_MISSING_PROPERTY = 'Mandatory property missing (See RFC 2426 section 5 for details)'
MSG_MISSING_VALUE_STRING = 'Missing value string (See RFC 2426 section 4 for contentline syntax)'
MSG_NON_EMPTY_PARAM = 'Property should not have parameters (See RFC 2426 section 3 for details)'
WARN_DEFAULT_TYPE_VALUE = 'Using default TYPE value; can be removed'
WARN_INVALID_DATE = 'Possible invalid date'
WARN_INVALID_EMAIL_TYPE = 'Possible invalid email TYPE'
WARN_MULTIPLE_NAMES = 'Possible split name (replace space with comma)'