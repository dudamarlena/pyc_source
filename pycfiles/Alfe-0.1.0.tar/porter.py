# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/lang/porter.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\nReimplementation of the\n`Porter stemming algorithm <http://tartarus.org/~martin/PorterStemmer/>`_\nin Python.\n\nIn my quick tests, this implementation about 3.5 times faster than the\nseriously weird Python linked from the official page.\n'
import re
_step2list = {'ational': 'ate', 
   'tional': 'tion', 
   'enci': 'ence', 
   'anci': 'ance', 
   'izer': 'ize', 
   'bli': 'ble', 
   'alli': 'al', 
   'entli': 'ent', 
   'eli': 'e', 
   'ousli': 'ous', 
   'ization': 'ize', 
   'ation': 'ate', 
   'ator': 'ate', 
   'alism': 'al', 
   'iveness': 'ive', 
   'fulness': 'ful', 
   'ousness': 'ous', 
   'aliti': 'al', 
   'iviti': 'ive', 
   'biliti': 'ble', 
   'logi': 'log'}
_step3list = {'icate': 'ic', 
   'ative': '', 
   'alize': 'al', 
   'iciti': 'ic', 
   'ical': 'ic', 
   'ful': '', 
   'ness': ''}
_cons = '[^aeiou]'
_vowel = '[aeiouy]'
_cons_seq = '[^aeiouy]+'
_vowel_seq = '[aeiou]+'
_mgr0 = re.compile('^(' + _cons_seq + ')?' + _vowel_seq + _cons_seq)
_meq1 = re.compile('^(' + _cons_seq + ')?' + _vowel_seq + _cons_seq + '(' + _vowel_seq + ')?$')
_mgr1 = re.compile('^(' + _cons_seq + ')?' + _vowel_seq + _cons_seq + _vowel_seq + _cons_seq)
_s_v = re.compile('^(' + _cons_seq + ')?' + _vowel)
_c_v = re.compile('^' + _cons_seq + _vowel + '[^aeiouwxy]$')
_ed_ing = re.compile('^(.*)(ed|ing)$')
_at_bl_iz = re.compile('(at|bl|iz)$')
_step1b = re.compile('([^aeiouylsz])\\1$')
_step2 = re.compile('^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi)$')
_step3 = re.compile('^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$')
_step4_1 = re.compile('^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$')
_step4_2 = re.compile('^(.+?)(s|t)(ion)$')
_step5 = re.compile('^(.+?)e$')

def stem(w):
    """Uses the Porter stemming algorithm to remove suffixes from English
    words.
    
    >>> stem("fundamentally")
    "fundament"
    """
    if len(w) < 3:
        return w
    first_is_y = w[0] == 'y'
    if first_is_y:
        w = 'Y' + w[1:]
    if w.endswith('s'):
        if w.endswith('sses'):
            w = w[:-2]
        elif w.endswith('ies'):
            w = w[:-2]
        elif w[(-2)] != 's':
            w = w[:-1]
    if w.endswith('eed'):
        s = w[:-3]
        if _mgr0.match(s):
            w = w[:-1]
    else:
        m = _ed_ing.match(w)
        if m:
            stem = m.group(1)
            if _s_v.match(stem):
                w = stem
                if _at_bl_iz.match(w):
                    w += 'e'
                elif _step1b.match(w):
                    w = w[:-1]
                elif _c_v.match(w):
                    w += 'e'
    if w.endswith('y'):
        stem = w[:-1]
        if _s_v.match(stem):
            w = stem + 'i'
    m = _step2.match(w)
    if m:
        stem = m.group(1)
        suffix = m.group(2)
        if _mgr0.match(stem):
            w = stem + _step2list[suffix]
    m = _step3.match(w)
    if m:
        stem = m.group(1)
        suffix = m.group(2)
        if _mgr0.match(stem):
            w = stem + _step3list[suffix]
    m = _step4_1.match(w)
    if m:
        stem = m.group(1)
        if _mgr1.match(stem):
            w = stem
    else:
        m = _step4_2.match(w)
        if m:
            stem = m.group(1) + m.group(2)
            if _mgr1.match(stem):
                w = stem
    m = _step5.match(w)
    if m:
        stem = m.group(1)
        if _mgr1.match(stem) or _meq1.match(stem) and not _c_v.match(stem):
            w = stem
    if w.endswith('ll') and _mgr1.match(w):
        w = w[:-1]
    if first_is_y:
        w = 'y' + w[1:]
    return w


if __name__ == '__main__':
    print stem('fundamentally')