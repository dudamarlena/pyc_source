# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Macros/I18n.py
# Compiled at: 2019-09-22 10:12:27
import gettext
_ = gettext.gettext

class I18n(object):

    def __init__(self, parser):
        pass

    def __call__(self, src, plural=None, n=None, id=None, domain=None, source=None, target=None, comment=None, parser=None, macros=None, isShortForm=False, EOLCharsInShortForm=None, startPos=None, endPos=None):
        """This is just a stub at this time.

           plural = the plural form of the message
           n = a sized argument to distinguish between single and plural forms

           id = msgid in the translation catalog
           domain = translation domain
           source = source lang
           target = a specific target lang
           comment = a comment to the translation team

        See the following for some ideas
        http://www.zope.org/DevHome/Wikis/DevSite/Projects/ComponentArchitecture/ZPTInternationalizationSupport

        Other notes:
        - There is no need to replicate the i18n:name attribute
          from plone/PTL, as cheetah placeholders serve the same purpose.
       """
        src = _(src)
        if isShortForm and endPos < len(parser):
            return src + EOLCharsInShortForm
        else:
            return src