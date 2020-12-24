# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/i18n.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 2555 bytes
import os, gettext
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locale')
language = gettext.translation('electrum', LOCALE_DIR, fallback=True)

def _(x):
    global language
    return language.gettext(x)


def set_language(x):
    global language
    if x:
        language = gettext.translation('electrum', LOCALE_DIR, fallback=True, languages=[x])


languages = {'':_('Default'), 
 'ar_SA':_('Arabic'), 
 'bg_BG':_('Bulgarian'), 
 'cs_CZ':_('Czech'), 
 'da_DK':_('Danish'), 
 'de_DE':_('German'), 
 'el_GR':_('Greek'), 
 'eo_UY':_('Esperanto'), 
 'en_UK':_('English'), 
 'es_ES':_('Spanish'), 
 'fa_IR':_('Persian'), 
 'fr_FR':_('French'), 
 'hu_HU':_('Hungarian'), 
 'hy_AM':_('Armenian'), 
 'id_ID':_('Indonesian'), 
 'it_IT':_('Italian'), 
 'ja_JP':_('Japanese'), 
 'ky_KG':_('Kyrgyz'), 
 'lv_LV':_('Latvian'), 
 'nb_NO':_('Norwegian Bokmal'), 
 'nl_NL':_('Dutch'), 
 'pl_PL':_('Polish'), 
 'pt_BR':_('Brasilian'), 
 'pt_PT':_('Portuguese'), 
 'ro_RO':_('Romanian'), 
 'ru_RU':_('Russian'), 
 'sk_SK':_('Slovak'), 
 'sl_SI':_('Slovenian'), 
 'sv_SE':_('Swedish'), 
 'ta_IN':_('Tamil'), 
 'th_TH':_('Thai'), 
 'tr_TR':_('Turkish'), 
 'uk_UA':_('Ukrainian'), 
 'vi_VN':_('Vietnamese'), 
 'zh_CN':_('Chinese Simplified'), 
 'zh_TW':_('Chinese Traditional')}