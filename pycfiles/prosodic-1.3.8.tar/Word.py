# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/lib/Word.py
# Compiled at: 2019-06-07 00:03:27
from entity import entity, being
from tools import *
import Meter

class Word(entity):

    def __init__(self, token, syllables=None, sylls_text=[], broken=False, lang=None):
        if syllables == None:
            import prosodic
            if lang == None:
                lang = prosodic.lang
            w = prosodic.dict[lang].get(token)[0]
            self.broken = len(w.__dict__) or True
        else:
            for k, v in list(w.__dict__.items()):
                setattr(self, k, v)

            return
        self.token = token.lower()
        self.punct = ''
        self.sylls_text = sylls_text
        self.finished = False
        self.children = syllables
        self.numSyll = len(syllables)
        self.broken = broken
        self.featpaths = {}
        self.stress = '?'
        self.lang = '?'
        self.feats = {}
        if '/' in self.token:
            tt = self.token.split('/')
            self.token = tt[0]
            self.pos = tt[1]
        self.token, self.punct = gleanPunc(self.token)
        self.setSyllText()
        self.feat('numSyll', self.numSyll)
        if not len(syllables) or self.token == '':
            self.broken = True
            self.token = '?' + self.token
        else:
            len_sylls = len(self.children)
            len_sylls_text = len(self.sylls_text)
            if len_sylls != len_sylls_text:
                self.om('<error> numSyll mismatch: [ipa] ' + self.u2s(('.').join([ child.str_ipa() for child in self.children ])) + ' vs [orth] ' + str(('.').join([ self.u2s(x) for x in self.sylls_text ])))
                length = min([len_sylls, len_sylls_text])
            else:
                length = len_sylls
            for i in range(length):
                self.children[i].settok(self.sylls_text[i])

        return

    def __repr__(self):
        return '<' + self.classname() + '.' + self.u2s(self.token) + '> [' + self.__str__stressedSylls() + ']'

    def __str__(self):
        tok = self.token if type(self.token) == str else self.token.encode('utf-8')
        return tok + str('\t<') + str(self.__str__stressedSylls()) + str('>')

    def __str__weight(self):
        if not hasattr(self, 'weight'):
            self.weight = ('').join([ entity.weight_bool2str[syll.children[0].feature('prom.weight')] for syll in self.children ])
        return self.weight

    def __str__stressedSylls(self):
        lang = self.lang
        import prosodic
        if 'output_' + lang not in prosodic.config:
            lang = '**'
        if prosodic.config.get('output_' + lang, '') == 'cmu':
            return (' . ').join([ str(syll) for syll in self.children ])
        return ('.').join([ str(syll) for syll in self.children ])

    def output_minform(self):
        return str(makeminlength(self.u2s(self.token), 20)) + '\t' + str(makeminlength('P:' + self.__str__stressedSylls(), 35)) + '\tS:' + str(self.stress) + '\tW:' + str(self.__str__weight())

    def CorV(self):
        o = ''
        for phoneme in self.phonemes():
            o += phoneme.CorV()

        return o

    def setSyllText(self):
        if not self.sylls_text and len(self.children):
            self.setSyllText_byphonemes()

    def addSuffix(self, phon):
        self.children[(len(self.children) - 1)].addSuffix(phon)

    def lastsyll(self):
        return self.children[(len(self.children) - 1)]

    def setSyllText_byphonemes(self):
        return self.setSyllText_byletters(self.CorV())
        corv = self.CorV()
        corvi = 0
        self.sylls_text = []
        for syll in self.children:
            syllshape = syll.feature('shape')
            if not syllshape:
                continue
            sylltail = syllshape[(-1)]
            vowi = corv.find('V', corvi)
            if len(corv) - 1 == vowi:
                self.sylls_text.append(corv[corvi:vowi])
            elif sylltail == 'V':
                if corv[(vowi + 1)] == 'V':
                    self.sylls_text.append(corv[corvi:vowi + 1])
                    corvi = vowi + 1 + 1
                else:
                    self.sylls_text.append(corv[corvi:vowi])
                    corvi = vowi + 1
            elif sylltail == 'C':
                self.sylls_text.append(corv[corvi:vowi + 1])
                corvi = vowi + 1 + 1

    def setSyllText_byletters(self, lengthby=None):
        i = 0
        textSyll = []
        self.sylls_text = []
        numSyll = len(self.children)
        numLetters = len(self.token)
        if not numLetters:
            for x in self.stress:
                self.sylls_text.append('?')

            return
        while i < numSyll:
            textSyll.append('')
            i += 1

        word = self.token
        if not lengthby:
            inc = numLetters / numSyll
        else:
            inc = len(lengthby) / numSyll
        if not inc:
            inc = 1
        curSyll = 0
        unit = ''
        curLetter = 1
        for letter in word:
            textSyll[curSyll] += letter
            if curLetter % inc == 0:
                if curSyll + 1 < numSyll:
                    curSyll += 1
            curLetter += 1

        self.sylls_text = textSyll
        return

    def addPunct(self, punct):
        self.punct = punct

    @property
    def weight(self):
        return ('').join([ entity.weight_bool2str[syll.children[0].feature('prom.weight')] for syll in self.children ])

    def getToken(self, punct=True):
        if punct and self.punct != None:
            return self.u2s(self.token) + self.u2s(self.punct)
        else:
            return self.u2s(self.token)
            return

    def getPOS(self):
        return self.pos

    def getStress(self):
        return self.stress

    def getWeight(self):
        return self.weight

    def getFeet(self):
        return self.feet

    def getPunct(self):
        return self.punct

    def isIgnored(self):
        return '?' in self.stress or '?' in self.weight

    def isLexMono(self):
        return self.numSyll == 1 and self.stress == 'P'

    def getTokenSyll(self):
        return ('.').join([ str(syll) for syll in self.children ])

    def getNumSyll(self):
        return len(self.children)

    def isMonoSyllab(self):
        return self.getNumSyll() == 1

    def isPolySyllab(self):
        return self.getNumSyll() > 1

    def get_unstressed_variant(self):
        new_ipa = self.ipa.replace("'", '').replace('`', '')
        return self.get_word_variant(new_ipa)

    def get_stressed_variant(self, stress_pattern=None):
        if not stress_pattern:
            if len(self.children) == 1:
                stress_pattern = [
                 'P']
            else:
                print (
                 '!! cannot force stressed variant to polysyllabic word', self, 'without a stress pattern set')
                return
        if len(stress_pattern) != len(self.children):
            print (
             '!! stress_pattern', stress_pattern, 'does not match # sylls of this word:', len(self.children), self.children)
            return
        if len(stress_pattern) != len(self.ipa.split('.')):
            print (
             '!! stress_pattern', stress_pattern, 'does not match # sylls of this word:', len(self.children), self.children)
            return
        new_stress_pattern = []
        for x in stress_pattern:
            if x in ('P', 'S', 'U'):
                new_stress_pattern += [x]
            elif x in ('1', 1, 1.0):
                new_stress_pattern += ['P']
            elif x in ('2', 2, 2.0):
                new_stress_pattern += ['S']
            elif x in ('0', 0, 0.0):
                new_stress_pattern += ['U']

        stress_pattern = new_stress_pattern
        newipa = []
        for i, x in enumerate(self.ipa.replace("'", '').replace('`', '').split('.')):
            stress = stress_pattern[i]
            if stress == 'P':
                newipa += ["'" + x]
            elif stress == 'S':
                newipa += ['`' + x]
            else:
                newipa += [x]

        newipa = ('.').join(newipa)
        return self.get_word_variant(newipa)

    def get_word_variant(self, stressedipa):
        from Dictionary import stressedipa2stress, getStrengthStress
        from Syllable import Syllable
        stress = stressedipa2stress(stressedipa)
        prom_stress, prom_strength = getStrengthStress(stress)
        syllphons = [ tuple(child.phonemes()) for child in self.children ]
        syllbodies = self.syllableBodies()
        sylls = []
        for i in range(len(syllphons)):
            syllbody = syllbodies[i]
            syll = Syllable((syllbody, prom_strength[i], prom_stress[i]), lang=self.lang, token=self.sylls_text[i])
            sylls.append(syll)

        word = Word(self.token, sylls, self.sylls_text)
        word.ipa = stressedipa
        word.stress = stress
        word.lang = self.lang
        if not word.ipa:
            word.broken = True
        return word