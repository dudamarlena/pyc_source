# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zupo/work/niteoweb.plr/src/niteoweb.aweber/src/niteoweb/aweber/interfaces.py
# Compiled at: 2013-02-08 05:15:03
"""Settings interface for niteoweb.aweber."""
from five import grok
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from plone import api

class ListsVocabulary(object):
    """Vocabulary class for dynamic choice available list names field."""
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        """Read from available_lists_record."""
        result = None
        try:
            lists_record = api.portal.get_registry_record('niteoweb.aweber.available_lists_record')
            if lists_record:
                result = SimpleVocabulary.fromValues(lists_record)
            else:
                result = SimpleVocabulary.fromValues([])
        except KeyError:
            result = SimpleVocabulary.fromValues([])

        return result


grok.global_utility(ListsVocabulary, name='niteoweb.aweber.available_lists_vocabulary')

class IAweberSettings(Interface):
    """Settings interface for niteoweb.aweber."""
    app_id = schema.TextLine(title='App ID', required=False)
    authorization_code = schema.TextLine(title='Authorization Code', required=False)
    consumer_key = schema.TextLine(title='Consumer Key')
    consumer_secret = schema.TextLine(title='Consumer Secret')
    access_token = schema.TextLine(title='Access Token')
    access_secret = schema.TextLine(title='Access Secret')
    list_name = schema.Choice(title='List Name', vocabulary='niteoweb.aweber.available_lists_vocabulary', required=False)
    subscribe_fullname = schema.TextLine(title="Subscriber's full name", required=False)
    subscribe_email = schema.TextLine(title="Subscriber's email", required=False)