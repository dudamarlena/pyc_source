# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/openstack/common/gettextutils.py
# Compiled at: 2016-06-13 14:11:03
"""
gettext for openstack-common modules.

Usual usage in an openstack.common module:

    from openstack.common.gettextutils import _
"""
import copy, gettext, locale
from logging import handlers
import os
from babel import localedata
import six
_AVAILABLE_LANGUAGES = {}
USE_LAZY = False

class TranslatorFactory(object):
    """Create translator functions
    """

    def __init__(self, domain, localedir=None):
        """Establish a set of translation functions for the domain.

        :param domain: Name of translation domain,
                       specifying a message catalog.
        :type domain: str
        :param lazy: Delays translation until a message is emitted.
                     Defaults to False.
        :type lazy: Boolean
        :param localedir: Directory with translation catalogs.
        :type localedir: str
        """
        self.domain = domain
        if localedir is None:
            localedir = os.environ.get(domain.upper() + '_LOCALEDIR')
        self.localedir = localedir
        return

    def _make_translation_func(self, domain=None):
        """Return a new translation function ready for use.

        Takes into account whether or not lazy translation is being
        done.

        The domain can be specified to override the default from the
        factory, but the localedir from the factory is always used
        because we assume the log-level translation catalogs are
        installed in the same directory as the main application
        catalog.

        """
        if domain is None:
            domain = self.domain
        t = gettext.translation(domain, localedir=self.localedir, fallback=True)
        m = t.gettext if six.PY3 else t.ugettext

        def f(msg):
            """oslo.i18n.gettextutils translation function."""
            global USE_LAZY
            if USE_LAZY:
                return Message(msg, domain=domain)
            return m(msg)

        return f

    @property
    def primary(self):
        """The default translation function."""
        return self._make_translation_func()

    def _make_log_translation_func(self, level):
        return self._make_translation_func(self.domain + '-log-' + level)

    @property
    def log_info(self):
        """Translate info-level log messages."""
        return self._make_log_translation_func('info')

    @property
    def log_warning(self):
        """Translate warning-level log messages."""
        return self._make_log_translation_func('warning')

    @property
    def log_error(self):
        """Translate error-level log messages."""
        return self._make_log_translation_func('error')

    @property
    def log_critical(self):
        """Translate critical-level log messages."""
        return self._make_log_translation_func('critical')


_translators = TranslatorFactory('vsmclient')
_ = _translators.primary
_LI = _translators.log_info
_LW = _translators.log_warning
_LE = _translators.log_error
_LC = _translators.log_critical

def enable_lazy():
    """Convenience function for configuring _() to use lazy gettext

    Call this at the start of execution to enable the gettextutils._
    function to use lazy gettext functionality. This is useful if
    your project is importing _ directly instead of using the
    gettextutils.install() way of importing the _ function.
    """
    global USE_LAZY
    USE_LAZY = True


def install(domain):
    """Install a _() function using the given translation domain.

    Given a translation domain, install a _() function using gettext's
    install() function.

    The main difference from gettext.install() is that we allow
    overriding the default localedir (e.g. /usr/share/locale) using
    a translation-domain-specific environment variable (e.g.
    NOVA_LOCALEDIR).

    Note that to enable lazy translation, enable_lazy must be
    called.

    :param domain: the translation domain
    """
    from six import moves
    tf = TranslatorFactory(domain)
    moves.builtins.__dict__['_'] = tf.primary


class Message(six.text_type):
    """A Message object is a unicode object that can be translated.

    Translation of Message is done explicitly using the translate() method.
    For all non-translation intents and purposes, a Message is simply unicode,
    and can be treated as such.
    """

    def __new__(cls, msgid, msgtext=None, params=None, domain='cinderclient', *args):
        """Create a new Message object.

        In order for translation to work gettext requires a message ID, this
        msgid will be used as the base unicode text. It is also possible
        for the msgid and the base unicode text to be different by passing
        the msgtext parameter.
        """
        if not msgtext:
            msgtext = Message._translate_msgid(msgid, domain)
        msg = super(Message, cls).__new__(cls, msgtext)
        msg.msgid = msgid
        msg.domain = domain
        msg.params = params
        return msg

    def translate(self, desired_locale=None):
        """Translate this message to the desired locale.

        :param desired_locale: The desired locale to translate the message to,
                               if no locale is provided the message will be
                               translated to the system's default locale.

        :returns: the translated message in unicode
        """
        translated_message = Message._translate_msgid(self.msgid, self.domain, desired_locale)
        if self.params is None:
            return translated_message
        else:
            translated_params = _translate_args(self.params, desired_locale)
            translated_message = translated_message % translated_params
            return translated_message

    @staticmethod
    def _translate_msgid(msgid, domain, desired_locale=None):
        if not desired_locale:
            system_locale = locale.getdefaultlocale()
            if not system_locale[0]:
                desired_locale = 'en_US'
            else:
                desired_locale = system_locale[0]
        locale_dir = os.environ.get(domain.upper() + '_LOCALEDIR')
        lang = gettext.translation(domain, localedir=locale_dir, languages=[
         desired_locale], fallback=True)
        if six.PY3:
            translator = lang.gettext
        else:
            translator = lang.ugettext
        translated_message = translator(msgid)
        return translated_message

    def __mod__(self, other):
        params = self._sanitize_mod_params(other)
        unicode_mod = super(Message, self).__mod__(params)
        modded = Message(self.msgid, msgtext=unicode_mod, params=params, domain=self.domain)
        return modded

    def _sanitize_mod_params(self, other):
        """Sanitize the object being modded with this Message.

        - Add support for modding 'None' so translation supports it
        - Trim the modded object, which can be a large dictionary, to only
        those keys that would actually be used in a translation
        - Snapshot the object being modded, in case the message is
        translated, it will be used as it was when the Message was created
        """
        if other is None:
            params = (
             other,)
        elif isinstance(other, dict):
            params = {}
            if isinstance(self.params, dict):
                for key, val in self.params.items():
                    params[key] = self._copy_param(val)

            for key, val in other.items():
                params[key] = self._copy_param(val)

        else:
            params = self._copy_param(other)
        return params

    def _copy_param(self, param):
        try:
            return copy.deepcopy(param)
        except Exception:
            return six.text_type(param)

    def __add__(self, other):
        msg = _('Message objects do not support addition.')
        raise TypeError(msg)

    def __radd__(self, other):
        return self.__add__(other)

    if six.PY2:

        def __str__(self):
            msg = _('Message objects do not support str() because they may contain non-ascii characters. Please use unicode() or translate() instead.')
            raise UnicodeError(msg)


def get_available_languages(domain):
    """Lists the available languages for the given translation domain.

    :param domain: the domain to get languages for
    """
    if domain in _AVAILABLE_LANGUAGES:
        return copy.copy(_AVAILABLE_LANGUAGES[domain])
    else:
        localedir = '%s_LOCALEDIR' % domain.upper()
        find = lambda x: gettext.find(domain, localedir=os.environ.get(localedir), languages=[
         x])
        language_list = [
         'en_US']
        list_identifiers = getattr(localedata, 'list', None) or getattr(localedata, 'locale_identifiers')
        locale_identifiers = list_identifiers()
        for i in locale_identifiers:
            if find(i) is not None:
                language_list.append(i)

        aliases = {'zh': 'zh_CN', 'zh_Hant_HK': 'zh_HK', 
           'zh_Hant': 'zh_TW', 
           'fil': 'tl_PH'}
        for locale_, alias in six.iteritems(aliases):
            if locale_ in language_list and alias not in language_list:
                language_list.append(alias)

        _AVAILABLE_LANGUAGES[domain] = language_list
        return copy.copy(language_list)


def translate(obj, desired_locale=None):
    """Gets the translated unicode representation of the given object.

    If the object is not translatable it is returned as-is.
    If the locale is None the object is translated to the system locale.

    :param obj: the object to translate
    :param desired_locale: the locale to translate the message to, if None the
                           default system locale will be used
    :returns: the translated object in unicode, or the original object if
              it could not be translated
    """
    message = obj
    if not isinstance(message, Message):
        message = six.text_type(obj)
    if isinstance(message, Message):
        return message.translate(desired_locale)
    return obj


def _translate_args(args, desired_locale=None):
    """Translates all the translatable elements of the given arguments object.

    This method is used for translating the translatable values in method
    arguments which include values of tuples or dictionaries.
    If the object is not a tuple or a dictionary the object itself is
    translated if it is translatable.

    If the locale is None the object is translated to the system locale.

    :param args: the args to translate
    :param desired_locale: the locale to translate the args to, if None the
                           default system locale will be used
    :returns: a new args object with the translated contents of the original
    """
    if isinstance(args, tuple):
        return tuple(translate(v, desired_locale) for v in args)
    if isinstance(args, dict):
        translated_dict = {}
        for k, v in six.iteritems(args):
            translated_v = translate(v, desired_locale)
            translated_dict[k] = translated_v

        return translated_dict
    return translate(args, desired_locale)


class TranslationHandler(handlers.MemoryHandler):
    """Handler that translates records before logging them.

    The TranslationHandler takes a locale and a target logging.Handler object
    to forward LogRecord objects to after translating them. This handler
    depends on Message objects being logged, instead of regular strings.

    The handler can be configured declaratively in the logging.conf as follows:

        [handlers]
        keys = translatedlog, translator

        [handler_translatedlog]
        class = handlers.WatchedFileHandler
        args = ('/var/log/api-localized.log',)
        formatter = context

        [handler_translator]
        class = openstack.common.log.TranslationHandler
        target = translatedlog
        args = ('zh_CN',)

    If the specified locale is not available in the system, the handler will
    log in the default locale.
    """

    def __init__(self, locale=None, target=None):
        """Initialize a TranslationHandler

        :param locale: locale to use for translating messages
        :param target: logging.Handler object to forward
                       LogRecord objects to after translation
        """
        handlers.MemoryHandler.__init__(self, capacity=0, target=target)
        self.locale = locale

    def setFormatter(self, fmt):
        self.target.setFormatter(fmt)

    def emit(self, record):
        original_msg = record.msg
        original_args = record.args
        try:
            self._translate_and_log_record(record)
        finally:
            record.msg = original_msg
            record.args = original_args

    def _translate_and_log_record(self, record):
        record.msg = translate(record.msg, self.locale)
        record.args = _translate_args(record.args, self.locale)
        self.target.emit(record)