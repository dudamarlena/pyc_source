# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sf_www/mezzanine/personal/heroku/personal/portfolio/translation.py
# Compiled at: 2016-12-25 14:17:39
# Size of source mod 2**32: 830 bytes
from modeltranslation.translator import translator
from mezzanine.core.translation import TranslatedSlugged, TranslatedDisplayable, TranslatedRichText, TranslationOptions
from portfolio.models import PortfolioCategory, PortfolioPost, PortfolioImage

class TranslatedPortfolioPost(TranslatedDisplayable, TranslatedRichText):
    fields = ()


class TranslatedPortfolioCategory(TranslatedSlugged):
    fields = ()


class TranslatedPortfolioImage(TranslationOptions):
    fields = ('description', )


translator.register(PortfolioCategory, TranslatedPortfolioCategory)
translator.register(PortfolioPost, TranslatedPortfolioPost)
translator.register(PortfolioImage, TranslatedPortfolioImage)