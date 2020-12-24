# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/collection/alphabetic/browser/character_options.py
# Compiled at: 2009-06-10 19:16:18
from zope.app.component.hooks import getSite
from zope.component import getUtility
from zope.formlib.form import FormFields, action
from zope.app.form.browser import TextWidget, CheckBoxWidget
from Products.Five.formlib.formbase import PageForm
from Products.CMFCore.utils import getToolByName
from collective.collection.alphabetic.interfaces import ICharacterOptions, ICharacterTokens
from collective.collection.alphabetic import CollectionAlphabeticMessageFactory as _

class CharacterOptionsView(PageForm):
    __module__ = __name__
    form_fields = FormFields(ICharacterOptions)
    label = _('Character Options')

    def __call__(self):
        self.request.set('disable_border', True)
        fields = self.form_fields
        fields['use_alphabet'].custom_widget = UseAlphabetWidget
        fields['character_tokens'].custom_widget = CharacterTokensWidget
        return super(CharacterOptionsView, self).__call__()

    @action(_('Save'))
    def action_save(self, action, data):
        site = getSite()
        use_alphabet = data.get('use_alphabet')
        character_tokens = data.get('character_tokens')
        ct = getUtility(ICharacterTokens)
        if character_tokens:
            character_tokens = ct(character_tokens, use_alphabet)
        properties = getToolByName(site, 'portal_properties').collection_alphabetic_properties
        properties.manage_changeProperties(use_alphabet=use_alphabet, character_tokens=character_tokens)


class UseAlphabetWidget(CheckBoxWidget):
    __module__ = __name__

    def _toFormValue(self, value):
        site = getSite()
        properties = getToolByName(site, 'portal_properties').collection_alphabetic_properties
        if properties.getProperty('use_alphabet'):
            return 'on'


class CharacterTokensWidget(TextWidget):
    __module__ = __name__

    def _toFormValue(self, value):
        site = getSite()
        properties = getToolByName(site, 'portal_properties').collection_alphabetic_properties
        character_tokens = properties.getProperty('character_tokens')
        if value == self.context.missing_value and character_tokens is not None and len(character_tokens) != 0:
            charset = site.management_page_charset
            encoded_character = [ character.encode(charset) for character in properties.getProperty('character_tokens') ]
            return ('').join(properties.getProperty('character_tokens'))
        else:
            return self._missing
        return