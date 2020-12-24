# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/Lipsum.py
# Compiled at: 2015-05-06 05:03:08
"""A simple Lorem ipsum generator.

$Id: Lipsum.py 24649 2005-08-29 14:20:19Z bdelbosc $
"""
import random
V_ASCII = ('ad', 'aquam', 'albus', 'archaeos', 'arctos', 'argentatus', 'arvensis',
           'australis', 'biscortborealis', 'brachy', 'bradus', 'brevis', 'campus',
           'cauda', 'caulos', 'cephalus', 'chilensis', 'chloreus', 'cola', 'cristatus',
           'cyanos', 'dactylus', 'deca', 'dermis', 'delorum', 'di', 'diplo', 'dodeca',
           'dolicho', 'domesticus', 'dorsum', 'dulcis', 'echinus', 'ennea', 'erythro',
           'familiaris', 'flora', 'folius', 'fuscus', 'fulvus', 'gaster', 'glycis',
           'hexa', 'hortensis', 'it', 'indicus', 'lateralis', 'leucus', 'lineatus',
           'lipsem', 'lutea', 'maculatus', 'major', 'maximus', 'melanus', 'minimus',
           'minor', 'mono', 'montanus', 'morphos', 'mauro', 'niger', 'nona', 'nothos',
           'notos', 'novaehollandiae', 'novaeseelandiae', 'noveboracensis', 'obscurus',
           'occidentalis', 'octa', 'oeos', 'officinalis', 'oleum', 'orientalis',
           'ortho', 'pachys', 'palustris', 'parvus', 'pedis', 'pelagius', 'penta',
           'petra', 'phyllo', 'phyton', 'platy', 'pratensis', 'protos', 'pteron',
           'punctatus', 'rhiza', 'rhytis', 'rubra', 'rostra', 'rufus', 'sativus',
           'saurus', 'sinensis', 'stoma', 'striatus', 'silvestris', 'sit', 'so',
           'tetra', 'tinctorius', 'tomentosus', 'tres', 'tris', 'trich', 'thrix',
           'unus', 'variabilis', 'variegatus', 'ventrus', 'verrucosus', 'via', 'viridis',
           'vitis', 'volans', 'vulgaris', 'xanthos', 'zygos')
V_DIAC = ('acanth', 'acro', 'actino', 'adelphe', b'ad\xe9no', b'a\xe9ro', 'agogue',
          'agro', 'algie', 'allo', 'amphi', 'andro', 'anti', 'anthropo', 'aqui',
          b'arch\xe9o', 'archie', 'auto', 'bio', 'calli', 'cephal', 'chiro', 'chromo',
          'chrono', 'dactyle', b'd\xe9mo', 'eco', 'eudaimonia', b'\xeathos', b'g\xe9o',
          'glyphe', 'gone', 'gramme', 'graphe', b'hi\xe9ro', 'homo', 'iatrie', 'lipi',
          'lipo', 'logie', 'lyco', 'lyse', 'machie', b'm\xe9lan', b'm\xe9ta', 'naute',
          b'n\xe8se', 'pedo', 'phil', 'phobie', 'podo', 'polis', 'poly', 'rhino',
          'xeno', 'zoo')
V_8859_15 = (b'j\xe0c\xe1nth', b'z\xe2cr\xf6', b'b\xe3ctin\xf5', b'z\xe4delphe', b'k\xe5d\xe9n\xf4',
             b'z\xe6r\xf3', b'ag\xf2gu\xea', b'algi\xeb', b'all\xf0', 'amphi', b'a\xf1dro',
             b'a\xf1ti', b'aq\xfai', b'a\xf9t\xf8', b'bi\xf8', b'ca\xdfi', b'\xe7ephal',
             b'l\xfdco', b'r\xfft\xf8\xf1', b'o\xfei\xdf', 'es', 'du', 'de', 'le',
             'as', 'us', 'i', 'ave', b'ov \xbc', b'zur \xbd', b'ab \xbe')
CHARS = 'abcdefghjkmnopqrstuvwxyz123456789'
SEP = ',,,,,,,,,,;?!'

class Lipsum:
    """Kind of Lorem ipsum generator."""

    def __init__(self, vocab=V_ASCII, chars=CHARS, sep=SEP):
        self.vocab = vocab
        self.chars = chars
        self.sep = sep

    def getWord(self):
        """Return a random word."""
        return random.choice(self.vocab)

    def getUniqWord(self, length_min=None, length_max=None):
        """Generate a kind of uniq identifier."""
        length_min = length_min or 5
        length_max = length_max or 9
        length = random.randrange(length_min, length_max)
        chars = self.chars
        return ('').join([ random.choice(chars) for i in range(length) ])

    def getSubject(self, length=5, prefix=None, uniq=False, length_min=None, length_max=None):
        """Return a subject of length words."""
        subject = []
        if prefix:
            subject.append(prefix)
        if uniq:
            subject.append(self.getUniqWord())
        if length_min and length_max:
            length = random.randrange(length_min, length_max + 1)
        for i in range(length):
            subject.append(self.getWord())

        return (' ').join(subject).capitalize()

    def getSentence(self):
        """Return a random sentence."""
        sep = self.sep
        length = random.randrange(5, 20)
        sentence = [ self.getWord() for i in range(length) ]
        for i in range(random.randrange(0, 3)):
            sentence.insert(random.randrange(length - 4) + 2, random.choice(sep))

        sentence = (' ').join(sentence).capitalize() + '.'
        sentence = sentence.replace(' ,', ',')
        sentence = sentence.replace(',,', ',')
        return sentence

    def getParagraph(self, length=4):
        """Return a paragraph."""
        return (' ').join([ self.getSentence() for i in range(length) ])

    def getMessage(self, length=7):
        """Return a message paragraph length."""
        return ('\n\n').join([ self.getParagraph() for i in range(random.randrange(3, length))
                             ])

    def getPhoneNumber(self, lang='fr', format='medium'):
        """Return a random Phone number."""
        if lang == 'en_US':
            num = []
            num.append('%3.3i' % random.randrange(0, 999))
            num.append('%4.4i' % random.randrange(0, 9999))
            if format == 'short':
                return ('-').join(num)
            num.insert(0, '%3.3i' % random.randrange(0, 999))
            if format == 'medium':
                return '(%s) %s-%s' % tuple(num)
            return '+00 1 (%s) %s-%s' % tuple(num)
        num = [
         '07']
        for i in range(4):
            num.append('%2.2i' % random.randrange(0, 99))

        if format == 'medium':
            return (' ').join(num)
        if format == 'long':
            num[0] = '(0)7'
            return '+33 ' + (' ').join(num)
        return ('').join(num)

    def getAddress(self, lang='fr'):
        """Return a random address."""
        return '%i %s %s\n%5.5i %s' % (
         random.randrange(1, 100),
         random.choice(['rue', 'avenue', 'place', 'boulevard']),
         self.getSubject(length_min=1, length_max=3),
         random.randrange(99000, 99999),
         self.getSubject(length_min=1, length_max=2))


def main():
    """Testing."""
    print 'Word: %s\n' % Lipsum().getWord()
    print 'UniqWord: %s\n' % Lipsum().getUniqWord()
    print 'Subject: %s\n' % Lipsum().getSubject()
    print 'Subject uniq: %s\n' % Lipsum().getSubject(uniq=True)
    print 'Sentence: %s\n' % Lipsum().getSentence()
    print 'Paragraph: %s\n' % Lipsum().getParagraph()
    print 'Message: %s\n' % Lipsum().getMessage()
    print 'Phone number: %s\n' % Lipsum().getPhoneNumber()
    print 'Phone number fr short: %s\n' % Lipsum().getPhoneNumber(lang='fr', format='short')
    print 'Phone number fr medium: %s\n' % Lipsum().getPhoneNumber(lang='fr', format='medium')
    print 'Phone number fr long: %s\n' % Lipsum().getPhoneNumber(lang='fr', format='long')
    print 'Phone number en_US short: %s\n' % Lipsum().getPhoneNumber(lang='en_US', format='short')
    print 'Phone number en_US medium: %s\n' % Lipsum().getPhoneNumber(lang='en_US', format='medium')
    print 'Phone number en_US long: %s\n' % Lipsum().getPhoneNumber(lang='en_US', format='long')
    print 'Address default: %s' % Lipsum().getAddress()


if __name__ == '__main__':
    main()