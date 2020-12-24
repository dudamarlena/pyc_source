# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/trait/localized.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1792 bytes
from ... import Document
from ...field import String, Mapping, Embed, Alias
from ....package.loader import traverse
from ....schema.compat import odict
LANGUAGES = {
 'en', 'fr', 'it', 'de', 'es', 'pt', 'ru'}
LANGUAGES |= {'da', 'nl', 'fi', 'hu', 'nb', 'pt', 'ro', 'sv', 'tr'}
LANGUAGES |= {'ara', 'prs', 'pes', 'urd'}
LANGUAGES |= {'zhs', 'zht'}

class Translated(Alias):
    __doc__ = 'Reference a localized field, providing a mapping interface to the translations.\n\t\n\t\tclass MyDocument(Localized, Document):\n\t\t\tclass Locale(Localized.Locale):\n\t\t\t\ttitle = String()\n\t\t\t\n\t\t\ttitle = Translated(\'title\')\n\t\t\n\t\t# Query\n\t\tMyDocument.title == "Hello world!"\n\t\t\n\t\tinst = MyDocument([Locale(\'en\', "Hi."), Locale(\'fr\', "Bonjour.")])\n\t\tassert inst.title == {\'en\': "Hi.", \'fr\': "Bonjour."}\n\t'

    def __init__(self, path, **kw):
        (super(Translated, self).__init__)(path='locale.' + path, **kw)

    def __get__(self, obj, cls=None):
        if obj is None:
            return super(Translated, self).__get__(obj, cls)
        else:
            collection = odict()
            path = self.path[7:]
            for lang, locale in obj.locale.items():
                collection[lang] = traverse(locale, path)

            return collection

    def __set__(self, obj, value):
        raise TypeError('Can not assign to a translated alias.')


class Localized(Document):
    __doc__ = 'The annotated Document contains localized data.'

    class Locale(Document):
        __pk__ = 'language'
        language = String(choices=LANGUAGES, default='en')

    locale = Mapping('.Locale', key='language', default=(lambda : []), assign=True, repr=False, positional=False)

    def __repr__(self):
        if self.locale:
            return super(Localized, self).__repr__('{' + ', '.join(self.locale) + '}')
        else:
            return super(Localized, self).__repr__()