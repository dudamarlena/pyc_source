# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/pronounce.py
# Compiled at: 2016-02-21 15:02:52
import logging, re
AKAN_TWI = [
 ('fo$', 'foɔ', 'e.g. sɔfo -> sɔfoɔ'),
 ('gua', 'dwa'),
 ('mb', 'mm'),
 ('nd', 'nn'),
 ('nye', 'ne'),
 ('nyi', 'ni'),
 ('te$', 'teɛ', 'e.g. aberante -> aberanteɛ'),
 ('tu$', 'tuo', 'e.g. afotu -> afotuo')]
AKAN_FANTI = [
 ('a(?P<consonant>[^aeɛioɔu])i', 'e\\g<consonant>i', 'e.g. adiban -> ediban'),
 ('a(?P<consonant>[^aeɛioɔu])u', 'e\\g<consonant>u', 'e.g. aduonu -> eduonu'),
 ('de', 'dze'),
 ('di', 'dzi'),
 ('te', 'tse'),
 ('e(?P<consonant>[^aeɛioɔu])e', 'e\\g<consonant>', 'e.g. bere -> ber'),
 ('iri', 'ir'),
 ('iri', 'ir'),
 ('oro', 'or'),
 ('ti', 'tsi')]
GEEZ = [
 ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
 ('ha', 'ሀ'), ('hu', 'ሁ'), ('hi', 'ሂ'), ('haa', 'ሃ'), ('he', 'ሄ'), ('hii', 'ህ'), ('ho', 'ሆ'),
 ('la', 'ለ'), ('lu', 'ሉ'), ('li', 'ሊ'), ('laa', 'ላ'), ('le', 'ሌ'), ('lii', 'ል'), ('lo', 'ሎ'),
 ('hwa', 'ሐ'), ('hwu', 'ሑ'), ('hwii', 'ሒ'), ('hwaa', 'ሓ'), ('hwe', 'ሔ'), ('hwi', 'ሕ'), ('hwo', 'ሖ'),
 ('ma', 'መ'), ('mu', 'ሙ'), ('mii', 'ሚ'), ('maa', 'ማ'), ('me', 'ሜ'), ('mi', 'ም'), ('mo', 'ሞ'),
 ('sa', 'ሠ'), ('su', 'ሡ'), ('sii', 'ሢ'), ('saa', 'ሣ'), ('se', 'ሤ'), ('si', 'ሥ'), ('so', 'ሦ'),
 ('ra', 'ረ'), ('ru', 'ሩ'), ('rii', 'ሪ'), ('raa', 'ራ'), ('re', 'ሬ'), ('ri', 'ር'), ('ro', 'ሮ'),
 ('ssa', 'ሰ'), ('ssu', 'ሱ'), ('ssii', 'ሲ'), ('ssaa', 'ሳ'), ('sse', 'ሴ'), ('ssi', 'ስ'), ('sso', 'ሶ'),
 ('sha', 'ሸ'), ('shu', 'ሹ'), ('shii', 'ሺ'), ('shaa', 'ሻ'), ('she', 'ሼ'), ('shi', 'ሽ'), ('sho', 'ሾ'),
 ('ka', 'ቀ'), ('ku', 'ቁ'), ('kii', 'ቂ'), ('kaa', 'ቃ'), ('ke', 'ቄ'), ('ki', 'ቅ'), ('ko', 'ቆ'),
 ('qa', 'ቐ'), ('qu', 'ቑ'), ('qii', 'ቒ'), ('qaa', 'ቓ'), ('qe', 'ቔ'), ('qi', 'ቕ'), ('qo', 'ቖ'),
 ('ba', 'በ'), ('bu', 'ቡ'), ('bii', 'ቢ'), ('baa', 'ባ'), ('be', 'ቤ'), ('bi', 'ብ'), ('bo', 'ቦ'),
 ('bwa', 'ቧ'),
 ('va', 'ቨ'), ('vu', 'ቩ'), ('vii', 'ቪ'), ('vaa', 'ቫ'), ('ve', 'ቬ'), ('vi', 'ቭ'), ('vo', 'ቮ'),
 ('ta', 'ተ'), ('tu', 'ቱ'), ('tii', 'ቲ'), ('taa', 'ታ'), ('te', 'ቴ'), ('ti', 'ት'), ('to', 'ቶ'),
 ('cha', 'ቸ'), ('chu', 'ቹ'), ('chii', 'ቺ'), ('chaa', 'ቻ'), ('che', 'ቼ'), ('chi', 'ች'), ('cho', 'ቾ'),
 ('hya', 'ኀ'), ('hyu', 'ኁ'), ('hyii', 'ኂ'), ('hyaa', 'ኃ'), ('hye', 'ኄ'), ('hyi', 'ኅ'), ('hyo', 'ኆ'), ('hywa', 'ኈ'), ('hywii', 'ኊ'), ('hywaa', 'ኋ'), ('hywe', 'ኌ'), ('hywi', 'ኍ'),
 ('naa', 'ነ'), ('nu', 'ኑ'), ('nii', 'ኒ'), ('na', 'ና'), ('ne', 'ኔ'), ('ni', 'ን'), ('no', 'ኖ'),
 ('nwa', 'ኗ'),
 ('gna', 'ኘ'), ('gnu', 'ኙ'), ('gni', 'ኚ'), ('gnaa', 'ኛ'), ('gne', 'ኜ'), ('gnii', 'ኝ'), ('gno', 'ኞ'),
 ('a', 'አ'), ('u', 'ኡ'), ('ii', 'ኢ'), ('aa', 'ኣ'), ('e', 'ኤ'), ('i', 'እ'), ('o', 'ኦ'),
 ('kha', 'ከ'), ('khu', 'ኩ'), ('khii', 'ኪ'), ('khaa', 'ካ'), ('khe', 'ኬ'), ('khi', 'ክ'), ('kho', 'ኮ'), ('khwa', 'ኰ'), ('khwii', 'ኲ'), ('khwaa', 'ኳ'), ('khwe', 'ኴ'), ('khwi', 'ኵ'),
 ('ksa', 'ኸ'), ('ksu', 'ኹ'), ('ksii', 'ኺ'), ('ksaa', 'ኻ'), ('kse', 'ኼ'), ('ksi', 'ኽ'), ('kso', 'ኾ'), ('kswa', 'ዀ'), ('kswii', 'ዂ'), ('kswaa', 'ዃ'), ('kswe', 'ዄ'), ('kswi', 'ዅ'),
 ('wa', 'ወ'), ('wu', 'ዉ'), ('wii', 'ዊ'), ('waa', 'ዋ'), ('we', 'ዌ'), ('wi', 'ው'), ('wo', 'ዎ'),
 ('ja', 'ዐ'), ('ju', 'ዑ'), ('jii', 'ዒ'), ('jaa', 'ዓ'), ('je', 'ዔ'), ('ji', 'ዕ'), ('jo', 'ዖ'),
 ('za', 'ዘ'), ('zu', 'ዙ'), ('zii', 'ዚ'), ('zaa', 'ዛ'), ('ze', 'ዜ'), ('zi', 'ዝ'), ('zo', 'ዞ'), ('zwaa', 'ዟ'),
 ('dza', 'ዠ'), ('dzu', 'ዡ'), ('dzii', 'ዢ'), ('dzaa', 'ዣ'), ('dze', 'ዤ'), ('dzi', 'ዥ'), ('dzo', 'ዦ'),
 ('ya', 'የ'), ('yu', 'ዩ'), ('yii', 'ዪ'), ('yaa', 'ያ'), ('ye', 'ዬ'), ('yi', 'ይ'), ('yo', 'ዮ'),
 ('da', 'ደ'), ('du', 'ዱ'), ('dii', 'ዲ'), ('daa', 'ዳ'), ('de', 'ዴ'), ('di', 'ድ'), ('do', 'ዶ'),
 ('gha', 'ጀ'), ('ghu', 'ጁ'), ('ghii', 'ጂ'), ('ghaa', 'ጃ'), ('ghe', 'ጄ'), ('ghi', 'ጅ'), ('gho', 'ጆ'),
 ('ga', 'ገ'), ('gu', 'ጉ'), ('gii', 'ጊ'), ('gaa', 'ጋ'), ('ge', 'ጌ'), ('gi', 'ግ'), ('go', 'ጎ'),
 ('tha', 'ጠ'), ('thu', 'ጡ'), ('thii', 'ጢ'), ('thaa', 'ጣ'), ('the', 'ጤ'), ('thi', 'ጥ'), ('tho', 'ጦ'),
 ('cza', 'ጨ'), ('czu', 'ጩ'), ('czii', 'ጪ'), ('czaa', 'ጫ'), ('cze', 'ጬ'), ('czi', 'ጭ'), ('czo', 'ጮ'),
 ('pha', 'ጰ'), ('phu', 'ጱ'), ('phii', 'ጲ'), ('phaa', 'ጳ'), ('phe', 'ጴ'), ('phi', 'ጵ'), ('pho', 'ጶ'),
 ('sza', 'ጸ'), ('szu', 'ጹ'), ('szii', 'ጺ'), ('szaa', 'ጻ'), ('sze', 'ጼ'), ('szi', 'ጽ'), ('szo', 'ጾ'),
 ('zsa', 'ፀ'), ('zsu', 'ፁ'), ('zsii', 'ፂ'), ('zsaa', 'ፃ'), ('zse', 'ፄ'), ('tze', 'ፅ'), ('zso', 'ፆ'),
 ('fa', 'ፈ'), ('fu', 'ፉ'), ('fii', 'ፊ'), ('faa', 'ፋ'), ('fe', 'ፌ'), ('fi', 'ፍ'), ('fo', 'ፎ'),
 ('pa', 'ፐ'), ('pu', 'ፑ'), ('pii', 'ፒ'), ('paa', 'ፓ'), ('pe', 'ፔ'), ('pi', 'ፕ'), ('po', 'ፖ'),
 ('gwa', 'ጐ'), ('gwaa', 'ጓ'),
 ('lwa', 'ሏ'),
 ('qwaa', 'ቋ'),
 ('swa', 'ሷ'),
 ('zhwa', 'ዧ')]
SINHALA = [
 ('a', 'අ'), ('aa', 'ා'), ('ee', 'ේ'), ('ɛ', 'ඇ'), ('ɛ', 'ැ'), ('ɛɛ', 'ෑ'), ('i', 'ි'), ('ii', 'ී'), ('o', 'ඔ'), ('o', 'ො'), ('oo', 'ෝ'), ('u', 'ු'), ('uu', 'ූ'), ('h', '්'), ('_', 'ණ'), ('_', 'ළ'), ('_', 'ට'),
 ('ba', 'බ'),
 ('da', 'ද'),
 ('ga', 'ග'),
 ('ha', 'හ'),
 ('ka', 'ක'),
 ('ja', 'ජ'),
 ('la', 'ල'),
 ('na', 'න'), ('nha', 'ඳ'),
 ('ma', 'ම'),
 ('pa', 'ප'),
 ('ra', 'ර'),
 ('sa', 'ස'),
 ('ta', 'ත'),
 ('tha', 'ථ'),
 ('va', 'ව'),
 ('ya', 'ය')]

def get_twi(word, pos):
    """Return Asante Twi pronunciation of Akan spelling."""
    twi = word
    for sub in AKAN_TWI:
        if len(sub) == 3:
            twi = re.sub(sub[0], sub[1], twi)
        else:
            twi = twi.replace(sub[0], sub[1])

    return twi.lower()


def get_fanti(word, pos):
    """Return Fante pronunciation of Akan spelling."""
    fanti = word
    if word in 'dede':
        return word
    for sub in AKAN_FANTI:
        if len(sub) == 3:
            fanti = re.sub(sub[0], sub[1], fanti)
        else:
            fanti = fanti.replace(sub[0], sub[1])

    return fanti.lower()


def from_twi(word, pos):
    """Convert Twi pronunciation to Akan spelling."""
    akan = word.lower()
    for sub in AKAN_TWI:
        if len(sub) == 3:
            akan = re.sub(sub[1], sub[0], akan)
        else:
            akan = akan.replace(sub[1], sub[0])

    return akan


def from_fanti(word, pos):
    """Convert Fante pronunciation to Akan spelling."""
    akan = word
    for sub in AKAN_FANTI:
        if len(sub) == 3:
            akan = re.sub(sub[1], sub[0], akan)
        else:
            akan = akan.replace(sub[1], sub[0])

    return akan


def sinhala_to_latin():
    """Return a dictionary of Geez characters and their latin tokens."""
    ltg = {}
    for pair in SINHALA:
        ltg[pair[1]] = pair[0]

    return ltg


def geez_to_latin():
    """Return a dictionary of Geez characters and their latin tokens."""
    ltg = {}
    for pair in GEEZ:
        ltg[pair[1]] = pair[0]

    return ltg


def geez_to_latin():
    """Return a dictionary of Geez characters and their latin tokens."""
    ltg = {}
    for pair in GEEZ:
        ltg[pair[1]] = pair[0]

    return ltg


def latin_to_geez():
    """Return a dictionary of latin tokens and their Geez characters."""
    ltg = {}
    for pair in GEEZ:
        ltg[pair[0]] = pair[1]

    return ltg


def tokenize_geez(word):
    latin_tokens = geez_to_latin().values()
    vowels = 'aeiou'
    tokens = []
    sofar = ''
    count = 0
    word_length = len(word)
    for c in word:
        count += 1
        sofar += c
        if count < word_length and word[count] in vowels:
            continue
        if sofar in latin_tokens:
            tokens.append(sofar)
            sofar = ''
        else:
            continue

    return tokens


def get_geez(word):
    """Given a Unicode string of kasahorow Tigrinya, return the phonetic Tigrinya Abugida."""
    pron = ''
    latin = word.lower()
    ti_pron = latin
    to_geez = latin_to_geez()
    tokens = tokenize_geez(latin)
    if len(tokens) > 1:
        tokens.sort(key=len)
        tokens.reverse()
    for token in tokens:
        ti_pron = ti_pron.replace(token, to_geez[token])

    pron = ti_pron
    return pron


def get_latin(geez):
    latin = ''
    tokens = geez
    gtl = geez_to_latin()
    for token in tokens:
        if token.strip():
            latin += gtl[token]
        else:
            latin += token

    return latin


def abugida_to_latin(abugida, language):
    latin = ''
    tokens = abugida
    gtl = abugida_to_latin_map(language)
    for token in tokens:
        if token.strip():
            latin += gtl[token]
        else:
            latin += token

    return latin


def abugida_to_latin_map(language):
    if language in ('amarinya', 'geez', 'tigrinya'):
        alphabet_map = GEEZ
    else:
        if 'sinhala' == language:
            alphabet_map = SINHALA
        ltg = {}
        for pair in alphabet_map:
            ltg[pair[1]] = pair[0]

    return ltg


def find_and_replace(word, subs):
    """Return Kirundi pronunciation of Ururimi spelling."""
    ru = word
    for sub in subs:
        if len(sub) == 3:
            ru = re.sub(sub[0], sub[1], ru)
        else:
            ru = ru.replace(sub[0], sub[1])

    return ru.lower()


def get_ururimi(word, style):
    if 'kirundi' == style:
        subs = [
         ('cy', 'c'), ('jy', 'j'), ('shy', 'sh'), ('by', 'vy')]
        word = find_and_replace(word, subs)
    return word


def get_yoruba(word, style):
    if 'oyo' == style:
        subs = [
         ('ah', 'á'), ('ha', 'à'), ('eh', 'é'), ('he', 'è'),
         ('ẹh', 'ẹ́'), ('hẹ', 'ẹ̀'), ('ih', 'í'), ('hi', 'ì'),
         ('oh', 'ó'), ('ho', 'ò'), ('ọh', 'ọ́'), ('họ', 'ọ̀'),
         ('uh', 'ú'), ('hu', 'ù')]
        word = find_and_replace(word, subs)
    return word


def get_phonetic(word, lang):
    phonetic = ''
    if lang == 'akan':
        phonetic = get_twi(word, 'noun')
    elif lang in ('amaarignaa', 'geez', 'tigirignaa'):
        phonetic = get_latin(word)
    elif lang in ('kirundi', 'kinyarwanda'):
        phonetic = get_ururimi(word, lang)
    elif lang == 'sinhala':
        phonetic = abugida_to_latin(word, 'sinhala')
    elif lang == 'yoruba':
        phonetic = get_yoruba(word, 'oyo')
    return phonetic