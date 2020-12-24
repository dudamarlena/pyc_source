# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/PY3/CONJUGAR_/conjugar/acentuacion.py
# Compiled at: 2019-04-16 09:22:12
# Size of source mod 2**32: 16407 bytes
import estring.estring as eses, elist.elist as elel, conjugar.symmtera as symm, conjugar.araq as araq, spaint.spaint as spsp, copy

class Help:

    def __init__(self):
        self.DI_U = '\n            <diacritic> <U-diaeresi> <ü>\n            https://en.wikipedia.org/wiki/Umlaut_(diacritic)\n            Several languages use diaeresis over the letter U\n            to show that the letter is pronounced in its regular way,\n            without dropping out, building diphthongs with neighbours, etc.\n            In Spanish, it is used to distinguish between "gue"/"güe" [ɡe]/[ɡwe] and "gui"/"güi" [ɡi]/[ɡwi]:\n            nicaragüense (Nicaraguan), pingüino (penguin).\n        '
        self.AC_ = '\n            <acute> <áéíóú>\n            https://en.wikipedia.org/wiki/Acute_accent\n        '
        self.ENE = '\n            <ñ>\n        '
        self.UD_QM = '\n            <upside down question mark> <¿>\n        '
        self.UD_EXCM = '\n            <upside down exclamation mark> <¡>\n        '
        self.CE_C = '\n            <cedilla> <ç>\n            https://en.wikipedia.org/wiki/%C3%87\n        '
        self.CL_CONSONANT = '\n            <consonant clusters>\n            https://en.wikipedia.org/wiki/Consonant_cluster\n        '
        self.DI_CONSONANT = '\n            <digraph>\n            https://zh.wikipedia.org/wiki/%E4%BA%8C%E5%90%88%E5%AD%97%E6%AF%8D\n        '
        self.DIPTRONGO = '\n            https://es.wikipedia.org/wiki/Diptongo\n            Un diptongo es una cadena sonora que consiste en la articulación de dos vocales, \n            una a continuación de la otra, sin interrupción y produciéndose una transición suave \n            en las frecuencias sonoras que caracterizan los timbres de cada una de las dos vocales. \n            Fonológicamente dos vocales articuladas de esa manera forman parte de la misma sílaba.\n        '
        self.TRIPTONGO = '\n            https://es.wikipedia.org/wiki/Triptongo \n            En español, un triptongo es siempre la unión de tres vocales que se pronuncian en una misma sílaba,\n            dos de ellas cerradas y una abierta, según el esquema:\n            VD-VF-VD\n        '
        self.conclst = '\n            <consonant cluster> \n            such as: b,ch,pl,....\n        '
        self.vowclst = '\n            <vowel cluster>\n            such as: a,ui,uu,uay.....\n        '
        self.clstarr = "\n            <cluster array>\n            such as: \n                paraguayo\n                ['p','a','r','a','g','uay','y','o']\n        "
        self.slb = "\n            <silaba>\n            such as :\n                paraguayo\n                ['pa','ra','guay','yo']\n        "
        self.stress_silaba = "\n            <stress silaba>\n            such as :\n                paraguayo\n                ['pa','ra','guay','yo']\n                'guay' \n        "
        self.stress_char = "\n            <stress char>\n            such as :\n                paraguayo\n                ['pa','ra','guay','yo']\n                'guay'\n                'a' in 'guay'\n        "
        self.stress_silaba_clstloc = "\n            <stress silaba location in cluster array>\n            such as :\n                paraguayo\n                ['pa','ra','guay','yo']\n                the index of 'guay' in ['pa','ra','guay','yo'] is 2\n        "
        self.stress_char_slbloc = "\n            <stress char location in silaba>\n            such as :\n                paraguayo\n                ['pa','ra','guay','yo']\n                the index of 'a' in 'guay' is 2\n        "
        self.stress_silaba_wordspan = "\n            <stress silaba locattion-span inword>\n            such as :\n                paraguayo\n                ['pa','ra','guay','yo']\n                the span of 'guay' in paraguayo is (4,8)\n        "
        self.stress_char_wordloc = "\n            <stress char location inword>\n            such as :\n                paraguayo\n                ['pa','ra','guay','yo']\n                the index of 'a' <'a' in 'guay'> in paraguayo is 6\n                \n        "


DI_U = chr(252)
AC_A = chr(225)
AC_E = chr(233)
AC_O = chr(243)
AC_I = chr(237)
AC_U = chr(250)
ENE = chr(241)
UD_QM = chr(191)
UD_EXCM = chr(161)
CE_C = chr(231)
ALPHABETA = 'abcdefghijklmnopqrstuvwxyzáéíóúñü!¡?¿ç'
VOWEL_CHARS = 'aeiou'
STRONG_VOWEL_CHARS = 'aeo'
WEAK_VOWEL_CHARS = 'iu'
ACUTE_CHARS = 'áéíóú'
ACUTE_CHARS_MIRROR_DICT = {'a':'á', 
 'e':'é', 
 'i':'í', 
 'o':'ó', 
 'u':'ú', 
 'á':'a', 
 'é':'e', 
 'í':'i', 
 'ó':'o', 
 'ú':'u'}
VOWEL = [
 'a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú']
ACUTE_VOWEL = ['á', 'é', 'í', 'ó', 'ú']
NORMAL_VOWEL = ['a', 'e', 'i', 'o', 'u']
ACUTE_STRONG_VOWEL = ['á', 'é', 'ó']
ACUTE_WEAK_VOWEL = ['í', 'ú']
NORMAL_STRONG_VOWEL = ['a', 'e', 'o']
NORMAL_WEAK_VOWEL = ['i', 'u']
CONSONANT = [
 'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'ñ']
BI_CONSONANT = ['ch', 'll', 'rr', 'pl', 'bl', 'tl', 'dl', 'cl', 'gl', 'pr', 'br', 'tr', 'dr', 'cr', 'gr']
CL_CONSONANT = ['pl', 'bl', 'tl', 'dl', 'cl', 'gl', 'pr', 'br', 'tr', 'dr', 'cr', 'gr']
DI_CONSONANT = ['ch', 'll', 'rr']
Y_LAST = [
 '@']
Y_DIPTRONGO = ['ay', 'ey', 'oy', 'uy', 'áy', 'éy', 'óy', 'üy']
Y_TRIPTONGO = ['iay', 'iey', 'ioy', 'iáy', 'iéy', 'ióy', 'uay', 'uey', 'uoy', 'uáy', 'uéy', 'uóy', 'üey']
DIPTRONGO = [
 'ai', 'au', 'ei', 'eu', 'oi', 'ou', 'ia', 'ie', 'io', 'ua', 'ue', 'uo', 'iu', 'ui', 'ái', 'áu', 'éi', 'éu', 'ói', 'óu', 'iá', 'uá', 'ié', 'ué', 'ió', 'uó', 'üe', 'üi']
TRIPTONGO = ['iai', 'iau', 'iei', 'ieu', 'ioi', 'iou', 'iái', 'iáu', 'iéi', 'iéu', 'iói', 'ióu', 'uai', 'uau', 'uei', 'ueu', 'uoi', 'uou', 'uái', 'uáu', 'uéi', 'uéu', 'uói', 'uóu', 'üei', 'üeu']

def is_acute_char(c):
    return c in ACUTE_CHARS


def to_acute_char(c):
    if c in VOWEL_CHARS:
        return ACUTE_CHARS_MIRROR_DICT[c]
    else:
        return c


def to_non_acute_char(c):
    if c in ACUTE_CHARS:
        return ACUTE_CHARS_MIRROR_DICT[c]
    else:
        return c


def acute(s):
    return s.replace('a', AC_A).replace('e', AC_E).replace('o', AC_O).replace('i', AC_I).replace('u', AC_U)


def deacute(s):
    return s.replace(AC_A, 'a').replace(AC_E, 'e').replace(AC_O, 'o').replace(AC_I, 'i').replace(AC_U, 'u')


def is_conclst(s):
    cond = (s in BI_CONSONANT) | (s in CONSONANT)
    return cond


def is_vowclst(s, last=False):
    cond = (s in DIPTRONGO) | (s in TRIPTONGO) | (s in Y_DIPTRONGO) | (s in Y_TRIPTONGO) | (s in VOWEL) | (s in Y_LAST)
    if last == True:
        if s == 'y':
            return True
    return cond


def is_diptrongo(s):
    if s in DIPTRONGO:
        return True
    else:
        return False


def is_triptongo(s):
    if s in TRIPTONGO:
        return True
    else:
        return False


def is_biconstant(s):
    if s in BI_CONSONANT:
        return True
    else:
        return False


def de_engine(last_de_rslt, curr_regex, conds):
    rslt = []
    for i in range(0, last_de_rslt.__len__()):
        ele = last_de_rslt[i]
        cond = araq.de_cond_or_engine(ele, conds)
        if cond:
            rslt.append(ele)
        else:
            tmp = araq.regex_split(curr_regex, ele)
            rslt.extend(tmp)

    return rslt


def de_y(s):
    regex_y_trip = araq.creat_or_from_sarr(Y_TRIPTONGO)
    de_y_rslt = araq.regex_split(regex_y_trip, s)
    de_y_rslt = de_engine(de_y_rslt, regex_y_trip, Y_TRIPTONGO)
    regex_y_dip = araq.creat_or_from_sarr(Y_DIPTRONGO)
    de_y_rslt = de_engine(de_y_rslt, regex_y_dip, Y_DIPTRONGO)
    return de_y_rslt


def de_trip(de_y_rslt):
    regex_trip = araq.creat_or_from_sarr(TRIPTONGO)
    de_trip_rslt = de_engine(de_y_rslt, regex_trip, Y_DIPTRONGO + Y_TRIPTONGO)
    return de_trip_rslt


def de_dip(de_trip_rslt):
    regex_dip = araq.creat_or_from_sarr(DIPTRONGO)
    de_dip_rslt = de_engine(de_trip_rslt, regex_dip, Y_DIPTRONGO + Y_TRIPTONGO + TRIPTONGO)
    return de_dip_rslt


def de_bi(de_dip_rslt):
    regex_bi = araq.creat_or_from_sarr(BI_CONSONANT)
    de_bi_rslt = de_engine(de_dip_rslt, regex_bi, Y_DIPTRONGO + Y_TRIPTONGO + TRIPTONGO + DIPTRONGO)
    return de_bi_rslt


def de_c(de_bi_rslt):
    regex_c = araq.creat_or_from_sarr(CONSONANT)
    de_c_rslt = de_engine(de_bi_rslt, regex_c, Y_DIPTRONGO + Y_TRIPTONGO + TRIPTONGO + DIPTRONGO + BI_CONSONANT)
    return de_c_rslt


def de_v(de_c_rslt):
    regex_v = araq.creat_or_from_sarr(VOWEL)
    de_v_rslt = de_engine(de_c_rslt, regex_v, Y_DIPTRONGO + Y_TRIPTONGO + TRIPTONGO + DIPTRONGO + BI_CONSONANT + CONSONANT)
    return de_v_rslt


def word2clstarr(s):
    de_y_rslt = de_y(s)
    de_trip_rslt = de_trip(de_y_rslt)
    de_dip_rslt = de_dip(de_trip_rslt)
    de_be_rslt = de_bi(de_dip_rslt)
    de_c_rslt = de_c(de_be_rslt)
    de_v_rslt = de_v(de_c_rslt)
    return de_v_rslt


def arr_repl_lasty(arr):
    lasty = arr[(-1)] == 'y'
    if lasty:
        arr[-1] = Y_LAST[0]
    return arr


def arr_recvr_lasty(arr):
    arr[-1] = arr[(-1)].replace(Y_LAST[0], 'y')
    return arr


def vowel_in(pongo):
    chars = VOWEL
    for c in chars:
        if c in pongo:
            return True

    return False


def get_silabas(word):
    arr = word2clstarr(word)
    arr = arr_repl_lasty(arr)

    def push(tok, input_symbol, rslt):
        tok = tok + input_symbol
        return tok

    def pop(tok, input_symbol, rslt):
        tok = tok + input_symbol
        rslt.append(tok)
        tok = ''
        return tok

    def pop_push(tok, input_symbol, rslt):
        rslt.append(tok)
        tok = input_symbol
        return tok

    def pop1_push(tok, input_symbol, rslt):
        rslt.append(arr[(i - 2)])
        tok = arr[(i - 1)] + input_symbol
        return tok

    def pop2_push(tok, input_symbol, rslt):
        rslt.append(arr[(i - 3)] + arr[(i - 2)])
        tok = arr[(i - 1)] + input_symbol
        return tok

    def pop3_push(tok, input_symbol, rslt):
        rslt.append(arr[(i - 3)] + arr[(i - 2)] + arr[(i - 1)])
        tok = input_symbol
        return tok

    machine = symm.FSM()
    machine.add('INIT', is_conclst, push, 'C')
    machine.add('INIT', is_vowclst, push, 'V')
    machine.add('C', is_vowclst, push, 'CV')
    machine.add('C', is_conclst, pop, 'CC')
    machine.add('V', is_conclst, push, 'VC')
    machine.add('V', is_vowclst, pop_push, 'V')
    machine.add('CC', is_vowclst, push, 'CCV')
    machine.add('CCV', is_vowclst, pop3_push, 'V')
    machine.add('CCV', is_conclst, push, 'CCVC')
    machine.add('CCVC', is_vowclst, pop3_push, 'CV')
    machine.add('CCVC', is_conclst, pop_push, 'C')
    machine.add('CV', is_vowclst, pop_push, 'V')
    machine.add('CV', is_conclst, push, 'CVC')
    machine.add('VC', is_vowclst, pop1_push, 'CV')
    machine.add('VC', is_conclst, push, 'VCC')
    machine.add('VCC', is_conclst, pop3_push, 'C')
    machine.add('VCC', is_vowclst, pop2_push, 'CV')
    machine.add('CVC', is_vowclst, pop2_push, 'CV')
    machine.add('CVC', is_conclst, pop_push, 'C')
    rslt = []
    tok = ''
    curr_state = 'INIT'
    for i in range(0, arr.__len__()):
        input_symbol = arr[i]
        action, next_state, trigger_checker = machine.search(curr_state, input_symbol)
        if action:
            tok = action(tok, input_symbol, rslt)
        curr_state = next_state
        if tok == '':
            break

    if tok == '':
        pass
    else:
        cond1 = not vowel_in(tok)
        cond2 = 'y' not in tok.lower()
        if cond1:
            if cond2:
                rslt[-1] = rslt[(-1)] + tok
        else:
            rslt.append(tok)
    rslt = arr_recvr_lasty(rslt)
    return rslt


def get_spans(arr):
    rslt = []
    si = 0
    for i in range(0, arr.__len__()):
        w = arr[i]
        ei = si + w.__len__()
        span = (si, ei)
        rslt.append(span)
        si = ei

    return rslt


def get_spanloc(spans, charloc):
    for i in range(0, spans.__len__()):
        span = spans[i]
        if (charloc >= span[0]) & (charloc < span[1]):
            return i


def get_charloc(spans, spanloc, offset):
    return spans[spanloc] + offset


def word_repl_lasty(word):
    lasty = word[(-1)] == 'y'
    if lasty:
        word = word[:-1] + Y_LAST[0]


def word_recvr_lasty(word):
    return word.replace(Y_LAST[0], 'y')


def get_stress_char_pos_of_silaba(silaba):
    arr = word2clstarr(silaba)
    spans = get_spans(arr)
    ii = None
    for i in range(arr.__len__()):
        ele = arr[i]
        if ele in Y_TRIPTONGO:
            ii = 1
            oi = i
        elif ele in Y_DIPTRONGO:
            ii = 0
            oi = i
        elif ele in TRIPTONGO:
            ii = 1
            oi = i
        elif ele in DIPTRONGO:
            oi = i
            if ele[0] in ACUTE_STRONG_VOWEL + NORMAL_STRONG_VOWEL:
                ii = 0
            else:
                ii = 1
        elif ele in VOWEL:
            ii = 0
            oi = i
        else:
            if ele.lower() == 'y' and i == arr.__len__() - 1:
                ii = 0
                oi = i
                continue

    if ii != None:
        acute_pos = spans[oi][0] + ii
    else:
        acute_pos = None
    return acute_pos


def acute_vowel_in(pongo):
    chars = ACUTE_VOWEL
    for c in chars:
        if c in pongo:
            return True

    return False


def get_accent_pos(s):
    silabas = get_silabas(s)
    stress_chars = elel.mapv(silabas, get_stress_char_pos_of_silaba)
    lngth = silabas.__len__()
    cond1 = s[(-1)] in CONSONANT
    cond2 = s[(-1)] not in 'ns'
    if cond1 & cond2:
        accent_pos = lngth - 1
    else:
        accent_pos = lngth - 2
    for i in range(lngth):
        pongo = silabas[i]
        cond = acute_vowel_in(pongo)
        if cond:
            accent_pos = i
            continue

    return (
     accent_pos, silabas[accent_pos])


def get_stress(s):
    silabas = get_silabas(s)
    tmp = get_accent_pos(s)
    accent_pos = tmp[0]
    accent = tmp[1]
    stress_char_pos = get_stress_char_pos_of_silaba(accent)
    stress_char = accent[stress_char_pos]
    d = {'silabas':silabas, 
     'accent_pos':accent_pos, 
     'accent':accent, 
     'stress_char_pos':stress_char_pos, 
     'stress_char':stress_char}
    return d


def show_stress(s, stress_word_color='green', stress_char_color='yellow'):
    d = get_stress(s)
    stress_char_pos = d['stress_char_pos']
    accent = d['accent']
    silabas = d['silabas']
    accent_pos = d['accent_pos']
    siei_params = [0, stress_char_pos, stress_word_color, stress_char_pos, stress_char_pos + 1, stress_char_color, stress_char_pos + 1, len(accent), stress_word_color]
    color_accent = (spsp.sieipaint)(accent, *siei_params, **{'rtrn': 1})
    nsilabas = copy.deepcopy(silabas)
    nsilabas[accent_pos] = color_accent
    rslt = elel.join(nsilabas, '-')
    print(rslt)
    return rslt