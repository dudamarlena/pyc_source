# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/locale.py
# Compiled at: 2012-01-23 23:44:33
"""Translation methods for generating localized strings.

To load a locale and generate a translated string::

    user_locale = locale.get("es_LA")
    print user_locale.translate("Sign out")

locale.get() returns the closest matching locale, not necessarily the
specific locale you requested. You can support pluralization with
additional arguments to translate(), e.g.::

    people = [...]
    message = user_locale.translate(
        "%(list)s is online", "%(list)s are online", len(people))
    print message % {"list": user_locale.list(people)}

The first string is chosen if len(people) == 1, otherwise the second
string is chosen.

Applications should call one of load_translations (which uses a simple
CSV format) or load_gettext_translations (which uses the .mo format
supported by gettext and related tools).  If neither method is called,
the locale.translate method will simply return the original string.
"""
import csv, datetime, logging, os, re
_default_locale = 'en_US'
_translations = {}
_supported_locales = frozenset([_default_locale])
_use_gettext = False

def get(*locale_codes):
    """Returns the closest match for the given locale codes.

    We iterate over all given locale codes in order. If we have a tight
    or a loose match for the code (e.g., "en" for "en_US"), we return
    the locale. Otherwise we move to the next code in the list.

    By default we return en_US if no translations are found for any of
    the specified locales. You can change the default locale with
    set_default_locale() below.
    """
    return Locale.get_closest(*locale_codes)


def set_default_locale(code):
    """Sets the default locale, used in get_closest_locale().

    The default locale is assumed to be the language used for all strings
    in the system. The translations loaded from disk are mappings from
    the default locale to the destination locale. Consequently, you don't
    need to create a translation file for the default locale.
    """
    global _default_locale
    global _supported_locales
    global _translations
    _default_locale = code
    _supported_locales = frozenset(_translations.keys() + [_default_locale])


def load_translations(directory):
    u"""Loads translations from CSV files in a directory.

    Translations are strings with optional Python-style named placeholders
    (e.g., "My name is %(name)s") and their associated translations.

    The directory should have translation files of the form LOCALE.csv,
    e.g. es_GT.csv. The CSV files should have two or three columns: string,
    translation, and an optional plural indicator. Plural indicators should
    be one of "plural" or "singular". A given string can have both singular
    and plural forms. For example "%(name)s liked this" may have a
    different verb conjugation depending on whether %(name)s is one
    name or a list of names. There should be two rows in the CSV file for
    that string, one with plural indicator "singular", and one "plural".
    For strings with no verbs that would change on translation, simply
    use "unknown" or the empty string (or don't include the column at all).

    The file is read using the csv module in the default "excel" dialect.
    In this format there should not be spaces after the commas.

    Example translation es_LA.csv:

        "I love you","Te amo"
        "%(name)s liked this","A %(name)s les gustó esto","plural"
        "%(name)s liked this","A %(name)s le gustó esto","singular"

    """
    global _supported_locales
    global _translations
    _translations = {}
    for path in os.listdir(directory):
        if not path.endswith('.csv'):
            continue
        locale, extension = path.split('.')
        if not re.match('[a-z]+(_[A-Z]+)?$', locale):
            logging.error('Unrecognized locale %r (path: %s)', locale, os.path.join(directory, path))
            continue
        f = open(os.path.join(directory, path), 'r')
        _translations[locale] = {}
        for i, row in enumerate(csv.reader(f)):
            if not row or len(row) < 2:
                continue
            row = [ c.decode('utf-8').strip() for c in row ]
            english, translation = row[:2]
            if len(row) > 2:
                plural = row[2] or 'unknown'
            else:
                plural = 'unknown'
            if plural not in ('plural', 'singular', 'unknown'):
                logging.error('Unrecognized plural indicator %r in %s line %d', plural, path, i + 1)
                continue
            _translations[locale].setdefault(plural, {})[english] = translation

        f.close()

    _supported_locales = frozenset(_translations.keys() + [_default_locale])
    logging.info('Supported locales: %s', sorted(_supported_locales))


def load_gettext_translations(directory, domain):
    """Loads translations from gettext's locale tree

    Locale tree is similar to system's /usr/share/locale, like:

    {directory}/{lang}/LC_MESSAGES/{domain}.mo

    Three steps are required to have you app translated:

    1. Generate POT translation file
        xgettext --language=Python --keyword=_:1,2 -d cyclone file1.py file2.html etc

    2. Merge against existing POT file:
        msgmerge old.po cyclone.po > new.po

    3. Compile:
        msgfmt cyclone.po -o {directory}/pt_BR/LC_MESSAGES/cyclone.mo
    """
    global _supported_locales
    global _translations
    global _use_gettext
    import gettext
    _translations = {}
    for lang in os.listdir(directory):
        if lang.startswith('.'):
            continue
        if os.path.isfile(os.path.join(directory, lang)):
            continue
        try:
            os.stat(os.path.join(directory, lang, 'LC_MESSAGES', domain + '.mo'))
            _translations[lang] = gettext.translation(domain, directory, languages=[
             lang])
        except Exception as e:
            logging.error("Cannot load translation for '%s': %s", lang, str(e))
            continue

    _supported_locales = frozenset(_translations.keys() + [_default_locale])
    _use_gettext = True
    logging.info('Supported locales: %s', sorted(_supported_locales))


def get_supported_locales(cls):
    """Returns a list of all the supported locale codes."""
    return _supported_locales


class Locale(object):
    """Object representing a locale.

    After calling one of `load_translations` or `load_gettext_translations`,
    call `get` or `get_closest` to get a Locale object.
    """

    @classmethod
    def get_closest(cls, *locale_codes):
        """Returns the closest match for the given locale code."""
        for code in locale_codes:
            if not code:
                continue
            code = code.replace('-', '_')
            parts = code.split('_')
            if len(parts) > 2:
                continue
            else:
                if len(parts) == 2:
                    code = parts[0].lower() + '_' + parts[1].upper()
                if code in _supported_locales:
                    return cls.get(code)
                if parts[0].lower() in _supported_locales:
                    return cls.get(parts[0].lower())

        return cls.get(_default_locale)

    @classmethod
    def get(cls, code):
        """Returns the Locale for the given locale code.

        If it is not supported, we raise an exception.
        """
        if not hasattr(cls, '_cache'):
            cls._cache = {}
        if code not in cls._cache:
            assert code in _supported_locales
            translations = _translations.get(code, None)
            if translations is None:
                locale = CSVLocale(code, {})
            elif _use_gettext:
                locale = GettextLocale(code, translations)
            else:
                locale = CSVLocale(code, translations)
            cls._cache[code] = locale
        return cls._cache[code]

    def __init__(self, code, translations):
        self.code = code
        self.name = LOCALE_NAMES.get(code, {}).get('name', 'Unknown')
        self.rtl = False
        for prefix in ['fa', 'ar', 'he']:
            if self.code.startswith(prefix):
                self.rtl = True
                break

        self.translations = translations
        _ = self.translate
        self._months = [
         _('January'), _('February'), _('March'), _('April'),
         _('May'), _('June'), _('July'), _('August'),
         _('September'), _('October'), _('November'), _('December')]
        self._weekdays = [
         _('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'),
         _('Friday'), _('Saturday'), _('Sunday')]

    def translate(self, message, plural_message=None, count=None):
        """Returns the translation for the given message for this locale.

        If plural_message is given, you must also provide count. We return
        plural_message when count != 1, and we return the singular form
        for the given message when count == 1.
        """
        raise NotImplementedError()

    def format_date(self, date, gmt_offset=0, relative=True, shorter=False, full_format=False):
        """Formats the given date (which should be GMT).

        By default, we return a relative time (e.g., "2 minutes ago"). You
        can return an absolute date string with relative=False.

        You can force a full format date ("July 10, 1980") with
        full_format=True.

        This method is primarily intended for dates in the past.
        For dates in the future, we fall back to full format.
        """
        if self.code.startswith('ru'):
            relative = False
        if type(date) in (int, long, float):
            date = datetime.datetime.utcfromtimestamp(date)
        now = datetime.datetime.utcnow()
        if date > now:
            if relative and (date - now).seconds < 60:
                date = now
            else:
                full_format = True
        local_date = date - datetime.timedelta(minutes=gmt_offset)
        local_now = now - datetime.timedelta(minutes=gmt_offset)
        local_yesterday = local_now - datetime.timedelta(hours=24)
        difference = now - date
        seconds = difference.seconds
        days = difference.days
        _ = self.translate
        format = None
        if not full_format:
            if relative and days == 0:
                if seconds < 50:
                    return _('1 second ago', '%(seconds)d seconds ago', seconds) % {'seconds': seconds}
                if seconds < 3000:
                    minutes = round(seconds / 60.0)
                    return _('1 minute ago', '%(minutes)d minutes ago', minutes) % {'minutes': minutes}
                hours = round(seconds / 3600.0)
                return _('1 hour ago', '%(hours)d hours ago', hours) % {'hours': hours}
            if days == 0:
                format = _('%(time)s')
            elif days == 1 and local_date.day == local_yesterday.day and relative:
                format = _('yesterday') if shorter else _('yesterday at %(time)s')
            elif days < 5:
                format = _('%(weekday)s') if shorter else _('%(weekday)s at %(time)s')
            elif days < 334:
                format = _('%(month_name)s %(day)s') if shorter else _('%(month_name)s %(day)s at %(time)s')
        if format is None:
            format = _('%(month_name)s %(day)s, %(year)s') if shorter else _('%(month_name)s %(day)s, %(year)s at %(time)s')
        tfhour_clock = self.code not in ('en', 'en_US', 'zh_CN')
        if tfhour_clock:
            str_time = '%d:%02d' % (local_date.hour, local_date.minute)
        elif self.code == 'zh_CN':
            str_time = '%s%d:%02d' % (
             ('上午', '下午')[(local_date.hour >= 12)],
             local_date.hour % 12 or 12, local_date.minute)
        else:
            str_time = '%d:%02d %s' % (
             local_date.hour % 12 or 12, local_date.minute,
             ('am', 'pm')[(local_date.hour >= 12)])
        return format % {'month_name': self._months[(local_date.month - 1)], 
           'weekday': self._weekdays[local_date.weekday()], 
           'day': str(local_date.day), 
           'year': str(local_date.year), 
           'time': str_time}

    def format_day(self, date, gmt_offset=0, dow=True):
        """Formats the given date as a day of week.

        Example: "Monday, January 22". You can remove the day of week with
        dow=False.
        """
        local_date = date - datetime.timedelta(minutes=gmt_offset)
        _ = self.translate
        if dow:
            return _('%(weekday)s, %(month_name)s %(day)s') % {'month_name': self._months[(local_date.month - 1)], 
               'weekday': self._weekdays[local_date.weekday()], 
               'day': str(local_date.day)}
        else:
            return _('%(month_name)s %(day)s') % {'month_name': self._months[(local_date.month - 1)], 
               'day': str(local_date.day)}

    def list(self, parts):
        """Returns a comma-separated list for the given list of parts.

        The format is, e.g., "A, B and C", "A and B" or just "A" for lists
        of size 1.
        """
        _ = self.translate
        if len(parts) == 0:
            return ''
        if len(parts) == 1:
            return parts[0]
        comma = ' و ' if self.code.startswith('fa') else ', '
        return _('%(commas)s and %(last)s') % {'commas': comma.join(parts[:-1]), 
           'last': parts[(len(parts) - 1)]}

    def friendly_number(self, value):
        """Returns a comma-separated number for the given integer."""
        if self.code not in ('en', 'en_US'):
            return str(value)
        value = str(value)
        parts = []
        while value:
            parts.append(value[-3:])
            value = value[:-3]

        return (',').join(reversed(parts))


class CSVLocale(Locale):
    """Locale implementation using tornado's CSV translation format."""

    def translate(self, message, plural_message=None, count=None):
        if plural_message is not None:
            assert count is not None
            if count != 1:
                message = plural_message
                message_dict = self.translations.get('plural', {})
            else:
                message_dict = self.translations.get('singular', {})
        else:
            message_dict = self.translations.get('unknown', {})
        return message_dict.get(message, message)


class GettextLocale(Locale):
    """Locale implementation using the gettext module."""

    def translate(self, message, plural_message=None, count=None):
        if plural_message is not None:
            assert count is not None
            return self.translations.ungettext(message, plural_message, count)
        else:
            return self.translations.ugettext(message)
            return


LOCALE_NAMES = {'af_ZA': {'name_en': 'Afrikaans', 'name': 'Afrikaans'}, 'am_ET': {'name_en': 'Amharic', 'name': 'አማርኛ'}, 'ar_AR': {'name_en': 'Arabic', 'name': 'العربية'}, 'bg_BG': {'name_en': 'Bulgarian', 'name': 'Български'}, 'bn_IN': {'name_en': 'Bengali', 'name': 'বাংলা'}, 'bs_BA': {'name_en': 'Bosnian', 'name': 'Bosanski'}, 'ca_ES': {'name_en': 'Catalan', 'name': 'Català'}, 'cs_CZ': {'name_en': 'Czech', 'name': 'Čeština'}, 'cy_GB': {'name_en': 'Welsh', 'name': 'Cymraeg'}, 'da_DK': {'name_en': 'Danish', 'name': 'Dansk'}, 'de_DE': {'name_en': 'German', 'name': 'Deutsch'}, 'el_GR': {'name_en': 'Greek', 'name': 'Ελληνικά'}, 'en_GB': {'name_en': 'English (UK)', 'name': 'English (UK)'}, 'en_US': {'name_en': 'English (US)', 'name': 'English (US)'}, 'es_ES': {'name_en': 'Spanish (Spain)', 'name': 'Español (España)'}, 'es_LA': {'name_en': 'Spanish', 'name': 'Español'}, 'et_EE': {'name_en': 'Estonian', 'name': 'Eesti'}, 'eu_ES': {'name_en': 'Basque', 'name': 'Euskara'}, 'fa_IR': {'name_en': 'Persian', 'name': 'فارسی'}, 'fi_FI': {'name_en': 'Finnish', 'name': 'Suomi'}, 'fr_CA': {'name_en': 'French (Canada)', 'name': 'Français (Canada)'}, 'fr_FR': {'name_en': 'French', 'name': 'Français'}, 'ga_IE': {'name_en': 'Irish', 'name': 'Gaeilge'}, 'gl_ES': {'name_en': 'Galician', 'name': 'Galego'}, 'he_IL': {'name_en': 'Hebrew', 'name': 'עברית'}, 'hi_IN': {'name_en': 'Hindi', 'name': 'हिन्दी'}, 'hr_HR': {'name_en': 'Croatian', 'name': 'Hrvatski'}, 'hu_HU': {'name_en': 'Hungarian', 'name': 'Magyar'}, 'id_ID': {'name_en': 'Indonesian', 'name': 'Bahasa Indonesia'}, 'is_IS': {'name_en': 'Icelandic', 'name': 'Íslenska'}, 'it_IT': {'name_en': 'Italian', 'name': 'Italiano'}, 'ja_JP': {'name_en': 'Japanese', 'name': '日本語'}, 'ko_KR': {'name_en': 'Korean', 'name': '한국어'}, 'lt_LT': {'name_en': 'Lithuanian', 'name': 'Lietuvių'}, 'lv_LV': {'name_en': 'Latvian', 'name': 'Latviešu'}, 'mk_MK': {'name_en': 'Macedonian', 'name': 'Македонски'}, 'ml_IN': {'name_en': 'Malayalam', 'name': 'മലയാളം'}, 'ms_MY': {'name_en': 'Malay', 'name': 'Bahasa Melayu'}, 'nb_NO': {'name_en': 'Norwegian (bokmal)', 'name': 'Norsk (bokmål)'}, 'nl_NL': {'name_en': 'Dutch', 'name': 'Nederlands'}, 'nn_NO': {'name_en': 'Norwegian (nynorsk)', 'name': 'Norsk (nynorsk)'}, 'pa_IN': {'name_en': 'Punjabi', 'name': 'ਪੰਜਾਬੀ'}, 'pl_PL': {'name_en': 'Polish', 'name': 'Polski'}, 'pt_BR': {'name_en': 'Portuguese (Brazil)', 'name': 'Português (Brasil)'}, 'pt_PT': {'name_en': 'Portuguese (Portugal)', 'name': 'Português (Portugal)'}, 'ro_RO': {'name_en': 'Romanian', 'name': 'Română'}, 'ru_RU': {'name_en': 'Russian', 'name': 'Русский'}, 'sk_SK': {'name_en': 'Slovak', 'name': 'Slovenčina'}, 'sl_SI': {'name_en': 'Slovenian', 'name': 'Slovenščina'}, 'sq_AL': {'name_en': 'Albanian', 'name': 'Shqip'}, 'sr_RS': {'name_en': 'Serbian', 'name': 'Српски'}, 'sv_SE': {'name_en': 'Swedish', 'name': 'Svenska'}, 'sw_KE': {'name_en': 'Swahili', 'name': 'Kiswahili'}, 'ta_IN': {'name_en': 'Tamil', 'name': 'தமிழ்'}, 'te_IN': {'name_en': 'Telugu', 'name': 'తెలుగు'}, 'th_TH': {'name_en': 'Thai', 'name': 'ภาษาไทย'}, 'tl_PH': {'name_en': 'Filipino', 'name': 'Filipino'}, 'tr_TR': {'name_en': 'Turkish', 'name': 'Türkçe'}, 'uk_UA': {'name_en': 'Ukraini ', 'name': 'Українська'}, 'vi_VN': {'name_en': 'Vietnamese', 'name': 'Tiếng Việt'}, 'zh_CN': {'name_en': 'Chinese (Simplified)', 'name': '中文(简体)'}, 'zh_TW': {'name_en': 'Chinese (Traditional)', 'name': '中文(繁體)'}}