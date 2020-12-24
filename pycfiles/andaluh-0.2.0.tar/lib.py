# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/andaluh/lib.py
# Compiled at: 2019-02-20 03:09:38
import re
from exceptions import Exception
from andaluh.defs import *

def get_vowel_circumflex(vowel):
    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel) + 5
        return VOWELS_ALL_NOTILDE[i:i + 1][0]
    if vowel and vowel in VOWELS_ALL_TILDE:
        return vowel
    raise AndaluhError('Not a vowel', vowel)


def get_vowel_tilde(vowel):
    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel)
        return VOWELS_ALL_TILDE[i]
    if vowel and vowel in VOWELS_ALL_TILDE:
        return vowel
    raise AndaluhError('Not a vowel', vowel)


def keep_case(word, replacement_word):
    if word.islower():
        return replacement_word
    else:
        if word.isupper():
            return replacement_word.upper()
        if word.istitle():
            return replacement_word.title()
        return replacement_word


def h_rules(text):
    """Supress mute /h/"""

    def replace_with_case(match):
        word = match.group(0)
        if word.lower() in H_RULES_EXCEPT.keys():
            return keep_case(word, H_RULES_EXCEPT[word.lower()])
        else:

            def replace_with_case(match):
                h_char = match.group(1)
                next_char = match.group(2)
                if next_char and h_char.isupper():
                    return next_char.upper()
                else:
                    if next_char and h_char.islower():
                        return next_char.lower()
                    return ''

            return re.sub('(?<!c)(h)(\\w?)', replace_with_case, word, flags=re.IGNORECASE)

    text = re.sub('(?<!c)(h)(ua)', lambda match: 'g' + match.group(2) if match.group(1).islower() else 'G' + match.group(2), text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('(?<!c)(h)(u)(e)', lambda match: 'g' + keep_case(match.group(2), 'ü') + match.group(3) if match.group(1).islower() else 'G' + keep_case(match.group(2), 'ü') + match.group(3), text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('\\b(\\w*?)(h)(\\w*?)\\b', replace_with_case, text, flags=re.IGNORECASE)
    return text


def x_rules(text, vaf=VAF):
    """Replacement rules for /ks/ with EPA VAF"""

    def replace_with_case(match):
        x_char = match.group(1)
        if x_char.islower():
            return vaf
        else:
            return vaf.upper()

    def replace_intervowel_with_case(match):
        prev_char = match.group(1)
        x_char = match.group(2)
        next_char = match.group(3)
        prev_char = get_vowel_circumflex(prev_char)
        if x_char.isupper():
            return prev_char + vaf.upper() * 2 + next_char
        else:
            return prev_char + vaf * 2 + next_char

    if text[0] == 'X':
        text = vaf.upper() + text[1:]
    if text[0] == 'x':
        text = vaf + text[1:]
    text = re.sub('(a|e|i|o|u|á|é|í|ó|ú)(x)(a|e|i|o|u|á|é|í|ó|ú)', replace_intervowel_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('\\b(x)', replace_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def ch_rules(text):
    u"""Replacement rules for /∫/ (voiceless postalveolar fricative)"""
    text = re.sub('(c)(h)', lambda match: 'x' if match.group(1).islower() else 'X', text, flags=re.IGNORECASE)
    return text


def gj_rules(text, vvf=VVF):
    """Replacing /x/ (voiceless postalveolar fricative) with /h/"""

    def replace_h_with_case(match):
        word = match.group(0)
        if word.lower() in GJ_RULES_EXCEPT.keys():
            return keep_case(word, GJ_RULES_EXCEPT[word.lower()])
        else:
            word = re.sub('(g|j)(e|i|é|í)', lambda match: vvf + match.group(2) if match.group(1).islower() else vvf.upper() + match.group(2), word, flags=re.IGNORECASE | re.UNICODE)
            word = re.sub('(j)(a|o|u|á|ó|ú)', lambda match: vvf + match.group(2) if match.group(1).islower() else vvf.upper() + match.group(2), word, flags=re.IGNORECASE | re.UNICODE)
            return word

    def replace_g_with_case(match):
        s = match.group('s')
        a = match.group('a')
        b = match.group('b')
        ue = match.group('ue')
        const = match.group('const')
        return s + a + keep_case(b, 'g') + ue + const

    text = re.sub('\\b(\\w*?)(g|j)(e|i|é|í)(\\w*?)\\b', replace_h_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('\\b(\\w*?)(j)(a|o|u|á|ó|ú)(\\w*?)\\b', replace_h_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('(gu|gU)(e|i|é|í|E|I|É|Í)', 'g\\2', text)
    text = re.sub('(Gu|GU)(e|i|é|í|E|I|É|Í)', 'G\\2', text)
    text = re.sub('(g|G)(ü)(e|i|é|í|E|I|É|Í)', '\\1u\\3', text)
    text = re.sub('(g|G)(Ü)(e|i|é|í|E|I|É|Í)', '\\1U\\3', text)
    text = re.sub('(b)(uen)', lambda match: 'g' + match.group(2) if match.group(1).islower() else 'G' + match.group(2), text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('(?P<s>s?)(?P<a>a?)(?<!m)(?P<b>b)(?P<ue>ue)(?P<const>l|s)', replace_g_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def v_rules(text):
    """Replacing all /v/ (Voiced labiodental fricative) with /b/"""

    def replace_with_case(match):
        word = match.group(0)
        if word.lower() in V_RULES_EXCEPT.keys():
            return keep_case(word, V_RULES_EXCEPT[word.lower()])
        else:
            word = re.sub('nv', lambda match: keep_case(match.group(0), 'mb'), word, flags=re.IGNORECASE | re.UNICODE)
            word = re.sub('v', 'b', word)
            word = re.sub('V', 'B', word)
            return word

    text = re.sub('\\b(\\w*?)(v)(\\w*?)\\b', replace_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def ll_rules(text):
    u"""Replacing /ʎ/ (digraph ll) with Greek Y for /ʤ/ sound (voiced postalveolar affricate)"""

    def replace_with_case(match):
        word = match.group(0)
        if word.lower() in LL_RULES_EXCEPT.keys():
            return keep_case(word, LL_RULES_EXCEPT[word.lower()])
        else:
            return re.sub('(l)(l)', lambda match: 'Y' if match.group(1).isupper() else 'y', word, flags=re.IGNORECASE)

    text = re.sub('\\b(\\w*?)(l)(l)(\\w*?)\\b', replace_with_case, text, flags=re.IGNORECASE)
    return text


def l_rules(text):
    """Rotating /l/ with /r/"""
    text = re.sub('(l)(b|c|ç|Ç|g|s|d|f|g|h|k|m|p|q|r|t|x|z)', lambda match: 'r' + match.group(2) if match.group(1).islower() else 'R' + match.group(2), text, flags=re.IGNORECASE)
    return text


def psico_pseudo_rules(text):
    """Drops /p/ for pseudo- or psico- prefixes"""

    def replace_psicpseud_with_case(match):
        ps_syllable = match.group(1)
        if ps_syllable[0] == 'p':
            return ps_syllable[1:]
        else:
            return ps_syllable[1].upper() + ps_syllable[2:]

    text = re.sub('(psic|pseud)', replace_psicpseud_with_case, text, flags=re.IGNORECASE)
    return text


def vaf_rules(text, vaf=VAF):
    u"""Replacing Voiceless alveolar fricative (vaf) /s/ /θ/ with EPA's ç/Ç"""

    def replace_with_case(match):
        l_char = match.group(1)
        next_char = match.group(2)
        if l_char.islower():
            return vaf + next_char
        else:
            return vaf.upper() + next_char

    text = re.sub('(z|s)(a|e|i|o|u|á|é|í|ó|ú|â|ê|î|ô|û)', replace_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('(c)(e|i|é|í|ê|î)', replace_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def digraph_rules(text):
    """Replacement of consecutive consonant with EPA VAF"""

    def replace_lstrst_with_case(match):
        vowel_char = match.group(1)
        lr_char = match.group(2)
        t_char = match.group(4)
        if lr_char == 'l':
            lr_char == 'r'
        elif lr_char == 'L':
            lr_char == 'R'
        return vowel_char + lr_char + t_char * 2

    def replace_bdnr_s_with_case(match):
        vowel_char = match.group(1)
        cons_char = match.group(2)
        s_char = match.group(3)
        digraph_char = match.group(4)
        if cons_char.lower() + s_char.lower() == 'rs':
            return vowel_char + cons_char + digraph_char * 2
        else:
            return get_vowel_circumflex(vowel_char) + digraph_char * 2

    def replace_transpost_with_case(match):
        init_char = match.group(1)
        vowel_char = match.group(2)
        cons_char = match.group(4)
        if cons_char.lower() == 'l':
            return init_char + get_vowel_circumflex(vowel_char) + cons_char + '-' + cons_char
        else:
            return init_char + get_vowel_circumflex(vowel_char) + cons_char * 2

    def replace_l_with_case(match):
        vowel_char = match.group(1)
        digraph_char = match.group(3)
        return get_vowel_circumflex(vowel_char) + digraph_char + '-' + digraph_char

    def replace_digraph_with_case(match):
        vowel_char = match.group(1)
        to_drop_char, digraph_char = match.group(2)
        return get_vowel_circumflex(vowel_char) + digraph_char * 2

    text = re.sub('(a|e|i|o|u|á|é|í|ó|ú)(l|r)(s)(t)', replace_lstrst_with_case, text, flags=re.IGNORECASE)
    text = re.sub('(tr|p)(a|o)(ns|st)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)', replace_transpost_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('(a|e|i|o|u|á|é|í|ó|ú)(b|d|n|r)(s)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)', replace_bdnr_s_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('(a|e|i|o|u|á|é|í|ó|ú)(d|j|r|s|t|x|z)(l)', replace_l_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('(a|e|i|o|u|á|é|í|ó|ú)(' + ('|').join(DIGRAPHS) + ')', replace_digraph_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def word_ending_rules(text):

    def replace_d_end_with_case(match):
        unstressed_rules = {'a': 'â', 
           'A': 'Â', 'á': 'â', 'Á': 'Â', 'e': 'ê', 
           'E': 'Ê', 'é': 'ê', 'É': 'Ê', 'i': 'î', 
           'I': 'Î', 'í': 'î', 'Í': 'Î', 'o': 'ô', 
           'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô', 'u': 'û', 
           'U': 'Û', 'ú': 'û', 'Ú': 'Û'}
        stressed_rules = {'a': 'á', 
           'A': 'Á', 'á': 'á', 'Á': 'Á', 'e': 'é', 
           'E': 'É', 'é': 'é', 'É': 'É', 'i': 'î', 
           'I': 'Î', 'í': 'î', 'Í': 'Î', 'o': 'ô', 
           'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô', 'u': 'û', 
           'U': 'Û', 'ú': 'û', 'Ú': 'Û'}
        word = match.group(0)
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)
        if word.lower() in WORDEND_D_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_D_RULES_EXCEPT[word.lower()])
        else:
            if any(s in prefix for s in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó',
                                         'Ú')):
                return prefix + unstressed_rules[suffix_vowel]
            if suffix_vowel in ('a', 'e', 'A', 'E', 'á', 'é', 'Á', 'É'):
                return prefix + stressed_rules[suffix_vowel]
            if suffix_const.isupper():
                return prefix + stressed_rules[suffix_vowel] + 'H'
            return prefix + stressed_rules[suffix_vowel] + 'h'

    def replace_s_end_with_case(match):
        repl_rules = {'a': 'â', 
           'A': 'Â', 'á': 'â', 'Á': 'Â', 'e': 'ê', 
           'E': 'Ê', 'é': 'ê', 'É': 'Ê', 'i': 'î', 
           'I': 'Î', 'í': 'î', 'Í': 'Î', 'o': 'ô', 
           'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô', 'u': 'û', 
           'U': 'Û', 'ú': 'û', 'Ú': 'Û'}
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)
        word = prefix + suffix_vowel + suffix_const
        if word.lower() in WORDEND_S_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_S_RULES_EXCEPT[word.lower()])
        if suffix_vowel in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú'):
            if suffix_const.isupper():
                return prefix + repl_rules[suffix_vowel] + 'H'
            else:
                return prefix + repl_rules[suffix_vowel] + 'h'

        else:
            return prefix + repl_rules[suffix_vowel]

    def replace_const_end_with_case(match):
        repl_rules = {'a': 'â', 
           'A': 'Â', 'á': 'â', 'Á': 'Â', 'e': 'ê', 
           'E': 'Ê', 'é': 'ê', 'É': 'Ê', 'i': 'î', 
           'I': 'Î', 'í': 'î', 'Í': 'Î', 'o': 'ô', 
           'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô', 'u': 'û', 
           'U': 'Û', 'ú': 'û', 'Ú': 'Û'}
        word = match.group(0)
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)
        if word.lower() in WORDEND_CONST_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_CONST_RULES_EXCEPT[word.lower()])
        else:
            if any(s in prefix for s in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó',
                                         'Ú')):
                return prefix + repl_rules[suffix_vowel]
            if suffix_const.isupper():
                return prefix + repl_rules[suffix_vowel] + 'H'
            return prefix + repl_rules[suffix_vowel] + 'h'

    def replace_eps_end_with_case(match):
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)
        if any(s in prefix for s in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú')):
            if suffix_vowel.isupper():
                return prefix + 'Ê'
            else:
                return prefix + 'ê'

        else:
            return prefix + suffix_vowel + suffix_const

    def replace_intervowel_d_end_with_case(match):
        prefix = match.group(1)
        suffix_vowel_a = match.group(2)
        suffix_d_char = match.group(3)
        suffix_vowel_b = match.group(4)
        ending_s = match.group('s')
        suffix = suffix_vowel_a + suffix_d_char + suffix_vowel_b + ending_s
        word = prefix + suffix
        if word.lower() in WORDEND_D_INTERVOWEL_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_D_INTERVOWEL_RULES_EXCEPT[word.lower()])
        if not any(s in prefix for s in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó',
                                         'Ú')):
            if suffix.lower() == 'ada':
                if suffix_vowel_b.isupper():
                    return prefix + 'Á'
                else:
                    return prefix + 'á'

            if suffix.lower() == 'adas':
                return prefix + keep_case(suffix[:2], get_vowel_circumflex(suffix[0]) + 'h')
            if suffix.lower() == 'ado':
                return prefix + suffix_vowel_a + suffix_vowel_b
            if suffix.lower() in ('ados', 'idos', 'ídos'):
                return prefix + get_vowel_tilde(suffix_vowel_a) + get_vowel_circumflex(suffix_vowel_b)
            if suffix.lower() in ('ido', 'ído'):
                if suffix_vowel_a.isupper():
                    return prefix + 'Í' + suffix_vowel_b
                else:
                    return prefix + 'í' + suffix_vowel_b

            else:
                return word
        else:
            return word

    text = re.sub('\\b(\\w*?)(a|i|í|Í)(d)(o|a)(?P<s>s?)\\b', replace_intervowel_d_end_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('\\b(\\w+?)(e)(ps)\\b', replace_eps_end_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('\\b(\\w+?)(a|e|i|o|u|á|é|í|ó|ú)(d)\\b', replace_d_end_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('\\b(\\w+?)(a|e|i|o|u|á|é|í|ó|ú)(s)\\b', replace_s_end_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub('\\b(\\w+?)(a|e|i|o|u|á|é|í|ó|ú)(b|c|f|g|j|k|l|p|r|t|x|z)\\b', replace_const_end_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def exception_rules(text):
    """Set of exceptions to the replacement algorithm"""

    def replace_with_case(match):
        word = match.group(1)
        replacement_word = ENDING_RULES_EXCEPTION[word.lower()]
        return keep_case(word, replacement_word)

    text = re.sub('\\b(' + ('|').join(ENDING_RULES_EXCEPTION.keys()) + ')\\b', replace_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def word_interaction_rules(text):
    """Contractions and other word interaction rules"""

    def replace_with_case(match):
        prefix = match.group(1)
        l_char = match.group(2)
        whitespace_char = match.group(3)
        next_word_char = match.group(4)
        r_char = keep_case(l_char, 'r')
        return prefix + r_char + whitespace_char + next_word_char

    text = re.sub('\\b(\\w*?)(l)(\\s)(b|c|ç|d|f|g|h|j|k|l|m|n|ñ|p|q|s|t|v|w|x|y|z)', replace_with_case, text, flags=re.IGNORECASE | re.UNICODE)
    return text


def epa(text, vaf=VAF, vvf=VVF, debug=False):
    rules = [
     h_rules,
     x_rules,
     ch_rules,
     gj_rules,
     v_rules,
     ll_rules,
     l_rules,
     psico_pseudo_rules,
     vaf_rules,
     word_ending_rules,
     digraph_rules,
     exception_rules,
     word_interaction_rules]
    if type(text) != unicode:
        text = unicode(text, 'utf-8')
    if not text:
        return text
    for rule in rules:
        if rule in [x_rules, vaf_rules]:
            text = rule(text, vaf)
        elif rule == gj_rules:
            text = rule(text, vvf)
        else:
            text = rule(text)
        if debug:
            print rule.func_name + ' => ' + text

    return text


class AndaluhError(Exception):

    def __init__(self, message, errors):
        super(AndaluhError, self).__init__(message)
        self.errors = errors