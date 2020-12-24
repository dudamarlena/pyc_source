# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/nlp/tools/czech_stemmer.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 5894 bytes
""" Czech stemmer
Copyright © 2010 Luís Gomes <luismsgomes@gmail.com>.
This code is released under a Creative Commons Attribution 3.0 Unported License.
https://creativecommons.org/licenses/by/3.0/

Ported from the Java implementation available at:
    http://members.unine.ch/jacques.savoy/clef/index.html

"""
import re, sys

def cz_stem_all(words, aggressive=True):
    return [cz_stem(word, aggressive) for word in words]


def cz_stem(word, aggressive=False):
    if not re.match('^\\w+$', word):
        return word
    else:
        if not word.islower():
            if not word.istitle():
                if not word.isupper():
                    print(('warning: skipping word with mixed case: {}'.format(word)), file=(sys.stderr))
                    return word
            s = word.lower()
            s = _remove_case(s)
            s = _remove_possessives(s)
            if aggressive:
                s = _remove_comparative(s)
                s = _remove_diminutive(s)
                s = _remove_augmentative(s)
                s = _remove_derivational(s)
        else:
            if word.isupper():
                return s.upper()
            if word.istitle():
                return s.title()
        return s


def _remove_case(word):
    if len(word) > 7:
        if word.endswith('atech'):
            return word[:-5]
        else:
            if len(word) > 6:
                if word.endswith('ětem'):
                    return _palatalise(word[:-3])
                if word.endswith('atům'):
                    return word[:-4]
            if len(word) > 5:
                if word[-3:] in frozenset({'ích', 'ich', 'ěmi', 'ími', 'ího', 'iho', 'ého', 'ému', 'ech', 'ete', 'imu', 'emi', 'eti'}):
                    return _palatalise(word[:-2])
                if word[-3:] in frozenset({'ými', 'aty', 'ách', 'ých', 'ové', 'ami', 'ama', 'ata', 'ovi'}):
                    return word[:-3]
            if len(word) > 4:
                if word.endswith('em'):
                    return _palatalise(word[:-1])
                if word[-2:] in frozenset({'ém', 'ím', 'es'}):
                    return _palatalise(word[:-2])
                if word[-2:] in frozenset({'ům', 'os', 'at', 'ým', 'ou', 'us', 'mi', 'ám'}):
                    return word[:-2]
    else:
        if len(word) > 3:
            if word[(-1)] in 'eiíě':
                return _palatalise(word)
            if word[(-1)] in 'uyůaoáéý':
                return word[:-1]
    return word


def _remove_possessives(word):
    if len(word) > 5:
        if word[-2:] in frozenset({'ov', 'ův'}):
            return word[:-2]
        if word.endswith('in'):
            return _palatalise(word[:-1])
    return word


def _remove_comparative(word):
    if len(word) > 5:
        if word[-3:] in frozenset({'ejš', 'ějš'}):
            return _palatalise(word[:-2])
    return word


def _remove_diminutive(word):
    if len(word) > 7:
        if word.endswith('oušek'):
            return word[:-5]
        else:
            if len(word) > 6:
                if word[-4:] in frozenset({'iček', 'ínek', 'íček', 'inek', 'éček', 'eček', 'enek', 'ének'}):
                    return _palatalise(word[:-3])
                if word[-4:] in frozenset({'uček', 'áček', 'aček', 'oček', 'unek', 'anek', 'onek', 'ánek'}):
                    return _palatalise(word[:-4])
            if len(word) > 5:
                if word[-3:] in frozenset({'enk', 'íčk', 'éčk', 'ečk', 'ink', 'énk', 'ínk', 'ičk'}):
                    return _palatalise(word[:-3])
                if word[-3:] in frozenset({'ank', 'áčk', 'átk', 'očk', 'onk', 'ušk', 'ánk', 'unk', 'učk', 'ačk'}):
                    return word[:-3]
            if len(word) > 4:
                if word[-2:] in frozenset({'ík', 'ék', 'ik', 'ek'}):
                    return _palatalise(word[:-1])
                if word[-2:] in frozenset({'ák', 'ak', 'uk', 'ok'}):
                    return word[:-1]
    else:
        if len(word) > 3:
            if word[(-1)] == 'k':
                return word[:-1]
    return word


def _remove_augmentative(word):
    if len(word) > 6:
        if word.endswith('ajzn'):
            return word[:-4]
        if len(word) > 5:
            if word[-3:] in frozenset({'izn', 'isk'}):
                return _palatalise(word[:-2])
    else:
        if len(word) > 4:
            if word.endswith('ák'):
                return word[:-2]
    return word


def _remove_derivational(word):
    if len(word) > 8:
        if word.endswith('obinec'):
            return word[:-6]
        else:
            if len(word) > 7:
                if word.endswith('ionář'):
                    return _palatalise(word[:-4])
                else:
                    if word[-5:] in frozenset({'ovník', 'ovisk', 'ovstv', 'ovišt'}):
                        return word[:-5]
                    if len(word) > 6:
                        if word[-4:] in frozenset({'ovík', 'teln', 'ovtv', 'štin', 'ásek', 'loun', 'nost', 'ovec', 'ovin'}):
                            return word[:-4]
                        if word[-4:] in frozenset({'itel', 'inec', 'enic'}):
                            return _palatalise(word[:-3])
            else:
                if len(word) > 5:
                    if word.endswith('árn'):
                        return word[:-3]
                    if word[-3:] in frozenset({'išt', 'ián', 'itb', 'ěnk', 'ist', 'isk', 'írn'}):
                        return _palatalise(word[:-2])
                    if word[-3:] in frozenset({'ouš', 'stv', 'ost', 'ušk', 'kyn', 'oun', 'out', 'ník', 'ovn', 'ctv', 'och', 'kář', 'néř', 'čan'}):
                        return word[:-3]
            if len(word) > 4:
                if word[-2:] in frozenset({'ář', 'an', 'áč', 'án', 'ač', 'as'}):
                    return word[:-2]
                if word[-2:] in frozenset({'ín', 'ec', 'iv', 'íř', 'in', 'it', 'ěn', 'en', 'éř', 'ic'}):
                    return _palatalise(word[:-1])
                if word[-2:] in frozenset({'ov', 'ul', 'oň', 'yn', 'ot', 'dl', 'vk', 'tv', 'tk', 'nk', 'čn', 'čk', 'ob'}):
                    return word[:-2]
    else:
        if len(word) > 3:
            if word[(-1)] in 'cčklnt':
                return word[:-1]
    return word


def _palatalise(word):
    if word[-2:] in frozenset({'či', 'ci', 'ce', 'če'}):
        return word[:-2] + 'k'
    else:
        if word[-2:] in frozenset({'ži', 'zi', 'ze', 'že'}):
            return word[:-2] + 'h'
        else:
            if word[-3:] in frozenset({'čti', 'čtí', 'čtě'}):
                return word[:-3] + 'ck'
            if word[-3:] in frozenset({'šti', 'ští', 'ště'}):
                return word[:-3] + 'sk'
        return word[:-1]