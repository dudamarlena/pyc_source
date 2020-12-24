# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/channel/vocabulary.py
# Compiled at: 2008-12-22 07:37:15
"""The Channel vocabulary class.

$Id: vocabulary.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.interface import classProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.app.component.vocabulary import UtilityVocabulary
from interfaces import IChannel

class ChannelsVocabulary(UtilityVocabulary):
    __module__ = __name__
    classProvides(IVocabularyFactory)
    interface = IChannel
    nameOnly = True