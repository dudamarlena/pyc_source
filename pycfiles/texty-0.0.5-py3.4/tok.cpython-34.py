# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/texty/tok.py
# Compiled at: 2015-12-15 03:36:04
# Size of source mod 2**32: 1679 bytes
import re

def guess_syllables(token_str, estimate_risk=False):
    """ Uses hardcoded rules to guess syllables for English words, optionally
        indicates estimated risk of error. The rules are not perfect,
        but testing shows decent results. Postcorrection is advised.
    """
    token_str = token_str.lower()
    vow_cluster_re = re.compile('[aeiou]+')
    final_e_re = re.compile('[^aeiou]e+\\b')
    final_2cons_y_re = re.compile('([^aeiou]{2,}y\\b)|(\\b[^aeiou]+y\\b)')
    guess = 0
    risk = 0
    vowels = vow_cluster_re.findall(token_str)
    for vc in vowels:
        guess += 1
        if vc in ('ue', 'ei'):
            risk += 1
            continue

    if token_str.startswith('rei'):
        guess += 1
    final_2cons_y = final_2cons_y_re.search(token_str)
    if final_2cons_y:
        guess += 1
        risk += 1
    else:
        final_e = final_e_re.search(token_str)
    if final_e:
        if guess > 1:
            guess -= 1
    if estimate_risk:
        return (guess, risk)
    else:
        return guess