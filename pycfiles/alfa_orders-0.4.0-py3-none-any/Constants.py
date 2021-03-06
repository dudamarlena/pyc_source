# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Constants.py
# Compiled at: 2015-06-30 06:52:38
SHAPING = {'ء': 'ﺀ', 
   'آ': ('ﺁ', 'ﺂ'), 
   'أ': ('ﺃ', 'ﺄ'), 
   'ؤ': ('ﺅ', 'ﺆ'), 
   'إ': ('ﺇ', 'ﺈ'), 
   'ئ': ('ﺉ', 'ﺋ', 'ﺌ', 'ﺊ'), 
   'ا': ('ﺍ', 'ﺎ'), 
   'ب': ('ﺏ', 'ﺑ', 'ﺒ', 'ﺐ'), 
   'ة': ('ﺓ', 'ﺔ'), 
   'ت': ('ﺕ', 'ﺗ', 'ﺘ', 'ﺖ'), 
   'ث': ('ﺙ', 'ﺛ', 'ﺜ', 'ﺚ'), 
   'ج': ('ﺝ', 'ﺟ', 'ﺠ', 'ﺞ'), 
   'ح': ('ﺡ', 'ﺣ', 'ﺤ', 'ﺢ'), 
   'خ': ('ﺥ', 'ﺧ', 'ﺨ', 'ﺦ'), 
   'د': ('ﺩ', 'ﺪ'), 
   'ذ': ('ﺫ', 'ﺬ'), 
   'ر': ('ﺭ', 'ﺮ'), 
   'ز': ('ﺯ', 'ﺰ'), 
   'س': ('ﺱ', 'ﺳ', 'ﺴ', 'ﺲ'), 
   'ش': ('ﺵ', 'ﺷ', 'ﺸ', 'ﺶ'), 
   'ص': ('ﺹ', 'ﺻ', 'ﺼ', 'ﺺ'), 
   'ض': ('ﺽ', 'ﺿ', 'ﻀ', 'ﺾ'), 
   'ط': ('ﻁ', 'ﻃ', 'ﻄ', 'ﻂ'), 
   'ظ': ('ﻅ', 'ﻇ', 'ﻈ', 'ﻆ'), 
   'ع': ('ﻉ', 'ﻋ', 'ﻌ', 'ﻊ'), 
   'غ': ('ﻍ', 'ﻏ', 'ﻐ', 'ﻎ'), 
   'ـ': 'ـ', 
   'ف': ('ﻑ', 'ﻓ', 'ﻔ', 'ﻒ'), 
   'ق': ('ﻕ', 'ﻗ', 'ﻘ', 'ﻖ'), 
   'ك': ('ﻙ', 'ﻛ', 'ﻜ', 'ﻚ'), 
   'ل': ('ﻝ', 'ﻟ', 'ﻠ', 'ﻞ'), 
   'م': ('ﻡ', 'ﻣ', 'ﻤ', 'ﻢ'), 
   'ن': ('ﻥ', 'ﻧ', 'ﻨ', 'ﻦ'), 
   'ه': ('ﻩ', 'ﻫ', 'ﻬ', 'ﻪ'), 
   'و': ('ﻭ', 'ﻮ'), 
   'ى': ('ﻯ', 'ﻰ'), 
   'ي': ('ﻱ', 'ﻳ', 'ﻴ', 'ﻲ')}
INVERTEDSHAPING = {'ﺃ': 'أ', 
   'ﺇ': 'إ', 
   'ﺋ': 'ئ', 
   'ﺏ': 'ب', 
   'ﺓ': 'ة', 
   'ﺗ': 'ت', 
   'ﺛ': 'ث', 
   'ﺟ': 'ج', 
   'ﺣ': 'ح', 
   'ﺧ': 'خ', 
   'ﺫ': 'ذ', 
   'ﺯ': 'ز', 
   'ﺳ': 'س', 
   'ﺷ': 'ش', 
   'ﺻ': 'ص', 
   'ﺿ': 'ض', 
   'ـ': 'ـ', 
   'ﻃ': 'ط', 
   'ﻇ': 'ظ', 
   'ﻋ': 'ع', 
   'ﻏ': 'غ', 
   'ﻓ': 'ف', 
   'ﻗ': 'ق', 
   'ﻛ': 'ك', 
   'ﻟ': 'ل', 
   'ﻣ': 'م', 
   'ﻧ': 'ن', 
   'ﻫ': 'ه', 
   'ﻯ': 'ى', 
   'ﻳ': 'ي', 
   'ﺀ': 'ء', 
   'ﺄ': 'أ', 
   'ﺈ': 'إ', 
   'ﺌ': 'ئ', 
   'ﺐ': 'ب', 
   'ﺔ': 'ة', 
   'ﺘ': 'ت', 
   'ﺜ': 'ث', 
   'ﺠ': 'ج', 
   'ﺤ': 'ح', 
   'ﺨ': 'خ', 
   'ﺬ': 'ذ', 
   'ﺰ': 'ز', 
   'ﺴ': 'س', 
   'ﺸ': 'ش', 
   'ﺼ': 'ص', 
   'ﻀ': 'ض', 
   'ﻄ': 'ط', 
   'ﻈ': 'ظ', 
   'ﻌ': 'ع', 
   'ﻐ': 'غ', 
   'ﻔ': 'ف', 
   'ﻘ': 'ق', 
   'ﻜ': 'ك', 
   'ﻠ': 'ل', 
   'ﻤ': 'م', 
   'ﻨ': 'ن', 
   'ﻬ': 'ه', 
   'ﻰ': 'ى', 
   'ﻴ': 'ي', 
   'ﺁ': 'آ', 
   'ﺅ': 'ؤ', 
   'ﺉ': 'ئ', 
   'ﺍ': 'ا', 
   'ﺑ': 'ب', 
   'ﺕ': 'ت', 
   'ﺙ': 'ث', 
   'ﺝ': 'ج', 
   'ﺡ': 'ح', 
   'ﺥ': 'خ', 
   'ﺩ': 'د', 
   'ﺭ': 'ر', 
   'ﺱ': 'س', 
   'ﺵ': 'ش', 
   'ﺹ': 'ص', 
   'ﺽ': 'ض', 
   'ﻁ': 'ط', 
   'ﻅ': 'ظ', 
   'ﻉ': 'ع', 
   'ﻍ': 'غ', 
   'ﻑ': 'ف', 
   'ﻕ': 'ق', 
   'ﻙ': 'ك', 
   'ﻝ': 'ل', 
   'ﻡ': 'م', 
   'ﻥ': 'ن', 
   'ﻩ': 'ه', 
   'ﻭ': 'و', 
   'ﻱ': 'ي', 
   'ﺂ': 'آ', 
   'ﺆ': 'ؤ', 
   'ﺊ': 'ئ', 
   'ﺎ': 'ا', 
   'ﺒ': 'ب', 
   'ﺖ': 'ت', 
   'ﺚ': 'ث', 
   'ﺞ': 'ج', 
   'ﺢ': 'ح', 
   'ﺦ': 'خ', 
   'ﺪ': 'د', 
   'ﺮ': 'ر', 
   'ﺲ': 'س', 
   'ﺶ': 'ش', 
   'ﺺ': 'ص', 
   'ﺾ': 'ض', 
   'ﻂ': 'ط', 
   'ﻆ': 'ظ', 
   'ﻊ': 'ع', 
   'ﻎ': 'غ', 
   'ﻒ': 'ف', 
   'ﻖ': 'ق', 
   'ﻚ': 'ك', 
   'ﻞ': 'ل', 
   'ﻢ': 'م', 
   'ﻦ': 'ن', 
   'ﻪ': 'ه', 
   'ﻮ': 'و', 
   'ﻲ': 'ي'}
LANGS = {'el': 'Greek', 
   'eo': 'Esperanto', 
   'en': 'English', 
   'vi': 'Vietnamese', 
   'ca': 'Catalan', 
   'it': 'Italian', 
   'lb': 'Luxembourgish', 
   'eu': 'Basque', 
   'ar': 'Arabic', 
   'bg': 'Bulgarian', 
   'cs': 'Czech', 
   'et': 'Estonian', 
   'gl': 'Galician', 
   'id': 'Indonesian', 
   'ru': 'Russian', 
   'nl': 'Dutch', 
   'pt': 'Portuguese', 
   'no': 'Norwegian', 
   'tr': 'Turkish', 
   'lv': 'Latvian', 
   'lt': 'Lithuanian', 
   'th': 'Thai', 
   'es': 'Spanish', 
   'ro': 'Romanian', 
   'en_GB': 'British English', 
   'fr': 'French', 
   'hy': 'Armenian', 
   'uk': 'Ukrainian', 
   'pt_BR': 'Brazilian', 
   'hr': 'Croatian', 
   'de': 'German', 
   'da': 'Danish', 
   'fa': 'Persian', 
   'bs': 'Bosnian', 
   'fi': 'Finnish', 
   'hu': 'Hungarian', 
   'ja': 'Japanese', 
   'he': 'Hebrew', 
   'ka': 'Georgian', 
   'zh': 'Chinese', 
   'kk': 'Kazakh', 
   'sr': 'Serbian', 
   'sq': 'Albanian', 
   'ko': 'Korean', 
   'sv': 'Swedish', 
   'mk': 'Macedonian', 
   'sk': 'Slovak', 
   'pl': 'Polish', 
   'ms': 'Malay', 
   'sl': 'Slovenian', 
   'sw': 'Swahili', 
   'sd': 'Sindhi', 
   'ml': 'Malayalam', 
   'tg': 'Tajik', 
   'ta': 'Tamil', 
   'ur': 'Urdu', 
   'uz': 'Uzbek', 
   'hi': 'Hindi', 
   'tt': 'Tatar', 
   'so': 'Somali', 
   'az': 'Azerbaijani', 
   'bn': 'Bengali', 
   'dv': 'Divehi', 
   'ha': 'Hausa', 
   'ug': 'Uughur'}