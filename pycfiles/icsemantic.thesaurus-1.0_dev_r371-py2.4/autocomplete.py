# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/browser/autocomplete.py
# Compiled at: 2008-10-06 10:31:07
try:
    from azax import AzaxBaseView, force_unicode
    from azax.plugins.core.interfaces import IKSSCoreCommands
    from azax.plugins.effects.interfaces import IScriptaculousEffectsCommands
except ImportError:
    try:
        from Products.azax import AzaxBaseView, force_unicode
        from Products.azax.plugins.core.interfaces import IKSSCoreCommands
        from Products.azax.plugins.effects.interfaces import IScriptaculousEffectsCommands
    except ImportError:
        from kss.core import force_unicode
        from kss.core.kssview import AzaxBaseView
        from kss.core.plugins.core.interfaces import IKSSCoreCommands
        from kss.core.plugins.effects.interfaces import IScriptaculousEffectsCommands

from Products.CMFPlone.utils import safe_unicode
from icsemantic.thesaurus.Thesaurus import thesaurus_utility
from icsemantic.core.vocabularies import LanguagesVocabularyFactory
import icsemantic.core.browser.admin, cgi

class AutoComplete(AzaxBaseView):
    __module__ = __name__

    def autocompleteConcepts(self, searchExpression):
        IKSSCoreCommands(self).replaceInnerHTML('div#searchResults', 'Resultado de "' + cgi.escape(safe_unicode(('<br>').join(searchExpression.split(',')))) + '"')
        return self.render()