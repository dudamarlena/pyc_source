# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/__init__.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 2331 bytes
import threading, gettext
from noval import ui_lang
_lock = threading.Lock()

def NewId():
    global _idCounter
    with _lock:
        _idCounter += 1
    return _idCounter


def GetApp():
    global _AppInstance
    assert _AppInstance is not None
    return _AppInstance


class Locale(object):

    def __init__(self, lang_id):
        self._lang_id = lang_id
        self._domains = []
        self._trans = []
        self._lookup_dirs = []

    @property
    def LangId(self):
        return self._lang_id

    def AddCatalogLookupPathPrefix(self, lookup_dir):
        if lookup_dir not in self._lookup_dirs:
            self._lookup_dirs.append(lookup_dir)

    def AddCatalog(self, domain):
        if domain in self._domains:
            raise RuntimeError('domain %s already exist in locale domains' % domain)
        self._domains.append(domain)
        for lookup_dir in self._lookup_dirs:
            t = gettext.translation(domain, lookup_dir, languages=[self.GetLanguageCanonicalName()], fallback=True)
            self._trans.append(t)

    def GetLanguageName(self):
        for lang in ui_lang.LANGUAGE_LIST:
            if lang[0] == self._lang_id:
                return lang[2]

        raise RuntimeError('unknown lang id %d', self._lang_id)

    def GetLanguageCanonicalName(self):
        for lang in ui_lang.LANGUAGE_LIST:
            if lang[0] == self._lang_id:
                return lang[1]

        raise RuntimeError('unknown lang id %d', self._lang_id)

    def GetText(self, raw_text):
        for tran in self._trans:
            to_text = tran.gettext(raw_text)
            if to_text != raw_text:
                return to_text

        return raw_text

    @classmethod
    def IsAvailable(cls, lang_id):
        for lang in ui_lang.LANGUAGE_LIST:
            if lang[0] == lang_id:
                return True

        return False


def GetTranslation(raw_text):
    assert _AppInstance is not None
    return _AppInstance.GetLocale().GetText(raw_text)


_ = GetTranslation
_idCounter = 1000
_AppInstance = None