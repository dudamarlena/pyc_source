# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/republisher/interfaces.py
# Compiled at: 2010-09-29 12:35:41
from z3c.form import interfaces
from zope.interface import Interface
from zope import schema

class IRepublisherSettings(Interface):
    """ The view for Republisher prefs form. """
    __module__ = __name__
    api_key = schema.TextLine(title='API key from Flickr', description='The app key given to you when you create your FLICKR app', required=False, default='88c9ed38ced3a04fa8c683f3eac9cd6f')
    api_secret = schema.TextLine(title='Flickr app secret', description='The secret that matches your api key', required=False, default='39615d0571871bdf')
    republisher_toggle = schema.Bool(title='Republisher on', description='Turn republisher on?', required=True, default=True)


class IRepublisherTokenKeeper(Interface):
    """A Record to keep the Authentication Tokens from the OAuth systems from the social networks"""
    __module__ = __name__
    flickr_token = schema.TextLine(title='Flickr Auth Token', default='None')
    flickr_frob = schema.TextLine(title='Flickr Auth Frob', default='None')