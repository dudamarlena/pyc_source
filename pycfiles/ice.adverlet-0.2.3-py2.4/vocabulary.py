# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/vocabulary.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope.component import getUtilitiesFor
from zope.schema.vocabulary import SimpleVocabulary

def tinyMcePluginsVocabulary(context):
    plugins = [
     'style', 'layer', 'table', 'save', 'advhr', 'advimage', 'advlink', 'emotions', 'iespell', 'insertdatetime', 'preview', 'zoom', 'media', 'searchreplace', 'print', 'contextmenu', 'paste', 'directionality', 'fullscreen', 'noneditable', 'visualchars', 'nonbreaking', 'xhtmlxtras']
    return SimpleVocabulary.fromValues(plugins)