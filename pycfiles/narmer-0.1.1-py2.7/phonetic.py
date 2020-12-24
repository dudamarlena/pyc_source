# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/narmer/phonetic.py
# Compiled at: 2015-05-12 23:59:21
"""narmer.phonetic

The phonetic module implements phonetic algorithms including:
    german_ipa
    Metaphone3

Copyright 2015 by Christopher C. Little.
This file is part of Narmer.

Narmer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Narmer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Narmer. If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals
from __future__ import division
from abydos._compat import _unicode, _range
import unicodedata, sys
try:
    from metaphone3.metaphone3 import Metaphone3
except ImportError:
    pass

def german_ipa(word):
    """Return the IPA transcription of a German word

    Arguments:
    word -- the German word to transcribe to IPA

    Description:
    This is based largely on the orthographic mapping described at:
    https://en.wikipedia.org/wiki/German_orthography

    No significant attempt is made to accomodate loanwords.
    """
    _vowels = tuple(b'AEIOUYÄÖÜ')
    word = unicodedata.normalize(b'NFKC', _unicode(word.upper()))
    word = word.replace(b'ß', b'SS')
    ipa = b''
    last = len(word) - 1
    skip = 0
    for i in _range(len(word)):
        if skip:
            skip -= 1
            continue
        if word[i] in b'BFJKLMR':
            ipa += word[i].lower()
        elif word[i] == b'C':
            if word[i:i + 2] == b'CH':
                if word[i:i + 3] == b'CHS':
                    ipa += b'ks'
                    skip = 2
                elif word[i:i + 4] == b'CHEN':
                    ipa += b'ç'
                    skip = 1
                elif i - 1 >= 0 and word[(i - 1)] in tuple(b'AOU'):
                    ipa += b'x'
                    skip = 1
                else:
                    ipa += b'ç'
                    skip = 1
            elif word[i:i + 2] == b'CK':
                ipa += b'k'
                skip = 1
            elif i != last and word[(i + 1)] in tuple(b'ÄEI'):
                ipa += b'ts'
            else:
                ipa += b'k'
        elif word[i] == b'D':
            if word[i:i + 4] == b'DSCH':
                ipa += b'dʒ'
                skip = 3
            elif word[i:i + 2] == b'DT':
                ipa += b't'
                skip = 1
            else:
                ipa += b'd'
        elif word[i] == b'G':
            if i - 1 >= 0 and word[(i - 1)] == b'I':
                ipa += b'ç'
            else:
                ipa += b'g'
        elif word[i] == b'H':
            ipa += b'h'
        elif word[i] == b'N':
            if word[i:i + 2] == b'NG':
                ipa += b'ŋ'
                skip = 1
            elif word[i:i + 2] == b'NK':
                ipa += b'ŋk'
                skip = 1
            else:
                ipa += b'n'
        elif word[i] == b'P':
            if word[i:i + 2] == b'PH':
                ipa += b'f'
                skip = 1
            else:
                ipa += b'p'
        elif word[i] == b'Q':
            if word[i:i + 2] == b'QU' and i + 1 != last and word[(i + 2)] in _vowels:
                ipa += b'kv'
                skip = 1
            else:
                ipa += b'k'
        elif word[i] == b'S':
            if word[i:i + 2] == b'SS':
                ipa += b's'
                skip = 1
            elif word[i:i + 3] == b'SCH':
                ipa += b'ʃ'
                skip = 2
            elif i == 0 and i != last and word[(i + 1)] in tuple(b'PT'):
                ipa += b'ʃ'
            elif i != last and word[(i + 1)] in _vowels:
                ipa += b'z'
            else:
                ipa += b's'
        elif word[i] == b'T':
            if word[i:i + 4] == b'TSCH':
                ipa += b'tʃ'
                skip = 3
            elif word[i:i + 5] == b'TZSCH':
                ipa += b'tʃ'
                skip = 4
            elif word[i:i + 4] == b'TION' or word[i:i + 4] == b'TIÄR' or word[i:i + 4] == b'TIAL' or word[i:i + 5] == b'TIELL':
                ipa += b'tsi'
                skip = 1
            elif word[i:i + 2] == b'TZ':
                ipa += b'ts'
                skip = 1
            elif word[i:i + 2] == b'TH':
                ipa += b't'
                skip = 1
            else:
                ipa += b't'
        elif word[i] == b'V':
            ipa += b'f'
        elif word[i] == b'W':
            ipa += b'v'
        elif word[i] == b'X':
            ipa += b'ks'
        elif word[i] == b'Z':
            if word[i:i + 4] == b'ZSCH':
                ipa += b'tʃ'
                skip = 3
            else:
                ipa += b'ts'
        elif word[i:i + 2] in tuple(('EI', 'AI', 'EY', 'AY')):
            ipa += b'ai'
            skip = 1
        elif word[i:i + 2] in tuple(('EU', 'ÄU')):
            ipa += b'oy'
            skip = 1
        elif word[i:i + 2] == b'AU':
            ipa += b'au'
            skip = 1
        elif word[i] == b'A':
            if word[i:i + 2] in tuple(('AA', 'AH')):
                skip = 1
            ipa += b'a'
        elif word[i] == b'E':
            if word[i:i + 2] in tuple(('EE', 'EH')):
                skip = 1
            ipa += b'e'
        elif word[i] == b'I':
            if word[i:i + 2] in tuple(('IE', 'IH')):
                skip = 1
            if word[i:i + 3] == b'IEH':
                skip = 2
            ipa += b'i'
        elif word[i] == b'O':
            if word[i:i + 2] in tuple(('OO', 'OH')):
                skip = 1
            ipa += b'o'
        elif word[i] == b'U':
            if word[i:i + 2] == b'UH':
                skip = 1
            ipa += b'u'
        elif word[i] == b'Y':
            ipa += b'y'
        elif word[i] == b'Ä':
            if word[i:i + 2] == b'ÄH':
                skip = 1
            ipa += b'e'
        elif word[i] == b'Ö':
            if word[i:i + 2] == b'ÖH':
                skip = 1
            ipa += b'ø'
        elif word[i] == b'Ü':
            if word[i:i + 2] == b'ÜH':
                skip = 1
            ipa += b'y'

    return ipa


def metaphone3(word, maxlength=float(b'inf'), vowels=False, exact=False):
    """Return the Metaphone3 encodings of a word as a tuple

    Arguments:
    word -- the word to apply the Metaphone3 algorithm to
    maxlength -- the maximum length of the returned Metaphone3 codes
        (defaults to unlimited though it is 8 by default in Metaphone3)
    vowels -- boolean indicating whether vowels are included in the encoding
    exact -- boolean indicating whether to use the exact vs. approximate
        encodings

    Description:
    This requires a metaphone3 Python library, without which this returns
    None. The inclusion of this is for convenience to keep a consistent
    API for the full set of phonetic algorithms.
    """
    if b'metaphone3.metaphone3' not in sys.modules:
        return None
    else:
        met3 = Metaphone3()
        met3.set_encode_vowels(vowels)
        met3.set_encode_exact(exact)
        met3.set_key_length(maxlength)
        met3.set_word(word)
        met3.encode()
        return (met3.get_metaph(), met3.get_alternate_metaph())