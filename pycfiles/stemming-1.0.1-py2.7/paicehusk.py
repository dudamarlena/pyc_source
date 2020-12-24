# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\stemming\paicehusk.py
# Compiled at: 2010-02-09 13:14:49
"""This module contains an object that implements the Paice-Husk stemming
algorithm.

If you just want to use the standard Paice-Husk stemming rules, use the
module's ``stem()`` function::

    stemmed_word = stem(word)

If you want to use a custom rule set, read the rules into a string where the
rules are separated by newlines, and instantiate the object with the string,
then use the object's stem method to stem words::

    stemmer = PaiceHuskStemmer(my_rules_string)
    stemmed_word = stemmer.stem(word)
"""
import re
from collections import defaultdict

class PaiceHuskStemmer(object):
    """Implements the Paice-Husk stemming algorithm.
    """
    rule_expr = re.compile('\n    ^(?P<ending>\\w+)\n    (?P<intact>[*]?)\n    (?P<num>\\d+)\n    (?P<append>\\w*)\n    (?P<cont>[.>])\n    ', re.UNICODE | re.VERBOSE)
    stem_expr = re.compile('^\\w+', re.UNICODE)

    def __init__(self, ruletable):
        """
        :param ruletable: a string containing the rule data, separated
            by newlines.
        """
        self.rules = defaultdict(list)
        self.read_rules(ruletable)

    def read_rules(self, ruletable):
        rule_expr = self.rule_expr
        rules = self.rules
        for line in ruletable.split('\n'):
            line = line.strip()
            if not line:
                continue
            match = rule_expr.match(line)
            if match:
                ending = match.group('ending')[::-1]
                lastchar = ending[(-1)]
                intact = match.group('intact') == '*'
                num = int(match.group('num'))
                append = match.group('append')
                cont = match.group('cont') == '>'
                rules[lastchar].append((ending, intact, num, append, cont))
            else:
                raise Exception('Bad rule: %r' % line)

    def first_vowel(self, word):
        vp = min([ p for p in [ word.find(v) for v in 'aeiou' ] if p > -1
                 ])
        yp = word.find('y')
        if yp > 0 and yp < vp:
            return yp
        return vp

    def strip_prefix(self, word):
        for prefix in ('kilo', 'micro', 'milli', 'intra', 'ultra', 'mega', 'nano',
                       'pico', 'pseudo'):
            if word.startswith(prefix):
                return word[len(prefix):]

        return word

    def stem(self, word):
        """Returns a stemmed version of the argument string.
        """
        rules = self.rules
        match = self.stem_expr.match(word)
        if not match:
            return word
        stem = self.strip_prefix(match.group(0))
        is_intact = True
        continuing = True
        while continuing:
            pfv = self.first_vowel(stem)
            rulelist = rules.get(stem[(-1)])
            if not rulelist:
                break
            continuing = False
            for ending, intact, num, append, cont in rulelist:
                if stem.endswith(ending):
                    if intact and not is_intact:
                        continue
                    newlen = len(stem) - num + len(append)
                    if pfv == 0 and newlen < 2 or pfv > 0 and newlen < 3:
                        continue
                    is_intact = False
                    stem = stem[:0 - num] + append
                    continuing = cont
                    break

        return stem


defaultrules = '\nai*2.     { -ia > -   if intact }\na*1.      { -a > -    if intact }\nbb1.      { -bb > -b   }\ncity3s.   { -ytic > -ys }\nci2>      { -ic > -    }\ncn1t>     { -nc > -nt  }\ndd1.      { -dd > -d   }\ndei3y>    { -ied > -y  }\ndeec2ss.  { -ceed > -cess }\ndee1.     { -eed > -ee }\nde2>      { -ed > -    }\ndooh4>    { -hood > -  }\ne1>       { -e > -     }\nfeil1v.   { -lief > -liev }\nfi2>      { -if > -    }\ngni3>     { -ing > -   }\ngai3y.    { -iag > -y  }\nga2>      { -ag > -    }\ngg1.      { -gg > -g   }\nht*2.     { -th > -   if intact }\nhsiug5ct. { -guish > -ct }\nhsi3>     { -ish > -   }\ni*1.      { -i > -    if intact }\ni1y>      { -i > -y    }\nji1d.     { -ij > -id   --  see nois4j> & vis3j> }\njuf1s.    { -fuj > -fus }\nju1d.     { -uj > -ud  }\njo1d.     { -oj > -od  }\njeh1r.    { -hej > -her }\njrev1t.   { -verj > -vert }\njsim2t.   { -misj > -mit }\njn1d.     { -nj > -nd  }\nj1s.      { -j > -s    }\nlbaifi6.  { -ifiabl > - }\nlbai4y.   { -iabl > -y }\nlba3>     { -abl > -   }\nlbi3.     { -ibl > -   }\nlib2l>    { -bil > -bl }\nlc1.      { -cl > c    }\nlufi4y.   { -iful > -y }\nluf3>     { -ful > -   }\nlu2.      { -ul > -    }\nlai3>     { -ial > -   }\nlau3>     { -ual > -   }\nla2>      { -al > -    }\nll1.      { -ll > -l   }\nmui3.     { -ium > -   }\nmu*2.     { -um > -   if intact }\nmsi3>     { -ism > -   }\nmm1.      { -mm > -m   }\nnois4j>   { -sion > -j }\nnoix4ct.  { -xion > -ct }\nnoi3>     { -ion > -   }\nnai3>     { -ian > -   }\nna2>      { -an > -    }\nnee0.     { protect  -een }\nne2>      { -en > -    }\nnn1.      { -nn > -n   }\npihs4>    { -ship > -  }\npp1.      { -pp > -p   }\nre2>      { -er > -    }\nrae0.     { protect  -ear }\nra2.      { -ar > -    }\nro2>      { -or > -    }\nru2>      { -ur > -    }\nrr1.      { -rr > -r   }\nrt1>      { -tr > -t   }\nrei3y>    { -ier > -y  }\nsei3y>    { -ies > -y  }\nsis2.     { -sis > -s  }\nsi2>      { -is > -    }\nssen4>    { -ness > -  }\nss0.      { protect  -ss }\nsuo3>     { -ous > -   }\nsu*2.     { -us > -   if intact }\ns*1>      { -s > -    if intact }\ns0.       { -s > -s    }\ntacilp4y. { -plicat > -ply }\nta2>      { -at > -    }\ntnem4>    { -ment > -  }\ntne3>     { -ent > -   }\ntna3>     { -ant > -   }\ntpir2b.   { -ript > -rib }\ntpro2b.   { -orpt > -orb }\ntcud1.    { -duct > -duc }\ntpmus2.   { -sumpt > -sum }\ntpec2iv.  { -cept > -ceiv }\ntulo2v.   { -olut > -olv }\ntsis0.    { protect  -sist }\ntsi3>     { -ist > -   }\ntt1.      { -tt > -t   }\nuqi3.     { -iqu > -   } \nugo1.     { -ogu > -og }\nvis3j>    { -siv > -j  }\nvie0.     { protect  -eiv }\nvi2>      { -iv > -    }\nylb1>     { -bly > -bl }\nyli3y>    { -ily > -y  }\nylp0.     { protect  -ply }\nyl2>      { -ly > -    }\nygo1.     { -ogy > -og }\nyhp1.     { -phy > -ph }\nymo1.     { -omy > -om }\nypo1.     { -opy > -op }\nyti3>     { -ity > -   }\nyte3>     { -ety > -   }\nytl2.     { -lty > -l  }\nyrtsi5.   { -istry > - }\nyra3>     { -ary > -   }\nyro3>     { -ory > -   }\nyfi3.     { -ify > -   }\nycn2t>    { -ncy > -nt }\nyca3>     { -acy > -   }\nzi2>      { -iz > -    }\nzy1s.     { -yz > -ys  }\n'
stem = PaiceHuskStemmer(defaultrules).stem