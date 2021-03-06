# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiio/model.py
# Compiled at: 2016-09-30 16:40:03
import random, iverbs
from cantools import db
POS = {'JJ': 'adj', 'VB': 'v', 'NN': 'n'}
IRR = {'be': {'root': 'be', 
          'first': 'am', 
          'second': 'are', 
          'third': 'is', 
          'past': 'was', 
          'gerund': 'being'}, 
   'have': {'root': 'have', 
            'first': 'have', 
            'second': 'have', 
            'third': 'has', 
            'past': 'had', 
            'gerund': 'having'}}
IRR['am'] = IRR['be']
IRR['are'] = IRR['be']
IRR['is'] = IRR['be']
IRR['was'] = IRR['be']
IRR['being'] = IRR['be']
IRR['has'] = IRR['have']
IRR['had'] = IRR['have']
IRR['having'] = IRR['have']
VMAP = {'VB': 'first', 
   'VBP': 'second', 
   'VBZ': 'third', 
   'VBD': 'past', 
   'VBN': 'participle', 
   'VBG': 'gerund'}
NEGS = {'first': "don't", 
   'second': "don't", 
   'third': "doesn't", 
   'past': "didn't", 
   'gerund': 'not'}
IPP = {}
for line in iverbs.IV.split('\n'):
    v, p, pp = line.split('\t')
    IPP[v] = IPP[p] = IPP[pp] = {'past': p, 
       'participle': pp}

class Symbol(db.TimeStampedBase):

    def meanings(self, count=False):
        q = Meaning.query(Meaning.synonyms.contains(self.key.urlsafe()))
        if count:
            return q.count()
        return q.all()

    def meaning(self):
        q = Meaning.query(Meaning.synonyms.contains(self.key.urlsafe()))
        r = q.fetch(1, random.randint(q.count()))
        return r and r[0]

    def opposite(self):
        q = Meaning.query(Meaning.antonyms.contains(self.key.urlsafe()))
        r = q.fetch(1, random.randint(q.count()))
        return r and r[0]


class Word(Symbol):
    word = db.String()

    def content(self):
        return self.word

    def negate(self, pos):
        if pos.startswith('VB'):
            if self.word in IRR:
                return '%s not' % (self.word,)
            return '%s %s' % (NEGS[VMAP[pos]], self.word)
        if pos.startswith('JJ'):
            return 'not %s' % (self.word,)

    def root(self):
        w = IRR.get(self.word)
        if w:
            return w['root']
        w = self.word
        if w.endswith('ed'):
            w = w[:-2]
        if w.endswith('ing'):
            w = w[:-3]
        return w

    def first(self):
        w = IRR.get(self.word)
        return w and w['first'] or self.root()

    def second(self):
        w = IRR.get(self.word)
        return w and w['second'] or self.root()

    def third(self):
        w = IRR.get(self.word)
        r = self.root()
        return w and w['third'] or r.endswith('s') and r or '%ss' % (r,)

    def gerund(self):
        w = IRR.get(self.word)
        r = self.root()
        return w and w['gerund'] or r.endswith('e') and '%sing' % (r[:-1],) or '%sing' % (r,)

    def past(self):
        w = IRR.get(self.word) or IPP.get(self.word)
        r = self.root()
        return w and w['past'] or r.endswith('e') and '%sd' % (r,) or '%sed' % (r,)

    def participle(self):
        w = IPP.get(self.word)
        return w and w['participle'] or self.past()

    def conjugate(self, part):
        return getattr(self, VMAP[part])()

    def parts(self):
        return {'root': self.root(), 
           'first': self.first(), 
           'second': self.second(), 
           'third': self.third(), 
           'gerund': self.gerund(), 
           'past': self.past()}


class Phrase(Symbol):
    words = db.ForeignKey(kind=Word, repeated=True)
    phrase = db.String()

    def content(self):
        return self.phrase


class Idea(Symbol):
    expressions = db.ForeignKey(kinds=[Word, Phrase], repeated=True)

    def content(self):
        return self.expressions[random.randint(0, len(self.expressions) - 1)].get().content()


class Meaning(db.TimeStampedBase):
    synonyms = db.ForeignKey(kinds=[Word, Phrase, Idea], repeated=True)
    antonyms = db.ForeignKey(kinds=[Word, Phrase, Idea], repeated=True)
    part = db.String(default='n')
    definition = db.Text()

    def content(self):
        return self.definition


class Object(Idea):
    name = db.String()
    qualifiers = db.ForeignKey(kinds=[Word, Phrase, Idea], repeated=True)
    summary = db.String()
    description = db.Text()

    def content(self):
        return self.summary


class Place(Object):
    location = db.ForeignKey(kind='place')


class Event(Object):
    location = db.ForeignKey(kind=Place)
    moment = db.DateTime()


class Person(Object):
    birth = db.ForeignKey(kind=Event)
    residence = db.ForeignKey(kind=Place)

    def content(self):
        return self.qualifiers and random.choice(self.qualifiers).get().content() or self.summary or self.description or self.name


class Thing(Object):
    purpose = db.ForeignKey(kind=Idea)


class Action(Object):
    verbs = db.ForeignKey(kinds=[Word, Phrase])


class Emotion(Idea):
    emotion = db.ForeignKey(kind=Word)


class Reason(Object):
    person = db.ForeignKey(kind=Person)
    reason = db.ForeignKey(kind=Phrase)

    def content(self):
        if self.person:
            return '%s says %s because %s' % (self.person.name, self.name, self.reason.content())
        return '%s because %s' % (self.name, self.reason.content())


class Method(Action):
    action = db.ForeignKey(kind=Action)
    rationale = db.ForeignKey(kind=Reason)


class Strategy(Object):
    methods = db.ForeignKey(kind=Method, repeated=True)


class Affinity(db.TimeStampedBase):
    person = db.ForeignKey(kind=Person)
    idea = db.ForeignKey(kind=Idea)
    value = db.Float()


class Question(db.TimeStampedBase):
    phrase = db.ForeignKey(kind=Phrase)
    answers = db.ForeignKey(kinds=[Word, Phrase, Idea, Meaning, Object, Person], repeated=True)