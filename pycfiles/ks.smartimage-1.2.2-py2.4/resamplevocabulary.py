# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimagecache/resamplevocabulary.py
# Compiled at: 2008-12-23 17:55:59
"""ScaleWidgets for the Zope 3 based smartimagecache package

$Id: resamplevocabulary.py 35335 2008-05-27 16:02:13Z anatoly $
"""
__author__ = 'Addrey Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 35335 $'
__date__ = '$Date: 2008-05-27 19:02:13 +0300 (Tue, 27 May 2008) $'
from zope.schema.vocabulary import SimpleVocabulary
from PIL import Image

def ResampleVocabulary(context):
    return SimpleVocabulary.fromItems((('NONE', Image.NONE), ('ANTIALIAS', Image.ANTIALIAS), ('BILINEAR', Image.BILINEAR), ('BICUBIC', Image.BICUBIC)))