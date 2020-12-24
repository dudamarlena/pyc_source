# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/lib/ipa.py
# Compiled at: 2019-06-07 00:03:27
ipakey = [
 'approx', 'cons', 'son', 'syll', 'constr', 'spread', 'voice', 'long', 'cont_acoust', 'cont_artic', 'delrel', 'lat', 'nas', 'strid', 'tap', 'trill', 'coronal', 'dorsal', 'labial', 'labiodental', 'ant', 'dist', 'back', 'front', 'high', 'low', 'tense', 'round']
ipa = {}
ipa['p'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
ipa['m'] = [False, True, True, False, False, False, True, None, True, False, False, False, True, False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
ipa['pʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
ipa['t'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['b'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
ipa['d'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['k'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
ipa['d̪'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['t̪'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['n'] = [False, True, True, False, False, False, True, None, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ɳ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True, False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['ɲ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True, False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
ipa['g'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
ipa['f'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
ipa['v'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
ipa['ʃ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
ipa['s'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['z'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ʒ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
ipa['j'] = [True, False, True, False, False, False, True, None, True, True, False, False, False, False, False, False, True, True, False, False, False, False, False, None, True, False, None, False]
ipa['ɦ'] = [False, True, False, False, False, True, True, None, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, None, False, False, None, False]
ipa['h'] = [False, True, False, False, False, True, False, None, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, None, False, False, None, False]
ipa['q'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
ipa['ɸ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
ipa['ʀ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, True, False, True, False, False, False, False, True, None, False, False, None, False]
ipa['ʁ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
ipa['ɣ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
ipa['ɬ'] = [False, True, False, False, False, False, False, None, True, True, False, True, False, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ɮ'] = [False, True, False, False, False, False, True, None, True, True, False, True, False, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['x'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
ipa['ʤ'] = [False, True, False, False, False, False, True, None, False, False, True, False, False, True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
ipa['ʧ'] = [False, True, False, False, False, False, False, None, False, False, True, False, False, True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
ipa['ð'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['θ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['β'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
ipa['ç'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
ipa['ʂ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, True, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['ʐ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, True, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['l'] = [True, True, True, False, False, False, True, None, True, True, False, True, False, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['r'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, True, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ɾ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, True, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ɥ'] = [True, False, True, False, False, False, True, None, True, True, False, False, False, False, False, False, True, True, True, False, False, False, False, None, True, False, None, True]
ipa['ʔ'] = [False, True, False, False, True, False, False, None, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, None, False, False, None, False]
ipa['ŋ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True, False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
ipa['ɻ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ħ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, False, False, False, False, True, False, False, False, False, True, None, False, True, None, False]
ipa['χ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
ipa['n̪'] = [False, True, True, False, False, False, True, None, True, False, False, False, True, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['kʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
ipa['tʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ʈ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['ʈʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['ɖ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['ɖʰ'] = [False, True, False, False, False, True, True, None, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['ʝ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False, False, False, False, False, True, False, False, False, True, False, None, True, False, None, False]
ipa['kʷ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, False, True, True, False, False, False, True, None, True, False, None, True]
ipa['gʷ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, False, True, True, False, False, False, True, None, True, False, None, True]
ipa['ɢ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
ipa['kʲ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, None, True, False, None, False]
ipa['gʲ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, None, True, False, None, False]
ipa['ɱ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True, False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
ipa['ʋ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
ipa['c'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
ipa['ʝ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
ipa['n̥'] = [False, True, True, False, False, False, False, None, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['m̥'] = [False, True, True, False, False, False, False, None, True, False, False, False, True, False, False, False, True, False, True, False, False, False, False, None, False, False, None, False]
ipa['pʷ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, None, False, False, None, True]
ipa['bʷ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False, False, False, False, False, False, True, False, True, False, False, None, False, False, None, True]
ipa['ɬ̪'] = [False, True, False, False, False, False, False, None, True, True, False, True, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['ɮ̪'] = [False, True, False, False, False, False, True, None, True, True, False, True, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['r̪'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, True, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['ɾ̪'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, True, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['ɹ̪'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['w̃'] = [True, True, True, False, False, False, True, None, True, True, False, False, True, False, False, False, False, True, True, False, True, False, True, None, True, False, None, True]
ipa['cʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False, False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
ipa['t̪ʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['s̪'] = [False, True, False, False, False, False, False, None, True, True, False, False, False, True, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['l̪'] = [True, True, True, False, False, False, True, None, True, True, False, True, False, False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
ipa['ʟ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, False, False, True, False, False, False, False, False, None, True, True, None, False]
ipa['ɭ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['ʎ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
ipa['ʦ'] = [False, True, False, False, False, False, False, None, False, False, True, False, False, True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ʣ'] = [False, True, False, False, False, False, True, None, False, False, True, False, False, True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
ipa['ɽ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False, True, False, True, False, False, False, False, False, False, None, False, False, None, False]
ipa['o'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, False, True, True]
ipa['ɔ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, False, False, True]
ipa['ɐ'] = [None, False, True, False, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, False, True, True, False]
ipa['w'] = [None, False, True, False, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, False, False, False, False]
ipa['ɤ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, False, True, False]
ipa['ɨ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, True, False, True, False]
ipa['ə'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, False, False, False, False]
ipa['i'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, True, False]
ipa['iː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, True, False]
ipa['y'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, True, True]
ipa['yː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, True, True]
ipa['ɪ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, False, False]
ipa['ɪː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, False, False]
ipa['ʏ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, False, True]
ipa['ʏː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, False, True]
ipa['e'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, True, False]
ipa['eː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, True, False]
ipa['ø'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, True, True]
ipa['øː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, True, True]
ipa['ɛ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, False, False]
ipa['ɛː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, False, False]
ipa['œ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, False, True]
ipa['œː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, False, True]
ipa['æ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, True, True, False]
ipa['æː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, True, True, False]
ipa['ɶ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, True, False, True]
ipa['ʉ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, True, False, True, True]
ipa['ʉː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, True, False, True, True]
ipa['a'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, False, True, False, False]
ipa['aː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, False, True, False, False]
ipa['ɯ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, True, False, True, False]
ipa['ɯː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, True, False, True, False]
ipa['u'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, True, False, True, True]
ipa['uː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, True, False, True, True]
ipa['ʊ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, True, False, False, True]
ipa['ʊː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, True, False, False, True]
ipa['oː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, False, True, True]
ipa['ʌ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, False, False, False]
ipa['ʌː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, False, False, False]
ipa['ɔː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, False, False, True]
ipa['ɑ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
ipa['ɑː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
ipa['ɒ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, True, False, True]
ipa['ɒː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False, None, None, None, None, None, None, None, None, None, True, False, False, True, False, True]
ipa['œ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, False, False, False, True]
ipa['ɵ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, False, False, False, False, True]
ipa['ʉ̞'] = [None, False, True, True, None, None, None, False, None, None, None, None, False, None, None, None, None, None, None, None, None, None, False, True, True, False, True, True]
ipa['ẽ'] = [None, False, True, True, None, None, None, True, None, None, None, None, True, None, None, None, None, None, None, None, None, None, False, True, False, False, True, False]
ipa['ɛ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, True, None, None, None, None, None, None, None, None, None, False, True, False, False, False, False]
ipa['ɔ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, True, None, None, None, None, None, None, None, None, None, True, False, False, False, False, True]
ipa['ɑ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, True, None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
ipa['ɑ̃ː'] = [None, False, True, True, None, None, None, False, None, None, None, None, True, None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
ipa['ã'] = [None, False, True, True, None, None, None, False, None, None, None, None, True, None, None, None, None, None, None, None, None, None, False, False, False, True, False, None]
ipa2cmu = {}
ipa2cmu['ɑ'] = 'AA'
ipa2cmu['æ'] = 'AE'
ipa2cmu['ə'] = 'AH'
ipa2cmu['ʌ'] = 'AH'
ipa2cmu['ɔː'] = 'AO'
ipa2cmu['aʊ'] = 'AW'
ipa2cmu['aɪ'] = 'AY'
ipa2cmu['ʧ'] = 'CH'
ipa2cmu['ð'] = 'DH'
ipa2cmu['ɛ'] = 'EH'
ipa2cmu['ɛː'] = 'ER'
ipa2cmu['eɪ'] = 'EY'
ipa2cmu['h'] = 'HH'
ipa2cmu['ɪ'] = 'IH'
ipa2cmu['iː'] = 'IY'
ipa2cmu['ŋ'] = 'NG'
ipa2cmu['oʊ'] = 'OW'
ipa2cmu['ɔɪ'] = 'OY'
ipa2cmu['ʃ'] = 'SH'
ipa2cmu['θ'] = 'TH'
ipa2cmu['ʊ'] = 'UH'
ipa2cmu['uː'] = 'UW'
ipa2cmu['ʒ'] = 'ZH'
ipa2cmu['b'] = 'B'
ipa2cmu['d'] = 'D'
ipa2cmu['f'] = 'F'
ipa2cmu['g'] = 'G'
ipa2cmu['ʤ'] = 'JH'
ipa2cmu['k'] = 'K'
ipa2cmu['l'] = 'L'
ipa2cmu['m'] = 'M'
ipa2cmu['n'] = 'N'
ipa2cmu['p'] = 'P'
ipa2cmu['r'] = 'R'
ipa2cmu['s'] = 'S'
ipa2cmu['t'] = 'T'
ipa2cmu['v'] = 'V'
ipa2cmu['w'] = 'W'
ipa2cmu['j'] = 'Y'
ipa2cmu['z'] = 'Z'
d_sampa2ipa = {}
sampa_table = 'i\ti\nI\tI\ne\te\nE\tɛ\n{\tæ\ny\ty\n2\tø\n9\tœ\n1\tɨ\n@\tə\n6\tɐ\n3\tɜ\na\ta\n}\tʉ\n8\tɵ\n&\tɶ\nM\tɯ\n7\tɤ\nV\tʌ\nA\tɑ\nu\tu\nU\tʊ \no\to\nO\tɔ \nQ\tɒ\np\tp\nb\tb\nt\tt\nd\td\ntS\tʧ\ndZ\tʤ\nc\tc\nJ\\\tɟ\nk\tk\ng\tg\nq\tq\np\\\tφ\nB\tβ \nf\tf\nv\tv\nT\tθ \nD\tð \ns\ts\nz\tz\nS\tʃ\nZ\tʒ\nC\tç\nj\\\tʝ\njj\tʝ\nx\tx\nG\tγ\nM\\\tɰ\nh\th\nh\\\tɦ\nm\tm\nF\tɱ\nn\tn\nJ\tɲ\nN\tŋ\nl\tl\nL\tʎ\n5\tɫ\n4\tɾ\nr\tɽ\nr\\`\tɻ\nR\tʀ\nw\tw\nH\tɥ \nj\tj\naI\taɪ\nAI\taɪ\naU\taʊ\nEI\tɛɪ\nOY\tɔɪ\nUI\tʊɪ \nts\tʦ\nY\tʏ\npf\tpʰ\nr=\tɽ'
for ln in sampa_table.split('\n'):
    sampa, ipa_str = ln.split('\t')
    d_sampa2ipa[sampa.strip()] = ipa_str.strip()

d_ipa2sampa = {}
for sm, ip in list(d_sampa2ipa.items()):
    d_ipa2sampa[ip] = sm

formantd = {}
x = 'i\t240\t2400\ny\t235\t2100\ne\t390\t2300\nø\t370\t1900\nɛ\t610\t1900\nœ\t585\t1710\na\t850\t1610\nɶ\t820\t1530\nɑ\t750\t940\nɒ\t700\t760\nʌ\t600\t1170\nɔ\t500\t700\nɤ\t460\t1310\no\t360\t640\nɯ\t300\t1390\nu\t250\t595'
f1s = []
f2s = []
for ln in x.split('\n'):
    _ipa, f1, f2 = ln.strip().split()
    f1s += [int(f1)]
    f2s += [int(f2)]
    formantd[_ipa] = [int(f1), int(f2)]

maxf1, minf1 = max(f1s), min(f1s)
maxf2, minf2 = max(f2s), min(f2s)
f1_range = maxf1 - minf1
f2_range = maxf2 - minf2
for _ipa in formantd:
    formantd[_ipa][0] = (formantd[_ipa][0] - minf1) / float(f1_range)
    formantd[_ipa][1] = (formantd[_ipa][1] - minf2) / float(f2_range)

ipa2featd = {}
for ph, vals in list(ipa.items()):
    ipa2featd[ph] = dict(list(zip(ipakey, vals)))

def sampa2ipa(sampa):
    import lexconvert
    if sampa == 'r=':
        return 'ɛː'
    else:
        return lexconvert.convert(sampa, 'x-sampa', 'unicode-ipa')
        sampa = sampa.replace('?', '')
        if not sampa:
            return sampa
        if ':' in sampa:
            colon = 'ː'
            sampa = sampa.replace(':', '')
        else:
            colon = ''
        if sampa not in d_sampa2ipa and len(sampa) == 2:
            return sampa2ipa(sampa[0]) + sampa2ipa(sampa[1])
        return d_sampa2ipa[sampa] + colon