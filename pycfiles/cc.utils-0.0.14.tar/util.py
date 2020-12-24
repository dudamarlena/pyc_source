# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cc/licenserdf/util.py
# Compiled at: 2012-01-24 12:18:08
from cc.i18n.gettext_i18n import ugettext_for_locale
import re
TRANSLATION_BIT_RE = re.compile('\\$\\{([^\\}]+)\\}')

def inverse_translate(string, target_language, domain='cc_org'):
    """
    Translate something like "Foo ${bar} baz", where we actually
    preserve "Foo " and " baz" and translate "${bar} (using "bar" as
    the msgid)

       >>> from cc.i18n import ccorg_i18n_setup
       >>> translated_string = inverse_translate(
       ...    'foo ${country.pt} baz ${license.GPL_name_full}',
       ...    target_language='en_US')
       >>> translated_string == 'foo Portugal baz GNU General Public License'
    """
    gettext = ugettext_for_locale(target_language)
    string = unicode_cleaner(string)
    translated_string = ''
    last_pos = 0
    for match in TRANSLATION_BIT_RE.finditer(string):
        translated_string += string[last_pos:match.start()]
        msgid = match.group(1)
        translated_string += gettext(msgid)
        last_pos = match.end()

    translated_string += string[last_pos:]
    return translated_string


def unicode_cleaner(string):
    if isinstance(string, unicode):
        return string
    try:
        return string.decode('utf-8')
    except UnicodeError:
        try:
            return string.decode('latin-1')
        except UnicodeError:
            return string.decode('utf-8', 'ignore')