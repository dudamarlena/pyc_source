# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/PyArabic/araby_constants.py
# Compiled at: 2015-06-30 06:52:38
import re
A = '،'
SEMICOLON = '؛'
QUESTION = '؟'
HAMZA = 'ء'
ALEF_MADDA = 'آ'
ALEF_HAMZA_ABOVE = 'أ'
WAW_HAMZA = 'ؤ'
ALEF_HAMZA_BELOW = 'إ'
YEH_HAMZA = 'ئ'
ALEF = 'ا'
BEH = 'ب'
TEH_MARBUTA = 'ة'
TEH = 'ت'
THEH = 'ث'
JEEM = 'ج'
HAH = 'ح'
KHAH = 'خ'
DAL = 'د'
THAL = 'ذ'
REH = 'ر'
ZAIN = 'ز'
SEEN = 'س'
SHEEN = 'ش'
SAD = 'ص'
DAD = 'ض'
TAH = 'ط'
ZAH = 'ظ'
AIN = 'ع'
GHAIN = 'غ'
TATWEEL = 'ـ'
FEH = 'ف'
QAF = 'ق'
KAF = 'ك'
LAM = 'ل'
MEEM = 'م'
NOON = 'ن'
HEH = 'ه'
WAW = 'و'
ALEF_MAKSURA = 'ى'
YEH = 'ي'
MADDA_ABOVE = 'ٓ'
HAMZA_ABOVE = 'ٔ'
HAMZA_BELOW = 'ٕ'
ZERO = '٠'
ONE = '١'
TWO = '٢'
THREE = '٣'
FOUR = '٤'
FIVE = '٥'
SIX = '٦'
SEVEN = '٧'
EIGHT = '٨'
NINE = '٩'
PERCENT = '٪'
DECIMAL = '٫'
THOUSANDS = '٬'
STAR = '٭'
MINI_ALEF = 'ٰ'
ALEF_WASLA = 'ٱ'
FULL_STOP = '۔'
BYTE_ORDER_MARK = '\ufeff'
FATHATAN = 'ً'
DAMMATAN = 'ٌ'
KASRATAN = 'ٍ'
FATHA = 'َ'
DAMMA = 'ُ'
KASRA = 'ِ'
SHADDA = 'ّ'
SUKUN = 'ْ'
SMALL_ALEF = 'ٰ'
SMALL_WAW = 'ۥ'
SMALL_YEH = 'ۦ'
LAM_ALEF = 'ﻻ'
LAM_ALEF_HAMZA_ABOVE = 'ﻷ'
LAM_ALEF_HAMZA_BELOW = 'ﻹ'
LAM_ALEF_MADDA_ABOVE = 'ﻵ'
simple_LAM_ALEF = 'لا'
simple_LAM_ALEF_HAMZA_ABOVE = 'لأ'
simple_LAM_ALEF_HAMZA_BELOW = 'لإ'
simple_LAM_ALEF_MADDA_ABOVE = 'لآ'
LETTERS = ('').join([
 ALEF, BEH, TEH, TEH_MARBUTA, THEH, JEEM, HAH, KHAH,
 DAL, THAL, REH, ZAIN, SEEN, SHEEN, SAD, DAD, TAH, ZAH,
 AIN, GHAIN, FEH, QAF, KAF, LAM, MEEM, NOON, HEH, WAW, YEH,
 HAMZA, ALEF_MADDA, ALEF_HAMZA_ABOVE, WAW_HAMZA, ALEF_HAMZA_BELOW, YEH_HAMZA])
TASHKEEL = (
 FATHATAN, DAMMATAN, KASRATAN,
 FATHA, DAMMA, KASRA,
 SUKUN,
 SHADDA)
HARAKAT = (FATHATAN, DAMMATAN, KASRATAN,
 FATHA, DAMMA, KASRA,
 SUKUN)
SHORTHARAKAT = (
 FATHA, DAMMA, KASRA, SUKUN)
TANWIN = (
 FATHATAN, DAMMATAN, KASRATAN)
LIGUATURES = (
 LAM_ALEF,
 LAM_ALEF_HAMZA_ABOVE,
 LAM_ALEF_HAMZA_BELOW,
 LAM_ALEF_MADDA_ABOVE)
HAMZAT = (
 HAMZA,
 WAW_HAMZA,
 YEH_HAMZA,
 HAMZA_ABOVE,
 HAMZA_BELOW,
 ALEF_HAMZA_BELOW,
 ALEF_HAMZA_ABOVE)
ALEFAT = (
 ALEF,
 ALEF_MADDA,
 ALEF_HAMZA_ABOVE,
 ALEF_HAMZA_BELOW,
 ALEF_WASLA,
 ALEF_MAKSURA,
 SMALL_ALEF)
WEAK = (
 ALEF, WAW, YEH, ALEF_MAKSURA)
YEHLIKE = (YEH, YEH_HAMZA, ALEF_MAKSURA, SMALL_YEH)
WAWLIKE = (
 WAW, WAW_HAMZA, SMALL_WAW)
TEHLIKE = (TEH, TEH_MARBUTA)
SMALL = (
 SMALL_ALEF, SMALL_WAW, SMALL_YEH)
MOON = (HAMZA,
 ALEF_MADDA,
 ALEF_HAMZA_ABOVE,
 ALEF_HAMZA_BELOW,
 ALEF,
 BEH,
 JEEM,
 HAH,
 KHAH,
 AIN,
 GHAIN,
 FEH,
 QAF,
 KAF,
 MEEM,
 HEH,
 WAW,
 YEH)
SUN = (
 TEH,
 THEH,
 DAL,
 THAL,
 REH,
 ZAIN,
 SEEN,
 SHEEN,
 SAD,
 DAD,
 TAH,
 ZAH,
 LAM,
 NOON)
AlphabeticOrder = {ALEF: 1, 
   BEH: 2, 
   TEH: 3, 
   TEH_MARBUTA: 3, 
   THEH: 4, 
   JEEM: 5, 
   HAH: 6, 
   KHAH: 7, 
   DAL: 8, 
   THAL: 9, 
   REH: 10, 
   ZAIN: 11, 
   SEEN: 12, 
   SHEEN: 13, 
   SAD: 14, 
   DAD: 15, 
   TAH: 16, 
   ZAH: 17, 
   AIN: 18, 
   GHAIN: 19, 
   FEH: 20, 
   QAF: 21, 
   KAF: 22, 
   LAM: 23, 
   MEEM: 24, 
   NOON: 25, 
   HEH: 26, 
   WAW: 27, 
   YEH: 28, 
   HAMZA: 29, 
   ALEF_MADDA: 29, 
   ALEF_HAMZA_ABOVE: 29, 
   WAW_HAMZA: 29, 
   ALEF_HAMZA_BELOW: 29, 
   YEH_HAMZA: 29}
NAMES = {ALEF: 'ألف', 
   BEH: 'باء', 
   TEH: 'تاء', 
   TEH_MARBUTA: 'تاء مربوطة', 
   THEH: 'ثاء', 
   JEEM: 'جيم', 
   HAH: 'حاء', 
   KHAH: 'خاء', 
   DAL: 'دال', 
   THAL: 'ذال', 
   REH: 'راء', 
   ZAIN: 'زاي', 
   SEEN: 'سين', 
   SHEEN: 'شين', 
   SAD: 'صاد', 
   DAD: 'ضاد', 
   TAH: 'طاء', 
   ZAH: 'ظاء', 
   AIN: 'عين', 
   GHAIN: 'غين', 
   FEH: 'فاء', 
   QAF: 'قاف', 
   KAF: 'كاف', 
   LAM: 'لام', 
   MEEM: 'ميم', 
   NOON: 'نون', 
   HEH: 'هاء', 
   WAW: 'واو', 
   YEH: 'ياء', 
   HAMZA: 'همزة', 
   TATWEEL: 'تطويل', 
   ALEF_MADDA: 'ألف ممدودة', 
   ALEF_MAKSURA: 'ألف مقصورة', 
   ALEF_HAMZA_ABOVE: 'همزة على الألف', 
   WAW_HAMZA: 'همزة على الواو', 
   ALEF_HAMZA_BELOW: 'همزة تحت الألف', 
   YEH_HAMZA: 'همزة على الياء', 
   FATHATAN: 'فتحتان', 
   DAMMATAN: 'ضمتان', 
   KASRATAN: 'كسرتان', 
   FATHA: 'فتحة', 
   DAMMA: 'ضمة', 
   KASRA: 'كسرة', 
   SHADDA: 'شدة', 
   SUKUN: 'سكون'}
HARAKAT_pattern = re.compile('[' + ('').join(HARAKAT) + ']')
TASHKEEL_pattern = re.compile('[' + ('').join(TASHKEEL) + ']')
HAMZAT_pattern = re.compile('[' + ('').join(HAMZAT) + ']')
ALEFAT_pattern = re.compile('[' + ('').join(ALEFAT) + ']')
LIGUATURES_pattern = re.compile('[' + ('').join(LIGUATURES) + ']')