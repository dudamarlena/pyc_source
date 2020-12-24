# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/dicts/en/syllabify.py
# Compiled at: 2016-09-29 14:06:27
English = {'consonants': [
                'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N',
                'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'], 
   'vowels': [
            'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW'], 
   'onsets': [
            'P', 'T', 'K', 'B', 'D', 'G', 'F', 'V', 'TH', 'DH', 'S', 'Z', 'SH', 'CH', 'JH', 'M',
            'N', 'R', 'L', 'HH', 'W', 'Y', 'P R', 'T R', 'K R', 'B R', 'D R', 'G R', 'F R',
            'TH R', 'SH R', 'P L', 'K L', 'B L', 'G L', 'F L', 'S L', 'T W', 'K W', 'D W',
            'S W', 'S P', 'S T', 'S K', 'S F', 'S M', 'S N', 'G W', 'SH W', 'S P R', 'S P L',
            'S T R', 'S K R', 'S K W', 'S K L', 'TH W', 'ZH', 'P Y', 'K Y', 'B Y', 'F Y',
            'HH Y', 'V Y', 'TH Y', 'M Y', 'S P Y', 'S K Y', 'G Y', 'HH W', '']}

def loadLanguage(filename):
    """This function loads up a language configuration file and returns
        the configuration to be passed to the syllabify function."""
    L = {'consonants': [], 'vowels': [], 'onsets': []}
    f = open(filename, 'r')
    section = None
    for line in f:
        line = line.strip()
        if line in ('[consonants]', '[vowels]', '[onsets]'):
            section = line[1:-1]
        elif section == None:
            raise ValueError, 'File must start with a section header such as [consonants].'
        elif section not in L:
            raise ValueError, 'Invalid section: ' + section
        else:
            L[section].append(line)

    for section in ('consonants', 'vowels', 'onsets'):
        if len(L[section]) == 0:
            raise ValueError, 'File does not contain any consonants, vowels, or onsets.'

    return L


def syllabify(language, word):
    """Syllabifies the word, given a language configuration loaded with loadLanguage.
           word is either a string of phonemes from the CMU pronouncing dictionary set
           (with optional stress numbers after vowels), or a Python list of phonemes,
           e.g. "B AE1 T" or ["B", "AE1", "T"]"""
    if type(word) == str:
        word = word.split()
    syllables = []
    internuclei = []
    for phoneme in word:
        phoneme = phoneme.strip()
        if phoneme == '':
            continue
        stress = None
        if phoneme[(-1)].isdigit():
            stress = int(phoneme[(-1)])
            phoneme = phoneme[0:-1]
        if phoneme in language['vowels']:
            coda = None
            onset = None
            if '.' in internuclei:
                period = internuclei.index('.')
                coda = internuclei[:period]
                onset = internuclei[period + 1:]
            else:
                for split in range(0, len(internuclei) + 1):
                    coda = internuclei[:split]
                    onset = internuclei[split:]
                    if (' ').join(onset) in language['onsets'] or len(syllables) == 0 or len(onset) == 0:
                        break

            if len(syllables) > 0:
                syllables[(-1)][3].extend(coda)
            syllables.append((stress, onset, [phoneme], []))
            internuclei = []
        elif phoneme not in language['consonants'] and phoneme != '.':
            raise ValueError, 'Invalid phoneme: ' + phoneme
        else:
            internuclei.append(phoneme)

    if len(internuclei) > 0:
        if len(syllables) == 0:
            syllables.append((None, internuclei, [], []))
        else:
            syllables[(-1)][3].extend(internuclei)
    return syllables


def stringify(syllables):
    """This function takes a syllabification returned by syllabify and
           turns it into a string, with phonemes spearated by spaces and
           syllables spearated by periods."""
    ret = []
    for syl in syllables:
        stress, onset, nucleus, coda = syl
        if stress != None and len(nucleus) != 0:
            nucleus[0] += str(stress)
        ret.append((' ').join(onset + nucleus + coda))

    return (' . ').join(ret)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print 'Usage: python syllabifier.py english.cfg < textfile.txt > outfile.txt'
    else:
        L = loadLanguage(sys.argv[1])
        for line in sys.stdin:
            if line[0] == '#':
                sys.stdout.write(line)
                continue
            line = line.strip()
            s = stringify(syllabify(L, line))
            sys.stdout.write(s + '\n')