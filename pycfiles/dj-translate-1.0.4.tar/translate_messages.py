# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/management/commands/translate_messages.py
# Compiled at: 2016-10-06 06:01:59
import logging, os, re
from optparse import make_option
import polib
from django.conf import settings
from django.core.management.base import BaseCommand
from autotranslate.utils import translate_strings
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'autotranslate all the message files that have been generated using the `makemessages` command.'
    option_list = BaseCommand.option_list + (
     make_option('--locale', '-l', default=[], dest='locale', action='append', help='autotranslate the message files for the given locale(s) (e.g. pt_BR). can be used multiple times.'),
     make_option('--untranslated', '-u', default=False, dest='skip_translated', action='store_true', help='autotranslate the fuzzy and empty messages only.'),
     make_option('--set-fuzzy', '-f', default=False, dest='set_fuzzy', action='store_true', help='set the fuzzy flag on autotranslated messages.'))

    def add_arguments(self, parser):
        parser.add_argument('--locale', '-l', default=[], dest='locale', action='append', help='autotranslate the message files for the given locale(s) (e.g. pt_BR). can be used multiple times.')
        parser.add_argument('--untranslated', '-u', default=False, dest='skip_translated', action='store_true', help='autotranslate the fuzzy and empty messages only.')
        parser.add_argument('--set-fuzzy', '-f', default=False, dest='set_fuzzy', action='store_true', help='set the fuzzy flag on autotranslated messages.')

    def set_options(self, **options):
        self.locale = options['locale']
        self.skip_translated = options['skip_translated']
        self.set_fuzzy = options['set_fuzzy']

    def handle(self, *args, **options):
        self.set_options(**options)
        assert getattr(settings, 'USE_I18N', False), 'i18n framework is disabled'
        assert getattr(settings, 'LOCALE_PATHS', []), 'locale paths is not configured properly'
        for directory in settings.LOCALE_PATHS:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if not file.endswith('.po'):
                        continue
                    target_language = os.path.basename(os.path.dirname(root))
                    if self.locale and target_language not in self.locale:
                        logger.info(('skipping translation for locale `{}`').format(target_language))
                        continue
                    self.translate_file(root, file, target_language)

    def translate_file(self, root, file_name, target_language):
        """
        convenience method for translating a pot file

        :param root:            the absolute path of folder where the file is present
        :param file_name:       name of the file to be translated (it should be a pot file)
        :param target_language: language in which the file needs to be translated
        """
        logger.info(('filling up translations for locale `{}`').format(target_language))
        po = polib.pofile(os.path.join(root, file_name))
        strings = self.get_strings_to_translate(po)
        translated_strings = translate_strings(strings, target_language, 'en', False)
        self.update_translations(po, translated_strings)
        po.save()

    def need_translate(self, entry):
        if self.skip_translated:
            if entry.translated():
                return False
            else:
                return True

        else:
            return True

    def get_strings_to_translate(self, po):
        """Return list of string to translate from po file.

        :param po: POFile object to translate
        :type po: polib.POFile
        :return: list of string to translate
        :rtype: collections.Iterable[six.text_type]
        """
        strings = []
        for index, entry in enumerate(po):
            if not self.need_translate(entry):
                continue
            strings.append(humanize_placeholders(entry.msgid))
            if entry.msgid_plural:
                strings.append(humanize_placeholders(entry.msgid_plural))

        return strings

    def update_translations(self, entries, translated_strings):
        """Update translations in entries.

        The order and number of translations should match to get_strings_to_translate() result.

        :param entries: list of entries to translate
        :type entries: collections.Iterable[polib.POEntry] | polib.POFile
        :param translated_strings: list of translations
        :type translated_strings: collections.Iterable[six.text_type]
        """
        translations = iter(translated_strings)
        for entry in entries:
            if not self.need_translate(entry):
                continue
            if entry.msgid_plural:
                translation = next(translations)
                translation = fix_translation(entry.msgid, translation)
                entry.msgstr_plural[0] = translation
                translation = next(translations)
                translation = fix_translation(entry.msgid_plural, translation)
                for k, v in entry.msgstr_plural.items():
                    if k != 0:
                        entry.msgstr_plural[k] = translation

            else:
                translation = next(translations)
                translation = fix_translation(entry.msgid, translation)
                entry.msgstr = translation
            if self.set_fuzzy and 'fuzzy' not in entry.flags:
                entry.flags.append('fuzzy')


def humanize_placeholders(msgid):
    """Convert placeholders to the (google translate) service friendly form.

    %(name)s -> __name__
    %s       -> __item__
    %d       -> __number__
    """
    return re.sub('%(?:\\((\\w+)\\))?([sd])', lambda match: ('__{0}__').format(match.group(1).lower() if match.group(1) else 'number' if match.group(2) == 'd' else 'item'), msgid)


def restore_placeholders(msgid, translation):
    """Restore placeholders in the translated message."""
    placehoders = re.findall('(\\s*)(%(?:\\(\\w+\\))?[sd])(\\s*)', msgid)
    return re.sub('(\\s*)(__[\\w]+?__)(\\s*)', lambda matches: ('{0}{1}{2}').format(placehoders[0][0], placehoders[0][1], placehoders.pop(0)[2]), translation)


def fix_translation(msgid, translation):
    if msgid.startswith('\n') and not translation.startswith('\n'):
        translation = '\n' + translation
    if msgid.endswith('\n') and not translation.endswith('\n'):
        translation += '\n'
    translation = restore_placeholders(msgid, translation)
    return translation